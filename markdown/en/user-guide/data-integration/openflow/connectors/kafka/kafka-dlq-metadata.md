Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Snowflake Openflow Connector for Kafka

This topic describes the basic concepts of the Openflow Connector for Kafka and its limitations.

The Openflow Connector for Kafka reads data from Kafka topics and writes it into Snowflake tables using the
[Snowpipe Streaming High Performance](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) architecture.

Use this connector if you’re looking to do the following:

- Ingest real-time events from Apache Kafka into Snowflake for near real-time analytics
- Ingest real-time events from Apache Kafka into Snowflake-managed Iceberg™ tables
- Accelerate your ingestion even more by combining Openflow speed with the Interactive Tables feature
- Do Single Message Transforms for data enrichments or filtering before data lands in Snowflake.

## Limitations

- Autoscaling isn’t supported. The number of Openflow runtime min and max nodes should be constant for the runtime where the Openflow Connector for Kafka is deployed.
- The Kafka cluster must be running version 0.10.0.0 or later. Prior versions of Kafka aren’t supported.

## Using different authentication options, data types or data manipulation

The connector is configured to work with the JSON data type and the SASL\_SSL authentication method. The connector can be modified and extended in many ways. See the dedicated sub-pages in the setup section for guidance on making necessary changes.

The following shared streaming customization guides apply to this connector:

- [Configuring Avro data type ingestion](/user-guide/data-integration/openflow/connectors/streaming/configuring-avro-data-type-ingestion)
- [Configuring Protobuf data type ingestion](/user-guide/data-integration/openflow/connectors/streaming/configuring-protobuf-data-type-ingestion)
- [Configuring custom transformations](/user-guide/data-integration/openflow/connectors/streaming/configuring-custom-transformations)
- [Configuring Dead Letter Queue (DLQ) handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling) and the Kafka-specific [Kafka as destination for DLQ messages](configuring-dead-letter-queue-handling)
- [Configuring Private Key Authentication](/user-guide/data-integration/openflow/connectors/streaming/configuring-private-key-authentication)

### Supported Data types

The Openflow Connector for Kafka supports the following data types:

- **JSON (available by default in the connector)**
- [Avro](/user-guide/data-integration/openflow/connectors/streaming/configuring-avro-data-type-ingestion) (extra configuration required)
- [Protobuf](/user-guide/data-integration/openflow/connectors/streaming/configuring-protobuf-data-type-ingestion) (extra configuration required)

### Supported Authentication Methods

The Openflow Connector for Kafka supports the following authentication mechanisms:

- SASL with the following SASL mechanisms:

  - PLAIN
  - SCRAM-SHA-256
  - **SCRAM-SHA-512 (available by default in the connector)**
  - OAUTHBEARER
- [SASL with AWS MSK IAM](/user-guide/data-integration/openflow/connectors/kafka/aws-msk-iam-auth) (extra configuration required via controller services)
- [mTLS](/user-guide/data-integration/openflow/connectors/kafka/mtls-auth) (extra configuration required via controller services)

## Next steps

[Set up the Openflow Connector for Kafka](/user-guide/data-integration/openflow/connectors/kafka/setup)
