# JettyWebSocketServer

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Implementation of WebSocketServerService. This service uses Jetty WebSocket server module to provide WebSocket session management throughout the application.

## Tags

Jetty, WebSocket, server

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Basic Authentication Enabled \* | Basic Authentication Enabled | false | - true - false | If enabled, client connection requests are authenticated with Basic authentication using the specified Login Provider. |
| Basic Authentication Path Spec | Basic Authentication Path Spec | /\* |  | Specify a Path Spec to apply Basic Authentication. |
| Basic Authentication Roles | Basic Authentication Roles | `**` |  | The authenticated user must have one of specified role. Multiple roles can be set as comma separated string. ‘\*’ represents any role and so does ‘\*\*’ any role including no role. |
| Client Authentication \* | Client Authentication | no | - No Authentication - Want Authentication - Need Authentication | Specifies whether or not the Processor should authenticate client by its certificate. This value is ignored if the <SSL Context Service> Property is not specified or the SSL Context provided uses only a KeyStore and not a TrustStore. |
| Idle Timeout \* | Idle Timeout | 0 sec |  | The maximum amount of time that a WebSocket connection may remain idle before it is closed. A value of 0 sec disables the timeout. |
| Input Buffer Size \* | Input Buffer Size | 4 kb |  | The size of the input (read from network layer) buffer size. |
| Login Service | Login Service | hash | - HashLoginService | Specify which Login Service to use for Basic Authentication. |
| Max Binary Message Size \* | Max Binary Message Size | 64 kb |  | The maximum size of a binary message during parsing/generating. |
| Max Text Message Size \* | Max Text Message Size | 64 kb |  | The maximum size of a text message during parsing/generating. |
| Port \* | Port |  |  | The port number on which this WebSocketServer listens to. |
| SSL Context Service | SSL Context Service |  |  | The SSL Context Service to use in order to secure the server. If specified, the server will accept only WSS requests; otherwise, the server will accept only WS requests |
| Users Properties File | users-properties-file |  |  | Specify a property file containing users for Basic Authentication using HashLoginService. See <http://www.eclipse.org/jetty/documentation/current/configuring-security.html> for detail. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
