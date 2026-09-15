# Data consistency and pipeline boundaries

Dynamic table pipelines provide snapshot isolation: every refresh reads all inputs at a single point in time. This page covers how that works, what happens when a refresh fails, and when to trade isolation for scheduling independence using refresh boundaries.

## How snapshot isolation works in a pipeline

When one dynamic table reads from another, Snowflake groups them into a single pipeline. Every
refresh in that pipeline reads all upstream inputs at one coordinated [data timestamp](/sql-reference/functions/dynamic_table_refresh_history). The data timestamp determines which version of each input the refresh reads, so the
downstream result is consistent with a single point-in-time snapshot of every upstream table.

This section uses the `dt_orders` and `dt_orders_daily` pipeline from
[Create a dynamic table](/user-guide/dynamic-tables/create).

In this pipeline, `dt_orders_daily` joins `dt_orders` with `dim_customers`. Every refresh reads
both at the same timestamp. Without this, a refresh could join today’s orders with yesterday’s
customer attributes, producing incorrect results.

Snapshot isolation guarantees two things:

- Each refresh is atomic: downstream tables never see partially refreshed upstream data.
- All inputs to a refresh reflect the same point in time, whether used in joins, filters, or aggregations.

Snapshot isolation applies within a single pipeline’s refresh cycle. Ad-hoc queries outside a refresh read each table’s latest committed version separately.

To manually refresh multiple dynamic tables at a single data timestamp, list them in one
`ALTER DYNAMIC TABLE ... REFRESH` statement. See
[Refresh multiple dynamic tables in one statement](/user-guide/dynamic-tables/manage#label-dynamic-tables-manage-multi-refresh).

## Failures cause staleness, never inconsistency

Each refresh is atomic: it fully completes or has no effect. If a refresh fails, all downstream tables hold their last successful version. They never advance past the failure.

| Scenario | What downstream tables see |
| --- | --- |
| Upstream refresh fails | Downstream tables remain at their last consistent version. Refresh status: UPSTREAM\_FAILED. |
| Mid-pipeline refresh fails | Same as an upstream failure for all dynamic tables below the failed one. |
| Multiple consecutive failures | Staleness accumulates. After five consecutive failures, Snowflake automatically suspends the table. Timeouts and cancellations count as failures toward this threshold. Only skipped refreshes (where the table was not attempted because an upstream failed) do not count. |

Expand

Show lessSee more

You can verify the pipeline state with a refresh history query:

Copy code

```
SELECT
    name,
    state,
    state_message,
    refresh_action,
    refresh_trigger
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'mydb.myschema.dt_orders_daily'
))
ORDER BY refresh_start_time DESC
LIMIT 5;
```

```
+------------------------------------+-----------------+---------------+----------------+-----------------+
| NAME                               | STATE           | STATE_MESSAGE | REFRESH_ACTION | REFRESH_TRIGGER |
|------------------------------------+-----------------+---------------+----------------+-----------------|
| MYDB.MYSCHEMA.DT_ORDERS_DAILY     | UPSTREAM_FAILED |               | NO_DATA        | SCHEDULED       |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY     | SUCCEEDED       |               | INCREMENTAL    | SCHEDULED       |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY     | SUCCEEDED       |               | INCREMENTAL    | SCHEDULED       |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY     | SUCCEEDED       |               | INCREMENTAL    | SCHEDULED       |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY     | SUCCEEDED       |               | INCREMENTAL    | CREATION        |
+------------------------------------+-----------------+---------------+----------------+-----------------+
```

A state of UPSTREAM\_FAILED means the table itself didn’t fail. An upstream dependency failed, and
this table was skipped to preserve consistency. Fix the upstream table first, and downstream tables
resume on the next scheduled refresh.

When staleness in one part of your pipeline should not block another, you can separate them with a
refresh boundary.

## Decouple pipelines with DYNAMIC\_TABLE\_REFRESH\_BOUNDARY()

By default, referencing one dynamic table from another places both in the same coordinated pipeline. Wrapping the reference in `DYNAMIC_TABLE_REFRESH_BOUNDARY()` breaks that coupling: the downstream table treats the wrapped input like an independently refreshed base table.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_enriched_orders
    TARGET_LAG = '5 minutes'
    WAREHOUSE = transform_wh
AS
    SELECT
        s.*,
        p.product_category
    FROM dt_orders s
    JOIN DYNAMIC_TABLE_REFRESH_BOUNDARY(dt_product_lookup) p
        ON s.product_name = p.product_name;
```

In this example, `dt_orders` is a direct dependency (same pipeline, coordinated refreshes,
snapshot isolation). `dt_product_lookup` is across a refresh boundary (separate pipeline, independent
schedule, no snapshot isolation on that edge). Each refresh of `dt_enriched_orders` reads whatever
version of `dt_product_lookup` exists at that moment.

### What changes across a boundary

| Behavior | Without boundary (default) | With boundary |
| --- | --- | --- |
| Pipeline membership | Same pipeline, coordinated refreshes | Separate pipelines, independent schedules |
| Snapshot isolation | Guaranteed across all inputs | Not guaranteed between the boundary input and the rest of the pipeline |
| Failure propagation | Upstream failure blocks downstream | Boundary input failure does not block downstream |
| Target lag constraint | Downstream lag must be >= upstream | No constraint across the boundary |

Expand

Show lessSee more

### When is the boundary required?

You must use `DYNAMIC_TABLE_REFRESH_BOUNDARY()` whenever your dynamic table reads from a regular view whose dependencies include another dynamic table. This applies whether the view is in the same account or accessed through a share. Wrap the outermost view that your dynamic table reads from.

This is NOT required when:

- Reading directly from another dynamic table (same account: both join the same pipeline automatically)
- Reading directly from a shared dynamic table (the share boundary already decouples the pipelines)
- Reading from a view whose dependencies include only base tables

| Scenario | Boundary required? | Why |
| --- | --- | --- |
| Dynamic table reads from another dynamic table directly | No (optional for decoupling) | Same pipeline, coordinated scheduling |
| Dynamic table reads from a view with no dynamic table in deps | No (optional, defensive) | View is a SQL overlay on base tables |
| Dynamic table reads from a view with dynamic table in deps | Yes | Cannot coordinate across the view’s dynamic table dependency |
| Dynamic table reads from a shared dynamic table | No | Share boundary already decouples |
| Dynamic table reads from a shared view with no dynamic table deps | No (optional, defensive) | Same as shared base table |
| Dynamic table reads from a shared view with dynamic table deps | Yes | Same coordination problem across boundary |

Expand

Show lessSee more

Defensive boundary wrapping

When reading from a view whose implementation you do not control, consider wrapping it in `DYNAMIC_TABLE_REFRESH_BOUNDARY()`. With the boundary, your dynamic table’s refresh graph stops at the wrapped reference. It reads the current state at refresh time without tracking what sits behind it. Changes below the boundary, such as disabled change tracking on base tables or restructured intermediate dependencies, do not prevent your pipeline from refreshing.

The boundary does not remove your need for access to the referenced object itself. If the object is dropped or your privileges on it are revoked, your dynamic table still fails.

The trade-off: wrapping an input means it is no longer refreshed together with the rest of your pipeline. If you join a wrapped view with another input, the two sides may reflect different points in time.

### What happens when a boundary input is stale

When a refresh boundary separates two pipelines, a failure on the upstream side does not propagate.
The downstream table still refreshes on its own schedule and reads the last available version of the
boundary input. This means:

- The downstream table can produce results based on stale boundary-input data without any warning in
  the refresh status.
- When using refresh boundaries, monitoring the downstream pipeline alone is insufficient. You must independently monitor the upstream pipeline to detect staleness on the boundary side.
- The downstream table’s own refresh status shows SUCCEEDED, because its own refresh completed
  normally.

Refresh boundaries prevent cascading staleness at the cost of cross-pipeline consistency. Use them only on dependencies where you don’t need snapshot isolation.

### Use a view with a refresh boundary (delayed-view pattern)

This pattern is common when different teams in the same organization share data. A refresh boundary
allows one team’s pipeline to operate independently, so failures or staleness in one team’s pipeline
do not cascade into another team’s downstream tables.

A dynamic table can’t read from a view that queries another dynamic table unless the view is wrapped
in `DYNAMIC_TABLE_REFRESH_BOUNDARY()`. This pattern is sometimes called a “delayed view” because the
downstream table sees whatever version the view resolves to at refresh time, not a coordinated
snapshot.

Copy code

```
-- View on top of a dynamic table
CREATE OR REPLACE VIEW v_completed_orders AS
    SELECT * FROM dt_orders WHERE order_status = 'completed';

-- Dynamic table reading through the view with a boundary
CREATE OR REPLACE DYNAMIC TABLE dt_completed_order_summary
    TARGET_LAG = '15 minutes'
    WAREHOUSE = transform_wh
AS
    SELECT
        customer_id,
        COUNT(*) AS completed_count,
        SUM(line_total) AS completed_revenue
    FROM DYNAMIC_TABLE_REFRESH_BOUNDARY(v_completed_orders)
    GROUP BY customer_id;
```

Without the boundary wrapper, the CREATE DYNAMIC TABLE statement returns an error because Snowflake
can’t resolve the view’s dynamic table dependency into a single coordinated pipeline. This also
applies to shared secure views. If a provider shares a secure view whose dependencies include a
dynamic table, the consumer must wrap it in `DYNAMIC_TABLE_REFRESH_BOUNDARY()`.

For sharing-specific guidance on pipeline boundaries, see [On a shared view that references a dynamic table](/user-guide/dynamic-tables/sharing#label-dynamic-tables-sharing-consumer-secure-view).

## Verify pipeline boundaries

Use DYNAMIC\_TABLE\_GRAPH\_HISTORY to confirm which tables share a pipeline and which are separated by
a boundary. Tables in the same pipeline share the same graph and have coordinated scheduling states.

Copy code

```
SELECT
    name,
    scheduling_state:"state"::STRING AS scheduling_state,
    target_lag_type,
    target_lag_sec,
    ARRAY_TO_STRING(
        TRANSFORM(inputs, o -> o:"name"::STRING),
        ', '
    ) AS inputs
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY())
WHERE name IN ('MYDB.MYSCHEMA.DT_ORDERS', 'MYDB.MYSCHEMA.DT_ORDERS_DAILY',
               'MYDB.MYSCHEMA.DT_ENRICHED_ORDERS')
ORDER BY name;
```

```
+------------------------------------+------------------+-----------------+----------------+-----------------------------------------------------+
| NAME                               | SCHEDULING_STATE | TARGET_LAG_TYPE | TARGET_LAG_SEC | INPUTS                                              |
|------------------------------------+------------------+-----------------+----------------+-----------------------------------------------------|
| MYDB.MYSCHEMA.DT_ENRICHED_ORDERS      | ACTIVE           | USER_DEFINED    |            300 | MYDB.MYSCHEMA.DT_ORDERS                            |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY     | ACTIVE           | USER_DEFINED    |           1800 | MYDB.MYSCHEMA.DT_ORDERS, MYDB.MYSCHEMA.DIM_CUSTOMERS |
| MYDB.MYSCHEMA.DT_ORDERS           | ACTIVE           | USER_DEFINED    |            600 | MYDB.MYSCHEMA.RAW_ORDERS                            |
+------------------------------------+------------------+-----------------+----------------+-----------------------------------------------------+
```

Tip

The query above does not distinguish boundary inputs. In the raw JSON, boundary inputs appear with `insideRefreshBoundary: true`. If a table you expected in this pipeline is missing from the output, check its definition for a `DYNAMIC_TABLE_REFRESH_BOUNDARY()` wrapper.

## Restrictions on refresh boundaries

Within a single definition, all references to the same upstream dynamic table must be consistently direct or consistently wrapped in `DYNAMIC_TABLE_REFRESH_BOUNDARY()`. Mixing both causes CREATE DYNAMIC TABLE to fail.

**Boundary targets must be named objects.** `DYNAMIC_TABLE_REFRESH_BOUNDARY()` wraps a table, view,
dynamic table, or CTE (common table expression). It can’t wrap inline subqueries, table functions, or
UDTFs (user-defined table functions).

**Has no effect outside dynamic tables.** You can call `DYNAMIC_TABLE_REFRESH_BOUNDARY()` in a regular
SELECT query, but it has no effect outside a dynamic table definition.

## What’s next

- To understand how Snowflake picks INCREMENTAL or FULL refresh, see
  [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To set up alerts when staleness exceeds your target lag, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To diagnose UPSTREAM\_FAILED and other refresh failures, see
  [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
