# Claim-to-Evidence Index

Every claim in matrix.md and findings.md maps to the harness script and
its unedited output. Retrieval timestamps are in outputs/results.json
(per source) and outputs/results.txt (run log). Run the harness with
`python3 src/fetch_governance.py`.

## Rule claims (matrix.md)

| Claim | Statement | Script | Unedited output |
|-------|-----------|--------|-----------------|
| M-1 | ETH-1 PASS: EIP-1 Living; 44 sampled EIP files parseable | src/fetch_governance.py (front-matter Range fetch) | outputs/raw/eth_eip_1.md, eth_eip_*.md (44 files); outputs/results.json eip_frontmatter_status |
| M-2 | ETH-2 PASS: 24/24 Pectra + Fusaka EIPs Final | src/fetch_governance.py | outputs/raw/eth_all_forks.json (eips lists); outputs/raw/eth_eip_*.md |
| M-3 | ETH-3 PASS: ACDE #248 (22 Oct 2026), ACDC #190 (29 Oct 2026) | src/fetch_governance.py (README table parse, 479 rows) | outputs/raw/eth_pm_readme.md |
| M-4 | ETH-4 PASS: worst execution leader 50.13% (Geth); consensus leader 48.14% (Lighthouse, MigaLabs) | src/fetch_governance.py (per-dataset div parse) | outputs/raw/eth_client_diversity.html |
| M-5 | ETH-5 PASS: latest active fork BPO2, ts 1767747671, epoch 419072; Glamsterdam/Hegota planned, no activation | src/fetch_governance.py | outputs/raw/eth_all_forks.json (schema 1.0.0) |
| M-6 | ETH-6 PASS: 972 EIP files in git tree; 1,232 rows on /all | src/fetch_governance.py | outputs/raw/eth_eips_tree.json; outputs/raw/eth_eips_all.html |
| M-7 | COS-1 PASS: 50 proposals, latest id 1060, all carry id/status/title | src/fetch_governance.py | outputs/raw/cosmos_proposals.json |
| M-8 | COS-2 PASS: quorum 0.4, threshold 0.5, veto 0.334, voting period 604800s | src/fetch_governance.py | outputs/raw/cosmos_params_voting.json |
| M-9 | COS-3 FAIL: turnouts 53.44/49.41/59.02/55.77/29.90%; #1056 below quorum | src/fetch_governance.py (tally + pool) | outputs/raw/cosmos_tally_1056.json … cosmos_tally_1060.json; outputs/raw/cosmos_pool.json |
| M-10 | COS-4 PASS: min deposit 500 ATOM, max deposit period 1209600s | src/fetch_governance.py | outputs/raw/cosmos_params_deposit.json |
| M-11 | COS-5 FAIL: top-10 validators 56.27% of bonded tokens; top-1 18.69% | src/fetch_governance.py | outputs/raw/cosmos_validators.json (180 bonded); outputs/raw/cosmos_pool.json |
| M-12 | COS-6 PASS: 9 x 604800s standard + 1 x 259200s expedited (#1055) | src/fetch_governance.py | outputs/raw/cosmos_proposals.json |

## Finding claims (findings.md)

| Claim | Statement | Script | Unedited output |
|-------|-----------|--------|-----------------|
| M-13 | F-1: top-10 validators 56.27% (191,918,216,784,882 / 341,070,008,069,953 uatom); top-1 18.69% | src/fetch_governance.py | outputs/raw/cosmos_validators.json; outputs/raw/cosmos_pool.json |
| M-14 | F-2: #1056 turnout 29.90%, veto 89.74% (91,513,508,906,190 / 101,976,738,214,747 uatom); voting 2026-09-23 → 2026-09-30 | src/fetch_governance.py | outputs/raw/cosmos_tally_1056.json; outputs/raw/cosmos_proposals.json |
| M-15 | F-3: latest EL note Meeting 204 (Jan 30, 2025); latest CL note call_150 (Feb 6, 2025); dirs list 199/148 files | src/fetch_governance.py | outputs/raw/eth_acd_el_dir.json; outputs/raw/eth_acd_cl_dir.json; outputs/raw/eth_acd_el_latest.md; outputs/raw/eth_acd_cl_latest.md; outputs/raw/eth_pm_readme.md |
| M-16 | F-4: consensus datasets disagree — MigaLabs Lighthouse 48.14%, Blockprint Teku 99.83%, Rated Teku 53.86% | src/fetch_governance.py | outputs/raw/eth_client_diversity.html |
| M-17 | F-5: supermajority dataset flagged "Data is stale" (not updated in over a year; Lido Q4 2025; Coinbase Q1 2025) | src/fetch_governance.py | outputs/raw/eth_client_diversity.html |
| M-18 | F-6: 260 numbers on /all absent from EIPs tree; ERC-838/7524/8444 resolve in ethereum/ERCs | src/fetch_governance.py | outputs/raw/eth_eips_all.html; outputs/raw/eth_eips_tree.json; outputs/raw/eth_erc_838_head.md, eth_erc_7524_head.md, eth_erc_8444_head.md |
| M-19 | F-7: Geth 50.13% execution node share (ethernodes) | src/fetch_governance.py | outputs/raw/eth_client_diversity.html |
| M-20 | F-8: #1055 expedited, 259200s window, PASSED; expedited threshold 0.667, expedited min deposit 501 ATOM | src/fetch_governance.py | outputs/raw/cosmos_proposals.json; outputs/raw/cosmos_params_voting.json |

## Score

10/12 rules PASS (20/24 points). Failures: COS-3, COS-5. No rule
UNAVAILABLE. Full per-rule detail: outputs/results.json (rules),
outputs/results.txt (run log).

## Source map (primary sources)

| Source | URL | Retrieved |
|--------|-----|-----------|
| EIPs git tree | https://api.github.com/repos/ethereum/EIPs/git/trees/master?recursive=1 | 2026-11-06 ~21:39 WIB — outputs/raw/eth_eips_tree.json |
| EIP files | https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-N.md | 2026-11-06 ~21:39 WIB — outputs/raw/eth_eip_*.md |
| all-forks.json | https://raw.githubusercontent.com/ethereum/pm/master/all-forks.json | 2026-11-06 ~21:39 WIB — outputs/raw/eth_all_forks.json |
| pm README | https://raw.githubusercontent.com/ethereum/pm/master/README.md | 2026-11-06 ~21:39 WIB — outputs/raw/eth_pm_readme.md |
| ACD directories | https://api.github.com/repos/ethereum/pm/contents/AllCoreDevs-EL-Meetings and …-CL-Meetings | 2026-11-06 ~21:39 WIB — outputs/raw/eth_acd_*_dir.json |
| Client diversity | https://clientdiversity.org/ | 2026-11-06 ~21:39 WIB — outputs/raw/eth_client_diversity.html |
| EIPs /all | https://eips.ethereum.org/all | 2026-11-06 ~21:39 WIB — outputs/raw/eth_eips_all.html |
| ERC samples | https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-N.md | 2026-11-06 ~21:39 WIB — outputs/raw/eth_erc_*_head.md |
| Cosmos Hub LCD | https://lcd-cosmoshub.keplr.app/cosmos/gov/v1/… and /cosmos/staking/v1beta1/… | 2026-11-06 ~21:40 WIB — outputs/raw/cosmos_*.json |

## Endpoints that did NOT serve this audit (recorded, not hidden)

- GitHub code search API: requires authentication (401 unauthenticated),
  so EIP status counts across all 972 files were not attempted; the audit
  samples 44 named EIPs instead (M-1, M-2).
- api.cosmos.network, rest.cosmos.directory, cosmos-rest.publicnode.com:
  526 / 501 "Not Implemented" for gov endpoints during probing
  (2026-11-06 ~21:21 WIB); the Keplr LCD served all Cosmos data instead.
- api.mintscan.io: 404 without a key. beaconcha.in: 401 (key required).
- ethernodes.org API: 404 (dead).
