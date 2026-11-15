# Claim-to-Evidence Index

Each testable claim → script(s) + output file(s) + result. "DERIVED"
means the number is arithmetic from a sourced figure, with the
arithmetic shown. All drill timings are SIMULATED.

| # | Claim | Evidence | Result |
| --- | --- | --- | --- |
| C1 | ML-DSA-65 public key 1,952 B, signature 3,309 B | `scripts/drill_02.py` → `outputs/drill_02.log` (checks 1–2); S-NIST-01, S-WHITE-01 | PASS |
| C2 | Quorum signature bytes 24 × 3,309 = 79,416 (DERIVED) | `scripts/drill_02.py` → `outputs/drill_02.log` (check 3); S-WHITE-01 §1.11 | PASS |
| C3 | Quorum holds with 1 validator offline (34 ≥ 24) | `scripts/drill_01.py`, `drill_02.py`, `drill_05.py` → logs 01, 02, 05 | PASS |
| C4 | Halt boundary is exactly k = 12 (k = 11 survives, k = 12 halts) | `scripts/drill_03.py` → `outputs/drill_03.log` (checks 1–7) | PASS |
| C5 | Sequential rotation keeps honest signers at q = 24 at every step (k = 11 recovery) | `scripts/drill_07.py` → `outputs/drill_07.log` (checks 6–16) | PASS (17/17) |
| C6 | Manifest revocation = sequence 4,294,967,295; 4,294,967,294 and 0 are not revocations | `scripts/drill_06.py` → `outputs/drill_06.log` (checks 1–5); S-XRPL-01, S-POSTFIATD-02 | PASS |
| C7 | Revocation published within 24 h simulated (1,228 s) | `scripts/drill_06.py` → `outputs/drill_06.log` (check 6); S-CAB-01 | PASS |
| C8 | Emergency rotation completes in under 30 min simulated (668 s) | `scripts/drill_05.py` → `outputs/drill_05.log` (check 1) | PASS |
| C9 | Postfiatd amendment votes needed = 24 (DERIVED: 35 × 67/100 = 23.45, votes > 23.45) | `scripts/drill_09.py` → `outputs/drill_09.log` (checks 1, 3–4); S-POSTFIATD-01 | PASS |
| C10 | Upstream amendment votes needed = 29 (DERIVED: 35 × 80/100 = 28.00, votes > 28.00); 28 votes fail upstream | `scripts/drill_09.py` → `outputs/drill_09.log` (checks 2, 5–6); S-XRPL-03 | PASS |
| C11 | Two-week amendment majority hold unchanged in the fork | `scripts/drill_09.py` → `outputs/drill_09.log` (check 7); S-POSTFIATD-01 | PASS |
| C12 | Ledger re-sync verifies all fetched hashes (1,500/1,500 simulated) | `scripts/drill_08.py` → `outputs/drill_08.log` (check 2); S-XRPL-04 | PASS |
| C13 | Compromised key never returns to Active; replacement is independent re-keying, never key update | `scripts/drill_01.py`, `drill_02.py` → logs 01, 02; S-NIST-03 §7/§8/§8.2.3 | PASS |
| C14 | Old ML-DSA key rejected after rotation (mirrors height-924 stolen-key rejection) | `scripts/drill_02.py`, `drill_05.py` → logs 02, 05; S-WHITE-01 §1.9 | PASS |
| C15 | All 9 drills pass; 72/72 checks, 0 failed | `scripts/run_all.py` → `outputs/run-summary.json` + `outputs/drill_*.log` | PASS |
| C16 | Full run is bounded (well under 5 min; ~0.4 s on this machine) | `scripts/run_all.py` (real wall time, this run); `verification/fresh-clone-verification.log` | PASS |
| C17 | Reproduction is deterministic (no timestamps, no randomness, no network) | `outputs/run-summary.json` (timestamp-free); fresh-clone run reproduces `outputs/` | PASS — see `verification/fresh-clone-verification.log` |
| C18 | No published PFTL disaster-recovery runbook or key-compromise procedure exists | S-WHITE-01 (searched "disaster"/"compromise"/"amendment"/"revok" — no matches); S-POSTFIATD-02 (no rotation code in files checked) | Established by search, not by drill — see limitations.md |

## Claims NOT made

- No claim that any runbook is a published PFTL procedure — all are
  labelled PROPOSED.
- No claim that SP 800-227 §4.6 authorizes hybrid signatures — it is
  KEM-scope only (S-NIST-04).
- No claim about the postfiatd consensus (ledger-validation) quorum —
  it was not checked (see limitations.md).
- No claim that bridge-witness set size or rotation rules are stated
  anywhere — they are not (see limitations.md).
- No real-world recovery-time claim — all timings are SIMULATED.
