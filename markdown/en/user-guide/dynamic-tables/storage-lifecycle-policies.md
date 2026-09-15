# Use storage lifecycle policies with dynamic tables

You can attach [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) to dynamic
tables to delete or archive rows that match a predicate, on a schedule that runs independently of dynamic table refresh.

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

To attach a storage lifecycle policy directly to a dynamic table, use the WITH STORAGE LIFECYCLE POLICY clause in the [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table)
statement or the ADD STORAGE LIFECYCLE POLICY clause in the [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) statement.

## How storage lifecycle policies work with dynamic tables

Rows that match the policy predicate form the dynamic table’s expired region. The expired region behaves like
a [frozen region](/user-guide/dynamic-tables/frozen-regions): refresh treats those rows as frozen and
never processes them. Storage lifecycle policy execution runs asynchronously on its own schedule (see
[Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies)), independent of dynamic table refresh.

A row can fall in both the frozen region and the expired region. The frozen region protects rows
from being processed by refresh, not from being expired by the policy: when the policy runs, it still
deletes or archives those rows.

## Limitations

The following limitations apply when you attach a storage lifecycle policy to a dynamic table:

- If a dynamic table is created using the [`BACKFILL FROM`](/user-guide/dynamic-tables/frozen-regions#label-create-dt-using-backfill)
  clause, storage lifecycle policies on the backfill table aren’t copied to the new dynamic table. Attach a
  policy to the new dynamic table separately.
- The policy predicate is subject to the same restrictions as a
  [frozen region](/user-guide/dynamic-tables/frozen-regions) predicate. For the full list of
  restrictions on supported expressions, see
  [Frozen region predicate limitations](/user-guide/dynamic-tables/frozen-regions#label-dts-frozen-where-limitations).
- The policy predicate can’t reference metadata columns, including
  [METADATA$ROW\_LAST\_COMMIT\_TIME](/user-guide/data-engineering/row-timestamps). Although standard tables support
  storage lifecycle policies on row timestamps, dynamic tables don’t. Attaching such a policy returns an
  unsupported feature error. Use a regular timestamp column in the dynamic table’s definition instead.

## Reinitialization triggers

Changing or removing a storage lifecycle policy can trigger reinitialization on the dynamic table’s next
refresh, depending on how the change affects the expired region. The following table lists the changes on a
dynamic table and whether they trigger reinitialization:

| Change | Triggers reinitialization? |
| --- | --- |
| Shortening retention (expired region grows; for example, `INTERVAL '2 weeks'` to `INTERVAL '1 week'`) | No. The next policy run deletes the newly expired rows. |
| Lengthening retention (expired region shrinks; for example, `INTERVAL '1 week'` to `INTERVAL '2 weeks'`) | Yes. The dynamic table must reprocess rows that were previously in the expired region. |
| Removing the policy, changing its predicate, or applying it to different columns | Yes. |

Expand

Show lessSee more

When a storage lifecycle policy change triggers reinitialization, the refresh-history `REINIT_REASON` column
contains a value identifying the storage lifecycle policy change. To query refresh history, see
[DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history).

For the canonical list of all reinitialization triggers, see
[What triggers reinitialization](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).
For dynamic table cost guidance, see [Understanding compute cost](/user-guide/cost-understanding-compute).

## Example: Limited retention dynamic table

The following dynamic table contains the most recent week of orders from the base table. The attached policy expires
rows older than one week, so the dynamic table retains only the most recent week:

Copy code

```
CREATE STORAGE LIFECYCLE POLICY expire_after_1w
  AS (ts TIMESTAMP) RETURNS BOOLEAN -> ts < CURRENT_TIMESTAMP() - INTERVAL '1 week';

CREATE OR REPLACE DYNAMIC TABLE dt_orders
  TARGET_LAG = '1 minute'
  WAREHOUSE = transform_wh
  WITH STORAGE LIFECYCLE POLICY expire_after_1w ON (order_date)
  AS
    SELECT order_id, customer_id, order_date, product_name, quantity, unit_price, order_status
    FROM raw_orders;
```

## Example: Unlimited retention dynamic table and base table with limited retention

The following example reuses the `expire_after_1w` policy defined in the previous example. It attaches the
policy to the `raw_orders` base table, then creates a dynamic table that aggregates those orders into daily
summaries that are retained indefinitely. The dynamic table uses a frozen region so that once a
day is closed, its aggregate row is no longer refreshed from the base table. This makes it safe for the
storage lifecycle policy to expire the older rows in the base table:

Copy code

```
ALTER TABLE raw_orders ADD STORAGE LIFECYCLE POLICY expire_after_1w ON (order_date);

CREATE OR REPLACE DYNAMIC TABLE dt_orders_daily (order_day DATE, region VARCHAR, order_count NUMBER, daily_revenue NUMBER)
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
  FROZEN WHERE (order_day < DATEADD('day', -2, CURRENT_DATE))
  AS
    SELECT DATE_TRUNC('DAY', o.order_date) AS order_day, c.region,
           COUNT(*) AS order_count, SUM(o.quantity * o.unit_price) AS daily_revenue
    FROM raw_orders o
    JOIN dim_customers c ON o.customer_id = c.customer_id
    GROUP BY 1, 2;
```

The storage lifecycle policy retention (one week) must be longer than the frozen region lag so that every day’s
aggregate is finalized before its corresponding base-table rows expire.

## What’s next

- For dynamic table compute and storage costs, see [Understanding compute cost](/user-guide/cost-understanding-compute).
- For more about frozen regions, including the interaction with storage lifecycle policies, see [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions).
- For the canonical list of reinitialization triggers, including those caused by storage lifecycle policy changes, see [What triggers reinitialization](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).
