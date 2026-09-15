# Validating Data from Oracle

This page covers Oracle-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **Oracle Instant Client** and ODBC driver on Workers (same as [Migrating Data from Oracle](./migrate-oracle)).

## Connectivity

Reuse `[connections.source.oracle]` Worker TOML from data migration:

Copy code

```
[connections.source.oracle]
oracle_connection_mode = "basic"
username = "scott"
password = "your_password"
database = "ORCL"
host = "db.example.com"
port = "1521"
```

Set `source_platform: oracle` in the validation workflow YAML.

For partitioning, `indexColumnList`, and other workflow settings shared across platforms, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

**Example workflow excerpt:**

Copy code

```
source_platform: oracle
target_database: TARGET_DB
schema_mappings:
  HR: HR
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
tables:
  - fully_qualified_name: HR.EMPLOYEES
    column_names_to_partition_by:
      - EMPLOYEE_ID
  - fully_qualified_name: HR.DEPARTMENTS
    column_names_to_partition_by:
      - DEPARTMENT_ID
    indexColumnList:
      - DEPARTMENT_ID
    validation_configuration:
      row_validation: true
```

## Data type mappings

| Oracle type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| NUMBER, FLOAT, integers, DECIMAL | NUMBER / FLOAT | Yes |  |
| VARCHAR2, NVARCHAR2, VARCHAR | VARCHAR | Yes | Oracle treats empty string as NULL |
| CHAR, NCHAR | VARCHAR | Yes | Trailing spaces ignored in comparison |
| CLOB, NCLOB | VARCHAR | Partial | Metrics comparison not supported |
| LONG | VARCHAR | Partial | Metrics and row comparison not supported |
| RAW, BLOB | BINARY | Yes | Row comparison covers the first 4000 bytes |
| DATE, TIMESTAMP types | TIMESTAMP\_NTZ / TIMESTAMP\_TZ | Yes |  |
| TIMESTAMP WITH LOCAL TIME ZONE | TIMESTAMP\_LTZ | Partial | Row comparison not supported |
| INTERVAL types | INTERVAL | Yes | Native `INTERVAL` comparison by default; known limitation comparing interval sign. See [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling). |
| XMLTYPE | VARIANT | Partial | Schema-level comparison only |
| JSON | VARIANT | Yes | Requires Oracle 21c or later |
| BOOLEAN | BOOLEAN | Yes | Requires Oracle 23ai or later |
| VECTOR | VECTOR(*element\_type*, *n*) | Yes | Requires Oracle 23ai or later. Row-level validation compares element by element |
| SDO\_GEOMETRY | GEOGRAPHY | Yes | Requires Oracle Spatial. Compared as WKT, truncated at 4000 characters in row-level validation |

Expand

Show lessSee more

## Platform-specific considerations

- **Starting validation**: Ask the agent to generate a validation workflow with the depth you need (schema validation, metrics validation, and row-level validation, per table).

  **Prompt:**

  Copy code

  ```
  Run cloud data validation for my Oracle tables, with schema and metrics validation on all tables and row-level validation on EMPLOYEES
  ```
- **Performance hints**: AIM DMV adds an automatic `PARALLEL` optimizer hint on large Oracle tables to speed up scans. Override with `queryModifiers.selectModifier`, or set `selectModifier` to `"NONE"` to disable. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data validation](./data-validation)
- [Migrating Data from Oracle](./migrate-oracle)
- [Manual Migration: Data validation](../manual-migration/data-validation)
