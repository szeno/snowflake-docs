# Snowflake Connector for Kafka: Test the connector

This topic describes the steps to test the Snowflake Connector for Kafka connector itself.

## Testing and using the Kafka connector

Snowflake recommends testing the Kafka connector with a small amount of data before using the connector in a production system.

1. Verify that Kafka and Kafka Connect are running.
2. Verify that you have created the appropriate Kafka topic.
3. Create (or use an existing) message publisher. Make sure that the messages published to the topic have the right format (JSON, Avro, Protobuf).
4. Create a configuration that specifies the topic to subscribe to and the Snowflake table to write to.
5. Grant the minimum privileges required on the Snowflake objects (database, schema) to the role that will be used to ingest data.
6. Publish a sample set of data to the configured Kafka topic.
7. Wait a few seconds for data to propagate through the system, and then check the Snowflake table to verify that the records were inserted.
