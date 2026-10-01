[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Mirror procedures reference

Reference for the mirror management procedures in the `snowflake.postgres` schema, the SQL
objects a mirror creates on the source and target, and the column layout of every `$changes`
change log table.

## Object layout

Each mirror creates several objects across the source and target:

| Object | Location | Name pattern | Purpose |
| --- | --- | --- | --- |
| Publication | Source PG | `<mirror_name>` | Drives logical replication |
| Replication slot | Source PG | `<mirror_name>` | Durable decoding cursor |
| Change log table | Source PG (Iceberg via pg\_lake) | `snowflake_cdc_logs.snowflake_cdc_<...>` | Per-table CDC feed |
| Metalog table | Source PG (Iceberg via pg\_lake) | `snowflake_cdc_logs.<mirror_name>` | Schema-change and batch queue |
| Target database | Snowflake | `<target_database>` | Holds materialized target tables |
| Target table | Snowflake | `<target_db>.<schema>.<table>` | Materialized copy of source |
| `$changes` table | Snowflake | `<target_db>.<schema>.<table>$changes` | Change log exposed via auto-refresh |
| `$live` view | Snowflake | `<target_db>.<schema>.<table>$live` | Target plus pending change log |

Expand

Show lessSee more

Identifiers are folded to uppercase on Snowflake so that schema, table, and column names are
case-insensitive in SQL.

## Mirror management procedures

All procedures live in Snowflake in the `snowflake.postgres` schema and require the `postgres_mirror_admin`
application role.

| Procedure | Description |
| --- | --- |
| `CREATE_MIRROR(...)` | Create a new mirror. Sets up the target database, apply task, and publication on the source. |
| `ALTER_MIRROR(...)` | Change the refresh interval, warehouse, or add/remove tables and schemas. |
| `DROP_MIRROR('<name>'[, drop_target_database])` | Remove a mirror and clean up all associated infrastructure. By default the target database is dropped with the mirror. Pass `drop_target_database => FALSE` to keep it. |
| `DESCRIBE_MIRROR('<name>')` | Return configuration and runtime state for a single mirror, including apply lag, last applied commit, and recent apply run durations. |
| `REFRESH_MIRROR('<name>')` | Apply pending changes to a mirror immediately and clear `last_apply_time`. |
| `SUSPEND_MIRROR('<name>')` | Stop scheduling new apply runs for a mirror. An existing, in-flight run finishes naturally. |
| `RESUME_MIRROR('<name>')` | Resume a suspended mirror in place. Fails with `RESTART_REQUIRED` if unapplied operations have aged out of the source metalog. |
| `RESTART_MIRROR('<name>'[, truncate_feed])` | Suspend the task, wait for any in-flight execution to finish, tell the source Postgres to RESTART the publication, then resume the task. Both modes re-snapshot all mirrored tables and rebuild `$changes` from a fresh baseline. Default (soft restart) preserves queued operations in the source-side metalog; pass `truncate_feed => TRUE` (hard restart) to truncate the metalog first. |
| `LIST_MIRRORS([<instance>])` | Return one row per mirror on the given Postgres instance. Called without arguments, returns all mirrors visible to the current role. |
| `LIST_MIRRORED_TABLES('<name>')` | Return one row per source table with its replication state and per-table snapshot progress. |
| `QUERY_ADMIN_LOG(...)` | Query mirror-internal events with optional filters by mirror name, level (`INFO`, `WARN`, `ERROR`, `DEBUG`), and timestamp. |
| `REFRESH_CHANGES_TABLE(<mirror>, <table>)` | Refresh the Iceberg metadata for one mirrored table’s $changes table to reduce $live view lag. |

Expand

Show lessSee more

### CREATE\_MIRROR parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `mirror_name` | Yes | Identifier for the mirror, also used as the publication name. Must be an unquoted identifier of 50 characters or fewer. Must be unique across all Postgres instances in the account. |
| `postgres_instance` | Yes | Name of the Postgres instance (case-sensitive). |
| `postgres_database` | Yes | Source database on the Postgres instance. |
| `target_database` | Yes | Snowflake database to create. |
| `postgres_tables` | At least one of `postgres_tables` or `postgres_schemas`; both are allowed | Fully qualified source table names (`schema.table`). |
| `postgres_schemas` | At least one of `postgres_tables` or `postgres_schemas`; both are allowed | Source schema names. All current and future tables in the schema are included. |
| `refresh_interval` | No | Merge cadence. Accepted values: `'30 seconds'`, `'1 minute'`, `'10 minutes'`, `'1 hour'`, `'1 day'`. Maximum value is `'1 day'`. Default: `'10 minutes'`. |
| `target_table_type` | No | Physical format of the target tables. `SNOWFLAKE` (default) creates standard Snowflake tables. `ICEBERG` creates Snowflake-managed Iceberg tables, on Snowflake-managed storage unless `external_volume` is set. |
| `warehouse` | No | Run the apply task on this user-managed warehouse instead of serverless compute. The apply task runs as the `snowflake` application, so grant `USAGE` on the warehouse to `APPLICATION snowflake` first. |
| `external_volume` | No | External volume for Iceberg target tables. Valid only with `target_table_type => 'ICEBERG'`. Default `NULL` uses Snowflake-managed storage. Grant `USAGE` on the volume to `APPLICATION snowflake` first. The volume is fixed after create; switching volumes means dropping and recreating the mirror. |

Expand

Show lessSee more

### ALTER\_MIRROR parameters

At least one of `refresh_interval`, `warehouse`, `add_tables`/`add_schemas`, or
`remove_tables`/`remove_schemas` is required.

| Parameter | Required | Description |
| --- | --- | --- |
| `mirror_name` | Yes | Name of an existing mirror. |
| `refresh_interval` | One of | New merge cadence. Same accepted values as `create_mirror`. |
| `add_tables` | One of | Fully qualified source table names to add. |
| `remove_tables` | One of | Fully qualified source table names to remove. |
| `add_schemas` | One of | Source schema names to add. All current and future tables in the schema are included. |
| `remove_schemas` | One of | Source schema names to remove. |
| `warehouse` | One of | Warehouse for the apply task. A warehouse name converts a serverless apply task to user-managed. `NULL` converts the task back to serverless. Omit the parameter to leave compute unchanged. `NULL` does not mean “leave this alone.” Grant `USAGE` on the warehouse to `APPLICATION snowflake` first. |

Expand

Show lessSee more

### DROP\_MIRROR parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `mirror_name` | Yes | Name of an existing mirror. |
| `drop_target_database` | No | When `TRUE` (the default), the target database is dropped with the mirror. Pass `FALSE` to keep the database and its target tables. |

Expand

Show lessSee more

### DESCRIBE\_MIRROR result columns

In addition to configuration and health columns (`status`, `error_message`, `last_operation_time`,
`recent_query_durations`, `postgres_status`, and others), `describe_mirror` returns:

| Column | Type | Description |
| --- | --- | --- |
| `feed_only` | `BOOLEAN` | When true, changes are ingested but not applied to target tables. |
| `apply_lag_seconds` | `NUMBER` | Apply-hop lag in seconds (flushed on Postgres to applied on the target). Never `NULL`. `0` when the target has applied every flushed operation. Add `postgres_status.cdc_flush_lag_seconds` for an end-to-end time lag. |
| `apply_lag_operations` | `NUMBER` | Apply-hop lag in operations. `0` when caught up. `NULL` when the source is unreachable or running `snowflake_cdc` older than 1.4. |
| `apply_lag_bytes` | `NUMBER` | Apply-hop lag in source WAL bytes. `0` when caught up. `NULL` when either watermark is unknown. |
| `last_applied_commit_lsn` | `NUMBER` | Source WAL position of the newest commit applied to the target. Use this for read-your-writes checks. `NULL` until the first change batch is applied. |
| `last_applied_commit_time` | `TIMESTAMP_NTZ` | When the commit behind `last_applied_commit_lsn` happened. Stays put on an idle mirror. |
| `external_volume` | `STRING` | External volume holding Iceberg target tables, or `NULL` for Snowflake-managed storage. |

Expand

Show lessSee more

### LIST\_MIRRORS result columns

Includes the usual per-mirror health fields plus:

| Column | Type | Description |
| --- | --- | --- |
| `initial_snapshot_tables_remaining` | `NUMBER` | How many tracked tables are still completing their **initial** snapshot. `0` once every table has finished its first copy. Does not count a later re-snapshot; use `list_mirrored_tables` for that. Cheap to read on a fleet listing. |

Expand

Show lessSee more

### LIST\_MIRRORED\_TABLES result columns

`state` is always present. The snapshot-detail columns are read from the source at call time; they
are `NULL` if the source is unreachable or is running `snowflake_cdc` older than 1.5.

| Column | Type | Description |
| --- | --- | --- |
| `source_schema_name` | `STRING` | Schema of the source table in Postgres. |
| `source_table_name` | `STRING` | Name of the source table in Postgres. |
| `state` | `STRING` | Coarse target-side state: `SNAPSHOTTING` during initial copy, `REPLICATING` once caught up. |
| `snapshot_state` | `STRING` | Finer source-side state: `SNAPSHOTTING`, `ERROR`, `PENDING`, or `REPLICATING`. |
| `snapshot_percentage` | `FLOAT` | Progress of the running copy, `0`–`100`. `NULL` when no copy is running. |
| `snapshot_rows_processed` | `NUMBER` | Rows copied so far by the running snapshot. |
| `snapshot_total_rows` | `NUMBER` | Estimated total rows for the running snapshot. |
| `snapshot_reason` | `STRING` | Why the table is snapshotting, or last did: `initial_publication`, `table_restart`, or `ddl_resync`. |
| `pending_since` | `TIMESTAMP_NTZ` | When the current snapshot was queued. |
| `last_snapshot_error` | `STRING` | Most recent snapshot error for this table, kept after recovery. |
| `last_snapshot_error_at` | `TIMESTAMP_NTZ` | When that error occurred. |

Expand

Show lessSee more

## Change log schema

Every `$changes` table begins with system columns followed by the source table’s data columns:

| Column | Type | Description |
| --- | --- | --- |
| `_commit_lsn` | `bigint` | LSN of the commit that produced the row. Shared by every row in the same transaction. |
| `_lsn` | `bigint` | LSN of the row itself. Unique per change within a transaction. |
| `_xid` | `bigint` | Source transaction ID. |
| `_commit_time` | `timestamptz` | Commit timestamp of the source transaction. |
| `_change_type` | `VARCHAR` | `S` for initial snapshot, `I` for insert, `D` for delete. An `UPDATE` is emitted as a `D`/`I` pair. |
| `_is_update` | `boolean` | True on the `I` half of an `UPDATE`; false on pure `INSERT` rows and on the `D` half of an `UPDATE`. |
| `_data_version` | `int` | Increments when the table’s data generation changes (`TRUNCATE`, add/drop primary key). |

Expand

Show lessSee more

You can query the change log from the Snowflake side:

Copy code

```
-- On Snowflake (auto-refreshed copy in the target database):
SELECT _commit_lsn, _change_type, _is_update, id, name
FROM orders_db.public.orders$changes
ORDER BY _commit_lsn DESC, _lsn DESC
LIMIT 20;
```
