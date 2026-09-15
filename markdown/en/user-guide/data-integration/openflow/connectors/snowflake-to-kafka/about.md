# About Openflow Connector for Snowflake to Kafka

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Snowflake to Kafka and limitations.

The connector consumes a Snowflake stream and sends consumed CDC records to a Kafka topic.
A Snowflake Stream object records data manipulation language (DML) changes made to tables,
including inserts, updates, and deletes, as well as metadata about each change, so that actions
can be taken using the changed data. This process is referred to as change data capture (CDC).

Use this connector if you’re looking to do the following:

- Replicate Snowflake tables to Apache Kafka using CDC for real-time insights distribution and event-driven architectures

## Workflow

Depending on the configuration of the Kafka broker, which is going to be receiving the CDC data, the workflow may differ slightly.

1. A Snowflake account administrator performs the following tasks:

   1. Creates or identifies the Snowflake stream that is going to be the source of the CDC data.
   2. Designates a warehouse to be used by the connector.
   3. Configures or identifies the Snowflake user used by the connector and a role for this user.
      The user must have appropriate permissions to the source Snowflake stream. At a minimum,
      the user needs USAGE privilege on the database and schema containing the Snowflake stream,
      and SELECT privilege on the stream and the stream’s underlying table or view object.
2. A Kafka administrator performs the following tasks.

   1. Creates or identifies a Kafka broker and topic that is going to be the destination for the CDC captured from the Snowflake stream.
   2. Sets up the authentication mechanism for the Kafka broker, which is going to be used by the connector.
3. A data engineer performs the following tasks:

   1. Installs and configures the connector.
   2. Provides Snowflake credentials and configuration.
   3. Provides Kafka credentials and configuration.
   4. Provides connector parameters.

## Stream metadata columns

Stream metadata columns `METADATA$ROW_ID`, `METADATA$ISUPDATE`, and `METADATA$ACTION` are sent to the Kafka topic.
The names of these columns are modified before they are sent to Kafka.
In the JSON message payload that is sent, they become `METADATA_ROW_ID`, `METADATA_ISUPDATE`, and `METADATA_ACTION`.

For more information, see [Stream columns](/user-guide/streams-intro#label-stream-metadata-columns).

## Limitations

- A single connector can only capture CDCs from one Snowflake stream.
- Messages are sent without a schema.
- Schema evolution is not supported.

## Next steps

[Set up the Openflow Connector for Snowflake to Kafka](/user-guide/data-integration/openflow/connectors/snowflake-to-kafka/setup)
