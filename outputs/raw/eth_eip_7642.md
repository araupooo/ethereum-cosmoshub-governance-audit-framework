---
eip: 7642
title: eth/69 - history expiry and simpler receipts
description: Adds history serving window and removes bloom filter in receipt
author: Marius van der Wijden (@MariusVanDerWijden), Felix Lange <fjl@ethereum.org>, Ahmad Bitar (@smartprogrammer93) <smartprogrammer@windowslive.com>
discussions-to: https://ethereum-magicians.org/t/eth-70-drop-pre-merge-fields-from-eth-protocol/19005
status: Final
type: Standards Track
category: Networking
created: 2024-02-29
requires: 5793
---

## Abstract

This EIP modifies the 'eth' p2p protocol to announce the historical block range served by
the node. We also simplify the handshake to remove total difficulty information, which
isn't used anymore after the merge. Additionally we propose to remove the `Bloom` field
from receipts transferred over the protocol.

## Motivation

### Block range in Status message

In the history expiry working group, it was decided that clients may drop pre-merge
history from their storage after May 1, 2025. For clients that want to sync history
through the 'eth' protocol, it is essential to know whether a peer still serves old
history. A similar idea was proposed in [EIP-7542](./eip-7542.md) but was later withdrawn
because a political decision on history expiry had not been reached at the time.

### Removing Bloom in Receipts

We recently discovered that none of the clients store the `Bloom` field of the receipts as
it can be recomputed on demand. However the networking spec requires the `Bloom` field to
be sent over the network. Thus a syncing node will ask for the Bloom filters for all
receipts. The serving node will regenerate roughly 530GB of bloom filters (2.3B txs * 256
byte). These 530GBs are send over the network to the syncing peer, the syncing peer will
verify them and not store them either. This adds an additional 530GB of unnecessary
bandwidth to every sync.

### BlockRangeUpdate message

We want clients to be aware of the available block range in their peers. The new
notification message can be used to detect sync status of 