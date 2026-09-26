# Migrating Data from PostgreSQL

This page covers PostgreSQL-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **Npgsql driver** (pure Python) on Workers. You don’t install a PostgreSQL ODBC driver for cloud migration.
- **TLS configuration**: Set **`ssl_mode`** in Worker TOML (`Disable`, `Prefer`, `Require`, `VerifyCA`, `VerifyFull`). Default **`Require`** for managed hosts; use **`Disable`** for local Docker or lab instances without TLS.

## Connectivity and extraction

PostgreSQL uses **`regular`** extraction (partitioned `SELECT` through the Worker to Parquet, then the internal migration stage).

### Managed host (TLS required)

Copy code

```
[connections.source.postgresql]
auth_method = "standard"
username = "scai"
password = "your_password"
database = "analytics"
host = "db.example.com"
port = "5432"
ssl_mode = "Require"
use_copy = true
```

### Local Docker or lab (no TLS)

Copy code

```
[connections.source.postgresql]
auth_method = "standard"
username = "scai"
password = "scai"
database = "scai_pg"
host = "localhost"
port = "5432"
ssl_mode = "Disable"
use_copy = true
```

**Workflow example:**

Copy code

```
tables:
  - source:
      databaseName: analytics
      schemaName: public
      tableName: customers
    target:
      databaseName: TARGET_DB
      schemaName: PUBLIC
      tableName: customers
    columnNamesToPartitionBy:
      - customer_id
```

## Data type mappings

| PostgreSQL type | Snowflake target type | Supported for migration | Notes |
| --- | --- | --- | --- |
| smallint, integer, bigint, serial types | NUMBER | Yes |  |
| numeric(p,s), decimal | NUMBER | Yes | Default NUMBER(20,10) when unspecified |
| real, double precision | FLOAT | Yes |  |
| boolean | BOOLEAN | Yes |  |
| date | DATE | Yes |  |
| time without/with time zone | TIME | Yes |  |
| timestamp without/with time zone | TIMESTAMP\_NTZ / TIMESTAMP\_TZ | Yes |  |
| character, character varying, text | VARCHAR | Yes |  |
| bytea | BINARY | Yes |  |
| uuid | VARCHAR(36) | Yes |  |
| json, jsonb, xml | VARIANT | Yes |  |
| money | VARCHAR | Yes | Stored as a text representation |
| bit, bit varying | VARCHAR | Yes | Stored as a text representation |
| interval | INTERVAL or VARCHAR | Yes | Depends on `intervalHandling`. See [INTERVAL columns and intervalHandling](#interval-columns-and-intervalhandling). |
| array | ARRAY | Yes |  |
| inet, cidr, macaddr types | VARCHAR | Yes | Stored as a text representation |
| point, line, lseg, box, path, polygon, circle | VARCHAR | Yes | Native PostgreSQL geometric types stored as text |
| PostGIS geometry | GEOMETRY | Yes |  |
| PostGIS geography | GEOGRAPHY | Yes |  |
| pgvector vector | VECTOR(*element\_type*, *n*) | Yes | Extreme floating-point values can round slightly |
| pg\_lsn, pg\_snapshot, txid\_snapshot | (unmapped) | No |  |

Expand

Show lessSee more

## INTERVAL columns and intervalHandling

PostgreSQL’s `interval` type can store year-month and day-time fields in the same value. Snowflake has no single interval qualifier that spans both families.

AIM DMV exposes that tradeoff through `intervalHandling`. Neither setting is universally better: choose based on what you need on Snowflake.

| `intervalHandling` | Target type | Implications |
| --- | --- | --- |
| `"interval"` (default) | Snowflake `INTERVAL DAY TO SECOND` | Keeps a native interval column and interval-aware operations. Mixed year-month and day-time values are folded into day-time, so months and years are treated as fixed-length spans and calendar-accurate year-month precision is lost. |
| `"varchar"` | `VARCHAR` | Preserves the source text form, including exact year-month fields in mixed-family intervals. You don’t get a native `INTERVAL` column on Snowflake. |

Expand

Show lessSee more

Set `intervalHandling` at the workflow root, on `defaultTableConfiguration`, or per table. Use the same value later during validation so comparisons match how the data was migrated. For the property reference, see [INTERVAL data type handling](../manual-migration/data-migration-configuration-reference#interval-data-type-handling).

**Prompt:**

Copy code

```
For the EVENTS table, store INTERVAL columns as text instead of native INTERVAL so we keep exact year-month fields
```

## Incremental sync and VACUUM FREEZE

PostgreSQL supports [incremental sync](../manual-migration/data-migration-configuration-reference#synchronizationstrategy-model) with both the `watermark` and `checksum` strategies. For `checksum`, PostgreSQL is a special case: instead of hashing column values, the default partition checksum fingerprints each partition from the MVCC system column `xmin` (the inserting transaction ID of each row). It reads no column data, so change detection stays cheap even on wide tables.

The one caveat comes from `VACUUM FREEZE`. To protect against transaction-ID wraparound, freezing rewrites each row’s `xmin` to a fixed “frozen” value. That has two effects on `checksum` sync:

- **A frozen partition may re-migrate once (safe).** Freezing changes a partition’s fingerprint even though no data changed, so the next sync run re-extracts that partition one extra time. This costs time but never loses data.
- **A change may be missed (rare).** Once every row in a partition is frozen, the partition’s fingerprint depends only on its row count. If rows are updated and then frozen again *between two consecutive sync runs*, the next run can reproduce the previous fingerprint and skip the partition. Reaching this requires roughly `vacuum_freeze_min_age` transactions (50 million by default) plus a vacuum landing between two runs, so it isn’t reachable at a normal sync cadence.

If a table is subject to aggressive freezing and you need value-based detection, set a value-derived `synchronization.checksumExpression` (for example `MAX(updated_at)`) or use the `watermark` strategy with a monotonic column. See [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect).

`xmin`-based detection reads the physical row header, so it works on ordinary tables and on declarative-partitioned parent tables, but not on views or foreign tables.

## Platform-specific considerations

- **`use_copy = true`**: PostgreSQL native COPY protocol is enabled by default for cloud migration and significantly improves extraction speed on large tables.
- **`ssl_mode`**: Set this to match your environment. Most managed cloud PostgreSQL hosts require `Require` or stricter. When you set up the Worker connection, confirm both COPY and `ssl_mode` match your host.

  **Prompt:**

  Copy code

  ```
  Set up PostgreSQL data migration for my project with COPY extraction and the right ssl_mode for my host
  ```
- **Anti-locking**: No automatic hint is added on PostgreSQL. Set `queryModifiers` only when you need custom source SQL hints. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data migration](./data-migration)
- [Validating Data from PostgreSQL](./validate-postgresql)
- [Manual Migration: Data migration](../manual-migration/data-migration)
