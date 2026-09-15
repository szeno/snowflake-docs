[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Query mirrored data

Each mirror creates target tables and companion objects in the target database. This page covers
how to query them, how to read the change feed, and how to use the `$live` view for low-latency
access.

## Roles and permissions

Reading mirrored data is governed by the **`<target_database>_admin`** database role inside the
target database. This role has:

- `USAGE` on every target schema
- `SELECT` on every target table, `$changes` change-feed table, `$live` view, and
  `SNOWFLAKE_CDC_LOGS` metalog tables

A role that holds only `<target_database>_admin` (without `ACCOUNTADMIN`) can query all of these
objects directly.

`create_mirror` grants this role to the invoker with `WITH GRANT OPTION`, so the invoker can
delegate read access to other roles:

Copy code

```
GRANT DATABASE ROLE POSTGRESMIRRORTOSNOWFLAKE.POSTGRESMIRRORTOSNOWFLAKE_admin TO ROLE analytics;
```

For the role that governs managing mirrors (create, alter, drop), see
[Manage and monitor mirrors](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#roles-and-permissions).

## Access the target database

Target tables live in `<target_database>.<schema>.<table>` and can be queried like any other
Snowflake table:

Copy code

```
SELECT COUNT(*) FROM POSTGRESMIRRORTOSNOWFLAKE.PUBLIC.READINGS;
```

Each source table has three derived objects in the target database:

- **`<schema>.<table>`**: The materialized target table, updated on the mirror’s
  `refresh_interval`.
- **`<schema>.<table>$changes`**: The change log table (Iceberg, auto-refreshed from the source).
  Contains system columns plus the source data columns.
- **`<schema>.<table>$live`**: A view that combines the target table with pending change log
  entries, so readers see every committed change from the source with minimal additional latency.

## Query at low latency with `$live`

The `$live` view combines the target table with not-yet-merged rows from `$changes`, so readers
see every committed source change without waiting for the next apply run.

Copy code

```
SELECT COUNT(*) FROM POSTGRESMIRRORTOSNOWFLAKE.PUBLIC.READINGS$live;
```

A large gap between counts on the target table and the `$live` view means many changes are pending and will be merged on the next apply run.

The `$live` view refreshes as soon as auto-refresh picks up new rows in the underlying `$changes`
table (every 30 seconds), so `$live` lag is independent of `refresh_interval`. The
trade-off is query cost: `$live` has to scan all `$changes` rows not yet merged into the target,
so queries get more expensive as the backlog grows. Pairing a small `$live` scan with a larger
`refresh_interval` is a good way to keep apply costs down while keeping read lag low.

Note

`$live` views aren’t transactional. Because `$changes` rows arrive incrementally, a `$live` view
can expose a partial transaction where some rows are visible before others. If you need transactional consistency, query the target tables instead.

## Query changes with the `$changes` table

Each mirrored table has a companion `$changes` table (for example, `orders_db.public.orders$changes`). It is a rolling **7-day change feed**: every insert, update, and delete that happens on the
source PostgreSQL table shows up here as a queryable row, with a `_change_type` column (`I` for insert, `D` for delete; updates appear as a delete/insert pair).

You can query `$changes` directly to build pipelines, audit trails, or point-in-time reads.

### Snapshotting

When a table is **added to a mirror for the first time,** whether by creating the mirror, adding a table explicitly, or creating a new table inside a schema that is already mirrored, the mirror needs a full baseline copy of any existing rows before the change feed can start. During this period the table shows as `SNAPSHOTTING` in `list_mirrored_tables`. No changes are lost; the feed starts automatically once the copy completes.

This is the only situation that triggers a full data copy. No DDL on an already-mirrored table causes a re-snapshot.

### DDL updates in `$changes`

When you run a **column-level DDL** on a mirrored table, `$changes` is immediately re-pointed to a brand-new, empty table with the updated column layout. The previous change history is no longer visible in `$changes` from that point on.

| PostgreSQL DDL | What happens |
| --- | --- |
| `ALTER TABLE ... ADD COLUMN` | A new `$changes` table is created with the new column included. Old rows are gone from the feed; new rows will have a value for the new column. |
| `ALTER TABLE ... DROP COLUMN` | A new `$changes` table is created with the column removed. Old rows are gone from the feed. |
| `ALTER TABLE ... RENAME COLUMN` | A new `$changes` table is created with the column under its new name. Old rows are gone from the feed. |

Expand

Show lessSee more

In other words: **after a column change, `$changes` only contains rows that were written after the DDL**. Any rows from before the column change are gone from the feed. The new `$changes` table’s `_data_version` carries forward from the previous table’s last value rather than resetting to 1, so consumers that use `_data_version` to detect a fresh start should treat any increase as a signal to reset state.

The underlying data files from before the DDL are not immediately deleted; they continue to exist for up to 7 days before being cleaned up, but they are no longer exposed through `$changes`.

If you have a pipeline or query that reads `$changes` and depends on seeing the full 7-day history, be aware that a column DDL will truncate that window back to zero at the moment it is applied.

## Check row version with `_data_version`

Every row in `$changes` carries a `_data_version` integer. Unlike the column DDL case above, these operations do not replace `$changes` with a new empty table; the feed keeps running and all existing rows remain visible. However, they still mark a new generation in the system: the `_data_version` value increments at the boundary, signaling that rows before and after that point should not be treated as part of the same continuous sequence. Consumers should treat a version bump as a cue to reset their bookmarks or deduplication state.

| PostgreSQL DDL | What happens |
| --- | --- |
| `TRUNCATE` | All existing rows on the source were wiped. `_data_version` bumps to mark the clean-slate boundary. |
| `ALTER TABLE ... ADD PRIMARY KEY` | The table gains the ability to accept updates and deletes (it was insert-only before). `_data_version` bumps to separate the two eras. |
| `ALTER TABLE ... DROP CONSTRAINT ... (primary key)` | The table reverts to insert-only mode. Same version bump. |
| `ALTER TABLE ... RENAME TO` | The table and its `$changes` companion are renamed on Snowflake. `_data_version` bumps to keep change batches from before and after the rename from being confused with each other. |
| `ALTER TABLE ... SET SCHEMA` | Same as a rename but the table moves to a different schema. |
| `ALTER SCHEMA ... RENAME TO` | All tables in the renamed schema are renamed on Snowflake simultaneously, each with a `_data_version` bump. |

Expand

Show lessSee more

## Use Cortex Search on mirrored tables

Change tracking is automatically enabled on mirrored target tables and `$changes` tables. This
satisfies the
[change tracking requirement](/sql-reference/sql/create-cortex-search#label-cortex-search-change-tracking-requirements)
for Cortex Search Services, so you can build a Cortex Search Service on any mirrored table the
same way you would on any other Snowflake table. See
[Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) for setup
instructions.
