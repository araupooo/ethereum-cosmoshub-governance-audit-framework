---
eip: 4844
title: Shard Blob Transactions
description: Shard Blob Transactions scale data-availability of Ethereum in a simple, forwards-compatible manner.
author: Vitalik Buterin (@vbuterin), Dankrad Feist (@dankrad), Diederik Loerakker (@protolambda), George Kadianakis (@asn-d6), Matt Garnett (@lightclient), Mofi Taiwo (@Inphi), Ansgar Dietrichs (@adietrichs)
discussions-to: https://ethereum-magicians.org/t/eip-4844-shard-blob-transactions/8430
status: Final
type: Standards Track
category: Core
created: 2022-02-25
requires: 1559, 2718, 2930, 4895
---

## Abstract

Introduce a new transaction format for "blob-carrying transactions" which contain a large amount of data that cannot be
accessed by EVM execution, but whose commitment can be accessed.
The format is intended to be fully compatible with the format that will be used in full sharding.

## Motivation

Rollups are in the short and medium term, and possibly in the long term, the only trustless scaling solution for Ethereum.
Transaction fees on L1 have been very high for months and there is greater urgency in doing anything required to help facilitate an ecosystem-wide move to rollups.
Rollups are significantly reducing fees for many Ethereum users: Optimism and Arbitrum frequently provide fees that are ~3-8x lower than the Ethereum base layer itself,
and ZK rollups, which have better data compression and can avoid including signatures, have fees ~40-100x lower than the base layer.

However, even these fees are too expensive for many users. The long-term solution to the long-term inadequacy of rollups
by themselves has always been data sharding, which would add ~16 MB per block of dedicated data space to the chain that rollups could use.
However, data sharding will still take a considerable amount of time to finish implementing and deploying.

This EIP provides a stop-gap solution until that point by implementing the _transaction format_ that would be used in sharding,
but not actually sharding those transactions. Instead, the data from this transaction f