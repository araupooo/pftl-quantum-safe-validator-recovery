# Runbook (a) — Validator Signing-Key Compromise (Classical and Post-Quantum)

> **PROPOSED procedure.** No published PFTL key-compromise procedure
> exists. Each step states its provenance. All drills are SIMULATED.

## Trigger

- Suspected or confirmed exposure of a validator's signing key
  (classical key, or ML-DSA-65 key), e.g. anomalous signatures,
  key material found outside its store, or host compromise.
- Provenance: SP 800-57 Rev. 5 §7 — a key moves to Compromised on
  known *or suspected* exposure; do not wait for proof.

## Detection

1. Automated alert after 2 ledger closes (8 s simulated) on anomalous
   signing behaviour. [PROPOSED — model: `scripts/common.py`]
2. Operator acknowledgement within 900 s simulated (assumption, not
   measured). [PROPOSED]
3. Confirm which key is affected (classical vs ML-DSA-65) and its
   scope: one validator only. [PROPOSED]

## Containment

1. Move the key to **Compromised** state; its use for protection stops.
   [SP 800-57 §7]
2. Isolate the validator: stop signing immediately. Do not sign
   anything further with the suspect key. [PROPOSED, grounded in §7]
3. If a regular/account key is also involved, do not conflate the two:
   account-key rotation (SetRegularKey) is a different mechanism from
   validator-key rotation. [xrpl.org, Cryptographic Keys]

## Rotation / revocation

1. Generate a new key pair **independently** of the old one
   (re-keying). Never derive the new key from the old key — key update
   "could result in a security exposure if an adversary obtains a key
   in the chain of derived keys". [SP 800-57 §8.2.3]
2. Classical case: generate a new classical key pair and publish a new
   manifest. [XRPL validator-keys / manifest mechanics, xrpl.org]
3. ML-DSA-65 case: generate a new ML-DSA-65 pair (public key 1,952 B,
   signature 3,309 B — FIPS 204 Table 2) under a domain-separated
   context (whitepaper §1.11). Publish the rotation authorization.
   [PROPOSED — no shipped ML-DSA rotation code exists in postfiatd]
4. Revoke the old key: publish a manifest with sequence 4,294,967,295
   (max uint32). [XLS-0045; postfiatd `Manifest.cpp`, commit 0085a1ff]
   Target: revocation published within 24 hours of compromise.
   [CA/B Forum BR §4.9.1.1, CROSS-CHECKED]
5. Reference design only: Cosmos rotates with zero downtime by running
   a second node on the new key, submitting the rotation, verifying,
   then retiring the old node. [Cosmos SDK docs — reference, not PFTL]

## Recovery

1. Bring the validator back with the new key; verify it signs and its
   signatures verify under the new public key. [PROPOSED]
2. Confirm the old key's signatures are rejected — mirroring the
   whitepaper height-924 evidence (legitimate rotation committed;
   stolen old key's attempt rejected). [Whitepaper §1.9]

## Verification gates (all must pass)

- [ ] New key signs; old key rejected. (Drill 01: 6/6; Drill 02: 7/7)
- [ ] Manifest sequence strictly increased; revocation sequence is
      4,294,967,295. (Drill 06: 8/8)
- [ ] Quorum signature bytes for q=24 recompute to 79,416
      (DERIVED 24 × 3,309). (Drill 02)
- [ ] No signing occurred with the compromised key after containment.

## Rollback protection

- Manifest sequences are monotonic; a replayed old manifest is rejected.
- A compromised key never returns to Active (SP 800-57 §8: a key shall
  not transfer back to any previous phase).
- A rotation is undone only by a further rotation, never by
  re-activating the old key.

## Quorum-safety gates

- Before, during, and after rotation: remaining honest validators ≥ 24.
  With 1 validator offline, 34 remain — the gate passes trivially.
  Any step that would breach q aborts the rotation.
- Loss of quorum halts the chain rather than lowering q.
  [Whitepaper §1.9]

## Simulated drill results

- Drill 01 (classical): 6/6 checks, simulated recovery 6,348 s.
- Drill 02 (ML-DSA-65): 7/7 checks, simulated recovery 6,388 s.
- Logs: `outputs/drill_01.log`, `outputs/drill_02.log`.
