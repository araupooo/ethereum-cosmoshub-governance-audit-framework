---
eip: 7691
title: Blob throughput increase
description: Increase the number of blobs to reach a new target and max of 6 and 9 blobs per block respectively
author: Parithosh Jayanthi (@parithosh), Toni Wahrstätter (@nerolation), Sam Calder-Mason (@samcm), Andrew Davis (@savid), Ansgar Dietrichs (@adietrichs)
discussions-to: https://ethereum-magicians.org/t/eip-7691-blob-throughput-increase/19694
status: Final
type: Standards Track
category: Core
created: 2024-04-17
---

## Abstract

Increases the number of blobs in a block to provide more scale to Ethereum via L2 solution that rely on L1 data capacity.

## Motivation

Ethereum, with its rollup centric roadmap, scales by relying on L2. Since the Dencun fork, the blob gas target and maximum was set to 3/6 respectively. The blob gas limit was arrived at based on a series of big block tests performed on the Ethereum mainnet network as well as a series of testnets. The values were chosen cautiously, as it's extremely hard to predict the exact p2p behaviour of Ethereum mainnet.

As we now have the Dencun upgrade live, we are able to use monitoring tools to check the network health. Initial monitoring indicates that we have a stable network with the current gas target and the re-org rate is trending downwards. Additionally, analysis on messages in gossipsub indicate that the inclusion of `IDONTWANT` messages could bring us a significant bandwidth savings. This allows us to consider starting a series of big block and blob tests to determine the theoretical headroom we currently have. The EIP specifies a proposed new blob gas target and limit based on the series of tests.

This EIP aims to increase the throughput short term to provide some scaling until future solutions are deployed. In order to alleviate valid concerns about solo-stakers, approaches such as the inclusion of a flag indicating the max blobs per block for locally built blocks could be considered.

## Specification

### Parameters

| Constant                                 | Value               |
|------