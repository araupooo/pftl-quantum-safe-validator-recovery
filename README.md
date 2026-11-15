# PFTL Quantum-Safe Validator Recovery Playbook

A validator disaster-recovery and key-compromise playbook for the PFTL
network, covering classical and post-quantum (ML-DSA-65) signing-key
compromise, quorum-member compromise, and bridge-witness compromise.
Every runbook is labelled **PROPOSED**: no published PFTL
disaster-recovery runbook or key-compromise procedure exists — the
PostFiat whitepaper contains no disaster-recovery, key-compromise,
amendment, or revocation procedure (see `limitations.md`). Each proposed
step states the primary source it is grounded in (NIST, XRPL/rippled,
postfiatd source, whitepaper, Cosmos, Ethereum, CA/B Forum).

## Reproduction (one command, bounded)

```sh
python3 -B scripts/run_all.py
```

- Runs all 9 simulated drills, writes unedited logs to `outputs/`, and
  writes `outputs/run-summary.json`.
- **Time bound: completes in well under 5 minutes** (measured on this
  machine: ~0.4 s; all drills are pure computation, no sleeps, no network).
- Python 3 standard library only; no pip installs; no network access;
  no real keys are generated or used. All drills are **SIMULATED** —
  no live network is touched.
- `run_all.py` passes `-B` to every subprocess, so no `__pycache__`
  directories are created.

## Verify digests

```sh
sha256sum -c DIGESTS.txt
```

`DIGESTS.txt` covers every deterministic file in the pack except itself.
`outputs/` logs and `outputs/run-summary.json` are deterministic
(no timestamps, no wall-clock times, no randomness) and are covered.
`verification/fresh-clone-verification.log` is excluded from
`DIGESTS.txt` (it records a verification run performed in `/tmp`, not
pack content); the exclusion is documented in the `DIGESTS.txt` header.

## File map

| Path | Contents |
| --- | --- |
| `findings.md` | The playbook: scope, assumptions, scenarios, procedures, measured drill results, limitations |
| `index.html` | The same playbook rendered as a static, self-contained page (no external assets) |
| `runbooks/a-signing-key-compromise.md` | Validator signing-key compromise (classical and post-quantum) |
| `runbooks/b-quorum-member-compromise.md` | Quorum-member compromise |
| `runbooks/c-bridge-witness-compromise.md` | Bridge-witness compromise |
| `runbooks/d-validator-set-recovery.md` | Validator-set recovery |
| `runbooks/e-ledger-resync.md` | Ledger re-sync after compromise |
| `runbooks/f-amendment-state-verification.md` | Amendment-state verification |
| `rotation.md` | Classical-to-hybrid ML-DSA rotation, emergency rotation, revocation |
| `scripts/common.py` | Shared simulated-time and quorum model |
| `scripts/drill_01.py` … `drill_09.py` | One simulated drill per scenario |
| `scripts/run_all.py` | Runs all drills, writes `outputs/` |
| `outputs/drill_*.log` | Unedited drill logs (real output of the final run) |
| `outputs/run-summary.json` | Timestamp-free summary: 72/72 checks passed |
| `verification/fresh-clone-verification.log` | Digest + full-run output from a clean copy in `/tmp` |
| `sources.md` | Primary-source citations for every spec-derived claim |
| `claims.md` | Claim-to-evidence index |
| `limitations.md` | What was not verified; failed/inconclusive checks |
| `DIGESTS.txt` | SHA-256 manifest |

## Key facts (all sourced in `sources.md`)

- Validators sign with **ML-DSA-65** from genesis: 1,952-byte public keys,
  3,309-byte signatures (FIPS 204 Table 2; whitepaper §1.11).
- Quorum **q = 24 of 35** validators; a quorum carries
  24 × 3,309 = **79,416** signature bytes (DERIVED; whitepaper §1.11).
- **Loss of quorum halts the chain** rather than lowering q (whitepaper §1.9).
- Amendment majority in the postfiatd fork is **67%** (post-fix), vs
  **80%** upstream — verified in postfiatd source at commit 0085a1ff.
  DERIVED for 35 trusted validators: 24 votes needed (postfiatd) vs
  29 votes (upstream). Two-week hold unchanged.
- Manifest revocation = sequence **4,294,967,295** (max uint32, XLS-0045).
- Whitepaper height-924 drill: a legitimate rotation committed; a
  stolen old key's attempt was rejected for lack of current-registry
  authorization.
- SP 800-227 §4.6 hybrid guidance is **KEM-scope only** — it is not
  signature-hybrid authority and is never cited as such here.
- Cosmos has production ML-DSA validator rotation; Ethereum has no
  rotation (exit and re-enter only).

## Simulated drill results (summary)

| Drill | Scenario | Checks | Simulated recovery time |
| --- | --- | --- | --- |
| 01 | Single classical key compromise | 6/6 | 6,348 s (~1.76 h) |
| 02 | Single ML-DSA-65 key compromise | 7/7 | 6,388 s (~1.77 h) |
| 03 | Quorum-member compromise (k of 35) | 8/8 | k=11 recovery 40,508 s (~11.25 h) |
| 04 | Bridge-witness compromise | 6/6 | 6,388 s (~1.77 h) |
| 05 | Emergency rotation | 6/6 | 668 s (~11.1 min) |
| 06 | Revocation (max-uint32 manifest) | 8/8 | 1,228 s (~20.5 min) to publish |
| 07 | Validator-set recovery (k=11) | 17/17 | 39,640 s (~11.0 h) |
| 08 | Ledger re-sync (1,500 ledgers) | 6/6 | 5,220 s (~1.45 h) |
| 09 | Amendment-state verification | 8/8 | 60 s |

All timings are **SIMULATED** under the model in `scripts/common.py`
(ledger close 4 s, alert 8 s, operator acknowledgement 900 s assumed).
They are not real-world measurements. Full logs: `outputs/`.

## Limitations (summary)

- All runbooks are **proposals**; no PFTL procedure exists to follow.
- No live-network testing was done; all timings are simulated.
- Bridge-witness set size and rotation rule are not stated anywhere
  in the sources read; the bridge runbook is the most speculative part.
- FIPS 205 Table 2 sizes are cross-checked (four independent sources),
  not PDF-line-verified in this pack's research pass; the FIPS 205 PDF
  was opened and confirms publication (13 Aug 2024) and the SPHINCS+
  basis. CA/B Forum BR §4.9.1.1 (24-hour revocation) is cross-checked
  via DigiCert summaries; the BR text itself was not opened.
- Full list: `limitations.md`.

## Drill environment

- Python 3.12.3, Linux, standard library only.
- Deterministic: no timestamps, no randomness, no network, no wall-clock
  dependence. Re-running `python3 -B scripts/run_all.py` reproduces
  `outputs/` byte-for-byte.
