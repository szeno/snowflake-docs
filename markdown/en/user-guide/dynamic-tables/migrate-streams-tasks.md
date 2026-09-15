# Migrate from streams and tasks to dynamic tables

Dynamic tables replace imperative pipeline code (INSERT, MERGE, stored procedure calls) with a declarative model: you write a SELECT that describes the result you want, and Snowflake keeps it fresh.

This page covers how to convert streams-and-tasks pipelines to dynamic tables one task at a time.

## Concept map: streams and tasks to dynamic tables

| Streams and tasks concept | Dynamic table equivalent | Notes |
| --- | --- | --- |
| Base table | Base table | Same object, no change required. |
| Stream on base table | (built in) | Snowflake tracks changes automatically. You don’t create a separate stream. |
| Task body (`INSERT INTO ... SELECT ...`) | The definition in CREATE DYNAMIC TABLE … AS SELECT | Write only the SELECT. No DML statements (such as INSERT INTO or MERGE). |
| Task schedule (`SCHEDULE = '10 MINUTE'`) | TARGET\_LAG = ’10 minutes’ | TARGET\_LAG is a freshness goal, not a fixed interval. Snowflake decides when to refresh. |
| Task DAG (root task + child tasks) | Pipeline of dynamic tables | Intermediate dynamic tables use `TARGET_LAG = DOWNSTREAM`. The terminal dynamic table carries the freshness goal. |
| Root task | Terminal dynamic table (or controller dynamic table) | The terminal dynamic table drives the refresh schedule for the whole pipeline. |
| MERGE ON key WHEN MATCHED UPDATE … | `QUALIFY ROW_NUMBER() OVER (...) = 1` | Dynamic tables express “latest state per key” as a window function, not as DML. See the [SCD Type 1 example](#label-dynamic-tables-migrate-scd1). |
| `SYSTEM$STREAM_HAS_DATA()` check | (not needed) | Snowflake skips refreshes automatically when base tables haven’t changed. |

Expand

Show lessSee more

## Choose a migration strategy

Dynamic tables support two operational models. Choose the one that fits your team’s workflow.

### Self-refreshing dynamic tables (Snowflake manages timing)

Set a TARGET\_LAG value and Snowflake handles the refresh schedule. This is the simplest model and is suited for new pipelines or teams that want to reduce operational overhead.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
AS
    SELECT ...
    FROM raw_orders;
```

Best for:

- New pipelines where you don’t already have orchestration in place.
- Teams that want Snowflake to manage refresh timing and dependency ordering.
- Pipelines where a freshness goal (such as “no more than 10 minutes stale”) is the correct requirement.

### Orchestrator-managed dynamic tables (SCHEDULER = DISABLE)

If you already run an orchestrator (dbt, Airflow, or even tasks), create dynamic tables with `SCHEDULER = DISABLE`. Snowflake does not schedule refreshes automatically. You trigger each refresh manually or from your orchestrator. Refreshes do not cascade upstream or downstream.

Copy code

```
-- Create the dynamic table with scheduling disabled.
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    WAREHOUSE = transform_wh
    SCHEDULER = DISABLE
AS
    SELECT ...
    FROM raw_orders;

-- Trigger a refresh manually or from your orchestrator.
ALTER DYNAMIC TABLE dt_orders REFRESH;
```

Key behaviors:

- You can’t set TARGET\_LAG when using `SCHEDULER = DISABLE`.
- Refreshes with `SCHEDULER = DISABLE` do not cascade upstream or downstream. Each dynamic table refreshes independently.
- Your orchestrator controls the order, timing, and error handling.
- GA since March 2026.

Best for:

- Teams that want to keep their existing orchestrator while adopting declarative definitions.
- Pipelines that require explicit control over refresh order or conditional refresh logic.

## Decide whether to migrate a task

Evaluate each task individually against these criteria to decide whether it should migrate.

| Criterion | Migrate to dynamic tables | Stay on streams and tasks |
| --- | --- | --- |
| Pipeline logic | Pure SQL: SELECT, JOIN, GROUP BY, CASE WHEN, window functions, custom UDFs | Loops, cursors, multi-statement procedural blocks |
| DML operations | Inserts, updates, and deletes propagate from base tables through incremental refresh. | Explicit DELETE, TRUNCATE, or delete-before-insert patterns |
| Data sources | Snowflake tables, views | External tables, directory tables (not supported as dynamic table inputs) |
| Latency requirement | One minute minimum (TARGET\_LAG floor). Actual freshness depends on refresh duration and pipeline depth. | Sub-minute orchestration (tasks support one-second schedules) |
| Non-deterministic functions (RANDOM) | Forces FULL refresh with `REFRESH_MODE = AUTO`. Fails with explicit `REFRESH_MODE = INCREMENTAL`. | Supported natively |
| Side effects or external API calls | Not possible. Dynamic tables are pure SELECT statements. | Supported: external functions, notifications, stored procedure calls |
| Multi-table writes in one transaction | Not supported. Each dynamic table produces exactly one output. | One task can write to multiple tables in a single transaction. |
| Multi-statement transactions | One definition per dynamic table (single SELECT) | Tasks can execute arbitrary multi-statement transactions |
| SQL-expressible business rules | JOINs, CASE WHEN, UNIONs, and conditional aggregations all work in a definition. | Runtime-evaluated procedural logic (cursors, dynamic SQL dispatch) |

Expand

Show lessSee more

Important

Non-deterministic functions like `RANDOM()` force full refresh when `REFRESH_MODE = AUTO`. If you set
`REFRESH_MODE = INCREMENTAL` explicitly, the CREATE statement fails. Replace non-deterministic functions
with deterministic alternatives before migrating. Sequence functions (`NEXTVAL`) are not supported in
incremental refresh mode. See [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries) for the full compatibility matrix.

### Custom incremental dynamic tables

If your streams+tasks pipeline uses MERGE or INSERT DML, custom incremental dynamic tables accept the same patterns with less orchestration overhead. The mapping is nearly one-to-one:

| Streams + Tasks | Custom incremental dynamic table |
| --- | --- |
| Stream on base table | `CHANGES()` clause |
| `SYSTEM$STREAM_HAS_DATA()` check | Automatic (Snowflake handles) |
| Task schedule / CRON | `TARGET_LAG` |
| `MERGE INTO target` | `MERGE INTO SELF` |
| `INSERT INTO target` | `INSERT INTO SELF` |
| Stream metadata columns (`METADATA$ACTION`, `METADATA$ISUPDATE`) | Same columns from `CHANGES()` |
| Manual stream advancement | Automatic advancement by dynamic table |
| Task DAG (predecessors) | Pipeline (`TARGET_LAG = DOWNSTREAM`) |

Expand

Show lessSee more

Custom incremental dynamic tables remove the need to manage streams, tasks, and their orchestration separately. You write the same MERGE or INSERT logic inside REFRESH USING, and Snowflake handles scheduling, retries, and transactional guarantees.

For full details, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).

## Patterns that migrate well

The following patterns convert cleanly from streams and tasks to dynamic tables.

### Append-only ingestion

This is the simplest migration. A stream and task that inserts new rows into a target table becomes a single
dynamic table.

Set up the base table and sample data first. This example uses the same `raw_orders` table from
[Create your first dynamic table](/user-guide/dynamic-tables/create). If you already ran that tutorial, you can skip the setup step.

**Before: stream and task**

Copy code

```
CREATE OR REPLACE STREAM raw_orders_stream ON TABLE raw_orders APPEND_ONLY = TRUE;

CREATE OR REPLACE TABLE clean_orders (
    order_id       INT,
    customer_id    INT,
    order_date     TIMESTAMP_NTZ,
    product_name   VARCHAR,
    quantity       INT,
    unit_price     DECIMAL(10,2),
    line_total     DECIMAL(12,2),
    order_status   VARCHAR
);

CREATE OR REPLACE TASK load_clean_orders
    WAREHOUSE = transform_wh
    SCHEDULE = '10 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('raw_orders_stream')
AS
    INSERT INTO clean_orders
    SELECT
        order_id,
        customer_id,
        order_date,
        TRIM(UPPER(product_name)) AS product_name,
        quantity,
        unit_price,
        quantity * unit_price AS line_total,
        order_status
    FROM raw_orders_stream
    WHERE order_status != 'returned';

ALTER TASK load_clean_orders RESUME;
```

**After: dynamic table**

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_clean_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        order_id, customer_id, order_date,
        TRIM(UPPER(product_name)) AS product_name,
        quantity, unit_price,
        quantity * unit_price AS line_total,
        order_status
        -- remaining columns omitted for brevity
    FROM raw_orders
    WHERE order_status != 'returned';
```

The stream, target table DDL, task, and INSERT all collapse into one CREATE DYNAMIC TABLE statement. The SELECT reads from the base table directly: no stream required.

Important

The APPEND\_ONLY stream in the “Before” version only captured newly inserted rows. The dynamic table
accurately represents the current state of the base table matching the WHERE filter. If the base table only
receives INSERTs (common for raw landing tables), the results are equivalent. If the base table also receives
UPDATEs or DELETEs, the dynamic table reflects those changes as well.

Verify the dynamic table contents after the initial refresh completes.

Note

Stream-static joins (where a task joins a stream with a dimension table) aren’t supported in SELECT-based dynamic tables, but custom incremental dynamic tables support this pattern natively. See [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).

Copy code

```
SELECT * FROM dt_clean_orders ORDER BY order_id;
```

```
+----------+-------------+---------------------+--------------+----------+------------+------------+--------------+
| ORDER_ID | CUSTOMER_ID | ORDER_DATE          | PRODUCT_NAME | QUANTITY | UNIT_PRICE | LINE_TOTAL | ORDER_STATUS |
+----------+-------------+---------------------+--------------+----------+------------+------------+--------------+
|     1001 |           1 | 2025-01-15 08:30:00 | WIDGET A     |        3 |      29.99 |      89.97 | completed    |
|     1002 |           2 | 2025-01-15 09:45:00 | WIDGET B     |        1 |      49.99 |      49.99 | completed    |
|     1003 |           1 | 2025-01-15 14:20:00 | WIDGET A     |        2 |      29.99 |      59.98 | pending      |
|     1004 |           3 | 2025-01-16 10:00:00 | GADGET X     |        5 |      12.50 |      62.50 | completed    |
+----------+-------------+---------------------+--------------+----------+------------+------------+--------------+
```

### SCD Type 1 upsert

In a streams and tasks pipeline, SCD Type 1 (keep only the latest version of each record) typically uses a
MERGE statement. In a dynamic table, you express the same logic as a window function that picks the most
recent row per key.

**Before: stream and task with MERGE**

Copy code

```
CREATE OR REPLACE TABLE customer_updates (
    customer_id    INT,
    customer_name  VARCHAR,
    region         VARCHAR,
    segment        VARCHAR,
    updated_at     TIMESTAMP_NTZ
);

INSERT INTO customer_updates VALUES
    (1, 'Acme Corp',      'US-West',  'Enterprise', '2025-01-10 09:00:00'),
    (2, 'Globex Inc',     'US-East',  'Mid-Market', '2025-01-10 09:00:00'),
    (1, 'Acme Corp',      'US-West',  'Strategic',  '2025-01-15 14:00:00'),
    (3, 'Initech LLC',    'EU-West',  'Startup',    '2025-01-12 11:00:00');

CREATE OR REPLACE STREAM customer_updates_stream ON TABLE customer_updates;

CREATE OR REPLACE TABLE dim_customers_scd1 (
    customer_id    INT,
    customer_name  VARCHAR,
    region         VARCHAR,
    segment        VARCHAR,
    updated_at     TIMESTAMP_NTZ
);

CREATE OR REPLACE TASK merge_customers
    WAREHOUSE = transform_wh
    SCHEDULE = '10 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('customer_updates_stream')
AS
    MERGE INTO dim_customers_scd1 AS tgt
    USING (
        SELECT customer_id, customer_name, region, segment, updated_at
        FROM customer_updates_stream
        QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
    ) AS src
    ON tgt.customer_id = src.customer_id
    WHEN MATCHED THEN UPDATE SET
        tgt.customer_name = src.customer_name,
        tgt.region        = src.region,
        tgt.segment       = src.segment,
        tgt.updated_at    = src.updated_at
    WHEN NOT MATCHED THEN INSERT
        (customer_id, customer_name, region, segment, updated_at)
    VALUES
        (src.customer_id, src.customer_name, src.region, src.segment, src.updated_at);

ALTER TASK merge_customers RESUME;
```

**After: dynamic table**

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_dim_customers_scd1
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        customer_id,
        customer_name,
        region,
        segment,
        updated_at
    FROM customer_updates
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
```

The MERGE logic disappears entirely. The dynamic table always produces the latest version of each
customer. When a new row arrives in `customer_updates` with a newer `updated_at`, the next refresh
automatically picks it up.

Copy code

```
SELECT * FROM dt_dim_customers_scd1 ORDER BY customer_id;
```

```
+-------------+---------------+---------+------------+---------------------+
| CUSTOMER_ID | CUSTOMER_NAME | REGION  | SEGMENT    | UPDATED_AT          |
+-------------+---------------+---------+------------+---------------------+
|           1 | Acme Corp     | US-West | Strategic  | 2025-01-15 14:00:00 |
|           2 | Globex Inc    | US-East | Mid-Market | 2025-01-10 09:00:00 |
|           3 | Initech LLC   | EU-West | Startup    | 2025-01-12 11:00:00 |
+-------------+---------------+---------+------------+---------------------+
```

Customer 1 shows `Strategic` (the newer segment), not `Enterprise`. The ROW\_NUMBER window function
handles the “most recent wins” logic that MERGE previously performed.

### Multi-step pipeline (task DAG to dynamic table pipeline)

Intermediate dynamic tables use `TARGET_LAG = DOWNSTREAM`, meaning they refresh only when a downstream table with a time-based lag needs fresh data. The terminal dynamic table drives the schedule for the whole pipeline.

**Before: task DAG**

Copy code

```
-- Stage 1: clean raw orders
CREATE OR REPLACE TASK stage1_clean
    WAREHOUSE = transform_wh
    SCHEDULE = '30 MINUTE'
AS
    INSERT INTO dt_orders
    SELECT order_id, customer_id, order_date,
           TRIM(UPPER(product_name)) AS product_name,
           quantity, unit_price,
           quantity * unit_price AS line_total,
           order_status
    FROM raw_orders_stream
    WHERE order_status != 'returned';

-- Stage 2: join with customers (depends on stage1_clean)
CREATE OR REPLACE TASK stage2_enrich
    WAREHOUSE = transform_wh
    AFTER stage1_clean
AS
    INSERT INTO enriched_orders
    SELECT s.order_id, s.order_date, s.product_name, s.line_total,
           c.customer_name, c.region, c.segment
    FROM dt_orders s
    JOIN dim_customers c ON s.customer_id = c.customer_id;

-- Stage 3: daily aggregate (depends on stage2_enrich)
CREATE OR REPLACE TASK stage3_aggregate
    WAREHOUSE = transform_wh
    AFTER stage2_enrich
AS
    INSERT INTO dt_orders_daily
    SELECT DATE_TRUNC('day', order_date) AS order_day,
           region, segment,
           COUNT(*) AS order_count,
           SUM(line_total) AS daily_revenue
    FROM enriched_orders
    GROUP BY ALL;

-- Resuming the root task starts the entire DAG. Child tasks run automatically.
ALTER TASK stage1_clean RESUME;
```

**After: dynamic table pipeline**

This example uses the `dim_customers` table from [Create a dynamic table](/user-guide/dynamic-tables/create). If you have not created it, see that page for the setup SQL.

Copy code

```
-- Stage 1: clean raw orders (reads from base table, not a stream)
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        order_id, customer_id, order_date,
        TRIM(UPPER(product_name)) AS product_name,
        quantity, unit_price,
        quantity * unit_price AS line_total,
        order_status
    FROM raw_orders
    WHERE order_status != 'returned';

-- Stage 2: enrich with customer data
CREATE OR REPLACE DYNAMIC TABLE dt_enriched_orders
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        s.order_id, s.order_date, s.product_name, s.line_total,
        c.customer_name, c.region, c.segment
    FROM dt_orders s
    JOIN dim_customers c ON s.customer_id = c.customer_id;

-- Stage 3: daily aggregate (terminal -- carries the freshness goal)
CREATE OR REPLACE DYNAMIC TABLE dt_orders_daily
    TARGET_LAG = '30 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        DATE_TRUNC('day', order_date) AS order_day,
        region, segment,
        COUNT(*) AS order_count,
        SUM(line_total) AS daily_revenue
    FROM dt_enriched_orders
    GROUP BY ALL;
```

The `AFTER` dependency ordering is replaced by the implicit data dependency between dynamic tables. Snowflake
reads the pipeline graph and refreshes `dt_orders` and `dt_enriched_orders` automatically before refreshing
`dt_orders_daily`.

Copy code

```
SELECT * FROM dt_orders_daily ORDER BY order_day, region;
```

```
+------------+---------+------------+-------------+---------------+
| ORDER_DAY  | REGION  | SEGMENT    | ORDER_COUNT | DAILY_REVENUE |
+------------+---------+------------+-------------+---------------+
| 2025-01-15 | US-East | Mid-Market |           1 |         49.99 |
| 2025-01-15 | US-West | Enterprise |           2 |        149.95 |
| 2025-01-16 | EU-West | Startup    |           1 |         62.50 |
+------------+---------+------------+-------------+---------------+
```

## Patterns that don’t migrate

The following patterns require streams and tasks. Don’t attempt to force them into dynamic tables.

### External API calls and side effects

If your task calls an external function, sends notifications, or produces any side effect beyond writing to a
target table, that logic can’t run inside a dynamic table. Dynamic tables are pure SELECT statements.

### Loops and cursor-based procedural code

Dynamic tables can’t contain multi-statement procedural blocks, loops, or cursor-based iteration. If your task
body opens a cursor, iterates over results, and conditionally applies different DML to each row, that step must
stay on streams and tasks.

Conditional logic that can be expressed in SQL (IF/ELSE that maps to CASE WHEN, branching JOINs that map to
OUTER JOINs with COALESCE) works fine in a dynamic table definition.

### GDPR and right-to-erasure

Deletes in base tables propagate through dynamic tables on the next refresh. If you delete a customer’s data
from the source, the dynamic table reflects that deletion after it refreshes. This works for most compliance
scenarios.

Dynamic tables with a frozen region do not propagate deletions from the frozen region. If your compliance workflow targets data within the frozen boundary, those rows remain even after deletion from the base table. See [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions) for details on frozen regions.

Verify delete propagation behavior for your specific definition by testing with a small dataset before relying on it for compliance. If your compliance workflow requires reliable delete propagation, either use `REFRESH_MODE = FULL` or keep the deletion step on streams and tasks.

### Sequence-based surrogate keys

Dynamic tables do not support `SEQUENCE.NEXTVAL` in incremental refresh mode. In full refresh mode, sequences
generate new values on every refresh, so surrogate keys are not stable.

Alternatives:

- Deterministic hashes: `SHA2(CONCAT(order_id, '|', customer_id)) AS surrogate_key`
- System-derived unique identifiers based on natural keys in the data.
- `HASH(*)` for row-level identity where collision probability is acceptable.
- Composite primary key with RELY constraint.

Copy code

```
-- Instead of SEQUENCE.NEXTVAL, use a deterministic hash:
SHA2(CONCAT(order_id, '|', customer_id)) AS surrogate_key
```

For best performance, materialize surrogate keys as early in the pipeline as possible. Computing keys in downstream dynamic tables adds unnecessary overhead to every refresh.

## Convert a single task

Follow these steps to convert one task at a time. Start with the simplest task in your pipeline, validate it,
then move to the next. This approach limits blast radius and makes rollback straightforward.

1. **Choose a migration strategy.** Decide between self-refreshing (set a TARGET\_LAG) and orchestrator-managed
   (set SCHEDULER = DISABLE). If you are migrating incrementally and want to keep your existing orchestration
   for now, SCHEDULER = DISABLE lets you adopt the declarative model without changing your scheduling approach.
2. **Choose a refresh mode.** Use `REFRESH_MODE = INCREMENTAL` for append-heavy workloads with supported
   operators. Use `REFRESH_MODE = FULL` for definitions with non-deterministic functions or unsupported
   operators. Use `REFRESH_MODE = AUTO` to let Snowflake decide at creation time. For details, see
   [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
3. **Validate the output.** Compare the dynamic table’s contents against the old target table. Check the
   refresh status and compare row counts:

   Copy code

   ```
   -- Check that the initial refresh completed successfully.
   SELECT name, refresh_mode, scheduling_state
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLES())
   WHERE name = 'DT_CLEAN_ORDERS';

   -- Compare row counts between old and new tables.
   SELECT
     (SELECT COUNT(*) FROM clean_orders_old) AS old_count,
     (SELECT COUNT(*) FROM dt_clean_orders) AS new_count;
   ```
4. **Suspend the old task.** Once validated, suspend the old task and run both pipelines in parallel for at
   least one full business cycle before decommissioning. Don’t drop the old target table or stream until you
   are confident in the new dynamic table. If you need to roll back, resuming the suspended task processes
   the backlog of stream changes.

## Suspend dynamic tables during migration

Schema changes to base tables or upstream objects can cause active dynamic tables to fail repeatedly during the transition. Suspend affected dynamic tables before you start and resume them after you finish.

The general workflow is: suspend in leaf-to-root order, apply your changes, then resume in root-to-leaf order.
For the full SUSPEND/RESUME workflow including dependency discovery, see
[Modify dynamic tables](/user-guide/dynamic-tables/modify).

## Hybrid pipelines: partial migration

You don’t have to migrate an entire pipeline at once. Dynamic tables and streams and tasks can coexist in the
same pipeline.

For example, you can convert the first two stages of a three-stage pipeline to dynamic tables while keeping
the final stage on streams and tasks (because it calls a stored procedure). To read changes from
a dynamic table into a task, create a stream on the dynamic table.

Copy code

```
-- Create a stream on a dynamic table (use ON DYNAMIC TABLE, not ON TABLE).
CREATE OR REPLACE STREAM dt_orders_stream ON DYNAMIC TABLE dt_orders;

-- The task reads from this stream as usual.
CREATE OR REPLACE TASK final_step
    WAREHOUSE = transform_wh
    SCHEDULE = '10 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('dt_orders_stream')
AS
    CALL my_procedure_with_side_effects(dt_orders_stream);
```

Important

When creating a stream on a dynamic table, you must use `ON DYNAMIC TABLE`, not `ON TABLE`. Using `ON TABLE`
causes an error. Also, triggered tasks (using the AFTER clause with stream-driven triggers) don’t work on
dynamic table streams. Use a scheduled task with a `WHEN SYSTEM$STREAM_HAS_DATA()` check instead.

## Common errors during migration

The following are the most frequent issues encountered when migrating to dynamic tables. For a complete list
of dynamic table error conditions, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).

### Non-deterministic functions force full refresh

If your definition includes a non-deterministic function and you set `REFRESH_MODE = AUTO`, Snowflake
resolves to FULL. Verify the resolved mode after creation with `SHOW DYNAMIC TABLES` and check the
`refresh_mode` and `refresh_mode_reason` columns. For details, see
[Refresh modes](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-auto) and
[Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

### How schema changes affect your dynamic table

Dynamic tables using `SELECT *` automatically adapt to most base table schema changes (added or dropped
columns). Only incompatible type changes (for example, TEXT to INT) cause refresh failures. Dynamic tables
with explicit column lists require `CREATE OR REPLACE` or `CREATE OR ALTER` to reflect upstream schema changes. For details on
schema evolution behavior, see [Modify dynamic tables](/user-guide/dynamic-tables/modify).

## What’s next

After migrating your pipelines, learn how to operate them effectively:

- To use MERGE or INSERT logic inside a dynamic table, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).
- To monitor refresh health, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To optimize refresh performance, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- To manage costs, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
- To troubleshoot refresh failures, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
