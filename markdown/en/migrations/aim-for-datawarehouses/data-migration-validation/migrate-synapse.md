# Migrating Data from Azure Synapse Analytics

This page covers Azure Synapse Analytics-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

Synapse support covers both pool types:

- **Dedicated SQL pool** (`azure_synapse`): the default and primary target.
- **Serverless SQL pool** (`azure_synapse_serverless`): supported where your Worker environment allows it.

Both pool types share the same connection block and driver. Set the pool type with `pool_type` in Worker TOML, and set `source_platform` in the workflow to the value that matches your pool.

## Prerequisites

- **Microsoft ODBC Driver 18 for SQL Server** on each Worker host. Synapse uses the same ODBC driver family as SQL Server. Override the driver name with `odbc_driver` in TOML if needed.
- **Azure Blob Storage and pre-created Synapse objects** when using **CETAS** extraction: a `DATABASE SCOPED CREDENTIAL`, an `EXTERNAL DATA SOURCE`, and an `EXTERNAL FILE FORMAT` (Parquet) on Synapse, plus a Snowflake external stage pointing at the same container. See [Using CETAS extraction](#using-cetas-extraction).

## Connectivity and extraction strategies

Synapse supports three extraction strategies:

| Strategy | When to use | Worker requirements |
| --- | --- | --- |
| **`regular`** (default) | Worker pulls partitioned result sets over ODBC and writes Parquet to the internal migration stage. Use for most tables. | Standard `[connections.source.azure_synapse]` TOML only |
| **`cet_as`** (CETAS, recommended for large tables when prerequisites are met) | Synapse writes Parquet to Azure Blob via `CREATE EXTERNAL TABLE AS SELECT`; Snowflake loads from an external stage. | Pre-created Synapse external objects; `cet_as_*` keys in TOML; Snowflake external stage aligned with the blob container |
| **`cloud_direct`** | Worker cursor extraction streamed directly to cloud object storage, skipping local disk and re-upload. | Snowflake external stage |

Expand

Show lessSee more

Synapse does **not** use the SQL Server `bcp` bulk-copy utility. Use `regular` (ODBC) or `cet_as` (server-side export) instead.

### SQL authentication

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

For a serverless SQL pool, set `pool_type = "serverless"` and point `database` at the serverless database (or `master`).

### Microsoft Entra ID (Azure AD) authentication

Set `mode` to a Microsoft Entra ID method. For a service principal, use `azure_ad` with `client_id` and `client_secret`:

Copy code

```
[connections.source.azure_synapse]
host = "your-workspace.sql.azuresynapse.net"
port = 1433
database = "YourDedicatedPoolDb"
mode = "azure_ad"
client_id = "your-application-client-id"
client_secret = "your-client-secret"
pool_type = "dedicated"
encrypt = true
trust_server_certificate = false
```

Supported `mode` values are `sql_auth` (default), `azure_ad` (service principal), `aad_integrated`, `aad_password`, `aad_msi` (managed identity, with an optional `client_id` for a user-assigned identity), and `trusted_connection`.

**Workflow example:**

Copy code

```
source_platform: azure_synapse
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

Tune `columnNamesToPartitionBy` and `partitionSize` for large tables. For a serverless SQL pool, set `source_platform: azure_synapse_serverless`.

### Iceberg targets

Synapse as a source doesn’t prevent **Apache Iceberg™** tables on Snowflake as targets. Set `target.tableType` to `"iceberg"` and supply `target.icebergConfig`. See [Data migration configuration reference](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig).

## Using CETAS extraction

CETAS (`CREATE EXTERNAL TABLE AS SELECT`) is the recommended extraction strategy for large Synapse tables when Azure Blob Storage and a Snowflake external stage are available. Instead of streaming result sets through the Worker over ODBC, Synapse writes Parquet files directly to Azure Blob. The Worker then loads those files into Snowflake from the external stage, skipping re-upload.

### When to use CETAS

Use CETAS when:

- Synapse has a `DATABASE SCOPED CREDENTIAL` with access to an Azure Blob container.
- You can create a Snowflake external stage pointing at the same container.

Use **`regular`** (ODBC) when data volume is small, or when those prerequisites aren’t in place yet.

**Prompt (when prerequisites are met):**

Copy code

```
Set up Azure Synapse data migration using CETAS extraction for my large tables and help me create the Azure storage integration and external stage
```

**Prompt (when Azure Blob and the external stage aren’t ready yet, or volume is small):**

Copy code

```
Set up Azure Synapse data migration for my project with regular extraction and the Worker connection
```

### Setup

**1. Create the Synapse external objects** (ahead of time on the source):

Copy code

```
CREATE DATABASE SCOPED CREDENTIAL MyBlobCredential
  WITH IDENTITY = 'Managed Identity';

CREATE EXTERNAL DATA SOURCE MyBlobDataSource
  WITH (
    LOCATION = 'abfss://mycontainer@myaccount.dfs.core.windows.net',
    CREDENTIAL = MyBlobCredential
  );

CREATE EXTERNAL FILE FORMAT MyParquetFormat
  WITH (FORMAT_TYPE = PARQUET);
```

**2. Create a Snowflake external stage** pointing at the same Azure container:

Copy code

```
CREATE STORAGE INTEGRATION my_azure_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'AZURE'
  ENABLED = TRUE
  AZURE_TENANT_ID = 'your-tenant-id'
  STORAGE_ALLOWED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer/synapse-cetas/');

CREATE OR REPLACE STAGE my_synapse_stage
  URL = 'azure://myaccount.blob.core.windows.net/mycontainer/synapse-cetas/'
  STORAGE_INTEGRATION = my_azure_integration
  FILE_FORMAT = (TYPE = 'PARQUET');
```

**3. Add CETAS settings to Worker TOML.** Reference the external data source and file format by name; CETAS is enabled when both are set:

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
cet_as_external_data_source = "MyBlobDataSource"
cet_as_file_format = "MyParquetFormat"
cet_as_path_prefix = "migration/prod"
```

`cet_as_path_prefix` is an optional folder prefix inside the container. The export schema defaults to `dbo`; override it with `cet_as_table_schema`.

**4. Reference the stage in your workflow YAML:**

Copy code

```
tables:
  - source:
      databaseName: mydb
      schemaName: dbo
      tableName: large_events
    target:
      databaseName: TARGET_DB
      schemaName: dbo
      tableName: large_events
    columnNamesToPartitionBy:
      - event_date
    extraction:
      strategy: cet_as
      externalStage: TARGET_DB.PUBLIC.MY_SYNAPSE_STAGE
```

## Data type mappings

Synapse dedicated SQL pool supports a subset of the SQL Server type system. Types that Synapse doesn’t support are not part of the migration mapping.

| Synapse type | Snowflake target type | Supported for migration | Notes |
| --- | --- | --- | --- |
| TINYINT, SMALLINT, INT, BIGINT | NUMBER | Yes |  |
| DECIMAL(p,s), NUMERIC(p,s) | NUMBER | Yes | Precision and scale carried from the source catalog |
| MONEY, SMALLMONEY | NUMBER(38, 4) | Yes |  |
| FLOAT, REAL | FLOAT | Yes |  |
| BIT | BOOLEAN | Yes |  |
| CHAR(n), VARCHAR(n), NCHAR(n), NVARCHAR(n) | VARCHAR | Yes | Includes `VARCHAR(MAX)` and `NVARCHAR(MAX)` |
| DATE | DATE | Yes |  |
| TIME(n) | TIME | Yes |  |
| DATETIME, DATETIME2(n), SMALLDATETIME | TIMESTAMP\_NTZ | Yes |  |
| DATETIMEOFFSET(n) | TIMESTAMP\_TZ | Yes | Time zone offset preserved |
| BINARY(n), VARBINARY(n) | BINARY | Yes | Includes `VARBINARY(MAX)` |
| UNIQUEIDENTIFIER | VARCHAR | Yes | Stored as a UUID string |
| SYSNAME | VARCHAR | Yes |  |
| XML, SQL\_VARIANT |  | No | Not supported on Synapse dedicated SQL pool |
| GEOGRAPHY, GEOMETRY |  | No | Not supported on Synapse dedicated SQL pool |
| HIERARCHYID |  | No | Not supported on Synapse dedicated SQL pool |
| IMAGE, TEXT, NTEXT |  | No | Not supported on Synapse dedicated SQL pool |

Expand

Show lessSee more

## Platform-specific considerations

- **Dedicated vs. serverless SQL pool**: Set `pool_type` in Worker TOML and match `source_platform` in the workflow (`azure_synapse` or `azure_synapse_serverless`). Metadata queries differ between the two pool types, so keep both settings aligned.
- **CETAS for throughput**: Prefer CETAS for large tables once the Synapse external objects and the Snowflake external stage are in place. Reserve `regular` (ODBC) for small volume or when those prerequisites aren’t set up yet. See [Using CETAS extraction](#using-cetas-extraction).

  **Prompt:**

  Copy code

  ```
  Set up Azure Synapse data migration for my project, including the Worker connection and CETAS extraction
  ```
- **Partitioning**: Tune `columnNamesToPartitionBy` and `partitionSize` for large or uneven tables.

  **Prompt:**

  Copy code

  ```
  Partition the ORDERS table by ORDER_ID for parallel extraction
  ```
- **Encryption**: `encrypt` defaults to enabled with ODBC Driver 18. Set `encrypt` and `trust_server_certificate` explicitly in lab or hardened environments.
- **Anti-locking**: Hints are off by default. On busy source tables, set `queryModifiers.objectModifier` to `" WITH (NOLOCK)"` to avoid blocking on source locks, at the cost of dirty reads. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data migration](./data-migration)
- [Validating Data from Azure Synapse Analytics](./validate-synapse)
- [Manual Migration: Data migration](../manual-migration/data-migration)
