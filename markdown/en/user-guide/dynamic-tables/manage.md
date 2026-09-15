# Manage dynamic tables

This page covers the lifecycle operations for dynamic tables after creation: suspending, resuming, altering
the warehouse and target lag, and dropping or restoring.

For the full syntax reference, see [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table).

- Suspend, resume, and alter (warehouse, target lag, `SCHEDULER`) require the OWNERSHIP or OPERATE privilege.
- Drop and undrop require the OWNERSHIP privilege.

For the full privilege reference, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

## Suspend a dynamic table

Suspending a dynamic table stops all scheduled refreshes. The table data stays intact and queryable, but
no new scheduled refreshes run until you resume it. You can still trigger a manual refresh on a suspended
dynamic table using ALTER DYNAMIC TABLE … REFRESH.

If you suspend a dynamic table longer than the base tables’ DATA\_RETENTION\_TIME\_IN\_DAYS, the change-tracking window expires and the table can’t resume normally. See [Resumption after a long suspension](#label-dynamic-tables-manage-long-suspension) below. Suspended dynamic tables incur only storage costs,
not refresh compute costs.

You can suspend a dynamic table to reduce compute spend during maintenance windows, to troubleshoot
refresh failures, or to suspend a pipeline you don’t need right now.

Suspending a dynamic table requires the OWNERSHIP or OPERATE privilege.

Important

Suspending a dynamic table also suspends all downstream dynamic tables that depend on it. Those downstream
tables can’t be resumed individually until the upstream table is resumed first.

SQLSnowsight

To suspend a dynamic table, run `ALTER DYNAMIC TABLE <name> SUSPEND`.

Verify the scheduling state:

Copy code

```
SELECT name,
       scheduling_state:state::STRING AS state,
       scheduling_state:reason_code::STRING AS reason_code
  FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY())
  WHERE name = 'DT_ORDERS'
  ORDER BY valid_from DESC
  LIMIT 1;
```

```
+------------+-----------+----------------+
| NAME       | STATE     | REASON_CODE    |
|------------+-----------+----------------|
| DT_ORDERS | SUSPENDED | USER_SUSPENDED |
+------------+-----------+----------------+
```

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Transformation** » **Dynamic tables**.
3. Find your dynamic table in the list and then select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Suspend**.
4. In the popup, confirm that you want to suspend your dynamic table.

## Automatic suspension after 5 consecutive errors

Snowflake automatically suspends a dynamic table after five consecutive scheduled refresh
failures. This prevents a failing table from consuming warehouse resources indefinitely.

Key rules for the error counter:

- Only **scheduled** refresh failures count. Errors from manually triggered refreshes (ALTER DYNAMIC TABLE … REFRESH)
  don’t increment the counter.
- A **successful** refresh (scheduled or manual) resets the counter to zero.
- After auto-suspension, downstream dynamic tables are also suspended with the reason
  `UPSTREAM_SUSPENDED_DUE_TO_ERRORS`.
- Dynamic tables don’t auto-resume after the underlying error is fixed. You must explicitly run
  ALTER DYNAMIC TABLE … RESUME.

To check whether a dynamic table was auto-suspended, query the scheduling state:

Copy code

```
SELECT name,
       scheduling_state:state::STRING AS state,
       scheduling_state:reason_code::STRING AS reason_code,
       scheduling_state:reason_message::STRING AS reason_message,
       scheduling_state:suspended_on::TIMESTAMP AS suspended_on
  FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY())
  WHERE name = 'DT_ORDERS'
  ORDER BY valid_from DESC
  LIMIT 1;
```

```
+------------+-----------+---------------------------+---------------------------------------------------+----------------------------------+
| NAME       | STATE     | REASON_CODE               | REASON_MESSAGE                                    | SUSPENDED_ON                     |
|------------+-----------+---------------------------+---------------------------------------------------+----------------------------------|
| DT_ORDERS | SUSPENDED | SUSPENDED_DUE_TO_ERRORS   | The dynamic table was suspended due to 5 consecutive refresh | 2025-01-16 08:27:29.142 -0700   |
|            |           |                           | errors.                                           |                                  |
+------------+-----------+---------------------------+---------------------------------------------------+----------------------------------+
```

Note

SHOW DYNAMIC TABLES reports the active scheduling state as `RUNNING`, which corresponds to `ACTIVE` in
DYNAMIC\_TABLE\_GRAPH\_HISTORY. Both indicate the same operational state.

### Suspension reason codes

The `reason_code` field in the `SCHEDULING_STATE` column indicates why a dynamic table is suspended:

| Reason code | Description |
| --- | --- |
| `USER_SUSPENDED` | A user ran ALTER DYNAMIC TABLE … SUSPEND. |
| `UPSTREAM_USER_SUSPENDED` | An upstream dynamic table was suspended by a user, which cascaded. |
| `SUSPENDED_DUE_TO_ERRORS` | Five consecutive scheduled refresh errors triggered auto-suspension. |
| `UPSTREAM_SUSPENDED_DUE_TO_ERRORS` | An upstream dynamic table was auto-suspended, which cascaded. |

Expand

Show lessSee more

## Resume a dynamic table

Resuming a dynamic table restarts its refresh schedule. Snowflake picks up from where it left off,
processing any data changes that accumulated during suspension.

Resuming requires the OWNERSHIP or OPERATE privilege.

SQLSnowsight

To resume a dynamic table, run `ALTER DYNAMIC TABLE <name> RESUME`.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Transformation** » **Dynamic tables**.
3. Find your dynamic table in the list and then select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Resume**.
4. In the popup, confirm that you want to resume your dynamic table.

### Resume cascade behavior

When you resume a dynamic table, downstream tables that were suspended as a cascade effect
(reason code `UPSTREAM_USER_SUSPENDED` or `UPSTREAM_SUSPENDED_DUE_TO_ERRORS`) also resume
automatically. Downstream tables that were directly suspended by a user (reason code
`USER_SUSPENDED`) don’t auto-resume. You must resume those individually.

### Resumption after a long suspension

If a dynamic table with incremental refresh was suspended longer than the Time Travel retention period
of its base tables, the change tracking data it needs is no longer available. On resume, the next
refresh fails because an incremental refresh can’t be performed without that data.

To check your risk, compare how long the table has been suspended against the base table’s
DATA\_RETENTION\_TIME\_IN\_DAYS setting (default: 1 day).

Warning

If the change tracking data has expired, the only recovery is to drop and recreate the dynamic table.
Before leaving a dynamic table suspended for extended periods, verify the base table’s
DATA\_RETENTION\_TIME\_IN\_DAYS setting.

## SCHEDULER = DISABLE vs. SUSPEND

Both SUSPEND and SCHEDULER = DISABLE stop refreshes, but they serve different purposes.
Both require the OWNERSHIP or OPERATE privilege.

| Operation | Behavior | Use when |
| --- | --- | --- |
| `ALTER DYNAMIC TABLE ... SUSPEND` | Suspends scheduling. Preserves all configuration (target lag, warehouse). Resume restarts refreshes. Manual refreshes still cascade to upstream and downstream tables normally. | You need a **temporary** stop, such as during maintenance or troubleshooting. |
| `ALTER DYNAMIC TABLE ... SET SCHEDULER = DISABLE` | Removes the table from scheduling entirely. TARGET\_LAG is reported as NULL; you must set a new TARGET\_LAG value to re-enable scheduling. Manual refreshes don’t cascade to upstream or downstream tables, creating an isolation boundary for external orchestrators like dbt. | You want to **permanently** detach from scheduling (static snapshot or external orchestrator). |

Expand

Show lessSee more

To re-enable scheduling after SCHEDULER = DISABLE, set a new TARGET\_LAG. To disable scheduling entirely,
run `ALTER DYNAMIC TABLE <name> SET SCHEDULER = DISABLE`. To re-enable it,
run `ALTER DYNAMIC TABLE <name> SET TARGET_LAG = '<interval>'`.

## Refresh multiple dynamic tables in one statement

To refresh multiple dynamic tables at a single point in time, list them after
`ALTER DYNAMIC TABLE`, separated by commas:

Copy code

```
ALTER DYNAMIC TABLE dt_orders, dt_orders_daily REFRESH;
```

Snowflake merges the upstream dependencies of every listed dynamic table into one pipeline and refreshes
them all at the same data timestamp. If two listed dynamic tables share an upstream, that upstream
refreshes exactly once. Each dynamic table refreshes on its own configured warehouse.

You need the OPERATE privilege on every listed dynamic table and on any upstream dynamic tables
that will refresh. See [REFRESH [ COPY SESSION ]](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-refresh)
for the full rule.

To see the full set of dynamic tables that refreshed as part of the statement, including cascaded
upstreams, query the refresh history filtered on `refresh_trigger = 'MANUAL'` and matching
`data_timestamp`. See
[View per-refresh history](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitor-refresh-history).

With `IF EXISTS`, Snowflake silently skips names in the list that don’t resolve to an existing
dynamic table; the statement succeeds for the remaining dynamic tables.

Note

Listing multiple dynamic tables refreshes each listed dynamic table regardless of its `SCHEDULER`
setting, so `SCHEDULER = DISABLE` doesn’t remove a listed dynamic table from the refresh set.

### Partial failures

Multi-table manual refresh isn’t atomic. If any listed dynamic table ends in a `FAILED`,
`UPSTREAM_FAILED`, or `CANCELLED` refresh status, the statement returns an error, but any dynamic
tables that already refreshed successfully remain refreshed.

Note

Snowflake records refresh history rows for both successful and failed dynamic tables; nothing is
rolled back.

To identify which dynamic tables succeeded or failed in a specific multi-table refresh, query the
refresh history for rows that share the same `data_timestamp`:

Copy code

```
-- Replace with the data_timestamp printed by the failed ALTER DYNAMIC TABLE ... REFRESH statement.
SET failed_ts = '2026-07-22 10:15:00.000';

SELECT name, state, state_message
  FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY())
  WHERE refresh_trigger = 'MANUAL'
    AND data_timestamp = $failed_ts
  ORDER BY name;
```

To retry, re-run the statement and list only the dynamic tables you want to refresh again. You
can’t wrap the statement in an explicit transaction (using `BEGIN` … `COMMIT`) to make the refresh
atomic; manual refresh isn’t supported inside a multi-statement transaction.

For the full list of restrictions, see
[Restrictions](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-refresh-multi-restrictions).
For error codes with causes and resolutions, see [Error code reference for dynamic tables](/user-guide/dynamic-tables/error-codes).

## Alter the warehouse or target lag

Use ALTER DYNAMIC TABLE to change the warehouse or target lag without recreating the table.
Changing these properties doesn’t trigger a reinitialization.

### Change the warehouse

To switch to a different warehouse for cost efficiency or to handle heavier workloads,
run `ALTER DYNAMIC TABLE <name> SET WAREHOUSE = <warehouse_name>`.

### Change the target lag

Adjust the target lag to balance data freshness against compute cost.
Run `ALTER DYNAMIC TABLE <name> SET TARGET_LAG = '<interval>'` to set a specific interval.
For intermediate pipeline tables that should refresh only when downstream tables need them,
use `ALTER DYNAMIC TABLE <name> SET TARGET_LAG = DOWNSTREAM`.

For guidance on choosing the right target lag, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).

## Drop a dynamic table

Dropping a dynamic table removes it from your environment and stops all associated refreshes. Drop
unused dynamic tables to reduce storage costs and clean up your pipeline.

Dropping a dynamic table requires the OWNERSHIP privilege.

Important

Downstream dynamic tables that reference a dropped table will fail on their next refresh. Before
dropping, check for downstream dependencies using
[DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history).

SQLSnowsight

To drop a dynamic table, run `DROP DYNAMIC TABLE <name>`. To avoid errors when the table might
not exist, use `DROP DYNAMIC TABLE IF EXISTS <name>`.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Transformation** » **Dynamic tables**.
3. Find your dynamic table in the list and then select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Drop**.
4. In the popup, confirm that you want to drop the dynamic table.

## Restore a dropped dynamic table

Use UNDROP DYNAMIC TABLE to restore a dropped dynamic table and its data. Undrop is available only within
the Time Travel retention period, which defaults to 24 hours. To change the retention period, set
DATA\_RETENTION\_TIME\_IN\_DAYS on the table before dropping it.

Restoring a dynamic table requires the OWNERSHIP privilege. To restore it,
run `UNDROP DYNAMIC TABLE <name>`.

If a new dynamic table with the same name was created after the original was dropped, or if the table
has already been restored, UNDROP fails:

Copy code

```
UNDROP DYNAMIC TABLE dt_orders;
```

```
Dynamic table 'DT_ORDERS' already exists.
```

After restoring, verify the scheduling state with `SHOW DYNAMIC TABLES LIKE '<name>'` and resume if needed
with `ALTER DYNAMIC TABLE <name> RESUME`.

## What’s next

- To monitor refresh history and scheduling state, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To troubleshoot refresh failures or suspension issues, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- To change the refresh mode or definition query, see [Modify dynamic tables](/user-guide/dynamic-tables/modify).
- To understand cost implications of refresh operations, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
