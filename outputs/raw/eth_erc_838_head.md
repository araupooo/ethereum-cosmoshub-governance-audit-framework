---
eip: 838
title: ABI specification for REVERT reason string
description: A proposal to extend the ABI specification to include typed errors in the REVERT reason string.
author: Federico Bond (@federicobond), Renan Rodrigues de Souza (@RenanSouza2)
discussions-to: https://ethereum-magicians.org/t/eip-838-what-is-the-current-status/14671
status: Draft
type: Standards Track
category: ERC
created: 2020-08-20
---

## Abstract

This proposal specifies how to encode potential error conditions in the JSON ABI of a smart contract. A high-level language could then provide a syntax for declaring and throwing these errors. The compiler will encode these errors in the reason parameter of the REVERT opcode in a way that can be easily reconstructed by libraries such as web3.


## Motivation

It's important to provide clear feedback to users (and developers) about what went wrong with their Ethereum transactions. The REVERT opcode is a step in the right direction, as it allows smart contract developers to encode a message describing the failure in the reason parameter. There is an implementation under review in Solidity that accepts a string, thus providing a low-level interface to this parameter. However, standardizing a method for passing errors from this parameter back to clients will bring many benefits to both users and developers.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

## Specification

To conform to this specification, compilers producing JSON ABIs SHOULD include error declarations alongside functions and events. Each error object MUST contain the keys name (string) and arguments (same types as the function’s inputs list). The value of type MUST be "error".

Example:

```
{ "type": "error", "name": "InsufficientBalance", "arguments": [ { "name": "amount", "type": "uint256" } ] }
```

A selector for this error can be computed from its signature (InsufficientBalanc