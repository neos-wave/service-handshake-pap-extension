# Worked service journeys and example files

All people, companies, identifiers and evidence references are fictional. These fixtures illustrate exchange and sequence. They do not contact a service, authenticate a person, verify delegation or carry out an action. Dates are fixed for repeatable checks, not live validity windows.

The examples use **Poppy 1.0**, **Operations version 3**, and the independent **Service Handshake extension version 3, wire draft 2026-11-25**. Package review 6 is a documentation/review identifier, not a protocol field. The underlying Service Handshake edition remains SH-1.2.

## Discovery and request context

- [company-discovery.json](company-discovery.json) advertises extension versions as arrays and describes its conversation endpoint, supported SH actions and profile. It offers Operations through conversations, so it advertises no website Operations endpoint.
- [client-metadata.json](client-metadata.json) contains OAuth client metadata only. It does not negotiate extension support.
- [request-negotiation.json](request-negotiation.json) is a **local fixture harness record**, not a Poppy request body. Its `headers` illustrate HTTP headers; `body_file` identifies the JSON body. `local_support` records the personal agent's local capabilities for offline checks and is never sent as a wire field. The Session value is deliberately not a valid JWT.

The agent checks that the company's version-3 SH entry advertises the exact supported wire draft, then selects that extension in the ordinary Poppy header:

```http
Poppy-Version: 1.0
Poppy-Extensions: "dualcx.com/service-handshake";v="3", "operations";v="3"
```

There is no extra draft-negotiation header. Selecting this SH version asserts support for its advertised `2026-11-25` wire draft; each SH payload carries that exact `draft_revision`. The company profile describes its supported requirements; the header does not negotiate or upgrade it. An incompatible future wire draft needs a new extension major version. Changing protocol or extension versions requires a new Session under Poppy's rules.

[manifest.json](manifest.json) identifies each complete Poppy envelope and nested SH record. SH content belongs in `message.extensions["dualcx.com/service-handshake"]`; Operations content belongs in `message.extensions.operations`. Ordinary company-defined service data stays in `message.data`. Request IDs are fixed examples generated with 128 random bits. The agent sends the ID at the request's top level, with no `id` or `role` in the nested message. Company events retain their message IDs and roles. Retrying a request reuses its ID; changing that ID never revives a declined approval.

## 1. A damaged order: refund or replacement

The customer received a damaged kettle. They prefer a full refund, would accept an equivalent replacement, refuse credit and require approval before committing to replacement terms. Their declaration describes those instructions; the company establishes the required authority separately.

| Step | File | Meaning |
|---|---|---|
| Customer terms | [message-declaration.json](message-declaration.json) | Customer declaration; authority evidence unresolved. |
| Company terms | [company-declaration.json](company-declaration.json) | Company declaration and boundaries. |
| Refuse one remedy | [voucher-denied.json](voucher-denied.json) | DENY the voucher; keep the damaged-order case open. |
| Explore an acceptable option | [replacement-request.json](replacement-request.json) | Discuss an equivalent replacement; retain the refund option. |
| Present exact terms | [replacement-operation.json](replacement-operation.json) | Native operation with required JSON `terms`, matching summary and separate SH binding. |
| Identify what is missing | [replacement-hold.json](replacement-hold.json) | A **pre-approval HOLD** for approval and authority evidence, not a Poppy decline. |
| Obtain approval | [replacement-approval.json](replacement-approval.json) | `approver: "user"` reports the customer's decision through the agent's own interface. |
| Revise claimed authority | [delivery-declaration-revised.json](delivery-declaration-revised.json) | Preserve boundaries; the evidence reference is still a claim until checked. |
| Assess after trusted checks | [replacement-allow.json](replacement-allow.json) | ALLOW supersedes the replacement hold, not the voucher denial. |
| Report execution | [replacement-arranged.json](replacement-arranged.json) | Arrangement is confirmed; delivery and resolution remain outstanding. |
| Report service completion | [replacement-delivered.json](replacement-delivered.json) | Illustrative delivery evidence and customer confirmation support closure. |

Between approval and ALLOW, the company independently verifies the evidence its service controls require, checks its own authority and policy, and records its canonical assessment. This trusted process is not supplied as a personal-agent assertion or runnable code. Poppy's approval does not independently prove how approval was obtained. If a valid approval cannot be acted on, apply Operations' native decline rules; do not turn the pre-approval hold into an approval-retry loop.

Operation approval does not waive a customer boundary. Changed material terms require the applicable new proposal, revision, assessment and approval. Discussing an alternative is not accepting it. Declining replacement leaves a refund or another permitted route to consider; it does not authorise credit.

`service_result` is ordinary company-defined example data, not a new SH or Poppy record. Arrangement and delivery are separate business events. These fixtures add no universal delivery-confirmation or refund-receipt requirement to SH-1.2.

## 2. Priya's mother's broadband: authority and continuity

Priya has recognised billing access. The account is her mother's; this is not use of her mother's login. Cancellation authority and continuity of any essential alarm need separate checks.

1. [family-declaration.json](family-declaration.json), [family-company-declaration.json](family-company-declaration.json) and [assessment-hold.json](assessment-hold.json) establish terms and a cancellation hold. Discussing the proposal needs no Poppy operation.
2. [relayed-concern.json](relayed-concern.json) reports a possible alarm dependency. Treat it as raised, not independently verified. [assessment-escalate.json](assessment-escalate.json) records the specialist route while preserving the authority hold; [handover.json](handover.json) carries both restrictions and support instructions. Handover grants no authority.
3. **Conditional safe branch:** the provider independently establishes limited delegation, resolves the alarm concern and checks continuity. [family-declaration-revised.json](family-declaration-revised.json) records revised claims, not proof. [operation-message.json](operation-message.json) presents exact cancellation terms as JSON and a matching summary.
4. [family-approval.json](family-approval.json) reports Priya's user approval. This is not her mother's delegation. [assessment-after-evidence.json](assessment-after-evidence.json) illustrates ALLOW only after both and the remaining checks pass. It reports no completed cancellation.

### Late concern: decline the approval, keep the service case open

[approval-blocked-message.json](approval-blocked-message.json) is a separate branch: a new alarm concern arrives **before commitment**, and the company knows the action was not performed. The message combines native `extensions.operations.declined` with an SH HOLD that supersedes the earlier ALLOW for the same proposal. It contains **no new operation**.

The decline is final for that approval: **the agent must not send it again**. The case remains open for review and permitted assistance. The alternative is information for the user, not a company instruction that expands the agent's authority. SH reason codes describe disclosed service conditions; they do not expose private risk rules or authorise workarounds.

If execution has started or its result is uncertain, this decline fixture is inappropriate. Reconcile the existing operation using Poppy's retry and at-most-once protections. Do not claim nothing happened or approve a fresh operation to retry blindly.

### Later recovery requires a fresh user decision

| Step | File | Meaning |
|---|---|---|
| User asks to reconsider | [family-recovery-request.json](family-recovery-request.json) | A subsequent explicit message from Priya requests a later date after continuity review. It does not establish her mother's delegation. |
| Revised mandate claim | [family-declaration-recovery.json](family-declaration-recovery.json) | Declaration revision 3 names the new proposal and evidence; the company verifies it. |
| Revised operation | [family-operation-revised.json](family-operation-revised.json) | After confirming no earlier execution and resolving the concerns: the **same operation ID**, a **new revision**, a new immutable SH proposal and a later date. This is a later message, not part of the decline. |
| Fresh user approval | [family-reapproval.json](family-reapproval.json) | Priya reviews the new revision through the agent's own interface. `approver` is `user`; the old approval is never reused. |
| Assess the new proposal | [family-recovery-allow.json](family-recovery-allow.json) | ALLOW follows independent delegation and continuity checks. Ordinary `restriction_review` data links the review to the earlier hold, preserving history. No completion is reported. |

A new proposal does not remove a case restriction: the original cause must actually be resolved. The new assessment does not claim to supersede an assessment of different terms. A fresh operation approval neither amends a hard boundary nor manufactures delegation.

## 3. A free support appointment: agent approval within prior instructions

The customer instructs their agent through its own interface to book a free, reversible 30-minute telephone appliance-support appointment on 26 November, wholly within 14:00–16:00 Europe/London. The instruction excludes deposits, payments, cancellation, rescheduling and no-show charges, extra customer confirmation conditions, new contracts, account-detail changes and changes to existing appointments. No access arrangements have been requested; `access_needs: "none_stated"` records that information, not an assessment that the customer has no support needs.

The `prior_user_instruction` metadata on the approval's [manifest.json](manifest.json) entry records that fictional **local** instruction, its source and the constraints used by offline checks. It is not a Poppy payload or company content. Its `record_ref` identifies the agent's example approval record; that opaque reference is not independent authority evidence.

| Step | File | Meaning |
|---|---|---|
| Customer terms | [appointment-declaration.json](appointment-declaration.json) | Prior-instruction boundaries and claimed limited appointment mandate. |
| Company terms | [appointment-company-declaration.json](appointment-company-declaration.json) | Offer and booking roles, availability and company authority remain distinct. |
| Exact appointment | [appointment-operation.json](appointment-operation.json) | Free 14:30–15:00 slot, with matching JSON terms and summary. |
| Agent approval | [appointment-agent-approval.json](appointment-agent-approval.json) | `approver: "agent"`, without `input_type`, after checking every material term against the prior user instruction. |
| Service checks | [appointment-allow.json](appointment-allow.json) | Company checks establish the limited mandate, its booking authority and availability. It permits booking but reports no completed booking. |

The company does not infer authority from `approver: "agent"`, a declaration or a confidence score. This reversible, no-fee appointment uses the company's existing trusted mandate process. It does not relax SH-1.2's independent-evidence requirements for irreversible actions, including the cancellation above.

If the instruction's coverage is uncertain, the agent asks the user. If the company answers this agent approval with a new revision, or declines it, the agent must ask the user before approving revised terms; it cannot automatically reuse the same instruction.

## Other fixtures and test limits

- [assessment-incomplete.json](assessment-incomplete.json) illustrates intake without fabricated declaration references.
- Tests check envelope structure, versions, request context, references, preserved boundaries, decline/revision sequences and the supplied appointment instruction constraints.
- Comparing those explicit constraints is not natural-language intent evaluation. No test authenticates the instruction's source, verifies real delegation, executes an action, delivers a human handover or measures a customer outcome.
- Company-defined `terms`, `service_result` and `restriction_review` keys have the meanings described here. They do not extend the SH-1.2 canonical schemas or Poppy itself.
