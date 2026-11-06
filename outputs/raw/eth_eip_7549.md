---
eip: 7549
title: Move committee index outside Attestation
description: Move committee index outside of the signed Attestation message
author: dapplion (@dapplion), Mikhail Kalinin (@mkalinin)
discussions-to: https://ethereum-magicians.org/t/eip-7549-move-committee-index-outside-attestation/16390
status: Final
type: Standards Track
category: Core
created: 2023-11-01
---

## Abstract

Move the committee's `index` field outside of the signed Attestation message to allow aggregation of equal consensus votes.

## Motivation

This proposal aims to make Casper FFG clients more efficient by reducing the average number of pairings needed to verify consensus rules. While all types of clients can benefit from this EIP, ZK circuits proving Casper FFG consensus will likely have the most impact.

On a beacon chain network with at least 262144 active indices, it's necessary to verify a minimum of `ceil(32*64 * 2/3) = 1366` attestations to reach a 2/3 threshold. Participants cast two votes at once: LMD GHOST vote and Casper-FFG vote. However, the Attestation message contains three elements:

1. LMD GHOST vote `(beacon_block_root, slot)`. Note: includes slot in the event (block, slot) voting is adopted.
2. FFG vote `(source, target)`
3. Committee index `(index)`

Signing over the 3rd item causes tuples of equal votes to produce different signing roots. If the committee index is moved outside of the Attestation message, the minimum number of attestations to verify to reach a 2/3 threshold is reduced to `ceil(32 * 2/3) = 22` (a factor of 62).

On-chain attestations can now be packed more space-efficiently into beacon blocks. This proposal allows for up to 8 slots worth of votes in a block, compared to 2 today. In other words, a chain with only 1/8 online proposers can still potentially include all votes on-chain.

## Specification

### Execution layer

This requires no changes to the Execution Layer.

### Consensus layer

- Set `index` field from `AttestationData` to a fixed value of zero
- Move committee indexing data to the o