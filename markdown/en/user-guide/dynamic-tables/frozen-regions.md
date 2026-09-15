# Frozen regions and backfill

Dynamic tables are defined by a query that Snowflake re-executes periodically to keep the table
current. Each re-execution is called a [refresh](/user-guide/dynamic-tables/refresh-modes).
A frozen region reduces refresh cost by telling Snowflake which rows to skip during refresh.

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

| Clause | What it does | Acts on |
| --- | --- | --- |
| FROZEN WHERE | Freezes dynamic table rows that match a predicate. Refresh skips those rows. | Output side |

Expand

Show lessSee more

The following example freezes output rows older than 30 days:

Copy code

```
-- Frozen region: freeze output rows older than 30 days
CREATE OR ALTER DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_date < CURRENT_TIMESTAMP() - INTERVAL '30 days')
AS
  SELECT
    order_id, customer_id, order_date,
    ...
  FROM raw_orders
  WHERE order_status != 'returned';
```

For the full `dt_orders` column list, see [Create a dynamic table](/user-guide/dynamic-tables/create).

## How frozen regions work

Rows that match the frozen region predicate are in the frozen region. Rows that don’t
match are in the active region. During each refresh, Snowflake refreshes only the active
region.

Key behaviors:

- **Initial refresh**: The predicate is ignored during initialization, and all rows are
  computed.
- **Subsequent refreshes**: Only the active region is refreshed, regardless of refresh mode.
- **Reinitialization**: Only the active region is refreshed during reinitialization.
- **Storage lifecycle policies**: If a dynamic table has both a storage lifecycle policy
  and a frozen region, the policy predicate acts as an additional frozen region.
  Rows that fall in both the frozen region and the expired region are still
  deleted when the policy runs. For more information, see [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies).
- **Data governance policies on base tables**: If you apply or alter a data governance policy on a
  base table after frozen rows exist, rows in the frozen region keep the values they had
  before the policy was applied or altered. To enforce the policy on frozen rows, apply it directly
  to the dynamic table. For related caveats, see
  [Column-level security considerations](/user-guide/security-column-intro#considerations).

Frozen region predicates can’t contain subqueries, nondeterministic functions (except
timestamp functions), user-defined or external functions, or metadata columns. Columns in the
predicate must be columns in the dynamic table, not columns from the base table. For the
complete list of restrictions, see the
[Frozen region usage notes](/sql-reference/sql/create-dynamic-table#label-frozen-where-dt-usage-notes).

To check which rows are frozen, query the `METADATA$IS_FROZEN` metadata column:

Copy code

```
SELECT order_id, order_date, line_total, METADATA$IS_FROZEN AS is_frozen
  FROM dt_orders
  ORDER BY order_date DESC
  LIMIT 5;
```

```
+----------+-------------------------+------------+-----------+
| ORDER_ID | ORDER_DATE              | LINE_TOTAL | IS_FROZEN |
|----------+-------------------------+------------+-----------|
| 1005     | 2025-01-16 11:30:00.000 |      49.99 | FALSE     |
| 1004     | 2025-01-16 10:00:00.000 |      62.50 | FALSE     |
| 1003     | 2025-01-15 14:20:00.000 |      59.98 | TRUE      |
| 1002     | 2025-01-15 09:45:00.000 |      49.99 | TRUE      |
| 1001     | 2025-01-15 08:30:00.000 |      89.97 | TRUE      |
+----------+-------------------------+------------+-----------+
```

## Seed a dynamic table with BACKFILL FROM

BACKFILL FROM copies existing data into a new dynamic table without recomputing it. Use
backfill to migrate existing pipelines, avoid expensive initialization when the table has
years of historical data, or recover from data issues.

BACKFILL FROM is only available in CREATE DYNAMIC TABLE. You can’t add backfill to an existing
dynamic table with ALTER.

The backfill source must contain matching columns with compatible data types in the same order
as the dynamic table. You can also specify a point in time using the AT or BEFORE clause to
copy data from a specific Time Travel snapshot.

When you combine BACKFILL FROM with a frozen region:

- The frozen region is cloned from the backfill source.
- The active region is computed from the definition.

The following limitations apply when you work with [frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions):

- Currently, only regular and dynamic tables can be used for backfilling.
- You can’t specify policies or tags in the new dynamic table because they are copied from the backfill table.
- Clustering keys in the new dynamic table and backfill table must be the same.

Copy code

```
-- dt_orders_snapshot is a regular table or clone containing historical order data.
-- Backfill the frozen region from the snapshot, compute recent data from the definition.
CREATE OR REPLACE DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_date < '2025-01-01')
  BACKFILL FROM dt_orders_snapshot
AS
  SELECT
    order_id, customer_id, order_date,
    ...
  FROM raw_orders
  WHERE order_status != 'returned';
```

You can also backfill from a specific Time Travel snapshot using the AT or BEFORE clause:

Copy code

```
-- Backfill from a Time Travel snapshot at a specific point in time.
CREATE OR REPLACE DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_date < '2025-01-01')
  BACKFILL FROM dt_orders_snapshot AT (TIMESTAMP => '2025-04-01 12:00:00'::TIMESTAMP_NTZ)
AS
  SELECT
    order_id, customer_id, order_date,
    ...
  FROM raw_orders
  WHERE order_status != 'returned';
```

Copy code

```
-- Backfill from just before a specific statement was executed.
CREATE OR REPLACE DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_date < '2025-01-01')
  BACKFILL FROM dt_orders_snapshot BEFORE (STATEMENT => '<statement_id>')
AS
  SELECT
    order_id, customer_id, order_date,
    ...
  FROM raw_orders
  WHERE order_status != 'returned';
```

For the full `dt_orders` column list, see [Create a dynamic table](/user-guide/dynamic-tables/create).

## Add or remove a frozen region

You can add, change, or remove a frozen region on an existing dynamic table using either
CREATE OR ALTER DYNAMIC TABLE or ALTER DYNAMIC TABLE. Adding or expanding a frozen region
doesn’t trigger reinitialization. Shrinking or removing it does.

### Change the frozen region predicate

To add or change the frozen region predicate, use CREATE OR ALTER DYNAMIC TABLE with the
`FROZEN WHERE` clause:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_date < '2025-01-01')
AS
  SELECT
    order_id, customer_id, order_date,
    ...
  FROM raw_orders
  WHERE order_status != 'returned';
```

You can also use ALTER DYNAMIC TABLE with the `SET FROZEN WHERE` clause:

Copy code

```
ALTER DYNAMIC TABLE dt_orders
  SET FROZEN WHERE (order_date < '2025-01-01');
```

Changing the predicate can trigger a reinitialization of the active region, depending on
whether the change expands or shrinks the frozen region.

Changes that expand the frozen region (such as `<= 2023` to `<= 2024`) don’t trigger
reinitialization. Changes that shrink or reshape the frozen region (such as `< '2025-01-02'`
to `< '2025-01-01'`) do trigger reinitialization. To apply this type of change, use either of the approaches shown above with the updated predicate.

### Remove a frozen region

Caution

Removing a frozen region triggers a full reinitialization on the next refresh.
This reprocesses all rows, including those that were previously in the frozen region.

To remove the frozen region, use CREATE OR ALTER DYNAMIC TABLE without a `FROZEN WHERE`
clause, or run `ALTER DYNAMIC TABLE <name> UNSET FROZEN WHERE`.

## DML into a frozen region

You can DML (INSERT, UPDATE, MERGE, DELETE) into frozen regions of dynamic tables. This enables use cases such as time-sensitive GDPR deletes, or catching up on records that have changed, without paying the cost of reprocessing all the rows.

Copy code

```
DELETE FROM dt_orders
  WHERE customer_id = 105;
```

## Verify a frozen region

To view the frozen region predicate on a dynamic table, run SHOW DYNAMIC TABLES and check
the `immutable_where` column. The column displays the predicate text, or NULL if no clause
is set:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders';
```

```
+------------+-------------------------------------------+
| name       | immutable_where                           |
|------------+-------------------------------------------|
| DT_ORDERS | order_date < '2025-01-01'::TIMESTAMP_NTZ  |
+------------+-------------------------------------------+
```

To check individual row status, query `METADATA$IS_FROZEN`:

Copy code

```
SELECT
  COUNT_IF(METADATA$IS_FROZEN) AS frozen_rows,
  COUNT_IF(NOT METADATA$IS_FROZEN) AS active_rows
FROM dt_orders;
```

```
+-------------+-------------+
| FROZEN_ROWS | ACTIVE_ROWS |
|-------------+-------------|
|           3 |           2 |
+-------------+-------------+
```

## Interaction with RELY constraints

[RELY constraints](/sql-reference/constraints-overview) tell the optimizer to trust that a
primary key or unique constraint holds, without enforcing it. When a dynamic table has both a
frozen region and at least one RELY constraint, the columns in the predicate must
appear in every RELY PRIMARY KEY and RELY UNIQUE constraint on the table. Put another way,
predicate columns must be in the intersection of all RELY constraint column sets.

| Table constraints | Allowed in the frozen region predicate |
| --- | --- |
| RELY primary key on `(A, B)`, RELY unique on `(B, C)` | `B` only |
| RELY primary key on `(A)`, RELY unique on `(A, B)` | `A` only |

Expand

Show lessSee more

Snowflake validates this rule when you add or change either the predicate or a RELY constraint.
If the resulting state violates the rule, the statement fails.

Note

RELY constraints can’t be declared in the CREATE DYNAMIC TABLE column list. To add a primary key or unique constraint to a dynamic table, use `ALTER TABLE <name> ADD CONSTRAINT ... RELY` after the table is created.

The following example shows one ALTER TABLE statement that succeeds and one that fails. The
first succeeds because `order_date` is in the RELY primary key. The second fails because
`order_date` is in the primary key but not in the unique constraint’s columns, so it’s not in
the intersection of all RELY constraints:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_date < '2025-01-01')
AS
  SELECT
    order_id,
    order_date,
    customer_id,
    line_total
  FROM raw_orders;

-- Succeeds: order_date is in the RELY primary key.
ALTER TABLE dt_orders ADD CONSTRAINT pk_orders PRIMARY KEY (order_id, order_date) RELY;

-- Fails: uq_customer does not include order_date, so order_date is no longer
-- in the intersection of all RELY constraints.
ALTER TABLE dt_orders ADD CONSTRAINT uq_customer UNIQUE (order_id, customer_id) RELY;
```

```
002857 (55000): If a FROZEN WHERE clause is used with a PRIMARY KEY RELY constraint or a
UNIQUE RELY constraint, the column(s) used in the FROZEN WHERE clause must be a subset of
the intersection of the columns used in the RELY constraints. If no such column exists, the
specified FROZEN WHERE clause or RELY constraint cannot be used together.
```

## What’s next

- For information about compute costs, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
- For query construct limitations that affect refresh mode, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
- To monitor refresh operations, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
