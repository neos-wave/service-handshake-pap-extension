# Migration from extension version 1

This is a new independent extension draft, not an upgrade to the SH framework. Preserve the earlier proposal in repository history or a release; do not reinterpret its records as version 2.

| Earlier package | New review package |
|---|---|
| Extension `"1"`, wire draft `2026-10-11` | Extension `"2"`, wire draft `2026-11-02` |
| Poppy 0.1 / Operations 1 | Pinned Poppy 0.3 / Operations 2 |
| Integer operation revisions | Opaque Poppy string revisions; SH declaration revisions remain integers |
| `sender` in messages | Current `author` object; Company-set event role |
| Binding inside operation | Binding inside the accompanying Company's `message.data` |
| Confirmation endpoint and proposed-state assumptions | Conversation approval field and ordinary Company assessment replies |
| Custom HTTP 409 action-block response | Removed; a not-started action block is explained in a Company message |
| Nested payload validation only | Full example envelopes checked against pinned upstream schemas plus extension checks |

Steps for a future implementation:

1. Keep old records immutable and labelled with their original version. Never coerce a former integer revision into a current operation identifier.
2. Implement and advertise matching extension version/draft and Operations support. A mismatch must not silently downgrade required checks.
3. Reassess outstanding actions under the new binding, retaining unresolved restrictions. Obtain any required new approval; migration is not permission.
4. Integrate current identity, account and session handling. The supplied documents contain fictional metadata, not credentials or working endpoints.
5. Review the proposed post-approval SH block with implementers and test its behaviour through a real client/company pair before claiming interoperability.

No general API, MCP or browser payload binding is added. No production service or live Neos OS deployment is established by this package. Exact draft matching remains until stable compatibility rules are agreed.
