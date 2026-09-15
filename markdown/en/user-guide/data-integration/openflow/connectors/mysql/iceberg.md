# Openflow Connector for MySQL: Iceberg table destinations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Openflow Connector for MySQL supports writing to Snowflake-managed Apache Apache Iceberg™ tables
as an opt-in destination format. Iceberg v2 and v3 are both supported. Setting **Table Storage Format** = `ICEBERG`
and choosing an **Iceberg Version** are the only connector-level changes required. The external volume,
catalog, and serialization policy are inherited from the Snowflake destination database defaults.
The Iceberg specification version is set via the **Iceberg Version** connector parameter, which
defaults to `3` for both Gen2 (Openflow UI wizard) and Gen1 (parameter context) connectors.

Storage can be either [Snowflake storage for Apache Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage)
(`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`) or an external volume in your cloud storage. When you use
Snowflake storage, no external cloud storage or IAM grants are required.

Existing connectors using standard tables aren’t affected.

## Prerequisites

- **Openflow runtime**: An existing runtime to host the connector.
- **MySQL source configured for CDC**: Binary logging enabled (`log_bin = ON`,
  `binlog_format = ROW`, `binlog_row_image = FULL`), a user with `REPLICATION SLAVE` and
  `REPLICATION CLIENT` privileges, and a sufficiently long `binlog_expire_logs_seconds` for
  snapshot reconciliation. For details, see
  [Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup).
- **External volume in your cloud storage**: An external volume configured for Iceberg storage,
  with USAGE granted to the connector’s Snowflake role. See
  [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume). Not required when using
  Snowflake storage (`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`).
- **Snowflake destination database**: An existing database configured with Iceberg parameters
  (next section).

## Step 1: Configure the Snowflake destination database

Set the Iceberg defaults on the destination database. The connector reads these defaults at runtime
for external volume and serialization policy. The Iceberg specification version is configured
per-connector via the **Iceberg Version** parameter (see Step 3), not solely via the database-level
`ICEBERG_VERSION_DEFAULT`.

### Option A: Snowflake storage

When you use Snowflake storage, Snowflake stores and manages the Iceberg table files for you.
No external cloud storage or IAM grants are required.

Copy code

```
CREATE DATABASE <db>
  EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
  STORAGE_SERIALIZATION_POLICY = <COMPATIBLE|OPTIMIZED>;
```

To configure an existing database:

Copy code

```
ALTER DATABASE <db> SET
  EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
  STORAGE_SERIALIZATION_POLICY = <COMPATIBLE|OPTIMIZED>;
```

### Option B: External volume in your cloud storage

If you need to keep table files in your own cloud storage, configure the database with your
external volume:

Copy code

```
CREATE DATABASE <db>
  EXTERNAL_VOLUME = '<volume>'
  STORAGE_SERIALIZATION_POLICY = <COMPATIBLE|OPTIMIZED>;
```

To configure an existing database:

Copy code

```
ALTER DATABASE <db> SET
  EXTERNAL_VOLUME = '<volume>'
  STORAGE_SERIALIZATION_POLICY = <COMPATIBLE|OPTIMIZED>;
```

| Parameter | Required | Notes |
| --- | --- | --- |
| EXTERNAL\_VOLUME | Yes | The external volume for Iceberg file storage. |
| ICEBERG\_VERSION\_DEFAULT | No | `2` or `3`. Legacy fallback for older connector flows where the **Iceberg Version** parameter is unset. New connectors set the version via the connector parameter (Step 3) and do not require this database setting. |
| STORAGE\_SERIALIZATION\_POLICY | Yes | `COMPATIBLE` produces Parquet files readable by external engines. `OPTIMIZED` enables Snowflake-specific query optimizations. Choose based on your data query needs. For more information, see [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#storage-serialization-policy). |

Expand

Show lessSee more

Note

`CATALOG = 'SNOWFLAKE'` is set automatically by the connector on each CREATE ICEBERG TABLE
statement. Don’t set it at the database level.

The base location for each table is auto-derived using the
[flat layout](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-snowflake-managed-flat-layout):
`STORAGE_BASE_URL/database/schema/table_name.randomId/[data | metadata]/`.
No user configuration is needed.

If using an external volume in your cloud storage (Option B), grant the connector’s Snowflake role
USAGE on the external volume:

Copy code

```
GRANT USAGE ON EXTERNAL VOLUME <volume> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

This step is not required for Snowflake storage.

## Step 2: Set Table Storage Format in the connector’s parameter context

Set the **Table Storage Format** parameter to `ICEBERG` in the connector’s destination parameter context.
The default is `STANDARD`.

For the full connector creation and configuration workflow, see
[Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup).

## Step 3: Set the Iceberg version

Set the **Iceberg Version** connector parameter to `2` or `3`. This controls the Iceberg specification
version used for type mapping (for example, JSON maps to `variant` on v3 vs `string` on v2)
and the `ICEBERG_VERSION=<n>` clause in CREATE ICEBERG TABLE DDL.

- **Gen2 (Openflow UI wizard)**: **Iceberg Version** is a required field when **Table Storage Format** =
  `ICEBERG`, defaulting to `3`. This setting is immutable after the connector configuration is first
  applied.
- **Gen1 (parameter context)**: The **Iceberg Version** parameter defaults to `3`. Review and change
  to `2` if needed before starting the connector. Do not change this value after ingestion begins.

## Step 4: Start and verify

Start the connector as usual. After the initial snapshot completes, verify the destination tables
are Iceberg:

Copy code

```
-- Confirm the table is Iceberg
SELECT GET_DDL('TABLE', '<db>.<schema>.<table>');

-- Confirm the Iceberg version on the database
SHOW PARAMETERS LIKE 'ICEBERG_VERSION_DEFAULT' IN DATABASE <db>;
```

## Known limitations

- **Tri-Secret Secure accounts and Snowflake storage**: Accounts with Tri-Secret Secure
  (TSS) enabled may be unable to create new Snowflake-managed Iceberg tables that use
  [Snowflake storage for Apache Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).
  For details, see [Encryption](/user-guide/tables-iceberg-internal-storage#encryption).
- **Incompatible type change.** When the source column type changes to a type that maps to a
  different Iceberg type, the table is marked as failed and requires a resnapshot. See
  [Type mapping reference](#type-mapping-reference) for the complete source-to-Iceberg type
  mapping.
- **Parameter change within the same Iceberg type.** The connector doesn’t recognize parameter
  changes within the same Iceberg type (for example, changing `decimal(10,2)` to `decimal(20,2)`).
  The column retains its current Iceberg type.
- **BIGINT to BIGINT UNSIGNED schema evolution not allowed**: Signed `BIGINT` maps to `long`
  while `BIGINT UNSIGNED` maps to `decimal(20,0)`. Iceberg does not allow promotion from `long`
  to `decimal`, so this schema change on the source will fail replication.
- **Do not change Table Storage Format or Iceberg Version after the connector starts**:
  The connector’s **Table Storage Format** and **Iceberg Version** parameter should not be modified
  after ingestion begins. Gen2 connectors enforce this by making **Iceberg Version** immutable after
  first apply. Mixing settings across destination tables is not supported. To switch, follow the
  steps in [Switching table storage format or Iceberg version](#switching-table-storage-format-or-iceberg-version).

## Type mapping reference

The following table shows how MySQL types map to Snowflake standard and Iceberg destination types:

| MySQL type | Snowflake (Standard) | Iceberg v3 | Iceberg v2 |
| --- | --- | --- | --- |
| TINYINT / SMALLINT / MEDIUMINT (signed or unsigned) | INT | `long` | `long` |
| INT (signed) | INT | `long` | `long` |
| INT UNSIGNED | INT | `long` | `long` |
| BIGINT (signed) | INT | `long` | `long` |
| BIGINT UNSIGNED | INT | `decimal(20,0)` | `decimal(20,0)` |
| YEAR | INT | `long` | `long` |
| FLOAT (signed/unsigned) | FLOAT | `double` | `double` |
| DOUBLE (signed/unsigned) | FLOAT | `double` | `double` |
| DECIMAL(P,S) (P ≤ 38) | NUMBER(P,S) | `decimal(P,S)` | `decimal(P,S)` |
| DECIMAL(P,S) (P > 38) | TEXT | `string` | `string` |
| BOOLEAN / BOOL | INT | `long` | `long` |
| DATE | DATE | `date` | `date` |
| TIME | TIME | `time` | `time` |
| DATETIME | TIMESTAMP\_NTZ | `timestamp` | `timestamp` |
| TIMESTAMP | TIMESTAMP\_TZ | `timestamptz` | `timestamptz` |
| CHAR / VARCHAR / TEXT / TINYTEXT / MEDIUMTEXT / LONGTEXT | TEXT | `string` | `string` |
| ENUM / SET | TEXT | `string` | `string` |
| BIT | TEXT | `string` | `string` |
| BINARY / VARBINARY / BLOB / TINYBLOB / MEDIUMBLOB / LONGBLOB | BINARY | `binary` | `binary` |
| JSON | VARIANT | `variant` | `string` |
| GEOMETRY family | TEXT | `string` | `string` |

Expand

Show lessSee more

Source types not listed in the table are mapped to TEXT on standard tables and `string` on Iceberg
tables.

## Switching table storage format or Iceberg version

Switching between Standard and Iceberg, or between Iceberg v2 and v3, requires recreating the
connector. Follow these steps:

1. Stop the connector.
2. Delete the process group in Openflow.
3. Manually clean up the destination database (drop the replicated schemas/tables, or use a new
   database).
4. Reimport the connector with the new **Table Storage Format** and select the target **Iceberg Version**
   when configuring the connector.

This ensures all connector state is correctly cleaned up within Openflow. The new connector performs
a fresh snapshot into the destination.

## Upgrading an existing connector to use Iceberg Version pinning

Gen2 connector version `2026.7.21` and Gen1 connector version `0.53.0` introduce the
**Iceberg Version** parameter. If you are upgrading from an earlier connector version (for example,
Gen1 `0.50.0` to `0.53.0` or later), a new **Iceberg Version** field appears that you must configure
to match your existing destination tables.

1. Stop the connector.
2. [Upgrade the runtime](/user-guide/data-integration/openflow/manage#label-openflow-upgrading-a-runtime)
   to version `2026.7.21` or later.
3. [Upgrade the connector](/user-guide/data-integration/openflow/manage#upgrade-a-connector)
   in place (Gen2: to version `2026.7.21` or later; Gen1: to version `0.53.0` or later).
4. Set the **Iceberg Version** parameter to match your existing destination tables:
   - **Gen2 (Openflow UI wizard)**: After upgrading, open the connector configuration wizard.
     The **Destination details** step now includes a required **Iceberg Version** field, defaulting
     to `3`. If your existing destination tables are Iceberg v2, change it to `2` before applying.
     This choice is locked after first apply and cannot be changed later.
   - **Gen1 (parameter context)**: The **Iceberg Version** parameter defaults to `3` after the flow
     upgrade. If your existing destination tables are Iceberg v2, change it to `2` before starting
     the connector.
5. Start the connector.

Caution

Selecting an **Iceberg Version** that doesn’t match your existing destination tables can cause
type-mapping errors or DDL failures. Always verify the version of your existing tables before
choosing a value.

## References

- [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume)
- [Data types for Apache Iceberg tables](/user-guide/tables-iceberg-data-types)
- [ALTER DATABASE](/sql-reference/sql/alter-database)
- [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#storage-serialization-policy)
- [Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup)
