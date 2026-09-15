# Share dynamic tables with other accounts

Providers share dynamic tables by granting SELECT through a share. Consumers can query those tables directly or build their own pipelines on top. This page covers both workflows.

For the full syntax reference, see [CREATE SHARE](/sql-reference/sql/create-share).

## Provider workflow: share a dynamic table

To share a dynamic table, create a share, grant the required database and schema privileges, then grant SELECT on the dynamic table.

### Enable change tracking before sharing

Consumers can’t enable change tracking on shared objects, so providers must run `ALTER TABLE <name> SET CHANGE_TRACKING = TRUE` on each base table before adding it to a share.

### Grant a dynamic table to a share

The following example shares a single dynamic table with one consumer account:

Copy code

```
-- Create the share and grant the required privileges
CREATE SHARE analytics_share;

GRANT USAGE ON DATABASE analytics_db TO SHARE analytics_share;
GRANT USAGE ON SCHEMA analytics_db.public TO SHARE analytics_share;
GRANT SELECT ON DYNAMIC TABLE analytics_db.public.dt_orders_daily TO SHARE analytics_share;

-- To share every dynamic table in a schema, use ALL DYNAMIC TABLES instead:
-- GRANT SELECT ON ALL DYNAMIC TABLES IN SCHEMA analytics_db.public TO SHARE analytics_share;

-- Add consumer accounts (comma-separated for multiple accounts)
ALTER SHARE analytics_share ADD ACCOUNTS = consumer_org.consumer_account;
```

### Sharing across regions and clouds

- **Same region:** Use a Direct Share ([Data sharing and collaboration in Snowflake](/guides-overview-sharing)).
- **Cross-region or cross-cloud:** Add the share or application package to a listing and set up Cross-Cloud Auto-Fulfillment ([Create and publish a listing](/collaboration/provider-listings-creating-publishing)).
- **Native Apps:** Add dynamic tables to an application package ([Share data content in a Snowflake Native App](/developer-guide/native-apps/preparing-data-content)).

## Consumer workflow: query shared dynamic tables

A consumer account can query a shared dynamic table the same way it queries any shared object. The provider’s refresh schedule continues
to run, and the consumer sees the latest refreshed data.

### Create a database from a share

Copy code

```
CREATE DATABASE shared_analytics FROM SHARE provider_org.provider_account.analytics_share;
GRANT IMPORTED PRIVILEGES ON DATABASE shared_analytics TO ROLE analyst_role;
```

### Query the shared dynamic table

Copy code

```
SELECT order_day, region, order_count, daily_revenue
FROM shared_analytics.public.dt_orders_daily
ORDER BY order_day DESC
LIMIT 5;
```

```
+------------+---------+-------------+---------------+
| ORDER_DAY  | REGION  | ORDER_COUNT | DAILY_REVENUE |
|------------+---------+-------------+---------------|
| 2025-01-16 | EU-West |           1 |         62.50 |
| 2025-01-15 | US-West |           2 |        149.97 |
| 2025-01-15 | US-East |           1 |         49.99 |
+------------+---------+-------------+---------------+
```

Note

The share boundary is a pipeline boundary: consumer and provider tables refresh independently, with no coordinated scheduling or target lag propagation across accounts.

## Consumer workflow: build a pipeline on shared data

A consumer can create a dynamic table on top of shared data. The pattern depends on whether the provider shared a base table, a dynamic table, or a view.

### On a shared base table

If the provider enabled change tracking on the base table before sharing, the consumer can create a dynamic table directly. This
also works when the provider shares a view (secure or non-secure) with no dynamic table in the view’s dependencies, over change-tracked base tables.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_consumer_summary
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT
    order_date::DATE AS order_day,
    COUNT(*) AS total_orders,
    SUM(quantity * unit_price) AS total_revenue
  FROM shared_analytics.public.raw_orders
  GROUP BY ALL;
```

### On a shared dynamic table

When a consumer builds a dynamic table on top of a shared dynamic table, the share boundary decouples the two pipelines. Refreshes (including incremental) run independently with no cross-account coordination.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_regional_report
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
AS
  SELECT *
  FROM shared_analytics.public.dt_orders_daily
  WHERE region = 'US-West';
```

The consumer’s target lag is independent of the provider’s. The consumer dynamic table sees the provider’s latest available data at
each refresh. There is no snapshot isolation across the share boundary.

Monitoring across the share boundary

Your refresh history shows SUCCEEDED even when the provider’s data is stale. You can’t monitor the provider’s refresh health directly.

To detect unexpected staleness: if your results are identical across several refresh cycles, the provider may have stopped refreshing.

### On a shared view that references a dynamic table

If the provider shares a view (secure or non-secure) whose dependencies include a dynamic table, wrap the view in `DYNAMIC_TABLE_REFRESH_BOUNDARY()`:

Snowflake can’t coordinate refresh schedules across a view’s dynamic table dependency when that view comes from another account. The wrapper tells Snowflake to treat the view as an independently-refreshed input.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_from_shared_view
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT *
  FROM DYNAMIC_TABLE_REFRESH_BOUNDARY(shared_analytics.public.v_daily_metrics);
```

Without the boundary wrapper, the statement fails.

If you are unsure whether a shared view depends on a dynamic table, wrapping it in `DYNAMIC_TABLE_REFRESH_BOUNDARY()` is always safe. The function has no effect when the view’s dependencies do not include a dynamic table.

For the full explanation of pipeline boundaries, including same-account scenarios, see [Decouple pipelines with DYNAMIC\_TABLE\_REFRESH\_BOUNDARY()](/user-guide/dynamic-tables/data-consistency#label-dynamic-tables-data-consistency-boundary-function).

## Supported sharing patterns

| Provider shares | Consumer can query? | Consumer can build a dynamic table on top? |
| --- | --- | --- |
| Dynamic table | Yes | Yes |
| Base table (change tracking enabled) | Yes | Yes |
| View (no dynamic table in the view’s dependencies) | Yes | Yes (if change tracking is enabled on the view’s base tables) |
| View (dynamic table in the view’s dependencies) | Yes | Yes (wrap the view in `DYNAMIC_TABLE_REFRESH_BOUNDARY()`) |

Expand

Show lessSee more

### Error: change tracking not enabled

If the provider didn’t enable change tracking before sharing a base table, the consumer sees this error when creating a dynamic table:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_consumer_summary
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
  SELECT *
  FROM shared_analytics.public.raw_orders;
```

```
091930 (2F003): SQL compilation error:
Change tracking is not enabled or has been missing for the time
range requested on table 'SHARED_ANALYTICS.PUBLIC.RAW_ORDERS'.
```

To fix this, ask the provider to run `ALTER TABLE <name> SET CHANGE_TRACKING = TRUE` on the base table.

## What’s next

- [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring) to track refresh health after sharing.
- [Manage dynamic tables](/user-guide/dynamic-tables/manage) to suspend or resume shared dynamic tables.
- [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes) if shared dynamic tables stop refreshing.
