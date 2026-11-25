# Source baselines

Reviewed 25 November 2026. Independent extension version 3 / wire draft `2026-11-25`, review package 6. This package updates the **service-specific** conversation binding to published Poppy 1.0 and Operations version 3. The underlying Service Handshake framework remains SH-1.2.

## Poppy 1.0

- [Specification, version 1.0](https://personalagentprotocol.org/docs/1.0/spec): discovery, extension negotiation, Sessions, account access, native conversations, handoff and task coverage.
- [Operations, version 3](https://personalagentprotocol.org/docs/1.0/extensions/operations): structured exact terms, user or instruction-based agent approval, declines, execution/retry rules and evidence limits.
- [Extension rules](https://personalagentprotocol.org/docs/1.0/extensions), [Links](https://personalagentprotocol.org/docs/1.0/extensions/links), [Disclosures](https://personalagentprotocol.org/docs/1.0/extensions/disclosures) and [implementation guides](https://personalagentprotocol.org/docs/1.0/guides).
- Frozen source revision: [`8c02b4282eda53468a7c09412558bc8b060d95f6`](https://github.com/personal-agent-protocol/personal-agent-protocol/commit/8c02b4282eda53468a7c09412558bc8b060d95f6), **Publish and freeze 1.0 (#197)**, 14 November 2026.

The pinned revision is the 1.0 publication snapshot, rather than the moving default branch or draft 1.1. All upstream schemas and document references in this package use that same revision. [SOURCE-LOCK.json](SOURCE-LOCK.json) records each schema's source path, Git blob, SHA-256 digest and immutable source URL. It also records the Git blob and SHA-256 digest of each referenced 1.0 document. Those documents are cited, not redistributed here.

The **fourteen** JSON schemas in `reference/poppy/` are unmodified byte-for-byte copies from that revision's `kit/company/schemas/`. They include the dependency closure needed for the supplied discovery and conversation examples. `approval-declined.schema.json` and `alternative.schema.json` are new to this package; the existing references are refreshed to the same 1.0 snapshot. All external JSON Schema `$ref` file dependencies in this subset resolve to another included schema. The retained client-metadata schema describes client identity metadata; it is not the mechanism for negotiating extension support in Poppy 1.0.

These schemas provide upstream structural checks, not a complete conformance verifier. They do not authenticate senders, verify customer instructions or authority, enforce execution controls, or prove that a service outcome occurred. Protocol negotiation, sender, binding, sequencing and service requirements need additional checks; live interoperability needs a real personal-agent/company integration.

### Licence and attribution

These Poppy files are licensed under Apache 2.0. The package's existing [LICENSE](LICENSE) is byte-for-byte identical to the upstream `LICENSE` at the pinned revision; its source blob and SHA-256 digest are also recorded in the source lock. See [NOTICE](NOTICE) for attribution. No upstream schema content or embedded notices have been changed.

The upstream licence does not cover the Personal Agent Protocol or Poppy names, logo or site design. This package uses the protocol names to identify the source and interoperability target, without claiming adoption or endorsement. Its independent extension work is not presented as part of the upstream protocol.

## Service Handshake

[SH-1.2 publication](https://zenodo.org/records/23181969), Maria McCann / Neos Wave Ltd. The documents are dated 1 October 2026; the earlier verified Zenodo record displayed publication on 6 October and record version v2. The framework edition is SH-1.2, distinct from the Zenodo record version and this extension version.

The earlier package checked both downloaded publication PDFs against the record's MD5 values: main paper `dca20e389f4c5ceda3ee69d8387edc62`; Technical Specification `838913018878697f5f973aae7616fbee`. This update does not claim a fresh PDF download or change those documents.

The canonical SH schemas remain unchanged from the local publication package associated with the [SH repository](https://github.com/neos-wave/service-handshake). Their review URNs are preserved identifiers, not hosted URLs. Their provenance is not misrepresented as a new Zenodo JSON download. Their SHA-256 digests were rechecked for this package:

- `sh-1.2.schema.json`: `ee2d7124f718b9f28cfa20764c2e8cd48b9f35749f3111b6638d2f55ccd11cb5`
- `sh-1.2.action-assessment.schema.json`: `be0d37779d76420112129cb364792414b68a1dd59151367c49ae4443a6253746`

SH papers: CC BY 4.0. SH reference schemas, examples and tests: Apache 2.0. New extension text, exchange schema and examples are original proposal work under Apache 2.0; they do not become requirements of SH-1.2 merely by inclusion here.

## Previous extension packages

This update starts from extension repository commit [`1bda0951fd57c1440a6be425555896c50a9af54f`](https://github.com/neos-wave/service-handshake-pap-extension/commit/1bda0951fd57c1440a6be425555896c50a9af54f), review package 5 dated 2 November 2026. That package used extension version 2 / draft `2026-11-02-r4`, Poppy draft 0.3 and Operations version 2, pinned to upstream commit `5313d8441abb55d2004e5fbc2a4fdab4af1624b3`. It had already removed the earlier custom HTTP 409 action-block response. Package 6 does not attribute that removal to this update.

The earlier same-day version-2 draft `2026-11-02` used Poppy commit `1de1990e4978b42179fe0e3e0ae554271808c308`; later changes to message placement required the `-r4` draft. The earlier package remains in extension history at `bbf82e55ee0889ae2c159e63d77c09d8221ff95f`.

The initial version-1 / draft `2026-10-11` targeted Poppy 0.1. Its earlier provenance review recorded revision/tree `7137d0b72297bb7891af14a95b5057fb44db5a98` and matched all 31 tracked files to the local publication copy. Historical versions remain in Git history; their records must retain their original version labels and must not be treated as current extension-v3 messages.
