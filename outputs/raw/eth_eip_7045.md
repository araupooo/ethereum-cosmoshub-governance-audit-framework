---
eip: 7045
title: Increase max attestation inclusion slot
description: Increases max attestation inclusion slot to the last slot in `N+1` where `N` is the epoch containing the attestation's slot.
author: Danny Ryan (@djrtwo)
discussions-to: https://ethereum-magicians.org/t/eip-7045-increase-attestation-slot-inclusion-range/14342
status: Final
type: Standards Track
category: Core
created: 2023-05-18
---

## Abstract

Increases max attestation inclusion slot from `attestation.slot + SLOTS_PER_EPOCH` to the last slot of epoch `N+1` where `N` is the epoch containing the attestation slot.

This increase is critical to the current LMD-GHOST security analysis as well as the confirmation rule.

## Motivation

Attestations can currently be included after some minimum delay (`1` slot on mainnet) up until `SLOTS_PER_EPOCH` slots after the slot the attestation was created in. This rolling window of one epoch was decided upon during Phase 0 because the equal inclusion window for any attestation was assessed as "fair". The alternative considered path was to allow inclusion during the current and next epoch which means attestations created during the start of an epoch have more potential slots of inclusion than those at the end of the epoch.

Since this decision, it has become apparent that the alternative design is critical for current LMD-GHOST security proofs as well as a new confirmation rule (which will allow for block confirmations in approximately 3-4 slots in normal mainnet conditions).

This specification thus increases the max inclusion slot for attestations in accordance with the learned security proof and confirmation rule needs.

## Specification

### Constants

| Name | Value | Comment |
| - | - | - |
|`FORK_TIMESTAMP` | `1710338135` | Mainnet |

### Execution layer

This requires no changes to the Execution Layer.

### Consensus layer

Specification changes are built into the Consensus Specs Deneb upgrade.

The specification makes two minor changes to the state transition function:

* Modify [`process_attestat