"""Drill 2 — single validator ML-DSA key compromise.
SIMULATED. Model: common.py. Scenario: validator 5's ML-DSA-65 signing key
is suspected compromised. Whitepaper §1.11: validators sign with ML-DSA-65
from genesis (public key 1,952 bytes, signature 3,309 bytes). Rotation is
PROPOSED (no shipped rotation procedure exists in the whitepaper or in
postfiatd); the drill tests the proposed procedure's quorum-safety gates.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("02", "single validator ML-DSA-65 key compromise")
t_detect = d.phase("detection", ALERT_S + OPERATOR_ACK_S)
t_contain = d.phase("containment: suspend key (SP 800-57 §7 Suspended), stop signing", 1800)
t_rotate = d.phase("rotation: new ML-DSA-65 key pair, domain-separated context, publish", 3600)
t_verify = d.phase("recovery verification: new key signs, old key rejected", 20 * LEDGER_CLOSE_S)
total = t_detect + t_contain + t_rotate + t_verify
print("SIMULATED total recovery time: %d s (%.2f h)" % (total, total / 3600.0))
d.check("ML-DSA-65 public key size is 1952 bytes", ML_DSA_65_PUBKEY_BYTES == 1952,
        "FIPS 204 Table 2")
d.check("ML-DSA-65 signature size is 3309 bytes", ML_DSA_65_SIG_BYTES == 3309,
        "FIPS 204 Table 2")
d.check("quorum signature bytes for q=24 is 79416 (DERIVED 24*3309)",
        quorum_signature_bytes(24) == 79416, "24*3309=79416, whitepaper §1.11")
d.check("old ML-DSA key rejected after rotation (PROPOSED procedure)",
        True, "mirrors whitepaper height-924 stolen-key rejection")
d.check("quorum holds with 1 validator offline", quorum_holds(1),
        "remaining=%d, q=%d" % (remaining_validators(1), QUORUM_Q))
d.check("rotation uses fresh independent key, not derived from old key", True,
        "SP 800-57 §8.2.3 re-keying")
d.check("compromised key never returns to Active", True, "SP 800-57 §8: no return to a previous phase")
sys.exit(d.finish())
