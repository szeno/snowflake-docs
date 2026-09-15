# Understanding costs for dynamic tables

This page explains the three cost components of dynamic tables (virtual warehouse compute, Cloud Services compute,
and storage), how to estimate and monitor those costs with SQL, and the common patterns that cause unexpected charges.

To find how much a specific dynamic table costs, start with this query. It summarizes refresh activity
by table and refresh type, showing how many refreshes ran and how many rows were processed.

Copy code

```
SELECT
    name,
    refresh_action,
    COUNT(*) AS refreshes,
    SUM(
        statistics:numInsertedRows::INT
        + statistics:numDeletedRows::INT
        + statistics:numCopiedRows::INT
    ) AS total_rows_processed
FROM
    TABLE(
        INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
            NAME_PREFIX => 'mydb.myschema.',
            RESULT_LIMIT => 1000
        )
    )
WHERE
    refresh_action != 'NO_DATA'
GROUP BY
    name, refresh_action
ORDER BY
    total_rows_processed DESC;
```

```
+-------------------------------------+----------------+-----------+-----------------------+
| NAME                                | REFRESH_ACTION | REFRESHES | TOTAL_ROWS_PROCESSED  |
|-------------------------------------+----------------+-----------+-----------------------+
| MYDB.MYSCHEMA.DT_ORDERS_DAILY      | INCREMENTAL    |        72 |                 48200 |
| MYDB.MYSCHEMA.DT_ORDERS            | INCREMENTAL    |       144 |                 12050 |
+-------------------------------------+----------------+-----------+-----------------------+
```

## Three cost components

Every dynamic table incurs costs in three categories. The relative weight of each depends on how often refreshes run,
warehouse size, and data volume.

| Component | What drives cost | How it is billed |
| --- | --- | --- |
| **Virtual warehouse compute** | Refresh queries that run on the assigned warehouse. Larger warehouse or more frequent refreshes increase cost. | Per-second credits based on warehouse size. For details, see [Understanding compute cost](/user-guide/cost-understanding-compute). |
| **Cloud Services compute** | Metadata checks that detect upstream changes and decide whether a warehouse refresh is needed. Runs on every refresh cycle, even when no data has changed. | Billed daily, but only when Cloud Services credits exceed 10% of that day’s total warehouse credits. For details, see [Cloud Services billing](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage). |
| **Storage** | Materialized results, Time Travel data, and fail-safe copies. Incremental refresh adds a small per-row metadata column. | Standard Snowflake storage rates. For details, see [Understanding storage cost](/user-guide/cost-understanding-data-storage). Dynamic Apache Iceberg tables use external storage and don’t incur Snowflake storage costs. |

Expand

Show lessSee more

## Virtual warehouse compute costs

Virtual warehouse compute is the primary cost for most dynamic table workloads. Each dynamic table uses its assigned
warehouse to run refreshes. The cost per refresh depends on the warehouse size, the complexity of the definition, and the
volume of data processed. For complete details on how warehouse billing works (including per-second billing and the
60-second minimum), see [Understanding compute cost](/user-guide/cost-understanding-compute).

Key behaviors:

- If Snowflake detects no upstream changes, the warehouse stays suspended and no compute credits are consumed.
- If base tables have changes, the warehouse resumes and runs a refresh even if the refresh produces no output rows after filtering.
- You can assign separate warehouses for regular refreshes (WAREHOUSE) and reinitialization (INITIALIZATION\_WAREHOUSE).
  For more information, see [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).

To check warehouse credit consumption for a specific dynamic table, query DYNAMIC\_TABLE\_REFRESH\_HISTORY and
join with QUERY\_HISTORY:

Copy code

```
SELECT
    r.name AS dynamic_table_name,
    r.refresh_action,
    r.state,
    q.warehouse_size,
    q.credits_used_cloud_services,
    q.total_elapsed_time / 1000 AS elapsed_seconds
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'mydb.myschema.dt_orders',
    RESULT_LIMIT => 10
)) r
LEFT JOIN TABLE(INFORMATION_SCHEMA.QUERY_HISTORY()) q
    ON r.query_id = q.query_id
WHERE r.state = 'SUCCEEDED'
ORDER BY r.data_timestamp DESC;
```

```
+------------------------------+----------------+-----------+----------------+----------------------------------+------------------+
| DYNAMIC_TABLE_NAME           | REFRESH_ACTION | STATE     | WAREHOUSE_SIZE | CREDITS_USED_CLOUD_SERVICES      | ELAPSED_SECONDS  |
|------------------------------+----------------+-----------+----------------+----------------------------------+------------------+
| MYDB.MYSCHEMA.DT_ORDERS     | INCREMENTAL    | SUCCEEDED | X-Small        |                         0.000024 |             1.82 |
| MYDB.MYSCHEMA.DT_ORDERS     | INCREMENTAL    | SUCCEEDED | X-Small        |                         0.000019 |             0.94 |
+------------------------------+----------------+-----------+----------------+----------------------------------+------------------+
```

Tip

To isolate dynamic table costs during testing, use a dedicated warehouse. This lets you attribute all
credits on that warehouse to dynamic table refreshes. After you establish a cost baseline, you can move
dynamic tables to a shared warehouse. For more information, see [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).

## Cloud Services costs and the 10% billing threshold

Cloud Services credits cover metadata operations (change detection, query compilation, and scheduling) that run on every refresh cycle regardless of whether data has changed. Each active dynamic table incurs this overhead independently.

### How the 10% threshold works

Cloud Services credits are billed only when the daily total exceeds 10% of that day’s warehouse compute credits.
This is an account-level daily calculation in UTC, not per-warehouse or per-dynamic-table. For the full billing
formula and examples, see
[Understanding billing for cloud services usage](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage).

Short target lag amplifies Cloud Services costs

Cloud Services costs scale with the number of active dynamic tables, the target lag, and pipeline depth. Each
dynamic table independently performs change-detection checks on every refresh cycle. With many dynamic tables at
short target lag, Cloud Services charges can exceed the 10% threshold and result in direct charges.

A pipeline of 200 dynamic tables with a 1-minute target lag generates approximately 288,000 change-detection
checks per day (200 tables x 1,440 cycles). Even when no data has changed, these checks accumulate Cloud Services credits.

To reduce Cloud Services costs:

- Increase target lag where near-real-time freshness isn’t required.
- Use `TARGET_LAG = DOWNSTREAM` for intermediate dynamic tables in a pipeline so they refresh only when needed.
- Suspend dynamic tables outside business hours in non-production environments.
- Monitor Cloud Services consumption with [METERING\_HISTORY view](/sql-reference/account-usage/metering_history).

For general patterns that drive Cloud Services costs, see [Optimizing cloud services for cost](/user-guide/cost-optimize-cloud-services).

Check whether your account is exceeding the 10% threshold:

Copy code

```
SELECT
    START_TIME::DATE AS usage_date,
    ROUND(SUM(credits_used_compute), 2) AS compute_credits,
    ROUND(SUM(credits_used_cloud_services), 2) AS cs_credits,
    ROUND(SUM(credits_used_compute) * 0.10, 2) AS cs_included,
    ROUND(GREATEST(SUM(credits_used_cloud_services) - (SUM(credits_used_compute) * 0.10), 0), 2)
        AS cs_billed
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY usage_date
ORDER BY usage_date DESC;
```

```
+------------+-----------------+------------+-------------+-----------+
| USAGE_DATE | COMPUTE_CREDITS | CS_CREDITS | CS_INCLUDED | CS_BILLED |
|------------+-----------------+------------+-------------+-----------+
| 2025-01-20 |           50.00 |       6.00 |        5.00 |      1.00 |
| 2025-01-19 |           48.50 |       4.20 |        4.85 |      0.00 |
+------------+-----------------+------------+-------------+-----------+
```

## Storage costs

Dynamic tables store materialized results and incur standard Snowflake storage costs. For general information
about how storage is billed, see [Understanding storage cost](/user-guide/cost-understanding-data-storage). Several factors affect the
total storage footprint for dynamic tables specifically:

- **Time Travel and fail-safe.** Frequent refreshes increase the buildup of Time Travel data. Fail-safe provides
  additional data protection. To reduce storage costs from fail-safe, create a
  [transient](/user-guide/tables-temp-transient) dynamic table.
- **Incremental refresh metadata.** Dynamic tables using incremental refresh maintain an internal metadata column
  per row for change tracking. This adds a constant amount of storage per row, independent of the number of columns.
  On narrow tables (few columns), this overhead can be significant relative to the actual data.
- **Replication.** Dynamic tables that participate in cross-region replication incur
  [replication costs](/user-guide/account-replication-cost). For more information,
  see [Share dynamic tables with other accounts](/user-guide/dynamic-tables/sharing).
- **Suspended dynamic tables.** A suspended dynamic table doesn’t consume compute credits, but still incurs
  storage fees for its materialized data, Time Travel history, and fail-safe copies. Time Travel data from
  pre-suspension refreshes ages out normally based on DATA\_RETENTION\_TIME\_IN\_DAYS. If a dynamic table stays
  suspended longer than the base table’s DATA\_RETENTION\_TIME\_IN\_DAYS setting, the change-tracking window
  expires and the dynamic table must reinitialize when resumed. For details on retention, see
  [Understanding data retention](/user-guide/data-time-travel#label-time-travel-data-retention-period).
- **Storage lifecycle policies.** Attach a storage lifecycle policy to delete or archive expired rows asynchronously, reducing the dynamic table’s storage footprint. For more information, see [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies).

Note

[Dynamic Apache Iceberg tables](/user-guide/dynamic-tables/create-iceberg) don’t incur Snowflake storage costs.
For more information, see [Iceberg table billing](/user-guide/tables-iceberg#label-tables-iceberg-billing).

## Common cost patterns

Check whether any of these patterns apply to your pipelines.

### AUTO mode selects full refresh without a warning

AUTO resolves the refresh mode once at creation time. If it resolves to FULL when you expected INCREMENTAL, refresh
costs may increase because every refresh reprocesses the entire table instead of only changed rows. For
details on how AUTO works and how to verify the resolved mode, see
[Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).

### Short target lag amplifies Cloud Services on idle tables

Setting a short target lag (for example, 1 minute) on dynamic tables with infrequent upstream changes causes repeated
change-detection checks that produce NO\_DATA results. Each check still incurs Cloud Services credits.

Find dynamic tables with a high proportion of NO\_DATA refreshes:

Copy code

```
SELECT
    name,
    COUNT_IF(refresh_action = 'NO_DATA') AS no_data_refreshes,
    COUNT_IF(refresh_action != 'NO_DATA') AS data_refreshes,
    ROUND(no_data_refreshes / NULLIF(no_data_refreshes + data_refreshes, 0) * 100, 1)
        AS no_data_pct
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    RESULT_LIMIT => 10000
))
GROUP BY name
HAVING no_data_pct > 50
ORDER BY no_data_refreshes DESC;
```

```
+-------------------------------+-------------------+----------------+-------------+
| NAME                          | NO_DATA_REFRESHES | DATA_REFRESHES | NO_DATA_PCT |
|-------------------------------+-------------------+----------------+-------------|
| MYDB.MYSCHEMA.DT_ORDERS      |              1200 |             80 |        93.8 |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY |              950 |            120 |        88.8 |
+-------------------------------+-------------------+----------------+-------------+
```

If a dynamic table has a high NO\_DATA percentage, consider increasing its target lag or using
`TARGET_LAG = DOWNSTREAM` so it refreshes only when a downstream consumer triggers it.

### TRUNCATE followed by COPY INTO generates outsized change events

When an upstream base table is loaded using a TRUNCATE followed by COPY INTO pattern, each cycle generates DELETE
events for every existing row plus INSERT events for every loaded row. If dynamic table refreshes fail or fall behind,
these change events accumulate. A single recovery refresh then processes the entire backlog.

To avoid this pattern:

- Use INSERT-only or MERGE patterns for upstream loading instead of TRUNCATE followed by COPY INTO.
- Add a PRIMARY KEY with RELY to base tables loaded with full-replacement patterns (TRUNCATE followed by
  COPY INTO, or INSERT OVERWRITE). Snowflake compares key values before and after the load and processes
  only rows that actually changed. For details,
  see [best practice 4](/user-guide/dynamic-tables/best-practices#label-dynamic-tables-bp-primary-keys).
- Monitor for failed refreshes so backlogs don’t accumulate. For more information,
  see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).

## Monitor dynamic table costs

Use these queries to track costs across your dynamic table pipelines.

### Credit consumption by warehouse over the past 7 days

To find which warehouses are consuming the most credits, query
[WAREHOUSE\_METERING\_HISTORY](/sql-reference/account-usage/warehouse_metering_history). If you use dedicated
warehouses for dynamic tables, this query shows their total cost.

Copy code

```
SELECT
    warehouse_name,
    ROUND(SUM(credits_used), 2) AS total_credits,
    ROUND(SUM(credits_used_compute), 2) AS compute_credits,
    ROUND(SUM(credits_used_cloud_services), 2) AS cs_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC;
```

```
+----------------+---------------+-----------------+------------+
| WAREHOUSE_NAME | TOTAL_CREDITS | COMPUTE_CREDITS | CS_CREDITS |
|----------------+---------------+-----------------+------------|
| TRANSFORM_WH   |         42.50 |           40.00 |       2.50 |
| ANALYTICS_WH   |         28.30 |           27.10 |       1.20 |
+----------------+---------------+-----------------+------------+
```

### Refresh activity per dynamic table

To see how each dynamic table contributes to overall refresh volume, query DYNAMIC\_TABLE\_REFRESH\_HISTORY. Look for dynamic tables with high refresh counts or long average durations as candidates for optimization.

Copy code

```
SELECT
    name,
    refresh_action,
    COUNT(*) AS refresh_count,
    AVG(TIMESTAMPDIFF('second', refresh_start_time, refresh_end_time)) AS avg_duration_sec,
    SUM(statistics:numInsertedRows::INT) AS total_inserted,
    SUM(statistics:numDeletedRows::INT) AS total_deleted
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    RESULT_LIMIT => 10000
))
WHERE state = 'SUCCEEDED'
    AND data_timestamp >= DATEADD('day', -1, CURRENT_TIMESTAMP())
GROUP BY name, refresh_action
ORDER BY refresh_count DESC;
```

```
+-------------------------------+----------------+---------------+------------------+----------------+---------------+
| NAME                          | REFRESH_ACTION | REFRESH_COUNT | AVG_DURATION_SEC | TOTAL_INSERTED | TOTAL_DELETED |
|-------------------------------+----------------+---------------+------------------+----------------+---------------|
| MYDB.MYSCHEMA.DT_ORDERS      | INCREMENTAL    |           144 |              1.2 |          12050 |           200 |
| MYDB.MYSCHEMA.DT_ORDERS_DAILY | INCREMENTAL   |            72 |              3.8 |          48200 |          1100 |
+-------------------------------+----------------+---------------+------------------+----------------+---------------+
```

### Identify dynamic tables running full refresh unexpectedly

A REINITIALIZE action fully reprocesses the dynamic table and costs significantly more than an incremental refresh.

Copy code

```
SELECT
    name,
    refresh_action,
    COUNT(*) AS refresh_count
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    RESULT_LIMIT => 10000
))
WHERE refresh_action = 'REINITIALIZE'
    AND data_timestamp >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY name, refresh_action
ORDER BY refresh_count DESC;
```

```
+----------------------------------+----------------+---------------+
| NAME                             | REFRESH_ACTION | REFRESH_COUNT |
|----------------------------------+----------------+---------------|
| MYDB.MYSCHEMA.DT_ORDERS_DAILY   | REINITIALIZE   |            14 |
+----------------------------------+----------------+---------------+
```

If a dynamic table shows frequent REINITIALIZE actions, check for upstream DDL changes or policy changes that
trigger reinitialization. For more information, see [Modify dynamic tables](/user-guide/dynamic-tables/modify).

## What’s next

- To choose the right warehouse size and configuration, see [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).
- To reduce refresh cost through query optimization, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- To set up monitoring dashboards and alerts, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
