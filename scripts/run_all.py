"""Run all recovery drills and write the run summary.

Usage: python3 -B scripts/run_all.py   (from the pack root)
  - Runs each drill as a subprocess with -B (no __pycache__ anywhere).
  - Captures each drill's stdout verbatim into outputs/drill_NN.log.
  - Writes outputs/run-summary.json (timestamp-free, deterministic).
  - Exits 0 only if every drill passes every check.
Bounded: the whole run completes in well under 5 minutes (seconds in
practice; all drills are pure computation with no sleeps and no network).
ALL DRILLS ARE SIMULATED. No live network is touched, no real keys used.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PACK_ROOT, "outputs")

DRILLS = [
    ("01", "single validator signing-key compromise (classical)"),
    ("02", "single validator ML-DSA-65 key compromise"),
    ("03", "quorum-member compromise (k of 35)"),
    ("04", "bridge-witness compromise"),
    ("05", "emergency rotation drill"),
    ("06", "revocation drill (manifest max-uint32 sequence)"),
    ("07", "validator-set recovery drill"),
    ("08", "ledger re-sync drill"),
    ("09", "amendment-state verification drill"),
]


def parse_result(text):
    """Parse the RESULT line: 'RESULT NN: X/Y checks passed, Z failed'."""
    import re
    for line in text.splitlines():
        if line.startswith("RESULT "):
            m = re.match(r"RESULT \S+: (\d+)/(\d+) checks passed, (\d+) failed", line)
            if m:
                return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return 0, 0, -1


def main():
    os.makedirs(OUTPUTS, exist_ok=True)
    summary = {
        "simulated": True,
        "deterministic": True,
        "python": "3 stdlib only, no pip installs, no network, no real keys",
        "time_model": "ledger-close=4s, alert=8s, operator-ack=900s (assumed); "
                      "all drill timings are SIMULATED elapsed times",
        "quorum": {"validators": 35, "quorum_q": 24,
                   "amendment_majority_postfiatd_percent": 67,
                   "amendment_majority_upstream_percent": 80},
        "drills": [],
        "total_checks": 0,
        "total_passed": 0,
        "total_failed": 0,
        "overall": "FAIL",
    }
    overall_ok = True
    for drill_id, name in DRILLS:
        script = os.path.join(HERE, "drill_%s.py" % drill_id)
        log_path = os.path.join(OUTPUTS, "drill_%s.log" % drill_id)
        proc = subprocess.run(
            [sys.executable, "-B", script],
            capture_output=True, text=True, cwd=PACK_ROOT)
        output = proc.stdout + proc.stderr
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(output)
        passed, total, failed = parse_result(output)
        ok = proc.returncode == 0 and failed == 0 and total > 0
        overall_ok = overall_ok and ok
        summary["drills"].append({
            "id": drill_id, "name": name, "status": "PASS" if ok else "FAIL",
            "checks": total, "passed": passed, "failed": failed,
            "log": "outputs/drill_%s.log" % drill_id,
        })
        summary["total_checks"] += total
        summary["total_passed"] += passed
        summary["total_failed"] += failed
        print("drill %s: %s (%d/%d passed)" % (drill_id, "PASS" if ok else "FAIL",
                                                passed, total))
    summary["overall"] = "PASS" if overall_ok else "FAIL"
    with open(os.path.join(OUTPUTS, "run-summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=False)
        f.write("\n")
    print("OVERALL: %s — %d/%d checks passed, %d failed"
          % (summary["overall"], summary["total_passed"],
             summary["total_checks"], summary["total_failed"]))
    print("Summary written to outputs/run-summary.json (timestamp-free)")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
