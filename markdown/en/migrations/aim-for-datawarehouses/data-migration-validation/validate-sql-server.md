# Validating Data from SQL Server

This page covers SQL Server-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **SQL Server connection driver** on Worker hosts. Install the Worker with the `sqlserver` extra to use the preferred `mssql-python` driver without a system ODBC installation. The Worker falls back to `pyodbc` when the native driver isn’t available or the Worker TOML `extra_options` contains an unsupported keyword. See [Migrating Data from SQL Server](./migrate-sql-server#prerequisites).

## Connectivity

Reuse `[connections.source.sqlserver]` Worker TOML from data migration:

Copy code

```
[connections.source.sqlserver]
username = "username"
password = "password"
database = "database_name"
host = "127.0.0.1"
port = 1433
prefer_native_driver = true
set_context_info = true
```

Set `prefer_native_driver = false` to force ODBC. Set `set_context_info = false` if your audit triggers or other applications already use the SQL Server session’s `CONTEXT_INFO` slot.

Set `source_platform: sqlserver` in the validation workflow YAML. For partitioning, row alignment, and tolerance settings that apply to all platforms, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

**Example workflow excerpt:**

Copy code

```
source_platform: sqlserver
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
comparison_configuration:
  tolerance: 0.001
tables:
  - fully_qualified_name: SampleStoreDB.dbo.store_employee
    target_name: target_employee
    column_names_to_partition_by:
      - ID
  - fully_qualified_name: SampleStoreDB.dbo.Sales_Simple
    column_names_to_partition_by:
      - ID
    indexColumnList:
      - ID
    validation_configuration:
      row_validation: true
      max_failed_rows_number: 500
    sourceWhereClause: "is_deleted = 0"
    targetWhereClause: "is_deleted = 0"
```

## Data type mappings

| SQL Server type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| BIT, integers, DECIMAL, MONEY, FLOAT, REAL | NUMBER / FLOAT | Yes |  |
| DATE, TIME, DATETIME types | DATE / TIME / TIMESTAMP | Yes |  |
| CHAR, VARCHAR, NCHAR, NVARCHAR | VARCHAR | Yes |  |
| BINARY, VARBINARY, UNIQUEIDENTIFIER | BINARY / VARCHAR | Yes | UUID compared as an uppercase string |
| TEXT, NTEXT | VARCHAR | Yes | Row-level comparison reads the full value; very large values may hit memory limits |
| XML, SQL\_VARIANT | VARIANT | Partial | Schema-level comparison only |
| GEOGRAPHY | GEOGRAPHY | Yes | Compared as despaced Well-Known Text |
| GEOMETRY | GEOMETRY | Yes | Compared as despaced Well-Known Text |
| VECTOR | VECTOR(*element\_type*, *n*) | Yes | Row-level validation compares element by element |

Expand

Show lessSee more

## Platform-specific considerations

- **Starting validation**: Ask the agent to generate a validation workflow with the depth you need (schema validation, metrics validation, and row-level validation, per table).

  **Prompt:**

  Copy code

  ```
  Run cloud data validation for my SQL Server tables, with schema and metrics validation on all tables and row-level validation on ORDERS
  ```
- **Anti-locking**: Hints are off by default. On busy source tables, set `queryModifiers.objectModifier` to `" WITH (NOLOCK)"` to avoid blocking on source locks, at the cost of dirty reads that can cause false `MISMATCH` results. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

  **Prompt:**

  Copy code

  ```
  Source reads are getting blocked during validation. Can we reduce locking?
  ```

## Related content

- [Data validation](./data-validation)
- [Migrating Data from SQL Server](./migrate-sql-server)
- [Manual Migration: Data validation](../manual-migration/data-validation)
