# The Apache Kafka and Kafka Connect framework

This topic describes the basic concepts of Apache Kafka and Kafka Connect Framework.

Apache Kafka software uses a publish and subscribe model to write and read streams of records,
similar to a message queue or enterprise messaging system.
Kafka allows processes to read and write messages asynchronously.
A subscriber does not need to be connected directly to a publisher; a publisher can queue a message in Kafka for the subscriber to receive later.

An application publishes messages to a *topic*, and an application subscribes to a topic to receive those messages.

Kafka Connect is a framework for connecting Kafka with external systems, including databases.
A Kafka Connect cluster is a separate cluster from the Kafka cluster.
The Kafka Connect cluster supports running and scaling out connectors (components that support reading and/or writing to external systems).

Kafka Connect can be used with two types of connectors:

- **Source connectors**: Import data from external systems into Kafka topics.
- **Sink connectors**: Export data from Kafka topics to external systems.

The Snowflake Connector for Kafka is a sink connector that reads data from Kafka topics and loads it into Snowflake tables.

Kafka Connect handles common operational concerns such as:

- Scalability: Kafka Connect can scale horizontally by adding more worker nodes to the cluster.
- Fault tolerance: If a worker node fails, Kafka Connect automatically redistributes the work to other available nodes.
- Offset management: Kafka Connect tracks which records have been processed, ensuring that data is not lost or duplicated in case of failures.
- Configuration management: Connectors can be configured and managed through a REST API, making it easier to deploy and monitor data pipelines.
