# Set up tasks for the Snowflake Connector for Kafka

This topic describes the overall tasks required to set up, configure, and run the Snowflake Connector for Kafka.

## Prerequisites

Ensure the following prerequisites are met:

1. Ensure that you have reviewed [Snowflake Connector for Kafka](/user-guide/kafka-connector/index).
2. Ensure that you have reviewed [how the connector works](/user-guide/kafka-connector/how-the-connector-works).
3. You have configured Kafka with the desired data retention time and/or storage limit.
   See [how the connector works](/user-guide/kafka-connector/how-the-connector-works) for all supported properties.
4. You have installed and configured the Kafka Connect cluster.   
   Snowflake recommends using the same versions on Kafka Broker and Kafka Connect Runtime.
5. You have configured the Kafka Connect cluster to run in the same cloud provider
   [region](/user-guide/intro-regions) as your Snowflake account.   
   While not strictly required, running in the same region improves throughput and reduces
   cross-region data transfer costs.

## Tasks

Perform the following tasks to set up, configure, and run the Snowflake Connector for Kafka.

| Order | Task | Description |
| --- | --- | --- |
| 0 | Review [Prerequisites](#label-kafkahp-of-connector-prerequisites) | Review and confirm all required prerequisites. |
| 1 | [Configure Snowflake](/user-guide/kafka-connector/setup-snowflake) | Configure Snowflake for the Snowflake Connector for Kafka. |
| 2 | [Configure Kafka](/user-guide/kafka-connector/setup-kafka) | Configure Kafka for the Snowflake Connector for Kafka. |
| 3 | [Test the connector](/user-guide/kafka-connector/test-connector) | Test the connector with a small amount of data. |

Expand

Show lessSee more
