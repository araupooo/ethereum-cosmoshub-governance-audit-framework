# Findings Memo — Ethereum + Cosmos Hub Governance Audit

Severity-ranked findings from the live-data harness run of 2026-11-06
~21:40 WIB (10/12 rules PASS, 20/24 points). Every finding cites the
measured value and the harness output that proves it; see index.md.

## F-1 — HIGH — Cosmos Hub voting power is concentrated: top-10 validators hold 56.27% of bonded tokens

- Measured: top-10 of 180 bonded validators hold 191,918,216,784,882 of
  341,070,008,069,953 uatom bonded (56.27%); the largest single validator
  holds 18.69%.
- Why it matters: the top 10 alone exceed the 50% approval threshold and
  the 40% quorum. Ten validators voting together can meet quorum and pass
  any proposal without any other participation; the top 1 alone is nearly
  half of quorum. This is the measured concentration of the live set, not
  a worst-case model.
- Evidence: outputs/raw/cosmos_validators.json (180 bonded validators),
  outputs/raw/cosmos_pool.json (bonded total), outputs/results.json
  (cosmos_top10_share 0.5627, cosmos_top1_share 0.1869).
- Remediation: no protocol change is proposed here; the audit records the
  concentration so delegators and proposal authors can see it. Reducing it
  requires delegation to spread beyond the top 10.

## F-2 — HIGH — Cosmos Hub proposal #1056 was decided with turnout below quorum (29.90% vs 40% required)

- Measured: proposal #1056, "ATOM Refund & Justice Bounty"
  (PROPOSAL_STATUS_REJECTED, voting 2026-09-23 → 2026-09-30), total votes
  101,976,738,214,747 uatom against 341,070,008,069,953 uatom bonded =
  29.90% turnout, below the 0.4000 quorum. The other four of the last five
  decided proposals cleared quorum (49.41%–59.02%).
- The outcome is over-determined: no_with_veto was 91,513,508,906,190
  uatom, 89.74% of votes cast, far above the 0.334 veto threshold — so
  #1056 was veto-rejected regardless of quorum. But the quorum shortfall
  is a separate fact: fewer than 3 in 10 bonded ATOM voted at all.
- Denominator caveat: turnout uses bonded tokens at retrieval time; the
  LCD does not serve historical bonded totals. For #1056 to have met
  quorum, vote-time bonded would have had to be ≤ 254,941,845,536,868
  uatom, ~25% below the current total 5.5 weeks earlier — an implausible
  move for bonded supply, so the shortfall is real.
- Evidence: outputs/raw/cosmos_tally_1056.json, outputs/raw/cosmos_pool.json,
  outputs/raw/cosmos_proposals.json, outputs/results.json (COS-3 FAIL).
- Remediation: quorum is a chain parameter (0.4000); the finding is about
  participation, not the parameter. Proposals with contentious or
  low-salience topics should expect sub-quorum turnout and plan outreach
  accordingly.

## F-3 — MEDIUM — Ethereum ACD meeting notes have moved out of the canonical repo directories

- Measured: the per-meeting markdown directories in ethereum/pm are
  stale archives. Latest EL note: "Meeting 204.md", dated Jan 30, 2025.
  Latest CL note: "call_150.md", dated Feb 6, 2025. The directories list
  199 (EL) and 148 (CL) files. (The EL directory's numeric maximum,
  2016, is a 2016-dated file, not the latest meeting.)
- The live record is now the README's "Previous AllCoreDevs Meetings"
  table: latest ACDE #248 (22 Oct 2026) and ACDC #190 (29 Oct 2026),
  with transcripts at nixorokish/eth-protocol-transcripts and video on
  the EthereumProtocol YouTube channel, indexed by Forkcast. The calls
  themselves are healthy (ETH-3 PASS); only the notes location moved.
- Why it matters: anyone auditing from the directories alone will
  conclude the calls stopped in early 2025. The README table is the
  authoritative cadence source, and this audit scores it as such.
- Evidence: outputs/raw/eth_acd_el_dir.json, outputs/raw/eth_acd_cl_dir.json,
  outputs/raw/eth_acd_el_latest.md, outputs/raw/eth_acd_cl_latest.md,
  outputs/raw/eth_pm_readme.md (479 table rows).
- Remediation: a pointer file in each stale directory naming the README
  table and the transcript repo would close the trap for future auditors.

## F-4 — MEDIUM — Client-diversity datasets disagree on the consensus leader

- Measured on clientdiversity.org (retrieved 2026-11-06 ~21:40 WIB),
  three consensus datasets on the same page:
  - MigaLabs (visible default): Lighthouse 48.14%, Nimbus 17.98%,
    Prysm 17.53%, Teku 6.40%.
  - Blockprint (hidden): Teku 99.83%, Lighthouse 0.16%, Lodestar 0.01%.
  - Rated (hidden): Teku 53.86%, Prysm 21.17%, Lighthouse 20.60%.
  Two different leaders across datasets; Blockprint's 99.83% Teku is not
  credible as a network share and reads as an identification-coverage
  artifact.
- Why it matters: any claim about consensus client diversity must name
  its dataset. The rubric scores the visible MigaLabs dataset (leader
  48.14% < 66.6%, ETH-4 PASS), but a reader who opens the Blockprint tab
  gets a contradictory picture.
- Evidence: outputs/raw/eth_client_diversity.html,
  outputs/results.json (client_diversity_datasets).

## F-5 — MEDIUM — The default-visible execution dataset is flagged stale

- Measured: the "supermajority" execution dataset (the visible default;
  Nethermind 43%, Geth 43%, Besu 8%, Reth 3%, Erigon 3%) carries a
  "Data is stale" warning: "Most of this data hasn't been updated in over
  a year", Lido data from Q4 2025, Coinbase data from Q1 2025, and "does
  not take into account consolidations so it skews results towards older
  data."
- The ethernodes node-share dataset (Geth 50.13%, Nethermind 25.46%,
  Besu 9.45%, Reth 7.67%, Erigon 6.53%) sits behind a toggle (hidden by
  default). Both datasets agree no client exceeds 66.6% (ETH-4 PASS).
- Evidence: outputs/raw/eth_client_diversity.html,
  outputs/results.json (execution_supermajority_stale_note).

## F-6 — LOW — The EIP catalogue is split across two repos

- Measured: eips.ethereum.org/all lists 1,232 distinct EIP numbers, but
  ethereum/EIPs master holds 972 files. The 260 numbers present on the
  site but absent from the tree are ERCs, now housed in ethereum/ERCs
  (verified: ERC-838, ERC-7524, ERC-8444 all resolve in the ERCs repo;
  ERC-7524 is "PLUME Signature in Wallets").
- Why it matters: tooling that clones only ethereum/EIPs silently misses
  260 standards, and the unified site list masks the split.
- Evidence: outputs/raw/eth_eips_all.html, outputs/raw/eth_eips_tree.json,
  outputs/raw/eth_erc_838_head.md, eth_erc_7524_head.md, eth_erc_8444_head.md,
  outputs/results.json (eips_page_not_in_tree_count 260).

## F-7 — LOW — Geth holds a 50.13% execution node share

- Measured: ethernodes dataset, Geth 50.13% of execution nodes — above a
  simple majority, below the 66.6% supermajority threshold (ETH-4 PASS).
  The supermajority (validator-weighted) dataset instead shows a 43%/43%
  Nethermind/Geth tie.
- Why it matters: the network is one majority-client incident away from
  the long-standing Geth-majority concern; the margin to the supermajority
  line is 16.5 points, and to the majority line it is already crossed on
  node share.
- Evidence: outputs/raw/eth_client_diversity.html.

## F-8 — INFO — Expedited proposals use a 3-day window and a higher threshold

- Measured: proposal #1055, "Gaia v28.2.0 upgrade", expedited=true, voted
  2026-09-17 → 2026-09-20 (259,200s) and PASSED. Live params confirm the
  expedited path: expedited_voting_period 259200s, expedited_threshold
  0.667, expedited_min_deposit 501 ATOM (501000000 uatom) vs the standard
  500 ATOM. All other last-10 decided proposals used the standard 604800s
  window (COS-6 PASS).
- Why it matters: the expedited path exists and is used for upgrades; its
  higher threshold and deposit are the compensating controls for the
  shorter window.
- Evidence: outputs/raw/cosmos_proposals.json,
  outputs/raw/cosmos_params_voting.json.
