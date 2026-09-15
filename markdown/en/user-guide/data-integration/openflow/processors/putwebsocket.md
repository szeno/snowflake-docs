# PutWebSocket 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-websocket-processors-nar

## Description

Sends messages to a WebSocket remote endpoint using a WebSocket session that is established by either ListenWebSocket or ConnectWebSocket.

## Tags

WebSocket, publish, send

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| websocket-controller-service-id | A NiFi Expression to retrieve the id of a WebSocket ControllerService. |
| websocket-endpoint-id | A NiFi Expression to retrieve the endpoint id of a WebSocket ControllerService. |
| websocket-message-type | The type of message content: TEXT or BINARY |
| websocket-session-id | A NiFi Expression to retrieve the session id. If not specified, a message will be sent to all connected WebSocket peers for the WebSocket controller service endpoint. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to the destination are transferred to this relationship. |
| success | FlowFiles that are sent successfully to the destination are transferred to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| websocket.controller.service.id | WebSocket Controller Service id. |
| websocket.session.id | Established WebSocket session id. |
| websocket.endpoint.id | WebSocket endpoint id. |
| websocket.message.type | TEXT or BINARY. |
| websocket.local.address | WebSocket server address. |
| websocket.remote.address | WebSocket client address. |
| websocket.failure.detail | Detail of the failure. |

Expand

Show lessSee more
