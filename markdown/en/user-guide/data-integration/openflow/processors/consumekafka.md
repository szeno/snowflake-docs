# ConsumeKafka 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-kafka-nar

## Description

Consumes messages from Apache Kafka Consumer API. The complementary NiFi processor for sending messages is PublishKafka. The Processor supports consumption of Kafka messages, optionally interpreted as NiFi records. Please note that, at this time (in read record mode), the Processor assumes that all records that are retrieved from a given partition have the same schema. For this mode, if any of the Kafka messages are pulled but cannot be parsed or written with the configured Record Reader or Record Writer, the contents of the message will be written to a separate FlowFile, and that FlowFile will be transferred to the ‘parse.failure’ relationship. Otherwise, each FlowFile is sent to the ‘success’ relationship and may contain many individual messages within the single FlowFile. A ‘record.count’ attribute is added to indicate how many messages are contained in the FlowFile. No two Kafka messages will be placed into the same FlowFile if they have different schemas, or if they have different values for a message header that is included by the <Headers to Add as Attributes> property.

## Tags

avro, consume, csv, get, ingest, ingress, json, kafka, openflow, pubsub, record, topic

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Commit Offsets | Specifies whether this Processor should commit the offsets to Kafka after receiving messages. Typically, this value should be set to true so that messages that are received are not duplicated. However, in certain scenarios, we may want to avoid committing the offsets, that the data can be processed and later acknowledged by PublishKafka in order to provide Exactly Once semantics. |
| Content Field | Specifies under what field of the record the content will be added. If not set, the content will be at the root of the record |
| Group ID | Kafka Consumer Group Identifier corresponding to Kafka group.id property |
| Header Encoding | Character encoding applied when reading Kafka Record Header values and writing FlowFile attributes |
| Header Name Pattern | Regular Expression Pattern applied to Kafka Record Header Names for selecting Header Values to be written as FlowFile attributes |
| Headers Field Parent | Specifies under what field of the record the headers field will be added. If not set, the headers field will be at the root of the record |
| Kafka Connection Service | Provides connections to Kafka Broker for publishing Kafka Records |
| Key Attribute Encoding | Encoding for value of configured FlowFile attribute containing Kafka Record Key. |
| Key Field Parent | Specifies under what field of the record the key field will be added. If not set, the key field will be at the root of the record |
| Key Format | Specifies how to represent the Kafka Record Key in the output FlowFile |
| Key Record Reader | The Record Reader to use for parsing the Kafka Record Key into a Record |
| Max Uncommitted Time | Specifies the maximum amount of time that the Processor can consume from Kafka before it must transfer FlowFiles on through the flow and commit the offsets to Kafka (if appropriate). A larger time period can result in longer latency |
| Message Demarcator | Since KafkaConsumer receives messages in batches, this Processor has an option to output FlowFiles which contains all Kafka messages in a single batch for a given topic and partition and this property allows you to provide a string (interpreted as UTF-8) to use for demarcating apart multiple Kafka messages. This is an optional property and if not provided each Kafka message received will result in a single FlowFile which time it is triggered. To enter special character such as ‘new line’ use CTRL+Enter or Shift+Enter depending on the OS |
| Metadata Field | Specifies under what field of the record the metadata will be added. If not set, the metadata will be at the root of the record |
| Metadata Received Timestamp Field | If specified a timestamp will be placed under the specified field in the metadata of record in the output FlowFile |
| Output Strategy | The format used to output the Kafka Record into a FlowFile Record. |
| Processing Strategy | Strategy for processing Kafka Records and writing serialized output to FlowFiles |
| Record Reader | The Record Reader to use for incoming Kafka messages |
| Record Writer | The Record Writer to use in order to serialize the outgoing FlowFiles |
| Separate By Key | When this property is enabled, two messages will only be added to the same FlowFile if both of the Kafka Messages have identical keys. |
| Topic Format | Specifies whether the Topics provided are a comma separated list of names or a single regular expression |
| Topics | The name or pattern of the Kafka Topics from which the Processor consumes Kafka Records. More than one can be supplied if comma separated. |
| auto.offset.reset | Automatic offset configuration applied when no previous consumer offset found corresponding to Kafka auto.offset.reset property |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles containing one or more serialized Kafka Records |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The number of records received |
| mime.type | The MIME Type that is provided by the configured Record Writer |
| kafka.count | The number of messages written if more than one |
| kafka.key | The key of message if present and if single message. How the key is encoded depends on the value of the ‘Key Attribute Encoding’ property. |
| kafka.offset | The offset of the message in the partition of the topic. |
| kafka.timestamp | The timestamp of the message in the partition of the topic. |
| kafka.partition | The partition of the topic the message or message bundle is from |
| kafka.topic | The topic the message or message bundle is from |
| kafka.tombstone | Set to true if the consumed message is a tombstone message |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.kafka.PublishKafka](/user-guide/data-integration/openflow/processors/publishkafka)
