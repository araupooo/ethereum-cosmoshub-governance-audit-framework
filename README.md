# Ethereum and Cosmos Hub Governance-Audit Framework

A reusable framework for auditing protocol governance from live primary
public sources: a shared 12-rule rubric, a runnable harness, a scored
matrix, a severity-ranked findings memo, and a claim-to-evidence index.

## Headline result

**10/12 rules PASS (20/24 points)**, scored 2026-11-06 ~21:40 WIB.
Ethereum: 6/6 PASS. Cosmos Hub: 4/6 PASS. The two failures are both on
the Cosmos Hub side: turnout below quorum on proposal #1056 (29.90% vs
40% required) and voting-power concentration (top-10 validators hold
56.27% of bonded tokens).

## Contents

| # | Component | File(s) |
|---|-----------|---------|
| 1 | Shared rubric (12 rules) | `rubric.md` |
| 2 | Runnable harness (Python stdlib only) | `src/fetch_governance.py` |
| 3 | Scored audit matrix | `matrix.md` |
| 4 | Severity-ranked findings memo (F-1..F-8) | `findings.md` |
| 5 | Claim-to-evidence index (M-1..M-20) | `index.md` |
| 6 | Public artifact page | `index.html` |
| 7 | Harness outputs (unedited) | `outputs/results.json`, `outputs/results.txt`, `outputs/run_harness.log`, `outputs/raw/*` (66 files) |

## How to run the audit

```bash
python3 src/fetch_governance.py
# Fetches live data from the primary sources in rubric.md, saves every
# raw retrieval under outputs/raw/ with timestamps and SHA-256, scores
# the 12 rules, and writes outputs/results.json + outputs/results.txt.
# No API keys. No third-party packages. Runtime ~2 minutes.
# Note: the GitHub API calls are unauthenticated (60/hour); a 403
# triggers one 65-second retry inside the harness.
```

## How to use this framework

```bash
# Re-score from the saved retrievals (no network):
python3 -c "import json; print(json.load(open('outputs/results.json'))['score'])"
# Extend the rubric: add a rule to rubric.md, implement it in
# src/fetch_governance.py, and map the claim in index.md.
```

## Most severe measured findings

- F-1 (HIGH): top-10 Cosmos Hub validators hold 56.27% of bonded
  tokens; the top 10 alone exceed the 50% approval threshold and the 40%
  quorum.
- F-2 (HIGH): proposal #1056 decided with 29.90% turnout, below the 40%
  quorum; independently veto-rejected at 89.74% no-with-veto.
- F-3 (MEDIUM): Ethereum ACD meeting notes moved out of the canonical
  repo directories (latest notes Jan/Feb 2025); the live record is the
  README meeting table plus external transcripts.
- F-4 (MEDIUM): the three consensus client-diversity datasets disagree
  on the leader (MigaLabs: Lighthouse 48.14%; Blockprint: Teku 99.83%;
  Rated: Teku 53.86%).

## Public artifact

The page in `index.html` presents the scored matrix and the findings
memo. Its content is fixed at build time and embeds the measured values
from this pack (it does not re-derive them at runtime).

## Environment and provenance

Harness: Python 3 stdlib only, Linux VM. All measurements retrieved
2026-11-06 ~21:39-21:40 WIB from the primary sources listed in
index.md. Specification-derived values are labelled as such; everything
else is measured from live responses saved under outputs/raw/.
