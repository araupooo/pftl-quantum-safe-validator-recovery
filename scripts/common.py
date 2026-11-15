"""Shared simulation model for the recovery drills.

ALL DRILLS ARE SIMULATED. No live network is touched, no real keys are
generated or used, no real validator is contacted. Every timing below is a
SIMULATED elapsed time produced by an explicit, deterministic model — never
a real-world measurement.

Simulated time model (stated once, used by every drill):
  * Ledger-close interval: 4 seconds (XRPL ledgers close every ~3-5 s;
    4 s is the midpoint; see sources.md S-XRPL-03).
  * Automated detection: an alert fires after 2 ledger closes = 8 s
    simulated, once the anomalous condition is observable on-chain.
  * Operator acknowledgement: 900 s simulated (15 minutes, human-response
    assumption — stated, not measured).
  * Operator action blocks: fixed simulated durations per phase, stated
    in each drill (e.g. isolate 1,800 s, publish manifest 300 s).
  * Propagation: one ledger close (4 s) per hop, stated per drill.
  * No wall-clock time, no timestamps, no randomness anywhere: identical
    input always produces identical output.

Quorum model (whitepaper §1.9, §1.11):
  * Validator set n = 35, quorum q = 24. A ledger/commit needs q votes.
  * Remaining honest validators = 35 - compromised. The chain halts
    (does not lower q) when remaining < 24, i.e. compromised >= 12.
  * Amendment majority in the postfiatd fork: 67% post-fix
    (SystemParameters.h, ratio 67/100, commit 0085a1ff). DERIVED:
    35 * 67 / 100 = 23.45, so votes must exceed 23.45, i.e. >= 24 votes.
    Upstream XRPL is 80%: 35 * 80 / 100 = 28.0, so > 28, i.e. >= 29 votes.

Python 3 standard library only. Run with `python3 -B` (no __pycache__).
"""

N_VALIDATORS = 35
QUORUM_Q = 24
LEDGER_CLOSE_S = 4
ALERT_LEDGERS = 2
ALERT_S = ALERT_LEDGERS * LEDGER_CLOSE_S  # 8 s simulated
OPERATOR_ACK_S = 900  # 15 min, human-response assumption (SIMULATED)
MAX_UINT32 = 2**32 - 1  # 4294967295, manifest revocation sequence (XLS-0045)
ML_DSA_65_SIG_BYTES = 3309
ML_DSA_65_PUBKEY_BYTES = 1952
AMENDMENT_MAJORITY_PFTL = 67  # percent, post-fix, postfiatd
AMENDMENT_MAJORITY_UPSTREAM = 80  # percent, XRPL upstream


def remaining_validators(compromised):
    return N_VALIDATORS - compromised


def quorum_holds(compromised):
    """True when at least q=24 validators remain."""
    return remaining_validators(compromised) >= QUORUM_Q


def quorum_signature_bytes(votes=QUORUM_Q):
    """DERIVED: votes * 3309. 24 * 3309 = 79416 (whitepaper §1.11)."""
    return votes * ML_DSA_65_SIG_BYTES


def amendment_votes_needed(trusted=N_VALIDATORS, percent=AMENDMENT_MAJORITY_PFTL):
    """DERIVED: smallest integer votes v with v > trusted*percent/100."""
    threshold = trusted * percent / 100.0
    needed = int(threshold) + 1
    return needed, threshold


def manifest_revoked(sequence):
    """XLS-0045 / Manifest.cpp: max uint32 sequence means revoked."""
    return sequence == MAX_UINT32


class Drill:
    """Tiny deterministic check harness: counts PASS/FAIL, prints lines."""

    def __init__(self, drill_id, name):
        self.drill_id = drill_id
        self.name = name
        self.passed = 0
        self.failed = 0
        print("DRILL %s: %s" % (drill_id, name))
        print("SIMULATED — no live network touched, no real keys used.")
        print("Time model: ledger-close=%ds, alert=%ds, operator-ack=%ds (assumed)"
              % (LEDGER_CLOSE_S, ALERT_S, OPERATOR_ACK_S))

    def check(self, label, condition, detail=""):
        status = "PASS" if condition else "FAIL"
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        line = "[%s] %s" % (status, label)
        if detail:
            line += " — " + detail
        print(line)
        return condition

    def phase(self, label, seconds):
        print("PHASE %s: %d s simulated" % (label, seconds))
        return seconds

    def finish(self):
        total = self.passed + self.failed
        print("RESULT %s: %d/%d checks passed, %d failed"
              % (self.drill_id, self.passed, total, self.failed))
        return 0 if self.failed == 0 else 1
