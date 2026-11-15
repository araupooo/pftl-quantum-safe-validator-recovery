# Runbook (e) — Ledger Re-Sync After Compromise

> **PROPOSED procedure built on an upstream mechanism.** Ledger
> re-sync is documented for XRPL/rippled; the whitepaper states no
> PFTL re-sync procedure. The mechanism below is upstream XRPL
> behaviour, flagged as such — not a whitepaper-stated procedure.

## Trigger

- A validator (or several) was isolated during a compromise response
  and must rejoin; or a node is found to disagree with trusted
  validators and must re-sync.

## Detection

1. The rejoining node reports its ledger state; trusted validators
   disagree with its results, or it is behind the validated ledger.
   [PROPOSED]
2. Confirm the node holds no compromised key material before it
   re-syncs — re-sync first, rejoin signing only after key rotation
   is complete (runbook a). [PROPOSED]

## Containment

1. The re-syncing node does not sign until it is synced and verified.
   [PROPOSED]
2. The node does not trust any single peer's history blindly.
   [XRPL Ledger History docs]

## Re-sync procedure

1. On start, the server's first priority is to get a complete copy of
   the latest validated ledger. [xrpl.org Ledger History]
2. Download missing ledger data from peer servers. [xrpl.org]
3. Verify the data's integrity using cryptographic hashes —
   LedgerHashes confirm the data received is correct and complete.
   A mismatched hash rejects the ledger. [xrpl.org]
4. If trusted validators disagree with the server's results, the
   server fetches the necessary data from its peers to achieve
   consistency. [xrpl.org]
5. Backfilling history is one of the server's lowest priorities and
   may take a long time; it requires at least one direct peer to hold
   the history; `[ledger_history]` config controls backfill depth;
   the server never downloads ledgers scheduled for deletion.
   [xrpl.org]
6. Stand-alone verification option: load a saved ledger with
   `xrpld -a --load --ledger <index-or-hash>`; replay requires both
   the target ledger and the one before it; advance with
   `ledger_accept`. [xrpl.org, Load a Saved Ledger in Stand-Alone Mode]

## Recovery

1. The node catches up to the validated ledger and verifies hashes.
2. Only then does it resume signing (with its rotated key, if the
   compromise required rotation). [PROPOSED]

## Verification gates

- [ ] Latest validated ledger fetched before catching up.
      (Drill 08: 6/6)
- [ ] All fetched ledger hashes verified (drill 08: 1,500/1,500).
- [ ] Tampered ledger hash would be rejected (hash verification).
- [ ] `server_info` reports complete ledgers covering the re-synced
      range. [xrpl.org — `complete_ledgers`]
- [ ] Node resumes signing only after verification passes.

## Rollback protection

- Hash-chained ledger history: a forged or tampered history fails
  hash verification and is rejected. (Whitepaper evidence, §1.9:
  tampered history and forged catch-up were rejected in 24 and 18
  cases — Cobalt devnet evidence, cited as precedent, not as a
  guarantee for this procedure.) [PROPOSED gate]

## Quorum-safety gates

- A re-syncing node does not count toward quorum until it is synced
  and signing with a valid key; the remaining 34 (or fewer) validators
  must still meet q = 24. [PROPOSED]

## Simulated drill results

- Drill 08 (1,500 ledgers behind): 6/6 checks, simulated re-sync
  5,220 s (~1.45 h).
- Log: `outputs/drill_08.log`.
