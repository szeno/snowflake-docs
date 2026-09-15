# PEMEncodedSSLContextProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

SSLContext Provider configurable using PEM Private Key and Certificate files. Supports PKCS1 and PKCS8 encoding for Private Keys as well as X.509 encoding for Certificates.

## Tags

Certificate, ECDSA, Ed25519, Key, PEM, PKCS1, PKCS8, RSA, SSL, TLS, X.509

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Certificate Authorities \* | Certificate Authorities |  |  | PEM X.509 Certificate Authorities trusted for verifying peers in TLS communications containing one or more standard certificates |
| Certificate Authorities Source \* | Certificate Authorities Source | PROPERTIES | - Properties - System | Source of information for loading trusted Certificate Authorities |
| Certificate Chain \* | Certificate Chain |  |  | PEM X.509 Certificate Chain associated with Private Key starting with standard BEGIN CERTIFICATE header |
| Certificate Chain Location \* | Certificate Chain Location |  |  | PEM X.509 Certificate Chain file location associated with Private Key starting with standard BEGIN CERTIFICATE header |
| Private Key \* | Private Key |  |  | PEM Private Key encoded using either PKCS1 or PKCS8. Supported algorithms include ECDSA, Ed25519, and RSA |
| Private Key Location \* | Private Key Location |  |  | PEM Private Key file location encoded using either PKCS1 or PKCS8. Supported algorithms include ECDSA, Ed25519, and RSA |
| Private Key Source \* | Private Key Source | PROPERTIES | - Undefined - Properties - Files | Source of information for loading Private Key and Certificate Chain |
| TLS Protocol \* | TLS Protocol | TLS | - TLS - TLSv1.3 - TLSv1.2 | TLS protocol version required for negotiating encrypted communications. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
