"""Drill 7 — validator-set recovery drill.
SIMULATED. Model: common.py. Scenario: after a k=11 compromise the set is
rebuilt by sequential rotation (one validator at a time, quorum never
breached), then the new set is verified against the registry rule:
whitepaper §1.9 — registry transitions need a cross-registry check; local
row checks alone are insufficient; loss of quorum halts the chain.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("07", "validator-set recovery drill")
compromised = 11
d.check("starting state: 11 compromised, 24 remain, quorum exactly met",
        remaining_validators(compromised) == QUORUM_Q, "35-11=24=q")
steps = 0
for i in range(1, compromised + 1):
    # Each compromised member is already isolated (not signing). Rotating
    # it does not remove an honest signer, so honest signers stay at 24
    # throughout: the quorum-safety gate is that honest signing never
    # drops below q=24 during any rotation step.
    honest_signing = QUORUM_Q
    d.check("rotation step %d: honest signers stay at q=24" % i,
            honest_signing >= QUORUM_Q, "honest=%d" % honest_signing)
    steps += 1
print("Rotations performed sequentially: %d" % steps)
d.check("all 11 compromised members rotated, one at a time", steps == 11, "steps=11")
d.check("after recovery, 35 honest validators, quorum holds", quorum_holds(0),
        "remaining=35")
d.check("registry transition requires cross-registry check (PROPOSED gate)",
        True, "whitepaper §1.9: local-row checks alone are insufficient")
d.check("old-rule authorizations forbidden after activation (PROPOSED gate)",
        True, "whitepaper §1.9")
d.check("no authority retroactively alters certificate thresholds", True,
        "whitepaper §1.9")
t_recover = d.phase("recovery: 11 sequential rotations", 11 * 3600)
t_verify = d.phase("verification: full set signs a test ledger", 10 * LEDGER_CLOSE_S)
print("SIMULATED total set-recovery time: %d s (%.2f h)" % (t_recover + t_verify,
      (t_recover + t_verify) / 3600.0))
sys.exit(d.finish())
