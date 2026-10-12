# Validation and remaining implementation work

Rechecked locally for review package draft 2 on 12 October 2026: **16 unittest tests passed**, covering all manifest-listed extension payloads and the three schema documents. Schema references resolve offline. The two SH reference schemas were copied unchanged; their checksums are recorded in SOURCES.md. The exchange schema, examples and test source are also unchanged from review package draft 1.

The checks cover required fields, supported draft/version, exact decision vocabulary, missing-declaration holds, allowing-decision references and expiry, non-allow reasons, declaration shape, relayed-report status, record placement, namespaced action strings, discovery dependencies, case-reference consistency and the illustrated blocked-confirmation state.

These are structural and fixture consistency tests. They do not run a Poppy server, authenticate a principal, verify delegation, measure accessibility, prove a real execution guard or validate the complete base-protocol envelopes. They are not a certification suite and do not establish that this extension is live in Neos OS.

## Required checks in a real implementation

Before a live support claim, test the declared scope against an actual personal-agent client and company implementation. At minimum:

- A direct confirmation attempt, alternate channel or repeated request cannot bypass a hold, denial or escalation.
- A stale allow, changed declaration, changed operation terms, expired or revoked evidence, or a newly raised material concern prevents commitment until correctly reassessed.
- Concurrent commitments and timeout recovery preserve the underlying operation's execution guarantees and applicable financial limits.
- An incoming assessment, forged case reference, reused record ID or prompt-injection text cannot become trusted policy, authority or access to another case.
- The receiving staff actually see blocked actions, reasons, missing information and restrictions. A transfer or fresh contact does not lift them.
- Unknown extensions and mismatched drafts receive the specified fallback without losing ordinary assistance or disclosing protected information.
- A principal's approval is independently checkable where required; an agent-supplied code, assertion or revised declaration does not manufacture it.
- Necessary support is provided for a relayed concern without treating it as a diagnosis or using it to profile the person.
- Cancellation/recovery after commitment respects what actually happened; a late concern does not rewrite an operation's history.

The proposed confirmation guard and its error format should be reviewed with Poppy implementers before claiming interoperability. Deployment-specific authority rules, private tests and operational risk controls remain outside this public proposal.
