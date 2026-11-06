---
eip: 7002
title: Execution layer triggerable withdrawals
description: Allow validators to trigger exits and partial withdrawals via their execution layer (0x01) withdrawal credentials
author: Danny Ryan (@djrtwo), Mikhail Kalinin (@mkalinin), Ansgar Dietrichs (@adietrichs), Hsiao-Wei Wang (@hwwhww), lightclient (@lightclient), Felix Lange (@fjl)
discussions-to: https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195
status: Final
type: Standards Track
category: Core
created: 2023-05-09
requires: 7685
---

## Abstract

Adds a new mechanism to allow validators to trigger withdrawals and exits from their execution layer (0x01) withdrawal credentials.

These new execution layer exit messages are appended to the execution layer block and then processed by the consensus layer.

## Motivation

Validators have two keys -- an active key and a withdrawal credential. The active key takes the form of a BLS key, whereas the withdrawal credential can either be a BLS key (0x00) or an execution layer address (0x01). The active key is "hot", actively signing and performing validator duties, whereas the withdrawal credential can remain "cold", only performing limited operations in relation to withdrawing and ownership of the staked ETH. Due to this security relationship, the withdrawal credential ultimately is the key that owns the staked ETH and any rewards.

As currently specified, only the active key can initiate a validator exit. This means that in any non-standard custody relationship (i.e., the active key is a separate entity from the withdrawal credentials), the ultimate owner of the funds -- the possessor of the withdrawal credentials -- cannot independently choose to exit and begin the withdrawal process. This leads to either trust issues (e.g. ETH can be "held hostage" by the active key owner) or insufficient work-arounds such as pre-signed exits. Additionally, in the event that active keys are lost, a user should still be able to recover their funds by using their cold withdrawal credential