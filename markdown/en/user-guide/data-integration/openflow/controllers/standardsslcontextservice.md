# StandardSSLContextService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Standard implementation of the SSLContextService. Provides the ability to configure keystore and/or truststore properties once and reuse that configuration throughout the application. This service can be used to communicate with both legacy and modern systems. If you only need to communicate with non-legacy systems, then the StandardRestrictedSSLContextService is recommended as it only allows a specific set of SSL protocols to be chosen.

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
| TLS Protocol | SSL Protocol | TLS | - SSL - TLS - TLSv1.3 - TLSv1.2 - TLSv1.1 - TLSv1 | SSL or TLS Protocol Version for encrypted connections. Supported versions include insecure legacy options and depend on the specific version of Java used. |
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
