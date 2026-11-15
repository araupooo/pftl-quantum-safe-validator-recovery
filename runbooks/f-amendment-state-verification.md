# Runbook (f) — Amendment-State Verification

> **PROPOSED procedure for the postfiatd fork rule.** The whitepaper
> states no amendment/majority rule (governance is Cobalt registry
> transitions). This runbook verifies the postfiatd fork's amendment
> rule, verified in source at commit 0085a1ff — not a whitepaper rule.

## Trigger

- An amendment is proposed, nearing its majority hold, or suspected
  to have activated; or an operator must confirm the current
  amendment state after a compromise recovery.

## Detection

1. Read the amendment table: list amendments, their trusted-vote
   counts, and their majority-hold timers. [PROPOSED]
2. Establish the trusted-validator count (35 in this playbook's model).
   [PROPOSED]

## Verification procedure

1. Apply the **postfiatd** post-fix rule: majority = 67%
   (`postFixAmendmentMajorityCalcThreshold`, ratio 67/100,
   `SystemParameters.h`, commit 0085a1ff). Do **not** apply the
   upstream 80% rule — it is wrong for this fork.
2. DERIVED threshold for 35 trusted validators: 35 × 67/100 = 23.45;
   an amendment passes only when votes exceed 23.45, i.e. **≥ 24
   votes**. A 23-vote majority fails; 24 votes pass.
3. Contrast (DERIVED): upstream 80% would need 35 × 80/100 = 28.00,
   i.e. ≥ 29 votes; 28 votes fail upstream ("28 is not enough",
   xrpl.org Amendments).
4. Check the hold: an amendment must maintain its majority for
   **two weeks**; if support drops below the threshold, the amendment
   is temporarily rejected and the two-week period restarts.
   [xrpl.org Amendments; `defaultAmendmentMajorityTime` = 2 weeks,
   unchanged in the fork]
5. Flag the stale comment: postfiatd `AmendmentTable.cpp` still says
   "percentage slightly less than 80%" at the `passes()` site — a stale
   upstream comment. The code uses 67%; trust the code, not the comment.

## Verification gates

- [ ] Vote count recomputed from the amendment table (not from a
      summary page). (Drill 09: 8/8)
- [ ] 23 votes → fails; 24 votes → passes (67% rule).
- [ ] 28 votes → fails; 29 votes → passes (80% upstream contrast).
- [ ] Two-week hold verified: continuous majority, no dip below
      threshold during the window.
- [ ] No amendment is treated as active on a 23-vote (or lower) count.

## Rollback protection

- An amendment that passes applies permanently to all subsequent
  ledger versions; there is no per-ledger rollback. Verify before
  the hold completes — after activation, the change is permanent.
  [xrpl.org Amendments]
- If a vote count was miscounted, correct the count before activation;
  do not "un-pass" an activated amendment. [PROPOSED]

## Quorum-safety gates

- Amendment verification is read-only: it never changes the validator
  set or quorum. Note the DERIVED coincidence that the postfiatd
  amendment threshold (24 votes) equals the Cobalt quorum q = 24 —
  the two are distinct mechanisms and must not be conflated.
  (Drill 09)
- The postfiatd consensus (ledger-validation) quorum was **not**
  checked for fork differences in this pack's research — only the
  amendment majority was verified. Do not assume it matches upstream.
  [UNVERIFIED — see limitations.md]

## Simulated drill results

- Drill 09: 8/8 checks, simulated verification 60 s.
- Log: `outputs/drill_09.log`.
