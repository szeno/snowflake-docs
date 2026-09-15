# Design patterns for dynamic tables

This page collects common recipes for structuring dynamic table pipelines. Use the decision table below to find the right starting point. For per-table configuration (target lag, refresh mode, warehouse selection), see [Quick-start best practices for dynamic tables](/user-guide/dynamic-tables/best-practices).

## Choose a pattern

| Pattern | Use when | How it works |
| --- | --- | --- |
| Multi-table pipeline | Your definition has more than one logical step | TARGET\_LAG = DOWNSTREAM on intermediates; medallion layers |
| Controller table | You need coordinated refreshes across independent pipelines | Zero-row coordination table with independent leaf lags |
| SCD Type 1 deduplication | Source appends CDC records; you need current state | QUALIFY ROW\_NUMBER; handles out-of-order arrival |
| Stream-static join | CDC enrichment with dimension lookups and delete propagation | MERGE INTO SELF with CHANGES and LEFT OUTER JOIN |
| Top-K leaderboard | Maintain a bounded result set that shrinks or grows | MERGE INTO SELF reading current state through FROM SELF |
| Daily snapshot | Accumulate periodic snapshots without CHANGES | INSERT INTO SELF with ROW\_TIMESTAMP |

Expand

Show lessSee more

## Decompose a definition into a multi-table pipeline

Break a monolithic definition into a pipeline of two or more dynamic tables, each handling
one logical step. Many teams organize pipeline layers using medallion vocabulary (bronze,
silver, gold). In dynamic table terms: bronze is the raw landing table, silver is a
cleaned or conformed dynamic table with TARGET\_LAG = DOWNSTREAM, and gold is an
aggregated dynamic table with a time-based freshness goal.

Decomposing joins and aggregations across multiple dynamic tables enables each step to
refresh incrementally. Place joins in the first dynamic table and aggregations in the
next.

Important

Avoid combining joins, aggregations, and window functions in a single dynamic table. This
forces the entire computation to re-run on every refresh. Separating these operators into
different pipeline stages enables incremental refresh for each step.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders_enriched
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        o.order_id,
        o.order_date,
        o.quantity,
        o.unit_price,
        o.quantity * o.unit_price AS line_total,
        c.region,
        c.segment,
        ...
    FROM raw_orders o
    JOIN dim_customers c ON o.customer_id = c.customer_id;

CREATE OR REPLACE DYNAMIC TABLE dt_orders_daily
    TARGET_LAG = '30 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        DATE_TRUNC('day', order_date) AS order_day,
        region,
        segment,
        COUNT(*) AS order_count,
        SUM(line_total) AS daily_revenue
    FROM dt_orders_enriched
    GROUP BY ALL;
```

The silver table (`dt_orders_enriched`) uses TARGET\_LAG = DOWNSTREAM so it refreshes only
when the gold table needs fresh data. The gold table (`dt_orders_daily`) owns the
time-based freshness goal and drives the entire pipeline. A common variation adds a
second gold table that rolls up hourly data into daily totals as an additional aggregation
layer.

## Synchronize multiple pipelines with a controller table

A controller dynamic table merges independent pipelines into a single coordinated refresh. When
triggered, the controller reads all inputs at the same timestamp. Between controller refreshes, leaf tables refresh on their own schedules. Use this pattern when a dashboard or downstream consumer joins data from
independent domains that must be temporally consistent.

The controller is a zero-row dynamic table that depends on multiple leaf tables. Leaves
have their own time-based target lag and refresh independently between controller
refreshes.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = '5 minutes'
    WAREHOUSE = transform_wh
AS
    SELECT order_id, customer_id, order_date, line_total
    FROM raw_orders;

CREATE OR REPLACE DYNAMIC TABLE dt_returns
    TARGET_LAG = '5 minutes'
    WAREHOUSE = transform_wh
AS
    SELECT return_id, order_id, return_date, refund_amount
    FROM raw_returns;

CREATE OR REPLACE DYNAMIC TABLE dt_checkpoint
    TARGET_LAG = DOWNSTREAM
    WAREHOUSE = transform_wh
AS
    SELECT 1 AS sync_flag FROM dt_orders, dt_returns LIMIT 0;
```

If the controller breaks, leaves continue refreshing independently on their own
schedules. If one leaf dynamic table fails, the controller also fails. Monitor all tables
in the controller group, not the controller alone.

Important

Avoid listing too many leaf tables in the FROM clause. The cross join in the controller is
never run (because of LIMIT 0), but compilation time grows with the number of tables.
For pipelines with more than five or six leaves, consider grouping leaves into
intermediate controllers.

## Latest row deduplication with SCD Type 1

When your base table receives append-only change data capture (CDC) records, use
QUALIFY ROW\_NUMBER to keep only the latest row per business key. The window function
picks the correct row regardless of ingestion order, handling out-of-order arrival without additional logic.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_customers_current
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT * EXCLUDE (raw_metadata_col)
    FROM raw_customers_cdc
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY updated_at DESC
    ) = 1;
```

Using `SELECT * EXCLUDE` supports incremental schema evolution: columns added to or dropped from the
base table automatically propagate without changing the dynamic table definition.
For more on schema evolution, see [Modify dynamic tables](/user-guide/dynamic-tables/modify).

To handle soft deletes, add a filter to the QUALIFY expression:

Copy code

```
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY updated_at DESC
) = 1
AND NOT is_deleted
```

This expresses soft-delete logic as a single window expression with no additional orchestration.

For best incremental performance, use a monotonic ORDER BY column (a sequence number or timestamp that only increases). Keep the QUALIFY expression as the top-level construct in the dynamic table. If you need further transformations, place them in a downstream dynamic table rather than combining them in the same definition.

Tip

Use `ROW_TIMESTAMP` as the built-in mechanism for tracking when rows were last refreshed.
This is cleaner than adding `CURRENT_TIMESTAMP()` as a column in the definition, which
forces full refresh mode.

## Stream-static join with full CDC (MERGE)

A stream-static join reads only the rows that changed since the last refresh (from a source
using `CHANGES()`) and joins them with a dimension table that provides lookup values. The
dimension table is read in full on each refresh but doesn’t drive which rows are processed.

For an append-only variant using INSERT INTO SELF, see
[Append-only enrichment](/user-guide/dynamic-tables/custom-incrementalization#label-dynamic-tables-custom-incremental-examples).

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_enriched_inventory (
  sku_id INT, product_name STRING, category STRING,
  warehouse_name STRING, region STRING, qty_on_hand INT
)
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
  REFRESH USING (
    MERGE INTO SELF AS tgt
    USING (
      SELECT s.sku_id, p.product_name, p.category,
             w.warehouse_name, w.region, s.qty_on_hand,
             s.METADATA$ACTION AS action,
             ROW_NUMBER() OVER (
               PARTITION BY s.sku_id
               ORDER BY s.event_timestamp DESC,
                        CASE s.METADATA$ACTION WHEN 'INSERT' THEN 0 ELSE 1 END
             ) AS rn
      FROM stock CHANGES(INFORMATION => DEFAULT) AS s
      LEFT OUTER JOIN products   AS p ON s.product_id   = p.product_id
      LEFT OUTER JOIN warehouses AS w ON s.warehouse_id  = w.warehouse_id
      QUALIFY rn = 1
    ) AS src
    ON tgt.sku_id = src.sku_id
    WHEN MATCHED AND src.action = 'DELETE' THEN
      DELETE
    WHEN MATCHED AND src.action = 'INSERT' THEN
      UPDATE SET
        tgt.product_name   = src.product_name,
        tgt.category       = src.category,
        tgt.warehouse_name = src.warehouse_name,
        tgt.region         = src.region,
        tgt.qty_on_hand    = src.qty_on_hand
    WHEN NOT MATCHED AND src.action = 'INSERT' THEN
      INSERT (sku_id, product_name, category, warehouse_name, region, qty_on_hand)
      VALUES (src.sku_id, src.product_name, src.category, src.warehouse_name,
              src.region, src.qty_on_hand)
  );
```

This pattern enriches CDC changes from `stock` with dimension lookups before merging:

- `stock` changes are enriched with dimension tables (`products`, `warehouses`) through LEFT OUTER JOIN.
- ROW\_NUMBER deduplication ensures one source row per key for the MERGE.
- When a key has both DELETE and INSERT in the same interval (an update), the INSERT is kept.
- Deletes propagate, inserts create new rows, and updates modify existing rows.

## Top-K leaderboard (MERGE reading SELF)

This pattern uses [custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization)
to maintain a bounded top-K result set that shrinks or grows as scores change.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_leaderboard (player_id INT, total_score INT, rank INT)
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
  REFRESH USING (
    MERGE INTO SELF AS tgt
    USING (
      WITH candidates AS (
        SELECT
          COALESCE(ch.player_id, cur.player_id) AS player_id,
          COALESCE(ch.total_score, cur.total_score) AS total_score
        FROM SELF AS cur
        FULL OUTER JOIN (
          SELECT player_id, total_score
          FROM player_scores CHANGES()
          WHERE METADATA$ACTION = 'INSERT'
        ) AS ch ON cur.player_id = ch.player_id
      ),
      ranked AS (
        SELECT *, ROW_NUMBER() OVER (
          ORDER BY total_score DESC, player_id ASC
        ) AS new_rank
        FROM candidates
      )
      SELECT player_id, total_score, new_rank FROM ranked
    ) AS src
    ON tgt.player_id = src.player_id
    WHEN MATCHED AND src.new_rank <= 3 THEN
      UPDATE SET tgt.total_score = src.total_score, tgt.rank = src.new_rank
    WHEN MATCHED AND src.new_rank > 3 THEN
      DELETE
    WHEN NOT MATCHED AND src.new_rank <= 3 THEN
      INSERT (player_id, total_score, rank)
      VALUES (src.player_id, src.total_score, src.new_rank)
  );
```

This pattern maintains a bounded top-K result set that shrinks or grows as scores change:

- `FROM SELF AS cur` reads the dynamic table’s current contents. SELF can be both the MERGE target and a read source.
- FULL OUTER JOIN merges the current state with incoming changes from `player_scores`.
- Players dropping below rank 3 are deleted; new top-3 players are inserted.
- Custom incremental dynamic tables can maintain bounded-size result sets that standard refresh modes can’t express, and these result sets can be reused as memoized state for the next round of incrementalization. In the example above, the previous top-K results are combined with current changes to derive fresh results, instead of having to scan all historical data.

## Daily snapshot (no CHANGES clause)

Not every custom incremental dynamic table needs `CHANGES()`. You can re-read source data on each refresh and accumulate snapshots over time using `ROW_TIMESTAMP`.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_daily_snapshot (
    id INT,
    val STRING
)
    TARGET_LAG = '1 day'
    WAREHOUSE = transform_wh
    ROW_TIMESTAMP = TRUE
    REFRESH USING (
        INSERT INTO SELF
        SELECT id, val
        FROM src
    );
```

Each refresh appends a full snapshot of `src` into the dynamic table. `ROW_TIMESTAMP = TRUE` automatically records when each row was inserted into the dynamic table, making it easy to query point-in-time state. Because there’s no `CHANGES()` clause, every refresh reads the full source. Keep the source small or use filtering to control cost.

## Anti-patterns

These patterns cause failures or unexpected behavior in production.

### Setting all tables to TARGET\_LAG = DOWNSTREAM

**Why it fails:** If no dynamic table in the pipeline has a time-based target lag, nothing
triggers a refresh. The pipeline produces tables that don’t change and no error is raised.

**What to do instead:** At least one dynamic table (the terminal table) must have a
time-based target lag. Intermediate tables use DOWNSTREAM.

Copy code

```
-- Wrong: nothing triggers a refresh
CREATE OR REPLACE DYNAMIC TABLE dt_staging
    TARGET_LAG = DOWNSTREAM ...;
CREATE OR REPLACE DYNAMIC TABLE dt_summary
    TARGET_LAG = DOWNSTREAM ...;

-- Correct: terminal table drives the pipeline
CREATE OR REPLACE DYNAMIC TABLE dt_summary
    TARGET_LAG = '30 minutes' ...;
```

### Short target lag relative to retention time

**Why it fails:** If lag exceeds the retention window due to transient errors, the table goes stale and requires reinitialization.

**What to do instead:** Set target lag several times shorter than retention time to leave a buffer for recovery. This applies to both incremental and full refresh modes.

## What’s next

- [Quick-start best practices for dynamic tables](/user-guide/dynamic-tables/best-practices)
- [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization)
- [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag)
- [Modify dynamic tables](/user-guide/dynamic-tables/modify)
- [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost)
- For workloads that require imperative logic or don’t fit these patterns, see [Decision guide for dynamic tables](/user-guide/dynamic-tables/decision-guide).
