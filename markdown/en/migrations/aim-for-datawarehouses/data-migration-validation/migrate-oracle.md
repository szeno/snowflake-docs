# Migrating Data from Oracle

This page covers Oracle-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **Oracle Instant Client** and a matching ODBC driver on each Worker host.
- **Service name or TNS configuration** for the target database.
- For **`dbms_cloud`** extraction: a source user with `EXECUTE` on `DBMS_CLOUD`, a stored credential created with `DBMS_CLOUD.CREATE_CREDENTIAL`, and a network ACL that allows HTTPS to your object-store endpoint. See [Server-side export with dbms\_cloud](#server-side-export-with-dbms_cloud).

## Connectivity and extraction

Oracle supports two extraction strategies:

- **`dbms_cloud`** (recommended when prerequisites are met): Oracle exports Parquet directly to object storage with `DBMS_CLOUD.EXPORT_DATA`, and Snowflake loads from an external stage. Data doesn’t pass through the Worker. Use this for **all** tables once object storage and the external stage are set up. See [Server-side export with dbms\_cloud](#server-side-export-with-dbms_cloud).
- **`regular`**: partitioned `SELECT` through the Worker to Parquet, then the internal migration stage. Use when data volume is genuinely small, or when `dbms_cloud` prerequisites (DBMS\_CLOUD grants, credentials, network ACL) aren’t available yet.

### Basic / EZConnect (default)

Copy code

```
[connections.source.oracle]
oracle_connection_mode = "basic"
username = "scott"
password = "your_password"
database = "ORCL"
host = "db.example.com"
port = "1521"
# odbc_driver = "Oracle in instantclient_21_13"
# wallet_directory = "/path/to/wallet"
# wallet_password = "wallet_secret"
```

### Connection modes

| Mode | When to use | Key TOML fields |
| --- | --- | --- |
| **`basic`** | Standard username/password (EZConnect) | `host`, `database` (service name), `port` |
| **`tns_alias`** | TNS name resolution | `tns_name`, optional `tns_admin` |
| **`connect_descriptor`** | Full DESCRIPTION block | Connect descriptor per site standards |

Expand

Show lessSee more

Set `odbc_driver` to the exact name from `pyodbc.drivers()` on the Worker host, or use `auto_detect_driver` when appropriate.

**Workflow example:**

Copy code

```
tables:
  - source:
      databaseName: HR
      schemaName: HR
      tableName: EMPLOYEES
    target:
      databaseName: TARGET_DB
      schemaName: HR
      tableName: EMPLOYEES
    columnNamesToPartitionBy:
      - EMPLOYEE_ID
```

### Server-side export with `dbms_cloud`

With the **`dbms_cloud`** strategy, Oracle writes Parquet files directly to object storage using `DBMS_CLOUD.EXPORT_DATA`, and Snowflake loads them from an external stage. Data never flows through the Worker. When the prerequisites below are in place, use **`dbms_cloud`** for all tables from the source. It’s the Oracle counterpart to Redshift UNLOAD and Teradata WRITE\_NOS.

**Oracle prerequisites** (a DBA typically handles these once):

- Grant `EXECUTE` on `DBMS_CLOUD` to the source user.
- Create a credential for your object store with `DBMS_CLOUD.CREATE_CREDENTIAL`. Credentials aren’t grantable, so the same user that runs the export must own it.
- Add a network ACL that allows HTTPS to your object-store endpoint (for example `*.amazonaws.com`).

**Worker TOML** on the Oracle source connection (both keys are required; partial configuration is rejected):

Copy code

```
[connections.source.oracle]
oracle_connection_mode = "basic"
username = "scott"
password = "your_password"
database = "ORCL"
host = "db.example.com"
port = "1521"

# Server-side export via DBMS_CLOUD.EXPORT_DATA
dbms_cloud_credential_name = "AWS_S3_CRED"
dbms_cloud_file_uri_prefix = "https://your-bucket.s3.us-west-2.amazonaws.com/your/prefix"
# dbms_cloud_format_clause = "JSON_OBJECT('type' VALUE 'parquet', 'compression' VALUE 'snappy')"  # optional; Parquet + snappy by default
```

- `dbms_cloud_file_uri_prefix` must start with `https://`. The Worker appends the partition path and an `export_` file-name prefix.
- Export format defaults to Parquet with snappy compression. Only Parquet loads into Snowflake; don’t override `dbms_cloud_format_clause` with JSON.

**Snowflake external stage** must point at the **same** prefix Oracle writes to:

Copy code

```
CREATE STAGE IF NOT EXISTS ORA_EXPORT_STAGE
  URL = 's3://your-bucket/your/prefix/'
  STORAGE_INTEGRATION = STORAGE_ORACLE_DBMS;
```

**Workflow example:**

Copy code

```
tables:
  - source:
      databaseName: HR
      schemaName: HR
      tableName: EMPLOYEES
    target:
      databaseName: TARGET_DB
      schemaName: HR
      tableName: EMPLOYEES
    columnNamesToPartitionBy:
      - EMPLOYEE_ID
    extraction:
      strategy: dbms_cloud
      externalStage: TARGET_DB.DATA_MIGRATION.ORA_EXPORT_STAGE
```

The workflow references the stage object, not the storage integration. Configuration parsing fails if `externalStage` is omitted.

### Incremental sync

Oracle supports all three strategies: **`none`**, **`watermark`**, and **`checksum`**.

For **`watermark`**, if your tables don’t have a reliable updated-at column, consider using **`ORA_ROWSCN`** — Oracle’s built-in system change number pseudo-column that advances whenever a row is modified. It’s a good default for watermark-based incremental sync on Oracle.

For **`checksum`**, AIM DMV computes a partition checksum over the normalized columns. Some Oracle types are excluded from the default hash, so review [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect) before relying on checksum sync.

**Prompt:**

Copy code

```
Set up incremental sync for ORDERS using ORA_ROWSCN as the watermark column
```

## Data type mappings

| Oracle type | Snowflake target type | Supported for migration | Notes |
| --- | --- | --- | --- |
| NUMBER, INTEGER, INT, SMALLINT | NUMBER | Yes |  |
| DECIMAL, NUMERIC, DEC | NUMBER | Yes |  |
| FLOAT, REAL, BINARY\_FLOAT, BINARY\_DOUBLE | FLOAT | Yes |  |
| DOUBLE PRECISION | FLOAT | Yes |  |
| VARCHAR2, NVARCHAR2, VARCHAR | VARCHAR | Yes | Oracle treats empty string as NULL |
| CHAR, NCHAR | VARCHAR | Yes |  |
| CLOB, NCLOB | VARCHAR | Yes | Truncated at 4000 characters |
| LONG | VARCHAR | Yes |  |
| RAW, BLOB, LONG RAW | BINARY | Yes |  |
| BFILE | VARCHAR | Yes | Requires a server `DIRECTORY` object |
| DATE | TIMESTAMP\_NTZ | Yes |  |
| TIMESTAMP | TIMESTAMP\_NTZ | Yes |  |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ | Yes |  |
| TIMESTAMP WITH LOCAL TIME ZONE | TIMESTAMP\_LTZ | Yes |  |
| INTERVAL YEAR TO MONTH, INTERVAL DAY TO SECOND | INTERVAL | Yes | Native `INTERVAL` by default. See [INTERVAL data type handling](../manual-migration/data-migration-configuration-reference#interval-data-type-handling). |
| ROWID | VARCHAR(18) | Yes | Stored as the hex string representation of the physical row address |
| UROWID | VARCHAR(4000) | Yes |  |
| XMLTYPE | VARIANT | Yes |  |
| JSON | VARIANT | Yes | Requires Oracle 21c or later |
| BOOLEAN | BOOLEAN | Yes | Requires Oracle 23ai or later |
| VECTOR | VECTOR(*element\_type*, *n*) | Yes | Requires Oracle 23ai or later |
| SDO\_GEOMETRY | GEOGRAPHY | Yes | Requires Oracle Spatial. Extracted as Well-Known Text. Non-geographic (projected or planar) geometries may not load as `GEOGRAPHY`; per-SRID routing to `GEOMETRY` is not available. Map the column to `VARCHAR` using `columnTypeMappings` and convert after the load if geometries are non-geographic. |

Expand

Show lessSee more

## Platform-specific considerations

- **Server-side export (`dbms_cloud`)**: Prefer **`dbms_cloud`** for all tables once object storage, `DBMS_CLOUD` grants, and the Snowflake external stage are in place. Reserve **`regular`** for genuinely small volume or when those prerequisites aren’t set up yet. See [Server-side export with dbms\_cloud](#server-side-export-with-dbms_cloud).

  **Prompt (when prerequisites are met):**

  Copy code

  ```
  Set up Oracle data migration using dbms_cloud extraction for all tables and help me create the matching Snowflake external stage
  ```

  **Prompt (when object storage isn’t ready yet, or volume is genuinely small):**

  Copy code

  ```
  Set up Oracle data migration for my project with regular extraction, including the Worker connection
  ```
- **Wallet-based TLS**: Use `wallet_directory` and `wallet_password` in Worker TOML when your Oracle environment requires wallet authentication.
- **Performance hints**: AIM DMV adds an automatic `PARALLEL` optimizer hint on large Oracle tables to speed up scans. Override with `queryModifiers.selectModifier`, or set `selectModifier` to `"NONE"` to disable. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data migration](./data-migration)
- [Validating Data from Oracle](./validate-oracle)
- [Manual Migration: Data migration](../manual-migration/data-migration)
