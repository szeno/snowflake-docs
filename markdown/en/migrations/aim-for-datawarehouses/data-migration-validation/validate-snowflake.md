# Validating Data from Snowflake

This page covers Snowflake-to-Snowflake setup for [Data validation](./data-validation). Use this path when both sides of the comparison are Snowflake objects, for example after copying data between databases or schemas in the same account, or after converting native tables to Iceberg. For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **Orchestrator only**: Snowflake-to-Snowflake cloud validation runs **in-warehouse**. The Orchestrator issues comparison SQL on a single Snowflake connection. You don’t need Workers or source ODBC drivers for this path.
- **Same account connection**: Source and target objects must be reachable with the Orchestrator’s Snowflake connection (typically different databases or schemas in the same account). Dual-connection (cross-account) validation isn’t the in-warehouse cloud lane.
- **SELECT on both sides**: The connection role needs `SELECT` on the source and target objects, plus the usual privileges to operate `SNOWCONVERT_AI`. See [Required privileges](./required-privileges).

## Connectivity

You don’t add a `[connections.source.*]` Worker TOML section. Set `SNOWFLAKE_CONNECTION_NAME` (or `--connection` / `--connection-name`) to a named Snowflake CLI connection that can query both the source and target objects.

Set `source_platform: snowflake` in the validation workflow YAML. Use three-part Snowflake names (`DATABASE.SCHEMA.OBJECT`) for `fully_qualified_name`, and map databases or schemas when the target names differ.

**Example workflow excerpt:**

Copy code

```
source_platform: snowflake
target_database: TARGET_DB
database_mappings:
  SOURCE_DB: TARGET_DB
schema_mappings:
  SRC: PUBLIC
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
tables:
  - fully_qualified_name: SOURCE_DB.SRC.CUSTOMERS
    column_names_to_partition_by:
      - CUSTOMER_ID
  - fully_qualified_name: SOURCE_DB.SRC.ORDERS
    column_names_to_partition_by:
      - ORDER_ID
    indexColumnList:
      - ORDER_ID
    validation_configuration:
      row_validation: true
```

## Validation behavior

Snowflake-to-Snowflake cloud validation uses a different compute path from other sources:

| Aspect | Other sources | Snowflake-to-Snowflake |
| --- | --- | --- |
| Compute | Workers extract, stage files, and load results | The Orchestrator runs comparison SQL inside Snowflake |
| Workers | Required | Not required |
| Result ingestion | Snowpipe (default) or `COPY INTO` | Direct writes; `use_snowpipe_for_results` is ignored and treated as off |
| L3 row validation | MD5 row hashes on Workers, then cell drill-down | SQL multiplicity checks and `MINUS` set-difference in the warehouse, with SQL cell detail when index columns are present |

Expand

Show lessSee more

L1 still compares `INFORMATION_SCHEMA` metadata. L2 still compares per-column metrics (min, max, average, and similar). Numeric comparisons honor `comparison_configuration.tolerance`.

When the unfiltered target table has zero rows, L1 still runs if enabled; L2 and L3 aren’t scheduled for that table.

## Data type mappings

Source and target are both Snowflake types. Synonyms (for example `INT` and `INTEGER`) resolve to the same comparison type.

| Snowflake type | Supported for validation | Notes |
| --- | --- | --- |
| NUMBER, DECIMAL, NUMERIC, INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT | Yes |  |
| FLOAT, FLOAT4, FLOAT8, DOUBLE, DOUBLE PRECISION, REAL | Yes |  |
| BOOLEAN | Yes |  |
| VARCHAR, STRING, TEXT, CHAR, CHARACTER | Yes |  |
| BINARY, VARBINARY | Yes |  |
| DATE, DATETIME, TIME, TIMESTAMP, TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, TIMESTAMP\_TZ | Yes |  |
| VARIANT, OBJECT, ARRAY | Yes |  |
| VECTOR | Yes |  |
| GEOGRAPHY, GEOMETRY | Yes |  |
| INTERVAL | Yes | Native `INTERVAL` comparison by default. See [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling). |

Expand

Show lessSee more

## Platform-specific considerations

- **Starting validation**: Set `source_platform: snowflake` in the workflow YAML, then submit with `scai data validate create-workflow` or `scai data validate start`. You only need a running Orchestrator; you can omit starting a Worker.

## Related content

- [Data validation](./data-validation)
- [Manual Migration: Data validation](../manual-migration/data-validation)
