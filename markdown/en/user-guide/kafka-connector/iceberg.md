# Load data into Iceberg tables

Kafka connector v4 supports ingestion and server-side schema evolution for Snowflake-managed Apache Iceberg™ v2 and v3 tables. Start with server-side validation (`snowflake.validation=server_side`, the default). Client-side schema evolution can also add columns to a pre-created Iceberg v3 table with a compatible schema; see [Client-side schema evolution](#label-kafkahp-iceberg-client-side-evolution) for the configuration and type restrictions.

## Choose how to create the target table

You can use an existing Snowflake-managed Iceberg table or let the connector create a missing table. Iceberg table auto-creation is supported in connector version 4.1.0 and later.

For the server-side setup paths in this section, configure:

- `snowflake.validation=server_side`
- `snowflake.streaming.validate.compatibility.with.classic=false`
- `snowflake.enable.schematization=true` to map record fields to columns

For an existing pipeline, review the offset migration settings in [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

### Auto-create an Iceberg table

The connector role needs the required Iceberg table creation privileges and `USAGE` on an external volume that you manage. If you use Snowflake storage (`EXTERNAL_VOLUME='SNOWFLAKE_MANAGED'`), you don’t need to create an external volume or grant `USAGE` on one. For details, see [CREATE ICEBERG TABLE access control](/sql-reference/sql/create-iceberg-table-snowflake) and [Configure Snowflake](/user-guide/kafka-connector/setup-snowflake).

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

To allow schema evolution and retain rejected records for inspection, set `ENABLE_SCHEMA_EVOLUTION=TRUE` and `ERROR_LOGGING=TRUE` on the table before ingestion. For example:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET ENABLE_SCHEMA_EVOLUTION = TRUE;
ALTER ICEBERG TABLE my_iceberg_table SET ERROR_LOGGING = TRUE;
```

With server-side validation and the default pipe, the ingestion role doesn’t need an additional `EVOLVE SCHEMA` grant. With a user-defined pipe, the pipe owner’s role needs `EVOLVE SCHEMA` or `OWNERSHIP` on the target table, and the pipe must use `MATCH_BY_COLUMN_NAME` for automatic schema evolution. Client-side evolution has separate role requirements; see [Client-side schema evolution](#label-kafkahp-iceberg-client-side-evolution).

For table creation and role requirements, see [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table), [Table schema evolution](/user-guide/data-load-schema-evolution), and [CREATE ICEBERG TABLE access control](/sql-reference/sql/create-iceberg-table-snowflake).

If the existing table has a structured `RECORD_METADATA` `OBJECT` column, verify that its field set matches the connector’s expected metadata schema. See [Record metadata](#label-kafkahp-iceberg-record-metadata) for the connector version 4.2.2 definition.

For Iceberg v3, you can define `RECORD_METADATA` as `VARIANT`. For complete table examples, see [Create an Iceberg table for ingestion](/user-guide/kafka-connector/how-the-connector-works#label-kafkahp-connector-with-iceberg-tables-create-iceberg-table).

## Schema evolution

### Server-side schema evolution

With `snowflake.validation=server_side`, `snowflake.enable.schematization=true`, and `ENABLE_SCHEMA_EVOLUTION=TRUE`, Snowflake infers new top-level fields from incoming values and adds columns asynchronously. Iceberg v2 and v3 support column inference from supported scalar values. On Iceberg v3, nested JSON objects can also become `VARIANT` columns. Lists and arrays don’t create new columns on either Iceberg version.

Pre-create columns when you need specific types, precision, or structured columns. A registry-backed converter can deserialize records for ingestion, but the registry schema doesn’t drive server-side column creation. For the complete inference restrictions, see [Table support and schema](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support#label-streaming-schema-evolution).

### Client-side schema evolution

Client-side evolution can detect new top-level fields and add columns with `ALTER ICEBERG TABLE` for a pre-created Iceberg v3 table with `RECORD_METADATA VARIANT` and column types supported by the client validator. Use the default pipe and configure:

Copy code

```
snowflake.validation=client_side
snowflake.enable.schematization=true
snowflake.streaming.validate.compatibility.with.classic=false
snowflake.autocreate.table.type=none
snowflake.topic2table.map=my_topic:MY_ICEBERG_TABLE
```

This is a configuration excerpt, not a complete connector configuration. Create the target table with `ENABLE_SCHEMA_EVOLUTION=TRUE` before starting the connector. The connector role needs `EVOLVE SCHEMA` or `OWNERSHIP` on the table, granted directly to that role. The `none` setting prevents table auto-creation; it doesn’t change the existing table’s type. Don’t set `snowflake.autocreate.table.type=iceberg` with `client_side`, because the connector rejects that combination even when the table already exists.

The excerpt disables the classic compatibility check. If you’re migrating an existing pipeline, first review the offset migration and compatibility settings in [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

When a converter supplies a Kafka Connect schema with top-level fields, such as an Avro or Protobuf record schema resolved from a schema registry, the connector maps those declared field types to Snowflake column types. For schemaless JSON, the connector infers column types from values instead. A new field is considered for evolution when it appears in an incoming record, not when its schema is registered.

These mappings don’t reproduce the complete registry schema. For example, floating-point fields map to `FLOAT` or `DOUBLE`, binary fields map to `BINARY`, and the Kafka Connect logical decimal type maps to `VARCHAR`, not `NUMBER` with the declared precision and scale. Structs and maps map to `VARIANT`, not structured `OBJECT` or `MAP` columns. Array fields map to unstructured `ARRAY`, which isn’t a valid new Iceberg column; define typed arrays beforehand and use server-side validation. Neither evolution mode widens existing column types or evolves fields inside structured columns.

Important

The client validator doesn’t support structured `OBJECT`, `ARRAY`, or `MAP` column schemas, including a structured `RECORD_METADATA` column used for Iceberg v2. If validation initialization fails, the connector logs a warning and disables client-side validation for that channel; connector-side schema evolution doesn’t run. Use server-side validation for these schemas.

### Differences between validation modes

The following differences apply to Iceberg targets:

- **Table creation and version:** The client-side path described here requires a pre-created Iceberg v3 table with `RECORD_METADATA VARIANT`. The connector rejects `client_side` with `snowflake.autocreate.table.type=iceberg`. Server-side validation supports Iceberg v2 and v3, including connector-created tables.
- **Pipes:** Client-side validation requires the default pipe. Server-side validation also supports user-defined pipes.
- **Existing complex columns:** Server-side validation can ingest matching values into predefined structured `OBJECT`, `ARRAY`, and `MAP` columns. The client validator doesn’t support these column schemas. This ingestion support doesn’t mean that either mode automatically creates or evolves typed complex columns.
- **New-column types:** Client-side evolution maps converter-provided schema types when available; otherwise it infers from values. Structs and maps become `VARIANT`, arrays map to unstructured `ARRAY` rather than typed Iceberg arrays, and logical decimals map to `VARCHAR`. Server-side evolution infers from serialized values, not registry types; new objects can become `VARIANT` on Iceberg v3, but arrays don’t create columns. Neither mode preserves every registry type or constraint.
- **Privileges:** Client-side evolution requires a direct `EVOLVE SCHEMA` or `OWNERSHIP` grant to the connector role. Server-side evolution through the default pipe doesn’t require an additional `EVOLVE SCHEMA` grant to the ingestion role; user-defined pipes check the pipe owner’s role.
- **Error routing:** Client-detected validation failures can use a Kafka dead-letter queue. Server-side ingestion failures use Snowflake error tables when error logging is enabled and aren’t routed to the dead-letter queue, regardless of the selected validation mode.

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

- **Validation mode:** Iceberg auto-creation with `snowflake.autocreate.table.type=iceberg` requires `server_side`. For the pre-created Iceberg v3 client-side path, see [Client-side schema evolution](#label-kafkahp-iceberg-client-side-evolution).
- **Catalog:** Externally managed Iceberg tables aren’t supported.
- **Schema registry:** Registry schema definitions and compatibility rules don’t drive server-side column creation. Client-side evolution uses the converter-provided Connect schema when available, but its type mappings don’t preserve every registry type or constraint. Pre-create columns when exact types or precision matter.
- **Column types:** Neither evolution mode creates structured `ARRAY`, `OBJECT`, or `MAP` columns or widens existing column precision, scale, or length. `VARIANT` requires Iceberg v3. For server-side inference restrictions, including lists, null-only fields, and timestamp precision, see [Table support and schema](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support#label-streaming-schema-evolution).
- **Auto-creation options:** Creation options apply only to missing tables configured with `snowflake.autocreate.table.type=iceberg`. Don’t include `CATALOG`, `ENABLE_SCHEMA_EVOLUTION`, or `ERROR_LOGGING`; the connector supplies them. With `snowflake.enable.schematization=false`, explicitly set `ICEBERG_VERSION=3` because records are stored in `VARIANT` columns.
- **Metadata:** Disabling record metadata fields makes `snowflake.autocreate.table.type=iceberg` configurations invalid. Existing structured `RECORD_METADATA` columns must match the connector’s expected field set.
- **Error routing:** Server-side ingestion errors aren’t routed to a Kafka dead-letter queue. Converter deserialization failures can use the connector’s dead-letter queue configuration.

## Investigate ingestion errors

Use Snowflake error tables to inspect records rejected during server-side ingestion. Use the connector’s dead-letter queue configuration to investigate converter deserialization failures or client-side validation failures. Server-side ingestion failures aren’t sent to the dead-letter queue, even when `client_side` is selected.

For details, see [Validation and error handling](/user-guide/kafka-connector/validation-error-handling) and [Error logging in Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).
