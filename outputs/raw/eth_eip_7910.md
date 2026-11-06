---
eip: 7910
title: eth_config JSON-RPC Method
description: A JSON-RPC method that describes the configuration of the current and next fork
author: Danno Ferrin (@shemnon)
discussions-to: https://ethereum-magicians.org/t/eth-config-json-rpc-method/23183
status: Final
type: Standards Track
category: Interface
created: 2025-03-18
---

## Abstract

This document describes an RPC method that provides node-relevant configuration data for the current, next, and last known forks.

## Motivation

Throughout Ethereum's history, there have been multiple instances where a client was not correctly configured for an upcoming hard fork, causing it to fall out of consensus when the fork boundary was crossed. Most incidents have been minor, such as a single client forking the chain in proof-of-work or having its blocks orphaned in proof-of-stake.

The most significant occurrence was during the Pectra activation on the Holešky testnet. Four out of six clients on the network had an incorrect configuration for the deposits contract. Instead of being orphaned, the incorrect chain was justified, and the side effects persist on Holešky even after reaching finality.

By providing an RPC method that allows clients to report key configuration variables before the next hard fork, operations teams can gain greater confidence that clients are correctly configured and prepared for upcoming forks.

### Target Audience and Use Cases

This method is intended for node operators, validator teams, and network monitoring tools to verify client readiness for upcoming forks. Use cases include:

- Automated pre-fork validation scripts comparing `eth_config` outputs across nodes.
- Manual checks by validator operators to ensure alignment with fork specifications.
- Debugging by client developers to identify configuration mismatches.
- Automated checks by Consensus Layer counterparties.

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL"