# Kafka connector v3 (classic)

Important

- Advance notice: The classic Kafka connector (v3 and earlier) is fully supported today,
  but it is planned for future deprecation.
- Action: No immediate changes are required. Your current workloads are safe
  and continue to be fully supported.
- Timeline: Snowflake plans to issue a formal deprecation announcement in mid-2026.
  After the announcement, an 18-month migration window begins before end-of-life.
- Recommendation: Use the
  [Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index)
  for all new implementations.

For migration guidance, see [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

The classic Snowflake Connector for Kafka (v3 and earlier) reads data from one or more
[Apache Kafka](https://kafka.apache.org/) topics and loads the data into a Snowflake table.

For information about using Snowpipe Streaming with the classic connector, see
[Snowflake Connector for Kafka with Snowpipe Streaming classic](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-kafka).

**Topics:**

- [Overview of the Kafka connector](/user-guide/kafka-connector/classic/overview)
- [Installing and configuring the Kafka connector](/user-guide/kafka-connector/classic/install)
- [Managing the Kafka connector](/user-guide/kafka-connector/classic/manage)
- [Monitoring the Kafka connector using Java Management Extensions (JMX)](/user-guide/kafka-connector/classic/monitor)
- [Loading protobuf data using the Snowflake Connector for Kafka](/user-guide/kafka-connector/classic/protobuf)
- [Using the Snowflake Connector for Kafka with Apache Iceberg™ tables](/user-guide/kafka-connector/classic/iceberg)
- [Troubleshooting the Kafka connector](/user-guide/kafka-connector/classic/troubleshoot)
