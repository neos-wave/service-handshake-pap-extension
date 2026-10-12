"""Offline structural and fixture checks. These do not exercise a Poppy server."""
import copy
import json
import unittest
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
EXT = 'dualcx.com/service-handshake'
SCHEMAS = [json.loads(p.read_text()) for p in sorted(ROOT.glob('reference/*.json'))]
SCHEMAS.append(json.loads((ROOT/'schema/sh-poppy-extension.schema.json').read_text()))
SID = SCHEMAS[-1]['$id']
REGISTRY = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in SCHEMAS)

def read(name):
    return json.loads((ROOT/'examples'/name).read_text())

def record(name):
    return read(name)['message']['data'][EXT]

def validator(definition='messageRecord'):
    return Draft202012Validator({'$ref': SID+'#/$defs/'+definition}, registry=REGISTRY, format_checker=FormatChecker())

def binding_matches(operation):
    binding = operation[EXT]
    return (operation['operation_id'], operation['revision']) == (binding['operation_id'], binding['revision'])

class PackageChecks(unittest.TestCase):
    def reject(self, value, definition='messageRecord'):
        self.assertTrue(list(validator(definition).iter_errors(value)))

    def test_schema_documents_are_valid(self):
        for schema in SCHEMAS:
            with self.subTest(schema=schema['$id']):
                Draft202012Validator.check_schema(schema)

    def test_every_manifest_payload_validates(self):
        for entry in read('manifest.json'):
            with self.subTest(file=entry['file'], definition=entry['definition']):
                value = read(entry['file'])
                for key in entry['pointer']:
                    value = value[key]
                validator(entry['definition']).validate(value)

    def test_manifest_covers_every_json_example(self):
        files = {p.name for p in (ROOT/'examples').glob('*.json')} - {'manifest.json'}
        self.assertEqual(files, {e['file'] for e in read('manifest.json')})

    def test_allow_requires_expiry_and_both_parties(self):
        for field in ['valid_until', 'declaration_refs']:
            value = record('assessment-after-evidence.json')
            del value[field]
            self.reject(value)
        value = record('assessment-after-evidence.json')
        value['declaration_refs'] = value['declaration_refs'][:1]
        self.reject(value)

    def test_hold_can_truthfully_omit_unavailable_declarations(self):
        value = record('assessment-incomplete.json')
        self.assertEqual([], value['declaration_refs'])
        validator().validate(value)
        value['decision'] = 'allow'
        value['valid_until'] = '2026-10-11T12:35:00Z'
        self.reject(value)

    def test_non_allow_requires_explanation(self):
        for decision in ['deny', 'hold', 'escalate']:
            value = record('assessment-hold.json')
            value.update(decision=decision, reasons=[])
            self.reject(value)

    def test_rejects_invented_decisions_and_duplicate_roles(self):
        value = record('assessment-hold.json')
        value['decision'] = 'offer_alternative'
        self.reject(value)
        value = record('assessment-hold.json')
        value['declaration_refs'][1]['party_role'] = 'consumer'
        self.reject(value)

    def test_rejects_unsupported_version_and_revision(self):
        for field, replacement in [('version', '2'), ('draft_revision', '2099-01-01')]:
            value = record('message-declaration.json')
            value[field] = replacement
            self.reject(value)

    def test_declaration_version_is_required_and_authority_shape_preserved(self):
        value = record('family-declaration.json')
        del value['declaration']['declaration_revision']
        self.reject(value)
        value = record('family-declaration.json')
        value['declaration']['authority_level']['configurator_ref'] = 'not-authority'
        self.reject(value)

    def test_concern_cannot_assert_verification(self):
        value = record('relayed-concern.json')
        value['report_status'] = 'verified'
        self.reject(value)

    def test_wrong_record_placement_rejected(self):
        self.reject(record('assessment-hold.json'), 'operationBinding')
        self.reject(read('operation-proposed.json')['operation'][EXT])

    def test_discovery_scope_and_operations_dependency(self):
        for name in ['company-discovery.json', 'client-metadata.json']:
            extensions = read(name)['extensions']
            config = extensions[EXT]
            self.assertTrue(set(config.get('required_actions', [])) <= set(config['actions']))
            if config['operations_binding']:
                self.assertEqual('1', extensions['operations']['version'])

    def test_namespaced_actions_are_structurally_supported(self):
        value = record('assessment-hold.json')
        value['proposal']['action_type'] = 'example.com:retention_offer'
        validator().validate(value)

    def test_operation_binding_and_blocked_confirmation_are_consistent(self):
        operation = read('operation-proposed.json')['operation']
        self.assertTrue(binding_matches(operation))
        altered = copy.deepcopy(operation)
        altered['revision'] = 2
        self.assertFalse(binding_matches(altered))
        blocked = read('confirmation-blocked.json')
        self.assertEqual(operation, blocked['operation'])
        self.assertEqual(operation, read('operation-message.json')['message']['operation'])
        self.assertEqual('proposed', blocked['operation']['state'])
        self.assertIsNone(blocked['operation']['confirmation'])
        self.assertIsNone(blocked['operation']['result'])
        self.assertEqual(record('assessment-hold.json'), blocked[EXT])

    def test_references_resolve_within_case_and_principal_claim_matches(self):
        declarations = {}
        records = []
        for path in (ROOT/'examples').glob('*.json'):
            data = json.loads(path.read_text())
            if not isinstance(data, dict):
                continue
            value = data.get('message', {}).get('data', {}).get(EXT)
            if not value:
                continue
            records.append(value)
            if value['type'] == 'declaration':
                decl = value['declaration']
                key = (value['case_ref'], value['party_role'], decl['declaration_id'], decl['declaration_revision'])
                self.assertNotIn(key, declarations)
                declarations[key] = value
                if 'representation' in value:
                    self.assertEqual(decl['principal_id'], value['representation']['principal_ref'])
        for value in records:
            for link in value.get('declaration_refs', []):
                key = (value['case_ref'], link['party_role'], link['declaration_id'], link['revision'])
                self.assertIn(key, declarations)

    def test_later_allow_uses_revised_declaration_and_does_not_change_offer(self):
        held = record('assessment-hold.json')
        allowed = record('assessment-after-evidence.json')
        self.assertEqual(held['proposal'], allowed['proposal'])
        self.assertEqual(held['assessment_ref'], allowed['supersedes'])
        self.assertNotEqual(held['declaration_refs'], allowed['declaration_refs'])
        self.assertGreater(datetime.fromisoformat(allowed['valid_until']), datetime.fromisoformat(allowed['assessed_at']))
        self.assertEqual(allowed['assessed_at'], read('assessment-after-evidence.json')['created_at'])

if __name__ == '__main__':
    unittest.main()
