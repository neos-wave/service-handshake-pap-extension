# Service Handshake extension proposal for the Personal Agent Protocol (Poppy)

**The Service Handshake helps a company and a customer's AI agent establish the terms of a service interaction, assess what can proceed within both sides' boundaries, and carry those terms through changes and human handovers.**

This package expresses that service framework through **Poppy 1.0 native conversations and Operations version 3**. Poppy supplies discovery, identity, account access, conversation and approval mechanisms. SH supplies shared service declarations and assessment records. The company's implementation performs the checks and connects decisions to its service systems.

**Independent review draft. Not adopted or endorsed by Poppy's authors; not demonstrated through a live integration.** The service framework remains **SH-1.2**. This update changes the Poppy binding, not the published SH framework.

## Where it fits for a company

| Capability | Role of this extension |
|---|---|
| Receive a customer agent and establish appropriate access | Use Poppy and the company's trusted identity/access procedures. |
| Establish the service goal, available remedies, boundaries, data permissions and relevant authority | Exchange the relevant SH declarations, with proportionate assistance where needed. |
| Assess a particular proposed action | Record allow, deny, hold or escalate, with the reason, responsible role and next step. |
| Handle changed terms, missing evidence and human handover | Preserve the applicable service conditions and reassess; changing the handler does not lift a restriction. |
| Execute and report what happened | Connect the trusted assessment to the real action. Record execution separately from permission and from eventual service completion. |

A declaration, approval statement or exchanged assessment is not a credential. The company's trusted checks still establish whether the action is authorised and appropriate. Unsupported agents retain permitted assistance and an appropriate human route.

## One service request, several decisions

| Situation | Service assessment | What happens next |
|---|---|---|
| The customer wants a refund or equivalent replacement and refuses credit. A voucher is offered. | **DENY** that proposal. | Keep the request open and consider compatible remedies. |
| A replacement fits the goal, but required approval or evidence is missing. | **HOLD** that action. | Establish the missing requirement while permitted discussion continues. |
| A fresh assessment establishes all requirements. | **ALLOW** this particular proposal. | Execute only through the authorised path while those checks remain valid. Permission is not completion. |
| A human or specialist is required. | **ESCALATE**, preserving any hold or denial. | Deliver the restrictions and next step into the receiving person's workflow. |

The [worked journeys](examples/README.md) include a refund/replacement case, a family-representation case and a reversible appointment approved under the customer's prior instruction. These are fictional examples, not customer results.

## What changed for Poppy 1.0

- Company extension advertisements use arrays; the Personal Agent selects versions through `Poppy-Version` and `Poppy-Extensions` on requests.
- Operations include exact structured `terms`. Approvals identify `approver: "user"` or `"agent"`; agent approval must rest on a genuine user instruction covering those terms.
- A service restriction after a valid approval uses Poppy's native `extensions.operations.declined`, alongside an SH assessment. The case can remain open, but the declined approval cannot be reused.
- Continuing the same action after a decline requires a later exchange, a fresh revision and fresh user approval. A decline response itself returns no new operation.
- Full message examples, reference schemas and failure checks use an immutable Poppy **1.0 release** snapshot, not the developing 1.1 draft.

Poppy already supports instruction checking, alternatives, handoff, exact-term approvals and refusals. This proposal adds a shared service model and records for adopters; it does not claim these capabilities are absent or exclusive to SH. See [mapping](MAPPING.md) and [migration](MIGRATION.md).

## Scope and version

| Item | Value |
|---|---|
| Extension name | `dualcx.com/service-handshake` |
| Proposed extension major version | `"3"` |
| Wire draft | `2026-11-25` |
| Package | Review draft 6, 25 November 2026 |
| Poppy baseline | Published 1.0; Operations `"3"` |
| Upstream snapshot | [`8c02b4282eda53468a7c09412558bc8b060d95f6`](https://github.com/personal-agent-protocol/personal-agent-protocol/commit/8c02b4282eda53468a7c09412558bc8b060d95f6), “Publish and freeze 1.0” |
| Service framework | [Published SH-1.2](https://zenodo.org/records/23181969) |
| Binding covered | Native conversations and Operations in those conversations |
| Author / publisher | Maria McCann / Neos Wave Ltd, Dual CX |
| Licence | Apache 2.0; see LICENSE and NOTICE |

Extension version 3 is **not Service Handshake 3.0**. The canonical SH declaration and action-assessment reference schemas are unchanged. Earlier extension versions remain in repository history; their records and approvals do not become version-3 records through relabelling.

Version 3 identifies this wire draft. The Personal Agent checks the Company's advertised draft before selecting it; each exchanged SH record contains the same draft identifier. No additional protocol header or out-of-band agreement is introduced. Incompatible future changes require another extension major version.

API, MCP and browser SH payload bindings are not supplied. Company controls must still preserve applicable restrictions on other execution paths, without implying this package defines their message formats.

## Start reading

| Reader | Start here |
|---|---|
| Service or CX leader | [Worked journeys](examples/README.md) and [where SH fits](MAPPING.md) |
| Protocol reviewer | [Specification](SPECIFICATION.md), especially discovery (§3), assessment (§6) and approval/decline composition (§7) |
| Implementer | [Exchange schema](schema/sh-poppy-extension.schema.json), [validation scope](VALIDATION.md), [migration](MIGRATION.md) |
| Researcher | [Sources](SOURCES.md), [source lock](SOURCE-LOCK.json), [changelog](CHANGELOG.md) and [review brief](REVIEW-BRIEF.md) |

## Schema downloads and loading

Use the following files **from the same package commit**. The links resolve within this checkout; use the GitHub commit permalink when retrieving an immutable copy.

| File | Use |
|---|---|
| [Extension message-content schema](schema/sh-poppy-extension.schema.json) | Validates `message.extensions["dualcx.com/service-handshake"]`. ID: `urn:dualcx:service-handshake:poppy:3:draft:2026-11-25`. |
| [SH-1.2 declaration schema](reference/sh-1.2.schema.json) | Unchanged required dependency. Register its existing `$id`. |
| [SH-1.2 action-assessment schema](reference/sh-1.2.action-assessment.schema.json) | Unchanged full local trusted assessment format; separate from the exchanged summary. |
| [Poppy 1.0 reference schemas](reference/poppy/) | Fourteen unmodified schemas from the pinned upstream release for envelope and Operations checks. |

For JSON Schema 2020-12 validation, register the extension and declaration schemas under their existing `$id` values, then validate the extension value. Register the action-assessment schema when validating full local assessments. URNs are identifiers, not network download addresses. Do not rename the canonical SH schema identifiers.

The tests show offline registration of the Poppy dependencies and the additional sender, placement, negotiation and binding checks needed beyond JSON shape. [SOURCE-LOCK.json](SOURCE-LOCK.json) pins upstream hashes; [PACKAGE-CONTENTS.sha256](PACKAGE-CONTENTS.sha256) covers package files. Neither schema validity nor matching hashes proves a sender's authority or a live execution control.

## Run the checks

```sh
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

The checks run offline once dependencies are installed. They validate example envelopes, extension records and defined failure cases. See [VALIDATION.md](VALIDATION.md) for the observed result and its limits.

## Evidence, privacy and feedback

This is a specification and example package. It is not a running service, production execution guard or certification suite, and does not establish deployment in Neos OS.

Full trusted assessments, raw authority evidence and internal policy stay with the organisation. The public package contains no private Neos prompts, assessment methods or risk thresholds. SH service explanations must not expose hidden risk rules or offer a path around a native decline.

Maria McCann / Neos Wave first published the Service Handshake in March 2026; SH-1.2 followed in October. The Poppy binding is later work. Review feedback should focus on the minimum useful service records, native decline/recovery composition and delivery of restrictions into actual staff workflows. Do not include customer records or credentials in public issues.

The parent framework remains in the [Service Handshake repository](https://github.com/neos-wave/service-handshake).
