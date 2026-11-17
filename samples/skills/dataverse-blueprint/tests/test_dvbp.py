"""Run: python -m unittest discover -s tests   (from the skill folder)"""
import json, sys, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "scripts"))
import dvbp  # noqa: E402

GOOD = str(HERE / "examples" / "ehs-inspections.blueprint.yaml")
BAD = str(HERE / "examples" / "legacy-tracker.blueprint.yaml")


def rules(bp):
    return {f["rule"] for f in dvbp.validate(bp)}


class ValidateTests(unittest.TestCase):
    def test_good_blueprint_has_no_errors(self):
        fs = dvbp.validate(dvbp.load_blueprint(GOOD))
        self.assertFalse([f for f in fs if f["severity"] == "error"], fs)
        self.assertEqual(dvbp.score(fs), (100, "A"))

    def test_legacy_blueprint_catches_classic_mistakes(self):
        r = rules(dvbp.load_blueprint(BAD))
        for expected in ["DV001", "DV003", "DV005", "DV006", "DV007", "DV008", "DV010", "DV011",
                         "DV013", "DV014", "DV016", "DV018", "DV021", "DV023", "DV017", "DV009"]:
            self.assertIn(expected, r)

    def test_formula_date_pairing(self):
        bp = dvbp.load_blueprint(GOOD)
        col = bp["tables"][2]["columns"][3]
        col["formula"] = col["formula"].replace("Now()", "UTCNow()")
        self.assertIn("DV015", rules(bp))

    def test_yaml_yes_no_options_survive(self):
        bp = dvbp.load_blueprint(BAD)
        self.assertEqual(bp["choices"][0]["options"], ["Yes", "No"])


class CompileTests(unittest.TestCase):
    def setUp(self):
        self.plan = dvbp.compile_plan(dvbp.load_blueprint(GOOD))

    def test_dependency_order(self):
        kinds = [s["kind"] for s in self.plan["steps"]]
        first = {k: kinds.index(k) for k in set(kinds)}
        self.assertLess(first["choice"], first["table"])
        self.assertLess(first["table"], first["column"])
        self.assertLess(first["column"], first["relationship"])
        self.assertLess(first["relationship"], first["key"])
        self.assertLess(first["key"], first["role"])
        self.assertLess(first["role"], first["publish"])

    def test_every_create_is_idempotent(self):
        for s in self.plan["steps"]:
            if s.get("request", {}).get("method") == "POST" and s["kind"] != "publish":
                self.assertIn("exists_if", s, s["title"])

    def test_payload_shapes(self):
        by = {s["title"]: s for s in self.plan["steps"]}
        date = next(s for t, s in by.items() if "cnt_InspectionDate" in t)["request"]["body"]
        self.assertEqual(date["DateTimeBehavior"], {"Value": "DateOnly"})
        rel = next(s for t, s in by.items() if "cnt_Inspection_Finding" in t)["request"]["body"]
        self.assertEqual(rel["CascadeConfiguration"]["Delete"], "Cascade")
        restrict = next(s for t, s in by.items() if "cnt_Site_Inspection" in t)["request"]["body"]
        self.assertEqual(restrict["CascadeConfiguration"]["Delete"], "Restrict")
        pii = next(s for t, s in by.items() if "cnt_ContractorNationalId" in t)["request"]["body"]
        self.assertTrue(pii["IsSecured"])
        auto = next(s for t, s in by.items() if t.startswith("Create table cnt_Inspection"))["request"]["body"]
        self.assertEqual(auto["Attributes"][0]["AutoNumberFormat"], "INS-{SEQNUM:6}")
        for s in self.plan["steps"]:
            if s.get("request") and s["kind"] not in ("publisher", "solution", "publish"):
                self.assertEqual(s["request"]["headers"]["MSCRM.SolutionUniqueName"], "EhsInspections")

    def test_formula_is_manual(self):
        self.assertTrue(any(s["kind"] == "manual" and "cnt_DaysOpen" in s["title"] for s in self.plan["steps"]))


class RenderAndSarifTests(unittest.TestCase):
    def test_render_has_all_sections(self):
        md = dvbp.render(dvbp.load_blueprint(GOOD))
        for h in ["## 1. Summary", "```mermaid", "## 5. Column Dictionary", "## 9. Security Model",
                  "## 11. Build Checklist", "## 13. Validation Report"]:
            self.assertIn(h, md)

    def test_sarif(self):
        s = dvbp.to_sarif(dvbp.validate(dvbp.load_blueprint(BAD)), BAD)
        self.assertEqual(s["version"], "2.1.0")
        self.assertTrue(s["runs"][0]["results"])


class ExportDiffTests(unittest.TestCase):
    def test_metadata_roundtrip_and_drift(self):
        entities = [{
            "SchemaName": "cnt_Site", "LogicalName": "cnt_site", "OwnershipType": "UserOwned",
            "PrimaryNameAttribute": "cnt_name", "IsAuditEnabled": {"Value": True},
            "DisplayName": {"LocalizedLabels": [{"Label": "Site"}]},
            "Attributes": [
                {"LogicalName": "cnt_name", "SchemaName": "cnt_Name", "AttributeType": "String", "IsCustomAttribute": True},
                {"LogicalName": "cnt_erpcode", "SchemaName": "cnt_ErpCode", "AttributeType": "String", "IsCustomAttribute": True,
                 "RequiredLevel": {"Value": "ApplicationRequired"}},
                {"LogicalName": "cnt_openedon", "SchemaName": "cnt_OpenedOn", "AttributeType": "DateTime", "IsCustomAttribute": True}],
            "_dates": [{"LogicalName": "cnt_openedon", "Format": "DateAndTime", "DateTimeBehavior": {"Value": "UserLocal"}}],
            "Keys": [], "ManyToOneRelationships": []}]
        live = dvbp.metadata_to_blueprint("cnt", entities)
        self.assertEqual(live["tables"][0]["primary"]["schema"], "cnt_Name")
        self.assertIn("DV013", rules({**live, "tables": [{**live["tables"][0], "integrated": True}]}))
        drift = dvbp.diff_blueprints(dvbp.load_blueprint(GOOD), live)
        self.assertTrue(any("cnt_City only in A" in d for d in drift))
        self.assertTrue(any("key cnt_Site.cnt_ErpCodeKey" in d for d in drift))
        self.assertTrue(any("cnt_OpenedOn only in B" in d for d in drift))


if __name__ == "__main__":
    unittest.main()
