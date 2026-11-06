# Shared Governance-Audit Rubric

Common rubric applied to Ethereum protocol governance and Cosmos Hub
on-chain governance. Each rule is scored PASS / FAIL / UNAVAILABLE from
live primary public sources only. A rule that cannot be measured from a
live source is scored UNAVAILABLE, never guessed.

## Ethereum rules

| Rule | Name | Pass criterion | Primary sources |
|------|------|----------------|-----------------|
| ETH-1 | EIP process documented | EIP-1 exists with status Living; every sampled EIP file has parseable front matter with status, type, category | raw.githubusercontent.com/ethereum/EIPs (EIPS/eip-1.md and sampled EIPs, Range fetch) |
| ETH-2 | Upgrade EIPs Final | Every EIP listed for Pectra and Fusaka in all-forks.json has status Final | ethereum/pm all-forks.json + EIP front matter (Range fetch per EIP) |
| ETH-3 | ACD cadence | Latest ACDE and latest ACDC entries in the ethereum/pm README meeting table are at most 30 days old | raw.githubusercontent.com/ethereum/pm README.md ("Previous AllCoreDevs Meetings" table) |
| ETH-4 | Client diversity | No execution client holds more than 66.6% share (supermajority threshold) in any of the page's datasets (ethernodes node share, supermajority validator share); consensus leader share reported from the visible MigaLabs dataset; dataset disagreements recorded as findings | clientdiversity.org (server-rendered page, parsed per dataset div) |
| ETH-5 | Upgrade activation recorded | Latest active fork in all-forks.json has an activation timestamp/epoch in the past and status active; planned forks carry no activation | ethereum/pm all-forks.json |
| ETH-6 | EIP discoverability | The EIPs git tree lists at least 900 EIP files and the eips.ethereum.org /all page lists at least 900 rows | api.github.com ethereum/EIPs git tree; eips.ethereum.org/all |

## Cosmos Hub rules

| Rule | Name | Pass criterion | Primary sources |
|------|------|----------------|-----------------|
| COS-1 | Proposals endpoint live | gov proposals endpoint returns 200; latest proposal id >= 1000; every proposal carries id, status, title | lcd-cosmoshub.keplr.app /cosmos/gov/v1/proposals |
| COS-2 | Params match documented values | Live voting params equal quorum 0.4000, threshold 0.5000, veto_threshold 0.334, voting_period 604800s | lcd-cosmoshub.keplr.app /cosmos/gov/v1/params/voting |
| COS-3 | Turnout meets quorum | For the last 5 decided proposals, turnout (total votes / bonded tokens) >= quorum 0.4000 | proposals + /cosmos/gov/v1/proposals/{id}/tally + /cosmos/staking/v1beta1/pool |
| COS-4 | Deposit params | min_deposit 500 ATOM (500000000 uatom), max_deposit_period 1209600s | lcd-cosmoshub.keplr.app /cosmos/gov/v1/params/deposit |
| COS-5 | Voting-power concentration | Top-10 validators hold < 50% of bonded tokens | /cosmos/staking/v1beta1/validators + /cosmos/staking/v1beta1/pool |
| COS-6 | Voting window is 7 days (3 for expedited) | Last 10 decided proposals all have voting_start_time and voting_end_time with a 604800s window, except proposals flagged expedited, which have a 259200s window | lcd-cosmoshub.keplr.app /cosmos/gov/v1/proposals |

## Scoring

- 2 points per PASS, 0 per FAIL, rule excluded when UNAVAILABLE.
- Total is reported as X/24 with per-rule results; a rule that fails
  does not invalidate the others.
- Every scored claim cites its primary source URL and the harness
  output file holding the unedited retrieval (see index.md).

## Source versions and retrieval timestamps

All retrievals are recorded with UTC and WIB timestamps and, where the
source provides one, a version identifier (git tree SHA, file SHA,
schema_version, LCD response). See outputs/results.json and
walkthrough.log.
