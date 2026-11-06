---
eip: 8444
title: Agentic Resource Discovery (ARD) Onchain
description: Address-rooted onchain value registry whose records are conformant ARD entries anchored to skill, tender and agent identity contracts
author: Gary Yang (@garyyang-finchip)
discussions-to: https://ethereum-magicians.org/t/erc-8444-agentic-resource-discovery-ard-onchain/29963
status: Draft
type: Standards Track
category: ERC
created: 2026-10-12
requires: 165, 712, 1271
---

## Abstract

This ERC defines an onchain registry of *value records* for agentic resources. A value record binds an ARD entry, as defined by the Agentic Resource Discovery (ARD) specification maintained by the ards-project working group, to an onchain *anchor* — a token-bound executable skill, a token-bound task tender, an address-anchored agent identity, or an ARD registry endpoint — and, through a *kind adapter*, to the address that controls that anchor. Every record is a valid ARD entry, and every resolver that serves records is a conformant ARD registry, so agents and agent users outside Web3 discover and consume onchain value through ordinary ARD search. Authority over a record belongs to an address, never to a domain; a domain is an endorsement that an address collects by claiming it onchain and being acknowledged in the domain's own ARD manifest. Records are identified by their anchor; ARD URNs are aliases.

## Motivation

ARD answers *what exists and who says so*. A publisher lists its MCP servers, A2A agents, skills and APIs in a manifest under its own domain; registries crawl, index and federate those manifests; a client asks in natural language and receives entries together with the publisher's identity. ARD deliberately defines nothing beyond discovery: no price, no payment, no settlement, no escrow, no credit. It has no demand side — only resources that are offered, never work that is wanted — and it roots trust in domain ownership.

An agent economy needs the complementary half: *what a resource is worth, who stands behind it, and how it settles*. Th