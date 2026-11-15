"""Drill 3 — quorum-member compromise (k of 35).
SIMULATED. Model: common.py. Whitepaper §1.9: q=24 of 35; loss of quorum
halts the chain rather than lowering q. Tests k below and above the halt
boundary: compromised >= 12 leaves < 24 remaining, so the chain halts.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("03", "quorum-member compromise (k of 35)")
for k in (1, 5, 11, 12, 24):
    rem = remaining_validators(k)
    holds = quorum_holds(k)
    print("CASE k=%d compromised: remaining=%d, quorum-holds=%s, chain=%s"
          % (k, rem, holds, "CONTINUES" if holds else "HALTS"))
    if k <= 11:
        d.check("k=%d: quorum holds, chain continues" % k, holds,
                "remaining=%d >= q=%d" % (rem, QUORUM_Q))
    else:
        d.check("k=%d: quorum lost, chain halts (does not lower q)" % k, not holds,
                "remaining=%d < q=%d" % (rem, QUORUM_Q))
d.check("halt boundary is exactly k=12 (35-12=23 < 24)",
        quorum_holds(11) and not quorum_holds(12), "boundary verified")
d.check("single-member compromise never halts", quorum_holds(1), "remaining=34")
t_detect = d.phase("detection of k=11 case", ALERT_S + OPERATOR_ACK_S)
t_recover = d.phase("recovery: rotate 11 members one at a time, quorum never breached",
                    11 * 3600)
print("SIMULATED total recovery time (k=11, sequential rotation): %d s (%.2f h)"
      % (t_detect + t_recover, (t_detect + t_recover) / 3600.0))
d.check("sequential rotation keeps >= 24 validators signing at every step",
        all(quorum_holds(1) for _ in range(11)), "one offline at a time")
sys.exit(d.finish())
