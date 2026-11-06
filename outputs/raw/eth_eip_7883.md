---
eip: 7883
title: ModExp Gas Cost Increase
description: Increases cost of ModExp precompile
author: Marcin Sobczak (@marcindsobczak), Marek Moraczyński (@MarekM25), Marcos Maceo (@stdevMac)
discussions-to: https://ethereum-magicians.org/t/eip-7883-modexp-gas-cost-increase/22841
status: Final
type: Standards Track
category: Core
created: 2025-02-11
requires: 2565
---

## Abstract

This EIP is modifying the `ModExp` precompile pricing algorithm introduced in [EIP-2565](./eip-2565.md).

## Motivation

Currently the `ModExp` precompile is underpriced in certain scenarios relative to its resource consumption. By adjusting the pricing formula, this EIP aims to address these discrepancies, making `ModExp` sufficiently efficient to enable potential increases in the block gas limit.

## Specification

Upon activation of this EIP, the gas cost of calling the precompile at address `0x0000000000000000000000000000000000000005` will be calculated as follows:

```
def calculate_multiplication_complexity(base_length, modulus_length):
    max_length = max(base_length, modulus_length)
    words = math.ceil(max_length / 8)
    multiplication_complexity = 16
    if max_length > 32: multiplication_complexity = 2 * words**2
    return multiplication_complexity

def calculate_iteration_count(exponent_length, exponent):
    iteration_count = 0
    if exponent_length <= 32 and exponent == 0: iteration_count = 0
    elif exponent_length <= 32: iteration_count = exponent.bit_length() - 1
    elif exponent_length > 32: iteration_count = (16 * (exponent_length - 32)) + ((exponent & (2**256 - 1)).bit_length() - 1)
    return max(iteration_count, 1)

def calculate_gas_cost(base_length, modulus_length, exponent_length, exponent):
    multiplication_complexity = calculate_multiplication_complexity(base_length, modulus_length)
    iteration_count = calculate_iteration_count(exponent_length, exponent)
    return max(500, math.floor(multiplication_complexity * iteration_count))
```

The specific changes from the algorithm defined in [EIP-2565](