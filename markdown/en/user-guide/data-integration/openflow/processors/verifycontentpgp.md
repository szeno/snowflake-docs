# VerifyContentPGP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-pgp-nar

## Description

Verify signatures using OpenPGP Public Keys

## Tags

Encryption, GPG, OpenPGP, PGP, RFC 4880, Signing

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| public-key-service | PGP Public Key Service for verifying signatures with Public Key Encryption |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Signature Verification Failed |
| success | Signature Verification Succeeded |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| pgp.literal.data.filename | Filename from Literal Data |
| pgp.literal.data.modified | Modified Date Time from Literal Data in milliseconds |
| pgp.signature.created | Signature Creation Time in milliseconds |
| pgp.signature.algorithm | Signature Algorithm including key and hash algorithm names |
| pgp.signature.hash.algorithm.id | Signature Hash Algorithm Identifier |
| pgp.signature.key.algorithm.id | Signature Key Algorithm Identifier |
| pgp.signature.key.id | Signature Public Key Identifier |
| pgp.signature.type.id | Signature Type Identifier |
| pgp.signature.version | Signature Version Number |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.pgp.DecryptContentPGP](/user-guide/data-integration/openflow/processors/decryptcontentpgp)
- [org.apache.nifi.processors.pgp.EncryptContentPGP](/user-guide/data-integration/openflow/processors/encryptcontentpgp)
- [org.apache.nifi.processors.pgp.SignContentPGP](/user-guide/data-integration/openflow/processors/signcontentpgp)
