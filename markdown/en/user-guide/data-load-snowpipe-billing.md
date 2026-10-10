# Snowpipe costs

In all Snowflake editions, Snowpipe charges a fixed number of credits for each GB of data that your pipes load. You don’t pay for warehouse time or for the number of files that you load, so your Snowpipe cost depends mainly on how much data you load and on the format of the files.

## How Snowpipe billing works

For the current credit rate per GB, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). The billed size of a file depends on its type:

| File type | Examples | Billed size |
| --- | --- | --- |
| Text | CSV, JSON, XML | Uncompressed size |
| Binary | Avro, ORC, Parquet | Size in storage (observed size), regardless of compression |

Expand

Show lessSee more

For example, a gzip-compressed CSV file that’s 1 GB in storage and 5 GB uncompressed is billed as 5 GB. A Parquet file that’s 1 GB in storage is billed as 1 GB.

The following factors don’t change what you pay:

- **Compute**: Snowflake provides and scales the compute for every load. There’s no warehouse to size, and no charge for load duration.
- **Number of files**: There’s no per-file charge, so delivering the same data in more or fewer files doesn’t change what you pay. File size and staging frequency still affect latency and throughput. For recommendations, see [File sizing for Snowpipe](/user-guide/data-load-considerations-prepare#label-snowpipe-file-size).

Snowpipe previously charged for the compute time used to load files, measured per second and per core, plus a fee for every 1,000 files. Snowflake moved Business Critical and Virtual Private Snowflake (VPS) accounts to the credit-per-GB model on August 1, 2025, and Standard and Enterprise accounts on December 8, 2025.

## Estimate Snowpipe costs

To estimate your Snowpipe cost, add up the billed size of the files that you expect to load, and then multiply that total by the rate in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). For compressed text files, use their uncompressed size. If you know only their compressed size, multiply it by the compression ratio of your files.

For example, suppose that each day you load two sets of files: 200 GB of gzip-compressed CSV files that are 1,000 GB uncompressed, and 100 GB of Parquet files. The following table shows the billed size of each:

| Files | Size in storage | Billed size |
| --- | --- | --- |
| CSV files (gzip) | 200 GB | 1,000 GB (uncompressed) |
| Parquet files | 100 GB | 100 GB (observed) |
| **Total for one day** | **300 GB** | **1,100 GB** |

Expand

Show lessSee more

At a rate of 0.0037 credits per GB, which is the rate in the [December 8, 2025 release note](/release-notes/2025/other/2025-12-08-snowpipe-simplified-pricing), this workload uses 1,100 × 0.0037 = 4.07 credits per day, or about 122 credits for a 30-day month. To convert credits to a dollar amount, multiply by the price per credit in your Snowflake agreement.

To check an estimate against real usage, load a representative set of files, and then compare your estimate with the `BYTES_BILLED` and `CREDITS_USED` values for the pipe, as described in [Monitor Snowpipe costs](#label-snowpipe-billing-monitor).

## Monitor Snowpipe costs

The privileges that you need depend on where you look:

- **Snowsight**: The `ACCOUNTADMIN` role, or a role that’s granted the `APP_USAGE_VIEWER` application role and the `USAGE_VIEWER` database role. For more information, see [Access control for cost management](/user-guide/cost-access-control).
- **The `PIPE_USAGE_HISTORY` table function**: The `ACCOUNTADMIN` role, or a role that has the `MONITOR USAGE` global privilege.
- **The `PIPE_USAGE_HISTORY` view**: A role that has the `IMPORTED PRIVILEGES` privilege on the `SNOWFLAKE` database, or that’s granted the `USAGE_VIEWER` database role. The per-pipe query in [Monitor costs with SQL](#label-snowpipe-billing-monitor-sql) also reads the `PIPES` view. If the role uses database roles instead of `IMPORTED PRIVILEGES`, it also needs the `OBJECT_VIEWER` database role. For more information, see [ACCOUNT\_USAGE schema SNOWFLAKE database roles](/sql-reference/account-usage#label-account-usage-snowflake-db-roles).

### Monitor costs in Snowsight

To see Snowpipe credits in Snowsight, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to cost and usage data](/user-guide/cost-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select a warehouse to use to view the usage data.
5. Select **Consumption**, and then select **Compute** from the usage type list.
6. Above the bar graph, select **By Service**. Snowpipe credits appear as `PIPE`.

For more information, see [Exploring compute cost](/user-guide/cost-exploring-compute).

### Monitor costs with SQL

Query either of the following:

- The [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history) in the Account Usage schema, which covers the last 365 days. Data in the view can be up to 3 hours behind.
- The [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) table function in the Information Schema, which covers the last 14 days. The function is generally deprecated in favor of the view, so use it only when you need usage from the last few hours, which the view might not show yet. If you don’t specify `DATE_RANGE_START`, the function returns only the last 10 minutes.

Both return the `CREDITS_USED` and `BYTES_BILLED` columns, along with the number of files and bytes loaded. The view returns rows for each pipe. The table function returns totals for all pipes unless you specify the `PIPE_NAME` argument.

The following query returns the credits used and bytes billed for each pipe, for each day in the last 30 days. `PIPE_NAME` doesn’t include the database or schema, so the query joins the [PIPES view](/sql-reference/account-usage/pipes) to tell apart pipes with the same name in different schemas:

Copy code

```
SELECT TO_DATE(u.start_time) AS usage_date,
       COALESCE(p.pipe_catalog || '.' || p.pipe_schema || '.' || p.pipe_name, u.pipe_name) AS pipe,
       SUM(u.credits_used) AS total_credits,
       SUM(u.bytes_billed) AS total_bytes_billed
  FROM snowflake.account_usage.pipe_usage_history u
  LEFT JOIN snowflake.account_usage.pipes p
    ON u.pipe_id = p.pipe_id
  WHERE u.start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY usage_date, pipe
  ORDER BY usage_date, total_credits DESC;
```

The results also include automated refreshes of external tables, directory tables, and Apache Iceberg™ tables, which use Snowpipe internally. For how these rows appear and how they’re billed, see [Other charges related to Snowpipe](#label-snowpipe-billing-other-charges).

The following query returns the average daily credits and bytes billed for each week in the last year. Use it to spot unexpected increases in Snowpipe usage. Days with no Snowpipe usage aren’t included in the averages. If your account moved to per-GB billing during this period, expect a change in credits on that date that isn’t caused by your workload:

Copy code

```
WITH usage_by_day AS (
  SELECT TO_DATE(start_time) AS usage_date,
         SUM(credits_used) AS daily_credits,
         SUM(bytes_billed) AS daily_bytes_billed
    FROM snowflake.account_usage.pipe_usage_history
    WHERE start_time >= DATEADD('year', -1, CURRENT_TIMESTAMP())
    GROUP BY usage_date
)
SELECT DATE_TRUNC('week', usage_date) AS usage_week,
       AVG(daily_credits) AS avg_daily_credits,
       AVG(daily_bytes_billed) AS avg_daily_bytes_billed
  FROM usage_by_day
  GROUP BY usage_week
  ORDER BY usage_week;
```

## Control Snowpipe costs

To track and reduce Snowpipe spending, use the following approaches:

- **Set a budget.** Add pipes to a [custom budget](/user-guide/budgets/custom-budget) with a spending limit. The budget sends a notification when spending is projected to exceed the limit. Budgets don’t stop pipes on their own, but a budget can [call a stored procedure](/user-guide/budgets/custom-actions) when projected or actual spending reaches a threshold, such as a procedure that [pauses pipes](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-pause-resume). If a pipe stays paused for longer than 14 days, it becomes [stale](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe). [Resource monitors](/user-guide/resource-monitors) can’t control Snowpipe credit usage, because they apply only to warehouses that you manage.
- **Load only the files that you need.** End stage URLs and pipe paths with a forward slash (`/`), and enable event filtering in your cloud provider, so that Snowpipe loads only the files that belong in the target table. For more information, see [Best practices](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-best-practices).
- **Avoid loading the same data twice.** If two pipes watch overlapping paths, or if you load the same files with both Snowpipe and `COPY INTO`, Snowflake loads and bills the same data twice. For more information, see [Duplicate data in the target table](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-duplicate-data).
- **Prefer binary formats when you control the producer.** A compressed CSV file is billed on its uncompressed size, so the same data in Parquet, Avro, or ORC files, which are billed on their observed size, can cost much less. For an example, see [Estimate Snowpipe costs](#label-snowpipe-billing-estimate).

## Other charges related to Snowpipe

Some charges appear under Snowpipe even though they don’t come from your pipes, and some charges for related work are billed separately.

### Snowpipe charges that don’t come from your pipes

Automated refreshes for [external tables](/user-guide/tables-external-intro), [directory tables](/user-guide/data-load-dirtables), and [Iceberg tables](/user-guide/tables-iceberg-auto-refresh) use Snowpipe internally, so their charges appear under Snowpipe on your bill and in the `PIPE_USAGE_HISTORY` view, even though they aren’t for pipes that you created.

These refreshes aren’t billed per GB; they’re billed for the compute time that they use. For external tables and directory tables, the refresh charges also include an overhead that increases with the number of files that are added to cloud storage. Automated refresh for Iceberg tables doesn’t incur this per-file overhead.

In the `PIPE_USAGE_HISTORY` view, rows for these refreshes show the name of the refreshed table, or `NULL`, in `PIPE_NAME`. They can show credits with `BYTES_INSERTED` and `FILES_INSERTED` values of 0. For more information, see [Billing for external tables](/user-guide/tables-external-intro#label-external-tables-billing), [Billing for directory tables](/user-guide/data-load-dirtables#label-directory-tables-billing), and [billing for automated refresh of Iceberg tables](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-billing).

### Related charges that are billed separately

The following charges are related to Snowpipe but billed separately:

- **Event logging**: Recording [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) in an event table. For more information, see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).
- **Replication**: Replicating pipes and their target tables, including when you use [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines). For more information, see [Understanding replication cost](/user-guide/account-replication-cost).
- **Warehouse compute**: Loading files with `COPY INTO`, for example to [backfill historical files](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill) or to [reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).
- **Storage**: Storing data in standard tables, in Iceberg tables that use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), and in internal stages, which Snowflake bills until you remove them. For Iceberg tables that use an external volume, your cloud storage provider bills you for the table’s data. With `LOAD_MODE = ADD_FILES_COPY`, you also pay to store the source files until you delete them.
- **Data transfer**: Reading files from cloud storage in a different region or on a different cloud platform from your Snowflake account. Snowflake doesn’t charge for data ingress, but your cloud storage provider might charge an egress fee. For more information, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).
