# Worked exchanges

All organisations, cases, IDs, limits and terms below are fictional. JSON files are message bodies, event bodies or labelled excerpts, not executable requests with real credentials. No raw evidence or private Neos procedures are included.

## Discovery

`company-discovery.json` is an excerpt of company discovery. `client-metadata.json` is an excerpt of personal-agent metadata. They are not complete discovery documents. Both advertise the same extension draft and Operations support. The company identifies cancellation as requiring extension support on this path, while preserving assisted and human alternatives.

## Case A: damaged delivery, no store credit

Read `message-declaration.json`, `company-declaration.json` and `voucher-denied.json`.

The customer prefers a refund and accepts a replacement, but refuses credit. The company can offer a voucher; that does not make this proposal compatible. The voucher assessment is denied. A refund or replacement requires its own proposal, complete terms and checks. These examples do not grant execution authority or show a completed refund.

## Case B: family broadband cancellation

This scenario assumes Priya has a provider-recognised way to discuss the account. It does not assume that she uses her mother's credentials. Her Poppy User identity, her mother's interests and authority to cancel remain separate questions. The provider must validate their relationship through its trusted process.

Read in this order:

1. `family-declaration.json`: the claimed represented party is identified, while cancellation authority remains unresolved. `family-company-declaration.json` supplies the provider's relevant terms.
2. `operation-message.json`: a company conversation event introduces the proposed operation. `operation-proposed.json` contains that same operation in a convenience wrapper for inspection; it is not a separate message type.
3. `assessment-hold.json`: the company holds cancellation because established billing access is insufficient for that act.
4. `confirmation-blocked.json`: the proposed **HTTP 409 response body** to a confirmation attempt. The operation remains proposed; no confirmation or execution is accepted. This is a fixture of the required behaviour, not proof of a working server.
5. `handover.json`: an incoming summary carries the restriction, missing evidence and accountable role. The company must reconcile it against its trusted record and deliver the resulting context to staff. Sending this message alone does not request or complete a handoff.

There are two independent continuations; do not read them as one successful execution:

- **Authority resolved:** `family-declaration-revised.json` and `assessment-after-evidence.json`. The scenario assumes that the provider has independently established limited delegation through its own process, resolved all applicable checks, and recorded the result locally. Revision 2 records that scope; the agent's revised claim is not what establishes authority. The new allow covers unchanged operation terms for five minutes. Poppy confirmation and fresh execution checks are still needed. Nothing here asserts that cancellation has happened.
- **Concern raised:** `relayed-concern.json`. An alarm dependency is reported before commitment. The provider treats it as raised and follows the applicable safeguarding route. If an allow had already been issued, it must be reassessed; an unresolved material dependency cannot be bypassed with that earlier summary. This concern is not a verified technical finding.

`assessment-incomplete.json` illustrates an earlier intake hold, before either declaration is available. The missing references are left empty and explained; the company offers assistance instead of manufacturing terms.

## Terms and identifiers used here

Core action types and their complementary verbs follow SH Appendix A. `no_new_contract: true` means this case does not authorise creating, replacing or renewing a contract. It grants no permission to cancel an existing one. The provider must confirm this interpretation where material. `cancel-proposal-1` refers to the exact operation summary in these fixtures; it is not a generic cancellation permission.

References such as `account-case-4410`, `mother-case-1` and `priya-user-1` are fictional case references. They are not credentials, personal data to resolve across organisations, or permission to retrieve another person's records. A local trusted case mapping must establish what each reference means.

The discovery example's `actions` describes supported exchange meanings. It does not mean every proposal of those types is permitted. Schema acceptance of an organisation-namespaced action similarly says nothing about whether its meaning is understood or authorised.

`manifest.json` tells the structural tests where to find the extension payload in each JSON file. The tests do not validate full Poppy transport envelopes or establish runtime conformance.
