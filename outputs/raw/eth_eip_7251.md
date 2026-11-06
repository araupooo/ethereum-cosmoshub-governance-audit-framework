---
eip: 7251
title: Increase the MAX_EFFECTIVE_BALANCE
description: Allow validators to have larger effective balances, while maintaining the 32 ETH lower bound.
author: mike (@michaelneuder), Francesco (@fradamt), dapplion (@dapplion), Mikhail (@mkalinin), Aditya (@adiasg), Justin (@justindrake), lightclient (@lightclient), Felix Lange (@fjl)
discussions-to: https://ethereum-magicians.org/t/eip-7251-increase-the-max-effective-balance/15982
status: Final
type: Standards Track
category: Core
created: 2023-06-28
requires: 7002, 7685
---
## Abstract

Increases the constant `MAX_EFFECTIVE_BALANCE`, while keeping the minimum staking balance `32 ETH`. This permits large node operators to consolidate into fewer validators while also allowing solo-stakers to earn compounding rewards and stake in more flexible increments.

## Motivation

As of October 3, 2023, there are currently over 830,000 validators participating in the consensus layer. The size of this set continues to grow due, in part, to the `MAX_EFFECTIVE_BALANCE`, which limits the stake of a single validator to `32 ETH`. This leads to large amounts of "redundant validators", which are controlled by a single entity, possibly running on the same beacon node, but with distinct BLS signing keys. The limit on the `MAX_EFFECTIVE_BALANCE` is technical debt from the original sharding design, in which subcommittees (not the attesting committee but the committee calculated in `is_aggregator`) needed to be majority honest. As a result, keeping the weights of subcommittee members approximately equal reduced the risk of a single large validator containing too much influence. Under the current design, these subcommittees are only used for attestation aggregation, and thus only have a `1/N` honesty assumption.

With the security model of the protocol no longer dependent on a low value for `MAX_EFFECTIVE_BALANCE`, we propose raising this value while keeping the minimum validator threshold of `32 ETH`. This increase aims to reduce the validator set size, thereby reducing the nu