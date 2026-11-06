---
eip: 1153
title: Transient storage opcodes
description: Add opcodes for manipulating state that behaves almost identically to storage but is discarded after every transaction
author: Alexey Akhunov (@AlexeyAkhunov), Moody Salem (@moodysalem)
discussions-to: https://ethereum-magicians.org/t/eip-transient-storage-opcodes/553
status: Final
type: Standards Track
category: Core
created: 2018-06-15
requires: 2200, 3529
---

## Abstract

This proposal introduces transient storage opcodes, which manipulate state that behaves identically to storage, except that transient storage is discarded after every transaction, and `TSTORE` is not subject to the gas stipend check as defined in [EIP-2200](./eip-2200.md). In other words, the values of transient storage are never deserialized from storage or serialized to storage. Thus transient storage is cheaper since it never requires disk access. Transient storage is accessible to smart contracts via 2 new opcodes, `TLOAD` and `TSTORE`, where “T” stands for "transient:"

```
TLOAD  (0x5c)
TSTORE (0x5d)
```

## Motivation

Running a transaction in Ethereum can generate multiple nested frames of execution, each created by `CALL` (or similar) instructions. Contracts can be re-entered during the same transaction, in which case there are more than one frame belonging to one contract. Currently, these frames can communicate in two ways: via inputs/outputs passed via `CALL` instructions, and via storage updates. If there is an intermediate frame belonging to another untrusted contract, communication via inputs/outputs is not secure. Notable example is a reentrancy lock which cannot rely on the intermediate frame to pass through the state of the lock. Communication via storage (`SSTORE`/`SLOAD`) is costly. Transient storage is a dedicated and gas efficient solution to the problem of inter frame communication.

Storage refunds accumulated due to inter frame communication are also limited to 20% of gas spent by a transaction due to [EIP-3529](./eip-3529.md) (introduced in the London h