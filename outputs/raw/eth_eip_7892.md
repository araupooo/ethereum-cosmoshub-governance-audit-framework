---
eip: 7892
title: Blob Parameter Only Hardforks
description: Defines a mechanism for scaling Ethereum’s blob capacity via specialized hard forks that modify only blob-related parameters.
author: Mark Mackey (@ethDreamer), Raúl Kripalani (@raulk)
discussions-to: https://ethereum-magicians.org/t/eip-7892-blob-parameter-only-hardforks/23018
status: Final
type: Informational
created: 2025-02-28
requires: 7840
---

## Abstract

This EIP introduces **Blob Parameter Only (BPO) Hardforks**, a lightweight mechanism for incrementally scaling Ethereum’s blob capacity through targeted hard forks that modify only blob-related parameters: `target`, `max`, and `baseFeeUpdateFraction`. Unlike traditional hard forks, which require extensive coordination and introduce broader protocol changes, BPO forks enable rapid, low-overhead scaling of blob capacity in response to **real-world demand and network conditions**.

## Motivation

Ethereum's scaling strategy relies on Layer 2 (L2) solutions for transaction execution while using Ethereum as a **data availability (DA) layer**. However, the demand for DA has increased rapidly, and the current approach of only modifying blob parameters in large, infrequent hard forks is **not agile enough** to keep up with L2 growth. 

The key motivations for BPO forks are as follows:

1. **Continuous Scaling**  
   - L2 DA demand is growing rapidly, leading to ongoing saturation of blob capacity.
   - Large, infrequent blob parameter changes create high costs and inefficiencies.
   - BPO forks allow for more frequent, safer capacity increases.

2. **Reduced Operational Overhead**  
   - Performance improvements and further testing will continue to unlock additional capacity.
   - It is desirable to reduce the time between core devs agreeing on a parameter increase and its effective deployment.
   - Full Ethereum hard forks require significant coordination, testing, and upgrade efforts across clients.
   - By isolating blob parameter changes, BPO forks reduce the complexity of upgrades.

3. **E