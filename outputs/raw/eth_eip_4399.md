---
eip: 4399
title: Supplant DIFFICULTY opcode with PREVRANDAO
description: Expose beacon chain randomness in the EVM by supplanting DIFFICULTY opcode semantics
author: Mikhail Kalinin (@mkalinin), Danny Ryan (@djrtwo)
discussions-to: https://ethereum-magicians.org/t/eip-4399-supplant-difficulty-opcode-with-random/7368
status: Final
type: Standards Track
category: Core
created: 2021-10-30
requires: 3675
---

## Abstract

This EIP supplants the semantics of the return value of existing `DIFFICULTY (0x44)` opcode and renames the opcode to `PREVRANDAO (0x44)`.

The return value of the `DIFFICULTY (0x44)` instruction after this change is the output of the randomness beacon provided by the beacon chain.


## Motivation

Applications may benefit from using the randomness accumulated by the beacon chain. Thus, randomness outputs produced by the beacon chain should be accessible in the EVM.

At the point of `TRANSITION_BLOCK` of the Proof-of-Stake (PoS) upgrade described in [EIP-3675](./eip-3675.md), the `difficulty` block field **MUST** be `0` thereafter because there is no longer any Proof-of-Work (PoW) seal on the block. This means that the `DIFFICULTY (0x44)` instruction no longer has it's previous semantic meaning, nor a clear "correct" value to return.

Given prior analysis on the usage of `DIFFICULTY`, the value returned by the instruction mixed with other values is a common pattern used by smart contracts to obtain randomness. The instruction with the same number as the `DIFFICULTY` opcode returning outputs of the beacon chain RANDAO implementation makes the upgrade to PoS backwards compatible for existing smart contracts obtaining randomness from the `DIFFICULTY` instruction.

Additionally, changes proposed by this EIP allow for smart contracts to determine whether the upgrade to the PoS has already happened. This can be done by analyzing the return value of the `DIFFICULTY` instruction. A value greater than `2**64` indicates that the transaction is being executed in the PoS block. Decompilers and other similar