# ConnectWebSocket 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-websocket-processors-nar

## Description

Acts as a WebSocket client endpoint to interact with a remote WebSocket server. FlowFiles are transferred to downstream relationships according to received message types as WebSocket client configured with this processor receives messages from remote WebSocket server. If a new flowfile is passed to the processor, the previous sessions will be closed and any data being sent will be aborted.

## Tags

WebSocket, consume, listen, subscribe

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| websocket-client-controller-service | A WebSocket CLIENT Controller Service which can connect to a WebSocket server. |
| websocket-client-id | The client ID to identify WebSocket session. It should be unique within the WebSocket Client Controller Service. Otherwise, it throws WebSocketConfigurationException when it gets started. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| binary message | The WebSocket binary message output |
| connected | The WebSocket session is established |
| disconnected | The WebSocket session is disconnected |
| failure | FlowFile holding connection configuration attributes (like URL or HTTP headers) in case of connection failure |
| success | FlowFile holding connection configuration attributes (like URL or HTTP headers) in case of successful connection |
| text message | The WebSocket text message output |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| websocket.controller.service.id | WebSocket Controller Service id. |
| websocket.session.id | Established WebSocket session id. |
| websocket.endpoint.id | WebSocket endpoint id. |
| websocket.local.address | WebSocket client address. |
| websocket.remote.address | WebSocket server address. |
| websocket.message.type | TEXT or BINARY. |

Expand

Show lessSee more
