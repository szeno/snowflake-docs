# PublishKafka 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-kafka-nar

## Description

Sends the contents of a FlowFile as either a message or as individual records to Apache Kafka using the Kafka Producer API. The messages to send may be individual FlowFiles, may be delimited using a user-specified delimiter (such as a new-line), or may be record-oriented data that can be read by the configured Record Reader. The complementary NiFi processor for fetching messages is ConsumeKafka.

## Tags

apache, avro, csv, json, kafka, logs, message, openflow, pubsub, put, record, send

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Failure Strategy | Specifies how the processor handles a FlowFile if it is unable to publish the data to Kafka |
| FlowFile Attribute Header Pattern | A Regular Expression that is matched against all FlowFile attribute names. Any attribute whose name matches the pattern will be added to the Kafka messages as a Header. If not specified, no FlowFile attributes will be added as headers. |
| Header Encoding | For any attribute that is added as a Kafka Record Header, this property indicates the Character Encoding to use for serializing the headers. |
| Kafka Connection Service | Provides connections to Kafka Broker for publishing Kafka Records |
| Kafka Key | The Key to use for the Message. If not specified, the FlowFile attribute ‘kafka.key’ is used as the message key, if it is present. Beware that setting Kafka key and demarcating at the same time may potentially lead to many Kafka messages with the same key. Normally this is not a problem as Kafka does not enforce or assume message and key uniqueness. Still, setting the demarcator and Kafka key at the same time poses a risk of data loss on Kafka. During a topic compaction on Kafka, messages will be deduplicated based on this key. |
| Kafka Key Attribute Encoding | FlowFiles that are emitted have an attribute named ‘kafka.key’. This property dictates how the value of the attribute should be encoded. |
| Message Demarcator | Specifies the string (interpreted as UTF-8) to use for demarcating multiple messages within a single FlowFile. If not specified, the entire content of the FlowFile will be used as a single message. If specified, the contents of the FlowFile will be split on this delimiter and each section sent as a separate Kafka message. To enter special character such as ‘new line’ use CTRL+Enter or Shift+Enter, depending on your OS. |
| Message Key Field | The name of a field in the Input Records that should be used as the Key for the Kafka message. |
| Publish Strategy | The format used to publish the incoming FlowFile record to Kafka. |
| Record Key Writer | The Record Key Writer to use for outgoing FlowFiles |
| Record Metadata Strategy | Specifies whether the Record ‘s metadata (topic and partition) should come from the Record’s metadata field or if it should come from the configured Topic Name and Partition / Partitioner class properties |
| Record Reader | The Record Reader to use for incoming FlowFiles |
| Record Writer | The Record Writer to use in order to serialize the data before sending to Kafka |
| Topic Name | Name of the Kafka Topic to which the Processor publishes Kafka Records |
| Transactional ID Prefix | Specifies the KafkaProducer config transactional.id will be a generated UUID and will be prefixed with the configured string. |
| Transactions Enabled | Specifies whether to provide transactional guarantees when communicating with Kafka. If there is a problem sending data to Kafka, and this property is set to false, then the messages that have already been sent to Kafka will continue on and be delivered to consumers. If this is set to true, then the Kafka transaction will be rolled back so that those messages are not available to consumers. Setting this to true requires that the [Delivery Guarantee] property be set to [Guarantee Replicated Delivery.] |
| acks | Specifies the requirement for guaranteeing that a message is sent to Kafka. Corresponds to Kafka Client acks property. |
| compression.type | Specifies the compression strategy for records sent to Kafka. Corresponds to Kafka Client compression.type property. |
| max.request.size | The maximum size of a request in bytes. Corresponds to Kafka Client max.request.size property. |
| partition | Specifies the Kafka Partition destination for Records. |
| partitioner.class | Specifies which class to use to compute a partition id for a message. Corresponds to Kafka Client partitioner.class property. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Any FlowFile that cannot be sent to Kafka will be routed to this Relationship |
| success | FlowFiles for which all content was sent to Kafka. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| msg.count | The number of messages that were sent to Kafka for this FlowFile. This attribute is added only to FlowFiles that are routed to success. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.kafka.ConsumeKafka](/user-guide/data-integration/openflow/processors/consumekafka)
