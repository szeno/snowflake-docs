# ConsumeMQTT 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mqtt-nar

## Description

Subscribes to a topic and receives messages from an MQTT broker

## Tags

IOT, MQTT, consume, listen, subscribe

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Broker URI | The URI(s) to use to connect to the MQTT broker (e.g., <tcp://localhost:1883>). The ‘tcp’, ‘ssl’, ‘ws’ and ‘wss’schemes are supported. In order to use ‘ssl’, the SSL Context Service property must be set. When a comma-separated URI list is set (e.g., <tcp://localhost:1883,tcp://localhost:1884>), the processor will use a round-robin algorithm to connect to the brokers on connection failure. |
| Client ID | MQTT client ID to use. If not set, a UUID will be generated. |
| Connection Timeout (seconds) | Maximum time interval the client will wait for the network connection to the MQTT server to be established. The default timeout is 30 seconds. A value of 0 disables timeout processing meaning the client will wait until the network connection is made successfully or fails. |
| Group ID | MQTT consumer group ID to use. If group ID not set, client will connect as individual consumer. |
| Keep Alive Interval (seconds) | Defines the maximum time interval between messages sent or received. It enables the client to detect if the server is no longer available, without having to wait for the TCP/IP timeout. The client will ensure that at least one message travels across the network within each keep alive period. In the absence of a data-related message during the time period, the client sends a very small “ping” message, which the server will acknowledge. A value of 0 disables keepalive processing in the client. |
| Last Will Message | The message to send as the client’s Last Will. |
| Last Will QoS Level | QoS level to be used when publishing the Last Will Message. |
| Last Will Retain | Whether to retain the client’s Last Will. |
| Last Will Topic | The topic to send the client’s Last Will to. |
| MQTT Specification Version | The MQTT specification version when connecting with the broker. See the allowable value descriptions for more details. |
| Max Queue Size | The MQTT messages are always being sent to subscribers on a topic regardless of how frequently the processor is scheduled to run. If the ‘Run Schedule’ is significantly behind the rate at which the messages are arriving to this processor, then a back up can occur in the internal queue of this processor. This property specifies the maximum number of messages this processor will hold in memory at one time in the internal queue. This data would be lost in case of a NiFi restart. |
| Password | Password to use when connecting to the broker |
| Quality of Service(QoS) | The Quality of Service (QoS) to receive the message with. Accepts values ’0’, ’1’ or ’2’; ’0’ for ‘at most once’, ’1’ for ‘at least once’, ’2’ for ‘exactly once’. |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Session Expiry Interval | After this interval the broker will expire the client and clear the session state. |
| Session state | Whether to start a fresh or resume previous flows. See the allowable value descriptions for more details. |
| Topic Filter | The MQTT topic filter to designate the topics to subscribe to. |
| Username | Username to use when connecting to the broker |
| add-attributes-as-fields | If setting this property to true, default fields are going to be added in each record: \_topic, \_qos, \_isDuplicate, \_isRetained. |
| message-demarcator | With this property, you have an option to output FlowFiles which contains multiple messages. This property allows you to provide a string (interpreted as UTF-8) to use for demarcating apart multiple messages. This is an optional property ; if not provided, and if not defining a Record Reader/Writer, each message received will result in a single FlowFile. To enter special character such as ‘new line’ use CTRL+Enter or Shift+Enter depending on the OS. |
| record-reader | The Record Reader to use for parsing received MQTT Messages into Records. |
| record-writer | The Record Writer to use for serializing Records before writing them to a FlowFile. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| Message | The MQTT message output |
| parse.failure | If a message cannot be parsed using the configured Record Reader, the contents of the message will be routed to this Relationship as its own individual FlowFile. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The number of records received |
| mqtt.broker | MQTT broker that was the message source |
| mqtt.topic | MQTT topic on which message was received |
| mqtt.qos | The quality of service for this message. |
| mqtt.isDuplicate | Whether or not this message might be a duplicate of one which has already been received. |
| mqtt.isRetained | Whether or not this message was from a current publisher, or was “retained” by the server as the last message published on the topic. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.mqtt.PublishMQTT](/user-guide/data-integration/openflow/processors/publishmqtt)
