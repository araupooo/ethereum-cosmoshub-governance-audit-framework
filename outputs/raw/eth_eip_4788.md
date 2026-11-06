---
eip: 4788
title: Beacon block root in the EVM
description: Expose beacon chain roots in the EVM
author: Alex Stokes (@ralexstokes), Ansgar Dietrichs (@adietrichs), Danny Ryan (@djrtwo), Martin Holst Swende (@holiman), lightclient (@lightclient)
discussions-to: https://ethereum-magicians.org/t/eip-4788-beacon-root-in-evm/8281
status: Final
type: Standards Track
category: Core
created: 2022-02-10
requires: 1559
---

## Abstract

Commit to the hash tree root of each beacon chain block in the corresponding execution payload header.

Store each of these roots in a smart contract.

## Motivation

Roots of the beacon chain blocks are cryptographic accumulators that allow proofs of arbitrary consensus state.
Exposing these roots inside the EVM allows for trust-minimized access to the consensus layer.
This functionality supports a wide variety of use cases that improve trust assumptions of staking pools,
restaking constructions, smart contract bridges, MEV mitigations and more.

## Specification

| constants                    | value                                        |
|---                           |---                                           |
| `FORK_TIMESTAMP`             | `1710338135`                                          |
| `HISTORY_BUFFER_LENGTH`      | `8191`                                       |
| `SYSTEM_ADDRESS`             | `0xfffffffffffffffffffffffffffffffffffffffe` |
| `BEACON_ROOTS_ADDRESS`       | `0x000F3df6D732807Ef1319fB7B8bB8522d0Beac02` |

### Background

The high-level idea is that each execution block contains the parent beacon block's root. Even in the event of missed slots since the previous block root does not change,
we only need a constant amount of space to represent this "oracle" in each execution block. To improve the usability of this oracle, a small history of block roots
are stored in the contract.

To bound the amount of storage this construction consumes, a ring buffer is used that mirrors a block root accumulator on the consensus layer.

### Block structure and val