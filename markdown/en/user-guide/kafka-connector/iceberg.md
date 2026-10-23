# Load data into Iceberg tables

Kafka connector v4 supports ingestion and schema evolution for Snowflake-managed Apache Iceberg™ v2 and v3 tables. Use server-side validation (`snowflake.validation=server_side`, the default) to evolve the schema as records arrive.

## Choose how to create the target table

You can use an existing Snowflake-managed Iceberg table or let the connector create a missing table. Iceberg table auto-creation is supported in connector version 4.1.0 and later.

For either setup path, configure:

- `snowflake.validation=server_side`
- `snowflake.streaming.validate.compatibility.with.classic=false`
- `snowflake.enable.schematization=true` to map record fields to columns

For an existing pipeline, review the offset migration settings in [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

### Auto-create an Iceberg table

The connector role needs the required Iceberg table creation privileges and `USAGE` on an external volume that you manage. For details, see [CREATE ICEBERG TABLE access control](/sql-reference/sql/create-iceberg-table-snowflake) and [Configure Snowflake](/user-guide/kafka-connector/setup-snowflake).

Keep all record metadata enabled. For the properties, see [Connector configuration](/user-guide/kafka-connector/setup-kafka).

Add the following properties to your connector configuration. This example creates an Iceberg v3 table using [Snowflake storage](/user-guide/tables-iceberg-internal-storage):

Copy code

```
snowflake.validation=server_side
snowflake.enable.schematization=true
snowflake.streaming.validate.compatibility.with.classic=false
snowflake.autocreate.table.type=iceberg
snowflake.iceberg.create.table.options=EXTERNAL_VOLUME='SNOWFLAKE_MANAGED' ICEBERG_VERSION=3
```

The connector creates the table with a `RECORD_METADATA` column and sets `CATALOG='SNOWFLAKE'`, `ENABLE_SCHEMA_EVOLUTION=TRUE`, and `ERROR_LOGGING=TRUE`. With schematization enabled, supported payload fields become columns through server-side schema evolution.

To use your own external volume, replace the creation options with the appropriate volume and base location:

Copy code

```
snowflake.iceberg.create.table.options=EXTERNAL_VOLUME='my_volume' BASE_LOCATION='kafka/my_table' ICEBERG_VERSION=3
```

Use `snowflake.iceberg.create.table.options` for storage and format options. The connector supplies the catalog, schema evolution, and error logging settings.

For Iceberg v2, the connector creates `RECORD_METADATA` as a structured `OBJECT`. For Iceberg v3, it can use `VARIANT`.

### Use an existing Iceberg table

Create the table beforehand when you need to control column types, precision, or structured columns. Configure server-side validation and map the topic to that table using `snowflake.topic2table.map`. The connector uses an existing table as-is.

To allow schema evolution and retain rejected records for inspection, set `ENABLE_SCHEMA_EVOLUTION=TRUE` and `ERROR_LOGGING=TRUE` on the table before ingestion. Give the ingestion role the required schema-evolution privileges. For example:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET ENABLE_SCHEMA_EVOLUTION = TRUE;
ALTER ICEBERG TABLE my_iceberg_table SET ERROR_LOGGING = TRUE;
```

For table creation and role requirements, see [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table), [Table schema evolution](/user-guide/data-load-schema-evolution), and [CREATE ICEBERG TABLE access control](/sql-reference/sql/create-iceberg-table-snowflake).

If the existing table has a structured `RECORD_METADATA` `OBJECT` column, verify that its field set matches the connector’s expected metadata schema. See [Record metadata](#label-kafkahp-iceberg-record-metadata) for the connector version 4.2.2 definition.

For Iceberg v3, you can define `RECORD_METADATA` as `VARIANT`. For complete table examples, see [Create an Iceberg table for ingestion](/user-guide/kafka-connector/how-the-connector-works#label-kafkahp-connector-with-iceberg-tables-create-iceberg-table).

## Schema evolution

With `snowflake.enable.schematization=true` and `ENABLE_SCHEMA_EVOLUTION=TRUE`, Snowflake infers new top-level fields from incoming values and adds columns as records arrive. Iceberg v2 and v3 support column inference from supported scalar values. On Iceberg v3, nested JSON objects can also become `VARIANT` columns.

Pre-create columns when you need specific types, precision, or structured columns. A registry-backed converter can deserialize Avro records for ingestion.

## Record metadata

For connector version 4.2.2, the structured `RECORD_METADATA` column definition is:

Copy code

```
RECORD_METADATA OBJECT(
    offset LONG,
    topic STRING,
    partition INTEGER,
    key STRING,
    CreateTime BIGINT,
    LogAppendTime BIGINT,
    SnowflakeConnectorPushTime BIGINT,
    headers MAP(VARCHAR, VARCHAR)
)
```

## Limitations

- **Validation mode:** Iceberg ingestion and schema evolution require `snowflake.validation=server_side`.
- **Catalog:** Externally managed Iceberg tables aren’t supported.
- **Schema registry:** Registry schema definitions and compatibility rules don’t drive server-side column creation. Types are inferred from incoming values.
- **Column types:** Evolution doesn’t create structured `ARRAY`, `OBJECT`, or `MAP` columns or widen existing column precision, scale, or length. `VARIANT` requires Iceberg v3. For the complete inference restrictions, including lists, null-only fields, and timestamp precision, see [Table support and schema](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support#label-streaming-schema-evolution).
- **Auto-creation options:** Creation options apply only to missing tables configured with `snowflake.autocreate.table.type=iceberg`. Don’t include `CATALOG`, `ENABLE_SCHEMA_EVOLUTION`, or `ERROR_LOGGING`; the connector supplies them. With `snowflake.enable.schematization=false`, explicitly set `ICEBERG_VERSION=3` because records are stored in `VARIANT` columns.
- **Metadata:** Disabling record metadata fields makes `snowflake.autocreate.table.type=iceberg` configurations invalid. Existing structured `RECORD_METADATA` columns must match the connector’s expected field set.
- **Error routing:** Server-side ingestion errors aren’t routed to a Kafka dead-letter queue. Converter deserialization failures can use the connector’s dead-letter queue configuration.

## Investigate ingestion errors

Use Snowflake error tables to inspect records rejected during ingestion. Use the connector’s dead-letter queue configuration to investigate converter deserialization failures.

For details, see [Validation and error handling](/user-guide/kafka-connector/validation-error-handling) and [Error logging in Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).
