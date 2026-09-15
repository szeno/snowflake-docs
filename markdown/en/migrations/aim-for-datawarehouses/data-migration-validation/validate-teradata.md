# Validating Data from Teradata

This page covers Teradata-specific setup for [Data validation](./data-validation). For workflow and Worker field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference). For SnowConvert AI CLI commands, see [Manual Migration: Data validation](../manual-migration/data-validation).

## Prerequisites

Before you validate Teradata data, make sure the following are in place:

- **Teradata connectivity on Workers**: Same as data migration. Prefer **`teradatasql`** when available; otherwise set **`odbc_driver`** to the exact registered driver name. Optional **`dbc_name`**, port **1025** by default, optional **`authentication`** (TD2, LDAP, KRB5).
- **HASH\_MD5 UDF (required for L3 row fingerprinting)**: See [HASH\_MD5 UDF](#hash_md5-udf) below.
- **No WRITE\_NOS or TPT for validation-only Workers**: Validation reads the source over SQL (metrics and row-level validation). You don’t need **`write_nos_*`** TOML or **`tbuild`** on a host solely running validation, unless the same Worker also executes migration **`tpt`** or **`write_nos`** tasks.

## HASH\_MD5 UDF

Teradata does not provide a built-in SQL function that Cloud Data Validation can use for row fingerprinting. Instead, validation generates SQL that calls a custom user-defined function named **`HASH_MD5`**.

### What HASH\_MD5 does

**`HASH_MD5`** is a C language UDF you install on Teradata. Row-level validation uses it to fingerprint each source row and compares the result against a matching hash on the Snowflake target. Schema and metrics validation don’t use it.

### Where the UDF must be installed

| Requirement | Detail |
| --- | --- |
| **Function name** | Must be exactly **`HASH_MD5`** |
| **Database** | Same database as **`[connections.source.teradata].database`** in the Worker TOML |
| **Name qualification** | Generated SQL calls **`HASH_MD5(...)`** without a database prefix |
| **Multiple source databases** | Install the UDF in **each** Teradata database used as a Worker source database |

Expand

Show lessSee more

When the Worker connects, Teradata uses the **`database`** value in Worker TOML as the session default. Unqualified **`HASH_MD5`** resolves only in that database. Pointing the Worker at a UDF in a different database is **not supported**.

### How to install HASH\_MD5 on Teradata

Installation is a **one-time DBA task** on your Teradata system:

1. Obtain the canonical **`HASH_MD5`** install script from your **Snowflake migration support** or **SnowConvert deployment** channel. The public documentation repository does not ship the UDF DDL.
2. Run the script as a Teradata user with privileges to **`CREATE FUNCTION`** (or **`REPLACE FUNCTION`**) in each database listed in your Worker TOML **`database`** field.
3. Grant **`EXECUTE FUNCTION`** on **`HASH_MD5`** to the Teradata user account the validation Worker uses to connect.

If you validate tables in more than one Teradata database, repeat installation in every database the Workers connect to.

### Verify HASH\_MD5 before running L3 validation

Connect as the Worker user (or any user with **`EXECUTE FUNCTION`** on the UDF) and run:

Copy code

```
DATABASE your_validation_db;
SELECT HASH_MD5('test');
```

A successful call returns an MD5 hex string. If the call fails, the UDF is likely missing from the session’s default database. Reinstall it there and retry.

Optional catalog check (replace the database name):

Copy code

```
SELECT DatabaseName, FunctionName
FROM DBC.FunctionsV
WHERE FunctionName = 'HASH_MD5'
  AND DatabaseName = 'YOUR_VALIDATION_DB';
```

**Prompt:**

Copy code

```
Help me verify that HASH_MD5 is installed in the Teradata database my Worker connects to
```

## Connectivity

Validation Workers reuse the same `[connections.source.teradata]` TOML as data migration.

**Worker TOML example:**

Copy code

```
[connections.source.teradata]
host = "teradata.example.com"
port = 1025
database = "MY_DB"
username = "your_username"
password = "your_password"
# L3 prerequisite: install HASH_MD5 in MY_DB (see HASH_MD5 UDF section)
```

| Topic | Data migration (load) | Cloud Data Validation |
| --- | --- | --- |
| **Purpose** | Move data with `regular`, `write_nos`, or `tpt` | Compare live Teradata tables/views to Snowflake with schema, metrics, and row-level validation |
| **`write_nos_*` TOML** | Required when strategy is `write_nos` | **Not** required for validation-only workloads |
| **`tbuild` / TTU** | Required for `tpt` migration tasks | **Not** required for validation-only Workers |

Expand

Show lessSee more

## Validation levels and Teradata behavior

**Schema validation on views:** Teradata views support the same L1 comparison as tables, including column name, data type, precision, scale, length, nullability, and ordinal position. AIM DMV retrieves view metadata from `DBC.ColumnsQV`.

If Queryable View Column Information (QVCI) isn’t available, AIM DMV falls back to `HELP COLUMN` and compares only column names and data types. This fallback occurs when a `DBC.ColumnsQV` query returns error `9719`, is denied, or yields incomplete metadata. The workflow logs a `WARNING` with `EVALUATION_CRITERIA="QVCI_METADATA"`.

Grant the Worker source user `SELECT` on `DBC.ColumnsQV` to enable full view metadata. See [Teradata source privileges](./required-privileges#teradata).

**Metrics validation:** Full support for tables. Full support for views.

**Row validation:** Requires the [**HASH\_MD5 UDF**](#hash_md5-udf). Use **`indexColumnList`** for row alignment. Set **`column_names_to_partition_by`** and **`target_partition_size_mb`** or **`target_partition_size_rows`** on wide tables.

**Example validation workflow excerpt:**

Copy code

```
source_platform: teradata
target_platform: Snowflake
target_database: MY_DATABASE
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 1000
  early_stopping: true
comparison_configuration:
  tolerance: 0.001
tables:
  - fully_qualified_name: my_database.sales_transactions
    target_schema: PUBLIC
    target_name: SALES_TRANSACTIONS
    indexColumnList:
      - TRANSACTION_ID
    column_names_to_partition_by:
      - TRANSACTION_ID
    target_partition_size_mb: 200
views:
  - fully_qualified_name: my_database.sales_summary_view
    target_schema: PUBLIC
    target_name: SALES_SUMMARY_VIEW
    indexColumnList:
      - ID
    target_partition_size_rows: 50000
```

## Data type mappings

During validation comparisons, these Teradata source types map automatically to Snowflake types:

| Teradata type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| BYTEINT, SMALLINT, INTEGER, BIGINT | NUMBER | Yes |  |
| NUMERIC, NUMBER, DECIMAL | NUMBER | Yes |  |
| FLOAT, REAL, DOUBLE PRECISION | FLOAT | Yes |  |
| DATE | DATE | Yes |  |
| TIME | TIME | Yes |  |
| TIME WITH TIME ZONE | TIME | Yes |  |
| TIMESTAMP | TIMESTAMP\_NTZ | Yes |  |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ | Yes |  |
| CHAR, VARCHAR | VARCHAR | Yes |  |
| BOOLEAN |  | No |  |
| CLOB |  | No |  |
| BYTE, VARBYTE, BLOB |  | No |  |
| JSON, XML |  | No |  |
| ST\_GEOMETRY |  | No |  |
| INTERVAL types | INTERVAL | Yes | Native `INTERVAL` comparison by default. See [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling). |
| PERIOD types |  | No |  |
| ARRAY |  | No |  |
| LONG VARCHAR, GRAPHIC, VARGRAPHIC, UNICODE types | VARCHAR | Partial | Row-level and metrics validation not supported |

Expand

Show lessSee more

Use `comparison_configuration.type_mapping_file_path` to supply a custom mapping file when needed.

## Platform-specific considerations

- **Starting validation**: Ask the agent to generate a validation workflow with the depth you need (schema validation, metrics validation, and row-level validation, per table).

  **Prompt:**

  Copy code

  ```
  Run cloud data validation for my Teradata tables, with schema and metrics validation on all tables and row-level validation on sales_transactions
  ```
- **After `tpt` or `write_nos` migrations**: Validation still reads the source over SQL. Ensure Teradata objects you validate are reachable and match the validation workflow names.
- **L3 cost control**: Enable **`early_stopping`** and tune **`max_failed_rows_number`** per table to avoid scanning partitions on a table that has clearly failed.
- **Partitioning**: Use **`column_names_to_partition_by`** so wide tables don’t time out on metrics and row-level validation scans.

  **Prompt:**

  Copy code

  ```
  Partition the sales_transactions table by TRANSACTION_ID for validation
  ```
- **Anti-locking**: AIM DMV adds `LOCKING ROW FOR ACCESS` automatically on every Teradata source scan. No configuration is required. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data validation](./data-validation)
- [Data validation configuration reference](../manual-migration/data-validation-configuration-reference)
- [Migrating Data from Teradata](./migrate-teradata)
- [Manual Migration: Data validation](../manual-migration/data-validation)
