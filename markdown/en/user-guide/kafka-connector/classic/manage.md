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

# Managing the Kafka connector

This topic describes the administrative tasks associated with managing the Kafka connector.

## Dropping Snowflake objects used by the Kafka connector

If you no longer plan to load data into Snowflake tables using the Kafka connector, you can shut down Kafka and drop the Snowflake objects used by the connector.

The connector uses Snowflake objects of the following types to ingest data:

- Named internal stages
- Pipes
- Tables

This section provides instructions for finding and dropping the Snowflake objects used by the Kafka connector.

### Dropping stages

The connector creates one named internal stage for each Kafka topic. The format of the stage name is:

> `SNOWFLAKE_KAFKA_CONNECTOR_connector_nameSTAGEtable_name`

Note that each internal stage stores not only files to be loaded into tables, but also “state” information that is used to ensure delivery
of rows from Kafka to the table.

If a stage and its state information are preserved, then if the connector is stopped and restarted, the connector automatically tries to
resume at the point where it left off. However, if a stage is removed, the connector cannot resume where it left off.

To drop the stages used by the Kafka connector:

1. Find the names of the stages by executing [SHOW STAGES](/sql-reference/sql/show-stages) as the stages owner (i.e. the role with the OWNERSHIP privilege on the stages. This should be the default role of the user defined in the Kafka configuration file to run the Kafka connector).
2. Execute [DROP STAGE](/sql-reference/sql/drop-stage) to drop each stage you want to remove from the system.

### Dropping pipes

The connector creates one pipe for each partition in a Kafka topic. The format of the pipe name is:

> `SNOWFLAKE_KAFKA_CONNECTOR_connector_namePIPEtable_name_partition_number`

To drop the pipes used by the Kafka connector:

1. Find the names of the pipes by executing [SHOW PIPES](/sql-reference/sql/show-pipes) as the pipes owner (i.e. the role with the
   OWNERSHIP privilege on the pipes. This should be the default role of the user defined in the Kafka configuration file to run
   the Kafka connector).
2. Execute [DROP PIPE](/sql-reference/sql/drop-pipe) to drop each pipe you want to remove from the system.

### Dropping tables

If the data loaded into your target tables is no longer needed, you can also drop these tables.

If you did not map Kafka topics to tables using the `snowflake.topic2table.map` parameter in the [Kafka configuration properties](/user-guide/kafka-connector-install#label-kafka-properties), the Kafka connector created new tables using the topic names. The table name is in uppercase but is otherwise identical to the topic name, as long as the topic name does not violate Snowflake object naming rules. For example, Snowflake creates a table name `TEMPERATURE_DATA` for a Kafka topic named `temperature_data`.

To drop the tables used by the Kafka connector:

1. Find the names of the tables by executing [SHOW TABLES](/sql-reference/sql/show-tables) as the tables owner (i.e. the role with the OWNERSHIP privilege on the tables. This should be the default role of the user defined in the Kafka configuration file to run the Kafka connector).
2. Execute [DROP TABLE](/sql-reference/sql/drop-table) to drop each table you want to remove from the system.
