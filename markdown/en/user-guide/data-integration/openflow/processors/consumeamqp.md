# ConsumeAMQP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-amqp-nar

## Description

Consumes AMQP Messages from an AMQP Broker using the AMQP 0.9.1 protocol. Each message that is received from the AMQP Broker will be emitted as its own FlowFile to the ‘success’ relationship.

## Tags

amqp, consume, get, message, rabbit, receive

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AMQP Version | AMQP Version. Currently only supports AMQP v0.9.1. |
| Auto-Acknowledge Messages | If false (Non-Auto-Acknowledge), the messages will be acknowledged by the processor after transferring the FlowFiles to success and committing the NiFi session. Non-Auto-Acknowledge mode provides ‘at-least-once’ delivery semantics. If true (Auto-Acknowledge), messages that are delivered to the AMQP Client will be auto-acknowledged by the AMQP Broker just after sending them out. This generally will provide better throughput but will also result in messages being lost upon restart/crash of the AMQP Broker, NiFi or the processor. Auto-Acknowledge mode provides ‘at-most-once’ delivery semantics and it is recommended only if losing messages is acceptable. |
| Batch Size | The maximum number of messages that should be processed in a single session. Once this many messages have been received (or once no more messages are readily available), the messages received will be transferred to the ‘success’ relationship and the messages will be acknowledged to the AMQP Broker. Setting this value to a larger number could result in better performance, particularly for very small messages, but can also result in more messages being duplicated upon sudden restart of NiFi. |
| Brokers | A comma-separated list of known AMQP Brokers in the format <host>:<port> (e.g., localhost:5672). If this is set, Host Name and Port are ignored. Only include hosts from the same AMQP cluster. |
| Client Certificate Authentication Enabled | Authenticate using the SSL certificate rather than user name/password. |
| Header Key Prefix | Text to be prefixed to header keys as the are added to the FlowFile attributes. Processor will append ‘.’ to the value of this property |
| Header Output Format | Defines how to output headers from the received message |
| Header Separator | The character that is used to separate key-value for header in String. The value must be only one character. |
| Host Name | Network address of AMQP broker (e.g., localhost). If Brokers is set, then this property is ignored. |
| Max Inbound Message Body Size | Maximum body size of inbound (received) messages. |
| Password | Password used for authentication and authorization. |
| Port | Numeric value identifying Port of AMQP broker (e.g., 5671). If Brokers is set, then this property is ignored. |
| Prefetch Count | The maximum number of unacknowledged messages for the consumer. If consumer has this number of unacknowledged messages, AMQP broker will no longer send new messages until consumer acknowledges some of the messages already delivered to it. Allowed values: from 0 to 65535.0 means no limit |
| Queue | The name of the existing AMQP Queue from which messages will be consumed. Usually pre-defined by AMQP administrator. |
| Remove Curly Braces | If true Remove Curly Braces, Curly Braces in the header will be automatically remove. |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Username | Username used for authentication and authorization. |
| Virtual Host | Virtual Host name which segregates AMQP system for enhanced security. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles that are received from the AMQP queue are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| amqp$appId | The App ID field from the AMQP Message |
| amqp$contentEncoding | The Content Encoding reported by the AMQP Message |
| amqp$contentType | The Content Type reported by the AMQP Message |
| amqp$headers | The headers present on the AMQP Message. Added only if processor is configured to output this attribute. |
| <Header Key Prefix>.<attribute> | Each message header will be inserted with this attribute name, if processor is configured to output headers as attribute |
| amqp$deliveryMode | The numeric indicator for the Message’s Delivery Mode |
| amqp$priority | The Message priority |
| amqp$correlationId | The Message’s Correlation ID |
| amqp$replyTo | The value of the Message’s Reply-To field |
| amqp$expiration | The Message Expiration |
| amqp$messageId | The unique ID of the Message |
| amqp$timestamp | The timestamp of the Message, as the number of milliseconds since epoch |
| amqp$type | The type of message |
| amqp$userId | The ID of the user |
| amqp$clusterId | The ID of the AMQP Cluster |
| amqp$routingKey | The routingKey of the AMQP Message |
| amqp$exchange | The exchange from which AMQP Message was received |

Expand

Show lessSee more
