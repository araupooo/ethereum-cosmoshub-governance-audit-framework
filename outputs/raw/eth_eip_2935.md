---
eip: 2935
title: Serve historical block hashes from state
description: Store and serve last 8191 block hashes as storage slots of a system contract to allow for stateless execution
author: Vitalik Buterin (@vbuterin), Tomasz Stanczak (@tkstanczak), Guillaume Ballet (@gballet), Gajinder Singh (@g11tech), Tanishq Jasoria (@tanishqjasoria), Ignacio Hagopian (@jsign), Jochem Brouwer (@jochem-brouwer), Sina Mahmoodi (@s1na)
discussions-to: https://ethereum-magicians.org/t/eip-2935-save-historical-block-hashes-in-state/4565
status: Final
type: Standards Track
category: Core
created: 2020-09-03
---

## Abstract

Store last `HISTORY_SERVE_WINDOW` historical block hashes in the storage of a system contract as part of the block processing logic. Furthermore this EIP has no impact on `BLOCKHASH` resolution mechanism (and hence its range/costs etc).

## Motivation

EVM implicitly assumes the client has the recent block (hashes) at hand. This assumption is not future-proof given the prospect of stateless clients. Including the block hashes in the state will allow bundling these hashes in the witness provided to a stateless client. This is already possible in the MPT and will become more efficient post-Verkle.

Extending the range of blocks which `BLOCKHASH` can serve (`BLOCKHASH_SERVE_WINDOW`) would have been a semantics change. Using extending that via this contract storage would allow a soft-transition. Rollups can benefit from the longer history window through directly querying this contract.

A side benefit of this approach could be that it allows building/validating proofs related to last `HISTORY_SERVE_WINDOW` ancestors directly against the current state.

## Specification

| Parameter | Value |
| - | - |
| `BLOCKHASH_SERVE_WINDOW`  | `256` |
| `HISTORY_SERVE_WINDOW`    | `8191` |
| `SYSTEM_ADDRESS`          | `0xfffffffffffffffffffffffffffffffffffffffe` |
| `HISTORY_STORAGE_ADDRESS` | `0x0000F90827F1C53a10cb7A02335B175320002935` |

This EIP specifies for storing last `HISTORY_SERVE_WINDOW` block hashes in a ring bu