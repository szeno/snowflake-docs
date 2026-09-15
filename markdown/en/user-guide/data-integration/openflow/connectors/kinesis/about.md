# Openflow Connector for Amazon Kinesis Data Streams

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

## About

This topic describes the basic concepts of Openflow Connector for Amazon Kinesis Data Streams, including its workflow and limitations.

You can use [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html) to collect and process large streams of data records in real time. Producers continually push data to Kinesis Data Streams, and consumers process the data in real time.

A Kinesis data stream is a set of [shards](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html#shard). Each shard has a sequence of data records. A data record is the unit of data stored in a Kinesis data stream. Data records are composed of a sequence number, a partition key, and a data blob, which is an immutable sequence of bytes.

Openflow Connector for Amazon Kinesis Data Streams reads data from Kinesis streams and writes it into Snowflake tables using the
[Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) architecture.

Use this connector if you’re looking to do the following:

- Ingest real-time events from Amazon Kinesis into Snowflake for near real-time analytics
- Ingest real-time events from Amazon Kinesis into Snowflake-managed Iceberg™ tables
- Accelerate your ingestion even more by combining Openflow speed with the Interactive Tables feature
- Use Single Message Transforms to enrich or filter data before it lands in Snowflake.

## Limitations

- One connector supports only ingestion from a single stream.
- Autoscaling is not supported. The number of Openflow runtime min and max nodes should be constant for the runtime where Openflow Connector for Amazon Kinesis Data Streams is deployed.
- The connector supports routing Kinesis traffic through Snowflake outbound AWS PrivateLink. DynamoDB traffic must use the public endpoint because Amazon DynamoDB doesn’t support Private DNS. For more information, see [(Optional) Configure outbound AWS PrivateLink](/user-guide/data-integration/openflow/connectors/kinesis/setup#label-kinesis-configure-aws-privatelink).

### Limitations of fault tolerance with the connector

Kinesis Streams can be configured with a retention time. If for any reason the Openflow Connector for Amazon Kinesis Data Streams is not able to ingest data for more than the retention time, then expired records will not be loaded.

## Using different data types or data manipulation

The connector is configured to work with the JSON data type. It can be modified and extended in many ways. See the dedicated sub-pages in the setup section for guidance on making necessary changes, and the following shared streaming customization guides:

- [Configuring Avro data type ingestion](/user-guide/data-integration/openflow/connectors/streaming/configuring-avro-data-type-ingestion)
- [Configuring Protobuf data type ingestion](/user-guide/data-integration/openflow/connectors/streaming/configuring-protobuf-data-type-ingestion)
- [Configuring custom transformations](/user-guide/data-integration/openflow/connectors/streaming/configuring-custom-transformations)
- [Configuring Dead Letter Queue (DLQ) handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling) and the Kinesis-specific [Kinesis as destination for DLQ messages](configuring-dead-letter-queue-handling)
- [Configuring Private Key Authentication](/user-guide/data-integration/openflow/connectors/streaming/configuring-private-key-authentication)

### Supported data types

Openflow Connector for Amazon Kinesis Data Streams supports the following data types:

- **JSON (available by default in the connector)**
- [Avro](/user-guide/data-integration/openflow/connectors/streaming/configuring-avro-data-type-ingestion) (extra configuration required)
- [Protobuf](/user-guide/data-integration/openflow/connectors/streaming/configuring-protobuf-data-type-ingestion) (extra configuration required)

## Next steps

- [Set up Openflow Connector for Amazon Kinesis Data Streams](/user-guide/data-integration/openflow/connectors/kinesis/setup)
