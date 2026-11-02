# Service Handshake extension proposal for the Personal Agent Protocol (Poppy): specification

Review package draft 4, 2 November 2026. Wire draft `2026-11-02-r4`, proposed major version `"2"`. Targets Poppy draft 0.3 and Operations version 2 at the source revision pinned in SOURCES.md. This is an incompatible update to the earlier extension proposal, not a new SH edition. Independent proposal; not adopted by Poppy or demonstrated through a live integration. Author: Maria McCann. Publisher: Neos Wave Ltd / Dual CX. Apache 2.0. See README and NOTICE for status and attribution.

## 1. Scope and precedence

This specification binds Service Handshake SH-1.2 to native Poppy conversations, with an optional Operations binding. Poppy's authentication, permissions and base errors remain applicable. This extension supplies additional requirements for implementations that agree to use it; it does not make a core Poppy error or state mean something different.

SH-1.2 requirements continue to apply to an SH conformance claim. This draft does not relax them or redefine its two profiles. It adds machine-exchange and binding requirements for adopters of this extension; those are not new requirements for every SH Participation implementation. The published SH declaration and assessment schemas are unchanged. The exchange schemas describe an additional format, not a replacement canonical assessment or authority credential.

Uppercase MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have their BCP 14 meanings. The normative SH references below are to the **Technical Specification** unless the main paper is named. In this draft, the prose defines behavioural requirements; the schema defines structural requirements. If they disagree, hold the affected protected action and report the defect rather than treating validation as permission.

## 2. Terms and trust

Poppy's User, Personal Agent, Company, Session and Operation retain their meanings. A **principal** is the represented party for the proposed act. A **configurator** set up the agent and may have no authority over that act. A **proposal** is a specific immutable action and its material terms. An **assessment** is a trusted local decision. An **assessment summary** communicates a limited view of that decision; the recipient cannot treat it as a credential or permission to exceed its own boundaries.

The Company MUST derive sender identity and access from its trusted protocol context, not fields supplied in a payload. `party_role`, representation references and case references are claims until appropriately bound to that context. A Personal Agent MAY prepare terms for its own User; that does not make them an assisted declaration.

## 3. Discovery and agreement

Both sides advertise `dualcx.com/service-handshake` under Poppy's `extensions`. The entry has these fields:

| Field | Meaning |
|---|---|
| `version` | Required string `"2"`. |
| `draft_revision` | Required `"2026-11-02-r4"` for this draft. |
| `profile` | Required `participation` or `verified_authority`, for that implementation's claimed role and scope. |
| `actions` | Required non-empty list of supported SH action types. Core meanings follow Appendix A; extensions use an organisation-controlled namespace. |
| `operations_binding` | Required boolean. True means this Operations binding is implemented. |
| `required_actions` | Optional Company-only subset of `actions` for requests it cannot safely handle on this path without this extension. Not a global denial of service. |
| `company_terms` | Optional Company-only HTTPS resource containing a public SH declaration. It is not an authority endpoint. |

See the discovery examples. `operations_binding: true` also requires both sides to advertise Poppy `operations` version `"2"`. A Company MUST NOT return an operation to a client that does not support Operations. Company configuration and client metadata use the corresponding definitions in the supplied schema.

During this draft, agreement requires an exact match of `version` and `draft_revision`. The effective action scope is the intersection of the advertised action categories whose meanings both parties support (for example `refund`, not the different role verbs `offer_refund` and `accept_refund`); other actions need clarification or an ordinary service route. Each party's profile describes its own claim, not a negotiated reduction of the other party's requirements. Unknown or unsupported extensions retain Poppy's ignore behaviour. A party MUST NOT send these extension payloads without agreement. If an affected request needs extension support that is unavailable, use Poppy's `extension_required` response naming this extension, and explain an available assisted or human route in plain language. For a draft mismatch, identify the supported revision without exposing protected information. Do not silently downgrade an action whose required checks would be lost. [Poppy §3.3](https://personalagentprotocol.org/docs/spec).

## 4. Wire records and placement

Use the exact key `dualcx.com/service-handshake` inside a Poppy message's `extensions` object, as required by Poppy §§3.3 and 8.4. The published [exchange schema](schema/sh-poppy-extension.schema.json) validates that key's value; it uses JSON Schema 2020-12 and references the unchanged SH reference schemas. The extension value is one record, not an instruction or collection of privileged rules. Each record has `version`, `draft_revision`, `type` and `record_id`. `record_id` identifies an immutable record in the sender's scope. Retransmission of the same record MUST NOT create a second effect; conflicting content under the same identity MUST NOT replace accepted content.

The message record types are `declaration`, `assessment`, `handover`, `concern` and `operation_binding`. Use ordinary `text` and, where appropriate, ordinary `data` to carry the message's meaning; extension records add structured service context. A recipient that ignores an unsupported extension must still receive an intelligible account of the proposal, restriction and next step. Never rely on a structured record alone to communicate material terms or a restriction to a person. New facts create a new record; they do not edit history.

An `operation_binding` belongs in `message.extensions["dualcx.com/service-handshake"]`, alongside `message.extensions.operations.operation` in the same Company message. It MUST NOT be attached inside the operation object. Other SH records use the same domain-named extension slot, in separate messages when necessary. `message.data` remains available for ordinary Company-defined business details, such as the illustrative `service_result`. It is not an alternative location for this extension's records. Legacy top-level `operation` or `approval` fields MUST NOT be interpreted as current Operations content, and SH records in legacy locations MUST NOT satisfy this binding. If an action depends on a valid SH record that is missing, keep the affected action restricted while explaining the correction needed. No new base endpoint, operation state, approval field or handoff body is introduced.

Messages and events MUST follow the pinned Poppy envelope and author rules. A Personal Agent supplies `author.type: "agent"`; the Company records `role` on events. Derive which party sent a record from the authenticated protocol context, not a claimed role. Only the Company may originate a trusted assessment summary or operation binding. Client-supplied versions of those records MUST NOT become Company decisions. Base schema validity does not establish this provenance.

## 5. Declarations and assistance

A `declaration` record includes `party_role`, an inline `declaration` conforming to the unchanged SH-1.2 schema, and optional `case_ref` and `representation`. This binding additionally requires `declaration_id` and `declaration_revision` for each exchanged declaration. Do not fabricate a principal or goal to meet those fields: use an ordinary intake conversation until they can truthfully be recorded.

AI status and representation MUST be disclosed at first contact. Relevant known terms SHOULD be supplied early; a full declaration in the first message is not required. Protected information and actions remain subject to the checks they need. A party MUST present material assisted terms for correction and confirmation, preserving unknowns and refusals.

The Company MUST offer proportionate assistance where the other side lacks a usable declaration, whether or not that side advertises this extension. This applies under both profiles. For an unsupported agent, use plain-language participation without an extension payload. Declining assistance alone MUST NOT terminate ordinary service; preserve permitted help and an accessible human route. Assistance does not waive account access checks.

Provenance retains SH §2.3 meanings: self-declared terms, previously agreed terms, or terms prepared with the other party's assistance. A party preparing an assisted declaration for the other side MUST record its actual confirmation status and provenance; it MUST NOT impersonate that party or manufacture confirmation. Confirmation establishes the claimed terms, not delegation.

Both parties' relevant boundaries MUST be established before a protected action. The Company MAY publish general terms at `company_terms` or send appropriate case terms through the conversation. It need not disclose private thresholds. A public policy is not proof of case-specific authority. Where the Personal Agent is the supporting party, its assisted record of Company statements remains unconfirmed until appropriately confirmed by the Company.

### 5.1 Representation

`representation` contains `poppy_user_ref`, `principal_ref`, and optionally `configurator_ref` and `affected_party_ref`. Use case-scoped, non-secret references. `principal_ref` MUST equal the declaration's top-level `principal_id`; any repeated principal in `authority_level` must also match. This object adds no field to SH's `authority_level`.

The Company MUST establish any material relationship between the Poppy User, authenticated account or representative, principal and affected resource through its trusted procedures. These references MUST NOT change the Session's authenticated identity, account, scopes or access to another person's case. An established representative permission may supply sufficient evidence; a configuration claim alone cannot.

### 5.2 Immutable declaration versions

For a given declaring party and case, an ID/revision pair identifies one immutable declaration. Reject a conflicting reuse; a material change requires a new revision. The Company MUST retain the exact UTF-8 declaration bytes it evaluated, or an authorised immutable reference, and bind their SHA-256 digest in its canonical assessment as required by SH §12.

For an inline JSON object, the receiver may create and store a UTF-8 representation once before evaluation; those stored bytes are then the evaluated artifact. This is a local binding, not a claim that arbitrary re-serialisations have the same digest or that the sender signed those bytes. Record source and transformation provenance. The wire format does not exchange or assert a cross-party digest. A signature scheme with its own canonicalisation must be handled separately and explicitly.

Handover and assessment records reference a declaration by role, ID and revision already available through an authorised path. An unresolved reference requires clarification; it MUST NOT be treated as empty terms or trigger unrestricted URL fetching.

### 5.3 Signed-out Sessions and unavailable sign-in

A Poppy Session starts signed out and may stay that way (Poppy §§2, 5). Where the Company permits signed-out contact, the parties MAY use this extension for intake, declarations that need no account access and general assistance. SH does not override the Company's access rules. Signed-out contact MUST NOT expose account or case details, link the contact to an existing account case or continue a conversation that already uses an account; Poppy's ownership and sign-in rules apply to those (Poppy §§8.2, 8.11).

Missing access restricts the affected action, not the whole contact. A proposal whose required account access, authority evidence or other check is unavailable is held, with a reason and next step. Permitted assistance and an appropriate human route remain available.

`auth.disabled` prevents new Direct, Device and Mediated Sign-In. It does not by itself revoke refresh tokens issued earlier; they keep working until the Company revokes them (Poppy §§3.2, 4.4). A Company refusing sign-in to a particular Personal Agent with `unauthorized_client` leaves that agent signed out (Poppy §4.1). In each case the Company evaluates the access actually held in the current Session, not the access advertised or expected. A declaration, assessment summary or company terms document never substitutes for sign-in.

## 6. Local assessment and exchanged summary

The Company MUST assess the particular proposal against both parties' relevant terms, current authority and applicable safeguards. All protected access and actions require the applicable checks, not only those using Operations. A preliminary hold may identify what is still needed; it is not approval. Follow SH §§8–9, 12–14 for evidence, local records and execution controls.

A Company-originated `assessment` record contains: `case_ref`, `assessment_ref`, `assessed_at`, optional `supersedes`, `decision`, `proposal`, `declaration_refs`, `reasons`, `responsible_role`, and `valid_until` when allowing. An `allow` requires both declaration references, one per party. A non-allow may carry only the known references, including none; its reasons MUST explain any missing declarations relevant to that decision. `proposal` identifies `proposal_ref`, `action_type`, `resource_ref` and, where applicable, the operation ID/revision. The actual offer and material terms must be available through the authorised conversation or operation; the reference is not an alternative place to hide terms.

| Decision | Effect |
|---|---|
| `allow` | The local assessment permits this specific proposal while its conditions remain satisfied. This summary alone is not an execution capability. |
| `deny` | Do not execute this proposal. A different acceptable remedy may still be considered. |
| `hold` | Do not execute; obtain the missing information or evidence described. |
| `escalate` | Do not execute under this assessment; use the designated human or specialist process. Preserve all concurrent holds and denials. |

Each non-allow summary MUST include at least one reason with `code`, `explanation` and `required_next_step`. Reasons MUST be truthful and useful while protecting private controls. A route to a person and an alternative are not replacement decision states. A compatible alternative gets a separate proposal and assessment. Human transfer does not lift a restriction.

The Company MUST keep its full trusted assessment separately from this summary, using SH's canonical assessment and verification requirements where the claimed profile requires them. An intake hold with missing declarations is recorded truthfully in the case record; do not fabricate bindings merely to produce a complete canonical assessment. An incoming summary cannot replace the trusted record. Share only necessary explanation and references; do not send internal verification records, private policy thresholds, raw evidence or private model reasoning merely because this extension is used. The Personal Agent MUST apply its own boundaries before agreeing to an action, regardless of a Company `allow`.

New evidence or changed circumstances require a new assessment record. `supersedes` names the earlier `assessment_ref` for the same proposal when applicable. Retain the history and make the current result available in the conversation before relying on it. A stale allowing message MUST NOT override a later restriction.

### 6.1 Proposal decisions and continuing service

A decision concerns the identified proposal, not whether the service request is resolved. The Company MUST NOT close a case merely because one offer is denied or held. It MUST consider compatible alternatives where available or explain the remaining route, subject to applicable safeguards and lawful obligations. An alternative uses a new `proposal_ref`, its own material terms and a fresh assessment; it MUST NOT overwrite the refused offer or inherit its approval. Link proposals through the same authorised `case_ref`.

The Personal Agent MAY continue exploring permitted options while a particular commitment is held. It MUST stay within the User's authority and boundaries. A human route is available where needed, not mandatory after every refusal. Automation limits, unresolved loops and safeguarding still apply. A hard boundary changes only through an authorised declaration revision and reassessment; an operation approval does not silently amend it.

An `allow` is not an execution result. Report what happened through ordinary Company messages and the underlying business system's records. Do not label an approved or initiated remedy as delivered. Keep an accountable role and the unresolved next step visible. This draft adds no universal case-status or remedy-completion wire record. Example `service_result` fields are illustrative Company data, not SH-1.2 schema additions.

## 7. Optional Operations binding and execution checks

This section defines an additional, negotiated SH precondition for commitment in **native conversations only**. It does not claim that core Poppy already enforces SH, and does not define an API, MCP or browser binding. The composition of a post-approval SH block with Operations is an explicit design proposal requiring implementer review. Nothing here changes how unextended Operations behaves.

### 7.1 Bind an offer to its SH proposal

An `operation_binding` contains the common record fields and `case_ref`, `proposal_ref`, `operation_id` and `revision`. The last two MUST exactly match the operation carried by the same Company message. They are opaque Poppy strings, distinct from SH declaration revision integers. The binding stays fixed for that operation revision. A later decision travels in a separate assessment message.

The Company MUST maintain a trusted mapping from Company, authorised account/resource, operation and revision to the immutable SH proposal and material terms. A material change requires a new SH proposal reference and reassessment. Changes that require a new Poppy revision MUST receive one; the Company MUST NOT reuse a revision for different content. Distinct revisions may bind to the same SH proposal only where its immutable material terms are unchanged, for example a changed approval expiry, and assessments must still bind the current operation revision. Do not copy an earlier approval or assessment to a new revision.

Prefer discussing proposed remedies in ordinary messages until non-approval requirements are established. An operation may be issued to obtain the remaining approval, with a corresponding `hold` explaining what is pending. This avoids requiring an `allow` before the approval needed to reach it. Explain any other unresolved requirement clearly; the offer must not promise unconditional execution.

### 7.2 Approval and the commitment boundary

Implement the pinned Operations approval rules, including user approval of each operation revision. Standing delegation or a prior general instruction does not replace that step. In this conversation binding the Personal Agent sends `message.extensions.operations.approval`, naming the operation and revision. Approval text alone is insufficient. Both parties SHOULD make each reply explicit about the question or proposal it addresses. An ambiguous reply such as 'done' MUST NOT be treated as approval or as evidence that a hold has cleared; seek clarification and preserve the restriction. This applies Poppy's explicit-reply guidance at the SH decision boundary. Authentication, authorised account/resource binding, valid operation terms and base retry protections remain prerequisites.

On receiving approval, the Company MUST assess it with the current SH requirements. The trusted component controlling the action MUST require a current local `allow` for the exact proposal, operation revision and declaration versions before commitment. Required independent evidence, data permissions, company authority and safeguards must remain satisfied. A summary from the counterparty is never the trusted assessment. Check dynamic restrictions and commit atomically with appropriate concurrency protection; never make a prompt responsible for enforcement.

If execution has **not started** and the decision is `deny`, `hold` or `escalate`, or no valid allow exists, the Company MUST NOT execute. It records or creates the truthful assessment and sends a Company message containing that summary and a plain-language account of what did not happen and what is needed next. The transport may acknowledge receipt of the approval message; receipt is not commitment. This draft does **not** return the old custom HTTP 409 confirmation error, create a confirmation endpoint or claim that the operation remains in a base state named `proposed`.

An agent receiving this response MUST stop automatic approval retries and follow the next step. When the requirement is resolved, the Company MUST reassess and tell the agent that it can retry the same operation/revision if still valid. Do not resume execution silently after a reported hold. The agent MUST establish that the User has not withdrawn approval before retrying. Changed terms or expiry require the applicable new operation revision and user approval. If the service cannot establish a safe route, preserve the restriction and offer an appropriate human route.

For an operation already started, completed or with an **unknown execution outcome**, this not-started response MUST NOT be used. Follow the base retry and at-most-once requirements and reconcile actual state. A later restriction does not rewrite an earlier effect. Do not open a fresh operation to evade uncertainty; appropriate recovery is a separate authorised action. On a duplicate completed request, return the known result without a second commitment. Expired approval does not prove that an earlier attempt failed.

All execution paths to the same protected action MUST enforce the applicable SH controls. Advertising only this conversation binding does not authorise bypass through another channel. No support for extension payloads on those other channels is implied.

### 7.3 Independent evidence and completion

Operation approval and independently checkable authority evidence are separate requirements. The Company's trusted evidence checks MUST cover the principal, representative or authenticated session, affected resource, exact action and material terms. For irreversible actions the independent-evidence requirement in SH §8.3 applies under either profile; an agent's approval assertion alone is insufficient. Existing trusted company processes may qualify. An assisted declaration cannot expand authority. See Operations §8.1 for the base evidence limit.

Verified authority claims retain all their additional checks. Record the trusted assessment separately from the minimised summary. After commitment, report actual execution and any remaining service work; arranging a replacement is not confirmation of delivery. No success claim may be inferred solely from an allow or transport acknowledgement.

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

After authenticating the caller, reject a malformed supported record with HTTP 400, `error: "dualcx.com/service-handshake/invalid_record"`, `extension` naming this extension, and a safe `message`. For a conflicting immutable record or declaration revision, use HTTP 409 and `error: "dualcx.com/service-handshake/record_conflict"`. Do not accept that mutation or replace the trusted record. These are proposed extension-defined validation responses, not Poppy base errors; they require implementation by both agreeing parties. They are not execution-block responses and MUST NOT replace base authentication, message-ID-conflict or retry handling. The package's normal action-block path uses §7.2 assessment messages.

Unknown unsupported extensions/fields follow base ignore behaviour. Within an agreed supported record, structural or material semantic invalidity MUST NOT be ignored to obtain an allowing decision. Resolve unknown required meanings or hold the affected action. No error grants permission. Do not echo sensitive submitted values; preserve ordinary assistance where possible.

## 12. Support claims and exclusions

Claims MUST identify this extension version and draft revision, the SH profile, roles, action types, services and execution paths covered, and whether Operations binding is supported. Verified authority claims must identify the evidence mechanisms covered. Schema acceptance does not establish conformance; a badge does not expand scope.

This proposal defines shared behaviour and exchange meaning. It does not issue credentials, decide legal validity, supply a vulnerability diagnosis, certify a system or specify Neos's private assessment method. It does not alter the underlying protocols by publication alone. Reference material and outstanding validation are listed in MAPPING.md, SOURCES.md and VALIDATION.md.


## 13. Optional service policy packs (informative)

Policy packs are a proposed future application alongside the framework. They could help organisations apply SH to a defined service situation by distinguishing applicable legal requirements, SH safeguards and discretionary company commitments. No policy pack, entitlement engine, new endpoint or policy-pack wire field is defined by this draft.

A company choosing to adopt a future pack should identify its publisher, version, jurisdiction and service/action scope, relevant exceptions, permitted variations, effective date and review owner. Adoption should be explicit; silence is not adoption. A pack reference may be explained in the ordinary conversation or linked public service terms using existing permitted fields; it must not be inserted as an unsupported field into the unchanged SH declaration schema. Poppy's optional Links extension can carry a relevant policy link when both parties support it. Its skill index can describe task workflows, but publishing a skill is not adoption of a policy pack and supplies no User approval. The Disclosures extension can identify relevant notices; transmission is not proof they were displayed, understood or accepted.

Identifying a pack would not establish compliance, customer consent, entitlement or delegated authority. Its applicability and the case facts would still need to be checked. No pack or company variation can override applicable mandatory rights, SH requirements or existing customer commitments. An uncertain or conflicting policy needs clarification before relying on it for the affected decision, while unrelated permitted assistance remains available.

Detailed pack contents and a machine-readable reference format should be developed from a bounded pilot and reviewed separately. Private company controls remain private. This section describes a direction for development, not an additional conformance level or a condition of participation.

## 14. Draft migration

Do not advertise version `"2"` unless the version-2 exchange and behaviours are implemented. Version `"1"` and draft `2026-10-11` remain a distinct historical proposal. Update stored operation references and message placement deliberately; do not coerce an integer revision into a string and assume it identifies a current operation. Never reinterpret an old allowing record as permission under the new binding. Draft `2026-11-02-r4` supersedes the earlier version-2 draft `2026-11-02` and is not wire-compatible with it. The draft identifier is an opaque string; the suffix distinguishes two revisions issued on the same date. Exact version/draft agreement remains required during review. Unsupported counterparts retain accessible assistance and the applicable ordinary service route.
