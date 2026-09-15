# Quick-start best practices for dynamic tables

Follow these practices when building dynamic table pipelines in production.

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

## 1. Set appropriate target lag for each table in your pipeline

Target lag is a staleness target, not a guaranteed latency bound and not a refresh schedule. Setting a shorter lag than
you actually need causes more frequent refreshes and higher cost without delivering value. The right
setting depends on the table’s role in the pipeline:

- **Leaf dynamic tables (consumer-facing):** Set an explicit lag that matches your freshness requirements
  (for example, `TARGET_LAG = '10 minutes'`). This value drives the refresh schedule for all
  upstream tables.
- **Intermediate dynamic tables:** Set `TARGET_LAG = DOWNSTREAM` so the table has no independent refresh
  schedule and refreshes only when a downstream consumer needs fresh data. Snowflake derives the
  timing from the shortest target lag among all downstream consumers, which avoids unnecessary
  refreshes that waste compute credits.

Copy code

```
-- Intermediate table: refreshes only when dt_orders_daily needs it
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT ... FROM raw_orders;

-- Leaf table: drives the refresh schedule for the entire pipeline
CREATE OR REPLACE DYNAMIC TABLE dt_orders_daily
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT ... FROM dt_orders;
```

Start with the longest acceptable lag on leaf tables and tighten it only when business
requirements demand it. To adjust the lag on an existing table, run
`ALTER DYNAMIC TABLE dt_orders_daily SET TARGET_LAG = '60 minutes'`.

DOWNSTREAM tables with no consumer never refresh

If a DOWNSTREAM table has no downstream consumer, it never refreshes automatically. This produces
no error or warning. Always set an explicit target lag on leaf tables that serve queries or
dashboards directly. For full details, see
[TARGET\_LAG = DOWNSTREAM](/user-guide/dynamic-tables/target-lag#label-dynamic-tables-target-lag-downstream).

## 2. Set REFRESH\_MODE explicitly

AUTO uses a heuristic to choose between INCREMENTAL and FULL at creation time. For details, see
[Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes). Setting REFRESH\_MODE explicitly
ensures the same refresh mode on every recreation and returns an error at creation time if the
query does not support the specified mode.

If you use AUTO, verify the resolved mode after creation with SHOW DYNAMIC TABLES. See
[Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes) for instructions.

## 3. Use a frozen region for historical data

When your dynamic table has a large stable historical portion and a small active head, define a
frozen region. Rows in the frozen region are skipped during refresh,
reducing both compute time and credit consumption.

A frozen region works best for:

- **Append-heavy time-series or event data** with a rolling active window, such as IoT
  telemetry or clickstream logs where rows older than a cutoff date never change.
- **Fact tables with a settlement boundary**, where historical facts are finalized and only
  recent facts need recomputation when dimensions update.
- **Boolean-flag or ID-based partitions**, such as `is_processed = TRUE` or `status_id IN (3, 4)`,
  where a subset of rows is known to be final.
- **Full-refresh dynamic tables over large datasets**, where skipping the frozen region significantly reduces refresh cost.

Avoid a frozen region when old data changes frequently and you need those changes to propagate.
Rare changes to frozen base-table data can be handled with DML on the base table or a periodic full refresh of the dynamic table. Also avoid it
when the definition has no natural column that separates frozen rows from active ones, such as a date, boolean flag, or ID. For example, user profile tables where any row might update do not benefit from a frozen region.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_events
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
    FROZEN WHERE (event_date < CURRENT_TIMESTAMP() - INTERVAL '30 days')
AS
    SELECT
        event_id, user_id, event_date, event_type, payload
        ...
    FROM raw_events;
```

For predicate restrictions, ALTER syntax, BACKFILL FROM, and the `METADATA$IS_FROZEN`
metadata column, see
[Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions).

## 4. Use primary keys for incremental refresh

When a base table has a PRIMARY KEY constraint with the RELY property, Snowflake uses those key
values as stable row identifiers. This is especially important for base tables loaded with INSERT
OVERWRITE, where primary keys let Snowflake compare key values before and after the overwrite
and process only the rows that actually changed. Without a primary key on tables loaded with
INSERT OVERWRITE, Snowflake must reprocess all rows on every refresh instead of only the changed
ones.

To add a primary key, declare the constraint on the base table and set RELY:

Copy code

```
ALTER TABLE dim_customers
  ADD CONSTRAINT pk_dim_customers PRIMARY KEY (customer_id) RELY;
```

For details on primary keys, system-derived unique keys, and how they affect change tracking, see
[Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization).

## 5. Test your query standalone before wrapping it in a dynamic table

Running the SELECT independently helps you catch errors, validate output, and get a rough sense of
query complexity before creating a dynamic table. Standalone execution time is not a
reliable predictor of incremental refresh time. Incremental refresh can be faster than standalone
because it only processes changed rows rather than the full result set. However, if the standalone
query is slow enough to indicate a problem (for example, missing filters or an inefficient join),
fix those issues before wrapping it in a dynamic table.

Check the query profile in Snowsight ([Exploring execution times](/user-guide/performance-query-exploring)) or query
INFORMATION\_SCHEMA.QUERY\_HISTORY\_BY\_SESSION to verify the query runs without errors and produces
the expected output.

If the query reveals performance issues, optimize the query before creating the dynamic table. For
general query tuning guidance, see
[Optimizing warehouses for performance](/guides-overview-performance).

## 6. Limit each dynamic table to a single non-row-wise operation

Non-row-wise operations (GROUP BY, DISTINCT, window functions) require
Snowflake to track how input changes map to output rows. Combining multiple such operations on different key sets prevents Snowflake from narrowing the affected output, which forces the refresh to reprocess more data than necessary.

As a general rule, keep each incremental dynamic table to one non-row-wise operation. When your
logic requires multiple operations, split them into a pipeline of simpler dynamic tables. For
example:

- **GROUP BY + JOIN on different keys:** Move the aggregation and the join into separate dynamic
  tables so each contains only one operation.
- **GROUP BY + DISTINCT on different columns:** Stage the DISTINCT into an upstream dynamic table,
  then aggregate in a downstream one.

The `dt_orders` and `dt_orders_daily` tables used in these examples are defined in the [Create a dynamic table](/user-guide/dynamic-tables/create) tutorial.

For guidance on which operators affect incremental refresh performance, see
[Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).

## 7. Use dedicated warehouses for cost isolation

A shared warehouse makes it harder to isolate refresh costs from ad-hoc query costs. Assign a
dedicated warehouse so you can track refresh costs independently and prevent refresh workloads
from competing with other queries. For incremental dynamic tables that require a large initial
refresh, consider specifying a separate INITIALIZATION\_WAREHOUSE to avoid oversizing the
steady-state refresh warehouse. INITIALIZATION\_WAREHOUSE does not apply to full refresh dynamic tables. Set the warehouse at creation time with the WAREHOUSE parameter
in CREATE DYNAMIC TABLE, or change it later with
`ALTER DYNAMIC TABLE dt_orders SET WAREHOUSE = transform_wh`.

For cost analysis, filter the QUERY\_HISTORY view by warehouse name to see only dynamic table
refresh costs.

## 8. Wrap views whose implementation you do not control in DYNAMIC\_TABLE\_REFRESH\_BOUNDARY()

`DYNAMIC_TABLE_REFRESH_BOUNDARY()` removes the wrapped reference from your pipeline’s refresh dependency graph. Your dynamic table reads whatever state the referenced object has at refresh time, without tracking lineage or coordinating refreshes below that point. Changes to the objects behind that reference (such as disabled change tracking on base tables or added intermediate dynamic tables) do not affect your pipeline’s ability to refresh.

Do not wrap inputs that you join together when those inputs must reflect the same point in time. For those inputs, leave them unwrapped so they participate in the same coordinated pipeline refresh.

For the full explanation of pipeline boundaries, see [Decouple pipelines with DYNAMIC\_TABLE\_REFRESH\_BOUNDARY()](/user-guide/dynamic-tables/data-consistency#label-dynamic-tables-data-consistency-boundary-function).

## 9. Set up refresh failure alerting

Refresh failures produce no alert by default: a failed table falls behind its target lag without
raising an exception. Set up alerting to catch failures early. For alert setup with examples, see
[Set up alerts with the event table](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitor-event-table-alerts).

After creating the alert, resume it with `ALTER ALERT dt_refresh_failure_alert RESUME`.

## 10. Monitor Cloud Services costs

Scheduling and change-detection checks run as Cloud Services compute, with query compilation being the largest contributor for tables with complex definitions. Short target lags and many dynamic tables can push this spend above the billable
threshold. For details on Cloud Services billing, see [Cloud Services billing](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage). Use the following query to check which query types contribute the most:

Copy code

```
SELECT
    query_type,
    SUM(credits_used_cloud_services) AS cs_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY query_type
ORDER BY cs_credits DESC;
```

If DYNAMIC\_TABLE\_REFRESH dominates Cloud Services costs, increase target lag on tables that don’t
need aggressive freshness. For details on how Cloud Services billing works with dynamic tables, see
[Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).

## 11. Extend a running pipeline with minimum disruption

Adding a table to a live pipeline requires care to avoid blocking deploys or triggering unnecessary
reinitialization. The approach depends on where the new table sits in the pipeline.

**Adding a new leaf consumer.** Create the table with `INITIALIZE = ON_SCHEDULE` so the
`CREATE` statement returns immediately instead of blocking until the initial refresh completes
(which is the default `INITIALIZE = ON_CREATE` behavior). The table stays empty until its initial refresh. Before connecting dashboards or downstream consumers, verify the initial refresh
succeeded by querying `DYNAMIC_TABLE_REFRESH_HISTORY`.

ON\_SCHEDULE tables are empty until the initial refresh

Until the initial refresh completes, queries against the table return a
`Dynamic table is not initialized` error. Do not point consumers at the table until you confirm data is present.

**Inserting an intermediate table.** Create the new intermediate table with
`TARGET_LAG = DOWNSTREAM` so it inherits its refresh schedule from existing consumers. Then
recreate the downstream table that should read from it using `CREATE OR REPLACE DYNAMIC TABLE`
with `COPY GRANTS` to preserve access controls.

CREATE OR REPLACE cascades reinitialization

`CREATE OR REPLACE` on a dynamic table triggers reinitialization of that table and its downstream
incremental dynamic tables. Downstream full-refresh dynamic tables are unaffected. Schedule this
operation during a maintenance window when a temporary lag spike is acceptable.

For the full safe-evolution workflow covering renames, column changes, and dependency rewiring, see
[Modify dynamic tables](/user-guide/dynamic-tables/modify).

## What’s next

- [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost)
- [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization)
- [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring)
- [Design patterns for dynamic tables](/user-guide/dynamic-tables/design-patterns)
