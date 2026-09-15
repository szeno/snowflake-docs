# Migrating Data from SQL Server

This page covers SQL Server-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **SQL Server connection driver**: Install the Worker with the `sqlserver` extra to use Microsoft’s preferred `mssql-python` driver. It bundles native binaries, so unixODBC and `msodbcsql` aren’t required. If `mssql-python` isn’t available or the Worker TOML `extra_options` contains a keyword that it doesn’t accept, the Worker falls back to `pyodbc` and a Microsoft ODBC Driver for SQL Server.
- **`bcp` utility (for faster extraction on custom Worker hosts)**: On [Snowpark Container Services](./deploy-workers) Workers, the unified image installs **`bcp`** automatically (via `mssql-tools18`) and sets **`use_bcp = true`** by default. On custom Worker hosts, install the SQL Server **`bcp`** bulk copy utility and set **`use_bcp = true`** in Worker TOML. See [Download and install the bcp utility](https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-download-install) and [bcp utility](https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-utility).
- **Azure Blob Storage and pre-created SQL Server objects for CETAS**: Create an external data source and a Parquet external file format on the source. Create a Snowflake external stage that points to the same container and prefix. See [Using CETAS extraction](#using-cetas-extraction).
- **Windows integrated security** (optional): set `use_windows_auth = true` on Windows Workers.

## Connectivity and extraction strategies

SQL Server supports the following extraction paths:

| Strategy | When to use | Requirements |
| --- | --- | --- |
| **`regular`** (default) | Worker pulls partitioned results through the native driver or ODBC and writes Parquet to the internal migration stage. | Source connection only |
| **`regular` with BCP** | Worker uses `bcp` to export CSV locally, then uploads it to the internal stage. Use for higher throughput without an external stage. | `use_bcp = true`; `bcp` installed |
| **`cet_as`** | SQL Server writes Parquet to Azure Blob with `CREATE EXTERNAL TABLE AS SELECT` (CETAS); Snowflake loads it from an external stage. | Supported SQL Server SKU, external data source, Parquet file format, and matching Snowflake external stage |
| **`cloud_direct`** | Worker streams cursor results directly to S3 or Azure Blob with PyArrow, skipping local disk and re-upload. | S3 or Azure Blob target connection and matching Snowflake external stage |

Expand

Show lessSee more

On SPCS Workers, **`use_bcp = true`** is the default and **`bcp`** is installed at container start. On custom Worker hosts, install **`bcp`** yourself and opt in with **`use_bcp = true`**. When **`bcp`** is unavailable, the Worker uses the configured database driver.

### SQL authentication

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

`prefer_native_driver` defaults to `true`. Set it to `false` to force the `pyodbc` path. The native path tags sessions with `SET CONTEXT_INFO`; set `set_context_info = false` if your audit triggers or other applications use the session’s `CONTEXT_INFO` slot.

### ODBC fallback and encryption

Copy code

```
[connections.source.sqlserver]
odbc_driver = "ODBC Driver 17 for SQL Server"
prefer_native_driver = false
username = "sa"
password = "mypassword"
database = "mydb"
host = "my-server.example.com"
port = 1433
encrypt = true
trust_server_certificate = false
```

Optional `encrypt` and `trust_server_certificate` apply to both connection paths. When they aren’t set, `mssql-python` and ODBC Driver 18 enable encryption by default, while ODBC Driver 17 and earlier disable it by default.

**Workflow example:**

Copy code

```
tables:
  - source:
      databaseName: MY_DB
      schemaName: dbo
      tableName: orders
    target:
      databaseName: TARGET_DB
      schemaName: dbo
      tableName: orders
    columnNamesToPartitionBy:
      - order_id
```

Tune `columnNamesToPartitionBy` and `partitionSize` for large tables.

### Iceberg targets

SQL Server extracts for Apache Iceberg™ targets must explicitly use `cet_as` or `cloud_direct`. Set `target.tableType` to `"iceberg"`, supply `target.icebergConfig`, and configure a Snowflake external stage for the selected extraction path. See [Iceberg configuration](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig).

## Using CETAS extraction

Use `cet_as` to let a supported SQL Server source write Parquet directly to Azure Blob. Snowflake then loads the files from an external stage that points to the same container and prefix.

### Supported SQL Server platforms

The following table lists CETAS support by SQL Server platform:

| Source platform | CETAS support |
| --- | --- |
| Azure SQL Database (EngineEdition 5) | Not supported. Use `cloud_direct`. |
| Azure SQL Managed Instance (EngineEdition 8) | Supported. |
| SQL Server 2022 or later (EngineEdition 3, major version 16 or later) | Supported. |
| Azure Synapse Analytics | Supported. See [Migrating Data from Azure Synapse Analytics](./migrate-synapse#using-cetas-extraction). |

Expand

Show lessSee more

Important

AIM DMV rejects `cet_as` for unsupported SQL Server editions. Don’t configure CETAS for Azure SQL Database.

### Configure CETAS

Create the external data source and Parquet file format on SQL Server before starting the workflow. Then add their names to the source connection:

Copy code

```
[connections.source.sqlserver]
# Standard SQL Server connection fields
cet_as_external_data_source = "MyBlobDataSource"
cet_as_file_format = "MyParquetFormat"
cet_as_path_prefix = "migration/prod"
# cet_as_table_schema = "dbo"
```

`cet_as_path_prefix` is optional. The export schema defaults to `dbo`; set `cet_as_table_schema` to use another schema.

Reference the matching Snowflake external stage in the workflow:

Copy code

```
defaultTableConfiguration:
  extraction:
    strategy: cet_as
    externalStage: TARGET_DB.PUBLIC.AZURE_LANDING
```

## Using cloud\_direct with Azure Blob

For `cloud_direct`, configure Azure Blob as a Worker target and use a Snowflake external stage that points to the same container and prefix:

Copy code

```
[connections.target.blob]
container_name = "migration-landing"
account_name = "mystorageaccount"
use_default_credential = true
```

Instead of the default credential, set `account_key` or `sas_token` with `account_name`, or set `connection_string`. Don’t put storage credentials in the workflow.

Copy code

```
defaultTableConfiguration:
  extraction:
    strategy: cloud_direct
    externalStage: TARGET_DB.PUBLIC.AZURE_LANDING
```

## Data type mappings

| SQL Server type | Snowflake target type | Supported for migration | Notes |
| --- | --- | --- | --- |
| BIT, TINYINT, SMALLINT, INT, BIGINT | NUMBER | Yes |  |
| DECIMAL(p,s), NUMERIC(p,s) | NUMBER | Yes | Precision/scale expanded: NUMBER(p+2, s+4) |
| MONEY, SMALLMONEY | NUMBER | Yes |  |
| FLOAT, REAL | FLOAT | Yes |  |
| DATE | DATE | Yes |  |
| TIME(n) | TIME | Yes |  |
| DATETIME, DATETIME2(n), SMALLDATETIME | TIMESTAMP\_NTZ | Yes | NULL `DATETIME` values may appear as `1970-01-01 00:00:00` on the target when BCP extraction is used |
| DATETIMEOFFSET(n) | TIMESTAMP\_TZ | Yes |  |
| CHAR(n), VARCHAR(n), NCHAR(n), NVARCHAR(n) | VARCHAR | Yes |  |
| BINARY(n), VARBINARY(n) | BINARY | Yes |  |
| UNIQUEIDENTIFIER | VARCHAR | Yes | Stored as an uppercase UUID string |
| SYSNAME | VARCHAR | Yes |  |
| TEXT, NTEXT | VARCHAR | Yes |  |
| IMAGE |  | No |  |
| XML, SQL\_VARIANT | VARIANT | Yes |  |
| HIERARCHYID | VARCHAR(4000) | Yes | Stored as its hierarchy path string |
| ROWVERSION, TIMESTAMP | BINARY(8) | Yes | SQL Server TIMESTAMP is a synonym for ROWVERSION, not a datetime |
| GEOGRAPHY | GEOGRAPHY | Yes | Extracted as Well-Known Text |
| GEOMETRY | GEOMETRY | Yes | Extracted as Well-Known Text |
| VECTOR | VECTOR(*element\_type*, *n*) | Yes |  |

Expand

Show lessSee more

## Platform-specific considerations

- **BCP for throughput**: On SPCS Workers, BCP is enabled by default. On custom Worker hosts, set `use_bcp = true` when **`bcp`** is installed. BCP applies to **migration only**; validation reads the source through `mssql-python` by default and falls back to ODBC when necessary.

  **Prompt:**

  Copy code

  ```
  Set up SQL Server data migration for my project, including the Worker connection and BCP extraction
  ```
- **Partitioning**: Tune `columnNamesToPartitionBy` and `partitionSize` for large or uneven tables.

  **Prompt:**

  Copy code

  ```
  Partition the ORDERS table by ORDER_ID for parallel extraction
  ```
- **Encryption**: Set `encrypt` and `trust_server_certificate` explicitly in lab or hardened environments.
- **Driver diagnostics**: `scai data doctor` reports `mssql-python` as the preferred driver. An ODBC-only setup produces a warning instead of a hard failure.
- **Anti-locking**: Hints are off by default. On busy source tables, set `queryModifiers.objectModifier` to `" WITH (NOLOCK)"` to avoid blocking on source locks, at the cost of dirty reads. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data migration](./data-migration)
- [Validating Data from SQL Server](./validate-sql-server)
- [Manual Migration: Data migration](../manual-migration/data-migration)
