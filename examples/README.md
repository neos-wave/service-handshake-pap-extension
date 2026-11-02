# Worked journeys and example files

All people, companies, identifiers and evidence references are fictional. Files illustrate exchange and sequence; they do not contact a service, establish legal entitlement or verify a real approval. Dates are fixed for repeatable checks, not live validity windows.

The complete discovery and client documents describe fictional endpoints and keys that do not exist. They demonstrate shape; they are not deployable authentication configuration. `manifest.json` identifies each full Poppy envelope and any nested extension record. SH records are in `message.extensions["dualcx.com/service-handshake"]`; Operations content is in `message.extensions.operations`. Ordinary business-result data remains in `message.data`. The initial customer declaration opens each conversation; subsequent personal-agent messages use the follow-up request schema.

## 1. A damaged order: refund or replacement

The customer received a damaged kettle. They prefer a full refund, would accept the same model as a replacement, refuse credit and require approval before committing to replacement terms. Their agent's declaration describes those instructions; the company must verify authority separately.

| Step | File | Meaning |
|---|---|---|
| Establish customer terms | [message-declaration.json](message-declaration.json) | Customer declaration; authority evidence unresolved. |
| Establish company terms | [company-declaration.json](company-declaration.json) | Company declaration and relevant boundaries. |
| Refuse one remedy | [voucher-denied.json](voucher-denied.json) | DENY the voucher. This is not closure of the damaged-order case. |
| Explore an acceptable option | [replacement-request.json](replacement-request.json) | Ask about an equivalent replacement; retain the refund option. |
| Present the exact offer | [replacement-operation.json](replacement-operation.json) | Poppy operation in `message.extensions.operations` plus SH binding in its separate domain-named extension slot; no extra fields inside the operation. |
| Identify what is missing | [replacement-hold.json](replacement-hold.json) | HOLD for approval and required independent evidence. |
| Obtain operation approval | [replacement-approval.json](replacement-approval.json) | Agent reports the user's approval through Poppy. This is not independent proof. |
| Record updated claimed authority | [delivery-declaration-revised.json](delivery-declaration-revised.json) | New declaration revision preserves no-credit and other boundaries. Its evidence reference is still a claim until checked. |
| Assess after trusted checks | [replacement-allow.json](replacement-allow.json) | Illustrative local checks have passed; ALLOW supersedes the replacement hold, not the voucher denial. |
| Report execution | [replacement-arranged.json](replacement-arranged.json) | Fulfilment confirms arrangement. Delivery and resolution remain outstanding. |
| Report service completion | [replacement-delivered.json](replacement-delivered.json) | Illustrative delivery evidence and customer confirmation support closing this case. |

**Between approval and allow**, the company must independently obtain and verify the required evidence, check its own authority and policy, and record its canonical assessment. That private process is not supplied as an agent assertion or as runnable code here. If it fails, the hold remains. A customer declining the replacement leaves the refund or another permitted route to be considered; it does not authorise credit.

An operation's approval does not waive a customer boundary. New material terms require the applicable new proposal, revision, assessment and approval. The agent can discuss permitted alternatives without accepting them.

`service_result` is ordinary Company-defined example data, not a new SH or Poppy standard record. Arranged and delivered refer to distinct business events. These files add no universal delivery-confirmation or refund-receipt requirement to SH-1.2.

## 2. Priya's mother's broadband: authority and continuity

Priya has recognised billing access. The account is her mother's; this is not use of her mother's login. Authority for cancellation and continuity of any essential alarm need separate checks.

1. [family-declaration.json](family-declaration.json), [family-company-declaration.json](family-company-declaration.json) and [assessment-hold.json](assessment-hold.json) establish terms and the cancellation hold. No Poppy operation is needed merely to discuss the proposal.
2. [relayed-concern.json](relayed-concern.json) reports a possible alarm dependency. Treat it as raised, not as a verified technical finding. [assessment-escalate.json](assessment-escalate.json) records the specialist route while preserving the authority hold. [handover.json](handover.json) carries both restrictions and the necessary support instructions. A human route does not grant cancellation authority.
3. **Conditional safe branch, not automatic progression:** the provider independently establishes limited delegation, resolves the alarm concern and checks service continuity. [family-declaration-revised.json](family-declaration-revised.json) records the revised claims; it is not the proof. [operation-message.json](operation-message.json) then presents terms for Priya to approve.
4. [family-approval.json](family-approval.json) is the Poppy User's approval step. Priya's approval is not her mother's delegation. [assessment-after-evidence.json](assessment-after-evidence.json) illustrates ALLOW only after all required checks and that step have passed. No cancellation-completion claim is made.
5. **Separate late-concern branch:** [approval-blocked-message.json](approval-blocked-message.json) shows a new concern arriving before commitment. It supersedes the allow with HOLD and states that cancellation has not started. It is a normal Company assessment message, not a new operation state or HTTP confirmation error.

If execution has already started or its outcome is unknown, step 5 is not an appropriate response. Investigate the existing operation and use Poppy's retry/recovery protections. Never describe an uncertain outcome as safely not executed or issue a fresh operation to retry blindly.

## Other fixtures and limits

- [assessment-incomplete.json](assessment-incomplete.json) illustrates an intake hold with no fabricated declaration references.
- [company-discovery.json](company-discovery.json) and [client-metadata.json](client-metadata.json) show extension version 2, draft 2026-11-02-r4 and Operations version 2.
- The public tests check envelopes, records, bindings, preserved boundaries and narrative consistency. No live authentication, delegation proof, execution, human delivery or customer outcome is exercised.
