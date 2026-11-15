# Runbook (d) — Validator-Set Recovery

> **PROPOSED procedure.** No published PFTL validator-set recovery
> procedure exists. Each step states its provenance.

## Trigger

- A quorum-member compromise (runbook b) has been contained, and the
  set must be rebuilt; or the chain halted after loss of quorum
  (k ≥ 12) and honest validators must be restored to ≥ 24.

## Detection

1. Establish the current set state: which members are compromised,
   isolated, rotated, or honest. Count honest validators.
   [PROPOSED]
2. If the chain halted, confirm the halt is a quorum halt (remaining
   < 24), not a fork: affected servers halt rather than fork.
   [XRPL consensus docs, upstream]

## Containment

1. All compromised keys are Compromised and not signing (runbook b).
   [SP 800-57 §7]
2. Do not lower q and do not accept a reduced quorum to "restart"
   faster. Loss of quorum halts the chain rather than lowering q.
   [Whitepaper §1.9]

## Rotation / revocation (set rebuild)

1. Rotate compromised members one at a time (runbook b, step order).
   Each rotation is an independent re-keying with a new manifest /
   authorization. [SP 800-57 §8.2.3; PROPOSED]
2. After each rotation, verify the new member signs and the old key is
   rejected before the next rotation. [PROPOSED]
3. Registry transition gate: a new set must pass a cross-registry
   check with a bound on Byzantine identities across the transition's
   influence window; local-row checks alone are insufficient.
   [Whitepaper §1.9, PROPOSED gate]
4. Current-registry signers authorize the exact payload, parent lock,
   sequence, slot, and expiry; old-rule authorizations are forbidden
   after activation. [Whitepaper §1.9]

## Recovery

1. When honest validators reach 35 (or the target set size), verify
   the full set signs a test ledger. [PROPOSED; drill 07]
2. Resume normal operation only after every verification gate passes.

## Verification gates

- [ ] All compromised members rotated (drill 07: 11/11 sequential
      rotations, each keeping honest signers at q = 24).
- [ ] Full set (35 honest) signs a test ledger.
- [ ] Cross-registry check passed; no retroactive threshold change.
- [ ] All old keys revoked (max-uint32 manifests).

## Rollback protection

- Monotonic manifest sequences; compromised keys never re-activated.
- A set rebuild is undone only by a further authorized transition,
  never by restoring an old registry. [PROPOSED, grounded in §1.9]

## Quorum-safety gates

- Honest signers never drop below 24 during any rotation step
  (drill 07 asserts this at every step).
- The chain restarts only when honest validators ≥ 24; a restart
  with fewer is forbidden. [PROPOSED, grounded in whitepaper §1.9]

## Simulated drill results

- Drill 07 (k = 11 set recovery): 17/17 checks, simulated recovery
  39,640 s (~11.0 h).
- Log: `outputs/drill_07.log`.
