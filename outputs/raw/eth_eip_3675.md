---
eip: 3675
title: Upgrade consensus to Proof-of-Stake
description: Specification of the consensus mechanism upgrade on Ethereum Mainnet that introduces Proof-of-Stake
author: Mikhail Kalinin (@mkalinin), Danny Ryan (@djrtwo), Vitalik Buterin (@vbuterin)
discussions-to: https://ethereum-magicians.org/t/eip-3675-upgrade-consensus-to-proof-of-stake/6706
status: Final
type: Standards Track
category: Core
created: 2021-07-22
requires: 2124
---


## Abstract

This EIP deprecates Proof-of-Work (PoW) and supersedes it with the new Proof-of-Stake consensus mechanism (PoS) driven by the beacon chain. Information on the bootstrapping of the new consensus mechanism is documented in [EIP-2982](./eip-2982.md). Full specification of the beacon chain can be found in the `ethereum/consensus-specs` repository.

This document specifies the set of changes to the block structure, block processing, fork choice rule and network interface introduced by the consensus upgrade.


## Motivation

The beacon chain network has been up and running since December 2020. Neither safety nor liveness failures were detected during this period of time. This long period of running without failure demonstrates the sustainability of the beacon chain system and its readiness to become a security provider for the Ethereum Mainnet.

To understand the motivation of introducing the Proof-of-Stake consensus see the Motivation section of [EIP-2982](./eip-2982.md#motivation).


## Specification

### Definitions

* **PoW block**: Block that is built and verified by the existing proof-of-work mechanism. In other words, a block of the Ethereum network before the consensus upgrade.
* **PoS block**: Block that is built and verified by the new proof-of-stake mechanism.
* **Terminal PoW block**: A PoW block that satisfies the following conditions --
`pow_block.total_difficulty >= TERMINAL_TOTAL_DIFFICULTY` *and* `pow_block.parent_block.total_difficulty < TERMINAL_TOTAL_DIFFICULTY`.
There can be more than one terminal PoW block in the network, e.g. multiple children 