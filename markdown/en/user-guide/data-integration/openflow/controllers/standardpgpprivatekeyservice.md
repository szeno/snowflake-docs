# StandardPGPPrivateKeyService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

PGP Private Key Service provides Private Keys loaded from files or properties

## Tags

Encryption, GPG, Key, OpenPGP, PGP, Private, RFC 4880

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Key Password \* | key-password |  |  | Password used for decrypting Private Keys |
| Keyring | keyring |  |  | PGP Keyring or Secret Key encoded in ASCII Armor |
| Keyring File | keyring-file |  |  | File path to PGP Keyring or Secret Key encoded in binary or ASCII Armor |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
