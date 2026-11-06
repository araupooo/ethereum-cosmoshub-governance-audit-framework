---
eip: 7702
title: Set Code for EOAs
description: Add a new tx type that permanently sets the code for an EOA
author: Vitalik Buterin (@vbuterin), Sam Wilson (@SamWilsn), Ansgar Dietrichs (@adietrichs), lightclient (@lightclient)
discussions-to: https://ethereum-magicians.org/t/eip-set-eoa-account-code-for-one-transaction/19923
status: Final
type: Standards Track
category: Core
created: 2024-05-07
requires: 2, 161, 1052, 2718, 2929, 2930, 3541, 3607, 4844
---

## Abstract

Add a new [EIP-2718](./eip-2718.md) transaction type that allows Externally
Owned Accounts (EOAs) to set the code in their account. This is done by
attaching a list of authorization tuples -- individually formatted as `[chain_id,
address, nonce, y_parity, r, s]` -- to the transaction. For each tuple, a
delegation indicator `(0xef0100 || address)` is written to the authorizing
account's code. All code executing operations must load and execute the code
pointed to by the delegation.

## Motivation

Despite great advances in the smart contract wallet ecosystem, EOAs have held
back broad adoption of UX improvements across applications. This EIP therefore
focuses on adding short-term functionality improvements to EOAs which will allow
UX improvements to permeate through the entire application stack. Three
particular features this EIP is designed around are:

* **Batching**: allowing multiple operations from the same user in one atomic
transaction. One common example is an [ERC-20](./eip-20.md) approval followed by
spending that approval. This is a common workflow in DEXes that requires two
transactions today. Advanced use cases of batching occasionally involve
dependencies: the output of the first operation is part of the input to the
second operation.
* **Sponsorship**: account X pays for a transaction on behalf of account Y.
Account X could be paid in some other ERC-20 for this service, or it could be an
application operator including the transactions of its users for free.
* **Privilege de-escalation**: users can sign sub-keys and give them spe