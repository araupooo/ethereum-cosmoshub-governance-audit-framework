---
eip: 7918
title: Blob base fee bounded by execution cost
description: Imposes that the price of GAS_PER_BLOB blob gas is greater than the price of BLOB_BASE_COST execution gas.
author: Anders Elowsson (@anderselowsson), Ben Adams (@benaadams), Francesco D'Amato (@fradamt)
discussions-to: https://ethereum-magicians.org/t/eip-blob-base-fee-bounded-by-price-of-blob-carrying-transaction/23271
status: Final
type: Standards Track
category: Core
created: 2025-03-25
requires: 4844, 7840
---

## Abstract

This EIP assigns a reserve price `BLOB_BASE_COST * base_fee_per_gas` to blobs by introducing an `if`-clause in `calc_excess_blob_gas()`. Specifically, when the reserve price is higher than `GAS_PER_BLOB * base_fee_per_blob_gas`, the function will not subtract `target_blob_gas` from `excess_blob_gas`, causing `excess_blob_gas` to increase according to `blob_gas_used`, while keeping the per-block maximum increase unchanged. The proposal ensures that the blob fee market can function properly and that blob consumers pay at least a relevant fraction of the market rate for the compute they request from nodes.

## Motivation

Ethereum uses a dynamic pricing auction to set the blob base fee, lowering the fee if less gas is consumed than `target_blob_gas = GAS_PER_BLOB * blobSchedule.target` and raising the fee if more gas is consumed. Such an auction can function well when the blob base fee represents the price signal, allowing the mechanism to control the real price for blob consumers. However, when execution costs dominate, the price signal is lost. The blob base fee then no longer represents a significant component of the total cost facing the consumer, and the protocol can no longer rely on the blob base fee to control the equilibrium quantity of blobs consumed. 

The current mechanism can therefore end up repeatedly lowering the blob base fee until it eventually settles at 1 wei. A change in the blob base fee of 10% may under such circumstances shift the total cost of utilizing blobspace by just 0.0000001%. Whenever dem