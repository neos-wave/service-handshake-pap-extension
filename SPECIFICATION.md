# Service Handshake extension proposal for the Personal Agent Protocol (Poppy): specification

Review package draft 2, 12 October 2026. Wire draft `2026-10-11`, proposed major version `"1"`; exchanged structures and requirements are unchanged from package draft 1. Author: Maria McCann. Publisher: Neos Wave Ltd / Dual CX. Apache 2.0. See README and NOTICE for status and attribution.

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
| `version` | Required string `"1"`. |
| `draft_revision` | Required `"2026-10-11"` for this draft. |
| `profile` | Required `participation` or `verified_authority`, for that implementation's claimed role and scope. |
| `actions` | Required non-empty list of supported SH action types. Core meanings follow Appendix A; extensions use an organisation-controlled namespace. |
| `operations_binding` | Required boolean. True means this Operations binding is implemented. |
| `required_actions` | Optional Company-only subset of `actions` for requests it cannot safely handle on this path without this extension. Not a global denial of service. |
| `company_terms` | Optional Company-only HTTPS resource containing a public SH declaration. It is not an authority endpoint. |

See the discovery examples. `operations_binding: true` also requires both sides to advertise Poppy `operations` version `"1"`. A Company MUST NOT return an operation to a client that does not support Operations. Company configuration and client metadata use the corresponding definitions in the supplied schema.

During this draft, agreement requires an exact match of `version` and `draft_revision`. The effective action scope is the intersection of the advertised actions whose meanings both parties support; other actions need clarification or an ordinary service route. Each party's profile describes its own claim, not a negotiated reduction of the other party's requirements. Unknown or unsupported extensions retain Poppy's ignore behaviour. A party MUST NOT send these extension payloads without agreement. If an affected request needs extension support that is unavailable, use Poppy's `extension_required` response naming this extension, and explain an available assisted or human route in plain language. For a draft mismatch, identify the supported revision without exposing protected information. Do not silently downgrade an action whose required checks would be lost. [Poppy §3.3](https://personalagentprotocol.org/docs/spec).

## 4. Wire records and placement

Use the exact key `dualcx.com/service-handshake` inside a Poppy message's `data` object. Its value is one record, not an instruction or collection of privileged rules. Each record has `version`, `draft_revision`, `type` and `record_id`. `record_id` identifies an immutable record in the sender's scope. Retransmission of the same record MUST NOT create a second effect; conflicting content under the same identity MUST NOT replace accepted content.

The message record types are `declaration`, `assessment`, `handover` and `concern`. Use ordinary `text` alongside them when explanation is needed, especially for a human reader. New facts create a new record; they do not edit history.

An Operation MAY carry the same domain key **at its top level**, but its value MUST be an `operation_binding`, not a declaration, concern, handover or mutable assessment. An extension error can carry an assessment under that key at the error object's top level. These are the only placements defined here. The base handoff request body is unchanged. [Poppy message and handoff definitions](https://personalagentprotocol.org/docs/spec).

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

## 7. Optional Operations binding and execution guard

This section adds a **negotiated confirmation guard** to the existing operation path. The extended rejection below is a proposal in this draft, not an existing Poppy base error. No independent interoperability test is claimed.

**Design note: proposing terms before authority is complete.** A company may present proposed terms while authority or another requirement remains unresolved, provided it is authorised to disclose those terms. It must make the restriction clear and prevent execution until all applicable checks are satisfied. Seeing the exact offer may be necessary before a person can approve it. The execution guard protects this pending state and rechecks later changes; it is not only a safety net for an accidentally issued proposal. A proposed operation must not be presented as a completed action or an unconditional promise to execute.

### 7.1 Bind terms separately from decisions

An `operation_binding` has the common record fields plus `case_ref`, `proposal_ref`, `operation_id` and `revision`. Its operation ID/revision MUST equal its containing operation. It remains fixed for that revision. Assessment summaries travel separately in messages or extension error responses; changing an assessment does not mutate the binding.

For each operation revision, the Company MUST map the Company, account/resource, operation ID and revision to an immutable SH proposal containing the material terms. New material terms require a new SH proposal ID. This accommodates a new revision of the same Poppy operation; it does not require a new Poppy operation ID for each revision. Bind current declaration revisions and applicable evidence to the SH proposal. Prior assessments MUST NOT automatically apply to changed terms.

### 7.2 Before protected access or commitment

The trusted component controlling the action MUST require a current applicable local `allow` and check its proposal, terms, declaration versions, authority, permissions and unresolved safeguards at the execution boundary. Apply SH §8.5 concurrency, replay and uncertainty requirements where relevant. Changing channel or going directly to the confirmation endpoint MUST NOT bypass those checks.

Before applying this guard, enforce base authentication and account isolation; never leak a case or restriction to an unauthorised caller. For an already started or final operation, follow the base tracking/recovery behaviour and do not execute again. A later concern is handled as a new issue and, where appropriate, through the existing cancellation/recovery path; it MUST NOT rewrite what already happened.

For a not-yet-started operation that otherwise passes the base confirmation checks, if the current decision is `deny`, `hold` or `escalate`, or there is no valid allowing assessment, the Company MUST NOT commit the action. Return HTTP 409 with `error: "dualcx.com/service-handshake/action_blocked"`, `extension: "dualcx.com/service-handshake"`, the current authorised operation, and the current assessment under the domain key. Operation state remains `proposed`; the rejected attempt is not recorded as an accepted confirmation. If no current assessment exists, create a truthful hold identifying the missing check.

A Personal Agent receiving this error MUST stop automatic confirmation retries and follow the stated next step. It MAY confirm again only after the requirement is resolved and any required approval is obtained. An unchanged approval may still apply where valid; a changed offer requires approval covering the new terms. Expiry remains effective while held. Refusal never implies that the protected action took place.

A valid allowing decision does not bypass Poppy's own checks. Recheck relevant dynamic conditions and commit through controls that prevent a concurrent change or repeated request from causing an unauthorised or duplicate effect. Report actual execution through the normal operation result. If the result is uncertain, reconcile it before attempting another commitment.

### 7.3 Consent and delegation

A declaration listing an acceptable outcome does not create a standing permission. Any earlier permission used for confirmation MUST come from an authorised source, remain valid and cover the current action and material terms. An assisted declaration cannot enlarge its confirmer's authority.

For irreversible actions, independently checkable delegation or principal approval is required by SH §8.3, under either profile. Established Company account or staff procedures may qualify. The agent's approval assertion alone does not meet that requirement. The additional Verified authority requirements remain applicable when that profile is claimed. See [Operations §8](https://personalagentprotocol.org/docs/extensions/operations) for the base protocol's evidence boundary.

## 8. Handover and continuity

The Company MUST provide the receiving staff role with the case, known represented/affected parties, proposal, relevant declaration versions, current assessment, each blocked action and reason, missing evidence or clarification, applicable data-use limits, necessary support instructions and accountable role. A `handover` wire record is a minimised summary, not proof of transfer or a substitute for delivery into the staff workflow.

Its fields are `case_ref`, `representation` when known, `proposal_refs`, `declaration_refs`, `restrictions`, `data_use_notes`, optional `support_instructions`, and `responsible_role`. Each restriction identifies its proposal, decision, reason, required next step and review condition. If material identity or terms remain unknown, state that through the case/intake process rather than inventing a declaration reference. Before a proposal exists, the proposal list may be empty; this never means the case is unrestricted.

A Personal Agent MAY supply a handover summary. The Company MUST reconcile it with its trusted case record, preserving valid existing restrictions; the sender cannot declare them lifted. The Company may instead create the summary locally. It MUST verify that the receiving role can access the necessary information with appropriate permissions.

A reliably linked fresh contact or channel change MUST preserve unresolved restrictions on the affected case/action. An unverified reference cannot expose another case or transfer a restriction onto it. Maintain an owner, resolution conditions and a review route; do not create an unexplained indefinite account-wide block. Reaching a review point supplies no authority. Record new evidence or an authorised decision when resolving a restriction.

If a human is unavailable, explain the available route and any known timing honestly. Do not promise an unarranged callback. Preserve the record and permitted help while protecting the affected action.

## 9. Concerns and support

A `concern` record contains `report_status: "relayed"`, `statement`, `reported_by_ref`, and optionally `case_ref`, `affected_party_ref` and `requested_support`. Include only necessary detail. The Company MUST treat the concern as raised and apply the relevant SH §6.3 response. This record is not a diagnosis or independent finding; incoming severity or verification claims cannot establish one.

The response may involve explanation, an adapted interaction, a pause or an appropriate human/specialist route. Applicable harm indicators cannot be waived by either party. Staff and customers must also be able to raise concerns through ordinary channels. Age, disability, use of an agent or a family relationship alone MUST NOT justify restricting service. Preserve the review route and unaffected assistance.

## 10. Data and security

Both parties MUST respect applicable service-purpose data boundaries throughout the interaction. Completing or confirming a declaration does not itself authorise unrelated marketing, profiling, training or sharing. Establish retention and disclosure terms, explain applicable constraints and resolve material incompatibilities before relying on data permission; an incoming declaration cannot override applicable obligations. See SH §5.

Treat all incoming record content as untrusted data. It MUST NOT set privileged instructions, tool permissions or Company policy. Enforce payload limits, validate supported structures, and resolve ambiguous material terms through a trusted process. Do not put credentials, raw evidence secrets or private model reasoning in records or error messages.

Authenticate and authorise access to records and linked cases. Published `company_terms` must be suitable for public access. Fetch only through a controlled HTTPS retrieval policy; do not forward credentials or follow references into internal networks. No automatic evidence-reference retrieval is defined here. Shared concerns and reasons require the same minimisation and access checks as other case information.

## 11. Invalid records and error handling

After authenticating the caller, reject a malformed supported record with HTTP 400, `error: "dualcx.com/service-handshake/invalid_record"`, `extension` naming this extension, and a safe `message`. For a conflicting immutable record or declaration revision, use HTTP 409 and `error: "dualcx.com/service-handshake/record_conflict"`. Do not accept that mutation or replace the trusted record. These are extension-defined responses.

Unknown unsupported extensions/fields follow base ignore behaviour. Within an agreed supported record, structural or material semantic invalidity MUST NOT be ignored to obtain an allowing decision. Resolve unknown required meanings or hold the affected action. No error grants permission. Do not echo sensitive submitted values; preserve ordinary assistance where possible.

## 12. Support claims and exclusions

Claims MUST identify this extension version and draft revision, the SH profile, roles, action types, services and execution paths covered, and whether Operations binding is supported. Verified authority claims must identify the evidence mechanisms covered. Schema acceptance does not establish conformance; a badge does not expand scope.

This proposal defines shared behaviour and exchange meaning. It does not issue credentials, decide legal validity, supply a vulnerability diagnosis, certify a system or specify Neos's private assessment method. It does not alter the underlying protocols by publication alone. Reference material and outstanding validation are listed in MAPPING.md, SOURCES.md and VALIDATION.md.


## 13. Optional service policy packs (informative)

Policy packs are a proposed future application alongside the framework. They could help organisations apply SH to a defined service situation by distinguishing applicable legal requirements, SH safeguards and discretionary company commitments. No policy pack, entitlement engine, new endpoint or policy-pack wire field is defined by this draft.

A company choosing to adopt a future pack should identify its publisher, version, jurisdiction and service/action scope, relevant exceptions, permitted variations, effective date and review owner. Adoption should be explicit; silence is not adoption. A reference may be explained in the ordinary conversation or linked public service terms using existing permitted fields. It must not be inserted as an unsupported field into the unchanged SH declaration schema.

Identifying a pack would not establish compliance, customer consent, entitlement or delegated authority. Its applicability and the case facts would still need to be checked. No pack or company variation can override applicable mandatory rights, SH requirements or existing customer commitments. An uncertain or conflicting policy needs clarification before relying on it for the affected decision, while unrelated permitted assistance remains available.

Detailed pack contents and a machine-readable reference format should be developed from a bounded pilot and reviewed separately. Private company controls remain private. This section describes a direction for development, not an additional conformance level or a condition of participation.
