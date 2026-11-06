---
eip: 7939
title: Count leading zeros (CLZ) opcode
description: Opcode to count the number of leading zero bits in a 256-bit word
author: Vectorized (@Vectorized), Georgios Konstantopoulos (@gakonst), Jochem Brouwer (@jochem-brouwer), Ben Adams (@benaadams), Giulio Rebuffo (@Giulio2002)
discussions-to: https://ethereum-magicians.org/t/create-a-new-opcode-for-counting-leading-zeros-clz/10805
status: Final
type: Standards Track
category: Core
created: 2025-04-28
---

## Abstract

Introduce a new opcode, `CLZ(x)`, which pops `x` from the stack and pushes the number of leading zero bits in `x` to the stack. If `x` is zero, pushes 256.

## Motivation

Count leading zeros (CLZ) is a native opcode in many processor architectures (even in RISC architectures like ARM).

It is a basic building block used in math operations, byte operations, compression algorithms, data structures:

- lnWad
- powWad
- lambertW0Wad
- sqrt
- cbrt
- byte string comparisons
- generalized calldata compression/decompression
- bitmaps (for finding the next/previous set/unset bit)
- post quantum signature schemes

Adding a `CLZ` opcode will:

- Lead to cheaper compute.
- Lead to cheaper ZK proving costs. The fastest known Solidity implementation uses several dynamic bitwise right shifts `shr`, which are very expensive to prove. In SP1 rv32im, a 32-bit right shift costs 1.6x more than a 32-bit mul.
- Lead to smaller bytecode size. The fastest known Solidity implementation contains several large constants and is often inlined for performance.

## Specification

A new opcode is introduced: `CLZ` (`0x1e`).

- Pops 1 value from the stack.
- Pushes a value to the stack, according to the following code:

```solidity
/// @dev Count leading zeros.
/// Returns the number of zeros preceding the most significant one bit.
/// If `x` is zero, returns 256.
/// This is the fastest known `CLZ` implementation in Solidity and uses about 184 gas.
function clz(uint256 x) internal pure returns (uint256 r) {
    /// @solidity memory-safe-assembly
    assembly {
      