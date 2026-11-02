# Review brief for a design-partner discussion

**Status:** independent proposal updated for review against a pinned Poppy 0.3 / Operations 2 baseline. Not adopted, deployed or live-tested.

## What we bring

An existing open service framework, practical contact-centre questions and two service journeys. The direct-customer case follows an unacceptable voucher through an acceptable replacement, approval, execution and completion. The family case separates billing access, cancellation authority and continuity of an essential service.

## What this update contributes

This draft follows Poppy's 2 November extension-message structure and recognises its Links, Disclosures and skill-index capabilities. Our contribution is the service decision and continuity requirements: a refused voucher need not end the request, a held replacement needs a clear next step, and a human transfer must preserve restrictions. We propose using existing Poppy mechanisms where they fit and reviewing the additional commitment check with implementers.

## What we want to test together

1. Can both sides exchange the minimum relevant boundaries without exposing private policy or customer information?
2. Can a refusal leave the service request open, with a compatible alternative and an owned next step?
3. How should an SH restriction arriving after operation approval be represented and enforced without breaking retry guarantees?
4. Can the receiving colleague see the restriction, its reason, required evidence and relevant support needs?
5. Which existing approval mechanisms supply sufficient evidence for each action, and where is an additional check needed?

The open question in item 3 is explicit in Specification §7. This package proposes a conversation response and additional local commitment precondition; it does not claim Poppy has adopted that behaviour. Record delivery into staff workflows and live execution protection also need testing.

## A bounded pilot

Start with the refund/replacement journey, one company and one personal-agent implementation. Agree the evidence mechanisms and action scope, exercise the current Poppy flow, then test a denied option, a held option, changed terms, withdrawn authority, an uncertain execution outcome and a handover. Compare the intended and observed result at each step. Expand only after the bounded path works.

Private prompts, risk methods, thresholds and the wider operational test suite stay outside the public proposal. Optional policy packs can follow evidence from the pilot.
