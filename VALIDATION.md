# Validation and remaining implementation work

Checked locally for **review package 6 on 25 November 2026: 76 unittest tests passed**.

The package targets **extension version 3 / wire draft 2026-11-25**, published **Poppy 1.0** and **Operations version 3**. Fourteen unmodified Poppy schemas are pinned to the immutable 1.0 release commit. The two canonical SH-1.2 reference schemas remain unchanged. [SOURCES.md](SOURCES.md) and [SOURCE-LOCK.json](SOURCE-LOCK.json) record the source revisions and hashes.

## Reproduce the checks

```sh
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

The checks run offline once those dependencies are installed. The example manifest contains **36 entries**: 35 complete native discovery, client-metadata, request or event envelopes, and one local request-context fixture.

## What was checked

| Area | Checks in this package |
|---|---|
| Published Poppy shapes | Complete native envelopes against the pinned upstream schemas; required conversation description, top-level Personal Agent request ID, operation terms and approval approver. |
| Extension discovery and selection | Company version arrays, native request headers, exact SH draft, action scope and optional Operations binding. Old discovery shapes and unsupported selections are rejected in the supplied traces. OAuth client metadata cannot substitute for request selection. |
| SH records | Supported version and draft, declaration references and integer revisions, assessment decisions and reasons, both-party requirements, expiry, record placement and claimed sender roles. Additive wrapper metadata is accepted; known required fields and canonical declaration validation remain enforced. |
| Operation binding | Exact operation ID/revision, case and proposal matches; opaque native revisions; immutable terms and expiry, with harmless summary rewording allowed. |
| Decline and recovery | A pre-approval hold is distinct from a native decline. A late restriction produces a matching non-allow assessment and native decline; re-sending that approval is rejected. A later revision needs fresh user approval. Supplied recovery metadata cannot contradict that sequence; optional metadata is not required. |
| Agent approval | The appointment's supplied prior instruction covers the material terms, actual duration and nested fee conditions. Missing, company-authored, unbound, late or insufficient instructions fail the fixture checks. A new revision after agent approval requires user approval. |
| Service continuity | A refused voucher leaves compatible remedies available; revised declarations preserve the no-credit boundary; arrangement differs from delivery. Handover retains concurrent authority and safeguarding restrictions. |
| Adjacent Poppy features | Links and Disclosures can coexist with a hold; a Company-first Direct Conversation uses the opening-request shape. These features do not clear the service requirements. |
| Provenance and diagnostics | Reference-schema hashes, manifest coverage and readable failure messages when copies of fixtures are damaged or records are misplaced. |

The local request-context fixture supplies headers, a body-file reference and `local_support` settings to the test harness. Only the native headers and referenced request body represent protocol traffic. The local settings are not OAuth metadata, a new handshake record or a prerequisite for an out-of-band agreement.

The supplied trace checks are deliberately limited. Their header parser accepts the canonical Structured Fields subset used by the examples; a production client needs a complete parser. The agent-instruction check compares explicitly supplied structured bounds. It does not interpret arbitrary language or establish who actually gave an instruction.

## What these results establish

The schemas and examples are internally consistent with the tested shapes and service rules. Negative tests demonstrate that the specified fixture checker detects the failures exercised.

They do **not** establish a running implementation or full Poppy conformance. Claimed roles in a fixture do not authenticate a sender. No server runs, no principal or delegation is verified, no live approval is obtained, no real action is blocked or committed, and no receiving colleague sees a handover. Example evidence references and business results are fictional. Matching a hash proves correspondence to a pinned file, not the correctness of a deployment.

In particular, the tests do not prove at-most-once execution under concurrency, actual request deduplication, account or Direct Conversation ownership checks, evidence revocation, transaction isolation or the delivery of restrictions into staff workflows. They do not exercise metadata fetching, notice display or skill execution. The package is neither a certification suite nor evidence of deployment in Neos OS.

## Required checks in a real implementation

Before a live support claim, test the declared service scope through an actual Personal Agent and Company implementation:

- **Selection and access:** use real discovery and request headers, enforce Session/account/ownership checks, and handle unsupported drafts without losing permitted assistance or disclosing another case.
- **Current authority and service terms:** reject stale allows, changed declarations or terms, expired or revoked evidence and newly raised material concerns. An approval statement or revised declaration must not manufacture independent evidence where it is required.
- **Commitment and concurrency:** enforce the trusted assessment at the actual protected action. Duplicate and concurrent requests, alternate execution paths and timeouts must preserve the native execution guarantees and applicable service limits.
- **Native decline:** if a valid approval cannot be acted on and execution has not started, return the exact native decline and matching service assessment without a new operation or any commitment. A later allow must not reactivate the declined approval.
- **Recovery and uncertain results:** require a later fresh revision and fresh user approval after decline. Reconcile an unknown execution outcome before offering another action; a late concern must not rewrite an effect that already occurred.
- **Instruction-based approval:** verify the actual user-instruction process and term coverage for the selected action. A company message, task guide or prompt-injection string must not supply the instruction.
- **Human continuity and support:** ensure the receiving colleague sees the blocked actions, reasons, missing requirements and next step. A transfer or fresh contact must preserve applicable restrictions and unaffected assistance.
- **Trust and privacy:** prevent incoming assessments, forged case references and reused record IDs from becoming trusted policy or access. Preserve data limits and provide necessary support for a relayed concern without treating it as a diagnosis.

Operations 3 now supplies the native decline mechanism. Live review should test this extension's composition with that mechanism, safe continuation and actual service-system controls. Malformed-record extension errors remain separate from native authentication, conflict and retry behaviour. Private authority rules, internal tests and operational controls are outside this public proposal.
