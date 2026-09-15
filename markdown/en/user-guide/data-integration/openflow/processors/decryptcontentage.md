# DecryptContentAge 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-cipher-nar

## Description

Decrypt content using the age-encryption.org/v1 specification. Detects binary or ASCII armored content encoding using the initial file header bytes. The age standard uses ChaCha20-Poly1305 for authenticated encryption of the payload. The age-keygen command supports generating X25519 key pairs for encryption and decryption operations.

## Tags

ChaCha20-Poly1305, X25519, age, age-encryption.org, encryption

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Private Key Identities | One or more X25519 Private Key Identities, separated with newlines, encoded according to the age specification, starting with AGE-SECRET-KEY-1 |
| Private Key Identity Resources | One or more files or URLs containing X25519 Private Key Identities, separated with newlines, encoded according to the age specification, starting with AGE-SECRET-KEY-1 |
| Private Key Source | Source of information determines the loading strategy for X25519 Private Key Identities |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Decryption Failed |
| success | Decryption Completed |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.cipher.EncryptContentAge](/user-guide/data-integration/openflow/processors/encryptcontentage)
