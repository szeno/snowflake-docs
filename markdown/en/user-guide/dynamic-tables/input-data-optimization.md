# Optimize input data for dynamic tables

This page explains how primary keys and clustering help Snowflake process fewer rows during each refresh.
Pipeline developers should read this page before building pipelines over base tables that use INSERT OVERWRITE
or other full-replacement loading patterns.

Add a primary key with the RELY property to your base table. This lets Snowflake detect which rows actually changed after an INSERT OVERWRITE, rather than treating every row as new:

Copy code

```
ALTER TABLE dim_customers
  ADD CONSTRAINT pk_dim_customers PRIMARY KEY (customer_id) RELY;
```

## How primary keys reduce refresh work

During each refresh, Snowflake must determine which rows changed in the base tables. Without a primary key,
an INSERT OVERWRITE replaces all change-tracking metadata, and Snowflake treats every row as new. This forces
a full refresh even when only a small fraction of the data actually changed.

When a base table has a PRIMARY KEY constraint with the RELY property, Snowflake uses those key values as
stable row identifiers across updates. It compares primary key values before and after the overwrite, identifies
only the rows that actually changed, and processes those rows through downstream dynamic tables.

RELY does not enforce uniqueness

RELY does not prevent future duplicates. Validate uniqueness in your upstream ETL before setting RELY, and repeat the check after every load cycle.

Copy code

```
SELECT customer_id, COUNT(*) AS cnt
FROM dim_customers
GROUP BY customer_id
HAVING cnt > 1;
```

```
+-------------+-----+
| CUSTOMER_ID | CNT |
|-------------+-----|
-- (no rows = safe to use RELY)
```

## Types of primary keys for dynamic tables

Snowflake recognizes two kinds of primary key for change tracking. The following table summarizes when each
applies.

| Type | How it is created | When to use |
| --- | --- | --- |
| Base table PRIMARY KEY with RELY | You declare the constraint on the base table and set RELY. | Base tables loaded by INSERT OVERWRITE, COPY INTO, or external ETL. |
| System-derived unique key | Snowflake infers it from the dynamic table’s definition (GROUP BY or QUALIFY ROW\_NUMBER() = 1). | Dynamic tables that produce one row per key by construction. |

Expand

Show lessSee more

### Base table primary key with RELY

When a base table has a PRIMARY KEY constraint with the RELY property, Snowflake uses that key for row-level
change tracking in all downstream dynamic tables. This is the primary mechanism for optimizing INSERT OVERWRITE
workloads.

Copy code

```
CREATE OR REPLACE TABLE dim_products (
  product_id   INT PRIMARY KEY RELY,
  product_name VARCHAR,
  category     VARCHAR,
  price        DECIMAL(10,2)
);
```

### System-derived unique key

Snowflake can automatically derive a unique key from a dynamic table’s definition. The following constructs
produce a system-derived unique key:

- **GROUP BY**: The grouping columns form the key because each group produces exactly one output row.
- **QUALIFY ROW\_NUMBER() = 1**: The partition-by columns form the key because the filter keeps exactly one row
  per partition.
- **Base table primary key passthrough**: If the dynamic table definition passes through a RELY primary key column without applying functions, casts, or expressions, the system-derived unique key propagates to the dynamic table.

To check whether a dynamic table has a system-derived unique key, run SHOW UNIQUE KEYS:

Copy code

```
SHOW UNIQUE KEYS IN dt_orders;
```

```
+----------------------------+-----------+--------+-------------+-----------+-----+----------------+
| CREATED_ON                 | TABLE_NAME| SCHEMA | COLUMN_NAME | KEY_INDEX | ... | CONSTRAINT_TYPE|
|----------------------------+-----------+--------+-------------+-----------+-----+----------------|
| 2025-01-15 08:32:28 +0000 | DT_ORDERS| TUTORIAL| ORDER_ID   |         1 | ... | UNIQUE         |
+----------------------------+-----------+--------+-------------+-----------+-----+----------------+
```

If the query returns no rows, the dynamic table doesn’t have a system-derived unique key.
Downstream dynamic tables can use incremental refresh against a full-refresh upstream when at least one of these conditions is met:

1. The upstream has a [system-derived unique key](#system-derived-unique-key).
2. The upstream has a [frozen region](/user-guide/dynamic-tables/frozen-regions).

Otherwise, creating a downstream table with `REFRESH_MODE = INCREMENTAL` fails, and `REFRESH_MODE = AUTO` resolves to FULL.

## Optimize INSERT OVERWRITE workloads

INSERT OVERWRITE is the most common loading pattern that benefits from primary keys. Without a primary key,
every INSERT OVERWRITE looks like a full delete-and-reinsert to Snowflake, even when only a few rows
changed.

The following example shows the recommended pattern. The base table declares a PRIMARY KEY with RELY, and the
downstream dynamic table uses incremental refresh:

Copy code

```
CREATE OR REPLACE TABLE dim_customers (
  customer_id   INT PRIMARY KEY RELY,
  customer_name VARCHAR,
  region        VARCHAR,
  segment       VARCHAR
);

-- External ETL rewrites this table nightly with INSERT OVERWRITE.
-- Snowflake uses the primary key to detect which rows actually changed.
CREATE OR REPLACE DYNAMIC TABLE dt_customer_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT
    o.order_id, o.customer_id,
    c.customer_name, c.region,
    ... -- remaining columns omitted for brevity
  FROM raw_orders o
  JOIN dim_customers c ON o.customer_id = c.customer_id;
```

When the external ETL process runs INSERT OVERWRITE on `dim_customers`, Snowflake compares primary key
values before and after the overwrite, identifies only the changed dimension rows, and refreshes only the
fact rows that join to those changed dimensions.

Note

If adding a primary key to your base table isn’t feasible, consider using [ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-adaptive) as an alternative. ADAPTIVE can handle INSERT OVERWRITE workloads without requiring primary keys on the base table.

How base table replacement methods affect primary keys

Not all table-replacement patterns preserve the primary key constraint and change-tracking history.

| Method | Primary key preserved? | Change history preserved? | Atomic? | Effect on downstream dynamic tables |
| --- | --- | --- | --- | --- |
| [INSERT … OVERWRITE](/sql-reference/sql/insert) (recommended) | Yes | Yes | Yes | Only changed rows are processed. |
| TRUNCATE + INSERT/COPY INTO | Yes | Yes | No (table is empty between the two statements). | Same as INSERT OVERWRITE once the load completes, but a refresh that runs mid-load sees an empty table. |
| CREATE OR REPLACE TABLE | No (primary key is dropped unless redeclared). | No (all streams become stale). | Yes | Full reinitialization required. Even if you redeclare the primary key, there is no before-state to compare against on the initial refresh. |

Expand

Show lessSee more

Use INSERT OVERWRITE for base tables that feed dynamic table pipelines. Avoid CREATE OR REPLACE on tables
that already have downstream dynamic tables.

## Enable incremental refresh downstream of full refresh

Normally, a dynamic table with `REFRESH_MODE = INCREMENTAL` can’t read from a dynamic table with
`REFRESH_MODE = FULL`, because the full refresh discards change-tracking metadata. When the upstream full
refresh dynamic table has a system-derived unique key, Snowflake can compute the differences between full
refreshes, and downstream tables can refresh incrementally.

Set REFRESH\_MODE = INCREMENTAL explicitly

To use incremental refresh downstream of a full refresh dynamic table with a system-derived unique key,
you must explicitly set `REFRESH_MODE = INCREMENTAL` on the downstream table. Setting `REFRESH_MODE = AUTO`
still resolves to FULL in this scenario.

### Example: GROUP BY produces a system-derived unique key

Copy code

```
-- Full refresh: GROUP BY produces a system-derived unique key on (order_day, region, segment).
CREATE OR REPLACE DYNAMIC TABLE dt_orders_daily
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
  REFRESH_MODE = FULL
AS
  SELECT
    DATE_TRUNC('day', s.order_date) AS order_day,
    c.region,
    c.segment,
    COUNT(*) AS order_count,
    SUM(s.line_total) AS daily_revenue
  FROM dt_orders s
  JOIN dim_customers c ON s.customer_id = c.customer_id
  GROUP BY ALL;

-- Downstream incremental: works because dt_orders_daily has a system-derived unique key.
CREATE OR REPLACE DYNAMIC TABLE dt_region_trends
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT
    region,
    AVG(daily_revenue) AS avg_daily_revenue,
    COUNT(*) AS days_with_orders
  FROM dt_orders_daily
  GROUP BY region;
```

### Verify the system-derived unique key

Before creating a downstream incremental dynamic table, verify that the upstream table has a system-derived
unique key:

Copy code

```
SHOW UNIQUE KEYS IN dt_orders_daily;
```

```
+----------------------------+------------------+--------+-------------+-----------+-----+----------------+
| CREATED_ON                 | TABLE_NAME       | SCHEMA | COLUMN_NAME | KEY_INDEX | ... | CONSTRAINT_TYPE|
|----------------------------+------------------+--------+-------------+-----------+-----+----------------|
| 2025-01-15 10:00:00 +0000 | DT_ORDERS_DAILY | TUTORIAL| ORDER_DAY  |         1 | ... | UNIQUE         |
| 2025-01-15 10:00:00 +0000 | DT_ORDERS_DAILY | TUTORIAL| REGION     |         2 | ... | UNIQUE         |
| 2025-01-15 10:00:00 +0000 | DT_ORDERS_DAILY | TUTORIAL| SEGMENT    |         3 | ... | UNIQUE         |
+----------------------------+------------------+--------+-------------+-----------+-----+----------------+
```

If SHOW UNIQUE KEYS returns no rows, the downstream CREATE with `REFRESH_MODE = INCREMENTAL` fails:

Copy code

```
-- This fails if the upstream table has no system-derived unique key.
CREATE OR REPLACE DYNAMIC TABLE dt_downstream_agg
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT region, SUM(daily_revenue) AS total_revenue
  FROM dt_orders_daily
  GROUP BY region;
```

```
SQL compilation error:
Incremental refresh mode is not supported because the upstream dynamic table
does not have a unique key for change tracking.
```

## Pair primary keys with clustering

Primary keys tell Snowflake which rows changed. Clustering determines how efficiently Snowflake can
locate those rows. When the base table is clustered on or near the primary key columns, Snowflake can typically
prune more micro-partitions during refresh and read less data.

For the best results:

- Cluster base tables on the primary key column or the column most frequently used in join conditions with
  downstream dynamic tables.
- If the base table already has a clustering key for query performance, check whether it overlaps with the
  primary key. Overlapping keys benefit both query pruning and refresh pruning.
- Be aware that background reclustering creates new micro-partitions, which can cause temporary spikes in
  refresh duration. These spikes are transient and resolve after reclustering completes.

For general clustering guidance, see [Micro-partitions & Data Clustering](/user-guide/tables-clustering-micropartitions).

## Detect primary-key tracking degradation

Primary key-based change tracking can degrade or stop working without producing an error. Snowflake
doesn’t raise an exception in these cases. Instead, it falls back to standard change-tracking columns, which
eliminates the performance benefit of primary key-based tracking.

| Scenario | What happens | How to detect |
| --- | --- | --- |
| Duplicate primary key values in the base table | Change tracking may produce unexpected results (rows miscounted or missed). | Run a GROUP BY / HAVING query on the primary key column before setting RELY. |
| Masking policy on a primary key column | Snowflake can’t read the key values and falls back to standard change-tracking columns. | Check whether masking policies are applied to any primary key column. |
| ALTER TABLE drops the primary key constraint | The system-derived unique key disappears from downstream dynamic tables. | Run SHOW UNIQUE KEYS after schema changes. |

Expand

Show lessSee more

### Masking policy on a primary key column

When a masking policy obfuscates a primary key column, Snowflake can’t use that column for change tracking.
The dynamic table continues to refresh, but Snowflake falls back to standard change-tracking columns. For
INSERT OVERWRITE workloads, this fallback means every refresh processes all rows, because INSERT OVERWRITE
resets the standard tracking columns. For normal DML operations (INSERT, UPDATE, DELETE), the standard
change-tracking columns can still detect row-level changes.

To detect this, check whether any masking policies are applied to primary key columns:

Copy code

```
-- Check for masking policies on columns used in primary keys
SELECT * FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
  REF_ENTITY_NAME => 'dim_customers',
  REF_ENTITY_DOMAIN => 'TABLE'
));
```

If a masking policy is applied to a primary key column, primary key-based change tracking is disabled regardless of
SHOW UNIQUE KEYS output. Remove the masking policy from the primary key column or move it to a non-key column.

---

## Try it: Compare refresh with and without primary keys

This tutorial builds two pipelines with the same data and the same join query. The only difference is whether
the dimension table has a primary key. You then simulate a dimension table rewrite with INSERT OVERWRITE and
compare the refresh performance.

### Prerequisites

- A Snowflake account with privileges to create databases, schemas, and dynamic tables.
- An X-Small warehouse. The tutorial uses `transform_wh` in all examples.

### Step 1: Create the source data

Copy code

```
CREATE DATABASE IF NOT EXISTS mydb;
CREATE SCHEMA IF NOT EXISTS mydb.myschema;
USE SCHEMA mydb.myschema;

-- Dimension table WITH primary key
CREATE OR REPLACE TABLE dim_products_with_pk (
  product_id   INT PRIMARY KEY RELY,
  product_name VARCHAR(200),
  category     VARCHAR(100),
  price        DECIMAL(10,2)
) CHANGE_TRACKING = TRUE;

-- Dimension table WITHOUT primary key (same schema otherwise)
CREATE OR REPLACE TABLE dim_products_no_pk (
  product_id   INT,
  product_name VARCHAR(200),
  category     VARCHAR(100),
  price        DECIMAL(10,2)
) CHANGE_TRACKING = TRUE;

-- Shared fact table
CREATE OR REPLACE TABLE fact_orders (
  order_id   INT,
  product_id INT,
  quantity   INT,
  order_date TIMESTAMP_NTZ
) CHANGE_TRACKING = TRUE;
```

Insert 100,000 products into both dimension tables and 10 million orders into the fact table:

Copy code

```
INSERT INTO dim_products_with_pk (product_id, product_name, category, price)
  SELECT
    SEQ4() + 1 AS product_id,
    'Product ' || LPAD(TO_VARCHAR(SEQ4() + 1), 6, '0') AS product_name,
    'Category ' || LPAD(TO_VARCHAR(MOD(SEQ4(), 10) + 1), 2, '0') AS category,
    ROUND(5.00 + MOD(SEQ4(), 500) * 0.50, 2) AS price
  FROM TABLE(GENERATOR(ROWCOUNT => 100000));

INSERT INTO dim_products_no_pk
  SELECT * FROM dim_products_with_pk;

INSERT INTO fact_orders (order_id, product_id, quantity, order_date)
  SELECT
    SEQ4() + 1 AS order_id,
    MOD(SEQ4(), 100000) + 1 AS product_id,
    MOD(SEQ4(), 10) + 1 AS quantity,
    DATEADD(SECOND, SEQ4(), '2025-01-01 00:00:00') AS order_date
  FROM TABLE(GENERATOR(ROWCOUNT => 10000000));
```

### Step 2: Create two pipelines and run the initial refresh

Create one pipeline with the primary key dimension table and one without. Both use the same join query.

Copy code

```
-- Pipeline WITH primary key
CREATE OR REPLACE DYNAMIC TABLE dt_enriched_with_pk
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT
    f.order_id, f.product_id, d.product_name, d.category,
    f.quantity, d.price, f.quantity * d.price AS order_total, f.order_date
  FROM fact_orders f
  JOIN dim_products_with_pk d ON f.product_id = d.product_id;

-- Pipeline WITHOUT primary key
CREATE OR REPLACE DYNAMIC TABLE dt_enriched_no_pk
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
  SELECT
    f.order_id, f.product_id, d.product_name, d.category,
    f.quantity, d.price, f.quantity * d.price AS order_total, f.order_date
  FROM fact_orders f
  JOIN dim_products_no_pk d ON f.product_id = d.product_id;

-- Run the initial refresh for both
ALTER DYNAMIC TABLE dt_enriched_with_pk REFRESH;
ALTER DYNAMIC TABLE dt_enriched_no_pk REFRESH;
```

### Step 3: Simulate INSERT OVERWRITE and compare

Rewrite both dimension tables, changing the price for 10% of products (Category 01) while keeping all other
rows identical:

Copy code

```
INSERT OVERWRITE INTO dim_products_with_pk
  SELECT product_id, product_name, category,
    CASE WHEN category = 'Category 01' THEN ROUND(price * 1.10, 2) ELSE price END AS price
  FROM dim_products_with_pk;

INSERT OVERWRITE INTO dim_products_no_pk
  SELECT product_id, product_name, category,
    CASE WHEN category = 'Category 01' THEN ROUND(price * 1.10, 2) ELSE price END AS price
  FROM dim_products_no_pk;
```

Refresh both pipelines and compare their performance:

Copy code

```
ALTER DYNAMIC TABLE dt_enriched_no_pk REFRESH;
ALTER DYNAMIC TABLE dt_enriched_with_pk REFRESH;
```

Check the refresh history for each:

Copy code

```
SELECT name, state, refresh_trigger,
  DATEDIFF('second', refresh_start_time, refresh_end_time) AS duration_seconds,
  statistics:numInsertedRows::INT AS num_inserted_rows,
  statistics:numDeletedRows::INT AS num_deleted_rows
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME_PREFIX => 'MYDB.MYSCHEMA.DT_ENRICHED_',
  ERROR_ONLY => FALSE
))
ORDER BY refresh_start_time DESC
LIMIT 4;
```

```
+-----------------------+-----------+-----------------+------------------+-------------------+------------------+
| NAME                  | STATE     | REFRESH_TRIGGER | DURATION_SECONDS | NUM_INSERTED_ROWS | NUM_DELETED_ROWS |
|-----------------------+-----------+-----------------+------------------+-------------------+------------------|
| DT_ENRICHED_WITH_PK   | SUCCEEDED | MANUAL          |               12 |           1000000 |          1000000 |
| DT_ENRICHED_NO_PK     | SUCCEEDED | MANUAL          |               34 |          10000000 |         10000000 |
| DT_ENRICHED_WITH_PK   | SUCCEEDED | MANUAL          |               45 |          10000000 |                0 |
| DT_ENRICHED_NO_PK     | SUCCEEDED | MANUAL          |               46 |          10000000 |                0 |
+-----------------------+-----------+-----------------+------------------+-------------------+------------------+
```

The pipeline with the primary key processed only the 1 million fact rows that reference the changed 10% of
dimension rows. The pipeline without a primary key refreshed all 10 million rows because Snowflake couldn’t
distinguish changed rows from unchanged rows after the INSERT OVERWRITE.

Tip

The performance gap widens as fact tables grow and the fraction of changed dimension rows shrinks. In
production pipelines with millions of dimension rows and single-digit percentage changes per load cycle,
primary key-based change tracking can reduce refresh times by an order of magnitude.

### Clean up

Copy code

```
DROP DATABASE mydb;
```

## What’s next

- [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization) for query-level tuning of incremental refresh.
- [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions) to skip unchanged historical partitions.
- [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring) to track refresh duration and detect regressions.
- [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost) to understand the credit impact of refresh modes.
- [Quick-start best practices for dynamic tables](/user-guide/dynamic-tables/best-practices)
