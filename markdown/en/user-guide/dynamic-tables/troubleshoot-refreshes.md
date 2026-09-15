# Troubleshoot dynamic table refresh issues

This page helps you diagnose and resolve dynamic table refresh problems.
For creation-time issues, see [Troubleshoot dynamic table creation issues](/user-guide/dynamic-tables/troubleshoot-creation). For permission-related failures, see [Troubleshoot dynamic table permission issues](/user-guide/dynamic-tables/troubleshoot-permissions).

Start by running the quick health check below. If your symptom is not visible there, scan the section headings to find a match. For slow refresh diagnostics, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).

Copy code

```
-- Quick health check: find dynamic tables that are failing, suspended, or lagging
SHOW DYNAMIC TABLES;

SELECT "name", "scheduling_state", "refresh_mode", "target_lag",
       DATEDIFF('minute', "data_timestamp", CURRENT_TIMESTAMP()) AS actual_lag_minutes
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
ORDER BY actual_lag_minutes DESC NULLS FIRST;
```

```
+-------------------+-------------------+--------------+------------+---------------------+
| name              | scheduling_state  | refresh_mode | target_lag | actual_lag_minutes  |
+-------------------+-------------------+--------------+------------+---------------------+
| dt_orders_daily  | SUSPENDED         | INCREMENTAL  | 30 minutes | NULL                |
| dt_orders        | RUNNING           | INCREMENTAL  | 10 minutes | 12                  |
+-------------------+-------------------+--------------+------------+---------------------+
```

You can also view refresh status in the Refresh History tab in Snowsight.

Look for rows where `scheduling_state` is not RUNNING or where `actual_lag_minutes` greatly
exceeds your target lag. If this query returns no rows, see
[Troubleshoot permission issues](/user-guide/dynamic-tables/troubleshoot-permissions#label-dynamic-tables-troubleshoot-permissions-cant-see-metadata)
to check your role’s privileges.

If you encounter an issue not listed here, contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Refresh fails with UPSTREAM\_FAILED status

When a dynamic table depends on another dynamic table that failed to refresh, the downstream table
reports UPSTREAM\_FAILED. The root cause is always upstream.

1. Find which dynamic tables show UPSTREAM\_FAILED:

   Copy code

   ```
   SELECT name, state, state_code, state_message,
          refresh_start_time
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema'
   ))
   WHERE state IN ('FAILED', 'UPSTREAM_FAILED')
   ORDER BY refresh_start_time DESC
   LIMIT 20;
   ```

   ```
   +---------------------+---------+-----------------+------------------------------------------+-------------------------+
   | NAME                | STATE   | STATE_CODE      | STATE_MESSAGE                            | REFRESH_START_TIME      |
   +---------------------+---------+-----------------+------------------------------------------+-------------------------+
   | DT_ORDERS_DAILY    | FAILED  | UPSTREAM_FAILED | Some inputs failed to refresh: [STG_O... | 2025-01-16 12:00:00.000 |
   | DT_ORDERS          | FAILED  | USER_ERROR      | SQL compilation error: invalid ident...  | 2025-01-16 11:59:45.000 |
   +---------------------+---------+-----------------+------------------------------------------+-------------------------+
   ```
2. Read the `state_message` column, which names the failing upstream table directly.
   In this example, `dt_orders` has a `USER_ERROR`, which means its own definition has a problem.
   That failure cascades to `dt_orders_daily`.
3. Alternatively, open the **Graph** view in Snowsight to visualize the pipeline.
   Navigate to **Transformation** > **Dynamic tables**, select any table in the pipeline,
   and switch to the **Graph** tab. The failing upstream table is highlighted.
4. Fix the root-cause table first. After the upstream table refreshes successfully,
   the downstream UPSTREAM\_FAILED tables recover automatically on their next scheduled refresh.

## Dynamic table is suspended

A suspended dynamic table stops refreshing entirely. No new refreshes are attempted
until you resume it.

1. Check the scheduling state and suspension reason:

   Copy code

   ```
   SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;
   ```

   ```
   +------------+-------------------+-----------+
   | name       | scheduling_state  | ...       |
   +------------+-------------------+-----------+
   | DT_ORDERS | SUSPENDED         | ...       |
   +------------+-------------------+-----------+
   ```
2. Determine why it was suspended. Query the scheduling state to see the reason code:

   Copy code

   ```
   SELECT name,
          scheduling_state:state::STRING AS state,
          scheduling_state:reason_code::STRING AS reason_code,
          scheduling_state:reason_message::STRING AS reason_message
     FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY())
     WHERE name = 'DT_ORDERS'
     ORDER BY valid_from DESC
     LIMIT 1;
   ```

   The most common causes are manual suspension (`USER_SUSPENDED`), five consecutive scheduled refresh
   failures (`SUSPENDED_DUE_TO_ERRORS`), and cascade from a suspended upstream table
   (`UPSTREAM_USER_SUSPENDED` or `UPSTREAM_SUSPENDED_DUE_TO_ERRORS`).

   For the complete list of suspension reason codes and resume cascade behavior, see
   [Manage dynamic tables](/user-guide/dynamic-tables/manage#label-dynamic-tables-manage-auto-suspend).
3. Fix the root cause (for example, correct the column name in the dynamic table’s definition), then resume:

   Copy code

   ```
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
   ```

   When you resume a dynamic table, downstream tables that were suspended as a cascade effect
   (reason `UPSTREAM_USER_SUSPENDED` or `UPSTREAM_SUSPENDED_DUE_TO_ERRORS`) also resume automatically.
   Tables you manually suspended must be resumed individually. Resuming restores schedulability
   but does not trigger an immediate refresh.

## Refresh fails with an error

For a complete list of refresh error codes with causes and resolutions, see [Error code reference for dynamic tables](/user-guide/dynamic-tables/error-codes). You can search that page by error message or error code.

If the error message includes a `query_id`, open the query profile in Snowsight to see resource usage and identify bottlenecks. See [Exploring execution times](/user-guide/performance-query-exploring).

## Refresh fails after a schema change on a base table

When a column referenced by the dynamic table’s definition is dropped or renamed in a base table,
refreshes fail. The dynamic table can’t adapt to the schema change automatically unless it uses `SELECT *` with schema evolution (see [Modify dynamic tables](/user-guide/dynamic-tables/modify)).

1. Check recent refresh failures for schema-related errors:

   Copy code

   ```
   SELECT name, state, state_message
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders',
       ERROR_ONLY => TRUE
   ))
   ORDER BY refresh_start_time DESC
   LIMIT 1;
   ```

   ```
   +------------+---------+--------------------------------------------------------------+
   | NAME       | STATE   | STATE_MESSAGE                                                |
   +------------+---------+--------------------------------------------------------------+
   | DT_ORDERS | FAILED  | SQL compilation error: invalid identifier 'ORDER_STATUS'     |
   +------------+---------+--------------------------------------------------------------+
   ```
2. Identify the schema change. Compare the dynamic table’s definition against the current base
   table schema:

   Copy code

   ```
   -- View the dynamic table's definition
   SELECT GET_DDL('DYNAMIC_TABLE', 'mydb.myschema.dt_orders');

   -- View the base table's current columns
   DESCRIBE TABLE mydb.myschema.raw_orders;
   ```

   Look for column names in the GET\_DDL output that don’t appear in the DESCRIBE output.

   ```
   -- GET_DDL shows the definition references order_status
   -- DESCRIBE TABLE shows the column was renamed to status
   +---------------+-------------------+
   | name          | type              |
   +---------------+-------------------+
   | ORDER_ID      | NUMBER(38,0)      |
   | CUSTOMER_ID   | NUMBER(38,0)      |
   | ORDER_DATE    | DATE              |
   | PRODUCT_NAME  | VARCHAR(16777216) |
   | QUANTITY       | NUMBER(38,0)      |
   | UNIT_PRICE    | NUMBER(10,2)      |
   | STATUS        | VARCHAR(16777216) |
   +---------------+-------------------+
   ```
3. Resolve the mismatch. Either restore the dropped column on the base table or recreate the
   dynamic table with an updated definition that references the correct columns.

Tip

If your dynamic table uses explicit column lists and a base table schema change causes a refresh failure,
consider switching to `SELECT *` or `SELECT * EXCLUDE (...)` for automatic schema evolution. See
[Modify dynamic tables](/user-guide/dynamic-tables/modify) for details.

## dbt or CREATE OR REPLACE breaks change tracking

When a base table is replaced with `CREATE OR REPLACE`, the new table is a different object.
The dynamic table loses its reference to the original table’s change tracking history, causing
incremental refresh to fail.

1. Check refresh history for change-tracking errors:

   Copy code

   ```
   SELECT name, state, state_message
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders',
       ERROR_ONLY => TRUE
   ))
   ORDER BY refresh_start_time DESC
   LIMIT 5;
   ```

   The specific error depends on what changed. If only change tracking was lost (same schema),
   you see:

   ```
   Change tracking is not enabled or has been missing for the time range requested on table <TABLE>.
   ```

   If the schema also changed:

   ```
   Base TABLE <TABLE> dropped, cannot read from stream on it.
   ```
2. If you use dbt or other tools that run `CREATE OR REPLACE TABLE`, use one of these
   workarounds:

   **Option A: Suspend and resume around DDL changes**

   Suspending prevents failures during the DDL window. The dynamic table still reinitializes
   after resume, but you avoid transient failures and control the timing.

   Copy code

   ```
   -- Before dbt run
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders SUSPEND;

   -- Run dbt

   -- After dbt completes
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
   ```

   **Option B: Re-enable change tracking after replacement**

   If your tooling must use `CREATE OR REPLACE`, add a post-hook to re-enable change tracking:

   Copy code

   ```
   ALTER TABLE mydb.myschema.raw_orders SET CHANGE_TRACKING = TRUE;
   ```

   Alternatively, include `CHANGE_TRACKING = TRUE` directly in the `CREATE OR REPLACE TABLE`
   statement.

   **Option C: Use `INSERT OVERWRITE` instead of `CREATE OR REPLACE`**

   `INSERT OVERWRITE` preserves the table object and its change tracking history:

   Copy code

   ```
   INSERT OVERWRITE INTO mydb.myschema.raw_orders
   SELECT * FROM mydb.myschema.raw_orders_staging;
   ```
3. After applying the workaround, resume the dynamic table if it was suspended:

   Copy code

   ```
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
   ```

## Dynamic table reinitializes unexpectedly

Reinitialization forces Snowflake to reprocess the entire dynamic table from scratch, even if it normally uses
incremental refresh. This is more expensive than a regular refresh and produces a large change set
for streams that depend on the dynamic table. Streams on the dynamic table survive reinitialization
but their next read returns the entire table as changes. Recreate the stream if you want to reset
the offset and avoid processing this large change set. See
[Streams on a dynamic table return a large change set after reinitialization](#label-dynamic-tables-troubleshoot-streams-after-reinit).

1. Confirm that a reinitialization happened by checking the `refresh_action` column:

   Copy code

   ```
   SELECT name, refresh_action, refresh_trigger, state, refresh_start_time
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders'
   ))
   ORDER BY refresh_start_time DESC
   LIMIT 5;
   ```

   ```
   +------------+----------------+-----------------+-----------+-------------------------+
   | NAME       | REFRESH_ACTION | REFRESH_TRIGGER | STATE     | REFRESH_START_TIME      |
   +------------+----------------+-----------------+-----------+-------------------------+
   | DT_ORDERS | REINITIALIZE   | CREATION        | SUCCEEDED | 2025-01-16 12:00:00.000 |
   | DT_ORDERS | INCREMENTAL    | SCHEDULED       | SUCCEEDED | 2025-01-16 11:50:00.000 |
   +------------+----------------+-----------------+-----------+-------------------------+
   ```
2. Identify the trigger. The most common causes are `CREATE OR REPLACE` on the dynamic table itself
   (appears as `refresh_trigger = CREATION` in refresh history)
   or on an upstream base table, and schema changes (dropping or renaming a column) on a base table
   that the dynamic table references.

   For the complete list of reinitialization triggers, see
   [Modify dynamic tables](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).
3. To control when reinitialization happens and avoid refresh failures during DDL changes
   (such as dbt runs), suspend the dynamic table before the DDL and resume it after. The dynamic
   table still reinitializes on its initial refresh after resume, but you avoid transient failures
   and control the timing:

   Copy code

   ```
   -- Before running DDL on base tables
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders SUSPEND;

   -- Run your DDL (dbt run, CREATE OR REPLACE, schema changes)

   -- After DDL completes
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
   ```

For more information about reinitialization, see [Reinitialization triggers](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).

## Streams on a dynamic table return a large change set after reinitialization

When a dynamic table reinitializes, all of its data is reprocessed. After a
reinitialization, the stream exposes all row-level differences between its last-read offset
and the reinitialized output. Every row in the new output appears as an INSERT, and every row
from the previous version appears as a DELETE. This can produce a very large change set.
For more details, see [Use streams on dynamic tables](/user-guide/dynamic-tables/streams-on-dts).

1. Confirm that the dynamic table reinitialized recently:

   Copy code

   ```
   SELECT name, refresh_action, refresh_trigger, refresh_start_time
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders'
   ))
   WHERE refresh_action = 'REINITIALIZE'
   ORDER BY refresh_start_time DESC
   LIMIT 1;
   ```

   ```
   +------------+----------------+-----------------+-------------------------+
   | NAME       | REFRESH_ACTION | REFRESH_TRIGGER | REFRESH_START_TIME      |
   +------------+----------------+-----------------+-------------------------+
   | DT_ORDERS | REINITIALIZE   | CREATION        | 2025-01-16 12:00:00.000 |
   +------------+----------------+-----------------+-------------------------+
   ```
2. Recreate the stream to reset the offset to the current state of the dynamic table:

   Copy code

   ```
   CREATE OR REPLACE STREAM mydb.myschema.dt_orders_stream
       ON DYNAMIC TABLE mydb.myschema.dt_orders;
   ```
3. To prevent recurrence, minimize reinitializations. See [Dynamic table reinitializes unexpectedly](#label-dynamic-tables-troubleshoot-reinitializing).
4. To reduce the volume of changes that downstream consumers must process after a reinitialization, add a RELY primary key to the dynamic table. Snowflake merges matching INSERT/DELETE pairs into UPDATEs for downstream dynamic tables and streams.

For more information about streams on dynamic tables, see
[Use streams on dynamic tables](/user-guide/dynamic-tables/streams-on-dts).

## Dynamic table refreshes as FULL when you expected INCREMENTAL

If a dynamic table was created with `REFRESH_MODE = AUTO`, the resolved mode is permanent and
can’t be changed with ALTER. See [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes) for details on
how AUTO resolves and how to verify the resolved mode.

If you need incremental refresh, fix the definition and recreate the dynamic table with
`CREATE OR REPLACE DYNAMIC TABLE ... REFRESH_MODE = INCREMENTAL` to force validation at
creation time.

## Row access policies or masking policies can block incremental refresh

Row access and masking policies on base tables can block incremental refresh depending on which functions they use. For supported combinations, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

Typical error messages:

```
Query contains context functions on which change tracking is not supported.
```

```
Incremental refresh is not supported for queries referencing tables with row access policies
that use context functions.
```

1. Identify which base tables have row access or masking policies:

   Copy code

   ```
   -- Check for row access policies
   SELECT * FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
       REF_ENTITY_NAME => 'mydb.myschema.raw_orders',
       REF_ENTITY_DOMAIN => 'TABLE'
   ));
   ```
2. Resolution options:

   **Option A: Switch to FULL refresh mode.** Full refresh evaluates the entire query from scratch
   on each refresh, so context functions in policies work correctly:

   Copy code

   ```
   CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
       TARGET_LAG = '30 minutes'
       WAREHOUSE = transform_wh
       REFRESH_MODE = FULL
   AS
       SELECT order_id, customer_id, order_date
       FROM mydb.myschema.raw_orders;
   ```

   **Option B: Apply the policy on the dynamic table instead.** Remove the policy from the base
   table and apply it to the dynamic table. Since the policy runs at query time (not refresh time),
   context functions work correctly:

   Copy code

   ```
   ALTER TABLE mydb.myschema.raw_orders
       DROP ROW ACCESS POLICY my_policy;

   ALTER DYNAMIC TABLE mydb.myschema.dt_orders
       ADD ROW ACCESS POLICY my_policy ON (customer_id);
   ```

## IS\_ROLE\_IN\_SESSION() only accepts constant arguments in incremental mode

When a dynamic table uses incremental refresh and the definition references a base table with a
row access policy that calls `IS_ROLE_IN_SESSION()`, the policy function must use only constant
string arguments. Variable or column-based arguments are not supported in incremental mode.

```
IS_ROLE_IN_SESSION() with non-constant arguments is not supported for incremental refresh.
```

1. Check the row access policy definition to see how `IS_ROLE_IN_SESSION()` is called:

   Copy code

   ```
   SELECT GET_DDL('POLICY', 'mydb.myschema.my_policy');
   ```
2. If the policy uses a column reference as the argument (for example,
   `IS_ROLE_IN_SESSION(allowed_role)`), this is not supported in incremental mode.
3. Resolution options:

   - Rewrite the policy to use constant role names:
     `IS_ROLE_IN_SESSION('ANALYST_ROLE')`.
   - Move the policy from the base table to the dynamic table, where it runs at query time
     rather than refresh time.
   - Switch the dynamic table to `REFRESH_MODE = FULL`.

## Projection policies cause unexpected refresh behavior

Projection policies on base table columns can affect dynamic table refresh behavior. If a projection policy restricts a column the definition references, the refresh either sees masked data (producing incorrect output) or fails outright if the owner role is not in the policy’s allowed list.

1. Check if any base tables have projection policies:

   Copy code

   ```
   SELECT * FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
       REF_ENTITY_NAME => 'mydb.myschema.raw_orders',
       REF_ENTITY_DOMAIN => 'TABLE'
   ))
   WHERE policy_kind = 'PROJECTION_POLICY';
   ```
2. If the dynamic table’s owner role is not in the projection policy’s allowed list, the
   refresh sees masked or restricted data. Grant the owner role the appropriate access or
   modify the projection policy:

   Copy code

   ```
   -- Option: Ensure the owner role is authorized in the projection policy
   -- Check your projection policy definition and update it to include the owner role
   ```
3. If you want the dynamic table to contain the unmasked data (for downstream consumption
   with separate access controls), ensure the owner role has full access through the
   projection policy.

## Dynamic table is not refreshing after RESUME

After you run `ALTER DYNAMIC TABLE ... RESUME`, a refresh may not be triggered
immediately. If the dynamic table exceeds its target lag, investigate the following.

1. Confirm the scheduling state changed to RUNNING:

   Copy code

   ```
   SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;
   ```

   ```
   +------------+-------------------+
   | name       | scheduling_state  |
   +------------+-------------------+
   | DT_ORDERS | RUNNING           |
   +------------+-------------------+
   ```
2. Incremental refresh relies on time-travel data. If the dynamic table was
   suspended longer than the DATA\_RETENTION\_TIME\_IN\_DAYS setting (default: 1 day for
   Standard Edition, configurable up to 90 days for Enterprise Edition and higher),
   inherited from the
   database or schema unless set explicitly, this data has expired and
   incremental refresh can’t find the historical change data. The refresh fails with:

   ```
   Time travel data is not available for table <TABLE>.
   The requested time is either beyond the allowed time travel period
   or before the object creation time.
   ```

   In this case, you must recreate the dynamic table. Use `SELECT GET_DDL('DYNAMIC_TABLE', 'mydb.myschema.dt_orders')` to
   capture the existing definition before recreation. Downstream dynamic tables will also reinitialize
   after the recreation. To recreate a dynamic table without reprocessing historical data, see [Seed a dynamic table with BACKFILL FROM](/user-guide/dynamic-tables/frozen-regions#label-dynamic-tables-frozen-backfill).
3. If the scheduling state shows RUNNING but no refreshes appear in the history, trigger a
   manual refresh to confirm the dynamic table can refresh:

   Copy code

   ```
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders REFRESH;
   ```

If the warehouse was dropped or reassigned during suspension, see the warehouse error in [Refresh fails with an error](#label-dynamic-tables-troubleshoot-failed-refreshes).

## Scheduled refreshes are being skipped

A skipped refresh means Snowflake chose not to run a scheduled refresh. The dynamic table’s data
doesn’t advance, but no error is reported.

1. Check for skipped refreshes in the refresh history:

   Copy code

   ```
   SELECT name, state, state_code, state_message, data_timestamp
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders'
   ))
   WHERE state = 'SKIPPED'
   ORDER BY refresh_start_time DESC
   LIMIT 10;
   ```

   ```
   +------------+---------+-------------------------------------+-------------------+-------------------------+
   | NAME       | STATE   | STATE_CODE                          | STATE_MESSAGE     | DATA_TIMESTAMP          |
   +------------+---------+-------------------------------------+-------------------+-------------------------+
   | DT_ORDERS | SKIPPED | NOT_EFFECTIVE_TICK_TO_REFRESH        | ...               | 2025-01-16 11:50:00.000 |
   | DT_ORDERS | SKIPPED | UPSTREAM_FAILED                     | ...               | 2025-01-16 11:40:00.000 |
   +------------+---------+-------------------------------------+-------------------+-------------------------+
   ```
2. Interpret the `state_code`:

   | State code | Meaning | Resolution |
   | --- | --- | --- |
   | UPSTREAM\_FAILED | An upstream dynamic table failed or was skipped | Fix the upstream table first |
   | NOT\_EFFECTIVE\_TICK\_TO\_REFRESH | Snowflake determined this scheduled refresh attempt was not effective (refresh duration greatly exceeds target lag) | Increase the warehouse size, optimize the definition, or increase target lag |

   Expand

   Show lessSee more

   SKIPPED with `UPSTREAM_FAILED` means a single refresh attempt is skipped because an upstream
   table failed this cycle. SUSPENDED means the table stopped refreshing entirely after repeated
   failures (five consecutive failures by default).

   If a previous refresh is still running when the next scheduled refresh attempt arrives, the new
   scheduled refresh attempt is skipped and the current refresh is allowed to complete. To reduce
   skips from overlapping refreshes, increase the warehouse size or increase the target lag.
3. If you see many consecutive skips with NOT\_EFFECTIVE\_TICK\_TO\_REFRESH, Snowflake is
   adjusting because refreshes take much longer than the target lag. For example, a dynamic table
   with a 1-minute target lag but 1-hour refresh duration causes most scheduled refresh attempts to be skipped.

   To resolve this, either increase the target lag to a realistic value or improve refresh
   performance. See [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).

Note

Manual refreshes (`ALTER DYNAMIC TABLE ... REFRESH`) are never skipped, but frequent manual
refreshes on a dynamic table with downstream consumers can prevent those downstream dynamic tables
from refreshing on schedule.

## Refreshes show cost but produce no new rows

A zero-row refresh still consumes compute if Snowflake detects upstream changes and resumes
the warehouse to evaluate them.

1. Check whether recent refreshes consumed warehouse resources:

   Copy code

   ```
   SELECT name, state,
          statistics:numInsertedRows::INT AS rows_inserted,
          statistics:numDeletedRows::INT AS rows_deleted,
          DATEDIFF('second', refresh_start_time, refresh_end_time) AS duration_sec
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders'
   ))
   ORDER BY refresh_start_time DESC
   LIMIT 10;
   ```

   ```
   +------------+-----------+---------------+--------------+--------------+
   | NAME       | STATE     | ROWS_INSERTED | ROWS_DELETED | DURATION_SEC |
   +------------+-----------+---------------+--------------+--------------+
   | DT_ORDERS | NO_DATA   | NULL          | NULL         | 0            |
   | DT_ORDERS | SUCCEEDED | 0             | 0            | 3            |
   | DT_ORDERS | SUCCEEDED | 0             | 0            | 2            |
   | DT_ORDERS | SUCCEEDED | 15            | 2            | 5            |
   +------------+-----------+---------------+--------------+--------------+
   ```
2. Understand the two types of zero-row refreshes:

   | Type | Warehouse used | Cost | Explanation |
   | --- | --- | --- | --- |
   | NO\_DATA | No | None | No changes detected in upstream objects. The warehouse stays suspended. |
   | Zero-row SUCCEEDED | Yes | Compute credits consumed | Changes were detected upstream, so the warehouse resumed to evaluate them, but the net result was zero rows applied to the dynamic table. |

   Expand

   Show lessSee more
3. If zero-row refreshes happen frequently and the cost is a concern, check whether
   upstream processes are generating changes that don’t affect the dynamic table’s output
   (for example, updating columns not referenced in the definition).

For more information, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).

## What’s next

- To troubleshoot creation-time issues, see
  [Troubleshoot dynamic table creation issues](/user-guide/dynamic-tables/troubleshoot-creation).
- To troubleshoot permission-related failures, see
  [Troubleshoot dynamic table permission issues](/user-guide/dynamic-tables/troubleshoot-permissions).
- To investigate slow refreshes or optimize refresh performance, see
  [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- To set up proactive monitoring and alerts for dynamic table refresh failures, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To understand the difference between INCREMENTAL, FULL, and AUTO refresh modes, see
  [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To query an event table for dynamic table failures across a database:

  Copy code

  ```
  SELECT timestamp,
         resource_attributes:"snow.executable.name"::VARCHAR AS dt_name,
         resource_attributes:"snow.query.id"::VARCHAR AS query_id,
         value:message::VARCHAR AS error
  FROM my_event_table
  WHERE resource_attributes:"snow.executable.type" = 'DYNAMIC_TABLE'
    AND resource_attributes:"snow.database.name" = 'MY_DB'
    AND value:state = 'FAILED'
  ORDER BY timestamp DESC;
  ```

  ```
  +-------------------------+-------------------+--------------+----------------------------------------------+
  | TIMESTAMP               | DT_NAME           | QUERY_ID     | ERROR                                        |
  +-------------------------+-------------------+--------------+----------------------------------------------+
  | 2025-01-16 12:00:00.000 | DT_ORDERS        | 01b7e3f2-... | SQL compilation error: invalid identifier ... |
  +-------------------------+-------------------+--------------+----------------------------------------------+
  ```

  For more information about setting up event tables for dynamic table monitoring, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- If you encounter an issue not covered here, contact
  [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
