# Where Service Handshake fits with Poppy 1.0

The Service Handshake specifies how a Company and a customer's Personal Agent establish and maintain the terms of a service interaction. This independent extension expresses SH-1.2 service requirements through published Poppy 1.0 conversations and Operations 3. It does not amend either specification or claim adoption by Poppy's authors.

## The company capability

| Company capability | Service Handshake's contribution |
|---|---|
| Receive and recognise customer agents | Use the company's protocol, session and account-access mechanisms. |
| Define available service actions | Give the company's relevant offers, boundaries and action meanings a common representation; actual company policy and delegation remain company responsibilities. |
| Establish the particular interaction | Record the goal, exclusions, relevant data permissions and both parties' service terms. Unknowns stay unresolved. |
| Assess a proposed action | Specify proposal-level allow, deny, hold or escalate decisions and useful next steps. Trusted implementation checks establish their validity. |
| Handle changes and human intervention | Preserve the applicable restrictions, declaration versions and responsibility through new proposals, handovers and reliably linked contacts. |
| Execute and report | Bind a trusted decision to the action, report what happened and retain outstanding service work. Permission, execution and goal fulfilment remain distinct. |

## Requirements mapping

| Service requirement | SH Technical Specification | Extension |
|---|---|---|
| Participation and Verified authority | §§1.2, 14 | §3 Company advertisement; §12 scoped claims |
| Disclosure, assistance and provenance | §§2.3–2.4 | §5 declarations |
| Both parties' goals and boundaries | §§3–5, 9.3 | §§5–6 assessment |
| Refused proposals and continuing service | §9.3; main paper §3.2 | §6.1; damaged-order example |
| Independent evidence and execution checks | §§8, 10 | §7 composition with Operations 3 |
| Safeguarding and human continuity | §§6.3–6.5 | §§8–9 |
| Immutable records and separate outcomes | §12 | §§5.2, 6–7; unchanged canonical reference schemas |
| Untrusted input and private controls | §§10.2, 13 | §§2, 6 and 10–11 |
| Common service-action meanings | Appendix A | Company action advertisement and per-proposal assessment |

## Reuse the published Poppy mechanisms

| Poppy 1.0 / Operations 3 capability | How this extension uses it |
|---|---|
| Discovery arrays and request version headers | Advertise the Company's SH version and draft, then select supported versions using the existing headers. OAuth client metadata is not the selection mechanism. |
| Exact structured operation terms | Bind a particular operation revision to its immutable SH service proposal. |
| User or instruction-based agent approval | Preserve Poppy's approval rules while applying the service action's evidence, boundary and safeguard requirements. |
| Native decline | Return `extensions.operations.declined` when a valid approval cannot be acted on, with a matching SH assessment. Keep the service case open where appropriate without reviving that approval. |
| At-most-once and retry handling | Preserve native responses for duplicates and unknown execution outcomes. Do not label an uncertain outcome a confirmed refusal. |
| Alternatives, task coverage and feedback | Explore a permitted route or remedy; an alternative does not inherit approval or lift a restriction. |
| Human handoff and Direct Conversations | Retain the service restrictions and use trusted case links. A transfer or human-authored message alone supplies no independent authority evidence. |
| Links, Disclosures and skills | Communicate useful content; receipt or publication does not establish consent, authority or policy adoption. |

Poppy already requires instruction checking for agent approval and provides ways to decline approvals and offer alternatives. SH adds a common service representation and assessment discipline for its adopters. A company can implement equivalent service behaviour independently; this package does not claim otherwise.

## Attachment points

- SH message records occupy `message.extensions["dualcx.com/service-handshake"]`.
- Native operation, approval and decline records occupy `message.extensions.operations`.
- A Company message offering an operation pairs it with an SH `operation_binding`. A refusal can pair a native `declined` object with an SH non-allow assessment referring to that same operation and revision.
- A native decline ends use of that approval. A later continuation uses a new revision and fresh user approval, after the service requirements are resolved. The decline response itself offers no new operation.
- Company configuration is advertised in `poppy.json`; the Personal Agent's local support settings in the examples are not new protocol metadata.
- Full verification and policy records remain local. Shared service explanations disclose only information the recipient may receive, and do not introduce native risk-reason codes.

## Scope and evidence

The package defines a conversation binding and structural/example checks, not a running evaluator or credential service. It supplies no general API/MCP/browser SH binding, universal case-completion record or policy-pack format. Example business-result data illustrates service progress without adding fields to SH-1.2.

A live implementation must prove that the control reaches the protected action, that the receiving person sees the restrictions, and that retry and recovery behaviour is correct. See [VALIDATION.md](VALIDATION.md), [SOURCES.md](SOURCES.md) and [MIGRATION.md](MIGRATION.md).

Primary Poppy references: [1.0 specification](https://personalagentprotocol.org/docs/1.0/spec), [Operations 3](https://personalagentprotocol.org/docs/1.0/extensions/operations) and [extension rules](https://personalagentprotocol.org/docs/1.0/extensions).
