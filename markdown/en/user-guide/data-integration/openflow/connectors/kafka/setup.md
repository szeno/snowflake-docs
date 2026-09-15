# Set up the Openflow Connector for Kafka

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

## Prerequisites

1. Ensure that you have reviewed [Snowflake Openflow Connector for Kafka](/user-guide/data-integration/openflow/connectors/kafka/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the Kafka connector. The connector must be able to connect to all Kafka brokers in the cluster.

## Set up Snowflake account

As a Snowflake account administrator, perform the following tasks:

1. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property).
2. Create a new role or use an existing role and grant the [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges).

   The connector requires a user to create the destination table. Make sure the user has the required privileges for managing Snowflake objects:

   | Object | Privilege | Notes |
   | --- | --- | --- |
   | Database | USAGE |  |
   | Schema | USAGE |  |
   | Table | OWNERSHIP | Required for the connector to ingest data into a table. |

   Expand

   Show lessSee more

   Snowflake recommends creating a separate user and role for each Kafka Cluster for better access control.

   You can use the following script to create and configure a custom role (requires SECURITYADMIN or equivalent):

   Copy code

   ```
   USE ROLE securityadmin;
   CREATE ROLE openflow_kafka_connector_role_1;

   GRANT USAGE ON DATABASE kafka_db TO ROLE openflow_kafka_connector_role_1;
   GRANT USAGE ON SCHEMA kafka_schema TO ROLE openflow_kafka_connector_role_1;
   ```

   Note

   Privileges must be granted directly to the connector role and cannot be inherited.
3. Configure the destination table

   Snowflake highly recommends using server-side schema evolution for schema changes and [an error table for DML error logging](/user-guide/data-load-overview).
   The following example shows how to create a table and add proper OWNERSHIP permissions.

   Copy code

   ```
   USE ROLE openflow_kafka_connector_role_1;

   CREATE TABLE kafka_db.kafka_schema.<DESTINATION_TABLE_NAME> (
     kafkaMetadata variant
   )
   ENABLE_SCHEMA_EVOLUTION = TRUE
   ERROR_LOGGING = TRUE;

   USE ROLE securityadmin;
   GRANT OWNERSHIP ON TABLE existing_table1 TO ROLE openflow_kafka_connector_role_1;
   ```

   The connector supports automatic schema detection and evolution. The structure of tables in Snowflake is defined and evolved automatically to support the structure of new data loaded by the connector. It automatically maps the record content’s first-level keys to table columns matching by name (case-insensitive).

   With Schema evolution enabled, Snowflake can automatically expand the destination table by adding new columns that are detected in the incoming stream and dropping NOT NULL constraints to accommodate new data patterns. For more information, see [Table schema evolution](/user-guide/data-load-schema-evolution).

   If ENABLE\_SCHEMA\_EVOLUTION isn’t enabled, you must create the schema manually by extending the table definition. The connector tries to match the record content’s first-level keys to the table columns by name. If keys from the JSON don’t match the table columns, the connector ignores the keys.
4. (Optional) Configure a secrets manager

   Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow, for example, AWS, Azure, and Hashicorp, and store the public and private keys in the secret store.

   1. Determine how you’ll authenticate to the secrets manager after it’s configured. On AWS, Snowflake recommends using the EC2 instance role associated with Openflow so no other secrets need to be persisted.
   2. Configure a Parameter Provider associated with this Secrets Manager in Openflow from the hamburger menu in the upper right. Navigate to Controller Settings > Parameter Provider and fetch your parameter values.
   3. Reference all credentials with the associated parameter paths so no sensitive values need to be persisted within Openflow.
5. Grant access to users

   For any other Snowflake users who require access to the raw ingested data by the connector (for example, for custom processing in Snowflake), grant those users the role created in step 1.

## Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

### Install the connector

To install the connector, do the following:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the Select runtime dialog, select your runtime from the **Available runtimes** drop-down list and select **Add**.

   Note

   Before you install the connector, ensure that you have created a database, schema, and a table in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

   The Openflow canvas appears with the connector process group added to it.

### Configure the connector

1. If needed, customize the connector configuration before configuring the built-in parameters.

   Some common customizations have dedicated guides, such as custom transformations, Avro and Protobuf data type ingestion, and dead-letter-queue handling. You can also apply customizations using the Openflow skill in Snowflake CoCo. See [Configuring custom transformations](/user-guide/data-integration/openflow/connectors/streaming/configuring-custom-transformations) for more details.
2. Populate the process group parameters

   1. Right click on the imported process group and select Parameters.
   2. Fill out the required parameter values

#### Parameters

The following table describes the parameters for the Openflow Connector for Kafka:

| Parameter | Description | Required |
| --- | --- | --- |
| Kafka Auto Offset Reset | Automatic offset configuration applied when no previous consumer offset is found corresponding to Kafka `auto.offset.reset` property.  Possible values: **earliest**: automatically reset the offset to the earlier offset, **latest**: automatically reset the offset to the latest offset, **none**: throw exception to the consumer if no previous offset found for the consumer group.  Default: latest | Yes |
| Kafka Bootstrap Servers | A comma-separated list of Kafka bootstrap servers, should contain a port, for example `kafka-broker:9092`. | Yes |
| Kafka Consumer Group ID | The ID of a consumer group used by the connector. Can be arbitrary but must be unique. | Yes |
| Kafka SASL Password | Password provided with configured password when using SASL512 SCRAM Mechanism |  |
| Kafka SASL Username | Username provided with configured password when using SASL512 SCRAM Mechanism |  |
| Kafka Topic Format | One of: names / pattern. Specifies whether the “Kafka Topics” provided are a comma separated list of names or a single regular expression. | Yes |
| Kafka Topics | A comma-separated list of Kafka topics or a regular expression. | Yes |
| Snowflake Destination Database | The database where data is persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Snowflake Destination Schema | The schema where data is persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME`.  `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively. | Yes |
| Snowflake Destination Table | The table where data is persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |

Expand

Show lessSee more

### Start the connector

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the plane and select **Start**. The connector starts data ingestion.

## Understanding KAFKAMETADATA column

The connector populates the KAFKAMETADATA structure with metadata about the Kafka record. The structure contains the following information:

| Field | Data Type | Description |
| --- | --- | --- |
| topic | String | The name of the Kafka topic that the record came from. |
| partition | number | The number of the partition within the topic. (Note that this is the Kafka partition, not the Snowflake micro-partition.) |
| offset | number | The offset in that partition. |
| timestamp | number | Timestamp when the record was added to Kafka. |
| key | String | If the message is a Kafka KeyedMessage, this is the key for that message. In order for the connector to store the key in the RECORD\_METADATA, the `key.converter` parameter in the Kafka configuration properties must be set to `org.apache.kafka.connect.storage.StringConverter`; otherwise, the connector ignores keys. |
| headers | Object | A header is a user-defined key-value pair associated with the record. Each record can have 0, 1, or multiple headers. |

Expand

Show lessSee more

## Measuring ingestion latency

For change tracking, incremental processing, and time-travel queries based on row modification time, the ROW\_TIMESTAMP feature can be used.

Enable it by running the following command on your destination table:

Copy code

```
ALTER TABLE <DESTINATION_TABLE> SET ROW_TIMESTAMP = TRUE;
```

After row timestamps are enabled, tables expose the `METADATA$ROW_LAST_COMMIT_TIME` column, which returns the timestamp when each row was last modified.

For more information, see [METADATA$ROW\_LAST\_COMMIT\_TIME](/user-guide/data-load-overview).

Note

Row timestamp isn’t available for interactive tables. For more information, see [Snowflake interactive analytics](/user-guide/interactive).

## Using the connector with Apache Iceberg™ tables

The connector can ingest data into a Snowflake-managed Apache Iceberg™ table.

The connector doesn’t create Iceberg tables automatically. You must create the Iceberg table manually before you run the connector.

The connector supports server-side schema evolution for Iceberg destination tables, the same way it does for standard Snowflake tables. When the destination table has `ENABLE_SCHEMA_EVOLUTION = TRUE`, Snowflake automatically adds new columns that are detected in the incoming stream and drops NOT NULL constraints to accommodate new data patterns. For more information about how schema evolution behaves, see [Table schema evolution](/user-guide/data-load-schema-evolution).

The Iceberg table can use either of the following storage options:

- [Snowflake storage](/user-guide/tables-iceberg-internal-storage): Snowflake stores and manages the Iceberg table files for you, so you don’t need to create an external volume or grant the connector access to it.
- External cloud storage that you manage, accessed through an external volume. You must grant the connector role USAGE on the external volume.

### Grant usage on an external volume

This step applies only when the Iceberg table uses an external volume that you manage. If the table uses [Snowflake storage](/user-guide/tables-iceberg-internal-storage), skip this step.

For example, if your Iceberg table uses the `kafka_external_volume` external volume and the connector uses the role `openflow_kafka_connector_role`, run the following statement:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT USAGE ON EXTERNAL VOLUME kafka_external_volume TO ROLE openflow_kafka_connector_role;
```

### Create an Apache Iceberg™ table for ingestion

When you create an Iceberg table, you can use Iceberg data types (including VARIANT) or
[compatible Snowflake types](/user-guide/tables-iceberg-data-types).

For example, consider the following message:

Copy code

```
{
  "id": 1,
  "name": "Steve",
  "body_temperature": 36.6,
  "approved_coffee_types": ["Espresso", "Doppio", "Ristretto", "Lungo"],
  "animals_possessed": {
    "dogs": true,
    "cats": false
  },
  "options": {
    "can_walk": true,
    "can_talk": false
  },
  "date_added": "2024-10-15"
}
```

To create an Iceberg table for the example message, use one of the following statements.

To use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), set `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` and omit `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  kafkaMetadata OBJECT(
    topic STRING,
    partition INTEGER,
    offset BIGINT,
    key STRING,
    headers MAP(STRING, STRING),
    timestamp BIGINT
  ),
  id INT,
  name string,
  body_temperature float,
  approved_coffee_types array(string),
  animals_possessed variant,
  date_added date,
  options object(can_walk boolean, can_talk boolean)
)
EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
CATALOG = 'SNOWFLAKE'
ICEBERG_VERSION = 3;
```

To use your own external volume, set `EXTERNAL_VOLUME` to the volume name and provide a `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  kafkaMetadata OBJECT(
    topic STRING,
    partition INTEGER,
    offset BIGINT,
    key STRING,
    headers MAP(STRING, STRING),
    timestamp BIGINT
  ),
  id INT,
  name string,
  body_temperature float,
  approved_coffee_types array(string),
  animals_possessed variant,
  date_added date,
  options object(can_walk boolean, can_talk boolean)
)
EXTERNAL_VOLUME = 'my_volume'
CATALOG = 'SNOWFLAKE'
BASE_LOCATION = 'my_location/my_iceberg_table'
ICEBERG_VERSION = 3;
```

## Using the connector with Interactive Tables

Interactive tables are a special type of Snowflake table optimized for low-latency, high-concurrency queries. For more information, see [Snowflake interactive analytics](/user-guide/interactive).

1. Create an interactive table:

   Copy code

   ```
   CREATE INTERACTIVE TABLE REALTIME_METRICS (
     metric_name VARCHAR,
     metric_value NUMBER,
     source_topic VARCHAR,
     timestamp TIMESTAMP_NTZ
   ) AS (SELECT
      $1:M_NAME::VARCHAR,
      $1:M_VALUE::NUMBER,
      $1:RECORD_METADATA.topic::VARCHAR,
      $1:RECORD_METADATA.timestamp::TIMESTAMP_NTZ
      from TABLE(DATA_SOURCE(TYPE => 'STREAMING')));
   ```

Important considerations:

- Interactive tables have specific limitations and query restrictions. Review [Snowflake interactive analytics](/user-guide/interactive) before using them with the connector.
- For interactive tables, any required transformations must be handled in the table definition.
- Interactive warehouses are required to query interactive tables efficiently.

## Using the connector with a customer-defined schema for the destination table

The connector treats each Kafka record as a row to be inserted into a Snowflake table. For example, if you have a Kafka topic with the content of the message structured like the following JSON:

Copy code

```
{
  "order_id": 12345,
  "customer_name": "John",
  "order_total": 100.00,
  "isPaid": true
}
```

By default you don’t have to specify all fields from the JSON thanks to the `ENABLE_SCHEMA_EVOLUTION = TRUE` feature. However, if you prefer a static schema, it can be created by running:

Copy code

```
CREATE TABLE ORDERS (
  kafkaMetadata OBJECT,
  order_id NUMBER,
  customer_name VARCHAR,
  order_total FLOAT,
  ispaid BOOLEAN
);
```

## Using the connector with a customer-defined PIPE

If you choose to create your own pipe, you can define the data transformation logic in the pipe’s
[COPY INTO](/sql-reference/sql/copy-into-table) statement. You can rename columns as required and cast the data types as needed. For example:

Copy code

```
CREATE TABLE ORDERS (
  order_id VARCHAR,
  customer_name VARCHAR,
  order_total VARCHAR,
  ispaid VARCHAR
);

CREATE PIPE ORDERS AS
COPY INTO ORDERS
SELECT
  $1:order_id::STRING,
  $1:customer_name,
  $1:order_total::STRING,
  $1:isPaid::STRING
FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'));
```

When you define your own pipe, your destination table columns don’t need to match the JSON keys. You can rename the columns to your desired names and cast the data types if required.

To adjust the connector to work with a custom pipe, perform the following tasks:

1. Right-click on the PublishSnowpipeStreaming processor used in your Kafka ingestion flow in the Openflow canvas.
2. Select Configure from the context menu.
3. Navigate to the Properties tab.
4. In the Destination type field, pick Pipe.
5. In the Pipe field, type the name of your PIPE.
6. Select Apply to save the configuration.

## Customizing error handling

Error handling is split between Openflow-side failures and server-side failures within the Snowpipe Streaming service.

- **Openflow Errors (Client-Side Failures)**: Errors such as unparseable payloads or custom transformation failures occur before records reach Snowflake. By default these records are discarded. It’s possible to process these errors in Openflow - use FlowFiles from the parse failure relationship in the ConsumeKafka processor. For a complete walkthrough, see [Kafka as destination for DLQ messages](configuring-dead-letter-queue-handling) and the shared [Configuring Dead Letter Queue (DLQ) handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling).
- **Snowpipe Streaming Errors (Server-Side Failures)**: Errors for records that successfully reach Snowflake but are incompatible with the destination table’s schema (for example, type mismatches) are captured by the Snowflake infrastructure. When error logging is enabled on the destination table (`error_logging = true`), these failed rows are automatically ingested into the destination Error table.

## Performance tuning

[Performance Tuning of the Openflow Connector for Kafka](/user-guide/data-integration/openflow/connectors/kafka/performance-tuning)
