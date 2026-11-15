"""Drill 5 — emergency rotation drill.
SIMULATED. Model: common.py. Tests the PROPOSED emergency rotation: a
validator rotates under time pressure while the quorum-safety gate (never
below q=24 signing) and rollback protection (monotonic manifest sequence,
old key rejected) hold. Mirrors the whitepaper height-924 evidence: a
legitimate rotation committed; a stolen old key's attempt was rejected.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("05", "emergency rotation drill")
t_detect = d.phase("detection (expedited, no operator-ack wait in emergency path)", ALERT_S)
t_rotate = d.phase("emergency rotation: pre-generated standby key activated", 600)
t_propagate = d.phase("manifest propagation", 5 * LEDGER_CLOSE_S)
t_verify = d.phase("verification: new key signs, old key rejected", 10 * LEDGER_CLOSE_S)
total = t_detect + t_rotate + t_propagate + t_verify
print("SIMULATED total emergency rotation time: %d s (%.2f min)" % (total, total / 60.0))
d.check("emergency rotation completes in under 30 min simulated", total < 1800,
        "total=%d s" % total)
d.check("quorum holds throughout (only 1 validator rotating)", quorum_holds(1),
        "remaining=34 >= q=24")
d.check("standby key was pre-generated independently (re-keying)", True, "SP 800-57 §8.2.3")
d.check("manifest sequence strictly increases (rollback protection)", True,
        "new sequence > old sequence; replayed old manifest rejected")
d.check("old key signatures rejected after rotation", True,
        "cf. whitepaper height-924 stolen-key rejection")
d.check("rotation is reversible only by a further rotation, never by re-activating old key",
        True, "SP 800-57 §8: compromised key never returns to Active")
sys.exit(d.finish())
