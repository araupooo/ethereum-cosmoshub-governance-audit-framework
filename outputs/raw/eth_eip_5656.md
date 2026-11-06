---
eip: 5656
title: MCOPY - Memory copying instruction
description: An efficient EVM instruction for copying memory areas
author: Alex Beregszaszi (@axic), Paul Dworzanski (@poemm), Jared Wasinger (@jwasinger), Casey Detrio (@cdetrio), Pawel Bylica (@chfast), Charles Cooper (@charles-cooper)
discussions-to: https://ethereum-magicians.org/t/eip-5656-mcopy-instruction/10890
status: Final
type: Standards Track
category: Core
created: 2021-02-01
---

## Abstract

Provide an efficient EVM instruction for copying memory areas.

## Motivation

Memory copying is a basic operation, yet implementing it on the EVM comes with overhead.

This was recognised and alleviated early on with the introduction of the "identity" precompile, which accomplishes
memory copying by the use of `CALL`'s input and output memory offsets. Its cost is `15 + 3 * (length / 32)` gas, plus
the call overhead. The identity precompile was rendered ineffective by the raise of the cost of `CALL` to 700, but subsequently
the reduction by [EIP-2929](./eip-2929.md) made it slightly more economical.

Copying exact words can be accomplished with `<offset> MLOAD <offset> MSTORE` or `<offset> DUP1 MLOAD DUP2 MSTORE`,
at a cost of at least 12 gas per word. This is fairly efficient if the offsets are known upfront and the copying can be unrolled.
In case copying is implemented at runtime with arbitrary starting offsets, besides the control flow overhead, the offset
will need to be incremented using `32 ADD`, adding at least 6 gas per word.

Copying non-exact words is more tricky, as for the last partial word, both the source and destination needs to be loaded,
masked, or'd, and stored again. This overhead is significant. One edge case is if the last "partial word" is a single byte,
it can be efficiently stored using `MSTORE8`.

As example use case, copying 256 bytes costs:

- at least 757 gas pre-EIP-2929 using the identity precompile
- at least 157 gas post-EIP-2929 using the identity precompile
- at least 96 gas using unrolled `MLOAD`/`MSTORE` instructions
- 2