#!/usr/bin/env python3
"""
dvbp — Dataverse Blueprint toolkit.

One file, standard library only (PyYAML is used for .yaml blueprints when present;
.json blueprints need nothing). Commands:

  validate  <blueprint>                 Lint the model against the rule catalog (DV001..). Exit 1 on errors.
  render    <blueprint> [-o design.md]  Generate the design document (Mermaid ER, catalogs, security matrix).
  compile   <blueprint> [-o plan.json]  Compile to an ordered, idempotent Dataverse Web API deployment plan.
  deploy    <plan.json> --env URL       Execute a plan (dry-run unless --apply). Token: $DATAVERSE_TOKEN or az CLI.
  export    --env URL --prefix p        Reverse-engineer a live environment into a blueprint (brownfield audit).
  diff      <blueprint> <blueprint>     Show drift between two blueprints (e.g. repo vs. exported live env).

Formats: validate supports --format text|json|sarif (SARIF feeds GitHub code scanning annotations on PRs).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

VERSION = "1.0.0"

STANDARD_TABLES = {"account", "contact", "systemuser", "team", "businessunit", "transactioncurrency"}
DUPLICATE_STANDARD_NAMES = {
    "user": "systemuser", "users": "systemuser", "customer": "account", "company": "account",
    "organization": "account", "client": "account", "contact": "contact", "person": "contact",
    "account": "account", "team": "team", "businessunit": "businessunit", "department": "businessunit",
}
COLUMN_TYPES = {"text", "memo", "whole", "decimal", "float", "currency", "bool", "date", "datetime",
                "choice", "choices", "file", "image", "formula", "autonumber", "email", "url", "phone",
                "calculated"}
DATE_TYPES = {"date", "datetime"}
BEHAVIORS = {"dateonly", "userlocal", "tzi"}
DEPTHS = {"-": None, "U": "Basic", "B": "Local", "P": "Deep", "O": "Global"}
PRIVS = ["create", "read", "write", "delete", "append", "appendto", "assign", "share"]
PRIV_TYPE = {"create": "Create", "read": "Read", "write": "Write", "delete": "Delete",
             "append": "Append", "appendto": "AppendTo", "assign": "Assign", "share": "Share"}
REL_BEHAVIORS = {
    "parental":    {"Assign": "Cascade", "Delete": "Cascade", "Merge": "Cascade", "Reparent": "Cascade",
                    "Share": "Cascade", "Unshare": "Cascade", "RollupView": "NoCascade"},
    "referential": {"Assign": "NoCascade", "Delete": "RemoveLink", "Merge": "NoCascade", "Reparent": "NoCascade",
                    "Share": "NoCascade", "Unshare": "NoCascade", "RollupView": "NoCascade"},
    "restrict":    {"Assign": "NoCascade", "Delete": "Restrict", "Merge": "NoCascade", "Reparent": "NoCascade",
                    "Share": "NoCascade", "Unshare": "NoCascade", "RollupView": "NoCascade"},
}
MONEY_HINT = re.compile(r"(amount|price|cost|salary|total|fee|budget|importe|precio|costo|salario|valor|monto)", re.I)
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}

# ---------------------------------------------------------------------------------------------
# Rule catalog (kept in sync with references/rule-catalog.md)
# ---------------------------------------------------------------------------------------------
RULES = {
    "DV001": ("error",   "Default or placeholder publisher prefix (new, cr###) used in a production design"),
    "DV002": ("error",   "Publisher prefix must be 2-8 lowercase alphanumerics starting with a letter"),
    "DV003": ("error",   "Schema name must be <prefix>_PascalCase, ASCII, no spaces or accents"),
    "DV004": ("warning", "Table schema name looks plural; Dataverse table names are singular"),
    "DV005": ("error",   "Custom table duplicates a standard table (reuse account/contact/systemuser/team/businessunit)"),
    "DV006": ("error",   "Table ownership must be explicit (user or organization) - it cannot be changed after creation"),
    "DV007": ("error",   "Table needs a meaningful primary name column (text or autonumber)"),
    "DV008": ("error",   "Date column needs an explicit behavior (dateonly, userlocal, tzi)"),
    "DV009": ("warning", "Two-option yes/no choice should be a Yes/No (bool) column"),
    "DV010": ("error",   "Column references a choice that is not defined"),
    "DV011": ("error",   "A table can be the child in only one Parental relationship"),
    "DV012": ("error",   "Relationship or key references an unknown table or column"),
    "DV013": ("error",   "Integrated table has no alternate key for upsert"),
    "DV014": ("error",   "PII column is not secured by a column security profile"),
    "DV015": ("error",   "Formula mixes date behaviors (userlocal pairs with Now()/Today(); dateonly/tzi with UTCNow()/UTCToday())"),
    "DV016": ("error",   "Text column max length must be 1..4000 (use memo for longer content)"),
    "DV017": ("warning", "Role can set a lookup but lacks Append on the child or AppendTo on the parent"),
    "DV018": ("error",   "Persona has no security role"),
    "DV019": ("warning", "Element has no traceability (source: process | assumed)"),
    "DV020": ("warning", "Legacy calculated column in a new design - use a formula column"),
    "DV021": ("warning", "Monetary-looking column is not of type currency"),
    "DV022": ("warning", "Organization-wide Delete granted to a non-admin role"),
    "DV023": ("error",   "Organization-owned table only supports None or Organization privilege depth"),
    "DV024": ("error",   "N:N relationship with attributes must be an explicit intersect table"),
    "DV025": ("error",   "Duplicate schema name"),
    "DV026": ("warning", "Lookup column schema name should end with 'Id'"),
    "DV027": ("error",   "Unknown column type"),
    "DV028": ("warning", "Role grants access to a table that is not in the blueprint"),
    "DV029": ("info",    "Assumption to confirm with the business before building"),
    "DV030": ("warning", "Table with approvals/compliance data should have auditing enabled"),
}

# ---------------------------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------------------------

def load_blueprint(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml  # type: ignore
        except ImportError:  # pragma: no cover
            sys.exit("PyYAML is not installed: run `pip install pyyaml` or use a .json blueprint.")
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict) or "tables" not in data:
        sys.exit(f"{path}: not a Dataverse blueprint (missing 'tables').")
    return normalize(data)


def normalize(bp: dict) -> dict:
    """YAML 1.1 turns Yes/No/On/Off into booleans; option labels must stay text."""
    fix = lambda o: ("Yes" if o else "No") if isinstance(o, bool) else o
    for ch in bp.get("choices", []) or []:
        ch["options"] = [fix(o) for o in ch.get("options", [])]
    for t in bp.get("tables", []) or []:
        for c in t.get("columns", []) or []:
            if "options" in c:
                c["options"] = [fix(o) for o in c["options"]]
    return bp


def dump(obj, path: str | None):
    payload = json.dumps(obj, indent=2, ensure_ascii=False)
    if path:
        Path(path).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def logical(schema: str) -> str:
    return schema.lower()


def label(text: str, lcid: int) -> dict:
    return {"@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                 "Label": text, "LanguageCode": lcid}]}


def is_ascii_pascal(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Za-z0-9]*", name)) and \
        unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode() == name


# ---------------------------------------------------------------------------------------------
# Model index
# ---------------------------------------------------------------------------------------------

class Model:
    def __init__(self, bp: dict):
        self.bp = bp
        self.prefix = bp.get("publisher", {}).get("prefix", "")
        self.lcid = int(bp.get("language", 1033))
        self.tables = bp.get("tables", []) or []
        self.choices = {c["name"]: c for c in bp.get("choices", []) or []}
        self.rels = bp.get("relationships", []) or []
        self.sec = bp.get("security", {}) or {}
        self.roles = self.sec.get("roles", []) or []
        self.profiles = self.sec.get("column_profiles", []) or []
        self.personas = bp.get("personas", []) or []
        self.by_table = {logical(t["schema"]): t for t in self.tables if t.get("schema")}

    def table_exists(self, name: str) -> bool:
        return logical(name) in self.by_table or logical(name) in STANDARD_TABLES

    def columns(self, t: dict) -> list[dict]:
        return t.get("columns", []) or []

    def column(self, table: str, col: str) -> dict | None:
        t = self.by_table.get(logical(table))
        if not t:
            return None
        prim = t.get("primary") or {}
        if logical(prim.get("schema", "")) == logical(col):
            return {"schema": prim["schema"], "type": "text"}
        for c in self.columns(t):
            if logical(c.get("schema", "")) == logical(col):
                return c
        for r in self.rels:
            if r.get("type", "N:1") != "N:N" and logical(r.get("child", "")) == logical(table) \
                    and logical(r.get("lookup", "")) == logical(col):
                return {"schema": r["lookup"], "type": "lookup"}
        return None

    def option_prefix(self) -> int:
        return int(self.bp.get("publisher", {}).get("option_value_prefix", 10000))


# ---------------------------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------------------------

def validate(bp: dict) -> list[dict]:
    m = Model(bp)
    out: list[dict] = []

    def add(rule, where, msg=None):
        sev, title = RULES[rule]
        out.append({"rule": rule, "severity": sev, "where": where, "message": msg or title})

    # publisher
    p = m.prefix
    if p == "new" or re.fullmatch(r"cr[0-9a-f]{3}", p or ""):
        add("DV001", "publisher.prefix", f"Prefix '{p}' is a default/placeholder prefix; create a custom publisher.")
    if not re.fullmatch(r"[a-z][a-z0-9]{1,7}", p or "") or p.startswith("mscrm"):
        add("DV002", "publisher.prefix")

    seen = defaultdict(int)

    def check_schema(schema: str, where: str, scope: str = "", segmented: bool = False):
        seen[(scope + "." if scope else "") + logical(schema)] += 1
        rest = schema[len(p) + 1:] if schema.startswith(p + "_") else None
        ok = rest is not None and (all(re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", seg) for seg in rest.split("_")) and rest.isascii()
                                   if segmented else is_ascii_pascal(rest))
        if not ok:
            add("DV003", where, f"'{schema}' should look like {p}_PascalCase (ASCII, no spaces/accents).")

    for name, ch in m.choices.items():
        check_schema_choice = name.startswith(p + "_") and re.fullmatch(r"[a-z0-9_]+", name)
        if not check_schema_choice:
            add("DV003", f"choices.{name}", f"Global choice '{name}' should be lowercase '{p}_name'.")
        opts = [str(o if isinstance(o, str) else o.get("label")).strip().lower() for o in ch.get("options", [])]
        if len(opts) == 2 and set(opts) & {"yes", "no", "sí", "si", "true", "false"}:
            add("DV009", f"choices.{name}")
        for o in ch.get("options", []):
            if isinstance(o, dict) and "value" in o and not str(o["value"]).startswith(str(m.option_prefix())):
                add("DV012", f"choices.{name}", f"Option value {o['value']} does not use the publisher option prefix {m.option_prefix()}.")
        if not ch.get("source"):
            add("DV019", f"choices.{name}")

    audit_words = re.compile(r"(approv|aprob|complian|cumplim|audit|inspect|incident|finding|hallazgo|contract|contrato|payment|pago|salary|health|salud)", re.I)

    for t in m.tables:
        ts = t.get("schema", "?")
        where = f"tables.{ts}"
        check_schema(ts, where)
        base = ts.split("_", 1)[-1]
        if re.search(r"[^s]s$", base) and not re.search(r"(us|is|ss|ics|ness|status|news)$", base, re.I):
            add("DV004", where, f"'{ts}' looks plural; use the singular noun.")
        if base.lower() in DUPLICATE_STANDARD_NAMES:
            add("DV005", where, f"'{ts}' duplicates standard table '{DUPLICATE_STANDARD_NAMES[base.lower()]}'.")
        own = t.get("ownership")
        if own not in ("user", "organization"):
            add("DV006", where)
        prim = t.get("primary") or {}
        if not prim.get("schema"):
            add("DV007", where)
        else:
            check_schema(prim["schema"], f"{where}.primary", scope=ts)
            if prim.get("max_length", 100) > 4000:
                add("DV016", f"{where}.primary")
        if not t.get("source"):
            add("DV019", where)
        if t.get("source") == "assumed":
            add("DV029", where, f"Table {ts} is an assumption: confirm with the business.")
        if t.get("integrated") and not t.get("keys"):
            add("DV013", where)
        if audit_words.search(ts + " " + str(t.get("purpose", ""))) and not t.get("audit"):
            add("DV030", where)

        date_cols = {}
        for c in m.columns(t):
            cs = c.get("schema", "?")
            cw = f"{where}.{cs}"
            check_schema(cs, cw, scope=ts)
            typ = c.get("type")
            if typ not in COLUMN_TYPES:
                add("DV027", cw, f"Unknown type '{typ}'.")
                continue
            if typ == "calculated":
                add("DV020", cw)
            if typ in DATE_TYPES:
                b = c.get("behavior")
                if b not in BEHAVIORS:
                    add("DV008", cw)
                date_cols[logical(cs)] = b
                if c.get("display"):
                    date_cols[c["display"].lower()] = b
            if typ in ("choice", "choices") and c.get("choice") not in m.choices:
                if not c.get("options"):
                    add("DV010", cw, f"Choice '{c.get('choice')}' is not defined in choices[] and no local options given.")
            if typ in ("choice", "choices") and c.get("options") and len(c["options"]) == 2:
                lo = {str(o).lower() for o in c["options"]}
                if lo & {"yes", "no", "sí", "si"}:
                    add("DV009", cw)
            if typ in ("text",) and not (1 <= int(c.get("max_length", 100)) <= 4000):
                add("DV016", cw)
            if typ in ("decimal", "float", "whole") and MONEY_HINT.search(cs + " " + str(c.get("display", ""))):
                add("DV021", cw, f"'{cs}' looks monetary; use currency (adds base-currency column).")
            if not c.get("source"):
                add("DV019", cw)
            elif c.get("source") == "assumed":
                add("DV029", cw, f"Column {cs} is an assumption: confirm with the business.")

        for c in m.columns(t):
            if c.get("type") == "formula" and c.get("formula"):
                f = c["formula"]
                refs = {logical(x) for x in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", f)} | \
                       {x.lower() for x in re.findall(r"'([^']+)'", f)}
                refs |= {"createdon", "modifiedon"} & set(re.findall(r"\b(createdon|modifiedon)\b", f.lower()))
                behaviors = {date_cols.get(r) for r in refs if r in date_cols}
                if {"createdon", "modifiedon"} & refs:
                    behaviors.add("userlocal")
                uses_utc = bool(re.search(r"\bUTC(Now|Today)\s*\(", f))
                uses_local = bool(re.search(r"(?<!UTC)\b(Now|Today)\s*\(", f))
                if (uses_utc and "userlocal" in behaviors) or (uses_local and behaviors & {"dateonly", "tzi"}):
                    add("DV015", f"{where}.{c['schema']}")

        for k in t.get("keys", []) or []:
            for kc in k.get("columns", []):
                if not m.column(ts, kc):
                    add("DV012", f"{where}.keys.{k.get('schema')}", f"Key column '{kc}' not found in {ts}.")

    # relationships
    parental_children = defaultdict(list)
    for r in m.rels:
        rs = r.get("schema", "?")
        where = f"relationships.{rs}"
        check_schema(rs, where, segmented=True)
        if r.get("type") == "N:N":
            for tn in r.get("tables", []):
                if not m.table_exists(tn):
                    add("DV012", where, f"Unknown table '{tn}'.")
            if r.get("columns"):
                add("DV024", where)
            continue
        for side in ("parent", "child"):
            if not m.table_exists(r.get(side, "")):
                add("DV012", where, f"Unknown {side} table '{r.get(side)}'.")
        if logical(r.get("child", "")) in STANDARD_TABLES and r.get("behavior") == "parental":
            add("DV011", where, "Standard tables already have a parental parent; use referential.")
        if r.get("behavior") == "parental":
            parental_children[logical(r.get("child", ""))].append(rs)
        if r.get("lookup"):
            check_schema(r["lookup"], f"{where}.lookup", scope=r.get("child", ""))
            if not r["lookup"].endswith("Id"):
                add("DV026", f"{where}.lookup")
        if r.get("behavior") not in ("parental", "referential", "restrict", "custom"):
            add("DV012", where, f"Unknown relationship behavior '{r.get('behavior')}'.")
        if not r.get("source"):
            add("DV019", where)
    for child, rs in parental_children.items():
        if len(rs) > 1:
            add("DV011", f"tables.{child}", f"{child} is child in {len(rs)} parental relationships: {', '.join(rs)}.")

    for name, n in seen.items():
        if n > 1:
            add("DV025", name, f"'{name}' is declared {n} times.")

    # security
    persona_ids = {pp.get("id") for pp in m.personas}
    covered = {r.get("persona") for r in m.roles}
    for pid in persona_ids - covered:
        add("DV018", f"personas.{pid}")
    lookups = [(logical(r["child"]), logical(r["parent"])) for r in m.rels if r.get("type", "N:1") != "N:N"]
    for role in m.roles:
        rn = role.get("name", "?")
        privs = {logical(k): v for k, v in (role.get("privileges") or {}).items()}
        admin = bool(re.search(r"(admin|director|owner|administra)", rn, re.I))
        for tname, pv in privs.items():
            if not m.table_exists(tname):
                add("DV028", f"security.roles.{rn}", f"Role grants on unknown table '{tname}'.")
                continue
            t = m.by_table.get(tname)
            for k, v in (pv or {}).items():
                if v not in DEPTHS:
                    add("DV012", f"security.roles.{rn}.{tname}.{k}", f"Unknown depth '{v}'. Use - U B P O.")
                if t and t.get("ownership") == "organization" and v in ("U", "B", "P"):
                    add("DV023", f"security.roles.{rn}.{tname}.{k}")
            if (pv or {}).get("delete") == "O" and not admin:
                add("DV022", f"security.roles.{rn}.{tname}")
        for child, parent in lookups:
            cp = privs.get(child) or {}
            if cp.get("create", "-") != "-" or cp.get("write", "-") != "-":
                pp = privs.get(parent) or {}
                if parent in STANDARD_TABLES:
                    pp = pp or {"appendto": "assumed"}
                if cp.get("append", "-") == "-" or pp.get("appendto", "-") == "-":
                    add("DV017", f"security.roles.{rn}", f"{rn}: can write {child} but needs Append on {child} and AppendTo on {parent}.")
    secured = {logical(c) for prof in m.profiles for c in prof.get("columns", [])}
    for t in m.tables:
        for c in m.columns(t):
            if c.get("pii") and logical(f"{t['schema']}.{c['schema']}") not in secured:
                add("DV014", f"tables.{t['schema']}.{c['schema']}")
    out.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["rule"], f["where"]))
    return out


def score(findings: list[dict]) -> tuple[int, str]:
    e = sum(1 for f in findings if f["severity"] == "error")
    w = sum(1 for f in findings if f["severity"] == "warning")
    s = max(0, 100 - 12 * e - 3 * w)
    grade = "A" if s >= 90 else "B" if s >= 80 else "C" if s >= 70 else "D" if s >= 50 else "F"
    return s, grade


def to_sarif(findings: list[dict], path: str) -> dict:
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    def line_of(where: str) -> int:
        token = where.split(".")[-1]
        for i, ln in enumerate(lines, 1):
            if token and token in ln:
                return i
        return 1

    level = {"error": "error", "warning": "warning", "info": "note"}
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "dataverse-blueprint", "version": VERSION,
                                "informationUri": "https://github.com/pnp/copilot-prompts/tree/main/samples/skills/dataverse-blueprint",
                                "rules": [{"id": k, "shortDescription": {"text": v[1]},
                                           "defaultConfiguration": {"level": level[v[0]]}} for k, v in RULES.items()]}},
            "results": [{"ruleId": f["rule"], "level": level[f["severity"]],
                         "message": {"text": f"{f['message']} ({f['where']})"},
                         "locations": [{"physicalLocation": {"artifactLocation": {"uri": path},
                                                             "region": {"startLine": line_of(f["where"])}}}]}
                        for f in findings]}]}


def cmd_validate(a):
    bp = load_blueprint(a.blueprint)
    fs = validate(bp)
    s, g = score(fs)
    if a.format == "json":
        dump({"score": s, "grade": g, "findings": fs}, a.output)
    elif a.format == "sarif":
        dump(to_sarif(fs, a.blueprint), a.output)
    else:
        icon = {"error": "✖", "warning": "▲", "info": "ℹ"}
        name = bp.get("solution", {}).get("display_name") or bp.get("solution", {}).get("name", "")
        print(f"Dataverse Blueprint · {name}")
        print(f"Tables {len(bp.get('tables', []))} · Relationships {len(bp.get('relationships', []) or [])} · "
              f"Roles {len((bp.get('security') or {}).get('roles', []) or [])}")
        print("-" * 78)
        for f in fs:
            print(f"{icon[f['severity']]} {f['rule']} {f['severity']:<7} {f['where']}\n    {f['message']}")
        e = sum(1 for f in fs if f["severity"] == "error")
        w = sum(1 for f in fs if f["severity"] == "warning")
        i = sum(1 for f in fs if f["severity"] == "info")
        print("-" * 78)
        print(f"Score {s}/100 · Grade {g} · {e} errors · {w} warnings · {i} assumptions to confirm")
    return 1 if any(f["severity"] == "error" for f in fs) else 0


# ---------------------------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------------------------

def type_label(c: dict, m: Model) -> str:
    t = c.get("type")
    if t == "text":
        return f"Text ({c.get('max_length', 100)})"
    if t == "memo":
        return f"Multiline text ({c.get('max_length', 2000)})"
    if t in DATE_TYPES:
        return f"{'Date only' if t == 'date' else 'Date and time'} · {({'dateonly': 'Date Only', 'userlocal': 'User Local', 'tzi': 'Time-Zone Independent'}).get(c.get('behavior'), '⚠ no behavior')}"
    if t in ("choice", "choices"):
        kind = "Choice" if t == "choice" else "Choices (multi)"
        return f"{kind} → `{c.get('choice')}`" if c.get("choice") else f"{kind} (local)"
    if t == "autonumber":
        return f"Autonumber `{c.get('format')}`"
    if t == "formula":
        return f"Formula ({c.get('returns', 'auto')})"
    if t == "file":
        return f"File (max {c.get('max_kb', 32768)} KB)"
    return {"whole": "Whole number", "decimal": "Decimal", "float": "Float", "currency": "Currency",
            "bool": "Yes/No", "image": "Image", "email": "Text · Email", "url": "Text · URL",
            "phone": "Text · Phone", "calculated": "Calculated (legacy)"}.get(t, str(t))


def mermaid(m: Model) -> str:
    rows = ["erDiagram"]
    used = set()
    for r in m.rels:
        if r.get("type") == "N:N":
            a, b = r["tables"]
            rows.append(f'    {a} }}o--o{{ {b} : "{r.get("schema")}"')
            used |= {a, b}
            continue
        card = "||--o{" if r.get("required") else "|o--o{"
        rows.append(f'    {r["parent"]} {card} {r["child"]} : "{r.get("behavior", "")} · {r.get("lookup", "")}"')
        used |= {r["parent"], r["child"]}
    for t in m.tables:
        cols = [f'        string {t["primary"]["schema"]} "primary name"'] if t.get("primary") else []
        for c in m.columns(t)[:8]:
            mt = {"text": "string", "memo": "string", "whole": "int", "decimal": "decimal", "currency": "money",
                  "bool": "bool", "date": "date", "datetime": "datetime", "choice": "choice", "choices": "choices",
                  "file": "file", "image": "image", "formula": "formula", "autonumber": "string"}.get(c.get("type"), "string")
            flag = ' "PII"' if c.get("pii") else (' UK "alternate key"' if any(c["schema"] in k.get("columns", []) for k in t.get("keys", []) or []) else "")
            cols.append(f'        {mt} {c["schema"]}{flag}')
        rows.append(f'    {t["schema"]} {{\n' + "\n".join(cols) + "\n    }")
    return "\n".join(rows)


def render(bp: dict) -> str:
    m = Model(bp)
    fs = validate(bp)
    s, g = score(fs)
    sol = bp.get("solution", {})
    pub = bp.get("publisher", {})
    L = []
    L.append(f"# {sol.get('display_name', sol.get('name', 'Dataverse model'))} — Data Model Design\n")
    L.append(f"> Generated by `dvbp render` from the blueprint — do not edit by hand. Blueprint score **{s}/100 ({g})**.\n")
    L.append("## 1. Summary\n")
    L.append((bp.get("summary") or "").strip() + "\n")
    L.append(f"- **Solution** `{sol.get('name')}` v{sol.get('version', '1.0.0.0')} · publisher `{pub.get('name')}` (prefix `{m.prefix}_`, option values {m.option_prefix()}xxxx)")
    L.append(f"- **{len(m.tables)} custom tables**, {len(m.choices)} global choices, {len(m.rels)} relationships, {len(m.roles)} security roles\n")

    L.append("## 2. Assumptions & Open Questions\n")
    n = 0
    for a in bp.get("assumptions", []) or []:
        n += 1
        L.append(f"{n}. `[ASSUMED]` {a}")
    for q in bp.get("open_questions", []) or []:
        n += 1
        L.append(f"{n}. `[DECIDE]` {q}")
    for f in fs:
        if f["rule"] == "DV029":
            n += 1
            L.append(f"{n}. `[ASSUMED]` {f['message']}")
    if n == 0:
        L.append("_None._")
    L.append("")

    L.append("## 3. Entity-Relationship Diagram\n")
    L.append("```mermaid\n" + mermaid(m) + "\n```\n")

    L.append("## 4. Table Catalog\n")
    L.append("| Display name | Schema name | Type | Ownership | Primary name column | Purpose | Est. volume/yr | Audit |")
    L.append("|---|---|---|---|---|---|---|---|")
    for t in m.tables:
        prim = t.get("primary") or {}
        pn = f"`{prim.get('schema')}`" + (f" Autonumber `{prim['autonumber']}`" if prim.get("autonumber") else "")
        L.append(f"| {t.get('display')} | `{t['schema']}` | {t.get('type', 'standard').title()} | "
                 f"{'User/Team' if t.get('ownership') == 'user' else 'Organization'} | {pn} | {t.get('purpose', '')} | "
                 f"{t.get('volume', '—')} | {'Yes' if t.get('audit') else 'No'} |")
    L.append("")

    L.append("## 5. Column Dictionary\n")
    for t in m.tables:
        L.append(f"### {t.get('display')} (`{t['schema']}`)\n")
        L.append("| Display name | Schema name | Data type / format | Required | Searchable | Notes |")
        L.append("|---|---|---|---|---|---|")
        for c in m.columns(t):
            notes = c.get("notes", "")
            if c.get("formula"):
                notes = f"`{c['formula']}` " + notes
            if c.get("pii"):
                notes = "🔒 PII · " + notes
            if c.get("source") == "assumed":
                notes = "`[ASSUMED]` " + notes
            L.append(f"| {c.get('display')} | `{c['schema']}` | {type_label(c, m)} | {'Yes' if c.get('required') else 'No'} | "
                     f"{'Yes' if c.get('searchable') else 'No'} | {notes.strip()} |")
        for r in m.rels:
            if r.get("type", "N:1") != "N:N" and r.get("child") == t["schema"]:
                L.append(f"| {r.get('lookup_display', r['parent'])} | `{r['lookup']}` | Lookup → `{r['parent']}` | "
                         f"{'Yes' if r.get('required') else 'No'} | Yes | {r.get('behavior', '').title()} |")
        L.append("")

    L.append("## 6. Choices\n")
    if m.choices:
        L.append("| Choice | Options (label → value) | Used by |")
        L.append("|---|---|---|")
        for name, ch in m.choices.items():
            opts = ", ".join(f"{lbl} {val}" for lbl, val in option_values(ch, m))
            users = [f"`{t['schema']}.{c['schema']}`" for t in m.tables for c in m.columns(t) if c.get("choice") == name]
            L.append(f"| `{name}` | {opts} | {', '.join(users)} |")
    L.append("")

    L.append("## 7. Relationships\n")
    L.append("| Schema name | Type | Parent → Child | Lookup | Behavior | Cascade (Assign/Delete/Reparent/Share) |")
    L.append("|---|---|---|---|---|---|")
    for r in m.rels:
        if r.get("type") == "N:N":
            L.append(f"| `{r['schema']}` | N:N | {r['tables'][0]} ↔ {r['tables'][1]} | — | Native | — |")
            continue
        cc = cascade(r)
        L.append(f"| `{r['schema']}` | 1:N | `{r['parent']}` → `{r['child']}` | `{r.get('lookup')}` | {r.get('behavior', '').title()} | "
                 f"{cc['Assign']}/{cc['Delete']}/{cc['Reparent']}/{cc['Share']} |")
    L.append("")

    L.append("## 8. Alternate Keys\n")
    keys = [(t, k) for t in m.tables for k in t.get("keys", []) or []]
    for t, k in keys:
        L.append(f"- `{t['schema']}.{k['schema']}` on ({', '.join(k['columns'])}) — {k.get('why', 'upsert from external system')}. "
                 "The index builds asynchronously: wait for status **Active** before the first upsert.")
    if not keys:
        L.append("_None (no integrated tables)._")
    L.append("")

    L.append("## 9. Security Model\n")
    L.append("Depth: `—` None · `U` User · `B` Business Unit · `P` Parent:Child BU · `O` Organization. "
             "Order per cell: C R W D A AT Asg Sh.\n")
    if m.roles:
        tnames = sorted({k for r in m.roles for k in (r.get("privileges") or {})}, key=lambda x: x.lower())
        L.append("| Role \\ Table | " + " | ".join(f"`{t}`" for t in tnames) + " |")
        L.append("|---|" + "---|" * len(tnames))
        for r in m.roles:
            cells = []
            for tn in tnames:
                pv = (r.get("privileges") or {}).get(tn) or {}
                cells.append(" ".join((pv.get(p, "-") if pv.get(p, "-") != "-" else "—") for p in PRIVS))
            L.append(f"| **{r['name']}** | " + " | ".join(f"`{c}`" for c in cells) + " |")
        L.append("")
    for prof in m.profiles:
        L.append(f"- **Column security profile `{prof['name']}`** — columns {', '.join(f'`{c}`' for c in prof['columns'])}; "
                 f"read {'✔' if prof.get('read') else '✖'}, create {'✔' if prof.get('create') else '✖'}, update {'✔' if prof.get('update') else '✖'}; "
                 f"granted to {', '.join(prof.get('granted_to', [])) or '—'}")
    for line in m.sec.get("notes", []) or []:
        L.append(f"- {line}")
    L.append("")

    L.append("## 10. Solution & ALM\n")
    alm = bp.get("alm", {}) or {}
    L.append(f"- Unmanaged solution `{sol.get('name')}` in development, **managed** in test/production.")
    for ev in alm.get("environment_variables", []) or []:
        L.append(f"- Environment variable `{ev}`")
    for cr in alm.get("connection_references", []) or []:
        L.append(f"- Connection reference `{cr}`")
    for line in alm.get("notes", []) or []:
        L.append(f"- {line}")
    L.append("- Deploy with `dvbp compile` → `dvbp deploy --apply` (idempotent; every component is added to the solution).")
    L.append("")

    L.append("## 11. Build Checklist\n")
    plan = compile_plan(bp)
    for i, st in enumerate(plan["steps"], 1):
        L.append(f"{i}. [ ] {st['title']}" + (" — **manual**" if st["kind"] == "manual" else ""))
    L.append("")

    L.append("## 12. Risks & Anti-patterns Avoided\n")
    for line in bp.get("anti_patterns_avoided", []) or []:
        L.append(f"- {line}")
    L.append("")
    L.append("## 13. Validation Report\n")
    L.append(f"**Score {s}/100 · Grade {g}**\n")
    if fs:
        L.append("| Rule | Severity | Where | Finding |")
        L.append("|---|---|---|---|")
        for f in fs:
            L.append(f"| {f['rule']} | {f['severity']} | `{f['where']}` | {f['message']} |")
    else:
        L.append("No findings.")
    return "\n".join(L) + "\n"


def option_values(ch: dict, m: Model) -> list[tuple[str, int]]:
    out = []
    for i, o in enumerate(ch.get("options", [])):
        if isinstance(o, dict):
            out.append((o["label"], int(o.get("value", m.option_prefix() * 10000 + i))))
        else:
            out.append((str(o), m.option_prefix() * 10000 + i))
    return out


def cascade(r: dict) -> dict:
    if r.get("behavior") == "custom":
        base = dict(REL_BEHAVIORS["referential"])
        base.update(r.get("cascade") or {})
        return base
    return REL_BEHAVIORS.get(r.get("behavior"), REL_BEHAVIORS["referential"])


def cmd_render(a):
    md = render(load_blueprint(a.blueprint))
    if a.output:
        Path(a.output).write_text(md, encoding="utf-8")
        print(f"Design document written to {a.output}")
    else:
        print(md)
    return 0


# ---------------------------------------------------------------------------------------------
# compile → Web API deployment plan
# ---------------------------------------------------------------------------------------------

def attribute_payload(c: dict, m: Model) -> dict | None:
    lc = m.lcid
    t = c["type"]
    common = {"SchemaName": c["schema"], "DisplayName": label(c.get("display", c["schema"]), lc),
              "Description": label(c.get("notes", "") or c.get("display", ""), lc),
              "RequiredLevel": {"Value": "ApplicationRequired" if c.get("required") else "None",
                                "CanBeChanged": True, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"}}
    if c.get("pii"):
        common["IsSecured"] = True
    if c.get("audit") is False:
        common["IsAuditEnabled"] = {"Value": False, "CanBeChanged": True}
    ns = "Microsoft.Dynamics.CRM."
    if t in ("text", "email", "url", "phone", "autonumber"):
        fmt = {"text": "Text", "email": "Email", "url": "Url", "phone": "Phone", "autonumber": "Text"}[t]
        p = {"@odata.type": ns + "StringAttributeMetadata", "MaxLength": int(c.get("max_length", 100)),
             "FormatName": {"Value": fmt}, **common}
        if t == "autonumber":
            p["AutoNumberFormat"] = c["format"]
        return p
    if t == "memo":
        return {"@odata.type": ns + "MemoAttributeMetadata", "MaxLength": int(c.get("max_length", 2000)),
                "Format": "TextArea", **common}
    if t == "whole":
        return {"@odata.type": ns + "IntegerAttributeMetadata", "Format": "None",
                "MinValue": c.get("min", -2147483648), "MaxValue": c.get("max", 2147483647), **common}
    if t == "decimal":
        return {"@odata.type": ns + "DecimalAttributeMetadata", "Precision": c.get("precision", 2),
                "MinValue": c.get("min", -100000000000), "MaxValue": c.get("max", 100000000000), **common}
    if t == "float":
        return {"@odata.type": ns + "DoubleAttributeMetadata", "Precision": c.get("precision", 2),
                "MinValue": c.get("min", -100000000000), "MaxValue": c.get("max", 100000000000), **common}
    if t == "currency":
        return {"@odata.type": ns + "MoneyAttributeMetadata", "PrecisionSource": 2,
                "MinValue": c.get("min", -922337203685477), "MaxValue": c.get("max", 922337203685477), **common}
    if t == "bool":
        return {"@odata.type": ns + "BooleanAttributeMetadata", "DefaultValue": bool(c.get("default", False)),
                "OptionSet": {"@odata.type": ns + "BooleanOptionSetMetadata",
                              "TrueOption": {"Value": 1, "Label": label(c.get("true_label", "Yes"), lc)},
                              "FalseOption": {"Value": 0, "Label": label(c.get("false_label", "No"), lc)}},
                **common}
    if t in DATE_TYPES:
        beh = {"dateonly": "DateOnly", "userlocal": "UserLocal", "tzi": "TimeZoneIndependent"}[c.get("behavior", "userlocal")]
        return {"@odata.type": ns + "DateTimeAttributeMetadata",
                "Format": "DateOnly" if t == "date" else "DateAndTime",
                "DateTimeBehavior": {"Value": beh}, **common}
    if t in ("choice", "choices"):
        odt = ns + ("PicklistAttributeMetadata" if t == "choice" else "MultiSelectPicklistAttributeMetadata")
        if c.get("choice") in m.choices:
            return {"@odata.type": odt, **common,
                    "GlobalOptionSet@odata.bind": f"/GlobalOptionSetDefinitions(Name='{c['choice']}')"}
        opts = [{"Value": m.option_prefix() * 10000 + i, "Label": label(str(o), lc)} for i, o in enumerate(c.get("options", []))]
        return {"@odata.type": odt, **common,
                "OptionSet": {"@odata.type": ns + "OptionSetMetadata", "IsGlobal": False,
                              "OptionSetType": "Picklist", "Options": opts}}
    if t == "file":
        return {"@odata.type": ns + "FileAttributeMetadata", "MaxSizeInKB": int(c.get("max_kb", 32768)), **common}
    if t == "image":
        return {"@odata.type": ns + "ImageAttributeMetadata", "CanStoreFullImage": True, "IsPrimaryImage": False, **common}
    return None  # formula / calculated → manual step


def compile_plan(bp: dict) -> dict:
    m = Model(bp)
    lc = m.lcid
    sol = bp.get("solution", {})
    pub = bp.get("publisher", {})
    sname = sol.get("name")
    steps: list[dict] = []

    def step(kind, title, method=None, path=None, body=None, exists=None, solution=True, **extra):
        s = {"id": f"S{len(steps) + 1:03d}", "kind": kind, "title": title}
        if method:
            s["request"] = {"method": method, "path": path, "body": body,
                            "headers": {"MSCRM.SolutionUniqueName": sname} if solution and sname else {}}
        if exists:
            s["exists_if"] = exists
        s.update(extra)
        steps.append(s)

    step("publisher", f"Create publisher '{pub.get('name')}' (prefix {m.prefix})", "POST", "publishers",
         {"uniquename": pub.get("name"), "friendlyname": pub.get("display_name", pub.get("name")),
          "customizationprefix": m.prefix, "customizationoptionvalueprefix": m.option_prefix()},
         exists=f"publishers?$select=publisherid&$filter=uniquename eq '{pub.get('name')}'", solution=False)
    step("solution", f"Create unmanaged solution '{sname}'", "POST", "solutions",
         {"uniquename": sname, "friendlyname": sol.get("display_name", sname), "version": sol.get("version", "1.0.0.0"),
          "publisherid@odata.bind": "{{publisher}}"},
         exists=f"solutions?$select=solutionid&$filter=uniquename eq '{sname}'", solution=False)

    for name, ch in m.choices.items():
        step("choice", f"Create global choice {name}", "POST", "GlobalOptionSetDefinitions",
             {"@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata", "Name": name, "IsGlobal": True,
              "OptionSetType": "Picklist", "DisplayName": label(ch.get("display_name", name), lc),
              "Options": [{"Value": v, "Label": label(lbl, lc)} for lbl, v in option_values(ch, m)]},
             exists=f"GlobalOptionSetDefinitions(Name='{name}')")

    for t in m.tables:
        prim = t.get("primary") or {}
        pa = {"@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata", "SchemaName": prim.get("schema"),
              "IsPrimaryName": True, "MaxLength": int(prim.get("max_length", 100)), "FormatName": {"Value": "Text"},
              "DisplayName": label(prim.get("display", "Name"), lc),
              "RequiredLevel": {"Value": "ApplicationRequired" if not prim.get("autonumber") else "None"}}
        if prim.get("autonumber"):
            pa["AutoNumberFormat"] = prim["autonumber"]
        body = {"@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata", "SchemaName": t["schema"],
                "DisplayName": label(t.get("display", t["schema"]), lc),
                "DisplayCollectionName": label(t.get("plural", t.get("display", t["schema"]) + "s"), lc),
                "Description": label(t.get("purpose", ""), lc),
                "OwnershipType": "UserOwned" if t.get("ownership") == "user" else "OrganizationOwned",
                "IsActivity": t.get("type") == "activity", "HasActivities": bool(t.get("timeline", False)),
                "HasNotes": bool(t.get("notes_enabled", False)),
                "IsAuditEnabled": {"Value": bool(t.get("audit")), "CanBeChanged": True},
                "Attributes": [pa]}
        if t.get("type") == "elastic":
            body["TableType"] = "Elastic"
        step("table", f"Create table {t['schema']} ({t.get('ownership')}-owned)", "POST", "EntityDefinitions", body,
             exists=f"EntityDefinitions(LogicalName='{logical(t['schema'])}')?$select=LogicalName")

    for t in m.tables:
        for c in m.columns(t):
            p = attribute_payload(c, m)
            path = f"EntityDefinitions(LogicalName='{logical(t['schema'])}')/Attributes"
            if p is None:
                step("manual", f"Create {c['type']} column {t['schema']}.{c['schema']} in the maker portal: {c.get('formula', '')}".strip())
                continue
            step("column", f"Add column {t['schema']}.{c['schema']} ({type_label(c, m)})", "POST", path, p,
                 exists=f"{path}(LogicalName='{logical(c['schema'])}')?$select=LogicalName")

    for r in m.rels:
        if r.get("type") == "N:N":
            a, b = r["tables"]
            step("relationship", f"Create N:N {r['schema']} ({a} ↔ {b})", "POST", "RelationshipDefinitions",
                 {"@odata.type": "Microsoft.Dynamics.CRM.ManyToManyRelationshipMetadata", "SchemaName": r["schema"],
                  "Entity1LogicalName": logical(a), "Entity2LogicalName": logical(b),
                  "IntersectEntityName": logical(r["schema"])},
                 exists=f"RelationshipDefinitions(SchemaName='{r['schema']}')")
            continue
        body = {"@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata", "SchemaName": r["schema"],
                "ReferencedEntity": logical(r["parent"]), "ReferencingEntity": logical(r["child"]),
                "CascadeConfiguration": cascade(r),
                "Lookup": {"@odata.type": "Microsoft.Dynamics.CRM.LookupAttributeMetadata", "SchemaName": r["lookup"],
                           "DisplayName": label(r.get("lookup_display", r["parent"]), lc),
                           "RequiredLevel": {"Value": "ApplicationRequired" if r.get("required") else "None"}}}
        step("relationship", f"Create {r.get('behavior')} 1:N {r['schema']} ({r['parent']} → {r['child']})", "POST",
             "RelationshipDefinitions", body, exists=f"RelationshipDefinitions(SchemaName='{r['schema']}')")

    for t in m.tables:
        for k in t.get("keys", []) or []:
            path = f"EntityDefinitions(LogicalName='{logical(t['schema'])}')/Keys"
            step("key", f"Create alternate key {t['schema']}.{k['schema']}", "POST", path,
                 {"SchemaName": k["schema"], "DisplayName": label(k.get("display", k["schema"]), lc),
                  "KeyAttributes": [logical(x) for x in k["columns"]]},
                 exists=f"{path}?$select=SchemaName&$filter=SchemaName eq '{k['schema']}'",
                 wait_for_index=f"{path}?$select=EntityKeyIndexStatus&$filter=SchemaName eq '{k['schema']}'")

    for prof in m.profiles:
        step("column_security", f"Create column security profile '{prof['name']}'", "POST", "fieldsecurityprofiles",
             {"name": prof["name"], "description": prof.get("description", "")},
             exists=f"fieldsecurityprofiles?$select=fieldsecurityprofileid&$filter=name eq '{prof['name']}'")
        for col in prof["columns"]:
            tn, cn = col.split(".")
            step("column_permission", f"Grant {prof['name']} on {col}", "POST", "fieldpermissions",
                 {"entityname": logical(tn), "attributelogicalname": logical(cn),
                  "canread": 4 if prof.get("read") else 0, "cancreate": 4 if prof.get("create") else 0,
                  "canupdate": 4 if prof.get("update") else 0,
                  "fieldsecurityprofileid@odata.bind": "{{profile:" + prof["name"] + "}}"},
                 exists=f"fieldpermissions?$select=fieldpermissionid&$filter=entityname eq '{logical(tn)}' and attributelogicalname eq '{logical(cn)}' and _fieldsecurityprofileid_value eq {{{{profile:{prof['name']}}}}}")

    for role in m.roles:
        step("role", f"Create security role '{role['name']}'", "POST", "roles",
             {"name": role["name"], "businessunitid@odata.bind": "/businessunits({{rootbu}})"},
             exists=f"roles?$select=roleid&$filter=name eq '{role['name']}' and _businessunitid_value eq {{{{rootbu}}}}")
        grants = []
        for tn, pv in (role.get("privileges") or {}).items():
            for p, d in (pv or {}).items():
                if DEPTHS.get(d):
                    grants.append({"table": logical(tn), "privilege": PRIV_TYPE[p], "depth": DEPTHS[d]})
        step("role_privileges", f"Grant {len(grants)} privileges to '{role['name']}'", role=role["name"], grants=grants)

    step("publish", "Publish customizations", "POST", "PublishXml",
         {"ParameterXml": "<importexportxml><entities>" +
          "".join(f"<entity>{logical(t['schema'])}</entity>" for t in m.tables) +
          "</entities><optionsets>" + "".join(f"<optionset>{n}</optionset>" for n in m.choices) +
          "</optionsets></importexportxml>"}, solution=False)
    for t in m.tables:
        if t.get("status_reasons"):
            step("manual", f"Configure Status Reason values for {t['schema']}: {', '.join(t['status_reasons'])}")
    for line in (bp.get("alm", {}) or {}).get("manual_steps", []) or []:
        step("manual", line)
    return {"blueprint": sname, "generated_by": f"dvbp {VERSION}", "language": lc, "steps": steps}


def cmd_compile(a):
    bp = load_blueprint(a.blueprint)
    errs = [f for f in validate(bp) if f["severity"] == "error"]
    if errs and not a.force:
        print(f"Refusing to compile: {len(errs)} validation errors. Run `dvbp validate` or pass --force.", file=sys.stderr)
        return 1
    plan = compile_plan(bp)
    dump(plan, a.output)
    if a.output:
        kinds = defaultdict(int)
        for s in plan["steps"]:
            kinds[s["kind"]] += 1
        print(f"Plan with {len(plan['steps'])} steps written to {a.output}: " + ", ".join(f"{v} {k}" for k, v in kinds.items()))
    return 0


# ---------------------------------------------------------------------------------------------
# Web API client (deploy / export)
# ---------------------------------------------------------------------------------------------

class Dataverse:
    def __init__(self, env: str, token: str | None = None):
        self.env = env.rstrip("/")
        self.base = f"{self.env}/api/data/v9.2/"
        self.token = token or os.environ.get("DATAVERSE_TOKEN") or self._az_token()

    def _az_token(self) -> str:
        try:
            return subprocess.check_output(["az", "account", "get-access-token", "--resource", self.env,
                                            "--query", "accessToken", "-o", "tsv"], text=True).strip()
        except Exception:
            sys.exit("No token. Set DATAVERSE_TOKEN or sign in with `az login` (an account with System Customizer or higher).")

    def call(self, method: str, path: str, body=None, headers=None):
        url = path if path.startswith("http") else self.base + urllib.parse.quote(path, safe="/()?$=&',:@{}-_.")
        h = {"Authorization": f"Bearer {self.token}", "Accept": "application/json", "OData-Version": "4.0",
             "OData-MaxVersion": "4.0", "Content-Type": "application/json; charset=utf-8", "Prefer": "return=representation"}
        h.update(headers or {})
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read()
                return resp.status, (json.loads(raw) if raw else {}), dict(resp.headers)
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                return e.code, json.loads(raw), dict(e.headers)
            except Exception:
                return e.code, {"error": {"message": raw.decode(errors="replace")}}, dict(e.headers)

    def get(self, path):
        return self.call("GET", path)


def substitute(obj, ctx: dict):
    s = json.dumps(obj)
    for k, v in ctx.items():
        s = s.replace("{{" + k + "}}", v)
    return json.loads(s)


def cmd_deploy(a):
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    apply = a.apply
    print(f"{'APPLY' if apply else 'DRY-RUN'} · {plan.get('blueprint')} → {a.env} · {len(plan['steps'])} steps")
    dv = Dataverse(a.env) if apply or a.check else None
    ctx: dict[str, str] = {}
    if dv:
        st, js, _ = dv.get("businessunits?$select=businessunitid&$filter=_parentbusinessunitid_value eq null")
        if st == 200 and js.get("value"):
            ctx["rootbu"] = js["value"][0]["businessunitid"]
    manual = []
    for s in plan["steps"]:
        tag = f"[{s['id']}] {s['title']}"
        if s["kind"] == "manual":
            manual.append(s["title"])
            print(f"  ✋ {tag}")
            continue
        if not dv:
            print(f"  · {tag}")
            continue
        if s["kind"] == "role_privileges":
            rid = ctx.get(f"role:{s['role']}")
            privs = []
            for g in s["grants"]:
                st, js, _ = dv.get(f"EntityDefinitions(LogicalName='{g['table']}')?$select=Privileges")
                for p in (js.get("Privileges") or []):
                    if p["PrivilegeType"] == g["privilege"]:
                        privs.append({"PrivilegeId": p["PrivilegeId"], "Depth": g["depth"], "BusinessUnitId": ctx.get("rootbu")})
            if apply and rid:
                st, js, _ = dv.call("POST", f"roles({rid})/Microsoft.Dynamics.CRM.AddPrivilegesRole", {"Privileges": privs})
                print(f"  {'✔' if st < 300 else '✖'} {tag} ({len(privs)} resolved)" + ("" if st < 300 else f" → {js}"))
            else:
                print(f"  · {tag} ({len(privs)} resolved)")
            continue
        req = substitute(s["request"], ctx)
        exists = substitute(s.get("exists_if"), ctx) if s.get("exists_if") else None
        if exists:
            st, js, _ = dv.get(exists)
            found = st == 200 and (js.get("value") is None or len(js.get("value", [])) > 0)
            if found:
                remember(s, js, ctx)
                print(f"  = {tag} (already exists, skipped)")
                continue
        if not apply:
            print(f"  + {tag} (would create)")
            continue
        st, js, hdr = dv.call(req["method"], req["path"], req["body"], req["headers"])
        if st >= 300:
            print(f"  ✖ {tag}\n      {st} {js.get('error', {}).get('message', js)}")
            if not a.continue_on_error:
                return 1
            continue
        remember(s, js, ctx, hdr)
        print(f"  ✔ {tag}")
        if s.get("wait_for_index"):
            print("      alternate key index queued — check EntityKeyIndexStatus becomes Active before upserts")
    if manual:
        print("\nManual steps remaining:")
        for x in manual:
            print(f"  - {x}")
    return 0


def remember(step: dict, js: dict, ctx: dict, hdr: dict | None = None):
    rec = (js.get("value") or [js])[0] if isinstance(js, dict) else {}
    kind = step["kind"]
    if kind == "publisher":
        ctx["publisher"] = f"/publishers({rec.get('publisherid')})"
    elif kind == "role":
        ctx[f"role:{step['title'].split(chr(39))[1]}"] = rec.get("roleid", "")
    elif kind == "column_security":
        ctx[f"profile:{step['title'].split(chr(39))[1]}"] = rec.get("fieldsecurityprofileid", "")


# ---------------------------------------------------------------------------------------------
# export (brownfield) and diff
# ---------------------------------------------------------------------------------------------
TYPE_MAP = {"String": "text", "Memo": "memo", "Integer": "whole", "Decimal": "decimal", "Double": "float",
            "Money": "currency", "Boolean": "bool", "Picklist": "choice", "Virtual": "choices", "File": "file",
            "Image": "image", "Lookup": "lookup", "Customer": "lookup", "Owner": "owner"}


def metadata_to_blueprint(prefix: str, entities: list[dict]) -> dict:
    """Pure transform from Web API metadata JSON to a blueprint (unit-testable offline)."""
    bp = {"blueprint": 1, "solution": {"name": f"{prefix}_exported"}, "publisher": {"prefix": prefix},
          "summary": "Reverse-engineered from a live environment by `dvbp export`.",
          "tables": [], "choices": [], "relationships": [], "security": {"roles": []}}
    rels = {}
    choices = {}
    for e in entities:
        t = {"schema": e["SchemaName"], "display": _lbl(e.get("DisplayName")) or e["SchemaName"],
             "ownership": "user" if e.get("OwnershipType") == "UserOwned" else "organization",
             "audit": bool((e.get("IsAuditEnabled") or {}).get("Value")), "source": "process", "columns": [],
             "keys": [{"schema": k["SchemaName"], "columns": k["KeyAttributes"]} for k in e.get("Keys", [])]}
        dates = {d["LogicalName"]: d for d in e.get("_dates", [])}
        for at in e.get("Attributes", []):
            if not at.get("IsCustomAttribute") or at.get("AttributeOf"):
                continue
            ln = at["LogicalName"]
            if ln == e.get("PrimaryNameAttribute"):
                t["primary"] = {"schema": at["SchemaName"], "display": _lbl(at.get("DisplayName"))}
                if at.get("AutoNumberFormat"):
                    t["primary"]["autonumber"] = at["AutoNumberFormat"]
                continue
            typ = TYPE_MAP.get(at.get("AttributeType"), at.get("AttributeType", "").lower())
            if at.get("AttributeType") == "DateTime":
                d = dates.get(ln, {})
                typ = "date" if d.get("Format") == "DateOnly" else "datetime"
            if typ in ("lookup", "owner"):
                continue
            col = {"schema": at["SchemaName"], "display": _lbl(at.get("DisplayName")) or at["SchemaName"],
                   "type": typ, "required": (at.get("RequiredLevel") or {}).get("Value") == "ApplicationRequired",
                   "source": "process"}
            if at.get("AttributeType") == "DateTime":
                beh = ((dates.get(ln) or {}).get("DateTimeBehavior") or {}).get("Value")
                col["behavior"] = {"DateOnly": "dateonly", "UserLocal": "userlocal", "TimeZoneIndependent": "tzi"}.get(beh)
            if at.get("IsSecured"):
                col["secured"] = True
            if at.get("AutoNumberFormat"):
                col["type"], col["format"] = "autonumber", at["AutoNumberFormat"]
            if at.get("_GlobalOptionSet"):
                col["choice"] = at["_GlobalOptionSet"]["Name"]
                choices[col["choice"]] = {"name": col["choice"], "source": "process",
                                          "options": [{"label": _lbl(o.get("Label")), "value": o["Value"]}
                                                      for o in at["_GlobalOptionSet"].get("Options", [])]}
            t["columns"].append(col)
        bp["tables"].append(t)
        for r in e.get("ManyToOneRelationships", []):
            cc = r.get("CascadeConfiguration") or {}
            beh = "parental" if cc.get("Delete") == "Cascade" and cc.get("Assign") == "Cascade" else \
                  "restrict" if cc.get("Delete") == "Restrict" else \
                  "referential" if cc.get("Delete") == "RemoveLink" and cc.get("Assign") == "NoCascade" else "custom"
            entry = {"schema": r["SchemaName"], "parent": r["ReferencedEntity"], "child": e["SchemaName"],
                     "lookup": r["ReferencingAttribute"], "behavior": beh, "source": "process"}
            if beh == "custom":
                entry["cascade"] = {k: v for k, v in cc.items() if isinstance(v, str)}
            rels[r["SchemaName"]] = entry
    # map logical parent names to schema names when they are custom
    by_logical = {t["schema"].lower(): t["schema"] for t in bp["tables"]}
    for r in rels.values():
        r["parent"] = by_logical.get(r["parent"], r["parent"])
        sch = None
        for e in entities:
            for at in e.get("Attributes", []):
                if at["LogicalName"] == r["lookup"] and e["SchemaName"] == r["child"]:
                    sch = at["SchemaName"]
        r["lookup"] = sch or r["lookup"]
    bp["relationships"] = list(rels.values())
    bp["choices"] = list(choices.values())
    return bp


def _lbl(lbl) -> str:
    try:
        return (lbl.get("UserLocalizedLabel") or lbl["LocalizedLabels"][0])["Label"]
    except Exception:
        return ""


def cmd_export(a):
    dv = Dataverse(a.env)
    p = a.prefix
    st, js, _ = dv.get("EntityDefinitions?$select=LogicalName,SchemaName,DisplayName,OwnershipType,PrimaryNameAttribute,"
                       f"IsAuditEnabled&$filter=IsCustomEntity eq true and startswith(LogicalName,'{p}_')")
    if st != 200:
        print(js, file=sys.stderr)
        return 1
    entities = []
    for e in js["value"]:
        ln = e["LogicalName"]
        base = f"EntityDefinitions(LogicalName='{ln}')"
        e["Attributes"] = dv.get(f"{base}/Attributes?$select=LogicalName,SchemaName,AttributeType,DisplayName,"
                                 "RequiredLevel,IsCustomAttribute,AttributeOf,IsSecured,AutoNumberFormat")[1].get("value", [])
        e["_dates"] = dv.get(f"{base}/Attributes/Microsoft.Dynamics.CRM.DateTimeAttributeMetadata?$select=LogicalName,"
                             "Format,DateTimeBehavior")[1].get("value", [])
        picks = dv.get(f"{base}/Attributes/Microsoft.Dynamics.CRM.PicklistAttributeMetadata?$select=LogicalName"
                       "&$expand=GlobalOptionSet($select=Name,Options)")[1].get("value", [])
        gmap = {x["LogicalName"]: x.get("GlobalOptionSet") for x in picks if x.get("GlobalOptionSet")}
        for at in e["Attributes"]:
            if at["LogicalName"] in gmap and gmap[at["LogicalName"]].get("Name", "").startswith(p + "_"):
                at["_GlobalOptionSet"] = gmap[at["LogicalName"]]
        e["Keys"] = dv.get(f"{base}/Keys?$select=SchemaName,KeyAttributes")[1].get("value", [])
        e["ManyToOneRelationships"] = dv.get(f"{base}/ManyToOneRelationships?$select=SchemaName,ReferencedEntity,"
                                             "ReferencingAttribute,CascadeConfiguration&$filter=IsCustomRelationship eq true")[1].get("value", [])
        entities.append(e)
    bp = metadata_to_blueprint(p, entities)
    text = json.dumps(bp, indent=2, ensure_ascii=False)
    if a.output and a.output.endswith((".yaml", ".yml")):
        import yaml  # type: ignore
        text = yaml.safe_dump(bp, sort_keys=False, allow_unicode=True)
    if a.output:
        Path(a.output).write_text(text, encoding="utf-8")
        print(f"Exported {len(bp['tables'])} tables to {a.output}. Next: dvbp validate {a.output}")
    else:
        print(text)
    return 0


def diff_blueprints(a: dict, b: dict) -> list[str]:
    out = []

    def tmap(bp):
        return {logical(t["schema"]): t for t in bp.get("tables", [])}

    ta, tb = tmap(a), tmap(b)
    for k in sorted(ta.keys() - tb.keys()):
        out.append(f"- table {ta[k]['schema']} only in A")
    for k in sorted(tb.keys() - ta.keys()):
        out.append(f"+ table {tb[k]['schema']} only in B")
    for k in sorted(ta.keys() & tb.keys()):
        x, y = ta[k], tb[k]
        if x.get("ownership") != y.get("ownership"):
            out.append(f"! {x['schema']}: ownership {x.get('ownership')} → {y.get('ownership')} (cannot be changed in place)")
        ca = {logical(c["schema"]): c for c in x.get("columns", [])}
        cb = {logical(c["schema"]): c for c in y.get("columns", [])}
        for c in sorted(ca.keys() - cb.keys()):
            out.append(f"- column {x['schema']}.{ca[c]['schema']} only in A")
        for c in sorted(cb.keys() - ca.keys()):
            out.append(f"+ column {y['schema']}.{cb[c]['schema']} only in B")
        for c in sorted(ca.keys() & cb.keys()):
            for prop in ("type", "behavior", "choice", "required"):
                va, vb = ca[c].get(prop), cb[c].get(prop)
                if prop == "type" and {va, vb} <= {"text", "email", "url", "phone"}:
                    continue
                if va != vb and not (prop == "required" and not va and not vb):
                    out.append(f"~ {x['schema']}.{ca[c]['schema']}: {prop} {va} → {vb}")
        ka = {k_["schema"] for k_ in x.get("keys", []) or []}
        kb = {k_["schema"] for k_ in y.get("keys", []) or []}
        for k_ in sorted(ka ^ kb):
            out.append(f"{'-' if k_ in ka else '+'} key {x['schema']}.{k_} only in {'A' if k_ in ka else 'B'}")
    ra = {r["schema"]: r for r in a.get("relationships", []) or []}
    rb = {r["schema"]: r for r in b.get("relationships", []) or []}
    for k in sorted(ra.keys() - rb.keys()):
        out.append(f"- relationship {k} only in A")
    for k in sorted(rb.keys() - ra.keys()):
        out.append(f"+ relationship {k} only in B")
    for k in sorted(ra.keys() & rb.keys()):
        if ra[k].get("behavior") != rb[k].get("behavior"):
            out.append(f"~ relationship {k}: behavior {ra[k].get('behavior')} → {rb[k].get('behavior')}")
    return out


def cmd_diff(a):
    d = diff_blueprints(load_blueprint(a.a), load_blueprint(a.b))
    print("\n".join(d) if d else "No drift: both blueprints describe the same model.")
    return 1 if d and a.fail_on_drift else 0


# ---------------------------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(prog="dvbp", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"dvbp {VERSION}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("blueprint"); v.add_argument("--format", choices=["text", "json", "sarif"], default="text"); v.add_argument("-o", "--output")
    r = sub.add_parser("render"); r.add_argument("blueprint"); r.add_argument("-o", "--output")
    c = sub.add_parser("compile"); c.add_argument("blueprint"); c.add_argument("-o", "--output"); c.add_argument("--force", action="store_true")
    d = sub.add_parser("deploy"); d.add_argument("plan"); d.add_argument("--env", required=True)
    d.add_argument("--apply", action="store_true", help="actually create components (default is dry-run)")
    d.add_argument("--check", action="store_true", help="dry-run that also checks what already exists in the environment")
    d.add_argument("--continue-on-error", action="store_true")
    e = sub.add_parser("export"); e.add_argument("--env", required=True); e.add_argument("--prefix", required=True); e.add_argument("-o", "--output")
    f = sub.add_parser("diff"); f.add_argument("a"); f.add_argument("b"); f.add_argument("--fail-on-drift", action="store_true")
    a = ap.parse_args(argv)
    return {"validate": cmd_validate, "render": cmd_render, "compile": cmd_compile, "deploy": cmd_deploy,
            "export": cmd_export, "diff": cmd_diff}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
