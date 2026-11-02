# Migration to wire draft 2026-11-02-r4

Review package 5 retains package 4's wire draft `2026-11-02-r4`; no schema or wire migration is required between these two packages. The instructions below concern migration from earlier wire drafts.

This is a new independent extension draft, not an upgrade to the SH framework. Preserve the earlier proposal in repository history or a release; do not reinterpret its records as version 2.

| Earlier package | New review package |
|---|---|
| Extension `"1"`, wire draft `2026-10-11` | Extension `"2"`, wire draft `2026-11-02-r4` |
| Poppy 0.1 / Operations 1 | Pinned Poppy 0.3 / Operations 2 |
| Integer operation revisions | Opaque Poppy string revisions; SH declaration revisions remain integers |
| `sender` in messages | Current `author` object; Company-set event role |
| Binding inside operation | Binding in `message.extensions["dualcx.com/service-handshake"]`, alongside `extensions.operations.operation` |
| Confirmation endpoint and proposed-state assumptions | `extensions.operations.approval` and ordinary Company assessment replies |
| Custom HTTP 409 action-block response | Removed; a not-started action block is explained in a Company message |
| Nested payload validation only | Full example envelopes checked against pinned upstream schemas plus extension checks |

## From the earlier version-2 draft issued on 2 November

- Change the negotiated `draft_revision` from `2026-11-02` to `2026-11-02-r4`; do not advertise both placements as the same draft.
- Move SH message records from `data["dualcx.com/service-handshake"]` to `extensions["dualcx.com/service-handshake"]`.
- Move message `operation` and `approval` into `extensions.operations`. Preserve the separate SH operation binding; do not insert it inside the operation.
- Use the new follow-up message request schema for subsequent messages; the opening request schema now also handles accepted Direct Conversation invitations.
- Replace pinned upstream schema copies and their dependencies together, then validate both new examples and rejection of legacy placement. Permissive base schemas may accept unknown old fields without giving them current protocol meaning.
- Keep historical records under their original revision. Reassess pending work deliberately; migration never grants approval or silently clears a restriction.

Steps for a future implementation:

1. Keep old records immutable and labelled with their original version. Never coerce a former integer revision into a current operation identifier.
2. Implement and advertise matching extension version/draft and Operations support. A mismatch must not silently downgrade required checks.
3. Reassess outstanding actions under the new binding, retaining unresolved restrictions. Obtain any required new approval; migration is not permission.
4. Integrate current identity, account and session handling. The supplied documents contain fictional metadata, not credentials or working endpoints.
5. Review the proposed post-approval SH block with implementers and test its behaviour through a real client/company pair before claiming interoperability.

No general API, MCP or browser payload binding is added. No production service or live Neos OS deployment is established by this package. Exact draft matching remains until stable compatibility rules are agreed.
