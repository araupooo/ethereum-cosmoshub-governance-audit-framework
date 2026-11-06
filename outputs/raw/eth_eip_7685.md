---
eip: 7685
title: General purpose execution layer requests
description: A general purpose bus for sharing EL triggered requests with the CL
author: lightclient (@lightclient), Felix Lange (@fjl)
discussions-to: https://ethereum-magicians.org/t/eip-7685-general-purpose-execution-layer-requests/19668
status: Final
type: Standards Track
category: Core
created: 2024-04-14
---

## Abstract

This proposal defines a general purpose framework for storing contract-triggered
requests. It extends the execution header with a single field to store the
request information. Requests are later on exposed to the consensus layer, which
then processes each one.

## Motivation

The proliferation of smart contract controlled validators has caused there to be
a demand for additional EL triggered behaviors. By allowing these systems to
delegate administrative operations to their governing smart contracts, they can
avoid intermediaries needing to step in and ensure certain operations occur.
This creates a safer system for end users. By abstracting each individual request
details from the EL, adding new request types is simpler and does not require an
update on the execution block structure.

## Specification

### Execution Layer

#### Requests

A `requests` object consists of a `request_type` byte prepended to an opaque byte array
`request_data`. The `request_data` contains zero or more encoded request objects.

```
requests = request_type ++ request_data
```

Each request type will define its own `requests` object with its own `request_data` format.

#### Block Header

Extend the header with a new 32 byte commitment value `requests_hash`.

While processing a block, multiple `requests` objects with different `request_type`s will
be produced by the system, and accumulated in the block requests list.

In order to compute the commitment, an intermediate hash list is first built by hashing
all non-empty requests elements of the block requests list. Items with empty
`request_data` are excluded, i.e. the intermediate list skips `requests` 