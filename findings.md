# PFTL Quantum-Safe Validator Recovery Playbook — Findings

> **Status of this document.** Every procedure in this playbook is
> **PROPOSED**. No published PFTL disaster-recovery runbook or
> key-compromise procedure exists: the PostFiat whitepaper contains no
> "disaster", "compromise", "amendment", or revocation procedure
> (searched 2026-11-15), and no ML-DSA validator-key or rotation code
> was found in the postfiatd files checked. Procedures below are built
> from primary sources — NIST standards, XRPL/rippled mechanics,
> postfiatd source, the whitepaper's Cobalt evidence, Cosmos production
> rotation, and CA/B Forum revocation timelines — with the provenance
> of each step stated. Nothing here was tested on a live network: all
> drills are **SIMULATED** (see §7 and `scripts/common.py`).

## 1. Scope and assumptions

**In scope.** Validator signing-key compromise (classical keys and
ML-DSA-65 keys), quorum-member compromise, bridge-witness compromise,
validator-set recovery, ledger re-sync after compromise, and
amendment-state verification — for the PFTL network as described in
the PostFiat whitepaper and the postfiatd fork of rippled.

**Assumptions (stated, not verified).**

- A1. Validator set n = 35, quorum q = 24 (whitepaper §1.11, §1.9).
  The testnet reports 53 validators on the home page; the 35 figure is
  the whitepaper's quorum model and is the basis of every drill here.
  If the live set differs, the quorum gates must be recomputed.
- A2. Validators sign with ML-DSA-65 from genesis (whitepaper §1.11).
  Classical keys appear only as the pre-rotation / legacy case and in
  the XRPL-derived manifest mechanics.
- A3. Operator response: automated alert after 2 ledger closes
  (8 s simulated) plus 900 s (15 min) operator acknowledgement —
  an assumption, not a measurement.
- A4. Ledger close 4 s (XRPL ledgers close every ~3–5 s; 4 s is the
  midpoint).
- A5. Bridge witnesses form a set separate from the 35 validators and
  sign with domain-separated ML-DSA-65 contexts (whitepaper §1.11
  names the context only). Witness set size and rotation rule are
  **not stated** in any source read — the bridge runbook is the most
  speculative part of this playbook (see `limitations.md`).
- A6. Amendment-state verification uses the postfiatd fork rule
  (67% post-fix), not the whitepaper — the whitepaper states no
  amendment rule; governance there is Cobalt registry transitions.

**Out of scope.** Shielded-stack cryptography (classical RedPallas/
Halo2/Pasta per whitepaper §1.11), external-chain bridge contracts,
slashing economics, and any live-network operation.

## 2. Grounded facts

| # | Fact | Source |
| --- | --- | --- |
| F1 | ML-DSA-44/65/87 categories 2/3/5; ML-DSA-65: private 4,032 B, public 1,952 B, signature 3,309 B | FIPS 204 §4 Table 1, Table 2 (PDF-verified) |
| F2 | SLH-DSA: 12 parameter sets, categories 1/3/5; e.g. SLH-DSA-128s: 32 B public key, 7,856 B signature | FIPS 205 Table 2 (CROSS-CHECKED, four sources; see limitations.md) |
| F3 | Key states: pre-activation, active, suspended, deactivated, compromised, destroyed; a compromised key never returns to a previous phase; replacement is re-keying, never key update from the old key | SP 800-57 Rev. 5 §7, §8, §8.2.3 |
| F4 | Hybrid KEM guidance (§4.6) is KEM-scope only; there is no equivalent NIST hybrid-signature guidance | SP 800-227 Final, 18 Sep 2025, §4.6 |
| F5 | Manifest revocation = sequence max uint32 (4,294,967,295) | XLS-0045; postfiatd `Manifest.cpp`, commit 0085a1ff |
| F6 | Amendment majority: postfiatd 67% post-fix (ratio 67/100) vs 80% upstream; 2-week hold unchanged | postfiatd `SystemParameters.h`, commit 0085a1ff; xrpl.org Amendments |
| F7 | Quorum q = 24 of 35; 24 × 3,309 = 79,416 signature bytes (DERIVED); loss of quorum halts the chain | Whitepaper §1.11, §1.9 |
| F8 | Height 924: legitimate rotation of validator 5 committed (authorizations 0–4); stolen old key's attempt rejected | Whitepaper §1.9 |
| F9 | Ledger re-sync: fetch latest validated ledger from peers, verify by cryptographic hashes (LedgerHashes), backfill at low priority | xrpl.org Ledger History |
| F10 | Key-compromise revocation within 24 hours | CA/B Forum BR §4.9.1.1 (CROSS-CHECKED via DigiCert summaries) |
| F11 | Cosmos: production ML-DSA validator rotation (SDK 0.55 / CometBFT 0.40); one rotation per unbonding period; set swaps two heights after execution | Cosmos SDK docs, 2026-07-29 / 2026-08-25 |
| F12 | Ethereum: no protocol-level validator signing-key rotation; exit and re-enter only | EthStaker docs (community docs; re-verify against ethereum.org) |
| F13 | Incident response: SP 800-61 Rev. 3 (Apr 2025) retires the Rev. 2 four-phase lifecycle in favour of the CSF 2.0 functions | SP 800-61 Rev. 3 (CROSS-CHECKED via two summaries) |

## 3. Compromise scenarios

### 3.1 Single validator signing-key compromise (classical)

A validator's classical signing key is suspected exposed. Per SP 800-57
§7 the key moves to Compromised; use for protection stops. The
validator is isolated, a new key pair is generated independently
(re-keying, §8.2.3 — never derived from the old key), and a new manifest
is published. Quorum is unaffected (34 of 35 remain). Drill 01:
6/6 checks, simulated recovery 6,348 s (~1.76 h). Runbook (a).

### 3.2 Single validator ML-DSA-65 key compromise

Same shape as §3.1, with ML-DSA-65 sizes (F1) and the whitepaper's
height-924 precedent: a legitimate rotation commits, a stolen old
key's attempt is rejected for lack of current-registry authorization.
The rotation procedure itself is PROPOSED — no shipped ML-DSA rotation
code exists in postfiatd. Drill 02: 7/7 checks, simulated recovery
6,388 s (~1.77 h). Runbook (a), `rotation.md`.

### 3.3 Quorum-member compromise

k members compromised. The boundary is exact: compromised ≥ 12 leaves
fewer than 24 honest validators, and the chain halts rather than
lowering q (F7). k = 11 is the worst survivable case (24 remain, quorum
exactly met). Recovery must rotate members one at a time so honest
signers never drop below 24. Drill 03: 8/8 checks; drill 07 (set
recovery, k = 11): 17/17 checks, simulated recovery 39,640 s (~11.0 h).
Runbooks (b) and (d).

### 3.4 Bridge-witness compromise

A bridge witness's ML-DSA-65 key is suspected exposed. The witness is
frozen out of attestations, re-keyed under a new domain-separated
context, and re-admitted only after verification. The witness set size
and any quorum rule for witnesses are unstated (A5); this runbook is
PROPOSED and is the least grounded part of the playbook. Drill 04:
6/6 checks, simulated recovery 6,388 s (~1.77 h). Runbook (c).

## 4. Rotation, revocation, and rollback protection

Full procedures in `rotation.md`. Headlines, all drill-tested:

- **Classical-to-hybrid ML-DSA rotation.** PROPOSED procedure: generate
  an ML-DSA-65 key pair offline, publish a new manifest / registry
  authorization, verify the new key signs, retire the old key. Grounded
  in FIPS 204 (F1), the whitepaper's ML-DSA-65-from-genesis claim, and
  the Cosmos production-rotation pattern (F11) as a reference design —
  not as PFTL behaviour.
- **Emergency rotation.** Pre-generated standby key, activated on
  compromise suspicion; drill 05: 6/6 checks, simulated 668 s
  (~11.1 min), under the 30-minute simulated target.
- **Revocation.** Publish a manifest with sequence 4,294,967,295
  (F5). Drill 06: 8/8 checks; revocation published 1,228 s simulated
  after detection, within the 24-hour target (F10).
- **Rollback protection.** Manifest sequences are monotonic; a replayed
  old manifest is rejected; a revoked key can never be re-activated
  (SP 800-57 §8: no return to a previous phase). A rotation is undone
  only by a further rotation, never by re-activating the old key.
- **Quorum-safety gates.** Every rotation asserts remaining honest
  validators ≥ 24 before, during, and after the step; any step that
  would breach q aborts the rotation and halts that validator instead.

## 5. Recovery runbooks

| Runbook | File | Drill |
| --- | --- | --- |
| (a) Validator signing-key compromise | `runbooks/a-signing-key-compromise.md` | 01, 02 |
| (b) Quorum-member compromise | `runbooks/b-quorum-member-compromise.md` | 03 |
| (c) Bridge-witness compromise | `runbooks/c-bridge-witness-compromise.md` | 04 |
| (d) Validator-set recovery | `runbooks/d-validator-set-recovery.md` | 07 |
| (e) Ledger re-sync after compromise | `runbooks/e-ledger-resync.md` | 08 |
| (f) Amendment-state verification | `runbooks/f-amendment-state-verification.md` | 09 |

Each runbook follows: trigger, detection, containment, rotation /
revocation, recovery, verification gates, rollback protection,
quorum-safety gates — every step labelled PROPOSED with its provenance.

## 6. Amendment-state verification

The postfiatd fork changed the post-fix amendment majority from 80%
to 67% (F6), while the 2-week hold is unchanged. DERIVED for 35 trusted
validators: postfiatd needs 24 votes (35 × 67/100 = 23.45; votes must
exceed 23.45), upstream needs 29 (35 × 80/100 = 28.00; votes must exceed
28.00). Note the postfiatd `AmendmentTable.cpp` comment still says
"slightly less than 80%" — a stale upstream comment; the code uses 67%.
Drill 09 verifies all four boundary cases (23 fails / 24 passes under
67%; 28 fails / 29 passes under 80%): 8/8 checks. The whitepaper states
no amendment rule — governance there is Cobalt registry transitions —
so this verification applies to the postfiatd fork rule only.

## 7. Measured drill results

All timings SIMULATED under the model in `scripts/common.py`. They are
not real-world measurements and must not be quoted as such.

| Drill | Checks | Simulated detection | Simulated rotation | Simulated recovery total |
| --- | --- | --- | --- | --- |
| 01 classical compromise | 6/6 | 908 s | 3,600 s | 6,348 s |
| 02 ML-DSA compromise | 7/7 | 908 s | 3,600 s | 6,388 s |
| 03 quorum-member (k=11) | 8/8 | 908 s | 11 × 3,600 s | 40,508 s |
| 04 bridge-witness | 6/6 | 908 s | 3,600 s | 6,388 s |
| 05 emergency rotation | 6/6 | 8 s | 600 s | 668 s |
| 06 revocation | 8/8 | 908 s | 300 s publish | 1,228 s to publish |
| 07 set recovery (k=11) | 17/17 | — | 11 × 3,600 s | 39,640 s |
| 08 ledger re-sync | 6/6 | — | — | 5,220 s |
| 09 amendment verification | 8/8 | — | — | 60 s |

Total: **72/72 checks passed, 0 failed.** Full unedited logs in
`outputs/drill_01.log` … `outputs/drill_09.log`; summary in
`outputs/run-summary.json`.

## 8. Limitations

See `limitations.md` for the full list. In short: all runbooks are
proposals; no live-network testing; simulated timings are not
real-world measurements; bridge-witness procedures are the least
grounded; FIPS 205 Table 2 and CA/B Forum BR §4.9.1.1 are
cross-checked, not read from the primary text in this pass; the
postfiatd consensus (ledger-validation) quorum was not checked for
fork differences — only the amendment majority was verified.
