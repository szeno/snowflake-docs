# Time Travel for Apache Iceberg™ tables

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An Apache Iceberg™ table keeps a history of snapshots, where each snapshot is the state of the table at a point in time. You can query
an earlier snapshot of a table by using the [AT | BEFORE](/sql-reference/constructs/at-before) clause.

## Overview

Snowflake supports four ways to identify the snapshot that you want to query. This page covers Snowflake-managed and
externally managed Iceberg tables. Where a behavior applies to only one type, the section says so.

| AT clause parameter | Identifies a snapshot by | Use it when |
| --- | --- | --- |
| `VERSION_TAG` | The name of a version tag | You want a stable, named reference to a snapshot that other engines can also use. |
| `VERSION` | The Iceberg snapshot ID | You already know the exact snapshot you want. |
| `VERSION_REF` | The name of a tag or a branch | You have a reference name but don’t know whether it’s a tag or a branch. |
| `TIMESTAMP` | A point in time | You want the table as of a specific date and time. |

Expand

Show lessSee more

A version tag is the only one of these that you create and manage yourself. The others reference state that already exists.

## Version tags

A version tag is a named reference to a specific snapshot of a table. Snowflake stores version tags in the Iceberg table metadata,
so other Apache Iceberg query engines can read the same tags.

A version tag isn’t a [Snowflake governance tag](/user-guide/object-tagging/introduction). Governance tags classify objects
(for example, to mark a column as containing personal data) and use `WITH TAG` or `ALTER ICEBERG TABLE ... SET TAG`. A version
tag names an Iceberg snapshot.

The tag doesn’t move when the table gets a newer snapshot. To make an existing tag point at a different snapshot, move the tag.
One snapshot can have several tags. Each tag points at only one snapshot.

Use version tags to keep a meaningful snapshot available for as long as you need it: a quarter-end close, the state of a table
before a backfill, or a dataset that a downstream job must be able to reproduce.

On a Snowflake-managed table, while a version tag references a snapshot, Snowflake retains that snapshot and the data files it
needs, even if the table’s [data retention period](/user-guide/tables-iceberg-metadata#label-tables-iceberg-time-travel-retention-period)
has elapsed and even if table maintenance would otherwise remove the snapshot.

For the complete syntax, see [ALTER ICEBERG TABLE … VERSION\_TAG](/sql-reference/sql/alter-iceberg-table-version-tag).

### Create a version tag

To tag the table’s current snapshot, run an [ALTER ICEBERG TABLE … VERSION\_TAG](/sql-reference/sql/alter-iceberg-table-version-tag) command without an `AS OF` clause.
If the table has no current snapshot, the command fails:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table CREATE VERSION_TAG end_of_quarter;
```

To tag an earlier snapshot, specify it by snapshot ID:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG audit_2026_q1 AS OF VERSION 3821550127947089009;
```

You can also specify the snapshot by time, as a number of milliseconds since the Unix epoch. Snowflake tags the most recent snapshot
that was committed at or before that time. To convert a timestamp to milliseconds:

Copy code

```
SELECT DATE_PART(EPOCH_MILLISECOND, '2025-12-01 00:00:00'::TIMESTAMP_LTZ);

ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG before_backfill AS OF TIMESTAMP 1764547200000;
```

Tag names are case-sensitive and are stored exactly as you write them, so `nightly` and `NIGHTLY` are two different tags. A tag name
can’t be empty, can’t be `main` in any letter case, and can’t match the name of a branch on the same table.

### Find a snapshot to tag

To list the data snapshots that Snowflake has indexed for a table, query the
[GET\_TABLE\_VERSIONS](/sql-reference/functions/get_table_versions) Information Schema table function:

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.GET_TABLE_VERSIONS('my_db.my_schema.my_iceberg_table'));
```

The function returns one row per indexed data snapshot, with the following columns:

| Column | Description |
| --- | --- |
| `VERSION_ID` | The Iceberg snapshot ID. Use this value with `AS OF VERSION` or `AT(VERSION => ...)`. |
| `VERSION_CREATED_AT` | When the snapshot was created. |
| `QUERY_ID` | The query that produced the snapshot. |

Expand

Show lessSee more

### Query a table at a version tag

Specify the tag name in an `AT` clause:

Copy code

```
SELECT * FROM my_iceberg_table AT(VERSION_TAG => 'audit_2026_q1');
```

The query returns the table as it was in the tagged snapshot. Writes to the table after the tag was created don’t affect the result,
and querying at a tag doesn’t affect the current state of the table.

You can use a version tag in a SELECT statement, including in joins, views, and as the source of an `INSERT ... SELECT`,
`MERGE`, or `CREATE TABLE ... AS SELECT` statement. Don’t use a version tag as the target of INSERT, UPDATE, DELETE, or MERGE.

### Repoint a version tag

To move an existing tag to a different snapshot, use `ALTER VERSION_TAG`:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  ALTER VERSION_TAG nightly AS OF VERSION 7245108833619203344;
```

The tag must already exist. To move a tag if it exists, or create it if it doesn’t, use `CREATE OR REPLACE VERSION_TAG`:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE OR REPLACE VERSION_TAG nightly AS OF VERSION 7245108833619203344;
```

### Set how long a tag is kept

By default, a version tag is kept until you drop it. To have Snowflake remove a tag automatically, add a `RETAIN` clause. `RETAIN`
is valid only with `AS OF`; `CREATE VERSION_TAG nightly RETAIN 7 DAYS` isn’t valid:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG audit_2026_q1 AS OF VERSION 3821550127947089009 RETAIN 7 DAYS;
```

Important

The retention period is measured from the time the *tagged snapshot* was committed, not from the time you create the tag. If you
tag a snapshot that was committed 10 days ago with `RETAIN 7 DAYS`, the tag is already past its retention period and Snowflake
can remove it during the next table maintenance operation.

Snowflake stores this value as the `max-reference-age-ms` property of the reference in the Iceberg table metadata, so other query
engines observe the same retention period.

To change the retention period of an existing tag, use `REPLACE VERSION_TAG`, which repoints the tag and sets the retention period
in one statement:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  REPLACE VERSION_TAG nightly AS OF VERSION 7245108833619203344 RETAIN 48 HOURS;
```

If you repoint a tag without specifying `RETAIN`, the tag keeps its current retention period.

### Drop a version tag

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table DROP VERSION_TAG nightly;
```

Queries that specify the tag fail after you drop it. Dropping a tag removes the name. It doesn’t delete data files, and it
doesn’t affect other tags, even if they reference the same snapshot.

After no tag references a snapshot, that snapshot and its data files follow the table’s normal data retention and maintenance
behavior, and Snowflake can remove them.

## Query a table at a snapshot ID

To query a snapshot directly, specify its Iceberg snapshot ID:

Copy code

```
SELECT * FROM my_iceberg_table AT(VERSION => 3821550127947089009);
```

Unlike a version tag, a snapshot ID doesn’t keep the snapshot available. If the snapshot is removed by the table’s data retention
policy or by table maintenance, the query fails. To keep a snapshot available, create a version tag that references it.

## Query a table at a reference name

Iceberg stores tags and branches in a single namespace, so a name identifies at most one reference of either kind. When you have a
reference name but don’t know whether it’s a tag or a branch, use `VERSION_REF`:

Copy code

```
SELECT * FROM my_iceberg_table AT(VERSION_REF => 'audit_2026_q1');
```

Snowflake looks up the name and resolves it to whichever reference it is. If no tag or branch on the table has that name, the
query fails.

## Query a table at a timestamp

To query a table as of a point in time, use the `TIMESTAMP` parameter:

Copy code

```
SELECT * FROM my_iceberg_table AT(TIMESTAMP => '2026-03-31 23:59:00'::TIMESTAMP_LTZ);
```

The `TIME_TRAVEL_TIMESTAMP_SOURCE` object parameter controls which timeline Snowflake uses to interpret the timestamp:

| Value | Description |
| --- | --- |
| `'SNOWFLAKE_METADATA'` | Uses the Snowflake transaction timeline. This is the default. |
| `'ICEBERG_METADATA'` | Uses the snapshot commit times recorded in the Iceberg table metadata. Supported for externally managed tables. Not supported for Snowflake-managed tables. |

Expand

Show lessSee more

You can set this parameter at the account, database, schema, or table level. For example:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET TIME_TRAVEL_TIMESTAMP_SOURCE = 'ICEBERG_METADATA';
```

## List the tags and branches on a table

To list version tags and branches, along with their retention settings, query the
[GET\_TABLE\_VERSION\_REFS](/sql-reference/functions/get_table_version_refs) Information Schema table function:

Copy code

```
SELECT reference_name, reference_type, version_id, version_created_at
  FROM TABLE(INFORMATION_SCHEMA.GET_TABLE_VERSION_REFS('my_iceberg_table'))
  WHERE reference_type = 'TAG';
```

To list every named ref:

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.GET_TABLE_VERSION_REFS('my_db.my_schema.my_iceberg_table'));
```

The function returns one row per indexed tag or branch whose target snapshot is present in the loaded metadata, with the following
columns:

| Column | Description |
| --- | --- |
| `REFERENCE_NAME` | The name of the tag or branch. |
| `REFERENCE_TYPE` | `TAG` or `BRANCH`. |
| `VERSION_ID` | The Iceberg snapshot ID that the reference points to. |
| `VERSION_CREATED_AT` | When that snapshot was committed. |
| `MAX_REFERENCE_AGE_IN_MS` | The retention period set by the `RETAIN` clause, in milliseconds. `NULL` if the reference has no retention period. |
| `MIN_SNAPSHOTS_TO_KEEP` | A branch retention setting. Always `NULL` for tags. |
| `MAX_SNAPSHOT_AGE_IN_MS` | A branch retention setting. Always `NULL` for tags. |

Expand

Show lessSee more

`GET_TABLE_VERSION_REFS` reads the Iceberg table metadata that Snowflake has indexed. For an externally managed table, refresh the
table to see references that another engine created. If the table uses automated refresh, the next refresh picks up the tag.
For a Snowflake-managed table, a tag that you just created appears after Snowflake next updates the table metadata.

To confirm that a tag you just created is queryable, run `SELECT ... AT(VERSION_TAG => '<tag_name>')`.

## Interoperability with external engines

Version tags are stored in the Iceberg table metadata, so other Apache Iceberg query engines can read them. For example, Apache Spark™
reads a tagged snapshot with `VERSION AS OF`:

Copy code

```
SELECT * FROM my_catalog.my_schema.my_iceberg_table VERSION AS OF 'audit_2026_q1';
```

How quickly a change becomes visible depends on the table type:

- **Snowflake-managed tables:** a tag that you create in Snowflake is available to queries in Snowflake immediately, and appears in
  the Iceberg table metadata after Snowflake next updates that metadata.
- **Externally managed tables:** if the table uses an Iceberg REST catalog, Snowflake commits the tag to that catalog as part of
  the statement, so other engines see it when the statement succeeds. For other catalog types, Snowflake records the tag in the
  Iceberg metadata it has already refreshed. A tag that another engine creates becomes available to Snowflake after the table is
  refreshed. If the table uses automated refresh, the next refresh picks up the tag. For more information, see
  [Refresh the table metadata](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata).

## Considerations and limitations

### Snowflake-managed and externally managed Iceberg tables

- The `BEFORE` keyword isn’t supported with `VERSION_TAG`, `VERSION_REF`, or `VERSION`. Use `AT` instead.
- Creating, repointing, and dropping a version tag requires the OWNERSHIP privilege on the table. Querying a table at a version
  tag requires the USAGE privilege on the database and schema and the SELECT privilege on the table.
- A query at an earlier snapshot uses the table’s current column definitions. If you rename a column, you must use the new name,
  even when you query a snapshot that was created before the rename. If you drop a column, it isn’t accessible at earlier
  snapshots.
- A tag and a branch on the same table can’t share a name.
- You can’t combine `OR REPLACE` and `IF NOT EXISTS` in the same `CREATE VERSION_TAG` statement.
- The `RETAIN` clause is valid only with `AS OF` on `CREATE VERSION_TAG` and `REPLACE VERSION_TAG`. It isn’t supported with
  `ALTER VERSION_TAG`.
- If you omit `AS OF` when you create a tag and the table has no current snapshot, the command fails.
- `AS OF TIMESTAMP` accepts an integer number of milliseconds since the Unix epoch, and resolves against the table’s main
  snapshot history. To tag a snapshot that exists only on a branch, use `AS OF VERSION`.
- Don’t use a version tag as the target of INSERT, UPDATE, DELETE, or MERGE.

### Snowflake-managed Iceberg tables

- A tag that you create is queryable in Snowflake immediately, and becomes visible to other query engines after Snowflake next
  updates the Iceberg table metadata.

### Externally managed Iceberg tables

- Tag DDL that uses an Iceberg REST catalog commits to that catalog. If another engine commits to the table at the same time, the
  statement can fail with a conflict. When it fails, the tag isn’t created or modified, and you can retry the statement.
- Snowflake discovers tags that other engines created when the table is refreshed. If the table uses automated refresh, the next
  refresh picks up the tag. A refresh also removes tags that were dropped externally and updates retention periods that changed.
- The external catalog controls snapshot expiration in cloud storage. Snowflake can still query a version tag when the snapshot
  is outside the Snowflake data retention period.
- The first query against a tagged snapshot that Snowflake hasn’t loaded yet takes longer, because Snowflake loads that snapshot
  on demand. Later queries against the same tag are faster.
- Setting `TIME_TRAVEL_TIMESTAMP_SOURCE = 'ICEBERG_METADATA'` is supported for externally managed tables and isn’t supported for
  Snowflake-managed tables.
