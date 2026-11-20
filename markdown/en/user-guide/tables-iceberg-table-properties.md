# Iceberg table properties

[Iceberg table properties](https://iceberg.apache.org/docs/latest/configuration/#table-properties)
are key-value settings stored with an Apache Iceberg™ table. You set them in
Snowflake with the `TABLE_PROPERTIES` clause on `CREATE ICEBERG TABLE` and `ALTER ICEBERG TABLE`.

Some keys map to a Snowflake parameter or property. Snowflake stores most other keys as written, subject to the checks below.

## Overview

Use `TABLE_PROPERTIES` when you want an Iceberg engine and Snowflake to share the same settings.
A key such as `write.target-file-size-bytes` or `write.delete.mode` changes the Snowflake parameter
that governs the same behavior. A key Snowflake doesn’t use, such as an external-engine-specific
table property, is stored with the table metadata so other engines can read it.

Where the value lives depends on the table:

- **Snowflake-managed tables** (`CATALOG = 'SNOWFLAKE'`): Snowflake writes the properties into the
  metadata it generates. Keys that map to a Snowflake setting first update the Snowflake setting,
  and then the Iceberg table property value is regenerated from that setting. Other keys are stored
  and copied into each new metadata file.
- **Externally managed tables that Snowflake can write**: Snowflake commits the properties to the
  external catalog. Keys that map to a Snowflake setting are also applied in Snowflake. The catalog
  keeps the value you wrote.
- **Other Iceberg tables**: `TABLE_PROPERTIES` isn’t supported. That includes tables created from
  Iceberg files in object storage, Delta-based tables, Parquet tables etc.

The clause is also supported on `CREATE ICEBERG TABLE ... AS SELECT` and `CREATE ICEBERG TABLE ... LIKE`.

## How Iceberg table properties work

Set properties when you create the table, change them later, or remove them by name. Property names
are case-sensitive. `CREATE` and `ALTER ... SET` require `'key' = 'value'` pairs. `ALTER ... UNSET`
takes property names and must name at least one.

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table (id INT, amount NUMBER(10,2))
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_ext_vol'
  BASE_LOCATION = 'my_iceberg_table'
  TABLE_PROPERTIES = (
    'write.target-file-size-bytes' = '67108864',
    'write.delete.mode' = 'merge-on-read',
    'read.split.target-size' = '268435456'
  );

ALTER ICEBERG TABLE my_iceberg_table SET
  TABLE_PROPERTIES = ('commit.retry.num-retries' = '10');

ALTER ICEBERG TABLE my_iceberg_table UNSET
  TABLE_PROPERTIES ('read.split.target-size');
```

If the same statement sets a Snowflake parameter and a `TABLE_PROPERTIES` key that maps to that
parameter, the two values must agree. Snowflake rejects the statement when they don’t.

Unsetting a key that maps to a Snowflake setting also unsets that setting at the table level.

### Properties that map to Snowflake settings

| Iceberg property | Snowflake setting | Conversion |
| --- | --- | --- |
| `write.target-file-size-bytes` | `TARGET_FILE_SIZE` | Positive number of bytes, rounded down to 16 MB, 32 MB, 64 MB, or 128 MB. A value below 16 MB is raised to 16 MB. |
| `history.expire.max-snapshot-age-ms` | `DATA_RETENTION_TIME_IN_DAYS` | A number of milliseconds, 0 or greater, rounded up to a whole number of days. |
| `format-version` | `ICEBERG_VERSION` | An integer format version that `CREATE ICEBERG TABLE` accepts. `CREATE` only. |
| `comment` | `COMMENT` | The text you specify. |
| `write.delete.mode`, `write.update.mode`, `write.merge.mode` | `ICEBERG_MERGE_ON_READ_BEHAVIOR` | `copy-on-write` or `merge-on-read`. If any named property is `merge-on-read`, Snowflake sets the parameter to `ENABLED`. If every named property is `copy-on-write`, Snowflake sets it to `DISABLED`. |
| `identifier-fields.rely` | `RELY` on the table’s primary key | `true` or `false`. The table must already declare a primary key. |
| `schema.name-mapping.default` | Column name mapping | A valid Iceberg name-mapping value. Field IDs must exist on the table. |

Expand

Show lessSee more

**Target file size.** `67108864` is 64 MB, so Snowflake sets `TARGET_FILE_SIZE` to `64MB`.
`100000000` is between 64 MB and 128 MB, so Snowflake sets `TARGET_FILE_SIZE` to `64MB`.
On a Snowflake-managed table, the metadata Snowflake generates uses the byte count of that size.
On an externally managed table, the catalog keeps the number you wrote. Setting
`TARGET_FILE_SIZE = 'AUTO'` removes `write.target-file-size-bytes`.

**Snapshot age.** `86400000` is one day, so `DATA_RETENTION_TIME_IN_DAYS` is `1`. A value that
isn’t a whole number of days rounds up: `90000000` becomes 2 days. Account and edition retention
limits can still change the value Snowflake stores. For an externally managed table, refresh of a
value written outside this clause also rounds up to a whole number of days. See
[Metadata and retention for Apache Iceberg™ tables](/user-guide/tables-iceberg-metadata).

**Format version.** You can set `format-version` only when you create the table. To change the
version of an existing table, use `ALTER ICEBERG TABLE ... UPGRADE TO ICEBERG VERSION`.

**Write modes.** Snowflake has one parameter for DELETE, UPDATE, and MERGE. Setting
any of `write.delete.mode`, `write.update.mode`, or `write.merge.mode` to `merge-on-read`
turns merge-on-read on for all three operations in Snowflake. Unsetting any one of the three resets `ICEBERG_MERGE_ON_READ_BEHAVIOR`. On a Snowflake-managed table,
the next metadata generation rewrites all three properties from `ICEBERG_MERGE_ON_READ_BEHAVIOR`. For how Snowflake
publishes these properties, see
[Write-mode property synchronization](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-property-sync).

**Identifier fields.** `identifier-fields.rely` = `'true'` marks the primary key `RELY`.
`'false'` removes the property. The statement fails if the table has no primary key, or if the
same statement also specifies a conflicting `RELY` or `NORELY` on that key.

**Name mapping.** You can add `schema.name-mapping.default` to a table that doesn’t have a mapping.
You can’t replace a mapping the table already has.

### View a table’s properties

[SYSTEM$READ\_ICEBERG\_TABLE\_PROPERTY](/sql-reference/functions/system_read_iceberg_table_property) reads properties from the table’s
metadata file. Omit the property name to return every property as a JSON object:

Copy code

```
SELECT PARSE_JSON(SYSTEM$READ_ICEBERG_TABLE_PROPERTY('my_iceberg_table'));

SELECT SYSTEM$READ_ICEBERG_TABLE_PROPERTY('my_iceberg_table', 'write.delete.mode');
```

The function returns the table’s latest properties, including a property you just set.

## Limitations and considerations

- On `ALTER ICEBERG TABLE`, you can’t set or unset `format-version`.
- A catalog-linked database rejects the clause when its allowed write operations don’t include
  property updates.
- For a Snowflake-managed table, a key that maps to a Snowflake setting is rewritten from that
  setting the next time Snowflake generates metadata.
- Snowflake doesn’t use `history.expire.min-snapshots-to-keep` when it expires snapshots. You can
  still store the property.

### Properties you can’t set

Snowflake rejects these keys on `CREATE`, `ALTER ... SET`, and `ALTER ... UNSET`.

| Key | Why |
| --- | --- |
| `write.location-provider.impl`, `write.data.path`, `write.metadata.path`, `write.folder-storage.path`, `write.object-storage.path` | Snowflake chooses where table files are written. |
| `s3.sse.key`, `s3.sse.type`, `encryption.enabled` | Snowflake manages encryption. |
| Any key that starts with `write.orc.` | Snowflake writes Parquet files. |
| `uuid`, `snapshot-count`, `current-snapshot-id`, `current-snapshot-summary`, `current-snapshot-timestamp-ms`, `current-schema`, `default-partition-spec`, `default-sort-order` | Iceberg derives these from the table metadata. |

Expand

Show lessSee more

These keys are accepted only at one value. `ALTER ... UNSET` is rejected. To replace a different
stored value, set the supported value.

| Key | Only accepted value |
| --- | --- |
| `write.format.default` | `parquet` |
| `write.delete.format.default` | `parquet` |
| `write.delete.isolation-level`, `write.update.isolation-level`, `write.merge.isolation-level` | `snapshot` |

Expand

Show lessSee more

You can’t set `gc.enabled`. You can remove a stored value:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table UNSET TABLE_PROPERTIES ('gc.enabled');
```

### Values Snowflake checks

Snowflake accepts the following keys only when the value has the shape below. `UNSET` isn’t
checked, so you can remove a stored value that would now be rejected. Extra spaces around a number
are rejected.

| Key | Accepted value |
| --- | --- |
| `history.expire.max-snapshot-age-ms` | A whole number of milliseconds, 0 or greater. |
| `history.expire.min-snapshots-to-keep`, `history.expire.max-snapshots-to-keep` | An integer. |
| `history.expire.max-ref-age-ms` | An integer. |
| `commit.retry.num-retries`, `commit.retry.min-wait-ms`, `commit.retry.max-wait-ms`, `commit.retry.total-timeout-ms` | An integer, 0 or greater. |
| `commit.manifest.target-size-bytes` | An integer. |
| `commit.manifest.min-count-to-merge`, `write.summary.partition-limit`, `write.metadata.previous-versions-max`, `write.metadata.metrics.max-inferred-column-defaults`, `write.manifest.compression-level` | An integer. |
| `write.metadata.metrics.default`, `write.metadata.metrics.column.<column>` | `none`, `counts`, `full`, or `truncate(<n>)`, where `<n>` is a positive integer. On a Snowflake-managed table, `<column>` must exist. |
| `write.manifest.compression-codec` | For format version 2 or 3: `uncompressed`, `snappy`, `gzip`, or `zstd`. For format version 4: a Parquet compression codec. |

Expand

Show lessSee more

## Related topics

- [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake): create a Snowflake-managed table, including `TABLE_PROPERTIES`.
- [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest): create an externally managed REST catalog table.
- [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table): set or unset properties on an existing table.
- [SYSTEM$READ\_ICEBERG\_TABLE\_PROPERTY](/sql-reference/functions/system_read_iceberg_table_property): read properties from the metadata file.
- [Metadata and retention for Apache Iceberg™ tables](/user-guide/tables-iceberg-metadata): retention and how refresh converts snapshot age.
