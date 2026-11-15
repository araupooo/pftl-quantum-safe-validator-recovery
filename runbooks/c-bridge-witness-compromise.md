# Runbook (c) — Bridge-Witness Compromise

> **PROPOSED procedure — the least grounded runbook in this pack.**
> The whitepaper names bridge witnesses only as a domain-separated
> ML-DSA-65 signing context (§1.11). No bridge architecture, witness
> set size, witness quorum rule, or witness rotation rule is stated in
> any source read. Everything below is a proposal grounded in the
> ML-DSA-65 sizes, SP 800-57 key lifecycle, and the validator quorum
> model — not a stated procedure.

## Trigger

- A bridge witness's ML-DSA-65 key suspected or confirmed exposed, or
  anomalous witness attestations observed.

## Detection

1. Automated alert after 2 ledger closes (8 s simulated) on anomalous
   attestations. [PROPOSED]
2. Operator acknowledgement 900 s simulated (assumption). [PROPOSED]
3. Identify the affected witness and the attestations it signed.
   [PROPOSED]

## Containment

1. Move the witness key to Compromised; stop its attestations.
   [SP 800-57 §7]
2. Freeze attestations from the suspect witness; do not accept new
   attestations under the old key. [PROPOSED]
3. Assess blast radius: which bridge operations the witness's
   attestations authorized. The bridge's acceptance rule (how many
   witnesses must attest) is **unstated** — the assessment must state
   the assumed rule explicitly before proceeding. [PROPOSED, UNVERIFIED]

## Rotation / revocation

1. Generate a new ML-DSA-65 witness key pair independently (re-keying).
   [SP 800-57 §8.2.3; FIPS 204 Table 2: public key 1,952 B]
2. Assign a new domain-separated context for the new key, so
   attestations under the old context are distinguishable from the new.
   [PROPOSED, grounded in whitepaper §1.11 domain separation]
3. Publish the rotation; revoke the old witness key.
   [PROPOSED — no revocation mechanism for witnesses is stated]

## Recovery

1. Re-admit the witness only after the new key is verified signing
   under the new context. [PROPOSED]
2. Re-verify any bridge operations attested by the compromised key
   during the exposure window; treat them as suspect until checked.
   [PROPOSED]

## Verification gates

- [ ] Old witness key rejected; new key signs under the new context.
      (Drill 04: 6/6)
- [ ] No attestation accepted from the compromised key after containment.
- [ ] Validator quorum (35/24) unaffected — witness set is separate
      from the validator set. (Drill 04; PROPOSED separation)
- [ ] The assumed bridge acceptance rule is written down, not implied.

## Rollback protection

- Compromised witness key never re-activated (SP 800-57 §8).
- Context change makes old-context attestations distinguishable;
  replay under the old context is rejected. [PROPOSED]

## Quorum-safety gates

- Witness rotation does not remove a validator from signing; the
  35/24 validator quorum is unaffected by a single-witness compromise.
  If witness and validator roles ever overlap on one operator, this
  gate must be re-evaluated — that overlap is not addressed in the
  sources read. [PROPOSED]

## Simulated drill results

- Drill 04: 6/6 checks, simulated recovery 6,388 s (~1.77 h).
- Log: `outputs/drill_04.log`.
