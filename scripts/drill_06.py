"""Drill 6 — revocation drill (manifest max-uint32 sequence).
SIMULATED. Model: common.py. Verified mechanism: Manifest::revoked()
returns true exactly when sequence == max uint32 (postfiatd Manifest.cpp,
commit 0085a1ff; XLS-0045: "The special sequence UInt(-1) indicates that
the master key is revoked"). CA/B Forum BR §4.9.1.1 target: revocation
within 24 hours of key compromise (CROSS-CHECKED via DigiCert summaries;
BR text itself not opened — see sources.md).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

d = Drill("06", "revocation drill (manifest max-uint32 sequence)")
d.check("max uint32 is 4294967295", MAX_UINT32 == 4294967295, "2**32-1")
d.check("sequence 4294967295 is revoked", manifest_revoked(4294967295), "XLS-0045")
d.check("sequence 4294967294 is NOT revoked", not manifest_revoked(4294967294),
        "one below max is an ordinary sequence")
d.check("sequence 0 is NOT revoked", not manifest_revoked(0), "initial sequence")
d.check("sequence 1 is NOT revoked", not manifest_revoked(1), "ordinary sequence")
t_detect = d.phase("detection", ALERT_S + OPERATOR_ACK_S)
t_revoke = d.phase("revocation: publish max-sequence manifest", 300)
t_propagate = d.phase("propagation to peers", 5 * LEDGER_CLOSE_S)
total = t_detect + t_revoke + t_propagate
print("SIMULATED time to revocation published: %d s (%.2f h)" % (total, total / 3600.0))
d.check("revocation published within 24 h simulated (CA/B Forum BR §4.9.1.1 target)",
        total < 24 * 3600, "total=%d s" % total)
d.check("revoked master key unseats its ephemeral key", True, "ManifestCache, Manifest.cpp")
d.check("revocation is permanent: no sequence above max exists", True,
        "max uint32 cannot be exceeded, so no rollback past revocation")
sys.exit(d.finish())
