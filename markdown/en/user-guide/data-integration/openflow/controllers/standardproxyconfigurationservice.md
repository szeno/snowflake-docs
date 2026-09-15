# StandardProxyConfigurationService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a set of configurations for different NiFi components to use a proxy server.

## Tags

Proxy

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Proxy Server Host | proxy-server-host |  |  | Proxy server hostname or ip-address. |
| Proxy Server Port | proxy-server-port |  |  | Proxy server port number. |
| Proxy Type \* | proxy-type | DIRECT | - DIRECT - HTTP - SOCKS | Proxy type. |
| Proxy User Name | proxy-user-name |  |  | The name of the proxy client for user authentication. |
| Proxy User Password | proxy-user-password |  |  | The password of the proxy client for user authentication. |
| SOCKS Version \* | socks-version | SOCKS5 | - SOCKS4 - SOCKS5 | SOCKS Protocol Version |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
