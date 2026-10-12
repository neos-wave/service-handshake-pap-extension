# Source baselines

Publication files checked 11 October 2026; protocol extension/version/error documentation and licence rechecked 12 October 2026. Package revision 2 retains the same wire draft.

- [Poppy extensions](https://personalagentprotocol.org/docs/extensions), Draft 0.1, updated 9 October 2026.
- [Poppy specification](https://personalagentprotocol.org/docs/spec), same draft; §§3.3 and 7 for discovery and conversations.
- [Operations](https://personalagentprotocol.org/docs/extensions/operations), version 1 within that draft; §§3, 5, 6 and 8 for action binding, execution and evidence boundaries.
- [SH-1.2 publication](https://zenodo.org/records/23181969), Maria McCann / Neos Wave Ltd. The main paper and Technical Specification were downloaded from the record and checked against its displayed MD5 values.

| Published file | Zenodo MD5, matched locally |
|---|---|
| Service Handshake 1.2.pdf | `dca20e389f4c5ceda3ee69d8387edc62` |
| Service Handshake Technical Spec 1.2.pdf | `838913018878697f5f973aae7616fbee` |

The documents are dated 1 October 2026. The Zenodo record displays publication on 6 October 2026 and record version v2; the framework edition is SH-1.2. These are distinct labels.

The published Technical Specification identifies two canonical schemas. Zenodo currently lists the two PDFs, not those JSON files. The unchanged reference schemas in this package were copied from the local SH-1.2 publication package associated with the [published repository](https://github.com/neos-wave/service-handshake). Their retained review URNs are identifiers, not URLs. They have not been rewritten to claim a stable hosted endpoint.

- `sh-1.2.schema.json` SHA-256: `ee2d7124f718b9f28cfa20764c2e8cd48b9f35749f3111b6638d2f55ccd11cb5`
- `sh-1.2.action-assessment.schema.json` SHA-256: `be0d37779d76420112129cb364792414b68a1dd59151367c49ae4443a6253746`

This proposal supplies original extension requirements and a new exchanged-summary schema. It does not redistribute the Poppy documents or the SH publication PDFs. The source documents retain their own licences. The reference SH-1.2 schemas, examples and tests in the original package are Apache 2.0; the SH papers are CC BY 4.0.


## Clarifications checked for package revision 2

- PAP §3.3 and Operations §2 show extension major versions as strings, including `"1"`.
- The published material permits domain-named extensions but does not expressly establish this proposal's custom confirmation-error convention. The error remains a design proposal requiring implementer review.
- [PAP licence](https://personalagentprotocol.org/license): the protocol documentation is Apache 2.0; the names, logo and site design are excluded from that licence grant. This package uses the names to identify the protocol under discussion, supplies no PAP logo, and claims no endorsement.
