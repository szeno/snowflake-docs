# Openflow Connector for SQL Server: Iceberg table destinations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Openflow multi-database connectors for SQL Server support writing to Snowflake-managed Apache
Apache Iceberg™ tables as an opt-in destination format. Iceberg v2 and v3 are both supported. Setting
**Table Storage Format** = `ICEBERG` and choosing an **Iceberg Version** are the only connector-level
changes required. The external volume, catalog, and serialization policy are inherited from the
Snowflake destination database defaults. The Iceberg specification version is set via the
**Iceberg Version** connector parameter, which defaults to `3`.

Storage can be either [Snowflake storage for Apache Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage)
(`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`) or an external volume in your cloud storage. When you use
Snowflake storage, no external cloud storage or IAM grants are required.

Existing connectors using standard tables aren’t affected.

## Prerequisites

- **Openflow runtime**: An existing runtime to host the connector.
- **SQL Server source configured for CDC or Change Tracking**:
  - For CDC: Enable CDC on the database and each replicated table.
  - For Change Tracking: Enable change tracking on the database and each replicated table with
    a primary key.
  - For details, see
    [Set up the Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/setup)
    or [Set up the SQL Server CDC connector](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup).
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
[Set up the Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/setup)
or [Set up the SQL Server CDC connector](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup).

## Step 3: Set the Iceberg version

Set the **Iceberg Version** connector parameter to `2` or `3`. This controls the Iceberg specification
version used for type mapping (for example, JSON maps to `variant` on v3 vs `string` on v2)
and the `ICEBERG_VERSION=<n>` clause in CREATE ICEBERG TABLE DDL.

The **Iceberg Version** parameter defaults to `3`. Review and change to `2` if needed before starting
the connector. Do not change this value after ingestion begins.

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
- **Nanosecond timestamp range restriction on v3**: When DATETIME2(7) or DATETIMEOFFSET(7)
  maps to `timestamp_ns` or `timestamptz_ns` on v3, the representable date range narrows to
  1677-09-21 through 2262-04-11. Values outside this range are rejected at insert time.
- **DATETIMEOFFSET offset collapsed to UTC**: Iceberg has no offset-preserving timestamp type.
  The original timezone offset is lost; only the UTC instant is stored.
- **Source timestamp precision widening not supported on v3**: If a source column’s precision
  increases (for example, DATETIME2(6) altered to DATETIME2(7)), the Iceberg column type cannot
  be promoted from `timestamp` to `timestamp_ns`. The connector was created based on the original
  precision.
- **Do not change Table Storage Format or Iceberg Version after the connector starts**:
  The connector’s **Table Storage Format** and **Iceberg Version** parameter should not be modified
  after ingestion begins. Mixing settings across destination tables is not supported. To switch,
  follow the steps in [Switching table storage format or Iceberg version](#switching-table-storage-format-or-iceberg-version).

## Type mapping reference

The following table shows how SQL Server types map to Snowflake standard and Iceberg destination types:

| SQL Server type | Snowflake (Standard) | Iceberg v3 | Iceberg v2 |
| --- | --- | --- | --- |
| TINYINT / SMALLINT / INT | INT | `long` | `long` |
| BIGINT | INT | `long` | `long` |
| BIT | BOOLEAN | `boolean` | `boolean` |
| DECIMAL(P,S) / NUMERIC(P,S) | NUMBER(P,S) | `decimal(P,S)` | `decimal(P,S)` |
| MONEY | NUMBER(19,4) | `decimal(19,4)` | `decimal(19,4)` |
| SMALLMONEY | NUMBER(10,4) | `decimal(10,4)` | `decimal(10,4)` |
| FLOAT / FLOAT(53) | FLOAT | `double` | `double` |
| REAL / FLOAT(n) (n ≤ 24) | FLOAT | `double` | `double` |
| DATE | DATE | `date` | `date` |
| TIME(0..6) | TIME | `time` | `time` |
| TIME(7) | TIME | `time` (100ns truncated) | `time` (100ns truncated) |
| SMALLDATETIME | TIMESTAMP\_NTZ | `timestamp` | `timestamp` |
| DATETIME | TIMESTAMP\_NTZ | `timestamp` | `timestamp` |
| DATETIME2(0..6) | TIMESTAMP\_NTZ | `timestamp` | `timestamp` |
| DATETIME2(7) | TIMESTAMP\_NTZ | `timestamp_ns` | `timestamp` (100ns truncated) |
| DATETIMEOFFSET(0..6) | TIMESTAMP\_TZ | `timestamptz` | `timestamptz` |
| DATETIMEOFFSET(7) | TIMESTAMP\_TZ | `timestamptz_ns` | `timestamptz` (100ns truncated) |
| CHAR / VARCHAR / NCHAR / NVARCHAR / TEXT / NTEXT | TEXT | `string` | `string` |
| BINARY / VARBINARY / IMAGE | BINARY | `binary` | `binary` |
| XML | TEXT | `string` | `string` |
| JSON (SQL Server 2025) | VARIANT | `variant` | `string` |
| UNIQUEIDENTIFIER | TEXT | `string` | `string` |
| ROWVERSION | TEXT | `string` | `string` |
| SQL\_VARIANT | TEXT | `string` | `string` |
| GEOMETRY / GEOGRAPHY | TEXT | `string` | `string` |

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

Connector version `0.45.0` (multi-database) / `0.44.0` (CDC) introduces the **Iceberg Version**
parameter. If you are upgrading from an earlier connector version, a new **Iceberg Version** field
appears that you must configure to match your existing destination tables.

1. Stop the connector.
2. [Upgrade the runtime](/user-guide/data-integration/openflow/manage#label-openflow-upgrading-a-runtime)
   to version `2026.7.21` or later.
3. [Upgrade the connector](/user-guide/data-integration/openflow/manage#upgrade-a-connector) in place
   to the version listed above or later.
4. The **Iceberg Version** parameter defaults to `3` after the flow upgrade. Review and change to `2`
   if your existing destination tables are Iceberg v2 before starting the connector.
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
- [Set up the Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/setup)
- [Set up the SQL Server CDC connector](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup)
