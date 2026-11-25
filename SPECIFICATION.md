# Service Handshake extension proposal for the Personal Agent Protocol (Poppy): specification

Review package draft 6, 25 November 2026. Wire draft `2026-11-25`, proposed extension major version `"3"`. Targets published Poppy 1.0 and Operations version 3 at the immutable 1.0 release revision pinned in SOURCES.md. This is an incompatible update to the extension binding, not a new SH edition. Independent proposal; not adopted by Poppy or demonstrated through a live integration. Author: Maria McCann. Publisher: Neos Wave Ltd / Dual CX. Apache 2.0. See README and NOTICE for status and attribution.

## 1. Scope and precedence

The Service Handshake gives a Company and a customer's Personal Agent a shared way to establish service goals, boundaries and conditions, assess proposed actions and preserve the relevant terms through changes and handovers. This specification binds that SH-1.2 service framework to native Poppy conversations, with an optional Operations binding. Poppy's authentication, permissions and base errors remain applicable. This extension supplies additional requirements for implementations that agree to use it; it does not make a core Poppy error or state mean something different.

SH-1.2 requirements continue to apply to an SH conformance claim. This draft does not relax them or redefine its two profiles. It adds machine-exchange and binding requirements for adopters of this extension; those are not new requirements for every SH Participation implementation. The published SH declaration and assessment schemas are unchanged. The exchange schemas describe an additional format, not a replacement canonical assessment or authority credential.

Uppercase MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have their BCP 14 meanings. The normative SH references below are to the **Technical Specification** unless the main paper is named. In this draft, the prose defines behavioural requirements; the schema defines structural requirements. If they disagree, hold the affected protected action and report the defect rather than treating validation as permission.

## 2. Terms and trust

Poppy's User, Personal Agent, Company, Session and Operation retain their meanings. A **principal** is the represented party for the proposed act. A **configurator** set up the agent and may have no authority over that act. A **proposal** is a specific immutable action and its material terms. An **assessment** is a trusted local decision. An **assessment summary** communicates a limited view of that decision; the recipient cannot treat it as a credential or permission to exceed its own boundaries.

The Company MUST derive sender identity and access from its trusted protocol context, not fields supplied in a payload. `party_role`, representation references and case references are claims until appropriately bound to that context. A Personal Agent MAY prepare terms for its own User; that does not make them an assisted declaration.

## 3. Discovery and agreement

The Company advertises `dualcx.com/service-handshake` in its Poppy 1.0 discovery document. Its value is an **array** of configuration objects, one per supported extension major version. The version-3 entry has these fields:

| Field | Meaning |
|---|---|
| `version` | Required string `"3"`. This version defines the wire draft below. |
| `draft_revision` | Required `"2026-11-25"` for this review draft. |
| `profile` | Required `participation` or `verified_authority`, describing the Company's own scoped claim. |
| `actions` | Required non-empty list of supported SH action categories. Core meanings follow SH Appendix A; other meanings need an organisation-controlled namespace and an explicit definition. |
| `operations_binding` | Required boolean. True means the Company implements §7 with Operations version 3. |
| `required_actions` | Optional subset of `actions` that the Company handles on this path only with this extension. It does not impose a global denial of service. |
| `company_terms` | Optional HTTPS resource containing a public SH declaration. It is not an authority-verification endpoint. |

```json
{
  "extensions": {
    "dualcx.com/service-handshake": [{
      "version": "3",
      "draft_revision": "2026-11-25",
      "profile": "participation",
      "actions": ["refund", "replacement"],
      "operations_binding": true
    }],
    "operations": [{ "version": "3" }]
  }
}
```

This is a discovery **fragment**. [The complete example](examples/company-discovery.json) also supplies the required Poppy fields, including each conversation protocol's description.

The Personal Agent MUST inspect the Company's advertised version and exact draft before selecting this extension. It sends its selection through Poppy's existing request headers, not an extension capability map in OAuth client metadata:

```http
Poppy-Version: 1.0
Poppy-Extensions: "dualcx.com/service-handshake";v="3", "operations";v="3"
```

These accompany the valid Session header on requests that require it. They are not sent on discovery or OAuth requests. Poppy requires the same version and extension selections throughout a Session; changing them requires a new Session. Parse `Poppy-Extensions` as the RFC 9651 List of Strings defined by Poppy §3.4. A missing or malformed header declares no extensions.

Selecting this extension's major version 3 asserts support for its defined wire draft `2026-11-25` and mandatory behaviour within the implementation's declared action scope. The Personal Agent MUST NOT select it when the advertised draft is unknown or incompatible. The Company checks the selected major version on each request and the exact version/draft in every SH payload. It sends SH records only when the request selects the version it advertises. This draft introduces no extra header, header parameter, approval step or out-of-band negotiation prerequisite. A future incompatible wire or behavioural revision MUST use a new extension major version; it MUST NOT reuse version 3 with incompatible meanings.

[request-negotiation.json](examples/request-negotiation.json) illustrates request headers and the Personal Agent's local support settings. Those local settings are test/implementation configuration, **not an HTTP request body, OAuth metadata or another message exchanged with the Company**. The schema's `localSupport` definition describes those settings only.

The Company advertises its supported action categories; the Personal Agent selects actions whose meanings it also understands. `refund` is a shared action category; `offer_refund` and `accept_refund` are complementary roles, not incompatible categories. An unknown material meaning requires clarification or an ordinary assisted route. Each party's SH profile describes its own scoped claim and never reduces the other's requirements. Local configuration or an advertised profile is not proof of conformance, authority or implementation behaviour.

Using §7 requires the Company's `operations_binding: true`, a Company advertisement for `operations` version `"3"`, and a request selecting both extensions at version `"3"`. A Personal Agent selecting both with that Company MUST implement the composition in §7. Otherwise it leaves out Operations support for that Session and uses permitted conversations or the Company's ordinary approval route. The Company MUST NOT send operation content when the request does not select Operations 3. SH conversations can still take place without the optional Operations binding.

Unknown extensions and unsupported versions follow Poppy's ignore rules. A party MUST NOT send unsupported extension content. Where the Company cannot handle an affected request without an extension that the request has not selected, use Poppy's `extension_required` response naming the extension, with an intelligible assisted or human route where available. An incompatible SH payload is handled under §11. Do not silently downgrade a protected action whose required checks would be lost. See [Poppy 1.0 §§3.3–3.4](https://personalagentprotocol.org/docs/1.0/spec#extensions).

## 4. Wire records and placement

Use the exact key `dualcx.com/service-handshake` inside a Poppy message's `extensions` object, as required by Poppy §§3.3 and 8.4. The published [exchange schema](schema/sh-poppy-extension.schema.json) validates that key's value; it uses JSON Schema 2020-12 and references the unchanged SH reference schemas. The extension value is one record, not an instruction or collection of privileged rules. Each record has `version`, `draft_revision`, `type` and `record_id`. `record_id` identifies an immutable record in the sender's scope. Retransmission of the same record MUST NOT create a second effect; conflicting content under the same identity MUST NOT replace accepted content.

The message record types are `declaration`, `assessment`, `handover`, `concern` and `operation_binding`. Use ordinary `text` and, where appropriate, ordinary `data` to carry the message's meaning; extension records add structured service context. A recipient that ignores an unsupported extension must still receive an intelligible account of the proposal, restriction and next step. Never rely on a structured record alone to communicate material terms or a restriction to a person. New facts create a new record; they do not edit history.

An `operation_binding` belongs in `message.extensions["dualcx.com/service-handshake"]`, alongside `message.extensions.operations.operation` in the same Company message. It MUST NOT be attached inside the operation object. Other SH records use the same domain-named extension slot, in separate messages when necessary. `message.data` remains available for ordinary Company-defined business details, such as the illustrative `service_result`. It is not an alternative location for this extension's records. Legacy top-level `operation` or `approval` fields MUST NOT be interpreted as current Operations content, and SH records in legacy locations MUST NOT satisfy this binding. If an action depends on a valid SH record that is missing, keep the affected action restricted while explaining the correction needed. No new base endpoint, operation state, approval field or handoff body is introduced. Native approval declines use `message.extensions.operations.declined` alongside a separate SH assessment summary, as §7 specifies.

Messages and events MUST follow the pinned Poppy envelope and author rules. A Personal Agent request carries its own top-level `id` with at least 128 random bits; retries reuse that request ID. A client-supplied `message.id` is not the request's idempotency key. A different request ID cannot renew an expired or declined approval. The Personal Agent uses `author.type: "agent"` for messages it writes, including summaries, paraphrases and translations, and `author.type: "human"` only for the User's own words, following Poppy §8.8. Operation approval objects are sent by the Personal Agent. The Company records `role` on events. Derive which party sent a record from the authenticated protocol context, not a claimed role. Only the Company may originate a trusted assessment summary or operation binding. Client-supplied versions of those records MUST NOT become Company decisions. Base schema validity does not establish this provenance.

Schema retrieval and identifiers are distinct: [README schema loading](README.md#schema-downloads-and-loading) identifies the version-3 schema and its dependencies. Pin the package commit when downloading it. This extension's schema has a new version-3 URN; the canonical SH-1.2 schema URNs and bytes remain unchanged.

## 5. Declarations and assistance

A `declaration` record includes `party_role`, an inline `declaration` conforming to the unchanged SH-1.2 schema, and optional `case_ref` and `representation`. This binding additionally requires `declaration_id` and `declaration_revision` for each exchanged declaration. Do not fabricate a principal or goal to meet those fields: use an ordinary intake conversation until they can truthfully be recorded.

AI status and representation MUST be disclosed at first contact. Relevant known terms SHOULD be supplied early; a full declaration in the first message is not required. Protected information and actions remain subject to the checks they need. A party MUST present material assisted terms for correction and confirmation, preserving unknowns and refusals.

The Company MUST offer proportionate assistance where the other side lacks a usable declaration, whether or not that side advertises this extension. This applies under both profiles. For an unsupported agent, use plain-language participation without an extension payload. Declining assistance alone MUST NOT terminate ordinary service; preserve permitted help and an accessible human route. Assistance does not waive account access checks.

Provenance retains SH §2.3 meanings: self-declared terms, previously agreed terms, or terms prepared with the other party's assistance. A party preparing an assisted declaration for the other side MUST record its actual confirmation status and provenance; it MUST NOT impersonate that party or manufacture confirmation. Confirmation establishes the claimed terms, not delegation.

Both parties' relevant boundaries MUST be established before a protected action. The Company MAY publish general terms at `company_terms` or send appropriate case terms through the conversation. It need not disclose private thresholds. A public policy is not proof of case-specific authority. Where the Personal Agent is the supporting party, its assisted record of Company statements remains unconfirmed until appropriately confirmed by the Company.

**Signed-out contact**

Where the Company accepts the Personal Agent and offers a signed-out service route, intake, permitted assistance and declaration exchange MAY continue without account sign-in. Extension exchange still requires agreement under §3, and claims about the principal or authority remain unverified until checked; do not invent a verified identity to complete a declaration. The Company MUST NOT disclose protected account information or execute an action while its required access or authority is missing. Explain what is missing and the available authorised route; the absence of sign-in does not by itself prohibit otherwise permitted assistance.

Apply Poppy's access and conversation-ownership rules. Refusing a particular sign-in type is not necessarily refusal of all contact, but this extension cannot require acceptance of a rejected client or continuation of an account-bound conversation while signed out. An appropriate new signed-out contact must not expose the protected history or silently lift a restriction. `auth.disabled` prevents new sign-in; it does not itself revoke previously issued refresh tokens, whose continued validity follows Poppy's rules. An SH declaration cannot override any of these access controls.

### 5.1 Representation

`representation` contains `poppy_user_ref`, `principal_ref`, and optionally `configurator_ref` and `affected_party_ref`. Use case-scoped, non-secret references. `principal_ref` MUST equal the declaration's top-level `principal_id`; any repeated principal in `authority_level` must also match. This object adds no field to SH's `authority_level`.

The Company MUST establish any material relationship between the Poppy User, authenticated account or representative, principal and affected resource through its trusted procedures. These references MUST NOT change the Session's authenticated identity, account, scopes or access to another person's case. An established representative permission may supply sufficient evidence; a configuration claim alone cannot.

### 5.2 Immutable declaration versions

For a given declaring party and case, an ID/revision pair identifies one immutable declaration. Reject a conflicting reuse; a material change requires a new revision. The Company MUST retain the exact UTF-8 declaration bytes it evaluated, or an authorised immutable reference, and bind their SHA-256 digest in its canonical assessment as required by SH §12.

For an inline JSON object, the receiver may create and store a UTF-8 representation once before evaluation; those stored bytes are then the evaluated artifact. This is a local binding, not a claim that arbitrary re-serialisations have the same digest or that the sender signed those bytes. Record source and transformation provenance. The wire format does not exchange or assert a cross-party digest. A signature scheme with its own canonicalisation must be handled separately and explicitly.

Handover and assessment records reference a declaration by role, ID and revision already available through an authorised path. An unresolved reference requires clarification; it MUST NOT be treated as empty terms or trigger unrestricted URL fetching.

## 6. Local assessment and exchanged summary

The Company MUST assess the particular proposal against both parties' relevant terms, current authority and applicable safeguards. All protected access and actions require the applicable checks, not only those using Operations. A preliminary hold may identify what is still needed; it is not approval. Follow SH §§8–9, 12–14 for evidence, local records and execution controls.

A Company-originated `assessment` record contains: `case_ref`, `assessment_ref`, `assessed_at`, optional `supersedes`, `decision`, `proposal`, `declaration_refs`, `reasons`, `responsible_role`, and `valid_until` when allowing. An `allow` requires both declaration references, one per party. A non-allow may carry only the known references, including none; its reasons MUST explain any missing declarations relevant to that decision. `proposal` identifies `proposal_ref`, `action_type`, `resource_ref` and, where applicable, the operation ID/revision. The actual offer and material terms must be available through the authorised conversation or operation; the reference is not an alternative place to hide terms.

| Decision | Effect |
|---|---|
| `allow` | The local assessment permits this specific proposal while its conditions remain satisfied. This summary alone is not an execution capability. |
| `deny` | Do not execute this proposal. A different acceptable remedy may still be considered. |
| `hold` | Do not execute; obtain the missing information or evidence described. |
| `escalate` | Do not execute under this assessment; use the designated human or specialist process. Preserve all concurrent holds and denials. |

Each non-allow summary MUST include at least one reason with `code`, `explanation` and `required_next_step`. Reasons MUST be truthful and useful while protecting private controls. Share only information the recipient is authorised to receive. SH reason categories describe service conditions; they MUST NOT reproduce hidden risk classifications or suggest ways to bypass a native decline. Do not add SH codes or fields to Poppy's native `declined` object, which deliberately has no reason-code field. A route to a person and an alternative are not replacement decision states. A compatible alternative gets a separate proposal and assessment. Human transfer does not lift a restriction.

The Company MUST keep its full trusted assessment separately from this summary, using SH's canonical assessment and verification requirements where the claimed profile requires them. An intake hold with missing declarations is recorded truthfully in the case record; do not fabricate bindings merely to produce a complete canonical assessment. An incoming summary cannot replace the trusted record. Share only necessary explanation and references; do not send internal verification records, private policy thresholds, raw evidence or private model reasoning merely because this extension is used. The Personal Agent MUST apply its own boundaries before agreeing to an action, regardless of a Company `allow`.

New evidence or changed circumstances require a new assessment record. `supersedes` names the earlier `assessment_ref` for the same proposal when applicable. Retain the history and make the current result available in the conversation before relying on it. A stale allowing message MUST NOT override a later restriction.

### 6.1 Proposal decisions and continuing service

A decision concerns the identified proposal, not whether the service request is resolved. The Company MUST NOT close a case merely because one offer is denied or held. It MUST consider compatible alternatives where available or explain the remaining route, subject to applicable safeguards and lawful obligations. An alternative uses a new `proposal_ref`, its own material terms and a fresh assessment; it MUST NOT overwrite the refused offer or inherit its approval. Link proposals through the same authorised `case_ref`.

The Personal Agent MAY continue exploring permitted options while a particular commitment is held. It MUST stay within the User's authority and boundaries. A human route is available where needed, not mandatory after every refusal. Automation limits, unresolved loops and safeguarding still apply. A hard boundary changes only through an authorised declaration revision and reassessment; an operation approval does not silently amend it.

An `allow` is not an execution result. Report what happened through ordinary Company messages and the underlying business system's records. Do not label an approved or initiated remedy as delivered. Keep an accountable role and the unresolved next step visible. This draft adds no universal case-status or remedy-completion wire record. Example `service_result` fields are illustrative Company data, not SH-1.2 schema additions.

## 7. Optional Operations binding and execution checks

This section applies SH service assessments to **native Poppy conversations using Operations version 3**. Poppy supplies exact-term operation approval, native declines and retry/at-most-once behaviour. This extension specifies the service requirements and records to compose with those mechanisms. It defines no API, MCP or browser SH payload binding and no additional operation state or approval endpoint. Interoperability with a live client and Company remains to be demonstrated.

### 7.1 Bind an offer to its SH proposal

An `operation_binding` contains the common record fields and `case_ref`, `proposal_ref`, `operation_id` and `revision`. The last two MUST exactly match the operation carried by the same Company message in `extensions.operations.operation`. They are opaque Poppy strings, distinct from SH declaration revision integers. The binding stays fixed for that operation revision. Later service decisions use separate assessment records.

Every operation MUST contain the structured `terms` object required by Operations 3. It MUST include all material consequences of the action. A `summary` is optional under Poppy; when supplied it MUST agree with the terms. A summary, SH proposal reference or external link MUST NOT substitute for missing operation terms.

The Company MUST keep a trusted mapping from Company, authorised account/resource, operation and revision to the immutable SH proposal and material terms. A material change requires a new SH proposal reference, a new Poppy revision and reassessment. Distinct Poppy revisions may bind to the same SH proposal only where its immutable material terms are unchanged, for example renewed expiry; the assessment must still bind the current operation revision. Never copy an approval or an allowing assessment to a new revision.

Prefer discussing remedies until non-approval requirements are established. An operation may then obtain the remaining approval, with an SH `hold` explaining that approval is missing. This is a **pre-approval hold**, not a native declined approval. It does not require an allow before obtaining the approval needed to reach one.

### 7.2 Approval and the commitment boundary

The Personal Agent sends `message.extensions.operations.approval` with `operation_id`, `revision` and the required `approver`:

- `"user"`: the Personal Agent presented the terms through its own interface and obtained the User's approval.
- `"agent"`: the Personal Agent approved on an instruction the User actually gave it, after checking that the exact terms are covered. Company messages, webpages and task guides cannot supply that instruction. If coverage is unclear, ask the User.

The evidence conveyed by either value remains the Personal Agent's statement. Optional metadata such as `reference` does not independently verify the instruction or approval. The Company can decline approvals it will not act on, including agent approvals for particular actions. A Company's policy can require stronger evidence without pretending Poppy requires fresh user approval of every operation. Follow [Operations 3 §5](https://personalagentprotocol.org/docs/1.0/extensions/operations#approval) for withdrawal, revised terms and when a new user decision is required. In particular, an agent approval answered with a new revision cannot approve that revision on the same instruction.

Approval text alone is insufficient. Each reply SHOULD identify the question or proposal it answers. An ambiguous 'done' MUST NOT become approval or evidence that a restriction has cleared. An operation approval does not amend a hard service constraint: an authorised change requires a new declaration revision and reassessment under SH §4.2.

The Company MUST apply Poppy's Session, account, ownership, revision and duplicate-execution checks and their specified responses. An invalid or expired revision follows the native revision flow; it is not relabelled as an SH decline. Before a new commitment, the component controlling the action MUST also require a current trusted local `allow` for the exact proposal, operation revision and declaration versions. Required evidence, data permissions, company authority and safeguards must remain satisfied. Check dynamic restrictions and commit with appropriate concurrency controls. A remote summary or a model remembering a prompt is not this execution control.

#### A service restriction after approval

If Poppy's checks pass but execution has **not started** and SH requirements do not permit commitment, the Company MUST perform nothing and use the native Operations 3 decline. In the conversation it sends:

- `extensions.operations.declined` identifying the approval's exact operation and revision, with an optional safe plain-language reason and alternative as defined by Poppy.
- An SH assessment identifying the same proposal/operation/revision and the current `deny`, `hold` or `escalate`, with the permitted service explanation and next step.

The records MAY share one Company message. A decline MUST NOT be accompanied by a new operation in that response. The native object contains no SH reason codes or private policy evidence. The Company MUST NOT record the declined approval as an accepted or usable approval for a later request. A necessary refusal audit record remains separate and cannot authorise execution.

The Personal Agent MUST NOT send the declined approval again. Changing a request ID, opening another conversation or obtaining a later allowing SH assessment does not revive it. Tell the User the action was not performed. A service case may remain open with permitted discussion and alternatives while that approval is unusable.

#### Continuing the case after a decline

Resolve the affected service requirement through an authorised process and record a new assessment. Do not execute silently when a hold clears. If the User wishes to continue and the Company can now offer the action, a **subsequent exchange** obtains a fresh operation revision and a fresh **user** approval. A changed material term also requires a new SH proposal. The Personal Agent MUST ask the User before approving that new revision, even if a prior instruction could otherwise cover it. A native decline response itself returns no new operation.

Keep the case link, outstanding restrictions and assessment history. A suitable alternative receives its own proposal and assessment; it does not inherit the declined approval. An assisted or human route remains available where appropriate and preserves the same requirements. This replaces the earlier extension's same-approval resume rule.

#### Retries and uncertain execution

For an action already started, completed or with an **unknown execution outcome**, do not send a decline claiming nothing happened. Follow Poppy's native retry and at-most-once rules and reconcile actual state. Retry a transport failure with the same request ID and approval as required; do not confuse an uncertain transport result with a confirmed native decline. On a duplicate completed request, return the known result without a second commitment.

A later service restriction does not rewrite an earlier effect. Do not open a new operation to evade uncertainty; recovery after a known effect is a separate authorised action. Expiry of an approval does not establish that its earlier use failed.

All execution paths to the same protected action MUST enforce applicable SH requirements. Advertising this conversation binding does not imply that the extension has defined payloads for other channels, or permit those channels to bypass a restriction.

### 7.3 Independent evidence and completion

Operation approval and independently checkable authority evidence are separate requirements. Trusted checks must cover the principal, representative or authenticated session, resource, exact action and material terms. For irreversible actions, SH §8.3 requires independent evidence under either profile; `approver: "user"` alone is no stronger proof than the Personal Agent's assertion.

Where the Company needs to observe the User's approval itself, use its authenticated website/app or another appropriate trusted process as [Operations §8.1](https://personalagentprotocol.org/docs/1.0/extensions/operations#approval-proof) explains. This extension does not create that approval channel. A previously verified, sufficiently scoped delegation can provide evidence for a representative's action; an assisted declaration or instruction reference cannot manufacture it.

Verified authority claims retain their additional checks. Keep the full trusted assessment separate from the minimised summary. After commitment, report actual execution and remaining service work. Arranging a replacement is not confirmation of delivery; neither an allow nor a transport acknowledgement proves the customer's goal is fulfilled.

## 8. Handover and continuity

The Company MUST provide the receiving staff role with the case, known represented/affected parties, proposal, relevant declaration versions, current assessment, each blocked action and reason, missing evidence or clarification, applicable data-use limits, necessary support instructions and accountable role. A `handover` wire record is a minimised summary, not proof of transfer or a substitute for delivery into the staff workflow.

Its fields are `case_ref`, `representation` when known, `proposal_refs`, `declaration_refs`, `restrictions`, `data_use_notes`, optional `support_instructions`, and `responsible_role`. Each restriction identifies its proposal, decision, reason, required next step and review condition. If material identity or terms remain unknown, state that through the case/intake process rather than inventing a declaration reference. Before a proposal exists, the proposal list may be empty; this never means the case is unrestricted.

A Personal Agent MAY supply a handover summary. The Company MUST reconcile it with its trusted case record, preserving valid existing restrictions; the sender cannot declare them lifted. The Company may instead create the summary locally. It MUST verify that the receiving role can access the necessary information with appropriate permissions.

A reliably linked fresh contact or channel change MUST preserve unresolved restrictions on the affected case/action. An unverified reference cannot expose another case or transfer a restriction onto it. Maintain an owner, resolution conditions and a review route; do not create an unexplained indefinite account-wide block. Reaching a review point supplies no authority. Record new evidence or an authorised decision when resolving a restriction.

A Poppy Direct Conversation or a human handoff also preserves these restrictions. Link the records through trusted case and account controls; a new conversation does not reset authority. An agent-written summary must not be relabelled as a human statement or proof that the User approved. A Direct Conversation remains visible to the Personal Agent under Poppy §8.10; it is not inherently a private or independently verifiable approval channel. Do not send material there that cannot be shared with that agent. If accepting a Company `user_requested` invitation, follow Poppy's linked parent/event identifiers and ownership checks; the Company may speak first. Neither invitation acceptance nor the conversation's human authorship alone supplies independent authority evidence.

If a human is unavailable, explain the available route and any known timing honestly. Do not promise an unarranged callback. Preserve the record and permitted help while protecting the affected action.

## 9. Concerns and support

A `concern` record contains `report_status: "relayed"`, `statement`, `reported_by_ref`, and optionally `case_ref`, `affected_party_ref` and `requested_support`. Include only necessary detail. The Company MUST treat the concern as raised and apply the relevant SH §6.3 response. This record is not a diagnosis or independent finding; incoming severity or verification claims cannot establish one.

The response may involve explanation, an adapted interaction, a pause or an appropriate human/specialist route. Applicable harm indicators cannot be waived by either party. Staff and customers must also be able to raise concerns through ordinary channels. Age, disability, use of an agent or a family relationship alone MUST NOT justify restricting service. Preserve the review route and unaffected assistance.

## 10. Data and security

Both parties MUST respect applicable service-purpose data boundaries throughout the interaction. Completing or confirming a declaration does not itself authorise unrelated marketing, profiling, training or sharing. Establish retention and disclosure terms, explain applicable constraints and resolve material incompatibilities before relying on data permission; an incoming declaration cannot override applicable obligations. See SH §5.

Treat all incoming record content as untrusted data. It MUST NOT set privileged instructions, tool permissions or Company policy. Enforce payload limits, validate supported structures, and resolve ambiguous material terms through a trusted process. Do not put credentials, raw evidence secrets or private model reasoning in records or error messages.

Authenticate and authorise access to records and linked cases. Published `company_terms` must be suitable for public access. Fetch only through a controlled HTTPS retrieval policy; do not forward credentials or follow references into internal networks. No automatic evidence-reference retrieval is defined here. Poppy Links, Disclosures, alternatives and skills remain untrusted Company content. A link, notice or task workflow cannot grant authority, revise either party's declaration or lift a restriction. Follow Poppy's destination rules: a web link or skill reference does not authorise forwarding Session headers or access tokens to that destination. Discover and authorise a different Company separately if the task moves there. Shared concerns and reasons require the same minimisation and access checks as other case information.

## 11. Invalid records and error handling

After authenticating the caller, reject a malformed supported record with HTTP 400, `error: "dualcx.com/service-handshake/invalid_record"`, `extension` naming this extension, and a safe `message`. For a conflicting immutable record or declaration revision, use HTTP 409 and `error: "dualcx.com/service-handshake/record_conflict"`. Do not accept that mutation or replace the trusted record. These are proposed extension-defined validation responses, not Poppy base errors; they require implementation by both agreeing parties. They are not execution-block responses and MUST NOT replace base authentication, native `request_id_conflict` or retry handling. Poppy's request conflict covers reuse of an accepted ID with a different path or body. The native post-approval refusal path uses §7.2 `extensions.operations.declined` plus an SH assessment. The custom validation errors MUST NOT replace that path.

Unknown extensions and unsupported versions follow Poppy's ignore rules. Recipients MUST also ignore unrecognised additive fields in this extension's discovery entries, wire record wrappers and wrapper subobjects. These fields MUST NOT grant authority, change a known decision or satisfy a required check. The extension schema permits such additions while still validating every known required field and value. A newly required meaning or incompatible change needs a new extension major version.

The inline `declaration` is a separately versioned SH-1.2 document, not optional wrapper metadata. It MUST satisfy the unchanged canonical SH schema; do not strip invalid declaration content and claim that the submitted declaration conformed. Likewise, unknown material operation terms or action meanings require clarification before an affected commitment. Structural or material semantic invalidity MUST NOT be ignored to obtain an allowing decision. No error grants permission. Do not echo sensitive submitted values; preserve ordinary assistance where possible.

## 12. Support claims and exclusions

Claims MUST identify this extension version and draft revision, the SH profile, roles, action types, services and execution paths covered, and whether Operations binding is supported. Verified authority claims must identify the evidence mechanisms covered. Schema acceptance does not establish conformance; a badge does not expand scope.

This proposal defines shared behaviour and exchange meaning. It does not issue credentials, decide legal validity, supply a vulnerability diagnosis, certify a system or specify Neos's private assessment method. It does not alter the underlying protocols by publication alone. Reference material and outstanding validation are listed in MAPPING.md, SOURCES.md and VALIDATION.md.


## 13. Optional service policy packs (informative)

Policy packs are a proposed future application alongside the framework. They could help organisations apply SH to a defined service situation by distinguishing applicable legal requirements, SH safeguards and discretionary company commitments. No policy pack, entitlement engine, new endpoint or policy-pack wire field is defined by this draft.

A company choosing to adopt a future pack should identify its publisher, version, jurisdiction and service/action scope, relevant exceptions, permitted variations, effective date and review owner. Adoption should be explicit; silence is not adoption. A pack reference may be explained in the ordinary conversation or linked public service terms using existing permitted fields; it must not be inserted as an unsupported field into the unchanged SH declaration schema. Poppy's optional Links extension can carry a relevant policy link when both parties support it. Its skill index can describe task workflows, but publishing a skill is not adoption of a policy pack and supplies no User approval. The Disclosures extension can identify relevant notices; transmission is not proof they were displayed, understood or accepted.

Identifying a pack would not establish compliance, customer consent, entitlement or delegated authority. Its applicability and the case facts would still need to be checked. No pack or company variation can override applicable mandatory rights, SH requirements or existing customer commitments. An uncertain or conflicting policy needs clarification before relying on it for the affected decision, while unrelated permitted assistance remains available.

Detailed pack contents and a machine-readable reference format should be developed from a bounded pilot and reviewed separately. Private company controls remain private. This section describes a direction for development, not an additional conformance level or a condition of participation.

## 14. Draft migration

Advertise extension major version `"3"` only when this wire draft and behaviour are implemented. Historical versions `"1"` and `"2"` remain distinct proposals; the extension's major version is not an SH edition or Poppy protocol version. Poppy is 1.0, Operations is 3 and the service framework remains SH-1.2.

Migrate discovery, request version headers, top-level request IDs, operation terms, approval provenance and decline/recovery behaviour together. Do not merely change a version label. Old records remain immutable under their original versions. A pending allow or approval does not acquire new meaning through migration: reassess the relevant action, retain unresolved restrictions and obtain any approval the new path requires.

This major version defines wire draft `2026-11-25`. Incompatible future wire or behavioural changes require a new major version; compatible editorial changes can retain this draft. Clients inspect the advertised draft before selecting the version and all received records are checked against it. No automatic fallback may remove a protected action's requirements. Unsupported counterparts retain proportionate assistance and the appropriate ordinary service route.

See [MIGRATION.md](MIGRATION.md) for the version-2 to version-3 mapping and [VALIDATION.md](VALIDATION.md) for what has and has not been tested.
