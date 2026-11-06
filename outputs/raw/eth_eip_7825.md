---
eip: 7825
title: Transaction Gas Limit Cap
description: Introduce a protocol-level cap on the maximum gas used by a transaction to 16,777,216 (2^24).
author: Giulio Rebuffo (@Giulio2002), Toni Wahrstätter (@nerolation)
discussions-to: https://ethereum-magicians.org/t/eip-7825-transaction-gas-limit-cap/21848
status: Final
type: Standards Track
category: Core
created: 2024-11-23
---

## Abstract

This proposal introduces a protocol-level cap on the maximum gas usage per transaction to 16,777,216 (2^24) gas. By implementing this limit, Ethereum can enhance its resilience against certain DoS vectors, improve network stability, and provide more predictability to transaction processing costs, especially in the context of increasing the gas limit.

## Motivation

Currently, transactions can theoretically consume up to the entire block gas limit, which poses several risks:

1. **DoS Attacks**: A single transaction consuming most or all of the block gas can result in uneven load distribution and impact network stability.  
2. **State Bloat Risks**: High-gas transactions often result in larger state changes, increasing the burden on nodes and exacerbating the Ethereum state growth problem.  
3. **Validation Overhead**: High-gas transactions can lead to longer block verification times, negatively impacting user experience and network decentralization.

By limiting individual transactions to a maximum of 16,777,216 gas, we aim to:

- Reduce the risks of single-transaction DoS attacks.  
- Promote fairer gas allocation across transactions within a block.  
- Ensure better synchronization among nodes by mitigating extreme block validation times.

## Specification

### Gas Cap

- Enforce a protocol-level maximum of **16,777,216 gas (2^24)** for any single transaction.  
- This cap applies regardless of the block gas limit set by miners or validators.  
- Transactions specifying gas limits higher than 16,777,216 gas will be rejected with an appropriate error code (e.g., `MAX_GAS_LIMIT_EXCEEDED`).  

### Changes to EVM Behav