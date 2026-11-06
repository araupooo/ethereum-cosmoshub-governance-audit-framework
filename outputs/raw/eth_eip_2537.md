---
eip: 2537
title: Precompile for BLS12-381 curve operations
description: Adds operation on BLS12-381 curve as a precompile in a set necessary to efficiently perform operations such as BLS signature verification.
author: Alex Vlasov (@shamatar), Kelly Olson (@ineffectualproperty), Alex Stokes (@ralexstokes), Antonio Sanso (@asanso)
discussions-to: https://ethereum-magicians.org/t/eip2537-bls12-precompile-discussion-thread/4187
status: Final
type: Standards Track
category: Core
created: 2020-02-21
---

## Abstract

Add functionality to efficiently perform operations over the BLS12-381 curve, including those for BLS signature verification.

Along with the curve arithmetic, multi-scalar-multiplication operations are included to efficiently aggregate public keys or individual signer's signatures during BLS signature verification.

## Motivation

The motivation of this precompile is to add a cryptographic primitive that allows to get 120+ bits of security for operations over pairing friendly curve compared to the existing BN254 precompile that only provides 80 bits of security.

## Specification

### Constants

| Name                | Value | Comment            |
|---------------------|-------|--------------------|
| BLS12_G1ADD         | 0x0b  | precompile address |
| BLS12_G1MSM         | 0x0c  | precompile address |
| BLS12_G2ADD         | 0x0d  | precompile address |
| BLS12_G2MSM         | 0x0e  | precompile address |
| BLS12_PAIRING_CHECK | 0x0f  | precompile address |
| BLS12_MAP_FP_TO_G1  | 0x10  | precompile address |
| BLS12_MAP_FP2_TO_G2 | 0x11  | precompile address |

We introduce *seven* separate precompiles to perform the following operations:

- BLS12_G1ADD - to perform point addition in G1 (curve over base prime field) with a gas cost of `375` gas
- BLS12_G1MSM - to perform multi-scalar-multiplication (MSM) in G1 (curve over base prime field) with a gas cost formula defined in the corresponding section
- BLS12_G2ADD - to perform point addition in G2 (curve over quadratic extension of the base prime f