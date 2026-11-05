# Migrating Data from SQL Server

This page covers SQL Server-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **SQL Server connection driver**: Install the Worker with the `sqlserver` extra to use Microsoft’s preferred `mssql-python` driver. It bundles native binaries, so unixODBC and `msodbcsql` aren’t required. If `mssql-python` isn’t available or the Worker TOML `extra_options` contains a keyword that it doesn’t accept, the Worker falls back to `pyodbc` and a Microsoft ODBC Driver for SQL Server.
- **`bcp` utility (for faster extraction on custom Worker hosts)**: On [Snowpark Container Services](./deploy-workers) Workers, the unified image installs **`bcp`** automatically (via `mssql-tools18`) and sets **`use_bcp = true`** by default. On custom Worker hosts, install the SQL Server **`bcp`** bulk copy utility and set **`use_bcp = true`** in Worker TOML. See [Download and install the bcp utility](https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-download-install) and [bcp utility](https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-utility).
- **Azure Blob Storage and pre-created SQL Server objects for CETAS**: Create an external data source and a Parquet external file format on the source. Create a Snowflake external stage that points to the same container and prefix. See [Using CETAS extraction](#using-cetas-extraction).
- **Windows authentication** (optional): on a Windows Worker host, the Worker can use the process identity. On Snowpark Container Services, the Worker uses a Kerberos keytab. See [Windows authentication](#windows-authentication).

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

SQL Server extracts for Apache Iceberg™ targets must explicitly use `cet_as` or `cloud_direct`. Set `target.tableType` to `"iceberg"`, supply `target.icebergConfig`, and configure a Snowflake external stage for the selected extraction path. See [Apache Iceberg™ tables (spec v2 and v3)](./iceberg) and [Iceberg configuration](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig).

## Windows authentication

Use Windows authentication when the SQL Server instance doesn’t allow SQL authentication. A Worker on Windows can use the account that is already running the process. A Worker on Snowpark Container Services (SPCS) is Linux, so it signs in with a Kerberos ticket from a keytab. The image doesn’t join the domain, and Microsoft ODBC Driver 18 doesn’t fall back to NTLM.

### On a Windows Worker host

Omit the SQL username and password, and set Windows authentication on the source connection:

Copy code

```
[connections.source.sqlserver]
host = "sql01.corp.example.com"
database = "SourceDb"
port = 1433
authentication = "windows_auth"
```

The Worker process has to be running as a domain account that SQL Server accepts. `use_windows_auth = true` still selects this mode.

### On Snowpark Container Services

The SQL Server instance has to be domain-joined. Connect with the fully qualified hostname that appears in the service principal. An IP address or a short name makes the principal lookup fail.

`scai data worker setup` reads a Windows source connection that includes `kerberos_principal`. It then mounts the keytab and `krb5.conf` from Snowflake secrets and starts the Worker with `authentication = "windows_auth"`. It doesn’t create a SQL password secret in this mode. SQL authentication is unchanged when the source connection uses a username and password.

#### Prepare Active Directory

Use two domain accounts:

- A SQL Server service account that owns the service principal `MSSQLSvc/<sql-server-fqdn>:<port>`.
- A separate client account for the Worker. This account owns the keytab. `kerberos_principal` is this account (`client@REALM`), not the SQL Server service account.

Create an AES256 keytab for the client account. Grant that account only the SQL Server permissions the migration or validation needs. Don’t put the SQL Server service keytab in Snowflake.

Write a `krb5.conf` that names the realm and every Key Distribution Center (KDC). The Worker can’t discover the KDC from Active Directory DNS inside SPCS, so turn DNS lookup off and prefer TCP:

Copy code

```
[libdefaults]
    default_realm = CORP.EXAMPLE.COM
    dns_lookup_kdc = false
    udp_preference_limit = 0

[realms]
    CORP.EXAMPLE.COM = {
        kdc = dc01.corp.example.com
    }

[domain_realm]
    .corp.example.com = CORP.EXAMPLE.COM
    corp.example.com = CORP.EXAMPLE.COM
```

Add a `kdc` line for each domain controller the Worker should reach.

#### Save the source connection

Create a Windows connection, then set the client principal on that profile. `scai connection add-sql-server` doesn’t prompt for the principal.

Copy code

```
scai connection add-sql-server --source-connection prod-sql --auth windows \
  --server-url sql01.corp.example.com --database SourceDb --port 1433
```

Add `kerberos_principal` under that connection in `~/.snowflake/scai/connections/sqlserver.toml` (or the `scai/connections/sqlserver.toml` file under `SNOWFLAKE_HOME` when that variable is set):

Copy code

```
[connections.prod-sql]
auth_method = "windows"
server_url = "sql01.corp.example.com"
database = "SourceDb"
port = "1433"
kerberos_principal = "dew-worker@CORP.EXAMPLE.COM"
```

`scai data worker setup` rejects a Windows connection that doesn’t set `kerberos_principal`.

#### Create the Kerberos secrets

Create both secrets before setup, in the metadata database the Worker uses. The default database is `SNOWCONVERT_AI`. When the Worker service name isn’t the default, both secret names and the egress rule name gain that service name as an uppercase prefix and an underscore, the same way a custom service prefixes `SQLSERVER_SECRET`.

Store the keytab as one line of base64 text. On Windows PowerShell:

Copy code

```
[Convert]::ToBase64String([IO.File]::ReadAllBytes("dew-worker.keytab"))
```

Create the secrets from a worksheet, or with `snow sql --enable-templating NONE`. The default Snowflake CLI templating removes `[libdefaults]`, `[realms]`, and `[domain_realm]` from `krb5.conf`, and the Worker then can’t find the realm.

Copy code

```
CREATE OR REPLACE SECRET <metadata_database>.PUBLIC.DEW_KERBEROS_KEYTAB
  TYPE = GENERIC_STRING
  SECRET_STRING = '<one-line-base64-keytab>';

CREATE OR REPLACE SECRET <metadata_database>.PUBLIC.DEW_KERBEROS_KRB5_CONF
  TYPE = GENERIC_STRING
  SECRET_STRING = $$
[libdefaults]
    default_realm = CORP.EXAMPLE.COM
    dns_lookup_kdc = false
    udp_preference_limit = 0

[realms]
    CORP.EXAMPLE.COM = {
        kdc = dc01.corp.example.com
    }

[domain_realm]
    .corp.example.com = CORP.EXAMPLE.COM
    corp.example.com = CORP.EXAMPLE.COM
$$;
```

The role that owns the Worker service needs `READ` on both secrets. That role already has access when it creates the secrets. When a different role creates them, grant `READ` to the service owner.

#### Set up the Worker

Copy code

```
scai data worker setup --compute-pool <compute_pool> --source-connection prod-sql
```

Setup mounts the two secrets on the service and doesn’t store a SQL password. It still creates the SQL Server egress network rule for the SQL Server host and the driver-download hosts. It doesn’t add the domain controllers. `CREATE OR REPLACE` on that rule replaces the host list, so add the domain controllers after setup, or prepare the rule yourself and pass `--skip-egress`.

Add every domain controller to the rule setup created. `SET VALUE_LIST` replaces the whole list, so keep the SQL Server host and the driver-download hosts that are already there. See [Driver download hosts by platform](../manual-migration/manual-spcs-worker-setup#driver-download-hosts-by-platform).

Copy code

```
ALTER NETWORK RULE <metadata_database>.PUBLIC.SQLSERVER_EGRESS_RULE SET
  VALUE_LIST = (
    'sql01.corp.example.com:1433',
    'dc01.corp.example.com:88'
    -- keep the driver-download hosts already on this rule
  );
```

If setup finishes before the domain controllers are on the rule, the container can’t get a ticket and exits before the agent starts. Those errors name the missing principal, keytab, or `krb5.conf`. They don’t print secret contents. After the rule includes the domain controllers, resume the service:

Copy code

```
scai data worker start
```

Note

On a public `HOST_PORT` network rule, Snowflake can reject TCP port 88 with error `001435` and the text “unresolvable host name”. When that happens, publish the KDC on TCP 443, forward that port to TCP 88 on the domain controller, and set the KDC port in `krb5.conf` to `443`. A private `PRIVATE_HOST_PORT` rule can still use port 88.

The SQL Server port in the connection, the `MSSQLSvc/<fqdn>:<port>` service principal, the SQL Server listener, and the network rule have to use the same port.

Allow the Snowflake egress ranges on both the SQL Server host and the domain controllers. Don’t open the source network to every address. Egress addresses can change within the published prefix, so refresh the allowlist when Workers stop connecting:

Copy code

```
SELECT SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES();
```

See [Allowing SPCS to reach your source system](./deploy-workers#allowing-spcs-to-reach-your-source-system-inbound-access).

To keep a network rule you already wrote, create the secrets first, include the SQL Server host, every domain controller, and the driver-download hosts on that rule, then run setup with `--skip-egress`. Without `--skip-egress`, setup replaces the rule and drops any domain controllers you added ahead of time.

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

Grant the CETAS credential identity and the Snowflake Azure service principal as described in [Azure Blob Storage](./required-privileges#azure-blob-storage).

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
- [Apache Iceberg™ tables (spec v2 and v3)](./iceberg)
- [Manual Migration: Data migration](../manual-migration/data-migration)
