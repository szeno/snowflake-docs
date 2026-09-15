# Create a dynamic table

This tutorial shows how to create a dynamic table and connect it into a two-table pipeline.

For the full syntax reference, see [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

Note

This tutorial assumes you know how to create tables and write SELECT queries. If you are new to
Snowflake, complete the [Snowflake in 20 minutes](/user-guide/tutorials/snowflake-in-20minutes)
tutorial first.

The examples on this page use CREATE OR ALTER DYNAMIC TABLE, which creates the dynamic table if it
doesn’t exist, or alters it to match the definition if it does. Run them in a test database and
schema to avoid unintended changes to production data.

## Before you start

Make sure you have USAGE on a warehouse and schema, and CREATE DYNAMIC TABLE on the target schema.
For full requirements, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

## Set up base tables

Create a base table and a dimension table, then insert sample data so you can copy and run every
example on this page:

Copy code

```
CREATE OR REPLACE TABLE raw_orders (
    order_id       INT,
    customer_id    INT,
    order_date     TIMESTAMP_NTZ,
    product_name   VARCHAR,
    quantity       INT,
    unit_price     DECIMAL(10,2),
    order_status   VARCHAR,
    CONSTRAINT pk_raw_orders PRIMARY KEY (order_id) RELY
);

INSERT INTO raw_orders (order_id, customer_id, order_date, product_name, quantity, unit_price, order_status)
VALUES
    (1001, 1, '2025-01-15 08:30:00', 'Widget A',  3, 29.99, 'completed'),
    (1002, 2, '2025-01-15 09:45:00', 'Widget B',  1, 49.99, 'completed'),
    (1003, 1, '2025-01-15 14:20:00', 'Widget A',  2, 29.99, 'pending'),
    (1004, 3, '2025-01-16 10:00:00', 'Gadget X',  5, 12.50, 'completed'),
    (1005, 2, '2025-01-16 11:30:00', 'Widget B',  1, 49.99, 'returned');
```

The downstream dynamic table in this tutorial also joins to a dimension table. Create that
table now:

Copy code

```
CREATE OR REPLACE TABLE dim_customers (
    customer_id    INT,
    customer_name  VARCHAR,
    region         VARCHAR,
    segment        VARCHAR,
    CONSTRAINT pk_dim_customers PRIMARY KEY (customer_id) RELY
);

INSERT INTO dim_customers (customer_id, customer_name, region, segment)
VALUES
    (1, 'Acme Corp',  'US-West',  'Enterprise'),
    (2, 'Globex Inc', 'US-East',  'Mid-Market'),
    (3, 'Initech LLC','EU-West',  'Startup');
```

Tip

Primary keys are optional but improve incremental refresh performance. Both base tables declare a PRIMARY KEY with RELY so Snowflake can identify changed rows during refresh. For more
information, see [primary key best practices](/user-guide/dynamic-tables/best-practices#label-dynamic-tables-bp-primary-keys).

## Create a dynamic table

Run the following statement to create a dynamic table that filters out returned orders and computes
a line total for each row:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        order_id,
        customer_id,
        order_date,
        TRIM(UPPER(product_name)) AS product_name,
        quantity,
        unit_price,
        quantity * unit_price AS line_total,
        order_status
    FROM raw_orders
    WHERE order_status != 'returned';
```

Note

If you omit REFRESH\_MODE, it defaults to AUTO and Snowflake selects incremental or full refresh
at creation time. This tutorial sets REFRESH\_MODE = INCREMENTAL explicitly so the refresh mode is
deterministic across recreations. For details on how each mode works, see
[Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).

The key parameters beyond the table name are:

- **TARGET\_LAG**: The freshness goal for the data. Snowflake schedules refreshes to keep data
  no more than 10 minutes behind the source. Actual staleness can exceed this depending on refresh
  runtime.
- **WAREHOUSE**: The compute resource that runs scheduled refreshes.
- **REFRESH\_MODE**: Determines how Snowflake processes changes. `INCREMENTAL` reprocesses only
  changed rows. `FULL` refreshes the entire table from scratch on every refresh. See the note that follows for guidance.

The dynamic table initializes immediately after creation by default.

Note

Set REFRESH\_MODE explicitly for production workloads to avoid unexpected refresh mode changes.
See [choosing a refresh mode](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-mode-decision) for details.

## Verify with SHOW DYNAMIC TABLES

The CREATE statement does not report the resolved refresh mode. Run SHOW DYNAMIC TABLES to confirm the mode and verify that `scheduling_state` is `RUNNING`:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders';
```

```
+------------+-----+--------------+---------------------+------------------+--------------+-----+
| name       | ... | refresh_mode | refresh_mode_reason | scheduling_state | warehouse    | ... |
|------------+-----+--------------+---------------------+------------------+--------------+-----|
| DT_ORDERS | ... | INCREMENTAL  | NULL                | RUNNING          | TRANSFORM_WH | ... |
+------------+-----+--------------+---------------------+------------------+--------------+-----+
```

Check that `refresh_mode` shows the mode you expect and `scheduling_state` is `RUNNING`.

## Add a downstream dynamic table

A downstream dynamic table reads from another dynamic table instead of a base table. This
downstream table joins `dt_orders` with `dim_customers` and aggregates daily revenue by region and
segment:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE dt_orders_daily
    TARGET_LAG = '30 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        s.order_date::DATE AS order_day,
        c.region,
        c.segment,
        COUNT(*) AS order_count,
        SUM(s.line_total) AS daily_revenue
    FROM dt_orders s
    JOIN dim_customers c ON s.customer_id = c.customer_id
    GROUP BY ALL;
```

Snowflake tracks the dependency between dynamic tables and refreshes them in the correct order
automatically (see [pipeline ordering](/user-guide/dynamic-tables/overview#label-dynamic-tables-overview-how-it-works)), so `dt_orders` is always refreshed before `dt_orders_daily`.

Note

The TARGET\_LAG of a downstream dynamic table must be greater than or equal to the TARGET\_LAG of
the dynamic table it depends on. In this example, `dt_orders_daily` (30 minutes) is greater than
`dt_orders` (10 minutes). For more information, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).

## Query the pipeline output

Copy code

```
SELECT * FROM dt_orders_daily ORDER BY order_day, region;
```

```
+------------+---------+------------+-------------+---------------+
| ORDER_DAY  | REGION  | SEGMENT    | ORDER_COUNT | DAILY_REVENUE |
|------------+---------+------------+-------------+---------------|
| 2025-01-15 | US-East | Mid-Market |           1 |         49.99 |
| 2025-01-15 | US-West | Enterprise |           2 |        149.95 |
| 2025-01-16 | EU-West | Startup    |           1 |         62.50 |
+------------+---------+------------+-------------+---------------+
```

`dt_orders` excludes the returned order (order 1005), so it does not appear in the
aggregated results.

To visualize the pipeline you created, navigate to **Transformation** » **Dynamic tables** in Snowsight, select any table in the pipeline, and open the **Graph** tab. For more on pipeline visualization, see [View the pipeline graph in Snowsight](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitor-view-graph-snowsight).

## Check refresh history

After verifying the query output, confirm that refreshes are completing successfully:

Copy code

```
SELECT name, state, state_message,
       refresh_trigger, refresh_action,
       data_timestamp
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY())
WHERE name IN ('DT_ORDERS', 'DT_ORDERS_DAILY')
ORDER BY data_timestamp DESC
LIMIT 10;
```

For more ways to monitor refresh status, set up alerts, and troubleshoot failures, see
[Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).

## Troubleshoot common issues

**Dynamic table shows no data:** If your dynamic table was created successfully but returns no
rows, verify that the query returns data when run as a standalone SELECT. A common cause is a
WHERE clause that filters out all current rows. Also check:

- If the table was created by a different role, access or masking policies may filter data
  differently for your current role.
- Verify that you have the correct warehouse, database, and schema context and that you have
  SELECT privilege on the base tables.

**Refresh mode is FULL instead of INCREMENTAL:** If SHOW DYNAMIC TABLES shows `refresh_mode` as
`FULL` when you expected `INCREMENTAL`, your definition contains a SQL feature that doesn’t support
incremental refresh. Check the `refresh_mode_reason` column for details, and see
[Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries) for the full list of supported query patterns.

## Clean up

If you created these objects for testing purposes, drop them to avoid ongoing warehouse costs from
scheduled refreshes:

Copy code

```
DROP DYNAMIC TABLE IF EXISTS dt_orders_daily;
DROP DYNAMIC TABLE IF EXISTS dt_orders;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS raw_orders;
```

## What’s next

- Choose a target lag for your workload: [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag)
- Understand incremental versus full refresh: [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes)
- Monitor refresh history and troubleshoot failures: [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring)
- Create or modify a dynamic table idempotently without DROP semantics: [Modify dynamic tables](/user-guide/dynamic-tables/modify)
