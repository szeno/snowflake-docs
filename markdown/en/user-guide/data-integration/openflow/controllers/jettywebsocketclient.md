# JettyWebSocketClient

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Implementation of WebSocketClientService. This service uses Jetty WebSocket client module to provide WebSocket session management throughout the application.

## Tags

Jetty, WebSocket, client

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Authentication Header Charset \* | Authentication Header Charset | US-ASCII |  | The charset for Basic Authentication header base64 string. |
| Connection Attempt Count \* | Connection Attempt Count | 3 |  | The number of times to try and establish a connection. |
| Connection Timeout \* | Connection Timeout | 3 sec |  | The timeout to connect the WebSocket URI. |
| Custom Authorization | Custom Authorization |  |  | Configures a custom HTTP Authorization Header as described in RFC 7235 Section 4.2. Setting a custom Authorization Header excludes configuring the User Name and User Password properties for Basic Authentication. |
| HTTP Proxy Host | HTTP Proxy Host |  |  | The host name of the HTTP Proxy. |
| HTTP Proxy Port | HTTP Proxy Port |  |  | The port number of the HTTP Proxy. |
| Idle Timeout \* | Idle Timeout | 0 sec |  | The maximum amount of time that a WebSocket connection may remain idle before it is closed. A value of 0 sec disables the timeout. |
| Input Buffer Size \* | Input Buffer Size | 4 kb |  | The size of the input (read from network layer) buffer size. |
| Max Binary Message Size \* | Max Binary Message Size | 64 kb |  | The maximum size of a binary message during parsing/generating. |
| Max Text Message Size \* | Max Text Message Size | 64 kb |  | The maximum size of a text message during parsing/generating. |
| Password | Password |  |  | The user password for Basic Authentication. |
| SSL Context Service | SSL Context Service |  |  | The SSL Context Service to use in order to secure the server. If specified, the server will accept only WSS requests; otherwise, the server will accept only WS requests |
| Session Maintenance Interval \* | Session Maintenance Interval | 10 sec |  | The interval between session maintenance activities. A WebSocket session established with a WebSocket server can be terminated due to different reasons including restarting the WebSocket server or timing out inactive sessions. This session maintenance activity is periodically executed in order to reconnect those lost sessions, so that a WebSocket client can reuse the same session id transparently after it reconnects successfully. The maintenance activity is executed until corresponding processors or this controller service is stopped. |
| Username | Username |  |  | The user name for Basic Authentication. |
| WebSocket URI \* | WebSocket URI |  |  | The WebSocket URI this client connects to. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
