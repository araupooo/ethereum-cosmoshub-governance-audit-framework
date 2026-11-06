---
eip: 2930
title: Optional access lists
author: Vitalik Buterin (@vbuterin), Martin Swende (@holiman)
discussions-to: https://ethereum-magicians.org/t/eip-2930-optional-access-lists/4561
status: Final
type: Standards Track
category: Core
created: 2020-08-29
requires: 2718, 2929
---

## Simple Summary

Adds a transaction type which contains an access list, a list of addresses and storage keys that the transaction plans to access. Accesses outside the list are possible, but become more expensive.

## Abstract

We introduce a new [EIP-2718](./eip-2718.md) transaction type, with the format `0x01 || rlp([chainId, nonce, gasPrice, gasLimit, to, value, data, accessList, signatureYParity, signatureR, signatureS])`.

The `accessList` specifies a list of addresses and storage keys; these addresses and storage keys are added into the `accessed_addresses` and `accessed_storage_keys` global sets (introduced in [EIP-2929](./eip-2929.md)). A gas cost is charged, though at a discount relative to the cost of accessing outside the list.

## Motivation

This EIP serves two functions:

1. Mitigates contract breakage risks introduced by [EIP-2929](./eip-2929.md), as transactions could pre-specify and pre-pay for the accounts and storage slots that the transaction plans to access; as a result, in the actual execution, the SLOAD and EXT* opcodes would only cost 100 gas: low enough that it would not only prevent breakage due to that EIP but also "unstuck" any contracts that became stuck due to EIP 1884.
2. Introduces the access list format and the logic for handling the format. This logic can later be repurposed for many other purposes, including block-wide witnesses, use in ReGenesis, moving toward static state access over time, and more.

## Specification

### Definitions

**`TransactionType`** `1`.  See [EIP-2718](./eip-2718.md)

**`ChainId`** The transaction only valid on networks with this `chainID`.

**`YParity`** The parity (0 for even, 1 for odd) of the y-value of a secp256k1 signature.


### Parameters

| Constant | Value |
