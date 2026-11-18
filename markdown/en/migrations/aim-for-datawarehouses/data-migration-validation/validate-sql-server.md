# Validating Data from SQL Server

This page covers SQL Server-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **SQL Server connection driver** on Worker hosts. Install the Worker with the `sqlserver` extra to use the preferred `mssql-python` driver without a system ODBC installation. The Worker falls back to `pyodbc` when the native driver isn’t available or the Worker TOML `extra_options` contains an unsupported keyword. See [Migrating Data from SQL Server](./migrate-sql-server#prerequisites).
- **L3 object storage (Recommended)**: Use **CETAS** (`extraction.strategy: cet_as`) so signatures land on **Azure Blob** (same CETAS objects and Snowflake external stage as [Migrating Data from SQL Server](./migrate-sql-server#using-cetas-extraction)). CETAS requires SQL Server 2022 or later or Azure SQL Managed Instance, and Microsoft ODBC Driver 18 for SQL Server on the Worker host. See [Object storage backends](../manual-migration/data-validation-configuration-reference#l3-extraction-object-storage) and [Azure Blob Storage](./required-privileges#azure-blob-storage).

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
set_context_info = true
```

Set `set_context_info = false` if your audit triggers or other applications already use the SQL Server session’s `CONTEXT_INFO` slot.

For Windows authentication, use the same source connection as data migration. On Snowpark Container Services that connection needs a Kerberos keytab. See [Windows authentication](./migrate-sql-server#windows-authentication).

Set `sourcePlatform: sqlserver` in the validation workflow YAML. For partitioning, row alignment, and tolerance settings that apply to all platforms, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

**Example workflow excerpt:**

Copy code

```
sourcePlatform: sqlserver
validationConfiguration:
  schemaValidation: true
  metricsValidation: true
  rowValidation: false
comparisonConfiguration:
  tolerance: 0.001
tables:
  - fullyQualifiedName: SampleStoreDB.dbo.store_employee
    targetName: target_employee
    columnNamesToPartitionBy:
      - ID
  - fullyQualifiedName: SampleStoreDB.dbo.Sales_Simple
    columnNamesToPartitionBy:
      - ID
    indexColumnList:
      - ID
    validationConfiguration:
      rowValidation: true
      maxFailedRowsNumber: 500
    sourceWhereClause: "is_deleted = 0"
    targetWhereClause: "is_deleted = 0"
```

## BCP and validation

BCP speeds up data migration only. With the default `regular` extraction strategy, validation reads the source through the SQL Server driver at every level, whatever `use_bcp` is set to, so you can keep one Worker TOML for both migration and validation. For faster row validation (L3) on large tables, set `validationConfiguration.extraction.strategy` to `cet_as` (SQL Server 2022 or later, or Azure SQL Managed Instance) or `cloud_direct` (for example, on Azure SQL Database), and set `validationConfiguration.extraction.externalStage` to the matching Snowflake external stage. See [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction).

Copy code

```
validationConfiguration:
  rowValidation: true
  extraction:
    strategy: cet_as
    externalStage: TARGET_DB.PUBLIC.AZURE_LANDING
```

## Data type mappings

| SQL Server type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| BIT | BOOLEAN | Yes |  |
| Integers, DECIMAL, NUMERIC, FLOAT, REAL | NUMBER / FLOAT | Yes |  |
| MONEY, SMALLMONEY | NUMBER(38, 4) | Yes |  |
| DATE, TIME, DATETIME, DATETIME2, SMALLDATETIME | DATE / TIME / TIMESTAMP\_NTZ | Yes |  |
| DATETIMEOFFSET | TIMESTAMP\_TZ | Yes |  |
| CHAR, VARCHAR, NCHAR, NVARCHAR | VARCHAR | Yes |  |
| BINARY, VARBINARY, UNIQUEIDENTIFIER | BINARY / VARCHAR | Yes | UUID compared as an uppercase string |
| ROWVERSION, TIMESTAMP | BINARY(8) | Yes | SQL Server TIMESTAMP is a synonym for ROWVERSION, not a datetime. L3 compares the value as hexadecimal |
| HIERARCHYID | VARCHAR(4000) | Yes | Compared as its hierarchy path string |
| TEXT, NTEXT, IMAGE | VARCHAR / BINARY | Yes | L1 and L2 check these columns. L3 leaves them out unless `includeLobColumnsInRowValidation` is `true`. See [LOB columns in L3](../manual-migration/data-validation-configuration-reference#lob-columns-in-l3) |
| XML, SQL\_VARIANT | VARIANT | Yes | L2 compares NULL counts. L3 compares the value as text |
| JSON | VARIANT | Yes | SQL Server 2025 or later. L3 compares the JSON text |
| GEOGRAPHY | GEOGRAPHY | Yes | Compared as despaced Well-Known Text |
| GEOMETRY | GEOMETRY | Yes | Compared as despaced Well-Known Text |
| VECTOR | VECTOR(*element\_type*, *n*) | Yes | Row-level validation compares element by element |

Expand

Show lessSee more

Note

Metrics validation (L2) summarizes each column with aggregates such as NULL count, min, and max; it doesn’t compare the values themselves. Distinct count is added only when you opt in with [`includeCountDistinct`](../manual-migration/data-validation-configuration-reference#l2-distinct-count). For `VECTOR`, `GEOGRAPHY`, `GEOMETRY`, `UNIQUEIDENTIFIER`, `XML`, and `SQL_VARIANT`, a value change that preserves those aggregates (for example, editing a GUID or an XML document without changing the column’s NULL count) passes L2 without a mismatch. To compare the actual values of these columns, enable [row validation (L3)](./data-validation#row-validation-l3).

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
- [Apache Iceberg™ tables (spec v2 and v3)](./iceberg)
- [Manual Migration: Data validation](../manual-migration/data-validation)
