# Error code reference for dynamic tables

When a dynamic table refresh fails, Snowflake records an error code and message in the refresh history. Use this page to look up the error, understand the cause, and resolve it.

Note

This page lists common error codes that dynamic table users encounter. It is not a complete list. If you encounter an error code not listed here, check the `state_message` column for guidance.

To find the error code for a failed refresh, run:

Copy code

```
SELECT name,
       state,
       state_code,
       state_message,
       query_id
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'mydb.myschema.dt_orders'
))
WHERE state = 'FAILED'
ORDER BY data_timestamp DESC
LIMIT 10;
```

```
+----------------------------+---------+------------+--------------------------------------------------+--------------------------------------+
| NAME                       | STATE   | STATE_CODE | STATE_MESSAGE                                    | QUERY_ID                             |
+----------------------------+---------+------------+--------------------------------------------------+--------------------------------------+
| MY_DATABASE...DT_ORDERS    | FAILED  | 091930     | Change tracking is not enabled or has been ...   | 01b23c4d-0501-a2b3-0000-00012345abcd |
+----------------------------+---------+------------+--------------------------------------------------+--------------------------------------+
```

The `state_code` column contains the numeric error code. The `state_message` column contains the full error message. Use the `query_id` to inspect the failed statement in the query history.

The messages listed below are representative. Your actual error message may include additional details such as object names, timestamps, or incident IDs.

Errors fall into three categories:

- **Configuration errors** are preventable. They result from missing prerequisites such as change tracking, warehouses, or privileges.
- **Operational errors** are recoverable. They result from upstream changes, timeouts, or schema evolution that you can fix without Snowflake support.
- **Internal errors** are not user-actionable. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and include the `query_id` from the refresh history.

Note

If a dynamic table fails to refresh five consecutive times, Snowflake [automatically suspends](/user-guide/dynamic-tables/manage#label-dynamic-tables-manage-auto-suspend) it. After you fix the underlying issue, resume the dynamic table with `ALTER DYNAMIC TABLE <name> RESUME`.

## Configuration errors (preventable)

These errors indicate that a required setting, object, or privilege is missing. Fix the configuration to resolve the error.

### Change tracking is not enabled (091930)

**Message:** Change tracking is not enabled or has been missing for the time range requested.

**Cause:** A base table referenced by the dynamic table does not have change tracking enabled, or change tracking history was lost.

**Resolution:** Enable change tracking on the affected base table with `ALTER TABLE ... SET CHANGE_TRACKING = TRUE`. If the error persists, recreate the dynamic table. For step-by-step diagnosis, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).

### Duplicate dynamic table in refresh list (002008)

**Message:** `Duplicate Dynamic Table: <name>`

**Cause:** The same dynamic table appears more than once in the list of tables passed to `ALTER DYNAMIC TABLE ... REFRESH`. Duplicate detection matches by table identity, so short names, quoted names, and fully qualified names that resolve to the same table are all treated as the same table.

**Resolution:** Remove duplicate entries from the list. Verify that each name resolves to a distinct dynamic table.

### Warehouse is missing (002725)

**Message:** Dynamic table could not be refreshed because warehouse is missing.

**Cause:** The warehouse assigned to the dynamic table was dropped, renamed, or the owner role lost USAGE privilege on it.

**Resolution:** Verify that the warehouse exists with `SHOW WAREHOUSES LIKE '<name>'` and check privileges with `SHOW GRANTS ON WAREHOUSE <name>`.

If the warehouse was dropped, reassign a warehouse with `ALTER DYNAMIC TABLE <name> SET WAREHOUSE = <warehouse_name>`.

### Data dependent function (002798)

**Message:** `Dynamic table contains a data dependent '<function_name>' function.`

**Cause:** A masking or row-access policy on a base table passes a column value to a context function such as `IS_ROLE_IN_SESSION(column_name)`, and the dynamic table uses `REFRESH_MODE = INCREMENTAL`. Policies with constant arguments are compatible with incremental refresh and do not trigger this error.

**Resolution:** Use `REFRESH_MODE = AUTO` to let Snowflake resolve to FULL refresh gracefully, or rewrite the policy to use constant arguments instead of column values. For more information, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).

### Object does not exist or not authorized (002037)

**Message:** Object does not exist or not authorized.

**Cause:** A table, view, or function referenced in the dynamic table’s definition does not exist, or the dynamic table’s owner role does not have the required privileges on it.

**Resolution:** Verify that all referenced objects exist and the owner role has SELECT privilege. Check the full `state_message` in the refresh history for the name of the missing object, then verify the object and its grants:

Copy code

```
SHOW GRANTS TO ROLE myrole;
```

For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

### Unknown function errors

**Message:** `Unknown function <FUNCTION_NAME>.`

**Cause:** The dynamic table’s owner role lost privileges on a user-defined function (UDF) or external function referenced in the definition. Refreshes execute as the owner role, so if USAGE on the function is revoked or the function is dropped, the refresh fails with this error.

**Resolution:** Grant USAGE on the function back to the owner role:

Copy code

```
GRANT USAGE ON FUNCTION mydb.myschema.my_udf(VARCHAR)
  TO ROLE dt_owner_role;
```

If the function was dropped, recreate it or update the dynamic table definition to remove the reference. Verify which functions the dynamic table references by inspecting its definition:

Copy code

```
SELECT GET_DDL('DYNAMIC_TABLE', 'mydb.myschema.dt_orders');
```

For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

### Security policy not compatible with incremental refresh (002744)

**Message:** Dynamic table must use full refresh because a security policy on a base table is not compatible with incremental refresh.

**Cause:** A row access policy or masking policy on a base table uses constructs that incremental refresh can’t track, forcing the dynamic table to use full refresh.

**Resolution:** Recreate the dynamic table with `REFRESH_MODE = FULL`:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
  ...
  REFRESH_MODE = FULL
AS
  SELECT ...;
```

Alternatively, remove or modify the security policy on the base table so it no longer uses incompatible constructs. REFRESH\_MODE can’t be changed after creation: to change it, recreate the dynamic table with CREATE OR REPLACE DYNAMIC TABLE. For more information, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).

### Insufficient OPERATE privilege for manual refresh (002756)

**Message:** Insufficient privileges to operate on dynamic table. OPERATE privilege is required for manual refresh.

**Cause:** The role running `ALTER DYNAMIC TABLE ... REFRESH` is missing the OPERATE privilege somewhere in the refresh pipeline. Only the owner role or a role with an explicit OPERATE grant can trigger a manual refresh.

- Single-table refresh: the role calling `ALTER DYNAMIC TABLE <name> REFRESH` does not have OPERATE on the dynamic table or on an upstream dynamic table.
- Multi-table refresh: the role has OPERATE on the listed dynamic tables but is missing OPERATE on one or more upstream dynamic tables in the refresh pipeline.

Missing OPERATE on a listed dynamic table itself raises error 002037 instead.

**Resolution:** Grant the OPERATE privilege to the role that needs to run manual refreshes:

Copy code

```
GRANT OPERATE ON DYNAMIC TABLE mydb.myschema.dt_orders
  TO ROLE pipeline_admin_role;
```

OWNERSHIP includes all capabilities of OPERATE. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

### Insufficient privileges for initial refresh (002757)

**Message:** Insufficient privileges to operate on dynamic table. OPERATE privilege is required for initial refresh.

**Cause:** The role that created the dynamic table does not have the OPERATE privilege on one or more upstream dynamic tables in the pipeline. During `INITIALIZE = ON_CREATE`, Snowflake checks that the creating role can operate on all upstream dynamic tables that need to be refreshed.

**Resolution:** Grant OPERATE on each upstream dynamic table to the role that will execute the CREATE DYNAMIC TABLE statement. After creation, background refreshes use the owner role and do not require OPERATE on upstream tables:

Copy code

```
GRANT OPERATE ON DYNAMIC TABLE mydb.myschema.dt_upstream
  TO ROLE transform_role;
```

Alternatively, create the dynamic table with `INITIALIZE = ON_SCHEDULE` to skip the immediate initial refresh. The background refresh process uses the owner role, which implicitly has OPERATE. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

### Owner role does not exist (002773)

**Message:** Owner role of the dynamic table does not exist.

**Cause:** The role that owns the dynamic table was dropped or no longer exists. Snowflake uses the owner role to run background refreshes, so when the role is missing, no refresh can execute.

**Resolution:** Transfer ownership to an existing role:

Copy code

```
GRANT OWNERSHIP ON DYNAMIC TABLE mydb.myschema.dt_orders TO ROLE transform_role COPY CURRENT GRANTS;
```

If the role was dropped accidentally, recreate it and re-grant the required privileges. Verify the current owner with:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;
```

The `owner` column shows which role currently owns the dynamic table. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

## Operational errors (recoverable)

These errors result from changes in your environment, such as dropped objects or schema evolution. They require you to take action, but do not need Snowflake support.

### Non-deterministic function not supported (091912)

**Message:** Query contains a non-deterministic function that change tracking does not support.

**Cause:** The dynamic table’s definition uses a non-deterministic function in a position where incremental refresh can’t track changes. Timestamp functions (CURRENT\_TIMESTAMP, CURRENT\_DATE, CURRENT\_TIME) are supported in WHERE, HAVING, and QUALIFY clauses. This error occurs when a non-deterministic function like RANDOM() or a session-context function (CURRENT\_USER, CURRENT\_ROLE) appears in the SELECT list or another unsupported position.

**Resolution:** Move the non-deterministic function to a WHERE, HAVING, or QUALIFY clause (supported for timestamp functions), remove it from the definition, or recreate the dynamic table with `REFRESH_MODE = FULL`. For example, `CURRENT_TIMESTAMP()` in the SELECT list forces full refresh:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
  ...
  REFRESH_MODE = FULL
AS
  SELECT order_id, customer_id, CURRENT_TIMESTAMP() AS refreshed_at
  FROM mydb.myschema.raw_orders;
```

If you need a timestamp that records when each row was last refreshed, use `METADATA$ROW_LAST_COMMIT_TIME` instead of `CURRENT_TIMESTAMP()`. This built-in column provides the actual commit time of each row and is compatible with incremental refresh.

For more information, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

### SQL compilation errors

**Message:** `SQL compilation error: invalid identifier '<COLUMN>'.`

**Cause:** A column referenced in the dynamic table’s definition was dropped or renamed in a base table. The dynamic table’s SQL can no longer compile because the identifier no longer exists.

**Resolution:** Identify the missing column by comparing the dynamic table definition against the current base table schema:

Copy code

```
-- View the dynamic table's definition
SELECT GET_DDL('DYNAMIC_TABLE', 'mydb.myschema.dt_orders');

-- View the base table's current columns
DESCRIBE TABLE mydb.myschema.raw_orders;
```

Then either restore the column on the base table or recreate the dynamic table with an updated definition that references the correct column names:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
  ...
AS
  SELECT ...;
```

Tip

If base table schema changes are frequent, consider using `SELECT *` or `SELECT * EXCLUDE (...)` for automatic schema evolution. See [Modify dynamic tables](/user-guide/dynamic-tables/modify).

### Dynamic table is not initialized (002741)

**Message:** Dynamic table is not initialized.

**Cause:** The dynamic table’s initial refresh has not completed. This can happen when the initial refresh fails (for example, due to a privilege issue or query error) or when the dynamic table was recently created and has not been scheduled yet.

**Resolution:** Check the refresh history for the initial refresh failure:

Copy code

```
SELECT state, state_code, state_message
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'mydb.myschema.dt_orders'
))
ORDER BY data_timestamp ASC
LIMIT 5;
```

Fix the root cause (missing privilege, invalid query, warehouse issue), then trigger a manual refresh:

Copy code

```
ALTER DYNAMIC TABLE mydb.myschema.dt_orders REFRESH;
```

### Manual refresh not supported in multi-statement transaction (002743)

**Message:** Manual refresh of a dynamic table is not supported inside a multi-statement transaction.

**Cause:** `ALTER DYNAMIC TABLE ... REFRESH` was executed inside a multi-statement transaction (`BEGIN` / `COMMIT` block). Manual refresh isn’t supported inside an explicit transaction.

**Resolution:** Run the manual refresh statement outside a multi-statement transaction.

Note

If `TRANSACTION_ABORT_ON_ERROR` is set to `TRUE`, the transaction is aborted when this error is raised.

### Error in secure object (002742)

**Message:** Failed to refresh dynamic table. Error in secure object.

**Cause:** The dynamic table’s definition references a secure view or secure function that returned an error during refresh. This commonly occurs after the secure object itself is modified in a way that breaks the dynamic table’s query.

**Resolution:** Verify the secure object’s SQL is valid and that the dynamic table’s owner role has the required privileges:

Copy code

```
SHOW GRANTS ON VIEW mydb.myschema.my_secure_view;
DESC VIEW mydb.myschema.my_secure_view;
```

If the secure object’s schema changed, recreate the dynamic table with an updated definition.

### Refresh was canceled or timed out (002724)

**Message:** Refresh was canceled or timed out.

**Cause:** The refresh query exceeded the statement timeout or was canceled. This occurs when the warehouse is too small for the workload, the definition is too complex, or resource contention caused the query to queue.

**Resolution:** Consider one or more of these approaches:

1. Increase the warehouse size. See [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).
2. Simplify the definition by breaking it into multiple dynamic tables.
3. Increase the STATEMENT\_TIMEOUT\_IN\_SECONDS parameter on the warehouse.

The effective timeout is the most restrictive value set across the account, warehouse, and session levels. Check all three if increasing the warehouse-level setting does not resolve the issue.

### Statement reached its statement or lock timeout (000627)

**Message:** Statement reached its statement or lock timeout.

**Cause:** The refresh statement could not acquire a lock on the dynamic table or a referenced object within the lock timeout period. This occurs during periods of high concurrency or when a long-running transaction holds a conflicting lock.

**Resolution:** Check for long-running transactions that may hold locks:

Copy code

```
SHOW LOCKS IN ACCOUNT;
SHOW TRANSACTIONS IN ACCOUNT;
```

If lock contention is recurring, consider increasing the LOCK\_TIMEOUT parameter or staggering refresh schedules across the pipeline.

### SQL execution canceled (000603)

**Message:** SQL execution canceled.

**Cause:** The refresh query was canceled before it completed. This occurs when the warehouse auto-suspends while a refresh is in progress, an administrator manually cancels the refresh query, or the system cancels the query due to resource pressure.

**Resolution:** Check the warehouse AUTO\_SUSPEND setting. If the warehouse suspends during refresh windows, increase AUTO\_SUSPEND or set it to 0 (never auto-suspend) while refreshes are running:

Copy code

```
ALTER WAREHOUSE transform_wh SET AUTO_SUSPEND = 600;
```

If the query was manually canceled, verify that no automated process or user is canceling active refresh queries.

### Some inputs failed to refresh (002753)

**Message:** `Some inputs failed to refresh: [<TABLE>].` (background refresh) or `Manual refresh failed because an upstream dynamic table failed to refresh.` (manual refresh)

**Cause:** One or more upstream dynamic tables in the pipeline failed to refresh. During a background (scheduled) refresh, Snowflake reports this as “Some inputs failed to refresh” with the names of the failing upstream tables. During a manual refresh (`ALTER DYNAMIC TABLE ... REFRESH`), the message is more explicit. In both cases, the upstream failure must be resolved before the downstream refresh can succeed.

**Resolution:** Identify which upstream dynamic table failed by checking the refresh history for each table in the pipeline:

Copy code

```
SELECT name, state, state_code, state_message
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY())
WHERE state = 'FAILED'
ORDER BY data_timestamp DESC
LIMIT 20;
```

Fix the upstream failure first, then retry the manual refresh on the downstream dynamic table:

Copy code

```
ALTER DYNAMIC TABLE mydb.myschema.dt_orders REFRESH;
```

For more information about diagnosing upstream failures, see [Refresh fails with UPSTREAM\_FAILED status](/user-guide/dynamic-tables/troubleshoot-refreshes#label-dynamic-tables-troubleshoot-upstream-failed).

### Dynamic table can no longer be refreshed incrementally (002766)

**Message:** Dynamic table can no longer be refreshed incrementally.

**Cause:** A structural change in the pipeline, such as adding a LIMIT clause to a view or altering a column in a referenced object, means the dynamic table’s definition can no longer be tracked incrementally. Snowflake detected that incremental change tracking is no longer valid for this definition.

**Resolution:** Recreate the dynamic table with CREATE OR REPLACE DYNAMIC TABLE. If the definition no longer supports incremental refresh, set `REFRESH_MODE = FULL`:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
  ...
  REFRESH_MODE = FULL
AS
  SELECT ...;
```

To keep incremental refresh, undo the structural change that broke compatibility (for example, remove a LIMIT clause from a referenced view). For details on which query patterns support incremental refresh, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

### Upstream table is outside the data retention period (002841)

**Message:** Upstream table is outside the data retention period. Change tracking data is no longer available.

**Cause:** An upstream table that the dynamic table depends on fell outside its DATA\_RETENTION\_TIME\_IN\_DAYS window. The change tracking data needed for incremental refresh is no longer available, so the dynamic table can’t refresh.

**Resolution:** The dynamic table must reinitialize. Recreate it with CREATE OR REPLACE DYNAMIC TABLE to reset the change tracking baseline:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
  ...
AS
  SELECT ...;
```

To prevent this issue in the future:

1. Monitor suspension duration. If a dynamic table is suspended, resume it before the upstream table’s retention period expires.
2. Increase the upstream table’s retention period if needed: `ALTER TABLE upstream_table SET DATA_RETENTION_TIME_IN_DAYS = 14`.
3. Set up alerts on the [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) function to detect suspensions early.

## Internal errors (contact support)

These errors indicate an internal issue that you can’t resolve on your own. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and provide the `query_id` and error details from the refresh history.

### Internal Dynamic Table refresh error (002781)

**Message:** Internal Dynamic Table refresh error. Invalid DT\_ROW\_ID.

**Cause:** An internal data integrity check failed during incremental refresh. Snowflake detected rows in the change delta that do not match existing rows in the dynamic table.

**Resolution:** This is an internal data integrity error. If it occurs, recreate the dynamic table with CREATE OR REPLACE. If the error persists, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) with the `query_id` from the refresh history.

### SQL execution internal error (300002, 300010)

**Message:** SQL execution internal error: Processing aborted due to error.

**Cause:** An internal execution error occurred during refresh processing. The error message includes a numeric error code (such as 300002 or 300010) and an incident ID. Other codes in the 300xxx range may also appear.

**Resolution:** This is not user-actionable. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and include the full error message with the error code and incident ID.

### ExecRsoProjection: Unresolved connector (370001)

**Message:** ExecRsoProjection: Unresolved connector.

**Cause:** An internal SQL compiler error occurred while processing the dynamic table’s definition.

**Resolution:** This is not user-actionable. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and include the `query_id`. As a temporary workaround, simplifying the definition (for example, breaking a complex JOIN + GROUP BY into two dynamic tables) may avoid the issue.

## When to contact Snowflake support

Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) when:

- The error is listed in the [Internal errors](#label-dynamic-tables-error-codes-internal) section above.
- The error message contains “Processing aborted due to error” with an incident number.
- The error message contains “Internal Error” or “incident.”
- Error 002781 (invalid DT\_ROW\_ID) occurs repeatedly.
- You have followed the resolution steps for a configuration or operational error and the issue persists.

When you open a support case, include:

1. The full error message from the refresh history.
2. The `query_id` from the `state_message` or refresh history output.
3. The dynamic table name and database/schema.
4. The output of `SHOW DYNAMIC TABLES LIKE '<table_name>'`.

## What’s next

- [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes)
- [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring)
- [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes)
- [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table)
