# Limitations

## What was NOT verified

1. **No PFTL procedure exists.** No published PFTL disaster-recovery
   runbook, emergency key-rotation procedure, key-compromise response
   procedure, validator-set recovery procedure, ledger re-sync
   procedure, amendment-state verification procedure, or
   bridge-witness compromise procedure exists in the sources read.
   All runbooks in this pack are **proposals** grounded in XRPL/NIST/
   Cosmos sources, labelled PROPOSED throughout. They must not be
   presented as PFTL-stated procedures.
2. **No live-network testing.** No drill touched a live network, a
   real validator, or a real key. All timings are SIMULATED under the
   model in `scripts/common.py` (ledger close 4 s, alert 8 s, operator
   acknowledgement 900 s assumed). Simulated timings are not
   real-world measurements and must not be quoted as such.
3. **Bridge witnesses.** Witness set size, witness quorum rule, and
   witness rotation rule are not stated in any source read. Runbook (c)
   is the least grounded part of the pack; its separation assumption
   (witness set distinct from the 35-validator set) is a proposal.
4. **postfiatd consensus quorum.** Only the amendment majority (67%)
   was verified in postfiatd source. Whether the ledger-validation
   (consensus) quorum differs from upstream 80% was **not checked**;
   do not assert it either way.
5. **postfiatl1v2 not inspected.** ML-DSA validator signing in PFTL
   lives in postfiatl1v2 (Cobalt), not in postfiatd. The Cobalt code
   was not inspected in this pack's research; the whitepaper's §1.9
   and §1.11 passages are the only Cobalt evidence used.
6. **Validator-set size.** The drills use n = 35, q = 24 from the
   whitepaper's quorum model. The testnet home page reports 53
   validators. If the live set differs, every quorum gate and every
   DERIVED threshold must be recomputed.
7. **FIPS 205 Table 2.** Sizes are CROSS-CHECKED (four independent
   sources), not PDF-line-verified in this pack's research pass. The
   FIPS 205 PDF was opened and confirms publication (13 Aug 2024) and
   the SPHINCS+ basis, but Table 2 was not line-verified from the PDF
   text. Re-check before citing as PDF-verified.
8. **CA/B Forum BR §4.9.1.1.** The 24-hour revocation rule is
   CROSS-CHECKED via DigiCert summaries; the BR text itself was not
   opened. Verify the wording at cabforum.org before quoting it.
9. **SP 800-61 Rev. 3.** The CSF 2.0 mapping is from two independent
   summaries; the full Rev. 3 text was not opened.
10. **Ethereum claims.** Rest partly on EthStaker community
    documentation; re-verify against ethereum.org before quoting the
    final wording elsewhere.
11. **`validator-keys` revoke subcommand.** The exact subcommand name
    (if one exists) is UNVERIFIED; no command name is asserted.
12. **Upstream rippled threshold constant.** The exact upstream ratio
    constant's definition file was not located; the 80% upstream figure
    is established via the xrpl.org Amendments page, not via the
    upstream constant.
13. **Code search.** GitHub code search returned 0 results for every
    query against postfiatd, including strings known to be present —
    the index is unavailable for this repo. Absence of search hits
    proves nothing and is never cited as evidence of absence.

## Failed / inconclusive checks

- **None in the drill harness:** 72/72 checks passed, 0 failed
  (`outputs/run-summary.json`). One harness defect was found and fixed
  during the build (a result-line parser in `run_all.py` that mis-split
  the `RESULT` line); the fix was verified by re-running the full
  harness to 72/72.
- **Inconclusive by design:** the bridge-witness runbook (c) and the
  classical-to-hybrid rotation procedure cannot be confirmed against
  any shipped PFTL procedure, because none exists. They remain
  PROPOSED, not verified.
- **Length / completeness:** the whitepaper's Part 3 evidence table
  ("one rotation accepted, seven invalid fixtures rejected") is cited
  from the whitepaper text; the underlying fixtures were not inspected.

## Assumptions that could change the results

- Operator acknowledgement (900 s) and per-phase action durations are
  assumptions; real incident response will differ.
- The simulated time model assumes a 4 s ledger close; Cobalt's actual
  block time may differ.
- The 35-validator model (A1) vs the reported 53-validator testnet.
