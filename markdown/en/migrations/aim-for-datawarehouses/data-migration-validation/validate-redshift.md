# Validating Data from Amazon Redshift

This page covers Amazon Redshift-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **ODBC connectivity** to Redshift from Worker hosts (standard or IAM auth; same TOML as [Migrating Data from Amazon Redshift](./migrate-redshift)).
- **Live Redshift access** for L2/L3: validation runs SQL against live Redshift even when tables were loaded via UNLOAD to S3.

## Connectivity

Reuse the same `[connections.source.redshift]` Worker TOML as [Migrating Data from Amazon Redshift](./migrate-redshift).

**Standard authentication example:**

Copy code

```
[connections.source.redshift]
username = "myuser"
password = "mypassword"
database = "mydatabase"
host = "my-cluster.abcdef123456.us-west-2.redshift.amazonaws.com"
port = 5439
auth_method = "standard"
```

## Validation behavior

- **After UNLOAD migrations**: Validation still runs **SQL against live Redshift** for source-side metrics and row checks. Ensure the Worker can reach the cluster and that large partition result sets stay within timeout and spool limits.
- **Iceberg targets**: Validation compares whatever is in Snowflake (native or Iceberg). Iceberg targets don’t change L2/L3 SQL on the Redshift side.

For partitioning and `indexColumnList`, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

**Example workflow excerpt:**

Copy code

```
source_platform: redshift
target_database: TARGET_DB
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
tables:
  - fully_qualified_name: snowconvert_demo.ecommerce_raw.customers
    column_names_to_partition_by:
      - customer_id
  - fully_qualified_name: snowconvert_demo.ecommerce_raw.orders
    column_names_to_partition_by:
      - order_id
    indexColumnList:
      - order_id
    validation_configuration:
      row_validation: true
```

## Data type mappings

| Redshift type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| SMALLINT, INTEGER, BIGINT, DECIMAL, REAL, DOUBLE PRECISION | NUMBER / FLOAT | Yes |  |
| BOOLEAN, DATE, TIMESTAMP | BOOLEAN / DATE / TIMESTAMP\_NTZ | Yes |  |
| CHAR, VARCHAR | VARCHAR | Yes |  |
| VARBYTE / BINARY VARYING | BINARY | Yes | Compared as uppercase hexadecimal |
| TIMESTAMPTZ | TIMESTAMP\_TZ | Partial | Row-level validation not yet supported |
| TIME | TIME | Yes |  |
| TIMETZ | TIMESTAMP\_TZ | Partial | Row-level validation not yet supported |
| INTERVALY2M, INTERVALD2S | INTERVAL | Yes | Native `INTERVAL` comparison by default. See [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling). |
| GEOMETRY | GEOMETRY | Yes | Compared as despaced Well-Known Text |
| GEOGRAPHY | GEOGRAPHY | Yes | Compared as despaced Well-Known Text |
| HLLSKETCH |  | No |  |
| SUPER | VARIANT | Yes |  |

Expand

Show lessSee more

## Platform-specific considerations

- **Starting validation**: Ask the agent to generate a validation workflow with the depth you need (schema validation, metrics validation, and row-level validation, per table).

  **Prompt:**

  Copy code

  ```
  Run cloud data validation for my Redshift tables, with schema and metrics validation on all tables and row-level validation on orders
  ```
- For tables migrated via **UNLOAD**, confirm the live Redshift source still reflects the data snapshot you expect to compare.

  **Prompt:**

  Copy code

  ```
  Validate the customers and orders tables that were migrated with UNLOAD extraction
  ```
- **Anti-locking**: No automatic hint is added on Redshift. Set `queryModifiers` only when you need custom source SQL hints. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data validation](./data-validation)
- [Migrating Data from Amazon Redshift](./migrate-redshift)
- [Manual Migration: Data validation](../manual-migration/data-validation)
