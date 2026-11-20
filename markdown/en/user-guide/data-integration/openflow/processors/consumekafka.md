# ConsumeKafka 2026.11.12.16

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-kafka-nar

## Description

Reads messages from Apache Kafka topics and writes them to FlowFiles as raw content, delimited batches, or structured records.

The Processing Strategy determines how consumed messages are written:

- `FLOW_FILE` (default) writes each Kafka message value to a separate FlowFile without parsing it.
- `DEMARCATOR` combines messages from the same topic and partition, placing the UTF-8 Message Demarcator between values. If Separate By Key is `true`, messages with different keys are placed in different FlowFiles.
- `RECORD` parses message values with the configured Record Reader and serializes them with the configured Record Writer. Records are grouped by topic, partition, and selected header values. Schema Conflict Resolution controls how records with conflicting schemas are grouped.

If a message can’t be parsed or written with the configured Record Reader or Record Writer, its contents are written to a separate FlowFile and transferred to the `parse.failure` relationship. Otherwise, FlowFiles are transferred to `success` and can contain multiple messages. The `record.count` attribute indicates the number of messages in a FlowFile.

Kafka header values selected for output use Header Format. They can be represented as text decoded with Header Encoding or as lowercase hexadecimal strings.

## Tags

Consume, Get, Ingest, Ingress, Kafka, PubSub, Record, Topic, avro, csv, json

## Input requirement

FORBIDDEN

## Supports sensitive dynamic properties

false

## Properties

Configure how the processor connects to Kafka, selects messages, and writes FlowFile content and attributes.

| Property | Description | Configuration |
| --- | --- | --- |
| Auto Offset Reset | Sets `auto.offset.reset` when the consumer group has no committed offset. | Required. Values: `earliest`, `latest` (default), `none`. Expression Language isn’t supported. |
| Commit Offsets | Controls whether the processor commits offsets after receiving messages. | Required. Values: `true` (default), `false`. |
| Group ID | Sets the Kafka consumer group identifier that corresponds to `group.id`. | Required. Expression Language isn’t supported. |
| Header Encoding | Character set used to decode Kafka header values. | Required when Header Format is `string`. Default: `UTF-8`. |
| Header Format | Controls how Kafka header values are represented in attributes or record fields. | Required. Values: `string` (default), `hex`. |
| Header Name Pattern | Java regular expression that selects Kafka headers for FlowFile attributes. | Optional. |
| Header Name Prefix | Prefix applied to attribute names created from Kafka headers to avoid reserved-name conflicts. | Optional. Applies when Processing Strategy is `FLOW_FILE`. |
| Kafka Connection Service | KafkaConnectionService controller service that supplies connections to Kafka brokers. | Required. Expression Language isn’t supported. |
| Key Attribute Encoding | Controls how the Kafka key is written to the `kafka.key` attribute. | Required. Values: `utf-8` (default), `hex`, `do-not-add`. |
| Key Format | Controls how wrapper output represents the Kafka record key. | Required when Output Strategy is `USE_WRAPPER` or `INJECT_METADATA`. Values: `string`, `byte-array` (default), `record`. |
| Key Record Reader | RecordReaderFactory controller service used to parse Kafka record keys. | Required when Key Format is `record`. Expression Language isn’t supported. |
| Max Uncommitted Size | Maximum combined size of serialized keys and values to consume before transferring FlowFiles. | Optional. Evaluated before Max Uncommitted Time. |
| Max Uncommitted Time | Maximum time to consume records before transferring FlowFiles. Longer periods can produce larger FlowFiles and increase latency. | Required. Default: `100 millis`. |
| Message Demarcator | UTF-8 string inserted between Kafka messages combined in one FlowFile. | Required when Processing Strategy is `DEMARCATOR`. |
| Output Strategy | Controls the representation of Kafka records in record-oriented FlowFiles. | Required when Processing Strategy is `RECORD`. Values: `USE_VALUE` (default), `USE_WRAPPER`, `INJECT_METADATA`, `INJECT_OFFSET`. |
| Processing Strategy | Controls whether output uses individual FlowFiles, demarcated batches, or records. | Required. Values: `FLOW_FILE` (default), `DEMARCATOR`, `RECORD`. Expression Language isn’t supported. |
| Record Reader | RecordReaderFactory controller service used to parse Kafka message values. | Required when Processing Strategy is `RECORD`. |
| Record Writer | RecordSetWriterFactory controller service used to serialize outgoing FlowFiles. | Required when Processing Strategy is `RECORD`. |
| Schema Conflict Resolution | Controls how records with different schemas are grouped into FlowFiles. | Required when Processing Strategy is `RECORD`. Values: `CREATE_NEW_FLOWFILE` (default), `CONTINUE_WITH_MERGED_SCHEMA`. |
| Separate By Key | Controls whether a demarcated FlowFile can contain messages with different keys. | Required when Message Demarcator is configured. Values: `true`, `false` (default). |
| Topic Format | Specifies whether Topics contains names or a Java regular expression. | Required. Values: `names` (default), `pattern`. |
| Topics | Identifies topics by a name, comma-separated names, or a pattern, depending on Topic Format. | Required. Supports JVM environment variables and system properties. |

Expand

Show lessSee more

The processor doesn’t support dynamic properties.

## Output strategies

The Output Strategy property applies when Processing Strategy is `RECORD`:

- **Use Content as Value** writes only the Kafka record value.
- **Use Wrapper** writes the key, value, headers, and metadata as separate fields. The metadata contains the topic, partition, offset, and timestamp.
- **Inject Metadata** writes the record value and adds a `kafkaMetadata` sub-record containing the topic, partition, offset, timestamp, headers, and key.
- **Inject Offset** writes the record value and adds the Kafka offset.

When Output Strategy is **Use Wrapper** or **Inject Metadata**, Key Format specifies whether the Kafka record key is represented as a byte array, a UTF-8 string, or a record parsed by Key Record Reader. A key that can’t be parsed with the selected format is transferred to `parse.failure`.

## Relationships

Connect this relationship to route FlowFiles after the processor consumes and serializes Kafka messages.

| Name | Description |
| --- | --- |
| success | Routes FlowFiles that contain one or more serialized Kafka records. |

Expand

Show lessSee more

## Writes attributes

The processor writes these attributes to describe the Kafka messages in each output FlowFile.

| Name | Description |
| --- | --- |
| record.count | Number of records written to the FlowFile. |
| mime.type | MIME type supplied by the configured Record Writer. |
| kafka.count | Number of Kafka messages represented by the FlowFile. |
| kafka.key | Key of a single Kafka message, when present. Key Attribute Encoding controls its encoding. |
| kafka.offset | Offset of a single Kafka message, or the lowest offset in a batch. |
| kafka.timestamp | Timestamp of a single Kafka message, or the earliest timestamp in a batch. The Kafka broker `log.message.timestamp.type` setting determines its meaning. |
| kafka.partition | Partition that supplied the message or batch. |
| kafka.topic | Topic that supplied the message or batch. |
| kafka.max.offset | Highest Kafka offset in a batch. |
| kafka.tombstone | Set to `true` when the consumed message is a tombstone message. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.kafka.processors.PublishKafka](/user-guide/data-integration/openflow/processors/publishkafka)
