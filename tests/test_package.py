"""Offline envelope, exchange and scenario checks; no network or running service."""
import copy
import hashlib
import json
import unittest
import tempfile
import shutil
import sys
from unittest.mock import patch
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from fixture_checks import (check_message_semantics, check_fixture_negotiation,
    check_fixture_lifecycle, check_handover_continuity, check_operation_bindings,
    parse_extensions_header)

ROOT=Path(__file__).resolve().parents[1]
EXT='dualcx.com/service-handshake'
BASE='https://personalagentprotocol.org/kit/company/schemas/'
SID='urn:dualcx:service-handshake:poppy:3:draft:2026-11-25'
SCHEMAS=[json.loads(p.read_text()) for p in sorted(ROOT.glob('reference/*.json'))]
SCHEMAS.append(json.loads((ROOT/'schema/sh-poppy-extension.schema.json').read_text()))
FIXTURE_SCHEMA=json.loads((ROOT/'tests/fixture-context.schema.json').read_text())
SCHEMAS.append(FIXTURE_SCHEMA)
POPPY={p.name:json.loads(p.read_text()) for p in (ROOT/'reference/poppy').glob('*.json')}
REGISTRY=Registry().with_resources([(s['$id'],Resource.from_contents(s)) for s in SCHEMAS]+[(BASE+n,Resource.from_contents(s)) for n,s in POPPY.items()])
def raw_example(name):
    try:
        return json.loads((ROOT/'examples'/name).read_text())
    except json.JSONDecodeError as error:
        raise AssertionError(f"{name}: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}") from None
    except OSError as error:
        raise AssertionError(f"{name}: cannot read example: {error.strerror}") from None

def field_path(keys):
    path='$'
    for key in keys:
        path += '.'+key if isinstance(key,str) and key.isidentifier() else '['+json.dumps(key)+']'
    return path

def fixture_value(name,value,pointer):
    current=value
    for i,key in enumerate(pointer):
        exists=(isinstance(current,dict) and key in current) or (isinstance(current,list) and isinstance(key,int) and 0<=key<len(current))
        if not exists:
            expected=field_path(pointer)
            raise AssertionError(f"{name}: missing {field_path(pointer[:i+1])}; expected content at {expected}. Check the example manifest and current message placement.") from None
        current=current[key]
    return current

def assert_valid_fixture(name,value,check,label):
    error=next(check.iter_errors(value),None)
    if error is not None:
        detail=error.message if error.validator=='required' else f"does not satisfy {error.validator}"
        raise AssertionError(f"{name}: {field_path(error.absolute_path)} {detail} ({label}). Correct the fixture before running scenario checks.")

def read(name):
    value=raw_example(name)
    if name=='manifest.json':
        return value
    entry=next((e for e in raw_example('manifest.json') if e['file']==name),None)
    if entry is None:
        raise AssertionError(f"{name}: example is not listed in manifest.json.")
    msg=value.get('message',{}) if isinstance(value,dict) else {}
    if isinstance(msg,dict):
        data=msg.get('data',{})
        if isinstance(data,dict) and EXT in data:
            raise AssertionError(f'{name}: legacy SH placement at $.message.data["{EXT}"]. Move the record to $.message.extensions["{EXT}"].')
        for key in ('operation','approval','declined'):
            if key in msg:
                raise AssertionError(f"{name}: legacy $.message.{key}. Move it to $.message.extensions.operations.{key}.")
    if 'pointer' in entry:
        nested=fixture_value(name,value,entry['pointer'])
        assert_valid_fixture(name,nested,validator(entry['definition']),entry['definition'])
    if 'base_schema' in entry:
        assert_valid_fixture(name,value,base_validator(entry['base_schema']),entry['base_schema'])
    elif entry.get('fixture_schema')=='request-context':
        assert_valid_fixture(name,value,Draft202012Validator(FIXTURE_SCHEMA,registry=REGISTRY,format_checker=FormatChecker()),'offline request context')
    else:
        raise AssertionError(f'{name}: no recognised schema in manifest.json.')
    if isinstance(value,dict) and 'message' in value:
        try:
            check_message_semantics(value)
        except (ValueError,KeyError,TypeError) as error:
            raise AssertionError(f"{name}: invalid message placement or binding: {error}. Check message.extensions and the matching operation reference.") from None
    return value

def record(name):
    return fixture_value(name,read(name),['message','extensions',EXT])
def validator(definition='messageRecord'):return Draft202012Validator({'$ref':SID+'#/$defs/'+definition},registry=REGISTRY,format_checker=FormatChecker())
def base_validator(name):return Draft202012Validator({'$ref':BASE+name},registry=REGISTRY,format_checker=FormatChecker())
def records():
    return [record(e['file']) for e in read('manifest.json') if e.get('definition')=='messageRecord']


class PackageChecks(unittest.TestCase):
    def reject(self,value,definition='messageRecord'):self.assertTrue(list(validator(definition).iter_errors(value)))

    def test_schema_documents(self):
        for s in SCHEMAS+list(POPPY.values()):Draft202012Validator.check_schema(s)

    def test_complete_upstream_envelopes(self):
        for e in read('manifest.json'):
            with self.subTest(file=e['file']):
                v=read(e['file'])
                if 'base_schema' in e:assert_valid_fixture(e['file'],v,base_validator(e['base_schema']),e['base_schema'])
                if 'message' in v:check_message_semantics(v)

    def test_extension_payloads(self):
        for e in read('manifest.json'):
            if 'definition' not in e:continue
            with self.subTest(file=e['file']):
                v=fixture_value(e['file'],read(e['file']),e['pointer'])
                assert_valid_fixture(e['file'],v,validator(e['definition']),e['definition'])

    def test_wire_wrappers_accept_additive_metadata_without_changing_known_fields(self):
        assessment=record('replacement-hold.json')
        assessment['adapter_note']={'label':'review example'}
        assessment['proposal']['display_hint']='compact'
        assessment['proposal']['operation']['display_hint']='opaque reference'
        assessment['reasons'][0]['translation_hint']='en-GB'
        assessment['declaration_refs'][0]['display_hint']='customer'
        validator().validate(assessment)
        self.assertEqual('hold',assessment['decision'])
        declaration=record('family-declaration.json');declaration['adapter_note']='harmless extra field'
        declaration['representation']['display_hint']='case-scoped references'
        validator().validate(declaration)
        company=read('company-discovery.json')['extensions'][EXT][0]
        company['display_metadata']={'label':'Service Handshake'}
        validator('companyConfig').validate(company)

    def test_additive_fields_do_not_replace_required_known_fields(self):
        value=record('replacement-hold.json');value['alternate_decision']='allow';del value['decision']
        self.reject(value)
        value=record('family-declaration.json');value['authority_verified']=True
        value['declaration']['authority_level']['unrecognised_permission']='execute_anything'
        self.reject(value)

    def test_local_support_is_strict_non_wire_configuration(self):
        value=read('request-negotiation.json')['local_support'][EXT]
        value['unknown_setting']=True
        self.reject(value,'localSupport')

    def test_manifest_covers_each_json_once(self):
        names=[e['file'] for e in read('manifest.json')]
        self.assertEqual({p.name for p in (ROOT/'examples').glob('*.json')}-{'manifest.json'},set(names));self.assertEqual(len(names),len(set(names)))

    def test_allow_requires_both_parties_and_expiry(self):
        for f in ['valid_until','declaration_refs']:
            v=record('replacement-allow.json');del v[f];self.reject(v)
        v=record('replacement-allow.json');v['declaration_refs']=v['declaration_refs'][:1];self.reject(v)

    def test_missing_declarations_cannot_allow(self):
        v=record('assessment-incomplete.json');self.assertEqual([],v['declaration_refs']);validator().validate(v)
        v.update(decision='allow',valid_until='2026-11-02T12:35:00Z');self.reject(v)

    def test_non_allow_requires_reason_and_next_step(self):
        for d in ['deny','hold','escalate']:
            v=record('assessment-hold.json');v.update(decision=d,reasons=[]);self.reject(v)
        v=record('assessment-hold.json');del v['reasons'][0]['required_next_step'];self.reject(v)

    def test_invented_decisions_and_duplicate_roles(self):
        v=record('assessment-hold.json');v['decision']='offer_alternative';self.reject(v)
        v=record('assessment-hold.json');v['declaration_refs'][1]['party_role']='consumer';self.reject(v)

    def test_old_version_and_draft(self):
        for f,x in [('version','1'),('version','2'),('draft_revision','2026-10-11'),('draft_revision','2026-11-02-r4')]:
            v=record('assessment-hold.json');v[f]=x;self.reject(v)

    def test_poppy_revision_string(self):
        v=record('replacement-operation.json');v['revision']='1791487200-k3Jd9Qx2mW8v';validator('operationBinding').validate(v)
        for revision in [1,True,'','has spaces','x'*257]:
            v['revision']=revision;self.reject(v,'operationBinding')
        v=record('replacement-hold.json');v['proposal']['operation']['revision']=1;self.reject(v)

    def test_sh_revision_integer(self):
        v=record('family-declaration.json');del v['declaration']['declaration_revision'];self.reject(v)
        v=record('family-declaration.json');v['declaration']['declaration_revision']='2';self.reject(v)
        v=record('assessment-hold.json');v['declaration_refs'][0]['revision']='2';self.reject(v)

    def test_authority_shape_preserved(self):
        v=record('family-declaration.json');v['declaration']['authority_level']['configurator_ref']='not-authority';self.reject(v)

    def test_concern_is_not_verification(self):
        v=record('relayed-concern.json');v['report_status']='verified';self.reject(v)

    def test_binding_placement(self):
        self.reject(record('replacement-hold.json'),'operationBinding')
        validator().validate(record('replacement-operation.json'))
        v=read('replacement-operation.json');del v['message']['extensions']['operations']['operation']
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_binding_revision_matches(self):
        v=read('replacement-operation.json');v['message']['extensions']['operations']['operation']['revision']='changed'
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_discovery_scope_and_operations_v3(self):
        company=read('company-discovery.json');context=read('request-negotiation.json')
        config=company['extensions'][EXT][0]
        self.assertEqual('3',config['version'])
        self.assertTrue(set(config.get('required_actions',[]))<=set(config['actions']))
        self.assertEqual('3',company['extensions']['operations'][0]['version'])
        self.assertNotIn('endpoint',company['extensions']['operations'][0])
        self.assertEqual('1.0',company['protocol_version'])
        self.assertNotIn('extensions',read('client-metadata.json'))
        self.assertEqual('3',parse_extensions_header(context['headers']['Poppy-Extensions'])[EXT])
        read(context['body_file'])

    def test_namespaced_actions(self):
        v=record('assessment-hold.json');v['proposal']['action_type']='example.com:retention_offer';validator().validate(v)

    def test_upstream_rejects_missing_author(self):
        v=read('message-declaration.json');del v['message']['author'];v['message']['sender']='agent'
        self.assertTrue(list(base_validator('conversation-request.schema.json').iter_errors(v)))

    def test_upstream_rejects_missing_event_role(self):
        v=read('replacement-allow.json');del v['message']['role']
        self.assertTrue(list(base_validator('event.schema.json').iter_errors(v)))

    def test_client_cannot_claim_company_assessment(self):
        v={'message':read('replacement-allow.json')['message']};v['message'].pop('role')
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_client_cannot_issue_operation(self):
        v={'message':read('replacement-operation.json')['message']};v['message'].pop('role')
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_company_cannot_supply_user_approval(self):
        v=read('replacement-allow.json');v['message']['extensions']['operations']={'approval':{'operation_id':'op-replacement-1','revision':'rev-replacement-a'}}
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_allow_interval(self):
        v=read('replacement-allow.json');v['message']['extensions'][EXT]['valid_until']='2026-11-02T12:00:00Z'
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_declaration_refs_and_principal(self):
        ds={}
        for r in records():
            if r['type']!='declaration':continue
            d=r['declaration'];k=(r['case_ref'],r['party_role'],d['declaration_id'],d['declaration_revision'])
            self.assertNotIn(k,ds);ds[k]=r
            if 'representation' in r:self.assertEqual(d['principal_id'],r['representation']['principal_ref'])
        for r in records():
            for ref in r.get('declaration_refs',[]):self.assertIn((r['case_ref'],ref['party_role'],ref['declaration_id'],ref['revision']),ds)

    def message_fixtures(self):
        return [value for entry in read('manifest.json') if 'message' in (value:=read(entry['file']))]

    def test_operation_refs_and_approvals(self):
        check_operation_bindings(self.message_fixtures())

    def test_assessment_case_and_proposal_must_match_operation_binding(self):
        for field in ('case_ref','proposal_ref'):
            values=self.message_fixtures()
            assessment=next(value['message']['extensions'][EXT] for value in values
                if value['message'].get('extensions',{}).get(EXT,{}).get('assessment_ref')==record('appointment-allow.json')['assessment_ref'])
            if field=='case_ref':assessment['case_ref']='another-case'
            else:assessment['proposal']['proposal_ref']='unrelated-proposal'
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'case or proposal'):
                check_operation_bindings(values)

    def test_supersession_keeps_case_and_proposal(self):
        assessments={r['assessment_ref']:r for r in records() if r['type']=='assessment'}
        for r in assessments.values():
            if 'supersedes' not in r:continue
            prev=assessments[r['supersedes']]
            self.assertEqual(prev['case_ref'],r['case_ref']);self.assertEqual(prev['proposal']['proposal_ref'],r['proposal']['proposal_ref'])
            self.assertGreater(datetime.fromisoformat(r['assessed_at']),datetime.fromisoformat(prev['assessed_at']))

    def test_refund_replacement_journey(self):
        denied=record('voucher-denied.json');held=record('replacement-hold.json');allowed=record('replacement-allow.json')
        self.assertEqual(['deny','hold','allow'],[r['decision'] for r in [denied,held,allowed]])
        self.assertEqual(denied['case_ref'],held['case_ref']);self.assertNotEqual(denied['proposal']['proposal_ref'],held['proposal']['proposal_ref'])
        self.assertEqual(held['proposal'],allowed['proposal']);self.assertEqual(held['assessment_ref'],allowed['supersedes'])
        self.assertNotEqual(held['declaration_refs'],allowed['declaration_refs'])

    def test_revised_declaration_keeps_boundary(self):
        a=record('message-declaration.json')['declaration'];b=record('delivery-declaration-revised.json')['declaration']
        self.assertEqual(a['options_constraints'],b['options_constraints']);self.assertEqual(a['goals'],b['goals']);self.assertEqual([],b['unresolved_fields'])

    def test_arranged_is_not_delivered(self):
        arranged=read('replacement-arranged.json');delivered=read('replacement-delivered.json')
        a=arranged['message']['data']['service_result'];b=delivered['message']['data']['service_result']
        self.assertFalse(a['case_resolved']);self.assertTrue(b['case_resolved']);self.assertEqual(a['replacement_ref'],b['replacement_ref'])
        self.assertGreater(datetime.fromisoformat(delivered['created_at']),datetime.fromisoformat(arranged['created_at']))

    def test_late_hold_keeps_history(self):
        a=record('assessment-after-evidence.json');b=record('approval-blocked-message.json')
        self.assertEqual('allow',a['decision']);self.assertEqual('hold',b['decision']);self.assertEqual(a['assessment_ref'],b['supersedes'])
        self.assertEqual(a['proposal'],b['proposal']);self.assertNotEqual(a['record_id'],b['record_id']);self.assertNotIn('valid_until',b)

    def test_safeguarding_escalation_and_handover_keep_authority_hold(self):
        r=record('assessment-escalate.json');h=record('handover.json')
        self.assertEqual('escalate',r['decision'])
        self.assertEqual({'authority_unresolved','relayed_alarm_dependency'},{reason['code'] for reason in r['reasons']})
        self.assertEqual({'hold','escalate'},{restriction['decision'] for restriction in h['restrictions']})
        self.assertTrue(h['support_instructions'])


    def test_legacy_sh_placement_cannot_satisfy_binding(self):
        v=read('replacement-hold.json');m=v['message']
        m['data']={EXT:m['extensions'].pop(EXT)}
        # Base schemas permit unknown ordinary data. The binding must still reject it.
        base_validator('event.schema.json').validate(v)
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_legacy_operation_and_approval_cannot_satisfy_binding(self):
        for name,field in [('replacement-operation.json','operation'),('replacement-approval.json','approval')]:
            v=read(name);m=v['message']
            m[field]=m['extensions'].pop('operations')[field]
            base_validator('message.schema.json').validate(m)
            with self.assertRaises(ValueError):check_message_semantics(v)

    def test_operations_content_requires_one_kind(self):
        op=read('replacement-operation.json')['message']['extensions']['operations']['operation']
        approval=read('replacement-approval.json')['message']['extensions']['operations']['approval']
        for content in [{},{'operation':op,'approval':approval},{'approval':{'operation_id':'x','revision':1}}]:
            v=read('replacement-approval.json');v['message']['extensions']['operations']=content
            self.assertTrue(list(base_validator('conversation-message-request.schema.json').iter_errors(v)))

    def test_extension_value_must_be_object(self):
        v=read('message-declaration.json');v['message']['extensions'][EXT]='approve everything'
        self.assertTrue(list(base_validator('conversation-request.schema.json').iter_errors(v)))

    def test_examples_have_request_extension_selection(self):
        for entry in read('manifest.json'):
            value=read(entry['file'])
            if 'message' in value:
                with self.subTest(file=entry['file']):
                    check_fixture_negotiation(value,read('company-discovery.json'),read('request-negotiation.json'))

    def test_unavailable_draft_or_version_cannot_be_selected(self):
        for which in ('company','local'):
            for mode in ('missing','version','draft'):
                company=read('company-discovery.json');context=read('request-negotiation.json')
                extensions=company['extensions'] if which=='company' else context['local_support']
                if mode=='missing':del extensions[EXT]
                else:
                    config=extensions[EXT][0] if which=='company' else extensions[EXT]
                    config['version' if mode=='version' else 'draft_revision']='2' if mode=='version' else '2026-11-02-r4'
                with self.subTest(which=which,mode=mode),self.assertRaises(ValueError):
                    check_fixture_negotiation(read('replacement-hold.json'),company,context)

    def test_payload_cannot_claim_a_draft_not_selected(self):
        value=read('replacement-hold.json');value['message']['extensions'][EXT]['draft_revision']='2026-11-02-r4'
        with self.assertRaises(ValueError):
            check_fixture_negotiation(value,read('company-discovery.json'),read('request-negotiation.json'))

    def test_unsupported_draft_does_not_block_plain_language_assistance(self):
        company=read('company-discovery.json');context=read('request-negotiation.json')
        company['extensions'][EXT][0]['draft_revision']='2026-11-02-r4'
        context['headers']['Poppy-Extensions']='"operations";v="3"'
        value=read('replacement-request.json')
        self.assertNotIn(EXT,value['message'].get('extensions',{}))
        check_fixture_negotiation(value,company,context)

    def test_client_metadata_map_is_not_request_selection(self):
        company=read('company-discovery.json');context=read('request-negotiation.json')
        context['headers']['Poppy-Extensions']='"operations";v="3"'
        context['extensions']=copy.deepcopy(company['extensions'])
        with self.assertRaises(ValueError):
            check_fixture_negotiation(read('replacement-hold.json'),company,context)

    def test_company_profile_is_scoped_claim_not_client_downgrade(self):
        company=read('company-discovery.json');context=read('request-negotiation.json')
        company['extensions'][EXT][0]['profile']='verified_authority'
        context['local_support'][EXT]['profile']='participation'
        check_fixture_negotiation(read('replacement-hold.json'),company,context)
        self.assertEqual('verified_authority',company['extensions'][EXT][0]['profile'])
        # Header selection neither changes this claim nor verifies its evidence.

    def test_operations_support_and_binding_are_both_needed(self):
        for which in ('company','local'):
            for mode in ('missing','version','binding'):
                company=read('company-discovery.json');context=read('request-negotiation.json')
                extensions=company['extensions'] if which=='company' else context['local_support']
                if mode=='missing':del extensions['operations']
                elif mode=='version':
                    config=extensions['operations'][0] if which=='company' else extensions['operations']
                    config['version']='2'
                else:
                    config=extensions[EXT][0] if which=='company' else extensions[EXT]
                    config['operations_binding']=False
                with self.subTest(which=which,mode=mode),self.assertRaises(ValueError):
                    check_fixture_negotiation(read('replacement-operation.json'),company,context)

    def test_old_discovery_shape_and_missing_description_are_rejected(self):
        company=read('company-discovery.json')
        company['extensions'][EXT]=company['extensions'][EXT][0]
        self.assertTrue(list(base_validator('poppy.schema.json').iter_errors(company)))
        company=read('company-discovery.json');del company['agent']['protocols'][0]['description']
        self.assertTrue(list(base_validator('poppy.schema.json').iter_errors(company)))

    def test_old_protocol_document_does_not_claim_this_binding(self):
        company=read('company-discovery.json');company['protocol_version']='0.3'
        with self.assertRaises(ValueError):
            check_fixture_negotiation(read('replacement-hold.json'),company,read('request-negotiation.json'))

    def test_links_and_disclosures_can_coexist_without_changing_hold(self):
        value=read('replacement-hold.json');before=copy.deepcopy(value['message']['extensions'][EXT])
        value['message']['extensions']['links']={'items':[{'url':'https://shop.example/returns','title':'Returns policy'}]}
        value['message']['extensions']['disclosures']={'items':[{'text':'Replacement delivery requires an agreed date.'}]}
        company=read('company-discovery.json');context=read('request-negotiation.json')
        for name in ('links','disclosures'):
            company['extensions'][name]=[{'version':'1'}]
            context['local_support'][name]={'version':'1'}
            context['headers']['Poppy-Extensions']+=f', "{name}";v="1"'
        base_validator('event.schema.json').validate(value)
        check_message_semantics(value);check_fixture_negotiation(value,company,context)
        self.assertEqual(before,value['message']['extensions'][EXT])
        self.assertEqual('hold',value['message']['extensions'][EXT]['decision'])

    def test_company_first_direct_invitation_uses_opening_schema(self):
        value={'id':'1c8fcc025565439bb3f449bf998d8550','parent_conversation_id':'cnv-parent','user_requested_event_id':'evt-invite'}
        base_validator('conversation-request.schema.json').validate(value)
        self.assertTrue(list(base_validator('conversation-message-request.schema.json').iter_errors(value)))
        del value['parent_conversation_id']
        self.assertTrue(list(base_validator('conversation-request.schema.json').iter_errors(value)))

    def test_top_level_request_id_is_required(self):
        for name,schema in [('message-declaration.json','conversation-request.schema.json'),('replacement-approval.json','conversation-message-request.schema.json')]:
            value=read(name);value['message']['id']=value.pop('id')
            self.assertTrue(list(base_validator(schema).iter_errors(value)))
            with self.assertRaises(ValueError):check_message_semantics(value)

    def test_native_operation_requires_terms(self):
        value=read('replacement-operation.json');del value['message']['extensions']['operations']['operation']['terms']
        self.assertTrue(list(base_validator('event.schema.json').iter_errors(value)))

    def test_native_approval_requires_approver(self):
        for approver in (None,'company'):
            value=read('replacement-approval.json');approval=value['message']['extensions']['operations']['approval']
            if approver is None:del approval['approver']
            else:approval['approver']=approver
            self.assertTrue(list(base_validator('conversation-message-request.schema.json').iter_errors(value)))

    def test_agent_approval_does_not_claim_user_input_type(self):
        value=read('appointment-agent-approval.json');value['message']['extensions']['operations']['approval']['input_type']='tap'
        self.assertTrue(list(base_validator('conversation-message-request.schema.json').iter_errors(value)))

    def family_trace(self):
        return [read(name) for name in ['operation-message.json','family-approval.json','approval-blocked-message.json',
                'family-recovery-request.json','family-declaration-recovery.json','family-operation-revised.json',
                'family-reapproval.json','family-recovery-allow.json']]

    def test_native_decline_and_safe_recovery_trace(self):
        check_fixture_lifecycle(self.family_trace())
        original=read('operation-message.json')['message']['extensions']['operations']['operation']
        revised=read('family-operation-revised.json')['message']['extensions']['operations']['operation']
        self.assertEqual(original['operation_id'],revised['operation_id'])
        self.assertNotEqual(original['revision'],revised['revision'])
        self.assertNotEqual(original['terms'],revised['terms'])
        self.assertNotEqual(record('operation-message.json')['proposal_ref'],record('family-operation-revised.json')['proposal_ref'])

    def test_native_decline_cannot_be_sent_as_allow_or_mismatched_summary(self):
        for field in ('operation_id','revision','decision'):
            value=read('approval-blocked-message.json')
            if field=='decision':
                value['message']['extensions'][EXT].update(decision='allow',valid_until='2026-11-25T12:35:00Z')
            else:value['message']['extensions']['operations']['declined'][field]='other'
            with self.subTest(field=field),self.assertRaises(ValueError):
                check_message_semantics(value)

    def test_declined_approval_cannot_be_resent(self):
        trace=self.family_trace()[:3]
        with self.assertRaisesRegex(ValueError,'declined approval'):
            check_fixture_lifecycle(trace+[read('family-approval.json')])
        value=read('family-approval.json');value['id']='f458433a562746e3ae425bb9590facb6'
        with self.assertRaisesRegex(ValueError,'declined approval'):
            check_fixture_lifecycle(trace+[value])

    def test_post_decline_recovery_needs_fresh_user_approval(self):
        trace=self.family_trace()
        trace[-2]['message']['extensions']['operations']['approval']['approver']='agent'
        trace[-2]['message']['extensions']['operations']['approval'].pop('input_type',None)
        with self.assertRaisesRegex(ValueError,'fresh User approval'):check_fixture_lifecycle(trace)

    def test_recovery_metadata_cannot_reuse_prior_approval(self):
        for field in ('approved_at','reference'):
            trace=self.family_trace()
            old=trace[1]['message']['extensions']['operations']['approval']
            recovery=trace[-2]['message']['extensions']['operations']['approval']
            recovery[field]=old[field]
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'predates|reused'):
                check_fixture_lifecycle(trace)

    def test_optional_approval_metadata_is_not_a_native_requirement(self):
        trace=self.family_trace()
        for value in trace:
            approval=value['message'].get('extensions',{}).get('operations',{}).get('approval')
            if approval:
                for field in ('approved_at','reference','input_type'):approval.pop(field,None)
                base_validator('conversation-message-request.schema.json').validate(value)
        check_fixture_lifecycle(trace)
        agent_trace,instructions=self.agent_trace()
        approval=agent_trace[1]['message']['extensions']['operations']['approval']
        for field in ('approved_at','reference'):approval.pop(field,None)
        check_fixture_lifecycle(agent_trace,instructions)

    def test_preapproval_hold_is_not_native_decline(self):
        trace=[read('operation-message.json'),read('approval-blocked-message.json')]
        with self.assertRaisesRegex(ValueError,'pre-approval hold'):check_fixture_lifecycle(trace)
        held=read('replacement-hold.json')
        self.assertNotIn('declined',held['message']['extensions'].get('operations',{}))
        check_fixture_lifecycle([read('replacement-operation.json'),held,read('replacement-approval.json'),read('replacement-allow.json')])

    def agent_trace(self):
        trace=[read(name) for name in ['appointment-operation.json','appointment-agent-approval.json','appointment-allow.json']]
        entry=next(entry for entry in read('manifest.json') if entry['file']=='appointment-agent-approval.json')
        return trace,{trace[1]['id']:copy.deepcopy(entry['prior_user_instruction'])}

    def test_agent_approval_has_bounded_prior_instruction(self):
        trace,instructions=self.agent_trace();check_fixture_lifecycle(trace,instructions)
        self.assertNotIn('prior_user_instruction',trace[1])
        self.assertNotIn('constraints',trace[1]['message'])

    def test_agent_approval_rejects_missing_or_company_authored_instruction(self):
        trace,instructions=self.agent_trace()
        with self.assertRaisesRegex(ValueError,'prior User instruction'):check_fixture_lifecycle(trace)
        instructions[trace[1]['id']]['source']='company_message'
        with self.assertRaisesRegex(ValueError,'prior User instruction'):check_fixture_lifecycle(trace,instructions)

    def test_agent_approval_terms_must_fit_supplied_bounds(self):
        for mutate in [lambda terms:terms['fee'].update(amount_minor=1),
                       lambda terms:terms.update(start='2026-11-26T13:00:00Z'),
                       lambda terms:terms.update(end='2026-11-26T17:00:00Z'),
                       lambda terms:terms.update(new_contract=True),
                       lambda terms:terms.update(cancellation_fee_minor=100),
                       lambda terms:terms.update(additional_material_condition='unapproved')]:
            trace,instructions=self.agent_trace()
            mutate(trace[0]['message']['extensions']['operations']['operation']['terms'])
            with self.assertRaises(ValueError):check_fixture_lifecycle(trace,instructions)

    def test_agent_approval_checks_real_interval_duration(self):
        trace,instructions=self.agent_trace()
        trace[0]['message']['extensions']['operations']['operation']['terms']['end']='2026-11-26T14:35:00Z'
        with self.assertRaisesRegex(ValueError,'interval does not match'):
            check_fixture_lifecycle(trace,instructions)

    def test_agent_approval_rejects_uncovered_nested_fee_terms(self):
        trace,instructions=self.agent_trace()
        trace[0]['message']['extensions']['operations']['operation']['terms']['fee']['recurring']=True
        with self.assertRaisesRegex(ValueError,'nested fee terms'):
            check_fixture_lifecycle(trace,instructions)

    def test_agent_approval_cannot_use_unbound_or_later_instruction(self):
        for mode in ('reference','future'):
            trace,instructions=self.agent_trace();instruction=instructions[trace[1]['id']]
            if mode=='reference':instruction['record_ref']='different-record'
            else:instruction['received_at']='2026-12-01T00:00:00Z'
            with self.assertRaises(ValueError):check_fixture_lifecycle(trace,instructions)

    def test_new_revision_after_agent_approval_needs_user(self):
        trace,instructions=self.agent_trace()
        operation=copy.deepcopy(trace[0]);operation['message']['extensions']['operations']['operation']['revision']='appointment-revision-b'
        operation['message']['extensions'][EXT]['revision']='appointment-revision-b'
        approval=copy.deepcopy(trace[1]);approval['id']='f45c0526ac9b43fdb47df6a6532594ca'
        approval['message']['extensions']['operations']['approval']['revision']='appointment-revision-b'
        with self.assertRaisesRegex(ValueError,'fresh User approval'):
            check_fixture_lifecycle(trace+[operation,approval],instructions)
        fresh_approval=approval['message']['extensions']['operations']['approval']
        fresh_approval.update(approver='user',reference='fresh-user-approval-record',approved_at=fresh_approval['approved_at']+60)
        operation['created_at']=datetime.fromtimestamp(fresh_approval['approved_at']-30,tz=timezone.utc).isoformat()
        check_fixture_lifecycle(trace+[operation,approval],instructions)

    def test_revision_identity_cannot_hide_changed_terms(self):
        value=read('replacement-operation.json');changed=copy.deepcopy(value)
        changed['message']['extensions']['operations']['operation']['terms']['unexpected_charge']=10
        with self.assertRaisesRegex(ValueError,'immutable operation revision'):
            check_fixture_lifecycle([value,changed])

    def test_revision_identity_cannot_hide_changed_expiry(self):
        value=read('replacement-operation.json');changed=copy.deepcopy(value)
        changed['message']['extensions']['operations']['operation']['expires_at']='2026-12-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'immutable operation revision'):
            check_fixture_lifecycle([value,changed])

    def test_summary_rewording_does_not_change_operation_revision(self):
        value=read('replacement-operation.json');reworded=copy.deepcopy(value)
        reworded['message']['extensions']['operations']['operation']['summary']='The same replacement, with every material term unchanged.'
        reworded['created_at']='2026-11-25T12:30:00Z'
        approval=read('replacement-approval.json')
        check_fixture_lifecycle([value,approval,reworded,approval])

    def test_handover_cannot_drop_a_concurrent_restriction(self):
        assessments=[record('assessment-hold.json'),record('assessment-escalate.json')]
        handover=record('handover.json');check_handover_continuity(assessments,handover)
        for index in range(len(handover['restrictions'])):
            changed=copy.deepcopy(handover);changed['restrictions'].pop(index)
            with self.assertRaisesRegex(ValueError,'dropped an unresolved'):
                check_handover_continuity(assessments,changed)

    def test_reference_hashes(self):
        lock=json.loads((ROOT/'SOURCE-LOCK.json').read_text())
        for e in lock['files']:self.assertEqual(e['sha256'],hashlib.sha256((ROOT/e['local_path']).read_bytes()).hexdigest(),e['local_path'])
        expected={'sh-1.2.schema.json':'ee2d7124f718b9f28cfa20764c2e8cd48b9f35749f3111b6638d2f55ccd11cb5',
                  'sh-1.2.action-assessment.schema.json':'be0d37779d76420112129cb364792414b68a1dd59151367c49ae4443a6253746'}
        for n,d in expected.items():self.assertEqual(d,hashlib.sha256((ROOT/'reference'/n).read_bytes()).hexdigest())

    def check_diagnostic(self,name,mutate,expected):
        # Run an existing test against a deliberately damaged copy of a fixture.
        # Confirm unittest reports a useful failure, rather than an ERROR/KeyError.
        with tempfile.TemporaryDirectory() as directory:
            temporary=Path(directory)
            shutil.copytree(ROOT/'examples',temporary/'examples')
            path=temporary/'examples'/name
            path.write_text(mutate(path.read_text()))
            result=unittest.TestResult()
            with patch.object(sys.modules[__name__],'ROOT',temporary):
                PackageChecks('test_complete_upstream_envelopes').run(result)
            self.assertEqual([],result.errors)
            self.assertEqual(1,len(result.failures))
            report=result.failures[0][1]
            self.assertIn(name,report)
            self.assertIn(expected,report)
            self.assertNotIn('KeyError:',report)

    def test_misplaced_sh_fixture_reports_readable_failure(self):
        def mutate(text):
            value=json.loads(text);msg=value['message']
            msg['data']={EXT:msg['extensions'].pop(EXT)}
            return json.dumps(value)
        self.check_diagnostic('replacement-hold.json',mutate,'Move the record to $.message.extensions')

    def test_misplaced_operation_fixture_reports_readable_failure(self):
        def mutate(text):
            value=json.loads(text);msg=value['message']
            msg['operation']=msg['extensions'].pop('operations')['operation']
            return json.dumps(value)
        self.check_diagnostic('replacement-operation.json',mutate,'Move it to $.message.extensions.operations.operation')

    def test_invalid_json_fixture_reports_readable_failure(self):
        self.check_diagnostic('replacement-hold.json',lambda text:'{"message":','invalid JSON at line')

if __name__=='__main__':unittest.main()
