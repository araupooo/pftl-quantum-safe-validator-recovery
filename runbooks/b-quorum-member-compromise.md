# Runbook (b) — Quorum-Member Compromise

> **PROPOSED procedure.** No published PFTL quorum-compromise
> procedure exists. Each step states its provenance.

## Trigger

- Two or more validators' signing keys suspected or confirmed
  compromised, or coordinated anomalous signing from several members.

## Detection

1. Automated alert after 2 ledger closes (8 s simulated) per member;
   correlate across members to establish k (number compromised).
   [PROPOSED — model: `scripts/common.py`]
2. Operator acknowledgement 900 s simulated (assumption).
   [PROPOSED]

## Containment

1. Move every affected key to Compromised; stop their signing.
   [SP 800-57 §7]
2. Count honest validators: remaining = 35 − k. If remaining < 24,
   the chain has halted — do not attempt to lower q; loss of quorum
   halts the chain rather than lowering q. [Whitepaper §1.9]
3. If k ≥ 12, the runbook switches to halt-and-recover mode: no new
   ledger can commit until honest validators are restored to ≥ 24.
   [PROPOSED, grounded in F7]

## Rotation / revocation

1. Rotate compromised members **one at a time** (sequential rotation).
   Each rotation re-keys independently (SP 800-57 §8.2.3) and publishes
   a new manifest / authorization. [PROPOSED]
2. Revoke each old key with a max-uint32-sequence manifest
   (4,294,967,295). [XLS-0045; postfiatd `Manifest.cpp`]
3. Never rotate two members simultaneously while at the quorum edge:
   at k = 11 exactly 24 honest validators remain, so any additional
   offline validator breaches q. [PROPOSED, drill-verified]

## Recovery

1. After each rotation, verify the new member signs and the old key is
   rejected before starting the next rotation. [PROPOSED]
2. When all k members are rotated, verify the full set (35 honest)
   signs a test ledger. [PROPOSED; drill 07]

## Verification gates

- [ ] k counted correctly; halt boundary verified (k = 11 survives,
      k = 12 halts). (Drill 03: 8/8)
- [ ] Honest signers never dropped below 24 during any rotation step.
      (Drill 07: 17/17)
- [ ] All old keys revoked (max-uint32 manifests published).
- [ ] Registry transition passed a cross-registry check — local-row
      checks alone are insufficient. [Whitepaper §1.9, PROPOSED gate]
- [ ] Old-rule authorizations forbidden after activation.
      [Whitepaper §1.9]

## Rollback protection

- Monotonic manifest sequences; compromised keys never re-activated
  (SP 800-57 §8).
- No authority retroactively alters certificate thresholds.
  [Whitepaper §1.9]

## Quorum-safety gates

| k compromised | Remaining | Chain state |
| --- | --- | --- |
| 1 | 34 | Continues |
| 5 | 30 | Continues |
| 11 | 24 | Continues (quorum exactly met) |
| 12 | 23 | **Halts** |
| 24 | 11 | **Halts** |

Drill 03 verifies every row above. Simulated k = 11 recovery:
40,508 s (~11.25 h) for sequential rotation.
Logs: `outputs/drill_03.log`, `outputs/drill_07.log`.
