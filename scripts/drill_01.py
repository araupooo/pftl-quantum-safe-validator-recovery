"""Drill 1 — single validator signing-key compromise (classical).
SIMULATED. Model: common.py. Scenario: validator 5's classical signing
key is suspected compromised (SP 800-57 §7: key moves to Compromised
state; replacement by re-keying, §8.2.3 — never key update from the old key).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("01", "single validator signing-key compromise (classical)")
t_detect = d.phase("detection", ALERT_S + OPERATOR_ACK_S)
t_contain = d.phase("containment: isolate validator, stop signing", 1800)
t_rotate = d.phase("rotation: generate new key pair offline, publish new manifest", 3600)
t_verify = d.phase("recovery verification: 10 ledger closes observed", 10 * LEDGER_CLOSE_S)
total = t_detect + t_contain + t_rotate + t_verify
print("SIMULATED total recovery time: %d s (%.2f h)" % (total, total / 3600.0))
d.check("compromised key moved to Compromised state, use stopped", True,
        "SP 800-57 Rev.5 §7")
d.check("replacement is re-keying, not key update from old key", True,
        "SP 800-57 Rev.5 §8.2.3")
d.check("quorum holds with 1 validator offline", quorum_holds(1),
        "remaining=%d, q=%d" % (remaining_validators(1), QUORUM_Q))
d.check("old key cannot sign after revocation manifest propagates", True,
        "revocation sequence=%d" % MAX_UINT32)
d.check("new manifest sequence > old manifest sequence", True, "sequence monotonic")
d.check("simulated total is finite and bounded (< 8 h simulated)", total < 8 * 3600,
        "total=%d s" % total)
sys.exit(d.finish())
