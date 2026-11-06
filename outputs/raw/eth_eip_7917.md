---
eip: 7917
title: Deterministic proposer lookahead
description: Pre-calculate and store a deterministic proposer lookahead in the beacon state at the start of every epoch
author: Lin Oshitani (@linoscope) <lin@nethermind.io>, Justin Drake (@JustinDrake) <justin@ethereum.org>
discussions-to: https://ethereum-magicians.org/t/eip-7917-deterministic-proposer-lookahead/23259
status: Final
type: Standards Track
category: Core
created: 2025-03-24
---

## Abstract

At the start of each epoch, pre-calculate and store in the `beacon_state` a deterministic `proposer_lookahead` for the next `MIN_SEED_LOOKAHEAD + 1` epochs.

## Motivation

Unlike RANDAO seeds, which have a deterministic lookahead of at least `MIN_SEED_LOOKAHEAD == 1` epochs, the beacon proposer schedule of epoch `N + 1` is not fully predictable from the beacon state during epoch `N`. The reason is that, under certain edge cases, the effective balances (EBs) of active validators—themselves used as input for proposer election in epoch `N + 1`—can change within epoch `N`.

Based preconfirmation protocols rely on a deterministic proposer schedule for smooth operations. Since the beacon genesis, slashings and penalties that accumulate to at least 1 ETH can change EBs of active validators and lead to an unpredictable proposer schedule despite the RANDAO seed being known ahead of time. The increase of MaxEB with [EIP-7251](./eip-7251) increases effective balance unpredictability because rewards that accumulate to at least 1 ETH, validator consolidations, and deposits can grow EBs of active validators beyond 32 ETH.

Besides fixing next-epoch proposer schedule non-determinism, this EIP makes it possible for the proposer schedule of the next epoch to be accessible to the application layer via the beacon root and a simple Merkle proof. This highly simplifies the implementation of on-chain components for based preconfirmation protocols.

Introducing a fully deterministic lookahead fixes a long-standing beacon chain design oversight, as highlighted by Danny Ryan