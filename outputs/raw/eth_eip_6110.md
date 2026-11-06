---
eip: 6110
title: Supply validator deposits on chain
description: Provides validator deposits as a list of deposit operations added to the Execution Layer block
author: Mikhail Kalinin (@mkalinin), Danny Ryan (@djrtwo), Peter Davies (@petertdavies)
discussions-to: https://ethereum-magicians.org/t/eip-6110-supply-validator-deposits-on-chain/12072
status: Final
type: Standards Track
category: Core
created: 2022-12-09
requires: 7685
---

## Abstract

Appends validator deposits to the Execution Layer block structure. This shifts responsibility of deposit inclusion and validation to the Execution Layer and removes the need for deposit (or `eth1data`) voting from the Consensus Layer.

Validator deposits list supplied in a block is obtained by parsing deposit contract log events emitted by each deposit transaction included in a given block.

## Motivation

Validator deposits are a core component of the proof-of-stake consensus mechanism. This EIP allows for an in-protocol mechanism of deposit processing on the Consensus Layer and eliminates the proposer voting mechanism utilized currently. This proposed mechanism relaxes safety assumptions and reduces complexity of client software design, contributing to the security of the deposits flow. It also improves validator UX.

Advantages of in-protocol deposit processing consist of, but are not limited to, the following:

* Significant increase of deposits security by supplanting proposer voting. With the proposed in-protocol mechanism, an honest online node can't be convinced to process fake deposits even when more than 2/3 portion of stake is adversarial.
* Decrease of delay between submitting deposit transaction on Execution Layer and its processing on Consensus Layer. That is, ~13 minutes with in-protocol deposit processing compared to ~12 hours with the existing mechanism.
* Eliminate beacon block proposal dependency on JSON-RPC API data polling that suffers from failures caused by inconsistencies between JSON-RPC API implementations and dependency of API calls process