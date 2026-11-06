---
eip: 7514
title: Add Max Epoch Churn Limit
description: Modify the churn limit function to upper bound it to a max value
author: dapplion (@dapplion), Tim Beiko (@timbeiko)
discussions-to: https://ethereum-magicians.org/t/eip-7514-add-max-epoch-churn-limit/15709
status: Final
type: Standards Track
category: Core
created: 2023-09-07
---

## Abstract

Update the maximum validator growth rate from an exponential to a linear increase by capping the epoch churn limit.

## Motivation

This proposal aims to mitigate the negative externalities of very high level of total ETH supply staked before a proper solution is implemented. In other words, this proposal accepts the complexities of changing the rewards curve and is meant only to slow down growth. 

In the event that the deposit queue stays 100% full, the share of ETH supply staked will reach 50% by May 2024, 75% by September 2024, and 100% by December 2024. While rewards decrease as the validator set size increases, at 100% of ETH supply staked, yearly consensus rewards alone (excluding MEV/transaction fees) for validators still represent ~1.6% of their stake. This small yield does not necessarily dissuade additional capital staking due to the often much higher and unpredictable yields from MEV. As such, the equilibrium point of the validator set size can be close to its maximum possible. Liquid staking tokens (LSTs) also contribute to this, given stakers can use them as they use unstaked ETH. 

As the levels of ETH staked increase, more strain is put on the consensus layer. A larger number of validators leads to an increase in gossip messages, as well as a growing Beacon state size. Additionally, as the amount of stake grows, it's unclear how much marginal security benefits come from additional economic weight. 

The Beacon Chain validator reward function was chosen before its launch in 2020. PoS research and reward curve design were performed in a pre-MEV world. Much has changed since then, including the Beacon chain achieving unprecedented success, beyond the 