# Rotation: Classical-to-Hybrid ML-DSA Rotation, Emergency Rotation, Revocation

> Every procedure here is **PROPOSED**. No shipped ML-DSA rotation
> procedure exists in the whitepaper or in postfiatd. Each step is
> tagged **MEASURED** (drill-tested in this pack — simulated) or
> **PROPOSED** (not drill-tested as a live procedure; grounded in the
> cited source). All drill timings are SIMULATED.

## 1. Classical-to-hybrid ML-DSA rotation

Goal: move a validator from a classical signing key to an ML-DSA-65
signing key without dropping below quorum and without ever trusting
the old key again.

| Step | Tag | Procedure | Provenance |
| --- | --- | --- | --- |
| 1 | PROPOSED | Generate an ML-DSA-65 key pair offline, on hardware separate from the validator; store the private key offline. | FIPS 204 Table 2 (public 1,952 B, signature 3,309 B); XRPL practice — store validator keys offline (xrpl.org) |
| 2 | MEASURED | Quorum-safety gate: assert remaining honest validators ≥ 24 before starting. With 1 rotating, 34 remain. | Drill 02, 7/7; whitepaper §1.9 (q=24/35) |
| 3 | PROPOSED | Publish the rotation authorization: new ML-DSA-65 public key under a domain-separated context for validator signing. | Whitepaper §1.11 (domain-separated contexts); PROPOSED — no shipped procedure |
| 4 | PROPOSED | Verify the new key signs and verifies before retiring the old key. Reference design: Cosmos runs a second node on the new key, submits the rotation, verifies, then retires the old node (zero downtime). | Cosmos SDK docs (reference design, not PFTL behaviour) |
| 5 | MEASURED | Retire the old key: publish a max-uint32-sequence revocation manifest (4,294,967,295). | Drill 06, 8/8; XLS-0045; postfiatd `Manifest.cpp` |
| 6 | MEASURED | Verify the old key's signatures are rejected after rotation. | Drill 02; whitepaper §1.9 height-924 precedent |
| 7 | PROPOSED | Record the rotation: old public key, new public key, manifest sequences, authorizing validators. Keep the record for at least the equivocation-evidence window (Cosmos: at least the unbonding period). | Cosmos SDK docs (reference); SP 800-57 §7 states |

**Hybrid note.** SP 800-227 §4.6 (hybrid KEMs) is KEM-scope only and
is **not** cited as authority for a hybrid signature scheme — there is
no equivalent NIST hybrid-signature guidance document. A "hybrid"
rotation here means: classical key retired, ML-DSA-65 key active, with
both verifiable during the transition window — not a composite
signature algorithm. Do not claim NIST hybrid-signature authority.

## 2. Emergency rotation

Goal: rotate a suspected-compromised key as fast as possible, using a
pre-generated standby key.

| Step | Tag | Procedure | Provenance |
| --- | --- | --- | --- |
| 1 | PROPOSED | Pre-generate a standby ML-DSA-65 key pair per validator, stored offline, **before** any incident. A standby key is an independent re-keying, not derived from the active key. | SP 800-57 §8.2.3 (re-keying); PROPOSED practice |
| 2 | MEASURED | On suspicion, activate the standby key immediately — no operator-ack wait in the emergency path (detection 8 s simulated). | Drill 05, 6/6 |
| 3 | MEASURED | Publish the rotation manifest (600 s simulated) and propagate (5 ledger closes, 20 s simulated). | Drill 05 |
| 4 | MEASURED | Verify: new key signs, old key rejected; manifest sequence strictly increased. | Drill 05 |
| 5 | PROPOSED | After the emergency, generate a fresh standby key — the activated standby is now the active key and must itself be backed by a new standby. | SP 800-57 lifecycle (§7/§8) |

Simulated emergency rotation total: **668 s (~11.1 min)**, under the
30-minute simulated target. Log: `outputs/drill_05.log`.

## 3. Revocation

| Step | Tag | Procedure | Provenance |
| --- | --- | --- | --- |
| 1 | MEASURED | Revocation = publish a manifest with sequence 4,294,967,295 (max uint32). Sequences 0, 1, and 4,294,967,294 are NOT revocations. | Drill 06, 8/8; XLS-0045; postfiatd `Manifest.cpp` |
| 2 | MEASURED | Revocation published 1,228 s simulated after detection — within the 24-hour target. | Drill 06; CA/B Forum BR §4.9.1.1 (CROSS-CHECKED) |
| 3 | PROPOSED | If the master key itself is compromised, disable it (account-level analogue: AccountSet + asfDisableMaster, signed by the master key itself) — and note this is the account-key mechanism, distinct from validator manifest revocation. Do not conflate the two. | xrpl.org, Cryptographic Keys |
| 4 | MEASURED | Revocation is permanent: no sequence above max uint32 exists, so no rollback past revocation is possible. | Drill 06 |

## 4. Rollback protection (applies to all rotations)

- Manifest sequences are monotonic; a replayed old manifest is rejected.
- A compromised key never returns to Active (SP 800-57 §8).
- A rotation is undone only by a further rotation, never by
  re-activating the old key.
- Registry transitions: current-registry signers authorize the exact
  payload, parent lock, sequence, slot, and expiry; old-rule
  authorizations are forbidden after activation; no authority
  retroactively alters certificate thresholds. [Whitepaper §1.9]

## 5. Quorum-safety gates (applies to all rotations)

- Before, during, and after every rotation: remaining honest
  validators ≥ 24. Any step that would breach q aborts.
- Rotations are sequential, never parallel, while at the quorum edge
  (k = 11: exactly 24 honest remain).
- Loss of quorum halts the chain rather than lowering q.
  [Whitepaper §1.9]
- Drill 03 verifies the halt boundary (k = 11 survives, k = 12 halts);
  drill 07 verifies sequential recovery keeps honest signers at q.
