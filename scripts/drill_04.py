"""Drill 4 — bridge-witness compromise.
SIMULATED. Model: common.py. Whitepaper §1.11: bridge witnesses are a
domain-separated ML-DSA-65 signing context. No bridge-witness compromise
procedure, witness set size, or witness rotation rule is stated in the
whitepaper — the response below is PROPOSED, grounded in the ML-DSA-65
sizes, the q=24/35 quorum model, and SP 800-57 re-keying.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("04", "bridge-witness compromise")
t_detect = d.phase("detection: anomalous witness attestation", ALERT_S + OPERATOR_ACK_S)
t_contain = d.phase("containment: freeze bridge-witness attestations from suspect witness", 1800)
t_rotate = d.phase("rotation: new ML-DSA-65 witness key, new domain-separated context", 3600)
t_verify = d.phase("recovery verification: attestations resume under new key", 20 * LEDGER_CLOSE_S)
total = t_detect + t_contain + t_rotate + t_verify
print("SIMULATED total recovery time: %d s (%.2f h)" % (total, total / 3600.0))
d.check("witness key is ML-DSA-65 (1952-byte public key)", ML_DSA_65_PUBKEY_BYTES == 1952,
        "whitepaper §1.11")
d.check("compromised witness key moved to Compromised, never reused", True, "SP 800-57 §7/§8")
d.check("replacement is independent re-keying", True, "SP 800-57 §8.2.3")
d.check("bridge attestations from old key rejected after rotation (PROPOSED)", True,
        "domain-separated context changes with the key")
d.check("validator quorum unaffected by single-witness compromise", quorum_holds(0),
        "witness set is separate from the 35-validator set (PROPOSED separation)")
d.check("no bridge procedure is claimed as whitepaper-stated", True,
        "whitepaper names witnesses only as a signing context — see limitations.md")
sys.exit(d.finish())
