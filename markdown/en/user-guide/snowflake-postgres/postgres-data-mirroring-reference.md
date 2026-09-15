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
| `ALTER_MIRROR(...)` | Change the refresh interval, or add/remove tables and schemas. |
| `DROP_MIRROR('<name>')` | Remove a mirror and clean up all associated infrastructure. The target database is left in place unless called with `DROP_TARGET_DATABASE => true`. |
| `DESCRIBE_MIRROR('<name>')` | Return configuration and runtime state for a single mirror, including recent apply run durations. |
| `REFRESH_MIRROR('<name>')` | Apply pending changes to a mirror immediately and clear `last_apply_time`. |
| `SUSPEND_MIRROR('<name>')` | Stop scheduling new apply runs for a mirror. An existing, in-flight run finishes naturally. |
| `RESTART_MIRROR('<name>'[, truncate_feed])` | Suspend the task, wait for any in-flight execution to finish, tell the source Postgres to RESTART the publication, then resume the task. Both modes re-snapshot all mirrored tables and rebuild `$changes` from a fresh baseline. Default (soft restart) preserves queued operations in the source-side metalog; pass `truncate_feed => TRUE` (hard restart) to truncate the metalog first. |
| `LIST_MIRRORS([<instance>])` | Return one row per mirror on the given Postgres instance. Called without arguments, returns all mirrors visible to the current role. |
| `LIST_MIRRORED_TABLES('<name>')` | Return one row per source table with its replication state (`SNAPSHOTTING` or `REPLICATING`). |
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
| `postgres_tables` | One of `postgres_tables` or `postgres_schemas` | Fully qualified source table names (`schema.table`). |
| `postgres_schemas` | One of `postgres_tables` or `postgres_schemas` | Source schema names. All current and future tables in the schema are included. |
| `refresh_interval` | No | Merge cadence. Accepted values: `'30 seconds'`, `'1 minute'`, `'10 minutes'`, `'1 hour'`, `'1 day'`. Maximum value is `'1 day'`. Default: `'10 minutes'`. |
| `target_table_type` | No | Physical format of the target tables. `SNOWFLAKE` (default) creates standard Snowflake tables. `ICEBERG` creates Snowflake-managed Iceberg tables in Snowflake-managed storage. |
| `warehouse` | No | Run the apply task on this user-managed warehouse instead of serverless compute. |

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
| `_is_update` | `boolean` | True on both the `I` and the `D` halves of an `UPDATE`; false on pure `INSERT` rows. |
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
