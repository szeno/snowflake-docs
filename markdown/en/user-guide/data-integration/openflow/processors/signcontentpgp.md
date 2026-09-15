# SignContentPGP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-pgp-nar

## Description

Sign content using OpenPGP Private Keys

## Tags

Encryption, GPG, OpenPGP, PGP, RFC 4880, Signing

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| file-encoding | File Encoding for signing |
| hash-algorithm | Hash Algorithm for signing |
| private-key-id | PGP Private Key Identifier formatted as uppercase hexadecimal string of 16 characters used for signing |
| private-key-service | PGP Private Key Service for generating content signatures |
| signing-strategy | Strategy for writing files to success after signing |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Content signing failed |
| success | Content signing succeeded |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| pgp.compression.algorithm | Compression Algorithm |
| pgp.compression.algorithm.id | Compression Algorithm Identifier |
| pgp.file.encoding | File Encoding |
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
- [org.apache.nifi.processors.pgp.VerifyContentPGP](/user-guide/data-integration/openflow/processors/verifycontentpgp)
