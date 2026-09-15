# Dynamic table refresh modes

Every dynamic table has a refresh mode that controls how its contents are refreshed. There are four Snowflake-managed modes: ADAPTIVE, FULL, INCREMENTAL, and AUTO. For advanced use cases, [CUSTOM\_INCREMENTAL](/user-guide/dynamic-tables/custom-incrementalization) lets you define your own refresh logic. The refresh mode is set at creation time. To change it, recreate the dynamic table with CREATE OR REPLACE or use CREATE OR ALTER DYNAMIC TABLE. For details on which transitions trigger reinitialization, see [Refresh mode transitions](/user-guide/dynamic-tables/modify#label-dynamic-tables-refresh-mode-transitions).

Copy code

```
-- Set the refresh mode explicitly in the CREATE statement
CREATE OR REPLACE DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  REFRESH_MODE = ADAPTIVE  -- or FULL, AUTO, or INCREMENTAL
AS
  SELECT ... FROM raw_orders ...;
```

For the full CREATE syntax with all options, see [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

## ADAPTIVE refresh

ADAPTIVE refresh uses incremental refresh by default but [automatically reinitializes the dynamic table](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers) when
internal heuristics detect that an incremental refresh would be significantly more expensive than rebuilding
from scratch. After reinitialization completes, the dynamic table resumes incremental refreshes.

Tip

Use ADAPTIVE refresh mode as your preferred refresh mode for all incremental workloads.

### When reinitialization triggers

ADAPTIVE refresh triggers a reinitialization when Snowflake determines that an incremental refresh would be
more expensive than a reinitialization. Common scenarios that trigger reinitialization include:

- INSERT OVERWRITE on a base table (replaces all rows in a partition or the entire table).
- Bulk deletes or updates that affect a large fraction of the rows tracked by the dynamic table.

### When reinitialization typically does not trigger

ADAPTIVE refresh typically does not reinitialize in these cases:

- Expensive operators in the definition. If the dynamic table’s definition uses Cortex AI functions, user-defined
  functions (UDFs), or external functions, the heuristic typically skips reinitialization because the cost of re-executing
  those operators across all rows outweighs the benefit of a fresh build.
- Simple definitions. Dynamic tables whose definitions contain only projections, filters, or sorts typically do not
  trigger reinitialization because incremental refresh is efficient for these patterns.

### Observability

To check whether an ADAPTIVE dynamic table reinitializes, query the
[DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) function. Reinitializations
appear as rows with `REFRESH_ACTION = 'REINITIALIZE'`. To learn why a refresh used
`REFRESH_ACTION = 'REINITIALIZE'`, check the `REINIT_REASON` column in
[DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history).

Tip

To reduce the impact of reinitializations, consider defining a frozen region on the dynamic table.
See [Frozen regions](/user-guide/dynamic-tables/frozen-regions).

### Use cases

Use ADAPTIVE refresh for any workload that is incrementalizable. The definition uses only [constructs supported for incremental refresh](/user-guide/dynamic-tables/supported-queries) (same requirement as INCREMENTAL mode). ADAPTIVE makes incremental processing even better, especially when base tables occasionally receive bulk loads (INSERT OVERWRITE) or large-scale updates, but most refreshes process small change volumes.

### Initialization warehouse

If you configure an [INITIALIZATION\_WAREHOUSE](/sql-reference/sql/create-dynamic-table), ADAPTIVE refresh
uses that warehouse for reinitializations. This lets you assign a larger warehouse for the occasional
full reinitialization without over-provisioning the warehouse used for routine incremental refreshes.

### Constraints

- ADAPTIVE requires the same incrementalizable query constructs as INCREMENTAL. If the definition contains constructs
  that don’t support incremental refresh, creation fails with a SQL compilation error.
- ADAPTIVE has the same pipeline constraint as INCREMENTAL: it can only be downstream from a FULL-refresh
  dynamic table if the upstream table has a system-derived unique key or a frozen region.
- ADAPTIVE dynamic tables can be upstream or downstream of other ADAPTIVE or INCREMENTAL dynamic tables.

### Example

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders_adaptive
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  INITIALIZATION_WAREHOUSE = transform_wh_xl
  REFRESH_MODE = ADAPTIVE
AS
  SELECT order_id, customer_id, order_date, total_amount
  FROM raw_orders
  WHERE order_status = 'COMPLETED';
```

In this example, `raw_orders` normally receives appended rows throughout the day (handled incrementally).
Periodically, an upstream ETL process runs INSERT OVERWRITE to reload the table. When that happens, ADAPTIVE
refresh detects the large change and reinitializes using `large_init_wh`, then resumes incremental refreshes
on the next cycle.

## INCREMENTAL refresh

An incremental refresh analyzes only the data that changed since the last refresh and merges those changes into the dynamic
table. This is typically the most efficient mode because it avoids reprocessing data that hasn’t changed.

Use an incremental refresh when:

- The definition uses only [constructs supported for incremental refresh](/user-guide/dynamic-tables/supported-queries).
- Fewer than five percent of the base table data changes between refreshes.
- You want to minimize warehouse compute cost per refresh.

If the definition contains a construct that doesn’t support incremental refresh, creation fails with a SQL compilation error identifying which construct is incompatible.

## FULL refresh

A full refresh re-executes the entire definition against the current state of all base tables and replaces the materialized output with the new query results.

Use a full refresh when:

- The definition uses constructs not supported by incremental refresh (for example, INTERSECT, EXCEPT, or
  exact percentile functions like `PERCENTILE_CONT`).
- A large fraction of the base table data changes between refreshes, making incremental processing more expensive than a
  full scan.
- You need predictable performance regardless of how much data changes between refreshes.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_non_null_orders
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
  REFRESH_MODE = FULL
AS
  SELECT order_id, product_name, quantity, unit_price
  FROM raw_orders
  EXCEPT
  SELECT order_id, product_name, quantity, unit_price
  FROM raw_orders
  WHERE order_status IS NULL;
```

Because EXCEPT is not supported for incremental refresh, this definition requires `REFRESH_MODE = FULL`.

### Why some computations require full refresh

Incremental refresh works by processing only the rows that changed since the last refresh. This is efficient when
the output for each new row can be computed on its own (for example, filtering rows, applying a format function, or
joining new orders against a customer table). The new rows don’t affect the results that were already computed for
previous rows.

But some computations depend on the relationship between all rows, not just the new ones. Consider finding
the median order value: if you have 1,000 orders and 5 new ones arrive, the median can shift. To find the
new median, you need to re-sort all 1,005 values and pick the middle one. There is no shortcut that lets you
update the answer by looking at only the 5 new rows.

These computations fundamentally require seeing all data on every refresh:

| Computation | Why it needs all rows | Example |
| --- | --- | --- |
| Exact percentile or median | Adding one row can shift which value lands in the middle of the sorted list. | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount)` |
| Set difference or intersection | Determining what’s in one set but not another requires comparing both full sets. | `SELECT ... EXCEPT SELECT ...` |

Expand

Show lessSee more

Full refresh is required because these computations need access to all rows. Set
`REFRESH_MODE = FULL` explicitly so that anyone reading the DDL understands the cost trade-off.

### Common workloads where full refresh is the right starting point

Incremental refresh is designed for workloads where a small fraction of data changes between refreshes. When the
data change pattern does not fit this model, full refresh is the appropriate starting mode for these workloads.

- Bulk-reload or truncate-and-replace patterns. When an upstream system replaces all rows on every load cycle,
  incremental refresh does strictly more work than full refresh. Set `REFRESH_MODE = FULL`. If the INSERT OVERWRITE
  doesn’t change actual data values and you can define a primary key with RELY, incremental refresh can still be
  efficient. For details on optimizing INSERT OVERWRITE workloads with primary keys, see
  [Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization).
- Dimension tables refreshed wholesale. Small-to-medium dimension tables that are periodically replaced in their
  entirety are faster to rebuild than to diff.
- Definitions that stack multiple blocking operators. When a query combines several blocking operators
  (GROUP BY, DISTINCT, window functions), full refresh can outperform incremental. See
  [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization) for guidance on splitting complex queries.
- High-churn workloads with heavy deletes. When base tables regularly purge large volumes of expired data,
  incremental refresh must scan many micro-partition files to identify deleted rows. Full refresh avoids this
  overhead entirely.

To determine whether incremental refresh is helping or hurting an existing dynamic table, compare average refresh
times using [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history). For details,
see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).

## AUTO refresh

AUTO is the default refresh mode. When you set `REFRESH_MODE = AUTO` (or omit the parameter entirely), Snowflake
evaluates the definition once at creation time and resolves it to either INCREMENTAL or FULL. After creation, the resolved
mode is locked in and does not change. For the full CREATE syntax with all options, see [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

Important

AUTO resolves once at creation time. It does not re-evaluate on subsequent refreshes. If something changes
later (for example, an upstream view is modified so that incremental refresh is no longer supported), refreshes fail
rather than switching to full refresh without a warning. To change the refresh mode, recreate the dynamic table with
CREATE OR REPLACE DYNAMIC TABLE.

### How AUTO chooses

Snowflake examines the definition for constructs, operators, functions, and base table properties. If the definition
supports incremental refresh and Snowflake expects it to be the more cost- and time-effective choice, AUTO resolves to
INCREMENTAL. If any part of the definition is incompatible, or if the definition complexity makes performance hard to predict,
Snowflake resolves to FULL. AUTO does not resolve to ADAPTIVE; to use ADAPTIVE refresh, set `REFRESH_MODE = ADAPTIVE` explicitly.

When AUTO resolves to FULL, the CREATE statement succeeds and its result message indicates why FULL was chosen. Verify the resolved mode after creation with SHOW DYNAMIC TABLES.

### Verify the resolved mode

Run SHOW DYNAMIC TABLES and inspect the `refresh_mode` and `refresh_mode_reason` columns:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders' ->> SELECT "name", "refresh_mode", "refresh_mode_reason" FROM $1;
```

```
+-------------------+--------------+---------------------+
| name              | refresh_mode | refresh_mode_reason |
|-------------------+--------------+---------------------|
| DT_ORDERS         | INCREMENTAL  | NULL                |
+-------------------+--------------+---------------------+
```

When `refresh_mode` is INCREMENTAL, `refresh_mode_reason` is NULL. When AUTO resolves to FULL, the
`refresh_mode_reason` column explains why incremental refresh wasn’t possible:

```
+------------------------+--------------+-------------------------------------------------------+
| name                   | refresh_mode | refresh_mode_reason                                   |
|------------------------+--------------+-------------------------------------------------------|
| DT_NON_NULL_ORDERS     | FULL         | Unsupported query operator type: SetOperation[EXCEPT] |
+------------------------+--------------+-------------------------------------------------------+
```

Tip

In production, set the refresh mode to ADAPTIVE, FULL, or INCREMENTAL explicitly rather than relying on AUTO. Explicit modes make costs predictable and prevent silent fallback to full refresh. Use AUTO for exploration and prototyping, then lock in the resolved mode before promoting to production.

## Custom incrementalization

When standard refresh modes can’t express your transformation, custom incrementalization lets you define
refresh logic as MERGE or INSERT DML inside a `REFRESH USING` clause. Custom incremental dynamic tables
bypass standard query analysis entirely. You take full control of how changes are applied to the table.

For syntax and examples, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).

## Choose a refresh mode

Use this table to decide which refresh mode to set for your dynamic table:

| Criteria | ADAPTIVE | FULL | INCREMENTAL | AUTO |
| --- | --- | --- | --- | --- |
| Best for | All workloads that can be incrementalized. Works great with workloads that have occasional bulk loads | Definitions with unsupported constructs or high change volumes | Append-heavy base tables with small change volumes | Exploration and prototyping |
| Cost per refresh | Usually lower; occasional reinitialization on bulk changes | Higher (reprocesses all data) | Lower (processes only changed data) | Depends on resolved mode |
| Unsupported constructs | Creation fails immediately (same as INCREMENTAL) | Always works | Creation fails immediately | Silently resolves to FULL |
| Mode visibility | Explicit in DDL | Explicit in DDL | Explicit in DDL | Requires SHOW DYNAMIC TABLES to verify |
| Production recommendation | Yes, when sources have mixed append and bulk-load patterns | Yes, when incremental isn’t possible or is slower | Yes, when the definition is compatible | Use for exploration, then set explicitly |

Expand

Show lessSee more

## Refresh mode can’t be changed with ALTER

ALTER DYNAMIC TABLE doesn’t support changing the refresh mode. To switch modes, use CREATE OR ALTER DYNAMIC TABLE or CREATE OR REPLACE DYNAMIC TABLE. For transition details, see [Refresh mode transitions](/user-guide/dynamic-tables/modify#label-dynamic-tables-refresh-mode-transitions).

Note

CREATE OR REPLACE drops and recreates the dynamic table, triggering [reinitialization](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers) for the table and its downstream dependencies.

## Incremental refresh does not have a fixed fallback threshold

The [refresh optimization](/user-guide/dynamic-tables/refresh-optimization) page recommends keeping changes to fewer
than five percent of data between refreshes for best incremental performance. The five-percent figure is a performance guideline.
Snowflake never automatically switches a dynamic table’s refresh mode based on change volume.

What does happen: when a large fraction of the base table data changes between refreshes, incremental refresh can become
slower than full refresh. The configured refresh mode stays as you set it. Snowflake does not automatically switch to a
different mode.

If incremental refresh is consistently slower than full refresh for your workload, recreate the dynamic table with
`REFRESH_MODE = FULL`.

Alternatively, if the slowdowns are caused by occasional bulk loads rather than
a consistently high change rate, consider `REFRESH_MODE = ADAPTIVE`, which automatically reinitializes
when large changes are detected and resumes incremental refresh afterward.

## Refresh modes in pipelines

Each dynamic table in a pipeline can have its own refresh mode. An upstream dynamic table using full refresh does not force
downstream dynamic tables to use full refresh.

One constraint applies: a dynamic table using INCREMENTAL or ADAPTIVE refresh mode can only be downstream from a dynamic table with full
refresh mode if the upstream full-refresh dynamic table has a system-derived unique key or a frozen region. For
more information, see [Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization) and
[Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions).

## What’s next

- [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization) to learn how to write
  definitions that work well with incremental refresh.
- [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries) for the full list of constructs
  compatible with incremental refresh.
- [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring) to track refresh status, cost, and performance.
- [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag) to control how often refreshes are triggered.
- [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization) to define custom refresh logic
  with MERGE or INSERT DML.
- [Refresh mode transitions](/user-guide/dynamic-tables/modify#label-dynamic-tables-refresh-mode-transitions) to understand which mode changes trigger reinitialization.
