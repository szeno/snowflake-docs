# Openflow Connector for Oracle: Iceberg table destinations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Openflow Connector for Oracle (multi-database) supports writing to Snowflake-managed Apache
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
- **Oracle source configured for CDC**: Archive logging enabled (`ARCHIVELOG` mode), supplemental
  logging configured, and a LogMiner or XStream user with the required privileges. For details, see
  [Set up the Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/setup-tasks).
- **Snowpipe Streaming v2**: The Oracle connector must have Snowpipe Streaming v2 based writes
  enabled. This is required for Iceberg table destinations.
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
[Set up the Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/setup-tasks).

## Step 3: Set the Iceberg version

Set the **Iceberg Version** connector parameter to `2` or `3`. This controls the Iceberg specification
version used for type mapping (for example, JSON maps to `variant` on v3 versus `string` on v2)
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
- **Incompatible type change:** When the source column type changes to a type that maps to a
  different Iceberg type, the table is marked as failed and requires a resnapshot. See
  [Type mapping reference](#type-mapping-reference) for the complete source-to-Iceberg type
  mapping.
- **Parameter change within the same Iceberg type:** The connector doesn’t recognize parameter
  changes within the same Iceberg type (for example, changing `decimal(10,2)` to `decimal(20,2)`).
  The column retains its current Iceberg type.
- **Nanosecond timestamp range restriction on v3**: When a TIMESTAMP(7..9) column maps to
  `timestamp_ns` or `timestamptz_ns` on v3, the representable date range narrows to
  1677-09-21 through 2262-04-11. Values outside this range are rejected at insert time.
- **TIMESTAMP WITH TIME ZONE offset collapsed to UTC**: Iceberg has no offset-preserving
  timestamp type. The original timezone offset or region name is lost; only the UTC instant is
  stored.
- **Source TIMESTAMP precision widening not supported on v3**: If a source column’s precision
  increases (for example, TIMESTAMP(6) altered to TIMESTAMP(7)), the Iceberg column type cannot
  be promoted from `timestamp` to `timestamp_ns`. The connector was created based on the original
  precision.
- **Do not change Table Storage Format or Iceberg Version after the connector starts**:
  The connector’s **Table Storage Format** and **Iceberg Version** parameter should not be modified
  after ingestion begins. Mixing settings across destination tables is not supported. To switch,
  follow the steps in [Switching table storage format or Iceberg version](#switching-table-storage-format-or-iceberg-version).

## Type mapping reference

The following table shows how Oracle types map to Snowflake standard and Iceberg destination types:

| Oracle type | Snowflake (Standard) | Iceberg v3 | Iceberg v2 |
| --- | --- | --- | --- |
| NUMBER(P,S) (P ≤ 38) | NUMBER(P,S) | `decimal(P,S)` | `decimal(P,S)` |
| NUMBER (no precision) | NUMBER(38,19) | `decimal(38,19)` | `decimal(38,19)` |
| INTEGER / SMALLINT / INT | NUMBER(38,0) | `decimal(38,0)` | `decimal(38,0)` |
| FLOAT(P) | FLOAT | `double` | `double` |
| BINARY\_FLOAT | FLOAT | `double` | `double` |
| BINARY\_DOUBLE | FLOAT | `double` | `double` |
| BOOLEAN (Oracle 23ai+) | BOOLEAN | `boolean` | `boolean` |
| DATE | TIMESTAMP\_NTZ | `timestamp` | `timestamp` |
| TIMESTAMP(0..6) | TIMESTAMP\_NTZ | `timestamp` | `timestamp` |
| TIMESTAMP(7..9) | TIMESTAMP\_NTZ | `timestamp_ns` | `timestamp` (truncated) |
| TIMESTAMP(0..6) WITH TIME ZONE | TIMESTAMP\_TZ | `timestamptz` | `timestamptz` |
| TIMESTAMP(7..9) WITH TIME ZONE | TIMESTAMP\_TZ | `timestamptz_ns` | `timestamptz` (truncated) |
| TIMESTAMP WITH LOCAL TIME ZONE (0..6) | TIMESTAMP\_LTZ | `timestamptz` | `timestamptz` |
| TIMESTAMP WITH LOCAL TIME ZONE (7..9) | TIMESTAMP\_LTZ | `timestamptz_ns` | `timestamptz` (truncated) |
| INTERVAL YEAR TO MONTH | TEXT | `string` | `string` |
| INTERVAL DAY TO SECOND | TEXT | `string` | `string` |
| CHAR / NCHAR / VARCHAR2 / NVARCHAR2 | TEXT | `string` | `string` |
| CLOB / NCLOB / LONG | TEXT | `string` | `string` |
| RAW | BINARY | `binary` | `binary` |
| BLOB / LONG RAW | BINARY | `binary` | `binary` |
| JSON (Oracle 21c+) | VARIANT | `variant` | `string` |
| XMLTYPE | TEXT | `string` | `string` |
| ROWID / UROWID | TEXT | `string` | `string` |

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

Connector version `0.42.0` (embedded license) / `0.41.0` (independent license) introduces the
**Iceberg Version** parameter. If you are upgrading from an earlier connector version, a new
**Iceberg Version** field appears that you must configure to match your existing destination tables.

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
- [Set up the Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/setup-tasks)
