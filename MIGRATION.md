# Migration to Poppy 1.0 and extension version 3

Review package 6, 25 November 2026. Extension major `"3"`, wire draft `2026-11-25`, published Poppy 1.0 and Operations `"3"`. The service framework and canonical SH-1.2 schemas are unchanged.

This is an incompatible update to the Poppy binding. Preserve earlier records and packages in their original versions; changing a label never renews an approval or supplies authority.

## From review package 5 / wire draft 2026-11-02-r4

| Earlier binding | Version-3 binding |
|---|---|
| Poppy 0.3 / Operations 2 | Frozen published Poppy 1.0 / Operations 3 |
| SH extension `"2"` / `2026-11-02-r4` | SH extension `"3"` / `2026-11-25` |
| One configuration object per Company extension | An array of configurations, one per supported major version |
| Company and OAuth client metadata used to agree extensions | Company discovery plus Personal Agent `Poppy-Version` / `Poppy-Extensions` request headers |
| Client SH settings in OAuth metadata | Local support settings; they are not transmitted as OAuth metadata |
| Conversation protocol without a description | Required description of what that endpoint can help with |
| Follow-up request identified only through `message.id` | Required top-level request `id`, retained on retries |
| Example operations expressed primarily in summary text | Required exact structured `terms`; an optional summary must agree |
| Approval containing only operation and revision | Required `approver` distinguishes `"user"` and `"agent"` |
| User approval required for every operation | Agent approval allowed where a real user instruction covers the terms and applicable service requirements are met |
| An SH post-approval hold could later resume with the same approval | Native `declined` plus SH assessment; the declined approval cannot be reused |
| A later allow could permit resending a previously blocked approval | Later continuation requires a fresh revision and fresh user approval; the decline response returns no new operation |
| Closed extension wrapper objects | Ignore unrecognised additive wrapper metadata while validating known fields; canonical SH declarations remain unchanged and strict |

The new extension schema has a new version-3 URN. Its Company configuration and `localSupport` definitions describe their respective roles; the latter is implementation/test configuration, not a new Poppy message. The two canonical SH schema identifiers and bytes do not change.

## Approval recovery is a behavioural migration

Before an approval arrives, an SH hold can explain that approval or another requirement is missing. That is not a native decline.

After a valid approval arrives, if the action has not started and current service checks prevent commitment, respond with `extensions.operations.declined` and a matching SH non-allow assessment. Perform nothing. Preserve a useful explanation, the case and any remaining service route.

Once declined, **do not resend that approval**, silently execute when a hold clears, or revive it by changing request IDs. If the User wishes to continue and the requirement can be resolved, a subsequent exchange obtains a fresh operation revision and fresh user approval. Changed material terms also create a new SH proposal. Existing instructions cannot automatically approve the revision following a decline.

If execution is in progress, completed or uncertain, do not claim it was declined without effect. Use the native result/retry rules and reconcile the business state before seeking approval for any replacement action.

## Implementation sequence

1. Pin the same published 1.0 documentation and schema snapshot as [SOURCE-LOCK.json](SOURCE-LOCK.json), including transitive schema dependencies.
2. Update Company discovery, request headers and message envelopes together. Maintain the same selected versions within a Session; start another Session to change them.
3. Inspect the advertised SH draft before selecting major version 3. Reject incompatible payloads under the selected extension; preserve permitted assistance when support is absent.
4. Map old open cases deliberately. Keep immutable history, current restrictions and evidence references. Reassess under the new binding without treating migration as permission.
5. Add structured operation terms and honest approval provenance. Decide which actions your service can accept under a prior user instruction and which require an appropriate trusted approval route.
6. Implement native decline/recovery composition and current local execution checks. Separate retry after a transport failure from a terminal declined approval.
7. Run structural, negative and scenario checks, then test the declared scope through an actual Company/client pair before a live interoperability claim.

## Earlier history

Version 1 / draft `2026-10-11` targeted Poppy 0.1. Version 2 / `2026-11-02-r4` moved SH records into `message.extensions` and Operations records into `message.extensions.operations`, used opaque Poppy operation revisions, and removed the custom HTTP 409 action-block response. Package 5 retained that wire draft while improving documentation and test diagnostics.

Those earlier placements, integer revision assumptions and custom confirmation endpoint remain historical. This migration does not reintroduce them. Historical documents are preserved in Git history and the [changelog](CHANGELOG.md).

No general API, MCP or browser SH payload binding, production service or certification claim is added. Version 3 identifies this wire draft; future incompatible wire or behavioural changes require another extension major version.
