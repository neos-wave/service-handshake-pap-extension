# Changelog

## Review draft 5 - 2 November 2026

Documentation and test diagnostics update. Wire draft remains `2026-11-02-r4`; extension version 2 and SH-1.2 are unchanged.

- Added immutable HTTPS download links for the extension and SH schemas, with instructions for resolving their existing identifiers offline.
- Clarified permitted signed-out contact, protected access, conversation ownership and the distinction between disabling new sign-in and revoking existing tokens.
- Made malformed or misplaced fixture content report the filename, expected location and correction instead of an unhandled lookup error.
- Added regression checks for readable failure reports; retained the explicit open question about post-approval execution checks.
- No published schema, example, licence or upstream source revision changed.

## Review draft 4 - 2 November 2026

Wire draft `2026-11-02-r4`, extension major version `"2"`; SH remains 1.2. This supersedes the earlier same-day extension draft and pins Poppy commit `5313d8441abb55d2004e5fbc2a4fdab4af1624b3`.

- Moved SH records to the domain-named message extension slot and Operations content to `extensions.operations`.
- Published the message-content schema relationship, refreshed upstream schemas and separated opening from follow-up request validation.
- Added negative checks for legacy placement, malformed Operations content and unsupported or mismatched extension exchange.
- Recognised Links, Disclosures, skills and expanded alternatives without treating them as authority or policy adoption.
- Clarified Direct Conversation visibility and ambiguous replies; neither supplies independent approval evidence by itself.
- Retained proposal-level decisions, continued service, both-party boundaries, safeguarding and the explicit unresolved post-approval composition question.
- Updated positioning, migration and review guidance; no deployment or endorsement claim added.

## Review draft 3 — 2 November 2026

Incompatible extension update: proposed major version `"2"`, wire draft `2026-11-02`. SH remains 1.2.

- Rebased the binding on pinned Poppy draft 0.3 and Operations version 2.
- Replaced integer operation revisions and legacy message authors; retained SH integer declaration revisions.
- Moved operation bindings into Company message data and removed legacy confirmation-endpoint, operation-state and HTTP 409 action-block examples.
- Defined the proposed additional commitment check and its normal conversation response, including not-started versus unknown/completed execution handling.
- Clarified operation approval versus independent authority evidence and preserved restrictions across human and Direct Conversations.
- Added the full damaged-order refund/replacement path and revised the family scenario with an explicit late-concern branch.
- Added pinned upstream schemas and offline checks of complete envelopes, references, direction and scenario consistency.
- Added migration guidance, source locking and a review brief. No live compatibility, endorsement or deployment claim is made.

## Earlier package history (retained)

# Changes

## Review package draft 2 - 12 October 2026

- Added a plain-English opening, a corrected relationship diagram and a recognised-billing-access example to the README.
- Used the full protocol name in the title and retained the independent-proposal status near the opening.
- Explained why proposed terms can precede final authority and why the execution guard also protects legitimate pending proposals.
- Clarified the intended move from exact draft-date matching to an agreed stable compatibility policy.
- Added an informative section on optional future policy packs, with explicit adoption, scope and limitations; no new fields or conformance obligations.
- Recorded checks on the string version format, unresolved custom-error mechanism and protocol licence.
- Distinguished SH-1.2's document date from its Zenodo publication date and package revision from wire revision.
- Named the maintainer and a lightweight feedback route. Fuller governance remains deferred.
- Prepared a separate extension repository and updated feedback links; the parent SH repository and releases remain unchanged.

The exchange schema, wire identifier, JSON examples, tests and both SH-1.2 reference schemas are unchanged. The historical maps and videos are not included: they still require separate correction. Publication of this package does not establish a live integration, submission to protocol maintainers or certification.

## Review package draft 1 - 11 October 2026

Initial independent specification, exchanged-record schema, fictional examples, SH mapping and structural checks against Personal Agent Protocol Draft 0.1 and published SH-1.2.
