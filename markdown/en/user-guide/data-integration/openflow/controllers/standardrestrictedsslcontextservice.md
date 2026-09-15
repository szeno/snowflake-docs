# StandardRestrictedSSLContextService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Restricted implementation of the SSLContextService. Provides the ability to configure keystore and/or truststore properties once and reuse that configuration throughout the application, but only allows a restricted set of TLS/SSL protocols to be chosen (no SSL protocols are supported). The set of protocols selectable will evolve over time as new protocols emerge and older protocols are deprecated. This service is recommended over StandardSSLContextService if a component doesn’t expect to communicate with legacy systems since it is unlikely that legacy systems will support these protocols.

## Tags

certificate, jks, keystore, p12, pkcs, pkcs12, secure, ssl, tls, truststore

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Keystore Filename | Keystore Filename |  |  | The fully-qualified filename of the Keystore |
| Keystore Password | Keystore Password |  |  | The password for the Keystore |
| Keystore Type | Keystore Type |  | - BCFKS - PKCS12 - JKS | The Type of the Keystore |
| TLS Protocol | SSL Protocol | TLS | - TLS - TLSv1.3 - TLSv1.2 | TLS Protocol Version for encrypted connections. Supported versions depend on the specific version of Java used. |
| Truststore Filename | Truststore Filename |  |  | The fully-qualified filename of the Truststore |
| Truststore Password | Truststore Password |  |  | The password for the Truststore |
| Truststore Type | Truststore Type |  | - BCFKS - PKCS12 - JKS | The Type of the Truststore |
| Key Password | key-password |  |  | The password for the key. If this is not specified, but the Keystore Filename, Password, and Type are specified, then the Keystore Password will be assumed to be the same as the Key Password. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
