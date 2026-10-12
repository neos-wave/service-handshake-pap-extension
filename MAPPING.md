# Relationship to the published standards

This is a new, optional binding proposed by Neos Wave. The existing SH publication supplies the service requirements; Poppy supplies the protocol context. This document does not imply that either publication already contains this extension.

| Service requirement | Published SH Technical Specification | Where this draft applies it |
|---|---|---|
| Two levels of requirements and scoped claims | §§1.2, 14 | Discovery profile; §12 support claims. Both profiles retain relevant authority checks. |
| Disclosure, provenance, assistance and confirmation | §§2.3–2.4 | §5 and the declaration envelope; assistance also remains available without extension support. |
| Both parties' boundaries and data permissions | §§3–5, 9.3 | §§5–6, 10; compatibility of the actual proposal, with data limits throughout the interaction. |
| Nonwaivable harm routing and continuity | §§6.3–6.5 | §§8–9; relayed concerns, restrictions and the receiving staff workflow. |
| Action-specific authority and independent evidence | §§8.3–8.4 | §§6–7; claims are separated from trusted verification. |
| Execution checks, financial controls and private limits | §§8.5–8.7 | §7 execution guard, with §10 minimisation. Private thresholds are not exchange requirements. |
| Immutable declarations, proposal and assessment records | §12 | §§5.2, 6–7. The public summary is a new format; canonical local assessment remains separate. |
| Untrusted declarations and input security | §§10.2, 13 | §§2, 10–11; incoming data cannot change instructions, policy or permissions. |
| Action meanings and material terms | Appendix A | §3 action scope; §7 immutable proposal binding; examples use core cancellation and voucher meanings. |

## Poppy attachment points

The extension uses Poppy's documented discovery configuration and domain-based extension naming. Its records occupy `message.data`; the optional Operations binding identifies the proposal at the operation object's top level. Authentication, account access and conversation transport remain Poppy's responsibility. See [the specification](https://personalagentprotocol.org/docs/spec) and [extension rules](https://personalagentprotocol.org/docs/extensions).

Poppy Operations already provides a confirmation mechanism and defines its evidence limits. This proposal requires the company to apply its additional service checks before commitment. It does not claim that Poppy lacks consent, access controls or human handoff. See [Operations](https://personalagentprotocol.org/docs/extensions/operations).

## New design choices requiring review

1. **Exchanged summaries.** The decision, handover and concern envelopes are new definitions, not fields already standardised by SH-1.2.
2. **Confirmation rejection.** The proposed namespaced HTTP 409 `action_blocked` response is an additional negotiated behaviour. It requires review and implementation on both sides; it is not a pre-existing Poppy error. A core-protocol implementation alone will not implement this guard.
3. **Draft agreement.** Exact draft matching avoids claiming compatibility while this design is still changing. A stable release is intended to replace exact draft-date matching with documented compatibility rules once those rules are agreed. Package revision 2 leaves the wire draft and schemas unchanged.
4. **Policy packs.** Specification §13 outlines an optional future application, without a new wire format or conformance obligation. Packs require explicit adoption and cannot override applicable requirements.
5. **Limited initial scope.** This draft covers native conversations and their Operations. A general MCP, API or website binding would need its own placement and error rules; it is not supplied by this package.

Publication can establish this as an independently authored extension proposal. It cannot establish acceptance by Poppy's maintainers, interoperability with Sierra, or a working Neos OS deployment. Those claims need separate evidence.
