# Primary Sources

Every spec-derived claim in this pack cites one of the sources below.
Status: **VERIFIED** (read directly from the primary source),
**CROSS-CHECKED** (multiple independent sources agree, each citing the
primary), **UNVERIFIED** (could not be confirmed — never stated as fact).

## S-NIST-01 — FIPS 204 (ML-DSA) — VERIFIED

NIST FIPS 204, *Module-Lattice-Based Digital Signature Standard*,
published and effective 13 Aug 2024. DOI 10.6028/NIST.FIPS.204.
PDF: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf
Publication page: https://csrc.nist.gov/pubs/fips/204/final
Used for: §4 Table 1 (ML-DSA-44/65/87 categories 2/3/5); Table 2
sizes (ML-DSA-65: private 4,032 B, public 1,952 B, signature 3,309 B);
§5.2 signing (context string max 255 bytes; hedged signing default).
Cross-check: RFC 9964 (IETF, May 2026), §5 / Table 1, repeats the
same figures. https://datatracker.ietf.org/doc/rfc9964/

## S-NIST-02 — FIPS 205 (SLH-DSA) — CROSS-CHECKED

NIST FIPS 205, *Stateless Hash-Based Digital Signature Standard*,
published 13 Aug 2024. DOI 10.6028/NIST.FIPS.205.
Publication page: https://csrc.nist.gov/pubs/fips/205/final
PDF: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf
Table 2 figures (12 parameter sets; e.g. SLH-DSA-128s: 32 B public key,
7,856 B signature) agree across four independent secondary sources
that each cite FIPS 205 Table 2 / §11. The FIPS 205 PDF was opened
during this pack's research (2026-11-16) and confirms publication
13 Aug 2024 and the SPHINCS+ basis, but Table 2 was not line-verified
from the PDF text in that pass — the sizes stay CROSS-CHECKED, not
PDF-verified. Caveat: all twelve sets meet their claimed category
"except SLH-DSA-SHA2-128f and SLH-DSA-SHAKE-128f" for message-bound
signatures.

## S-NIST-03 — SP 800-57 Part 1 Rev. 5 — CROSS-CHECKED

NIST SP 800-57 Part 1 Rev. 5, *Recommendation for Key Management:
Part 1 — General*, Elaine Barker, May 2020. DOI:
https://doi.org/10.6028/NIST.SP.800-57pt1r5
Used for: §7 six key states; §8 phases (a key shall not transfer back
to any previous phase); §8.2.3 re-keying vs key update; §5.3
cryptoperiods. Rev. 6 initial public draft published 5 Dec 2025;
Rev. 5 remains the final version as of this research date.

## S-NIST-04 — SP 800-227 (hybrid KEMs, §4.6) — VERIFIED

NIST SP 800-227, *Recommendations for Key-Encapsulation Mechanisms*,
Final, 18 Sep 2025. DOI: https://doi.org/10.6028/NIST.SP.800-227
CSRC: https://csrc.nist.gov/pubs/sp/800/227/final
Used for: §4.6 multi-algorithm KEMs / PQ/T hybrids (a well-designed
hybrid remains secure as long as at least one component remains
secure; X-Wing KEM example). **Scope: KEMs only, NOT signatures.**
There is no equivalent NIST hybrid-signature guidance document; this
pack never cites §4.6 as signature-hybrid authority.

## S-NIST-05 — SP 800-61 Rev. 3 — CROSS-CHECKED

NIST SP 800-61 Rev. 3, *Incident Response Recommendations and
Considerations for Cybersecurity Risk Management: A CSF 2.0 Community
Profile*, April 2025. CSRC: https://csrc.nist.gov/pubs/sp/800/61/r3/final
Used for: Rev. 3 retires the Rev. 2 four-phase lifecycle and reframes
incident response around the six CSF 2.0 functions (Govern, Identify,
Protect, Detect, Respond, Recover). The full Rev. 3 text was not
opened; the mapping is from two independent summaries.

## S-XRPL-01 — Validator keys, manifest, revocation — VERIFIED

- Run a validator: https://xrpl.org/docs/infrastructure/configuration/server-modes/run-xrpld-as-a-validator
  (`validator-keys create_keys`; store `validator-keys.json` offline;
  "If your `secret_key` is compromised, revoke the key immediately.")
- XLS-0045, *Prepublish Validator Lists* (Final):
  "The special sequence UInt(-1) indicates that the master key is
  revoked." https://xls.xrpl.org/xls/XLS-0045-prepublish-validator-lists.html
- `validator-keys` revoke subcommand name: **UNVERIFIED** — the xrpl.org
  pages instruct "revoke the key immediately" without naming a
  subcommand; no command name is asserted in this pack.

## S-XRPL-02 — Account keys — VERIFIED

xrpl.org, Cryptographic Keys / Disable Master Key Pair / Remove a
Regular Key Pair: master key cannot be changed, only disabled
(AccountSet + asfDisableMaster); regular key can be removed/replaced
(SetRegularKey); removal fails with `tecNO_ALTERNATIVE_KEY` if no other
signing method remains. Account-key rotation is NOT validator-key
rotation; the two are never conflated in this pack.

## S-XRPL-03 — Amendments and quorum (80% upstream) — VERIFIED

https://xrpl.org/docs/concepts/networks-and-servers/amendments
"If an amendment receives more than 80% support for two weeks, the
amendment passes." Flag ledgers every 256 ledgers; with 35 validators,
strictly more than 80% means 29 votes (28 is not enough). Ledgers close
every ~3–5 s. `fixAmendmentMajorityCalc` (enabled 2021-04-08) fixed
rounding so the minimum is never less than 80%.

## S-XRPL-04 — Ledger re-sync — VERIFIED

https://xrpl.org/docs/concepts/networks-and-servers/ledger-history/
"When an XRP Ledger server starts, its first priority is to get a
complete copy of the latest validated ledger." Data integrity verified
using cryptographic hashes (LedgerHashes); backfilling is low priority
and may take a long time; `server_info` reports `complete_ledgers`.
Stand-alone load: https://xrpl.org/es-es/docs/infrastructure/testing-and-auditing/load-a-saved-ledger-in-stand-alone-mode

## S-POSTFIATD-01 — Amendment majority 67% — VERIFIED IN SOURCE

https://github.com/postfiatorg/postfiatd, commit
0085a1ff885d6a446369cf73a4430f75af22be55.
`include/xrpl/protocol/SystemParameters.h`, lines 78–88:
`postFixAmendmentMajorityCalcThreshold` = ratio 67/100; pre-fix
204/256 (~79.7%); `defaultAmendmentMajorityTime` = 2 weeks (unchanged).
`src/xrpld/app/misc/detail/AmendmentTable.cpp`: `computeThreshold`
uses the post-fix ratio after `fixAmendmentMajorityCalc` is enabled;
`passes()` requires votes > threshold_. The comment at the `passes()`
site still says "slightly less than 80%" — a stale upstream comment.

## S-POSTFIATD-02 — Manifest revocation identical to upstream — VERIFIED IN SOURCE

Same repo and commit. `src/xrpld/app/misc/detail/Manifest.cpp`:
`Manifest::revoked(sequence)` returns true exactly when sequence ==
max uint32: "The maximum possible sequence number means that the
master key has been revoked." No ML-DSA or rotation-specific code in
this file.

## S-WHITE-01 — PostFiat whitepaper — VERIFIED

Post Fiat Whitepaper, "Post Fiat: A Buy-Side Internet of Value".
https://postfiat.org/whitepaper/ (read 2026-11-15).
Used for: abstract (ML-DSA from genesis; "one organization administers
the current validator fleet"; independently operated validators still a
proposal); §1.11 (ML-DSA-65 from genesis: 1,952-byte public keys,
3,309-byte signatures; q = 24 of 35; 24 × 3,309 = 79,416 signature
bytes; domain-separated contexts incl. bridge witnesses); §1.9 (Cobalt
governance: registry transitions, cross-registry check, t_S < 2q_S −
n_S; height-924 rotation/stolen-key drill; "loss of quorum halts the
chain rather than lowering q"; durable cross-phase fence is a proposed
normative rule, enforcement unestablished).
**NOT FOUND in the whitepaper** (searched "disaster", "compromise",
"amendment", "revok"): no disaster-recovery runbook, no emergency
rotation procedure, no key-compromise response procedure, no
amendment/majority rule, no revocation section. Testnet scale (home
page, https://postfiat.org/): 53 validators, 39 verified domains,
ledger ~6.5M (snapshot Sep 21, 2026).

## S-COSMOS-01 — Validator key rotation — VERIFIED

- Rotate a consensus key: https://docs.cosmos.network/sdk/latest/keys/rotate-validator-key
  (updated 2026-07-29): zero-downtime rotation; one rotation per
  unbonding period; set swaps atomically two heights after execution;
  old key remains slashable for past behaviour until the unbonding period ends.
- Migrate a validator to ML-DSA: https://docs.cosmos.network/sdk/latest/keys/migrate-validator-ml-dsa
  (updated 2026-08-25): `--consensus-key-algo ml_dsa_65`; chain is
  post-quantum secure once validators holding ≥ two thirds of voting
  power report a post-quantum type.
- ADR 016: https://docs.cosmos.network/sdk/v0.47/build/architecture/adr-016-validator-consensus-key-rotation

## S-ETH-01 — Ethereum: no rotation — VERIFIED (community docs)

EthStaker Knowledge Base, https://docs.ethstaker.org/tutorials/updating-withdrawal-credentials/:
withdrawal credentials 0x00 → 0x01 can change once only; after that no
consensus-layer operation replaces the credential — change requires
voluntary exit (~27.3 h / 256 epochs) and re-entry. Corroborated by
ethereum.org staking pages as cited therein. The EthStaker page is
community documentation, not ethereum.org itself — re-verify against
ethereum.org before quoting the final wording elsewhere.

## S-CAB-01 — CA/B Forum BR §4.9.1.1 (24-hour revocation) — CROSS-CHECKED

CA/Browser Forum, *Baseline Requirements*, §4.9.1.1: a certificate
whose secret key is stolen or compromised MUST be revoked within
24 hours. Consistent across DigiCert summaries (2025-08-28 and
2020-07-31). The BR text itself was not opened in this session — cite
the section number; verify the wording at
https://cabforum.org/baseline-requirements-documents/ before quoting it.
