# Source baselines

Reviewed 2 November 2026. Extension version 2 / draft 2026-11-02-r4, review package 5. Package 5 clarifies access handling and schema retrieval and improves test diagnostics; it does not change the wire draft, schemas, examples or upstream baseline.

## Poppy

- [Specification, draft 0.3](https://personalagentprotocol.org/docs/0.3/spec): discovery, sessions, account access, native conversations, handoff and task coverage.
- [Operations, version 2](https://personalagentprotocol.org/docs/0.3/extensions/operations): terms, approvals, execution/retry rules and evidence limits.
- [Extension rules](https://personalagentprotocol.org/docs/0.3/extensions), [Links](https://personalagentprotocol.org/docs/0.3/extensions/links), [Disclosures](https://personalagentprotocol.org/docs/0.3/extensions/disclosures) and [implementation guides](https://personalagentprotocol.org/docs/0.3/guides).
- Source repository revision: [`5313d8441abb55d2004e5fbc2a4fdab4af1624b3`](https://github.com/personal-agent-protocol/personal-agent-protocol/commit/5313d8441abb55d2004e5fbc2a4fdab4af1624b3). Documentation paths and Git blob hashes are recorded in [SOURCE-LOCK.json](SOURCE-LOCK.json).

The twelve JSON schemas in `reference/poppy/` are unmodified copies from that revision's `kit/company/schemas/`. Their Git blob hashes were matched against the repository and their SHA-256 hashes are locked. They are upstream shape checks, not a full conformance verifier. Some sender, binding and sequencing requirements need additional checks or live implementation testing.

These Poppy files are Apache 2.0. See LICENSE and NOTICE. Names, logos and site design are not granted by that licence; this package uses protocol names only for identification and claims no endorsement. The Poppy documentation itself is not redistributed here.

## Service Handshake

[SH-1.2 publication](https://zenodo.org/records/23181969), Maria McCann / Neos Wave Ltd. The documents are dated 1 October 2026; the earlier verified Zenodo record displayed publication on 6 October and record version v2. The framework edition is SH-1.2, distinct from the Zenodo record version and this extension version.

The earlier package checked both downloaded publication PDFs against the record's MD5 values: main paper `dca20e389f4c5ceda3ee69d8387edc62`; Technical Specification `838913018878697f5f973aae7616fbee`. This update does not claim a fresh PDF download or change those documents.

The canonical SH schemas remain unchanged from the local publication package associated with the [SH repository](https://github.com/neos-wave/service-handshake). Their review URNs are preserved identifiers, not hosted URLs. Their provenance is not misrepresented as a new Zenodo JSON download.

- `sh-1.2.schema.json`: `ee2d7124f718b9f28cfa20764c2e8cd48b9f35749f3111b6638d2f55ccd11cb5`
- `sh-1.2.action-assessment.schema.json`: `be0d37779d76420112129cb364792414b68a1dd59151367c49ae4443a6253746`

SH papers: CC BY 4.0. SH reference schemas, examples and tests: Apache 2.0. New extension text, exchange schema and examples are original proposal work under Apache 2.0; they do not become requirements of SH-1.2 merely by inclusion here.

## Same-day upstream change

The earlier version-2 draft `2026-11-02` used Poppy commit `1de1990e4978b42179fe0e3e0ae554271808c308`. Eight subsequent upstream commits changed message placement, added Links and Disclosures, introduced task skills and clarified access, direct conversations and replies. This package uses draft `2026-11-02-r4` to avoid treating those incompatible placements as the same agreed draft. The earlier extension package remains in Git history at `bbf82e55ee0889ae2c159e63d77c09d8221ff95f`.

## Earlier extension

The starting package was the public [extension repository](https://github.com/neos-wave/service-handshake-pap-extension), revision/tree returned as `7137d0b72297bb7891af14a95b5057fb44db5a98` on 2 November. All 31 tracked files matched the local publication copy using Git blob hashes. Its version 1 / draft 2026-10-11 targeted Poppy 0.1. This update preserves that history rather than implying current compatibility for the older draft.
