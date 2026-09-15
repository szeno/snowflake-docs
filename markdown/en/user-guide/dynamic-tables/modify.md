# Modify dynamic tables

As requirements change, you need to modify dynamic table pipelines: updating the definition, adding columns, or
changing the refresh mode. This page explains how to make those changes safely, what triggers reinitialization, and
how changes cascade through a pipeline.

Tip

Before you run a change, you can preview what it will do to the table’s next refresh. See
[Predict refresh behavior](/user-guide/dynamic-tables/predict-refresh).

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

For the full syntax reference, see [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) and [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

The most common modification, changing the definition, can be done with CREATE OR ALTER DYNAMIC TABLE.
CREATE OR ALTER is a declarative, idempotent command: you describe the full intended state of the dynamic table,
and Snowflake computes and applies what changes are needed. If the dynamic table doesn’t exist, it’s created.
If it exists, it’s altered to match the definition. If it already matches, it remains unchanged.

See [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

Copy code

```
-- Same as the dt_orders definition in create.mdx, with a new column added
CREATE OR ALTER DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        order_id, customer_id, order_date,
        ...
        order_date::DATE AS order_day  -- new column
    FROM raw_orders
    WHERE order_status != 'returned';
```

CREATE OR ALTER updates the definition of the existing dynamic table. The next refresh is a full reinitialization after a definition update. Consumers can still read from the existing dynamic table during this process.

### CREATE OR REPLACE DYNAMIC TABLE

CREATE OR REPLACE DYNAMIC TABLE can also modify the definition with DROP semantics. CREATE OR REPLACE is atomic: consumers (downstream dynamic tables and concurrent readers) see either the old definition or the new one, never a partial state. If the statement fails, the original dynamic table remains unchanged. CREATE OR REPLACE always triggers reinitialization, even if the new definition is identical to the previous one. With `INITIALIZE = ON_SCHEDULE`, the table is empty until the initial refresh completes. With the default `INITIALIZE = ON_CREATE`, the CREATE statement blocks until the initial refresh is done.

## ALTER DYNAMIC TABLE vs. CREATE OR REPLACE vs. CREATE OR ALTER

Some properties are mutable with ALTER DYNAMIC TABLE. Others require CREATE OR ALTER or CREATE OR REPLACE. CREATE OR REPLACE always reinitializes the dynamic table; CREATE OR ALTER reinitializes only for some changes. Use the following table to determine which approach you need.

| Change | ALTER | CREATE OR ALTER | CREATE OR REPLACE | Reinitializes? |
| --- | --- | --- | --- | --- |
| TARGET\_LAG | ✓ | ✓ | — | No |
| WAREHOUSE | ✓ | ✓ | — | No |
| REFRESH\_MODE | — | ✓ | ✓ | Depends on transition (see [Refresh mode transitions](#label-dynamic-tables-refresh-mode-transitions)) |
| Scheduling state (suspend/resume) | ✓ | — | — | No |
| SCHEDULER (ENABLE/DISABLE) | ✓ | ✓ | — | No |
| Clustering key | ✓ | ✓ | — | No (triggers reclustering; incurs compute cost) |
| Definition | — | ✓ | ✓ | Yes |
| Column additions or removals | — | ✓ | ✓ | Yes |
| Data type changes | — | — | ✓ | Yes |
| Rename | ✓ | — | — | No |
| Swap | ✓ | — | — | No |
| Frozen region (add/expand) | ✓ | ✓ | — | No |
| Frozen region (shrink) | ✓ | ✓ | — | Yes (active region reinitializes) |
| Frozen region (remove) | ✓ | ✓ | — | Yes (full reinitialization) |
| Storage lifecycle policy (shorten) | — | — | — | No (use CREATE OR REPLACE STORAGE LIFECYCLE POLICY) |
| Storage lifecycle policy (lengthen/add) | ✓ | — | — | Yes (previously expired rows must be reprocessed) |
| Storage lifecycle policy (remove/modify) | ✓ | — | — | Yes (full reinitialization) |

Expand

Show lessSee more

This table shows the most commonly changed properties. For the full list of ALTER-able properties,
see [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table).

For property changes that don’t require reinitialization, use ALTER DYNAMIC TABLE:

Copy code

```
ALTER DYNAMIC TABLE dt_orders SET
    TARGET_LAG = '5 minutes'
    WAREHOUSE = transform_wh_xl;
```

## Modify the definition

To change the definition of a dynamic table, use CREATE OR ALTER DYNAMIC TABLE or CREATE OR REPLACE DYNAMIC TABLE. There is no ALTER syntax for modifying the definition.

The following example adds a `discount_pct` column and changes the filter logic using CREATE OR ALTER:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        order_id, customer_id, order_date,
        ...
        COALESCE(discount_pct, 0) AS discount_pct,  -- new column
        order_status
    FROM raw_orders
    WHERE order_status NOT IN ('returned', 'cancelled');  -- updated filter
```

For the full `dt_orders` column list, see [Create a dynamic table](/user-guide/dynamic-tables/create).

## What triggers reinitialization

Reinitialization is a forced full refresh that reprocesses all data from scratch. The following changes trigger
reinitialization:

| Trigger | Notes |
| --- | --- |
| CREATE OR REPLACE on the dynamic table itself | Changing the definition, adding columns |
| CREATE OR REPLACE on an upstream base table, dynamic table, view, or UDF | Recreating a base table in a dbt run |
| Dropping and re-adding a referenced column on a base table | Even with the same name and type |
| Adding or removing a row access or masking policy on a base table | Incremental dynamic tables only |
| Changing REFRESH\_MODE across structural boundaries (for example, FULL to INCREMENTAL) | See [Refresh mode transitions](#label-dynamic-tables-refresh-mode-transitions) below |
| Failover of a replicated incremental dynamic table | Internal change-tracking state doesn’t transfer during failover, so a full refresh is required |
| Removing or modifying a frozen region on the dynamic table | The previously frozen region must be reprocessed. For details, see [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions). |
| Removing or modifying a storage lifecycle policy on the dynamic table | Previously expired rows must be reprocessed. The refresh-history `REINIT_REASON` column identifies the change. For details, see [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies). |

Expand

Show lessSee more

Important

If a dynamic table becomes stale beyond MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS, it can’t refresh automatically.
Unlike the triggers above, which cause automatic reinitialization, this requires manual intervention.
Recreate the dynamic table using CREATE OR REPLACE DYNAMIC TABLE to recover.

Note

Custom incremental dynamic tables don’t reinitialize when upstream schema changes occur. Instead,
the next refresh fails with a compile error. To recover, use `CREATE OR ALTER` with an updated `REFRESH USING`
definition (the next refresh after `CREATE OR ALTER` can be incremental). If you need to change `BACKFILL FROM` or
`START AT`, use CREATE OR REPLACE instead. For details, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).

### Refresh mode transitions

You can change REFRESH\_MODE with CREATE OR ALTER DYNAMIC TABLE. The effect depends on the transition:

| Transition | Effect |
| --- | --- |
| INCREMENTAL ↔ ADAPTIVE | Updates the refresh mode. No reinitialization. These modes share the same structural requirements (row ID columns and change tracking). |
| FULL ↔ INCREMENTAL or FULL ↔ ADAPTIVE | Updates the refresh mode and triggers reinitialization. These modes have different structural requirements. |
| Concrete mode (INCREMENTAL, FULL, or ADAPTIVE) → AUTO or AUTO → same concrete mode | Metadata-only change. The dynamic table continues using its current refresh mode. |

Expand

Show lessSee more

AUTO resolves to either INCREMENTAL or FULL at creation time (never ADAPTIVE). After resolution, switching between AUTO and the resolved concrete mode does not trigger reinitialization or change behavior.

#### Locking in a production mode

If you manage dynamic table definitions in version control and used AUTO during prototyping, you should change the definition to an explicit mode (for example, INCREMENTAL) before promoting to production. Existing dynamic tables deployed from the earlier definition keep their current refresh mode. New dynamic tables created from the updated definition use the explicit mode, making costs predictable. For more guidance, see [Choose a refresh mode](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-mode-decision).

### What doesn’t trigger reinitialization

The following changes do not trigger reinitialization:

| Change | Why it’s safe |
| --- | --- |
| ALTER … SET TARGET\_LAG or CREATE OR ALTER | Changes scheduling behavior only; doesn’t affect data |
| ALTER … SET WAREHOUSE or CREATE OR ALTER | Changes which warehouse runs the refresh; doesn’t affect data |
| ALTER … SUSPEND / RESUME | Changes scheduling state only; doesn’t affect data |
| ALTER … CLUSTER BY or CREATE OR ALTER | Adds reclustering; doesn’t reprocess data |
| ALTER … SET EXECUTE AS USER or CREATE OR ALTER | Changes the execution context for refreshes; doesn’t affect data |
| Adding or deleting an unreferenced column on a base table | The dynamic table’s column lineage isn’t affected |

Expand

Show lessSee more

Note

If you drop a column from a base table and re-add it with the same name and data type, Snowflake treats it as
a new column and triggers reinitialization.

## How changes cascade downstream

When you modify an upstream dynamic table, the effect depends on the type of change.

Property changes (ALTER): Changing TARGET\_LAG or WAREHOUSE on an upstream dynamic table does not trigger
reinitialization of downstream dynamic tables. Downstream tables continue to read from the upstream table’s
output through [snapshot-isolated](/user-guide/dynamic-tables/data-consistency) refreshes. However, changing
TARGET\_LAG can alter how frequently the upstream data is refreshed, which affects freshness for the entire
pipeline.

Definition or mode changes (CREATE OR ALTER): Changing a definition, refresh mode, or frozen region on an upstream dynamic table with CREATE OR ALTER might trigger reinitialization of that upstream table. However, it does not trigger reinitialization of downstream dynamic tables. Downstream tables continue to read from the upstream table’s output through [snapshot-isolated](/user-guide/dynamic-tables/data-consistency) refreshes.

Recreation (CREATE OR REPLACE): Recreating an upstream dynamic table triggers reinitialization of that
table. Downstream incremental dynamic tables also reinitialize on their next refresh, because the upstream
table is treated as a new object. Downstream full-refresh dynamic tables are unaffected because they already
reprocess all data on each refresh.

Refresh mode compatibility: An incremental downstream dynamic table can’t depend on a full-refresh
upstream dynamic table unless the upstream table provides row-level change information through a system-derived unique key or a frozen region (see [Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization)).
If you change an upstream table’s refresh mode from INCREMENTAL to FULL, verify that downstream tables are
compatible:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders%';
```

```
+-----------------+--------------+
| name            | refresh_mode |
+-----------------+--------------+
| DT_ORDERS_DAILY | INCREMENTAL  |
+-----------------+--------------+
```

If the downstream table is INCREMENTAL and the upstream is now FULL, recreate the downstream table with
`REFRESH_MODE = FULL` or verify that the upstream table provides a system-derived unique key or has a
frozen region.

## SELECT \* for automatic schema evolution

Dynamic tables using `SELECT *` automatically adapt to most base table schema changes. Snowflake handles
most schema changes incrementally without reinitialization.

Handled automatically (incremental refresh):

- Adding a column to the base table
- Dropping a column from the base table
- Type widening (for example, NUMBER(10) to NUMBER(38))
- Type narrowing (for example, NUMBER(20) to NUMBER(10)). The dynamic table retains the original wider type.
- Multiple sequential schema changes
- Changes propagate through the full pipeline graph. Each downstream dynamic table picks up the change incrementally on its next refresh: no cascading reinitialization occurs.

Existing rows receive NULL for newly added columns. No backfill occurs.

Handled automatically but triggers reinitialization:

- Dropping and re-adding a column with the same name (regardless of type)
- Adding a column with a DEFAULT value
- Adding a column to a base table when the dynamic table uses `SELECT *, expr AS alias` (the new column shifts ordinal positions)
- Changing a view definition that the dynamic table reads from (CREATE OR ALTER VIEW)
- Replacing the base table with CREATE OR REPLACE TABLE (creates a new table object)

Requires manual intervention (refresh fails):

- Incompatible type changes (for example, TEXT to INT in-place)
- Dynamic tables with explicit column specs in the CREATE statement
- Dropping a column referenced by CLUSTER BY

Use `SELECT * EXCLUDE (col1, col2)` to drop specific columns while retaining automatic evolution for
everything else:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT * EXCLUDE (order_status, unit_price)
    FROM raw_orders
    WHERE order_status != 'cancelled';
```

When a new column is added to `raw_orders`, `dt_orders` picks it up automatically on the next refresh.
Dropped columns disappear without requiring CREATE OR REPLACE.

When to use explicit column lists instead:

- When you need to transform, rename, or cast specific columns
- When you need to control column order in the output
- When the base table contains sensitive columns you must not propagate

If schema evolution does not work as expected, contact Snowflake Support to verify that the schema evolution
feature is enabled for your account.

## Safe schema evolution workflow

For most schema changes, use CREATE OR ALTER DYNAMIC TABLE or CREATE OR REPLACE DYNAMIC TABLE.

CREATE OR ALTER performs schema updates immediately: added columns are visible right away but contain null values until the next refresh, and renamed columns (last columns only) are also immediately visible with null values until the next refresh.

CREATE OR REPLACE is atomic: Snowflake creates the replacement as a hidden table, runs the initial refresh, then atomically swaps it in. Downstream tables see either the old or new version, never a partial state. Downstream incremental dynamic tables reinitialize automatically on their next refresh.

To evolve the schema without reinitializing, use a frozen region to protect stable data while modifying the
active region.

### Advanced: when to suspend downstream

In most cases you do not need to suspend downstream tables. Consider suspending only when:

- dbt concurrent replacement races: Multiple dbt threads running CREATE OR REPLACE on related tables can
  create transient resolution failures. Suspend downstream tables before the batch and resume after.
- Cost control: If a downstream table is expensive to reinitialize (large data volume), suspend it to
  defer the reinitialization until an off-peak window.
- Streams on downstream dynamic tables: Streams on a dynamic table lose their offset when the table
  reinitializes. Suspend the downstream table, consume the stream first, then resume.

When you do suspend, complete all steps in the same session. If a suspended table exceeds
MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS without resuming, it must be fully recreated.

## Rename a dynamic table

Renaming is useful when you want to replace a dynamic table while keeping existing scripts that reference the
original name. Use `ALTER DYNAMIC TABLE ... RENAME TO` to rename a dynamic table.

Important

Renaming a dynamic table does not update references in downstream dynamic table definitions. If
`dt_orders_daily` references `dt_orders` by name, renaming `dt_orders` breaks `dt_orders_daily` on the
next refresh. Recreate downstream tables after renaming an upstream dependency.

## Swap dynamic tables

Swapping exchanges two dynamic tables’ names and contents atomically. This is useful for blue-green
deployments: build and validate a new version, then swap it into place.

You can only swap a dynamic table with another dynamic table. Use `ALTER DYNAMIC TABLE <name> SWAP WITH <other_name>` to
perform the swap.

After the swap, `dt_orders` contains the data and definition that `dt_orders_v2` had, and vice versa.
Downstream tables that reference `dt_orders` by name now read from the swapped-in version.

## Add clustering keys

You can add or change clustering keys on an existing dynamic table with ALTER DYNAMIC TABLE, and the change
takes effect without reinitialization. Clustering keys can improve both query performance and refresh speed
for dynamic tables that use incremental or full refresh modes.

For guidance on choosing clustering keys and measuring their effectiveness, see
[Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization) and
[Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization).

## What’s next

- To understand the differences between INCREMENTAL, FULL, AUTO, ADAPTIVE, and CUSTOM\_INCREMENTAL refresh modes, see
  [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To monitor refresh history and diagnose failures, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To troubleshoot refresh failures after pipeline changes, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
