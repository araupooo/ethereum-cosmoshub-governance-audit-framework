---
eip: 6780
title: SELFDESTRUCT only in same transaction
description: SELFDESTRUCT will recover all funds to the target but not delete the account, except when called in the same transaction as creation
author: Guillaume Ballet (@gballet), Vitalik Buterin (@vbuterin), Dankrad Feist (@dankrad)
discussions-to: https://ethereum-magicians.org/t/deactivate-selfdestruct-except-where-it-occurs-in-the-same-transaction-in-which-a-contract-was-created/13539
status: Final
type: Standards Track
category: Core
created: 2023-03-25
requires: 2681, 2929, 3529
---

## Abstract

This EIP changes the functionality of the `SELFDESTRUCT` opcode. The new functionality will be only to send all Ether in the account to the target, except that the current behaviour is preserved when `SELFDESTRUCT` is called in the same transaction a contract was created.

## Motivation

The `SELFDESTRUCT` opcode requires large changes to the state of an account, in particular removing all code and storage. This will not be possible in the future with Verkle trees: Each account will be stored in many different account keys, which will not be obviously connected to the root account.

This EIP implements this change. Applications that only use `SELFDESTRUCT` to retrieve funds will still work. Applications that only use `SELFDESTRUCT` in the same transaction as they created a contract will also continue to work without any changes.

## Specification

The behaviour of `SELFDESTRUCT` is changed in the following way:

1. When `SELFDESTRUCT` is executed in a transaction that is not the same as the contract calling `SELFDESTRUCT` was created:

   - The current execution frame halts.
   - `SELFDESTRUCT` does not delete any data (including storage keys, code, or the account itself).
   - `SELFDESTRUCT` transfers the entire account balance to the target.
   - Note that if the target is the same as the contract calling `SELFDESTRUCT` there is no net change in balances.  Unlike the prior specification, Ether will not be burnt in this case.
   - Note that no refund is