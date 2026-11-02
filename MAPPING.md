# Relationship to SH and Poppy

This independent proposal applies published SH-1.2 requirements within a limited Poppy binding. It neither amends SH-1.2 nor claims acceptance by Poppy's authors.

| Service requirement | SH Technical Specification | Extension |
|---|---|---|
| Participation and Verified authority | §§1.2, 14 | §3 discovery and §12 scoped claims |
| Disclosure, assistance, provenance | §§2.3–2.4 | §5 declarations |
| Both parties' goals and boundaries | §§3–5, 9.3 | §§5–6 assessment |
| Hold, alternatives and permitted assistance | §9.3; main paper §3.2 | §6.1; complete recovery example |
| Independent evidence and execution checks | §§8, 10 | §7, subject to current approval rules |
| Safeguarding and human continuity | §§6.3–6.5 | §§8–9, including linked Direct Conversations |
| Immutable records and separate outcomes | §12 | §§5.2, 6–7; existing reference schemas unchanged |
| Untrusted data and private controls | §§10.2, 13 | §§2, 10–11 |
| Core action meanings | Appendix A | Advertised action categories and per-proposal assessment |

## Existing protocol capabilities

Poppy covers identity, delegated account access, conversations, handoff and direct user conversations. Operations handles particular-term approval and retry protections. Task coverage can describe excluded tasks and alternatives; context can communicate situational information. These mechanisms can support service work and should be reused where appropriate.

SH adds explicit service-assessment expectations for adopters, including both parties' boundaries, evidence appropriate to the action, required safeguarding, explanations and continuity. It is not the only possible service policy framework, and this proposal does not claim that a core Poppy implementer cannot provide those controls independently.

## Attachment points and design decisions

- Discovery uses the domain-named extension and exact draft agreement. Action categories describe supported meaning, not what each side is authorised to do.
- Records use `message.data`. A Company operation message may pair an operation with a separate binding record in `data`; no custom operation members are added.
- Assessments remain separate from declarations, credentials and execution results. Company checks apply locally at commitment.
- The additional SH block after operation approval is proposed composition, not a published Poppy base guarantee. It uses a Company assessment message and preserves base retry semantics. It needs joint implementer review and live testing.
- Custom malformed-record/conflicting-record errors in §11 remain proposed extension validation behaviour. They do not change base authentication or message-conflict errors.
- A complete case-status record, policy packs and non-conversation bindings are not added. Example business-result data is informative only.

See [sources](SOURCES.md), [migration](MIGRATION.md) and [validation](VALIDATION.md) for the exact baseline and limits.
