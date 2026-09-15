# Migrating Data from Teradata

This page covers Teradata-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference). For SnowConvert AI CLI commands, see [Manual Migration: Data migration](../manual-migration/data-migration).

## Prerequisites

Before you migrate data from Teradata, make sure the following are in place:

- **Teradata connectivity on Workers**: Install **`teradatasql`** (preferred, pure Python) or register a Teradata ODBC driver on each Worker host. Default gateway port is **1025** unless your site uses another.
- **Teradata Tools and Utilities (for `tpt`)**: If you use the **`tpt`** extraction strategy, **`tbuild`** must be on `PATH` or set via **`TPT_TBUILD_EXECUTABLE`**.
- **NOS / WRITE\_NOS (for `write_nos`)**: Teradata **NOS / WRITE\_NOS** must be enabled on the source system, and you need cloud storage credentials aligned with your Snowflake external stage.
- **Snowflake external stage (for `write_nos`)**: Create an external stage whose URL matches the bucket or container Teradata writes to.

## Connectivity and extraction strategies

Teradata supports three extraction strategies. Pick **one** per table (or inherit from `defaultTableConfiguration.extraction`).

| Strategy | Workflow `extraction.externalStage` | Snowflake stage | Worker requirements |
| --- | --- | --- | --- |
| **`write_nos`** (recommended when prerequisites are met) | **Required** (same bucket/container Teradata writes to) | **External** stage | `write_nos_*` TOML fields; Teradata NOS enabled. Use for **all** tables once cloud storage and the external stage are set up. |
| **`regular`** | Omit | Internal migration stage | `teradatasql` or Teradata ODBC; optional `odbc_driver`, `dbc_name`, `authentication`. Use when volume is genuinely small, or when WRITE\_NOS prerequisites aren’t available yet. |
| **`tpt`** | Omit | Internal migration stage (same as `regular`) | **`tbuild`** on `PATH` or **`TPT_TBUILD_EXECUTABLE`**. Worker-side bulk export when WRITE\_NOS isn’t an option. |

Expand

Show lessSee more

### `regular`: partitioned SQL extraction

The Worker runs **partitioned `SELECT`** streams through **`teradatasql`** (preferred) or **`pyodbc`** with a registered Teradata ODBC driver. Data is converted to Parquet and uploaded to the Snowflake internal migration stage.

**Authentication:** TD2 (default), LDAP, or KRB5 via optional `authentication` in Worker TOML.

**Worker TOML example (standard authentication):**

Copy code

```
[connections.source.teradata]
host = "teradata.example.com"
port = 1025
database = "MY_DB"
username = "your_username"
password = "your_password"
# odbc_driver = "Teradata Database ODBC Driver 17.20"  # when not using teradatasql
# dbc_name = "TDPID_ALIAS"
# authentication = "LDAP"
```

**Workflow YAML (default: omit `extraction` block):**

Copy code

```
tables:
  - source:
      databaseName: MY_DB
      schemaName: sales
      tableName: orders
    target:
      databaseName: TARGET_DB
      schemaName: sales
      tableName: orders
    columnNamesToPartitionBy:
      - order_id
```

**Prompt (when cloud storage isn’t ready yet, or volume is genuinely small):**

Copy code

```
Set up Teradata data migration for my project with regular extraction, including the Worker connection
```

### `write_nos`: server-side export to object storage

Teradata writes Parquet directly to **S3, Azure Blob, or GCS**. Fixed output settings: FORMAT PARQUET, COMPRESSION SNAPPY, MAXOBJECTSIZE 16MB, OVERWRITE FALSE.

**Worker TOML example:**

Copy code

```
[connections.source.teradata]
host = "teradata.example.com"
port = 1025
database = "MY_DB"
username = "your_username"
password = "your_password"
write_nos_location_scheme = "/az/"                    # /s3/, /az/, or /gs/
write_nos_location_host = "myaccount.blob.core.windows.net"
write_nos_location_container = "td-nos-exports"
write_nos_function_mapping = "nos_util.WRITE_NOS_FM"  # recommended credential mode
```

**Workflow YAML:**

Copy code

```
    extraction:
      strategy: write_nos
      externalStage: TARGET_DB.SALES.MY_CLOUD_STAGE
```

Credential modes (choose **exactly one**): `write_nos_function_mapping` (recommended), `write_nos_authorization_name`, or `write_nos_access_id` plus `write_nos_access_key`.

**Prompt:**

Copy code

```
Set up Teradata data migration using write_nos extraction for all tables and help me create the matching Snowflake external stage
```

### `tpt`: Teradata Parallel Transporter on the Worker

The Worker generates a **TPT EXPORT** job, runs **`tbuild`**, converts delimited output to Parquet, then uploads like **`regular`**. Optional tuning: `tpt_delimiter` (default ASCII file separator U+001C), `tpt_max_sessions` (default `4`).

**Worker TOML example:**

Copy code

```
[connections.source.teradata]
host = "teradata.example.com"
port = 1025
database = "MY_DB"
username = "your_username"
password = "your_password"
tpt_delimiter = "|"
tpt_max_sessions = 8
```

**Workflow YAML:**

Copy code

```
    extraction:
      strategy: tpt
```

**Prompt:**

Copy code

```
Use tpt extraction for the ORDERS table
```

Under **`regular`** extraction, the Worker auto-enables TPT when `tbuild` is available unless you set **`use_tpt_for_bulk = false`** in Worker TOML.

## Data type mappings

These mappings are applied automatically during migration type conversion:

| Teradata type | Snowflake target type | Supported for migration | Notes |
| --- | --- | --- | --- |
| BYTEINT, SMALLINT, INTEGER, BIGINT | NUMBER | Yes |  |
| NUMERIC, NUMBER, DECIMAL | NUMBER | Yes |  |
| FLOAT, REAL, DOUBLE PRECISION | FLOAT | Yes |  |
| DATE | DATE | Yes |  |
| TIME | TIME | Yes |  |
| TIME WITH TIME ZONE | TIME | Yes | TZ offset dropped; local time preserved |
| TIMESTAMP | TIMESTAMP\_NTZ | Yes |  |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ | Yes |  |
| CHAR, VARCHAR | VARCHAR | Yes |  |
| CLOB | TEXT | Yes | LOB; max 2GB |
| BYTE, VARBYTE, BLOB | BINARY | Yes | LOB; max 2GB for BLOB |
| JSON, XML | VARIANT | Yes |  |
| ST\_GEOMETRY | GEOGRAPHY | Yes |  |
| BOOLEAN | BOOLEAN | Yes |  |
| INTERVAL types (YEAR, DAY, HOUR, and so on) | INTERVAL | Yes | Native `INTERVAL` by default. See [INTERVAL data type handling](../manual-migration/data-migration-configuration-reference#interval-data-type-handling). |
| PERIOD(DATE), PERIOD(TIME), PERIOD(TIMESTAMP), and TIME ZONE variants | VARCHAR | Yes | Stored as a text representation |
| ARRAY | ARRAY | Yes |  |
| LONG VARCHAR, GRAPHIC, VARGRAPHIC, CHAR/VARCHAR UNICODE | VARCHAR | Yes |  |

Expand

Show lessSee more

## Platform-specific considerations

- **Server-side export (`write_nos`)**: Prefer **`write_nos`** for all tables when Teradata NOS and a Snowflake external stage aligned with the target bucket or container are in place. Use **`regular`** or **`tpt`** when volume is genuinely small, or when WRITE\_NOS prerequisites aren’t set up yet.
- **Worker parallelism**: Teradata systems are often CPU and BYNET sensitive. Keep Worker parallelism moderate and coordinate with your DBA.
- **Anti-locking**: AIM DMV adds `LOCKING ROW FOR ACCESS` automatically on every Teradata source scan. No configuration is required. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data migration](./data-migration)
- [Data migration configuration reference](../manual-migration/data-migration-configuration-reference)
- [Validating Data from Teradata](./validate-teradata)
