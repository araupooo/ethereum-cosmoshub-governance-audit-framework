---
eip: 7524
title: PLUME Signature in Wallets
description: A new signature scheme for Ethereum keypairs that allows for "nullifiers" to enable unique anonymity and zk voting.
author: Yush G (@Divide-By-0) <aayushg@mit.edu>, Kobi Gurkan (@kobigurk), Richard Liu (@rrrliu), Vivek Bhupatiraju (@vb7401), Barry Whitehat (@barryWhiteHat)
discussions-to: https://ethereum-magicians.org/t/erc-7524-plume-signature-in-wallets/15902
status: Draft
type: Standards Track
category: ERC
created: 2023-09-24
---

## Abstract

ZK-SNARKs have enabled ideation for new identity applications based on anonymous proof-of-ownership. One of the primary technologies that would enable the jump from existing apps to systems that require anonymous uniqueness is the development of verifiably deterministic signatures. Because Ethereum is based on ECDSA, there is no way right now for someone to verify that a signature is generated deterministically, even with ‘deterministic’ ECDSA signatures: a ZK-SNARK proof would need someone’s private key to do so, and some hardware wallets do not even allow viewing of a private key. Broadly, we don’t want to export/copy-paste the private key into a SNARK to be an intended user behavior, and most hardware wallets will not be able to run SNARK arithmetization inside a secure enclave for existing schemes (and nor do we want to standardize an entire proof system inside a wallet right now when they emerge and evolve almost every year). Thus we are left to select a new algorithm that offers us verifiable, deterministic nullifiers that can be SNARKed outside the enclave.

One specific example of how such a signature can lead to unique pseudonymity is that we prove it was generated correctly in a ZK-SNARK that only reveals publicly the hash(signature), and the SNARK additionally proves some property the public key has (i.e. is in some anonymity set, has executed some set of actions on chain, etc). This proof is the only thing that is ever seen by other people, and so the hash(signature) can be used as a “nu