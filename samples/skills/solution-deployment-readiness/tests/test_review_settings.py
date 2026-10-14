import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checker', ROOT / 'scripts/review_settings.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.template = json.loads((ROOT / 'examples/template.json').read_text())
        self.settings = json.loads((ROOT / 'examples/complete-settings.json').read_text())
    def codes(self, settings=None, template=None):
        return {f['code'] for f in checker.review(self.template if template is None else template, self.settings if settings is None else settings)['findings']}
    def test_complete_still_requires_target_checks(self):
        report = checker.review(self.template, self.settings)
        self.assertEqual(report['status'], 'STATIC_COVERAGE_COMPLETE')
        self.assertTrue(report['unverified'])
    def test_known_incomplete_fixture(self):
        bad = json.loads((ROOT / 'examples/incomplete-settings.json').read_text())
        self.assertEqual(self.codes(bad), {'EMPTY_VALUE','MISSING_MAPPING','EMPTY_CONNECTION','CONNECTOR_MISMATCH'})
        self.assertEqual(checker.review(self.template,bad)['status'],'BLOCKED')
    def test_missing_variable_is_review_not_import_failure(self):
        self.settings['EnvironmentVariables'].pop()
        report = checker.review(self.template,self.settings)
        self.assertEqual(report['status'],'REVIEW_REQUIRED')
    def test_blank_variable_is_review(self):
        self.settings['EnvironmentVariables'][0]['Value']=''
        self.assertEqual(checker.review(self.template,self.settings)['status'],'REVIEW_REQUIRED')
    def test_nonstring_variable(self):
        self.settings['EnvironmentVariables'][0]['Value']=False
        self.assertIn('INVALID_VALUE',self.codes())
    def test_missing_connection(self):
        self.settings['ConnectionReferences']=[]
        self.assertEqual(checker.review(self.template,self.settings)['status'],'BLOCKED')
    def test_duplicate_case_insensitive(self):
        item=copy.deepcopy(self.settings['EnvironmentVariables'][0]);item['SchemaName']=item['SchemaName'].upper()
        self.settings['EnvironmentVariables'].append(item)
        self.assertIn('DUPLICATE_NAME',self.codes())
    def test_extra_mapping(self):
        self.settings['EnvironmentVariables'].append({'SchemaName':'demo_Obsolete','Value':'x'})
        self.assertIn('EXTRA_MAPPING',self.codes())
    def test_invalid_roots(self):
        for value in [None, [], 'x', 5]:
            self.assertIn('INVALID_ROOT', {f['code'] for f in checker.review(self.template, value)['findings']})
    def test_missing_section(self):
        del self.settings['ConnectionReferences']
        self.assertIn('INVALID_SECTION',self.codes())
    def test_invalid_entry(self):
        self.settings['EnvironmentVariables'].append(None)
        self.assertIn('INVALID_ENTRY',self.codes())
    def test_names_case_insensitive(self):
        for group,key in checker.GROUPS.items():
            for item in self.settings[group]: item[key]=item[key].upper()
        self.assertEqual(self.codes(),set())
    def test_connection_placeholder(self):
        self.settings['ConnectionReferences'][0]['ConnectionId']='<connection-id>'
        self.assertIn('PLACEHOLDER_CONNECTION',self.codes())
    def test_bad_template_connector(self):
        self.template['ConnectionReferences'][0]['ConnectorId']=''
        self.assertIn('INVALID_TEMPLATE_CONNECTOR',self.codes())
    def test_no_value_disclosure(self):
        marker='PRIVATE_SECRET_SENTINEL'
        self.settings['EnvironmentVariables'][0]['Value']=marker
        self.settings['ConnectionReferences'][0]['ConnectionId']=marker
        self.settings['ConnectionReferences'][0]['ConnectorId']=marker
        report=checker.review(self.template,self.settings)
        self.assertNotIn(marker,json.dumps(report))
        self.assertNotIn(marker,checker.markdown(report))
    def test_cli_exit_statuses_and_output(self):
        for fixture,code,status in [('complete-settings',0,'STATIC_COVERAGE_COMPLETE'),('incomplete-settings',1,'BLOCKED')]:
            result=subprocess.run([sys.executable,str(ROOT/'scripts/review_settings.py'),'--template',str(ROOT/'examples/template.json'),'--settings',str(ROOT/'examples'/f'{fixture}.json'),'--format','json'],capture_output=True,text=True)
            self.assertEqual(result.returncode,code)
            self.assertEqual(json.loads(result.stdout)['status'],status)
    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'ambiguous.json';file.write_text('{"EnvironmentVariables":[],"EnvironmentVariables":[]}')
            with self.assertRaises(ValueError): checker.load(file)
    def test_malformed_json_cli_does_not_echo_values(self):
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'bad.json';file.write_text('PRIVATE_SECRET_SENTINEL')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/review_settings.py'),'--template',str(file),'--settings',str(file)],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            self.assertNotIn('PRIVATE_SECRET_SENTINEL',result.stderr+result.stdout)
    def test_empty_solution_settings(self):
        empty={'EnvironmentVariables':[],'ConnectionReferences':[]}
        self.assertEqual(checker.review(empty,empty)['status'],'STATIC_COVERAGE_COMPLETE')

if __name__ == '__main__': unittest.main()
