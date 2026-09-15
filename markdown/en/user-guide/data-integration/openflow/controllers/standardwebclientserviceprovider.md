# StandardWebClientServiceProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Web Client Service Provider with support for configuring standard HTTP connection properties

## Tags

Client, HTTP, Web

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Connect Timeout \* | Connect Timeout | 10 secs |  | Maximum amount of time to wait before failing during initial socket connection |
| HTTP Protocol Version \* | HTTP Protocol Version | HTTP\_2 | - HTTP\_1\_1 - HTTP\_2 | Preferred HTTP protocol version for requests |
| Read Timeout \* | Read Timeout | 10 secs |  | Maximum amount of time to wait before failing while reading socket responses |
| Redirect Handling Strategy \* | Redirect Handling Strategy | FOLLOWED | - FOLLOWED - IGNORED | Handling strategy for responding to HTTP 301 or 302 redirects received with a Location header |
| SSL Context Service | SSL Context Service |  |  | SSL Context Service overrides system default TLS settings for HTTPS communication |
| Write Timeout \* | Write Timeout | 10 secs |  | Maximum amount of time to wait before failing while writing socket requests |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
