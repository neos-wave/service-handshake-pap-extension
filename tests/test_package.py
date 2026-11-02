"""Offline envelope, exchange and scenario checks; no network or running service."""
import copy
import hashlib
import json
import unittest
from datetime import datetime
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT=Path(__file__).resolve().parents[1]
EXT='dualcx.com/service-handshake'
BASE='https://personalagentprotocol.org/kit/company/schemas/'
SID='urn:dualcx:service-handshake:poppy:2:draft:2026-11-02-r4'
SCHEMAS=[json.loads(p.read_text()) for p in sorted(ROOT.glob('reference/*.json'))]
SCHEMAS.append(json.loads((ROOT/'schema/sh-poppy-extension.schema.json').read_text()))
POPPY={p.name:json.loads(p.read_text()) for p in (ROOT/'reference/poppy').glob('*.json')}
REGISTRY=Registry().with_resources([(s['$id'],Resource.from_contents(s)) for s in SCHEMAS]+[(BASE+n,Resource.from_contents(s)) for n,s in POPPY.items()])
def read(name):return json.loads((ROOT/'examples'/name).read_text())
HINTS={EXT:'SH records belong in message.extensions["%s"], not message.data (Specification §4; MIGRATION.md)'%EXT,
       'operations':'Operations content belongs in message.extensions.operations.operation or .approval, not a top-level field (Specification §§4, 7; MIGRATION.md)'}
def at(value,path,where):
    """Return value at path, or fail naming the file, expected location and correction."""
    cur=value
    for i,k in enumerate(path):
        if not isinstance(cur,dict) or k not in cur:
            loc=''.join('["%s"]'%x if '/' in str(x) else '.'+str(x) for x in path).lstrip('.')
            hint=next((h for key,h in HINTS.items() if key in path),'check the example against the manifest pointer')
            raise AssertionError('%s: expected %s (missing "%s"). %s.'%(where,loc,k,hint))
        cur=cur[k]
    return cur
def record(name):return at(read(name),['message','extensions',EXT],name)
def operation(name):return at(read(name),['message','extensions','operations','operation'],name)
def approval(name):return at(read(name),['message','extensions','operations','approval'],name)
def validator(definition='messageRecord'):return Draft202012Validator({'$ref':SID+'#/$defs/'+definition},registry=REGISTRY,format_checker=FormatChecker())
def base_validator(name):return Draft202012Validator({'$ref':BASE+name},registry=REGISTRY,format_checker=FormatChecker())
def records():
    return [v for e in read('manifest.json') if (v:=read(e['file']).get('message',{}).get('extensions',{}).get(EXT))]

def check_message_semantics(value):
    """Fixture sender/placement checks, not authentication of a real sender."""
    msg=value['message']
    company=value.get('type')=='message' and msg.get('role')=='company'
    exts=msg.get('extensions',{})
    operations=exts.get('operations',{})
    if any(k in msg for k in ('sender','operation','approval')):
        raise ValueError('legacy top-level sender/operation/approval field: '+HINTS['operations'])
    if EXT in msg.get('data',{}):
        raise ValueError('legacy SH placement in message.data: '+HINTS[EXT])
    if value.get('type')!='message' and 'role' in msg:raise ValueError('client role')
    if not company and any(k in msg['author'] for k in ('id','name','image')):raise ValueError('client company-author fields')
    if 'operation' in operations and not company:raise ValueError('client operation')
    if 'approval' in operations and (company or msg['author']['type']!='agent'):raise ValueError('approval sender')
    if company and 'context' in msg:raise ValueError('company context')
    if not company and any(k in exts for k in ('links','disclosures')):raise ValueError('company-only extension')
    rec=exts.get(EXT)
    if rec:
        if rec['type'] in ('assessment','operation_binding') and not company:raise ValueError('client trusted company record')
        if rec['type']=='operation_binding':
            op=operations.get('operation')
            if not op or any(op[k]!=rec[k] for k in ('operation_id','revision')):raise ValueError('operation_binding needs extensions.operations.operation with the same operation_id and revision in the same Company message')
        if rec['type']=='assessment' and rec['decision']=='allow':
            if datetime.fromisoformat(rec['valid_until'])<=datetime.fromisoformat(rec['assessed_at']):raise ValueError('allow interval')
    if 'operation' in operations:
        if not rec or rec['type']!='operation_binding':raise ValueError('operation has no operation_binding in the same message: '+HINTS[EXT])
        if any(k in operations['operation'] for k in ('state','confirmation','result','user_approval_required',EXT)):raise ValueError('legacy operation')

def check_fixture_negotiation(value, company, client):
    """Checks supplied fixture advertisements, not live metadata or negotiation."""
    ce=company.get('extensions',{});pe=client.get('extensions',{})
    for name in value.get('message',{}).get('extensions',{}):
        if name not in ce or name not in pe or ce[name]['version']!=pe[name]['version']:
            raise ValueError('extension not mutually advertised at same version')
        if name==EXT:
            rec=value['message']['extensions'][name]
            if any(e[name]['version']!=rec['version'] or e[name]['draft_revision']!=rec['draft_revision'] for e in (ce,pe)):
                raise ValueError('SH draft mismatch')
    if 'operations' in value.get('message',{}).get('extensions',{}):
        if not all(e.get(EXT,{}).get('operations_binding') for e in (ce,pe)):
            raise ValueError('SH Operations binding not agreed')

class PackageChecks(unittest.TestCase):
    def reject(self,value,definition='messageRecord'):self.assertTrue(list(validator(definition).iter_errors(value)))

    def test_schema_documents(self):
        for s in SCHEMAS+list(POPPY.values()):Draft202012Validator.check_schema(s)

    def test_complete_upstream_envelopes(self):
        for e in read('manifest.json'):
            with self.subTest(file=e['file']):
                v=read(e['file'])
                errs=sorted(base_validator(e['base_schema']).iter_errors(v),key=lambda x:list(x.path))
                if errs:self.fail('%s: does not match Poppy %s at %s: %s'%(e['file'],e['base_schema'],'/'.join(map(str,errs[0].path)) or '(root)',errs[0].message))
                if 'message' in v:
                    try:check_message_semantics(v)
                    except ValueError as x:self.fail('%s: %s'%(e['file'],x))

    def test_extension_payloads(self):
        for e in read('manifest.json'):
            if 'definition' not in e:continue
            with self.subTest(file=e['file']):
                v=at(read(e['file']),e['pointer'],e['file'])
                errs=list(validator(e['definition']).iter_errors(v))
                if errs:self.fail('%s: SH %s record invalid at %s: %s'%(e['file'],e['definition'],'/'.join(map(str,errs[0].path)) or '(root)',errs[0].message))

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
        for f,x in [('version','1'),('draft_revision','2026-10-11'),('draft_revision','2026-11-02')]:
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
        v=read('replacement-operation.json');del at(v,['message','extensions','operations'],'replacement-operation.json')['operation']
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_binding_revision_matches(self):
        v=read('replacement-operation.json');at(v,['message','extensions','operations','operation'],'replacement-operation.json')['revision']='changed'
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_discovery_scope_and_operations_v2(self):
        for name in ['company-discovery.json','client-metadata.json']:
            e=read(name)['extensions'];c=e[EXT]
            self.assertEqual('2',c['version']);self.assertTrue(set(c.get('required_actions',[]))<=set(c['actions']))
            if c['operations_binding']:self.assertEqual('2',e['operations']['version'])
            self.assertNotIn('endpoint',e['operations'])
        self.assertEqual('0.3',read('company-discovery.json')['protocol_version'])

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
        v=read('replacement-allow.json');at(v,['message','extensions',EXT],'replacement-allow.json')['valid_until']='2026-11-02T12:00:00Z'
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

    def test_operation_refs_and_approvals(self):
        ops={}
        for e in read('manifest.json'):
            msg=read(e['file']).get('message',{})
            if 'operation' in msg.get('extensions',{}).get('operations',{}):
                op=msg['extensions']['operations']['operation'];k=(op['operation_id'],op['revision']);self.assertNotIn(k,ops);ops[k]=op
        for e in read('manifest.json'):
            msg=read(e['file']).get('message',{});r=msg.get('extensions',{}).get(EXT,{})
            ref=r.get('proposal',{}).get('operation') or msg.get('extensions',{}).get('operations',{}).get('approval')
            if ref:self.assertIn((ref['operation_id'],ref['revision']),ops,'%s refers to operation %s revision %s, but no example carries it in message.extensions.operations.operation. %s.'%(e['file'],ref['operation_id'],ref['revision'],HINTS['operations']))

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
        at(v,['message','extensions',EXT],'replacement-hold.json');m['data']={EXT:m['extensions'].pop(EXT)}
        # Base schemas permit unknown ordinary data. The binding must still reject it.
        base_validator('event.schema.json').validate(v)
        with self.assertRaises(ValueError):check_message_semantics(v)

    def test_legacy_operation_and_approval_cannot_satisfy_binding(self):
        for name,field in [('replacement-operation.json','operation'),('replacement-approval.json','approval')]:
            v=read(name);m=v['message'];at(v,['message','extensions','operations',field],name)
            m[field]=m['extensions'].pop('operations')[field]
            base_validator('message.schema.json').validate(m)
            with self.assertRaises(ValueError):check_message_semantics(v)

    def test_operations_content_requires_one_kind(self):
        op=operation('replacement-operation.json')
        appr=approval('replacement-approval.json')
        for content in [{},{'operation':op,'approval':appr},{'approval':{'operation_id':'x','revision':1}}]:
            v=read('replacement-approval.json');v['message']['extensions']['operations']=content
            self.assertTrue(list(base_validator('conversation-message-request.schema.json').iter_errors(v)))

    def test_extension_value_must_be_object(self):
        v=read('message-declaration.json');v['message']['extensions'][EXT]='approve everything'
        self.assertTrue(list(base_validator('conversation-request.schema.json').iter_errors(v)))

    def test_examples_have_mutual_extension_agreement(self):
        for e in read('manifest.json'):
            check_fixture_negotiation(read(e['file']),read('company-discovery.json'),read('client-metadata.json'))

    def test_unadvertised_or_mismatched_extension_is_not_sent(self):
        for which in ('company','client'):
            for mode in ('missing','version','draft'):
                c=read('company-discovery.json');a=read('client-metadata.json')
                exts=(c if which=='company' else a)['extensions']
                if mode=='missing':del exts[EXT]
                elif mode=='version':exts[EXT]['version']='1'
                else:exts[EXT]['draft_revision']='2026-11-02'
                with self.assertRaises(ValueError):check_fixture_negotiation(read('replacement-hold.json'),c,a)

    def test_operations_support_and_binding_are_both_needed(self):
        for mode in ('missing','version','binding'):
            c=read('company-discovery.json');a=read('client-metadata.json')
            if mode=='missing':del a['extensions']['operations']
            elif mode=='version':a['extensions']['operations']['version']='1'
            else:a['extensions'][EXT]['operations_binding']=False
            with self.assertRaises(ValueError,msg='replacement-operation.json: expected an Operations message in message.extensions.operations, so a missing Operations agreement (%s) must be rejected. %s.'%(mode,HINTS['operations'])):check_fixture_negotiation(read('replacement-operation.json'),c,a)

    def test_links_and_disclosures_can_coexist_without_changing_hold(self):
        v=read('replacement-hold.json');before=copy.deepcopy(at(v,['message','extensions',EXT],'replacement-hold.json'))
        v['message']['extensions']['links']={'items':[{'url':'https://shop.example/returns','title':'Returns policy'}]}
        v['message']['extensions']['disclosures']={'items':[{'text':'Replacement delivery requires an agreed date.'}]}
        c=read('company-discovery.json');a=read('client-metadata.json')
        for e in (c,a):
            e['extensions'].update(links={'version':'1'},disclosures={'version':'1'})
        base_validator('event.schema.json').validate(v);check_message_semantics(v);check_fixture_negotiation(v,c,a)
        self.assertEqual(before,v['message']['extensions'][EXT])
        self.assertEqual('hold',v['message']['extensions'][EXT]['decision'])

    def test_company_first_direct_invitation_uses_opening_schema(self):
        v={'parent_conversation_id':'cnv-parent','user_requested_event_id':'evt-invite'}
        base_validator('conversation-request.schema.json').validate(v)
        self.assertTrue(list(base_validator('conversation-message-request.schema.json').iter_errors(v)))
        del v['parent_conversation_id']
        self.assertTrue(list(base_validator('conversation-request.schema.json').iter_errors(v)))

    def test_reference_hashes(self):
        lock=json.loads((ROOT/'SOURCE-LOCK.json').read_text())
        for e in lock['files']:self.assertEqual(e['sha256'],hashlib.sha256((ROOT/e['local_path']).read_bytes()).hexdigest(),e['local_path'])
        expected={'sh-1.2.schema.json':'ee2d7124f718b9f28cfa20764c2e8cd48b9f35749f3111b6638d2f55ccd11cb5',
                  'sh-1.2.action-assessment.schema.json':'be0d37779d76420112129cb364792414b68a1dd59151367c49ae4443a6253746'}
        for n,d in expected.items():self.assertEqual(d,hashlib.sha256((ROOT/'reference'/n).read_bytes()).hexdigest())

if __name__=='__main__':unittest.main()
