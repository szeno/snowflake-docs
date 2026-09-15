# StandardPrivateKeyService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Private Key Service provides access to a Private Key loaded from configured sources

## Tags

PEM, PKCS8

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Key | key |  |  | Private Key structured using PKCS8 and encoded as PEM |
| Key File | key-file |  |  | File path to Private Key structured using PKCS8 and encoded as PEM |
| Key Password | key-password |  |  | Password used for decrypting Private Keys |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
