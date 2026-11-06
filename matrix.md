# Governance-Audit Matrix — Ethereum + Cosmos Hub

Scored 2026-11-06 ~21:40 WIB by `src/fetch_governance.py` (stdlib only,
live primary sources). Total: **10/12 rules PASS (20/24 points)**.
Two rules FAIL (COS-3, COS-5); none UNAVAILABLE. Every scored claim
cites its primary source and the harness output holding the unedited
retrieval; see index.md for the claim-to-evidence map.

## Ethereum — 6/6 PASS

| Rule | Result | Measured value | Primary source |
|------|--------|----------------|----------------|
| ETH-1 EIP process documented | PASS | EIP-1 status Living; 44 sampled EIP files (Pectra 12, Fusaka 13, Dencun 9, sample 10) all have parseable front matter with status/type/category | raw.githubusercontent.com/ethereum/EIPs, EIPS/eip-*.md (Range fetch, first 2 KiB) — outputs/raw/eth_eip_*.md |
| ETH-2 Upgrade EIPs Final | PASS | 24/24 Pectra + Fusaka EIPs status Final (Pectra: 2537, 2935, 6110, 7002, 7251, 7549, 7623, 7642, 7685, 7691, 7702, 7840; Fusaka: 7594, 7823, 7825, 7883, 7892, 7642, 7910, 7917, 7918, 7934, 7935, 7939, 7951) | ethereum/pm all-forks.json (schema 1.0.0) + EIP front matter — outputs/raw/eth_all_forks.json, eth_eip_*.md |
| ETH-3 ACD cadence | PASS | Latest ACDE #248, 22 Oct 2026 (15 days ago); latest ACDC #190, 29 Oct 2026 (8 days ago); 479 rows in the meeting table | ethereum/pm README.md, "Previous AllCoreDevs Meetings" table — outputs/raw/eth_pm_readme.md |
| ETH-4 Client diversity | PASS | Execution: worst leader across datasets 50.13% (Geth, ethernodes node share); supermajority dataset leader 43% (Nethermind/Geth tie). Consensus (MigaLabs, visible): Lighthouse 48.14%. No dataset exceeds the 66.6% supermajority threshold | clientdiversity.org, parsed per dataset div — outputs/raw/eth_client_diversity.html |
| ETH-5 Upgrade activation recorded | PASS | Latest active fork BPO2, activation timestamp 1767747671 (epoch 419072), status active; planned forks Glamsterdam and Hegota carry no activation | ethereum/pm all-forks.json — outputs/raw/eth_all_forks.json |
| ETH-6 EIP discoverability | PASS | Git tree lists 972 EIP files (tree SHA recorded in results.json); eips.ethereum.org/all lists 1,232 rows | api.github.com ethereum/EIPs git tree; eips.ethereum.org/all — outputs/raw/eth_eips_tree.json, eth_eips_all.html |

## Cosmos Hub — 4/6 PASS

| Rule | Result | Measured value | Primary source |
|------|--------|----------------|----------------|
| COS-1 Proposals endpoint live | PASS | 50 proposals returned; latest id 1060 ("Migrate Community Pool USDC.n to USDC.inj via a Community Multisig", PASSED); every proposal carries id, status, title | lcd-cosmoshub.keplr.app /cosmos/gov/v1/proposals — outputs/raw/cosmos_proposals.json |
| COS-2 Params match documented values | PASS | quorum 0.400000000000000000; threshold 0.500000000000000000; veto_threshold 0.334000000000000000; voting_period 604800s | lcd-cosmoshub.keplr.app /cosmos/gov/v1/params/voting — outputs/raw/cosmos_params_voting.json |
| COS-3 Turnout meets quorum | FAIL | Last-5 decided turnouts: #1060 53.44%, #1059 49.41%, #1058 59.02%, #1057 55.77%, #1056 29.90% — #1056 below the 0.4000 quorum | proposals + /cosmos/gov/v1/proposals/{id}/tally + /cosmos/staking/v1beta1/pool — outputs/raw/cosmos_tally_*.json, cosmos_pool.json |
| COS-4 Deposit params | PASS | min_deposit 500 ATOM (500000000 uatom); max_deposit_period 1209600s (14 days) | lcd-cosmoshub.keplr.app /cosmos/gov/v1/params/deposit — outputs/raw/cosmos_params_deposit.json |
| COS-5 Voting-power concentration | FAIL | Top-10 validators hold 56.27% of bonded tokens (191,918,216,784,882 / 341,070,008,069,953 uatom); top-1 holds 18.69%; 180 bonded validators | /cosmos/staking/v1beta1/validators + /cosmos/staking/v1beta1/pool — outputs/raw/cosmos_validators.json, cosmos_pool.json |
| COS-6 Voting window is 7 days (3 for expedited) | PASS | Last-10 decided windows: 9 x 604800s standard, 1 x 259200s expedited (#1055, Gaia v28.2.0 upgrade, expedited=true); all match the expected window for their type | lcd-cosmoshub.keplr.app /cosmos/gov/v1/proposals — outputs/raw/cosmos_proposals.json |

## How the score was computed

`src/fetch_governance.py` fetches each source, saves the raw bytes
under outputs/raw/ with retrieval timestamps (UTC and WIB) and SHA-256,
then scores each rule from the saved files. Re-run:

```bash
python3 src/fetch_governance.py
# writes outputs/results.json, outputs/results.txt, outputs/run_harness.log
```

## Denominator caveat (COS-3)

Turnout is total votes (yes + no + abstain + no_with_veto, from each
proposal's tally) divided by bonded tokens at retrieval time
(341,070,008,069,953 uatom on 2026-11-06 ~21:40 WIB). The LCD does not
serve historical bonded totals, so vote-time turnout for #1056 (voting
ended 2026-09-30) is approximated with the current denominator. For
#1056 to have met the 40% quorum, vote-time bonded tokens would have
had to be at most 254,941,845,536,868 uatom — about 25% below the current
total 5.5 weeks earlier. Bonded supply moves slowly, so the shortfall
is real; see F-2 in findings.md. #1056 was also veto-rejected
(no_with_veto 89.74% of votes cast), so its REJECTED outcome is
over-determined.
