---
eip: 2718
title: Typed Transaction Envelope
description: Defines a new transaction type that is an envelope for future transaction types.
author: Micah Zoltu (@MicahZoltu)
discussions-to: https://ethereum-magicians.org/t/eip-2718-typed-transaction-envelope/4355
status: Final
type: Standards Track
category: Core
created: 2020-06-13
---

## Abstract
`TransactionType || TransactionPayload` is a valid transaction and `TransactionType || ReceiptPayload` is a valid transaction receipt where `TransactionType` identifies the format of the transaction and `*Payload` is the transaction/receipt contents, which are defined in future EIPs.

## Motivation
In the past, when we have wanted to add new transaction types we have had to ensure they were backward compatible with all other transactions, meaning that you could differentiate them based only on the encoded payload, and it was not possible to have a transaction that matched both types.
This was seen in [EIP-155](./eip-155.md) where the new value was bit-packed into one of the encoded fields.
There are multiple proposals in discussion that define new transaction types such as one that allows EOA accounts to execute code directly within their context, one that enables someone besides `msg.sender` to pay for gas, and proposals related to layer 1 multi-sig transactions.
These all need to be defined in a way that is mutually compatible, which quickly becomes burdensome to EIP authors and to clients who now have to follow complex rules for differentiating transaction type.

By introducing an envelope transaction type, we only need to ensure backward compatibility with existing transactions and from then on we just need to solve the much simpler problem of ensuring there is no numbering conflict between `TransactionType`s.

## Specification
### Definitions
* `||` is the byte/byte-array concatenation operator.

### Transactions
As of `FORK_BLOCK_NUMBER`, the transaction root in the block header **MUST** be the root hash of `patriciaTrie(rlp(Index) => Transaction)` where:
* `I