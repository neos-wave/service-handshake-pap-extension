# Service Handshake extension proposal for the Personal Agent Protocol (Poppy)

A customer’s agent refuses a voucher. The customer still needs a refund or replacement. This proposal sets out how a company and a personal agent can keep working towards a permitted resolution while preserving both parties’ boundaries, authority and safeguards.

**Independent review draft. Not adopted or endorsed by Poppy’s authors; not demonstrated through a live integration.** This version updates the earlier proposal for Poppy draft 0.3 and Operations version 2. The underlying framework remains **SH-1.2**.

## Refund or replacement: one service request, several decisions

| Situation | Decision on the proposal | What happens next |
|---|---|---|
| Customer wants a refund or equivalent replacement and refuses credit. A voucher is proposed. | **DENY** the voucher. | Keep the service request open and consider permitted alternatives. |
| An equivalent replacement is available, but required approval and evidence are missing. | **HOLD** that action. | Explain the terms and the approval needed. Permitted discussion can continue. |
| The company verifies the required evidence, receives operation approval and completes its checks. | **ALLOW** this proposal. | Arrange the replacement while the checks remain valid. Permission is not completion. |
| A human or specialist is needed, including for applicable safeguarding. | **ESCALATE** with restrictions intact. | Give the receiving colleague the blocked action, reasons and next step. |

The [complete worked journey](examples/README.md) follows the replacement through arrangement and delivery. A second case shows why Priya’s recognised billing access does not itself establish authority to cancel her mother’s broadband. These are fictional illustrations, not customer results.

## How it fits with Poppy

Poppy supplies discovery, identity, account access and interaction mechanisms. Its Operations extension supports approval of particular terms. Its task-coverage features can describe another way to complete a task or another task serving the same need. SH does not claim these capabilities are missing.

This extension adds shared service requirements for adopters: declarations from both parties, an assessment of each proposal, reasons and next steps, safeguards and continuity through handover. The company implements the checks; an exchanged record does not enforce them or become a credential. Existing trusted processes may supply the necessary evidence.

The extension’s conversation binding includes a proposed additional SH check before commitment. If a new restriction blocks an approved operation before it starts, the company reports that through a normal assessment message. The exact composition with Poppy’s Operations flow remains a design question for implementer review; this package does not claim agreed interoperability.

## Start reading

| Reader | Start here |
|---|---|
| Service or CX leader | [Worked journeys](examples/README.md) and [mapping](MAPPING.md) |
| Protocol reviewer | [Specification](SPECIFICATION.md), especially §§4, 6.1 and 7 |
| Implementer | [Exchange schema](schema/sh-poppy-extension.schema.json), [validation scope](VALIDATION.md), [migration](MIGRATION.md) |
| Researcher | [Sources](SOURCES.md), [source lock](SOURCE-LOCK.json) and [changelog](CHANGELOG.md) |

## Scope and version

| Item | Value |
|---|---|
| Extension name | `dualcx.com/service-handshake` |
| Proposed extension major version | `"2"` |
| Wire draft | `2026-11-02` |
| Package | Review draft 3, 2 November 2026 |
| Poppy baseline | Draft 0.3; Operations version `"2"`; exact source revision in SOURCES.md |
| Service framework | [Published SH-1.2](https://zenodo.org/records/23181969) |
| Binding covered | Native conversations and Operations in those conversations |
| Author / publisher | Maria McCann / Neos Wave Ltd, Dual CX |
| Licence | Apache 2.0; see LICENSE and NOTICE |

The extension’s version 2 is **not Service Handshake 2.0**. The SH declaration and action-assessment reference schemas remain unchanged. Version 1 and its draft date are not compatible with this update. Exact extension-version and draft agreement is required during review; future stable compatibility rules remain to be defined.

API, MCP and browser extension bindings are not supplied here. Alternative channels must still enforce applicable service restrictions, but their SH exchange formats are outside this draft. Unsupported agents retain proportionate assistance and an appropriate human route.

## Evidence and privacy

The package includes public structural and example checks, using pinned Poppy schemas. It is not a running service, a production execution guard, a certification suite or proof of deployment in Neos OS. [VALIDATION.md](VALIDATION.md) separates what has been checked from what still needs a live pilot.

Full trusted assessments, raw approval evidence and internal policy remain with the organisation. No private Neos prompts, assessment methods, risk thresholds or operational test suite are included. Optional policy packs remain future work in Specification §13.

## Run the checks

```sh
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

The tests run offline after dependencies are installed. External schemas resolve to the copies supplied in `reference/`.

## Provenance and feedback

Maria McCann / Neos Wave first published the Service Handshake in March 2026. SH-1.2 followed in October. The independent Poppy extension is later work; none of its later protocol bindings is claimed to have existed in March.

Review questions: the negotiated post-approval block, delivery of restrictions into staff workflows, and the minimum records needed to keep service moving after a refusal. Feedback belongs in the [extension repository](https://github.com/neos-wave/service-handshake-pap-extension). Do not include customer records, credentials or sensitive controls in public issues.

The parent framework remains in the [Service Handshake repository](https://github.com/neos-wave/service-handshake).
