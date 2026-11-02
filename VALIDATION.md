# Validation and remaining implementation work

Checked locally for review package draft 4 on 2 November 2026: **41 unittest tests passed**. The package targets extension version 2 / draft 2026-11-02-r4, Poppy draft 0.3 and Operations version 2 at the pinned source revision. The two SH-1.2 reference schemas remain unchanged; twelve unmodified Poppy schemas are included for offline envelope checks. SOURCES.md and SOURCE-LOCK.json record provenance and hashes.

The checks cover complete example requests/events/discovery documents against upstream shapes, supported draft/version, operation revision strings versus SH revision integers, decision vocabulary, non-allow reasons, declared roles, record placement and operation binding, declaration and operation references, assessment history, relayed-report status, discovery dependencies and reference checksums. Scenario checks distinguish a denied voucher from a held replacement, preserve the no-credit boundary, separate arrangement from delivery, and retain a later restriction without rewriting the earlier assessment.

Additional migration checks reject legacy SH and Operations placement even where Poppy's permissive base schema accepts the unknown fields. They check supported version/draft advertisements in supplied fixtures, malformed Operations content, coexistence with Links and Disclosures, and the distinct opening-request shape for a Company-first Direct Conversation. The fixtures do not exercise actual metadata fetching, notice display, skill execution or Direct Conversation ownership enforcement.

A missing or misplaced record is reported as a test failure naming the example file, the expected location and the correction, rather than as a lookup error.

These are structural and fixture consistency tests. Although complete example envelopes are now checked, this is not full Poppy conformance validation. Sender checks in the fixtures do not authenticate a real sender. No server runs, no principal or delegation is verified, no real execution is blocked and no human receives a handover. The tests are not a certification suite and do not establish that this extension is live in Neos OS.

## Required checks in a real implementation

Before a live support claim, test the declared scope against an actual personal-agent client and company implementation. At minimum:

- An approval message, alternate channel or repeated request cannot bypass a hold, denial or escalation. Receipt of a message is not evidence of commitment.
- A stale allow, changed declaration, changed operation terms, expired or revoked evidence, or a newly raised material concern prevents commitment until correctly reassessed.
- Concurrent commitments and timeout recovery preserve the underlying operation's execution guarantees and applicable financial limits.
- An incoming assessment, forged case reference, reused record ID or prompt-injection text cannot become trusted policy, authority or access to another case.
- The receiving staff actually see blocked actions, reasons, missing information and restrictions. A transfer or fresh contact does not lift them.
- Unknown extensions and mismatched drafts receive the specified fallback without losing ordinary assistance or disclosing protected information.
- A principal's approval is independently checkable where required; an agent-supplied code, assertion or revised declaration does not manufacture it.
- A short or ambiguous reply does not clear a hold. Links, notices and skills cannot become permission, and Direct Conversation visibility is respected when selecting an evidence channel.
- Necessary support is provided for a relayed concern without treating it as a diagnosis or using it to profile the person.
- Cancellation/recovery after commitment respects what actually happened; a late concern does not rewrite an operation's history.

Review the proposed post-approval SH precondition and conversation response with Poppy implementers before claiming interoperability. In particular, agree what happens when a valid approval arrives after a new restriction and how a resolved hold resumes without duplicate or silent execution. Test malformed-record extension responses separately from base authentication, message-conflict and retry behaviour. Deployment-specific authority rules, private tests and operational risk controls remain outside this public proposal.
