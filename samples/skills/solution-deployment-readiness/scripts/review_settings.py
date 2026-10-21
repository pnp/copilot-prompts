#!/usr/bin/env python3
"""Offline deployment-settings comparison. Python standard library only."""
import argparse
import json
from pathlib import Path
import sys

GROUPS = {'EnvironmentVariables': 'SchemaName', 'ConnectionReferences': 'LogicalName'}
PENDING = [
    'Confirm template was generated from the exact solution artifact being deployed.',
    'Verify target connections exist, match their connectors, and are usable by the deployment/flow owner.',
    'Verify target environment variable values/defaults and secret references; do not disclose secrets.',
    'Verify required solution dependencies, versions, privileges, licenses, DLP policy and gateway access.',
    'Perform an authorized sandbox import and smoke test; static settings coverage does not prove deployment success.'
]


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON object key')
            result[key] = value
        return result
    with open(path, encoding='utf-8-sig') as stream:
        return json.load(stream, object_pairs_hook=unique)


def review(template, settings):
    findings = []
    def add(level, code, location, message, fix):
        findings.append(dict(level=level, code=code, location=location, message=message, remediation=fix))
    def index(doc, label):
        result = {}
        if not isinstance(doc, dict):
            add('BLOCKER', 'INVALID_ROOT', label, 'Expected a JSON object.', 'Regenerate or repair the settings file.')
            return {group: {} for group in GROUPS}
        # Missing sections cannot silently produce a clean report.
        for group, key in GROUPS.items():
            rows = doc.get(group)
            items = {}
            if not isinstance(rows, list):
                add('BLOCKER', 'INVALID_SECTION', f'{label}.{group}', 'Expected an array, including an empty array when appropriate.', 'Regenerate a complete settings file.')
                rows = []
            for n, row in enumerate(rows):
                loc = f'{label}.{group}[{n}]'
                if not isinstance(row, dict) or not isinstance(row.get(key), str) or not row[key].strip():
                    add('BLOCKER', 'INVALID_ENTRY', loc, f'Expected a nonempty {key}.', 'Supply the schema/logical name from PAC output.')
                    continue
                name = row[key]
                if name != name.strip():
                    add('BLOCKER', 'INVALID_NAME', loc, 'Name contains surrounding whitespace.', 'Use the exact PAC-generated name.')
                canonical = name.casefold()
                if canonical in items:
                    add('BLOCKER', 'DUPLICATE_NAME', loc, 'Duplicate name; comparison is ambiguous.', 'Keep one mapping per name.')
                    continue
                items[canonical] = (n, row)
            result[group] = items
        return result
    expected, actual = index(template, 'template'), index(settings, 'settings')
    for group, key in GROUPS.items():
        for name, (n, source) in expected[group].items():
            loc = f'template.{group}[{n}]'
            if group == 'ConnectionReferences' and (not isinstance(source.get('ConnectorId'), str) or not source['ConnectorId'].strip()):
                add('BLOCKER', 'INVALID_TEMPLATE_CONNECTOR', loc, 'Template lacks a connector identifier.', 'Regenerate the template from the exact solution.')
            if name not in actual[group]:
                add('REVIEW' if group == 'EnvironmentVariables' else 'BLOCKER', 'MISSING_MAPPING', loc,
                    'No corresponding target settings entry.',
                    'Document verified target/default value evidence or supply a value.' if group == 'EnvironmentVariables' else 'Map to a verified target connection for unattended deployment.')
                continue
            i, row = actual[group][name]
            loc = f'settings.{group}[{i}]'
            if group == 'EnvironmentVariables':
                if 'Value' not in row or not isinstance(row['Value'], str):
                    add('BLOCKER', 'INVALID_VALUE', loc, 'Value must be present as a string.', 'Use the deployment-settings string representation.')
                elif not row['Value'].strip():
                    add('REVIEW', 'EMPTY_VALUE', loc, 'Empty value requires an explicit decision; it may be intentional or a target/default value may apply.', 'Confirm intended effective target value before deployment.')
                elif row['Value'].strip().lower() in {'todo', 'tbd', '<value>', '<target-value>', 'changeme'}:
                    add('REVIEW', 'PLACEHOLDER_VALUE', loc, 'Value resembles an unresolved placeholder.', 'Confirm and replace if unresolved.')
            else:
                value = row.get('ConnectionId')
                if not isinstance(value, str) or not value.strip():
                    add('BLOCKER', 'EMPTY_CONNECTION', loc, 'Target connection identifier is missing.', 'Supply a verified target connection identifier.')
                elif value.strip().lower() in {'todo', 'tbd', '<connection-id>', 'changeme'}:
                    add('BLOCKER', 'PLACEHOLDER_CONNECTION', loc, 'Connection identifier is an unresolved placeholder.', 'Supply a verified target connection identifier.')
                connector = row.get('ConnectorId')
                if not isinstance(connector, str) or not connector.strip():
                    add('BLOCKER', 'EMPTY_CONNECTOR', loc, 'Connector identifier is missing.', 'Copy the connector identifier from the template.')
                elif isinstance(source.get('ConnectorId'), str) and connector.casefold() != source['ConnectorId'].casefold():
                    add('BLOCKER', 'CONNECTOR_MISMATCH', loc, 'Connector differs from the template.', 'Resolve the mismatch using the exact solution and target connection.')
        for name, (i, row) in actual[group].items():
            if name not in expected[group]:
                add('REVIEW', 'EXTRA_MAPPING', f'settings.{group}[{i}]', 'Entry is absent from the template.', 'Check for stale settings or a template from another solution version.')
    status = 'BLOCKED' if any(f['level'] == 'BLOCKER' for f in findings) else 'REVIEW_REQUIRED' if findings else 'STATIC_COVERAGE_COMPLETE'
    return dict(status=status, scope='Offline settings coverage for unattended deployment; no target validation.', findings=findings, unverified=PENDING)


def markdown(report):
    lines = ['# Solution deployment readiness review', '', '**Status: ' + report['status'] + '**', '', report['scope'], '', '| Level | Check | Location | Finding | Remediation |', '|---|---|---|---|---|']
    for f in report['findings']:
        lines.append('| ' + ' | '.join(str(f[k]).replace('|', '\\|').replace('\n', ' ') for k in ('level', 'code', 'location', 'message', 'remediation')) + ' |')
    if not report['findings']:
        lines.append('| — | — | — | No settings coverage issues found. | Complete target verification below. |')
    lines += ['', '## Unverified target checks', ''] + ['- ' + x for x in report['unverified']]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', required=True)
    parser.add_argument('--settings', required=True)
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown')
    args = parser.parse_args()
    try:
        report = review(load(args.template), load(args.settings))
    except (OSError, ValueError, RecursionError):
        print('Input error: cannot read valid, unambiguous JSON settings. No values displayed.', file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.format == 'json' else markdown(report), end='\n')
    return 1 if report['status'] == 'BLOCKED' else 0

if __name__ == '__main__':
    sys.exit(main())
