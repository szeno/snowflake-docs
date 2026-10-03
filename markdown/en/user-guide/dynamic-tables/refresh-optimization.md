# Optimize queries for incremental refresh

Use this page to design dynamic table queries that perform well with incremental refresh.
This guide covers which operators work efficiently, which need restructuring, and
how to diagnose problems.

For a complete list of which query constructs are supported for incremental refresh, see
[Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

## Run your query standalone first

Before wrapping a query in a dynamic table, run it as a standalone SELECT and check its
execution time. If the query takes longer than your target lag, the dynamic table can never
stay within its target lag. For the full `dt_orders` definition, see [Create a dynamic table](/user-guide/dynamic-tables/create).

Check the query profile for execution time, bytes spilled, and partitions scanned. For steps to
access the query profile, see [Exploring execution times](/user-guide/performance-query-exploring). These numbers are your
baseline. If the standalone query is slow, optimize it before creating the dynamic table.

## Performance expectations by operator

Not all operators benefit equally from incremental refresh. Some process only changed rows,
while others must fully process entire groups or partitions when any row in that group changes.

Note

Short queries (under 10 seconds) might show smaller gains from incremental refresh because
of fixed overhead like query compilation and warehouse scheduling.

### Operators that perform consistently well

These operators process only changed rows and scale linearly with the volume of changes:

- SELECT
- WHERE
- FROM <base table>
- UNION ALL
- LATERAL FLATTEN
- QUALIFY (RANK, ROW\_NUMBER, or DENSE\_RANK) … = 1 (insert-only workloads; deletes can require broader partition scans)

### Operators affected by data locality

For these operators, performance depends on [data locality](#label-dynamic-tables-refresh-optimization-locality),
which measures how closely Snowflake stores rows that share the same key values:

- INNER JOIN
- OUTER JOIN
- GROUP BY
- DISTINCT
- OVER (window functions)

These operators perform well when changes affect fewer than about five percent of grouping or partition keys. If changes spread across many keys or the base tables lack clustering, incremental refresh can be slower than full refresh.

## Operator reference

The following table explains how Snowflake processes each SQL operator during incremental
refresh.

| Operator | How Snowflake processes it | Performance notes |
| --- | --- | --- |
| SELECT | Applies expressions to changed rows only. | Performs well. No special considerations. |
| WHERE | Evaluates the predicate on changed rows only. | Performs well. Cost scales linearly with changes. A highly selective WHERE might still require warehouse uptime even when the output doesn’t change. |
| FROM <table> | Scans micro-partitions that Snowflake added or removed since the last refresh. | Cost scales with the volume of changed partitions. Keep changes to about five percent of the base table or less. |
| UNION ALL | Takes the union of changes from each side. | Performs well. No special considerations. |
| WITH (CTEs) | Computes changes for each Common Table Expression. | Performs well, but avoid overly complex single-table definitions. Consider splitting into multiple dynamic tables. |
| Scalar aggregates | Fully recalculates the aggregate when any input changes. | Avoid in performance-critical tables. Consider grouping by a constant instead. |
| GROUP BY | Recalculates aggregates for every grouping key that contains changes. When the GROUP BY is the top-level operator and the definition exposes the grouping keys and aggregates in supported form, Snowflake reuses the previously computed state. | Cluster base tables by grouping keys. Avoid compound expressions in keys. Make the aggregate top-level by splitting dynamic tables if possible. See [Optimize aggregations](#label-dynamic-tables-refresh-optimization-aggregations). |
| DISTINCT | Equivalent to GROUP BY ALL. | Locality-sensitive. Consider using QUALIFY instead. See [Remove duplicates efficiently](#label-dynamic-tables-refresh-optimization-deduplication). |
| Window functions | Recalculates the function for every partition that contains changes. | Always include PARTITION BY. Cluster base tables by partition keys. See [Optimize window functions](#label-dynamic-tables-refresh-optimization-windows). |
| INNER JOIN | Joins changes from each side with the other table. | Performs well when one side is small or changes infrequently. Cluster the less-frequently-changing side. See [Optimize joins](#label-dynamic-tables-refresh-optimization-joins). |
| OUTER JOIN | Combines inner join logic with NOT EXISTS queries for NULL computation. | Most locality-sensitive operator. See [Optimize joins](#label-dynamic-tables-refresh-optimization-joins). |
| LATERAL FLATTEN | Applies flatten to changed rows only. | Performs well. Cost scales linearly with changes. |
| QUALIFY with ranking | Uses an optimized path for ROW\_NUMBER/RANK/DENSE\_RANK … = 1. | Highly efficient when placed at the top-level projection of the dynamic table. See [Remove duplicates efficiently](#label-dynamic-tables-refresh-optimization-deduplication). |

Expand

Show lessSee more

## Common optimization patterns

The following sections show how to restructure queries that use locality-sensitive operators.

### Optimize aggregations

#### Simplify compound expressions in grouping keys

Unless the
[optimization for top-level aggregates](#label-dynamic-tables-refresh-optimization-top-level-aggregates)
can be used, Snowflake recalculates aggregates for every grouping key that contains changes
when you use [GROUP BY](/sql-reference/constructs/group-by). Performance depends on the
following factors:

- **Data clustering**: Base tables clustered by grouping keys perform best.
- **Change distribution**: Keep changes to fewer than [five percent](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-no-5-percent-rule) of grouping keys.
- **Key complexity**: Simple column references outperform compound expressions.

##### Problem: Compound expressions in grouping keys

This query performs poorly because the grouping key is an expression:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_hourly_sums
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT DATE_TRUNC('minute', order_date), SUM(quantity * unit_price)
  FROM raw_orders
  GROUP BY 1;
```

##### Solution: Materialize the expression

Split into two dynamic tables to expose a simple grouping key:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders_with_minute
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
AS
  SELECT DATE_TRUNC('minute', order_date) AS order_minute, quantity * unit_price AS line_total
  FROM raw_orders;

CREATE OR REPLACE DYNAMIC TABLE dt_hourly_sums
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT order_minute, SUM(line_total)
  FROM dt_orders_with_minute
  GROUP BY 1;
```

The intermediate table exposes a simple column for GROUP BY, and Snowflake can
track changes at the partition level more efficiently.

#### Benefit from top-level aggregates

When a GROUP BY appears at the top-level projection of a dynamic table, Snowflake can
maintain it incrementally by reusing the values already stored in the dynamic table instead
of recomputing every impacted group from scratch. This optimization is applied automatically
when the definition meets the requirements listed in this section.

For example, the following definitions qualify for this optimization:

- `SELECT customer_id, SUM(quantity * unit_price) FROM raw_orders GROUP BY customer_id`
- `SELECT customer_id, COUNT(*) FROM raw_orders GROUP BY customer_id HAVING COUNT(*) > 5`
- `SELECT product_name, ROUND(AVG(quantity), 2) FROM raw_orders GROUP BY product_name`

The optimization is applied only when a dynamic table is created or recreated. If your
existing dynamic table already qualifies, recreate it with `CREATE OR REPLACE` to benefit
from the optimization. `CREATE OR ALTER` is not sufficient.

The optimization supports the following aggregates: `AVG`, `BOOLAND_AGG`, `BOOLOR_AGG`,
`BOOLXOR_AGG`, `CORR`, `COUNT`, `COUNT(*)`, `COUNT_IF`, `COVAR_POP`, `COVAR_SAMP`,
`KURTOSIS`, `MAX`, `MIN`, `REGR_AVGX`, `REGR_AVGY`, `REGR_COUNT`, `REGR_INTERCEPT`,
`REGR_R2`, `REGR_SLOPE`, `REGR_SXX`, `REGR_SXY`, `REGR_SYY`, `SKEW`, `STDDEV`,
`STDDEV_POP`, `STDDEV_SAMP`, `SUM`, `VARIANCE`, `VARIANCE_POP`, `VARIANCE_SAMP`,
`VAR_POP`, and `VAR_SAMP`. `DISTINCT` inside an aggregate is not supported by the
optimization: for example, `COUNT(DISTINCT …)` and `SUM(DISTINCT …)` prevent it.

When the SELECT list does not directly expose a grouping key or aggregate that the
optimization needs, Snowflake can account for it automatically on re-creation for the
following data types:
`BIGINT`, `BOOLEAN`, `BYTEINT`, `DATE`, `DATETIME`, `DEC`, `DECFLOAT`, `DECIMAL`, `DOUBLE`,
`DOUBLE PRECISION`, `FLOAT`, `FLOAT4`, `FLOAT8`, `INT`, `INTEGER`, `INTERVAL`, `IPADDRESS`,
`LONG`, `NUMBER`, `NUMERIC`, `REAL`, `SMALLINT`, `TIME`, `TIMESTAMP`, `TIMESTAMP WITH LOCAL TIME ZONE`, `TIMESTAMP WITH TIME ZONE`, `TIMESTAMP WITHOUT TIME ZONE`, `TIMESTAMPLTZ`,
`TIMESTAMPNTZ`, `TIMESTAMPTZ`, `TIMESTAMP_LTZ`, `TIMESTAMP_NTZ`, `TIMESTAMP_TZ`, `TINYINT`,
and `UUID`. For other data types, select the keys and aggregates themselves explicitly
rather than relying on automatic support. The same data type restriction applies to
aggregates referenced only in a `HAVING` predicate.

If a dynamic table does not qualify for this optimization with its current definition, the
following adjustments can make it qualify:

- If an operator such as a join sits above the GROUP BY, move the aggregate into its own
  dynamic table and perform the join in a downstream dynamic table, as shown in the example
  below.
- If you select a grouping key only wrapped in a non-injective expression and the key’s
  data type is not among the supported data types listed above, select the key itself
  explicitly as well. For example, if the dynamic table is defined as
  `SELECT UPPER(product_name), ... FROM raw_orders GROUP BY product_name` with
  `product_name` being a `VARCHAR` and `UPPER` being non-injective, then `product_name`
  needs to be selected explicitly. The requirement applies to the expression in the GROUP BY
  clause, not to the columns inside it: with `GROUP BY UPPER(product_name)` the grouping key
  is `UPPER(product_name)`, so selecting that expression is sufficient.
- If you do not select a grouping key at all and its data type is not among the supported
  data types listed above, select the key itself explicitly. For example, if the
  dynamic table is defined as `SELECT COUNT(*), ... FROM raw_orders GROUP BY order_status`
  with `order_status` being a `VARCHAR`, then `order_status` needs to be selected explicitly.
- If you wrap an aggregate, select the aggregate itself explicitly as well if its result
  type is not among the supported data types listed above. For example,
  `MIN(product_name)` returns a `VARCHAR`, so selecting `SUBSTR(MIN(product_name), 1, 5)`
  requires selecting `MIN(product_name)` explicitly. The same applies to a cast: selecting
  `MIN(order_ref)::INT` with `order_ref` being a `VARCHAR` encoding an `INT` requires
  selecting `MIN(order_ref)` explicitly.
- If you select an expression containing multiple keys or aggregates, select the keys and
  aggregates whose data type is not among the supported data types listed above
  explicitly unwrapped as well. For example, if the dynamic table is defined as
  `SELECT customer_id || ' ' || product_name || ' (' || MIN(order_status) || '): ' || SUM(quantity * unit_price), ... FROM raw_orders GROUP BY customer_id, product_name`,
  then `product_name` and `MIN(order_status)` are `VARCHAR` and need to be selected
  explicitly, while `customer_id` is an `INT` and `SUM(quantity * unit_price)` is a
  `DECIMAL`, so Snowflake accounts for those automatically.
- If a `HAVING` predicate references an aggregate that is not in the SELECT list, select the
  aggregate explicitly if its result type is not among the supported data types listed
  above.
  Context-aware predicates that reference `CURRENT_TIMESTAMP`, `CURRENT_DATE`, or constant
  subqueries are not supported by the optimization.

Note

Grouping keys with non-binary collations, `TIMESTAMP_TZ`, and semi-structured `VARIANT`,
`OBJECT`, or `ARRAY` types are not supported by the optimization because these
types can have multiple stored representations for the same value.

##### Problem: A join sits above the aggregate

This definition puts the aggregate in a subquery and joins a dimension table on top of it,
so the GROUP BY does not appear at the top-level projection. Snowflake cannot apply
the optimization:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_customer_revenue
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    c.region,
    t.total_revenue
  FROM (
    SELECT customer_id, SUM(quantity * unit_price) AS total_revenue
    FROM raw_orders
    GROUP BY customer_id
  ) t
  JOIN dim_customers c ON t.customer_id = c.customer_id;
```

The join sits above the GROUP BY in the subquery, so the GROUP BY does not appear at the
top-level projection.

##### Solution: Split the aggregate and the join into two dynamic tables

Move the aggregate into its own top-level dynamic table, then perform the join in a
downstream dynamic table that consumes it:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_customer_revenue_totals
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
AS
  SELECT
    customer_id,
    SUM(quantity * unit_price) AS total_revenue
  FROM raw_orders
  GROUP BY customer_id;

CREATE OR REPLACE DYNAMIC TABLE dt_customer_revenue
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    c.region,
    s.total_revenue
  FROM dt_customer_revenue_totals s
  JOIN dim_customers c ON s.customer_id = c.customer_id;
```

The first dynamic table has the GROUP BY at the top-level projection and exposes the key and
aggregate, so Snowflake can apply the optimization. The second dynamic table handles the join
and consumes the pre-aggregated results.

### Optimize joins

Join performance depends on which side changes and how you cluster your data.

**INNER JOIN**: Snowflake joins changes from the left side with the right table, then joins
changes from the right side with the left table. This works well when one side is small
or changes infrequently.

**OUTER JOIN**: Snowflake must also compute NULL values for non-matching rows. This is the
most locality-sensitive operator. Performance depends heavily on which side changes.

#### Problem: Large tables on both sides without clustering

Neither base table is clustered by the join key:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_order_details
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT o.order_id, o.customer_id, c.customer_name, o.quantity
  FROM raw_orders o
  JOIN dim_customers c ON o.customer_id = c.customer_id;
```

#### Solution: Cluster the table that changes less often

Cluster the dimension table by the join key so that the join benefits from better locality:

Copy code

```
ALTER TABLE dim_customers CLUSTER BY (customer_id);

CREATE OR REPLACE DYNAMIC TABLE dt_order_details
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT o.order_id, o.customer_id, c.customer_name, o.quantity
  FROM raw_orders o
  JOIN dim_customers c ON o.customer_id = c.customer_id;
```

For OUTER JOINs:

- Put the table that changes more often on the LEFT side.
- Minimize changes on the side opposite the OUTER keyword.
- For FULL OUTER JOINs, good locality is critical on both sides.
- Use inner joins when possible. If your data has referential integrity, you don’t need
  an outer join.

#### Problem: Non-equality join conditions cause row explosions

Non-equality join conditions (such as range joins or BETWEEN conditions) can cause
intermediate row explosions that make incremental refresh extremely slow, even when the
join is technically supported.

For example, joining sessions to events using a time range can produce billions of
intermediate rows:

Copy code

```
-- Avoid: Non-equality join causes row explosion.
CREATE OR REPLACE DYNAMIC TABLE dt_session_events
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT s.session_id, e.event_type, e.event_time
  FROM sessions s
  JOIN events e
    ON e.event_time BETWEEN s.start_time AND s.end_time;
```

#### Solution: Bin timestamps and use equality joins

Replace the range condition with an equality join on a binned time column. Materialize
the bin in an upstream dynamic table:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_events_binned
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT *, DATE_TRUNC('hour', event_time) AS event_hour
  FROM events;

CREATE OR REPLACE DYNAMIC TABLE dt_sessions_binned
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT *, DATE_TRUNC('hour', start_time) AS session_hour
  FROM sessions;

-- Now join on the equality key. Post-filter retains the original range logic.
CREATE OR REPLACE DYNAMIC TABLE dt_session_events
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT s.session_id, e.event_type, e.event_time
  FROM dt_sessions_binned s
  JOIN dt_events_binned e
    ON s.session_hour = e.event_hour
  WHERE e.event_time BETWEEN s.start_time AND s.end_time;
```

The equality join on `session_hour` limits the rows that Snowflake must match, avoiding
the row explosion. The WHERE clause then applies the precise range filter.

Important

This pattern assumes each session fits within a single time bin. If sessions can span
multiple bins (for example, a session starting at 10:30 and ending at 12:15), you must
generate one row per bin in the `dt_sessions_binned` table to avoid dropping events without notification.
Choose a bin width larger than your maximum session duration, or explode each session into
multiple bin rows.

### Optimize window functions

Snowflake recalculates [window functions](/sql-reference/functions-window) for every partition
that contains changes. Optimize them the same way as GROUP BY.

Key requirements:

- Always include a PARTITION BY clause. Window functions without PARTITION BY treat the
  entire dataset as one partition, causing a full refresh on every cycle.
- Cluster base tables by partition keys.
- Keep changes to fewer than [five percent](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-no-5-percent-rule) of partitions.

#### Problem: Window function without partition clustering

The base table isn’t clustered by the partition key:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_ranked_sales
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    region,
    salesperson,
    amount,
    RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS sales_rank
  FROM daily_sales;
```

#### Solution: Cluster by the partition key

Cluster the base table by the window function’s partition key:

Copy code

```
ALTER TABLE daily_sales CLUSTER BY (region);

CREATE OR REPLACE DYNAMIC TABLE dt_ranked_sales
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    region,
    salesperson,
    amount,
    RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS sales_rank
  FROM daily_sales;
```

### Remove duplicates efficiently

Both [DISTINCT](/sql-reference/sql/select) and [QUALIFY](/sql-reference/constructs/qualify)
can remove duplicates, but they perform differently with incremental refresh.

**DISTINCT**: Equivalent to `GROUP BY ALL`. Performance depends entirely on data locality.

**QUALIFY with ROW\_NUMBER = 1**: Snowflake optimizes the pattern
`QUALIFY ROW_NUMBER() ... = 1` when it appears at the top-level projection of the
dynamic table.

Include all PARTITION BY and ORDER BY columns from the OVER() clause in the dynamic table’s SELECT list. This lets the engine track changed partitions without a full table scan.

Use `QUALIFY` when you need the entire row for each key. If you need only one value per
key, such as the latest `updated_at`, use a top-level `GROUP BY` with `MAX` or `MIN` instead.
That pattern is eligible for the
[optimization for top-level aggregates](#label-dynamic-tables-refresh-optimization-top-level-aggregates).

#### Recommendation: Use QUALIFY instead of DISTINCT

Using DISTINCT:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_unique_customers
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT DISTINCT customer_id, customer_name, region
  FROM dim_customers;
```

Using QUALIFY (preferred):

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_unique_customers
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT customer_id, customer_name, region, segment, updated_at
  FROM dim_customers
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
```

The QUALIFY version is explicit about which duplicate to keep. Also remove redundant
DISTINCT clauses when your data is already unique or you eliminate duplicates upstream.

### Limit blocking operators per dynamic table

Some operators are **blocking**, meaning Snowflake must see all input rows before it can
produce any output. Blocking operators include:

- Window functions (the entire partition must be processed before producing output)
- GROUP BY and DISTINCT
- ORDER BY (in subqueries)

When a query combines multiple blocking operators, each one must wait for the previous
to finish. This reduces parallelism and increases memory pressure.

As a guideline, limit each dynamic table to a single blocking operation.
When a query has multiple joins combined with aggregations and window functions, split
it into intermediate dynamic tables so that each stage handles one blocking step.

### Split complex queries across dynamic tables

Breaking complex queries into intermediate dynamic tables makes it easier to identify
bottlenecks and improves incremental refresh efficiency.

Guidelines:

- **Filter early.** Apply WHERE clauses in the dynamic tables closest to your base tables
  so that downstream tables process fewer rows.
- **Deduplicate early.** Remove duplicate rows upstream to avoid repeated DISTINCT work
  downstream.
- **Split between blocking operators.** Move joins, aggregations, and window functions
  into separate intermediate dynamic tables so each stage has good data locality for
  its key operation.
- **Materialize compound expressions.** Move expressions like `DATE_TRUNC('minute', ts)`
  into an intermediate table before grouping by them. See
  [Optimize aggregations](#label-dynamic-tables-refresh-optimization-aggregations).

Initial complex query:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_final_result
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    DATE_TRUNC('day', o.order_date) AS order_day,
    c.region,
    COUNT(*) AS order_count,
    SUM(o.quantity * o.unit_price) AS daily_revenue
  FROM raw_orders o
  JOIN dim_customers c ON o.customer_id = c.customer_id
  GROUP BY ALL;
```

Split the pipeline by adding an intermediate dynamic table:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_stg_order_customers
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
AS
  SELECT
    o.order_id,
    o.order_date,
    o.quantity * o.unit_price AS line_total,
    c.region
  FROM raw_orders o
  JOIN dim_customers c ON o.customer_id = c.customer_id;

CREATE OR REPLACE DYNAMIC TABLE dt_final_result
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    DATE_TRUNC('day', order_date) AS order_day,
    region,
    COUNT(*) AS order_count,
    SUM(line_total) AS daily_revenue
  FROM dt_stg_order_customers
  GROUP BY ALL;
```

The intermediate table handles the join, and the final table handles the aggregation.
Each stage can maintain better data locality for its specific operation.

## Improve data locality

**Data locality** describes how closely Snowflake stores rows that share the same key values.
When rows with matching keys are stored in fewer micro-partitions (good locality), incremental
refreshes scan less data. When matching keys span many micro-partitions (poor locality),
incremental refresh can take longer than full refresh.

For more information about how Snowflake stores data, see
[Micro-partitions & Data Clustering](/user-guide/tables-clustering-micropartitions).

### Cluster base tables

The most effective way to improve locality is to cluster your base tables by the keys
used in your definition (JOIN, GROUP BY, or PARTITION BY keys):

Copy code

```
ALTER TABLE raw_orders CLUSTER BY (customer_id);
```

When you join on multiple columns and can’t cluster by all of them:

- Prioritize clustering the larger table by the most selective key.
- Consider splitting the pipeline so that each join operates on well-clustered data.

For more information, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys). To enable automatic
reclustering, see [Automatic Clustering](/user-guide/tables-auto-reclustering).

### Factors that affect locality

Beyond base table clustering, two factors affect locality:

- **How new data aligns with partition keys.** Incremental refresh is faster when new rows
  affect a small portion of keys. Time-series data grouped by hour has good locality
  because new rows share recent timestamps. Data grouped by a column with values spread
  across the entire table has poor locality.
- **How changes align with dynamic table clustering.** When Snowflake writes changes to a dynamic table during refresh, it must locate the affected rows. Changes to recent rows in a time-ordered table are fast. Changes scattered across the entire table are slow.

When you experience poor locality because of these factors, consider restructuring your data
model or ingestion patterns upstream.

## When incremental refresh is slower than full refresh

Incremental refresh isn’t always faster. The following conditions can make incremental
refresh slower and more expensive than full refresh:

- **High change volume.** When more than about five percent of rows or micro-partitions change
  between refreshes, the overhead of tracking changes exceeds the cost of a full refresh.
- **Poor data locality.** When changed keys span many micro-partitions, incremental refresh
  must scan broadly.
- **Heavy delete or truncate-reload patterns.** Large batches of deletes can force the engine
  to scan many files to identify removed rows.

To check whether incremental refresh is helping or hurting, compare incremental and full
refresh times using [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history):

Copy code

```
SELECT
    refresh_action,
    AVG(DATEDIFF('second', refresh_start_time, refresh_end_time)) AS avg_seconds
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'mydb.myschema.dt_orders'
))
WHERE refresh_start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND refresh_action IN ('INCREMENTAL', 'FULL')
GROUP BY refresh_action;
```

If the average incremental refresh time is close to or exceeds the average full refresh
time, switch to `REFRESH_MODE = FULL`.

Note

If your workload is usually incremental-friendly but occasionally spikes in change volume, consider
[ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-adaptive).
ADAPTIVE uses incremental refresh by default but automatically reinitializes when large upstream changes are detected, then resumes incremental refresh.

If declarative optimizations aren’t sufficient,
[custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization) lets you take full control of
refresh logic. You write the exact MERGE or INSERT statement that runs each refresh.

---

## Try it: Rewrite a dynamic table to refresh incrementally

This tutorial shows how replacing a suboptimal subquery pattern with
`QUALIFY RANK() = 1` improves incremental refresh performance for an SCD Type 1 workload.

### Prerequisites

- A [warehouse](/user-guide/warehouses-overview). An x-small warehouse is sufficient.
  The tutorial uses `transform_wh` as the warehouse name. Replace this with your own
  warehouse name throughout the tutorial.
- Privileges to create databases, schemas, and dynamic tables. See
  [Access control privileges](/user-guide/security-access-control-privileges).

### Step 1: Create the base data

Create a database, schema, and base table with price history:

Copy code

```
CREATE DATABASE IF NOT EXISTS mydb;
CREATE SCHEMA IF NOT EXISTS mydb.myschema;
USE SCHEMA mydb.myschema;

CREATE OR REPLACE TABLE product_changes (
    product_code VARCHAR(50),
    product_name VARCHAR(200),
    price NUMBER(10, 2),
    price_start_date TIMESTAMP_NTZ(9)
);

-- Generate 100 million rows: 10,000 products with price history.
INSERT INTO product_changes (product_code, product_name, price, price_start_date)
  SELECT
      'PC-' || LPAD(TO_VARCHAR(MOD(SEQ4(), 10000) + 1), 3, '0') AS product_code,
      'Product ' || LPAD(TO_VARCHAR(MOD(SEQ4(), 10000) + 1), 3, '0') AS product_name,
      ROUND(10.00 + (MOD(SEQ4(), 10000) * 5) + (SEQ4() * 0.01), 2) AS price,
      DATEADD(MINUTE, SEQ4() * 5, '2025-01-01 00:00:00') AS price_start_date
  FROM TABLE(GENERATOR(ROWCOUNT => 100000000));
```

### Step 2: Create two dynamic tables for comparison

Create a suboptimal version that uses a self-join with MAX():

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_product_current_price_v1
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    INITIALIZE = ON_SCHEDULE
    REFRESH_MODE = INCREMENTAL
  AS
  SELECT
      h.product_code,
      h.product_name,
      h.price,
      h.price_start_date
  FROM product_changes h
  INNER JOIN (
      SELECT product_code, MAX(price_start_date) max_price_start_date
      FROM product_changes
      GROUP BY product_code
  ) m ON h.price_start_date = m.max_price_start_date AND h.product_code = m.product_code;
```

Create an optimized version using QUALIFY:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_product_current_price_v2
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
    INITIALIZE = ON_SCHEDULE
  AS
  SELECT
      product_code,
      product_name,
      price,
      price_start_date
  FROM product_changes
  QUALIFY RANK() OVER (PARTITION BY product_code ORDER BY price_start_date DESC) = 1;
```

Initialize both tables:

Copy code

```
ALTER DYNAMIC TABLE dt_product_current_price_v1 REFRESH;
ALTER DYNAMIC TABLE dt_product_current_price_v2 REFRESH;
```

### Step 3: Compare incremental refresh performance

Insert 1,000 new rows that update prices for five products:

Copy code

```
INSERT INTO product_changes (product_code, product_name, price, price_start_date)
  SELECT
      'PC-' || LPAD(TO_VARCHAR(MOD(SEQ4(), 5) + 1), 3, '0') AS product_code,
      'Product ' || LPAD(TO_VARCHAR(MOD(SEQ4(), 5) + 1), 3, '0') AS product_name,
      ROUND(50.00 + (MOD(SEQ4(), 10) * 5) + ((SEQ4() + 100000000) * 0.01), 2) AS price,
      DATEADD(MINUTE, (SEQ4() + 100000000) * 5, '2025-01-01 00:00:00') AS price_start_date
  FROM TABLE(GENERATOR(ROWCOUNT => 1000));
```

Refresh each table and compare:

Copy code

```
ALTER DYNAMIC TABLE dt_product_current_price_v1 REFRESH;
ALTER DYNAMIC TABLE dt_product_current_price_v2 REFRESH;
```

Check results in the refresh history:

Copy code

```
SELECT
    name,
    refresh_action,
    DATEDIFF('millisecond', refresh_start_time, refresh_end_time) AS duration_ms
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME_PREFIX => 'mydb.myschema.dt_product_current_price_'
))
ORDER BY refresh_start_time DESC
LIMIT 4;
```

The QUALIFY version (`dt_product_current_price_v2`) should complete significantly faster
because the engine identifies and processes only the five products that changed. The
self-join version (`dt_product_current_price_v1`) must recalculate the MAX() subquery
across all 10,000 products.

### Clean up

Drop the tutorial database and all objects within it:

Copy code

```
DROP DATABASE mydb;
```

## What’s next

- To check which constructs support incremental refresh, see
  [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
- To take full control of refresh logic with custom MERGE or INSERT statements, see
  [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).
- To mark historical data as unchanging and reduce refresh scope, see
  [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions).
- To monitor refresh performance and diagnose bottlenecks, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To understand cost implications of refresh strategies, see
  [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
