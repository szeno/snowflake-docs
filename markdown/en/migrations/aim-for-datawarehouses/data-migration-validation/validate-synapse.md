# Validating Data from Azure Synapse Analytics

This page covers Azure Synapse Analytics-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

Validation supports both the **dedicated SQL pool** (`azure_synapse`) and the **serverless SQL pool** (`azure_synapse_serverless`). Set `source_platform` to the value that matches the pool you migrated from.

## Prerequisites

- **Microsoft ODBC Driver 18 for SQL Server** on Worker hosts (same guidance as [Migrating Data from Azure Synapse Analytics](./migrate-synapse)).
- **Live Synapse access** for metrics and row-level validation: validation runs SQL against live Synapse even when tables were migrated via CETAS export to Azure Blob.

## Connectivity

Reuse the same `[connections.source.azure_synapse]` Worker TOML as [Migrating Data from Azure Synapse Analytics](./migrate-synapse):

Copy code

```
[connections.source.azure_synapse]
host = "your-workspace.sql.azuresynapse.net"
port = 1433
database = "YourDedicatedPoolDb"
username = "sqladminuser"
password = "YOUR_PASSWORD"
mode = "sql_auth"
pool_type = "dedicated"
encrypt = true
trust_server_certificate = true
```

Set `source_platform: azure_synapse` (or `azure_synapse_serverless`) in the validation workflow YAML. For partitioning, row alignment, and tolerance settings that apply to all platforms, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Validation behavior

- **After CETAS migrations**: Validation still runs **SQL against live Synapse** for source-side metrics and row checks. Ensure the Worker can reach the Synapse endpoint and that large partition result sets stay within timeout limits.
- **Serverless SQL pool**: Metadata and row-count queries differ from the dedicated pool because the serverless pool doesn’t expose the dedicated pool’s system statistics. Set `source_platform: azure_synapse_serverless` so the correct queries are used.
- **Iceberg targets**: Validation compares whatever is in Snowflake (native or Iceberg). Iceberg targets don’t change source-side validation SQL on Synapse.

**Example workflow excerpt:**

Copy code

```
source_platform: azure_synapse
target_database: TARGET_DB
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
comparison_configuration:
  tolerance: 0.001
tables:
  - fully_qualified_name: MY_DB.dbo.store_employee
    target_name: target_employee
    column_names_to_partition_by:
      - ID
  - fully_qualified_name: MY_DB.dbo.sales
    column_names_to_partition_by:
      - ID
    indexColumnList:
      - ID
    validation_configuration:
      row_validation: true
      max_failed_rows_number: 500
```

## Data type mappings

| Synapse type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| TINYINT, SMALLINT, INT, BIGINT | NUMBER | Yes |  |
| DECIMAL, NUMERIC, MONEY, SMALLMONEY | NUMBER | Yes |  |
| FLOAT, REAL | FLOAT | Yes |  |
| BIT | BOOLEAN | Yes |  |
| CHAR, VARCHAR, NCHAR, NVARCHAR | VARCHAR | Yes |  |
| DATE | DATE | Yes |  |
| TIME | TIME | Yes |  |
| DATETIME, DATETIME2, SMALLDATETIME | TIMESTAMP\_NTZ | Yes |  |
| DATETIMEOFFSET | TIMESTAMP\_TZ | Yes | Time zone offset preserved |
| BINARY, VARBINARY | BINARY | Yes | Compared as uppercase hexadecimal |
| UNIQUEIDENTIFIER | VARCHAR | Yes | Compared as a UUID string |
| SYSNAME | VARCHAR | Yes |  |
| XML, SQL\_VARIANT, GEOGRAPHY, GEOMETRY, HIERARCHYID, IMAGE, TEXT, NTEXT |  | No | Not supported on Synapse dedicated SQL pool |

Expand

Show lessSee more

## Platform-specific considerations

- **Starting validation**: Ask the agent to generate a validation workflow with the depth you need (schema validation, metrics validation, and row-level validation, per table).

  **Prompt:**

  Copy code

  ```
  Run cloud data validation for my Azure Synapse tables, with schema and metrics validation on all tables and row-level validation on ORDERS
  ```
- For tables migrated via **CETAS**, confirm the live Synapse source still reflects the data snapshot you expect to compare.

  **Prompt:**

  Copy code

  ```
  Validate the store_employee and sales tables that were migrated from Azure Synapse
  ```
- **Anti-locking**: Hints are off by default. On busy source tables, set `queryModifiers.objectModifier` to `" WITH (NOLOCK)"` to avoid blocking on source locks, at the cost of dirty reads that can cause false `MISMATCH` results. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

  **Prompt:**

  Copy code

  ```
  Source reads are getting blocked during validation. Can we reduce locking?
  ```

## Related content

- [Data validation](./data-validation)
- [Migrating Data from Azure Synapse Analytics](./migrate-synapse)
- [Manual Migration: Data validation](../manual-migration/data-validation)
