---
eip: 7623
title: Increase calldata cost
description: Increase calldata cost to reduce maximum block size
author: Toni Wahrstätter (@nerolation), Vitalik Buterin (@vbuterin)
discussions-to: https://ethereum-magicians.org/t/eip-7623-increase-calldata-cost/18647
status: Final
type: Standards Track
category: Core
created: 2024-02-13
---

## Abstract

The current calldata pricing permits EL payloads of up to 7.15 MB, while the average size is much smaller at around 100 KB.
This EIP proposes adjusting the calldata cost to reduce the maximum possible block size and its variance without negatively impacting regular users.
This is achieved by increasing calldata costs for transactions that predominantly post data.

## Motivation

The block gas limit has not been increased since [EIP-1559](./eip-1559.md), while the average size of blocks has continuously increased due to the growing number of rollups posting data to Ethereum. Moreover, calldata costs have remained unchanged since [EIP-2028](./eip-2028).
[EIP-4844](./eip-4844.md) introduces blobs as a preferred method for data availability (DA).
This transition demands a reevaluation of calldata pricing, especially in order to address the disparity between average and maximum block sizes.
By introducing a floor cost dependent on the ratio of gas spent on EVM operations to calldata, this proposal aims to reduce the maximum block size to make room for additional blobs or potential block gas limit increases.

## Specification

| Parameter                    | Value |
| ---------------------------- | ----- |
| `STANDARD_TOKEN_COST`        | `4`   |
| `TOTAL_COST_FLOOR_PER_TOKEN` | `10`  |

Let `tokens_in_calldata = zero_bytes_in_calldata + nonzero_bytes_in_calldata * 4`.

Let `isContractCreation` be a boolean indicating the respective event.

Let `execution_gas_used` be the gas used for EVM execution with the gas refund subtracted.

Let `INITCODE_WORD_COST` be 2 as defined in [EIP-3860](./eip-3860.md).

The current formula for determining the total gas used per transaction