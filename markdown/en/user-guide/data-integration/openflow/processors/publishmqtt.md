# PublishMQTT 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mqtt-nar

## Description

Publishes a message to an MQTT topic

## Tags

IOT, MQTT, publish

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Broker URI | The URI(s) to use to connect to the MQTT broker (e.g., <tcp://localhost:1883>). The ‘tcp’, ‘ssl’, ‘ws’ and ‘wss’schemes are supported. In order to use ‘ssl’, the SSL Context Service property must be set. When a comma-separated URI list is set (e.g., <tcp://localhost:1883,tcp://localhost:1884>), the processor will use a round-robin algorithm to connect to the brokers on connection failure. |
| Client ID | MQTT client ID to use. If not set, a UUID will be generated. |
| Connection Timeout (seconds) | Maximum time interval the client will wait for the network connection to the MQTT server to be established. The default timeout is 30 seconds. A value of 0 disables timeout processing meaning the client will wait until the network connection is made successfully or fails. |
| Keep Alive Interval (seconds) | Defines the maximum time interval between messages sent or received. It enables the client to detect if the server is no longer available, without having to wait for the TCP/IP timeout. The client will ensure that at least one message travels across the network within each keep alive period. In the absence of a data-related message during the time period, the client sends a very small “ping” message, which the server will acknowledge. A value of 0 disables keepalive processing in the client. |
| Last Will Message | The message to send as the client’s Last Will. |
| Last Will QoS Level | QoS level to be used when publishing the Last Will Message. |
| Last Will Retain | Whether to retain the client’s Last Will. |
| Last Will Topic | The topic to send the client’s Last Will to. |
| MQTT Specification Version | The MQTT specification version when connecting with the broker. See the allowable value descriptions for more details. |
| Password | Password to use when connecting to the broker |
| Quality of Service(QoS) | The Quality of Service (QoS) to send the message with. Accepts three values ’0’, ’1’ and ’2’; ’0’ for ‘at most once’, ’1’ for ‘at least once’, ’2’ for ‘exactly once’. Expression language is allowed in order to support publishing messages with different QoS but the end value of the property must be either ’0’, ’1’ or ’2’. |
| Retain Message | Whether or not the retain flag should be set on the MQTT message. |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Session Expiry Interval | After this interval the broker will expire the client and clear the session state. |
| Session state | Whether to start a fresh or resume previous flows. See the allowable value descriptions for more details. |
| Topic | The topic to publish the message to. |
| Username | Username to use when connecting to the broker |
| message-demarcator | With this property, you have an option to publish multiple messages from a single FlowFile. This property allows you to provide a string (interpreted as UTF-8) to use for demarcating apart the FlowFile content. This is an optional property ; if not provided, and if not defining a Record Reader/Writer, each FlowFile will be published as a single message. To enter special character such as ‘new line’ use CTRL+Enter or Shift+Enter depending on the OS. |
| record-reader | The Record Reader to use for parsing the incoming FlowFile into Records. |
| record-writer | The Record Writer to use for serializing Records before publishing them as an MQTT Message. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to the destination are transferred to this relationship. |
| success | FlowFiles that are sent successfully to the destination are transferred to this relationship. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.mqtt.ConsumeMQTT](/user-guide/data-integration/openflow/processors/consumemqtt)
