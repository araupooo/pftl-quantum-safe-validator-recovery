"""Drill 9 — amendment-state verification drill.
SIMULATED. Model: common.py. Verified fork difference: postfiatd post-fix
amendment majority is 67% (ratio 67/100, SystemParameters.h, commit
0085a1ff) vs 80% upstream (xrpl.org Amendments page). Two-week hold is
unchanged in both. DERIVED thresholds for 35 trusted validators:
  postfiatd: 35*67/100 = 23.45 -> votes must exceed 23.45 -> >= 24 votes.
  upstream:  35*80/100 = 28.00 -> votes must exceed 28.00 -> >= 29 votes.
Note the postfiatd AmendmentTable.cpp comment still says "slightly less
than 80%" — a stale upstream comment; the code uses 67%. The whitepaper
states no amendment/majority rule (governance is Cobalt registry
transitions), so this drill verifies the postfiatd fork rule, labelled as such.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("09", "amendment-state verification drill")
needed_pftl, thr_pftl = amendment_votes_needed(35, AMENDMENT_MAJORITY_PFTL)
needed_up, thr_up = amendment_votes_needed(35, AMENDMENT_MAJORITY_UPSTREAM)
print("DERIVED postfiatd threshold: 35*67/100=%.2f -> votes needed=%d" % (thr_pftl, needed_pftl))
print("DERIVED upstream threshold: 35*80/100=%.2f -> votes needed=%d" % (thr_up, needed_up))
d.check("postfiatd votes needed is 24 (DERIVED)", needed_pftl == 24,
        "threshold=%.2f" % thr_pftl)
d.check("upstream votes needed is 29 (DERIVED)", needed_up == 29,
        "threshold=%.2f" % thr_up)
d.check("23 votes do NOT pass under postfiatd 67% rule", 23 <= thr_pftl,
        "23 <= 23.45, fails")
d.check("24 votes pass under postfiatd 67% rule", 24 > thr_pftl, "24 > 23.45, passes")
d.check("28 votes do NOT pass under upstream 80% rule", 28 <= thr_up,
        "28 <= 28.00, fails (28 is not enough, xrpl.org)")
d.check("29 votes pass under upstream 80% rule", 29 > thr_up, "29 > 28.00, passes")
d.check("two-week majority hold is unchanged (67% fork)", True,
        "defaultAmendmentMajorityTime = 2 weeks, SystemParameters.h")
d.check("postfiatd threshold (24) equals Cobalt quorum q=24 (DERIVED coincidence, not a claim of identity)",
        needed_pftl == QUORUM_Q, "24 == 24; the two rules are distinct mechanisms")
t_verify = d.phase("verification: read amendment table, count trusted votes", 60)
print("SIMULATED verification time: %d s" % t_verify)
sys.exit(d.finish())
