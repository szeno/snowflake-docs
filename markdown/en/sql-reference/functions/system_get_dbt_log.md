Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_DBT\_LOG

Returns logs for the specified run for a dbt Projects on Snowflake.

Use this function with the [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) function to access dbt artifacts and logs programmatically.

## Syntax

Copy code

```
SYSTEM$GET_DBT_LOG ( '<query_id>' [ , <max_num_lines> ] )
```

## Arguments

`query_id`
:   Query ID of the run that you want logs for.

`max_num_lines`
:   Optional. Maximum number of lines to return from the end of the `dbt.log` file. Defaults to `1000`.

    The combined size of the returned lines is capped at approximately 10 MB. If the lines you
    request exceed this limit, the function drops the oldest lines from the start of the result
    until it fits, so the output always reflects the most recent lines in the log.

## Returns

The function returns up to `max_num_lines` lines from the end of the `dbt.log` file (1,000 lines by default). For full logs, download the archive ZIP file.

For more information and examples, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

## Access control requirements

This function can only be used with dbt project objects, not Workspaces, when you have one of the following privileges:

- OWNERSHIP, USAGE, or MONITOR on the dbt project object

For details about these privileges, see [dbt project object privileges](/user-guide/security-access-control-privileges#label-access-control-privs-dbt).

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This system function works only on dbt project objects and isn’t available for Workspaces.
- Query IDs generated from CREATE DBT PROJECT or ALTER DBT PROJECT … DEPLOY aren’t supported for this system function.
- Direct querying of file content (for example, [Query examples](/user-guide/querying-stage#label-querying-stage-query-examples)) isn’t supported.
- If `query_id` is NULL or not a dbt execution, you’ll get an error.
- dbt project results are available for up to 14 days.
- Logs might be unavailable if a run times out, is canceled, or fails before files are uploaded. In such cases, runs appear as `UNHANDLED ERROR` in dbt history, and these entries might not include logs.
- You can’t use this function to get logs for runs that are in progress because the logs file is only available after the run is complete.

## Examples

The following example looks up the most recent dbt project object execution using DBT\_PROJECT\_EXECUTION\_HISTORY and then fetches the logs for that execution using
SYSTEM$GET\_DBT\_LOG, so you can inspect what happened during the execution.

Tip

Use function arguments such as `DATABASE`, `SCHEMA`, and `OBJECT_NAME` to filter results whenever possible. These filters are applied before the `RESULT_LIMIT` (default: 100 rows), so using them ensures you get the most relevant results rather than filtering a potentially truncated result set with a `WHERE` clause.

Copy code

```
--Look up the most recent dbt project object execution
SET latest_query_id = (SELECT query_id
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY(
    DATABASE => 'ANALYTICS_DB',
    SCHEMA => 'DBT_PROD',
    OBJECT_NAME => 'FINANCE_ANALYTICS'
  ))
  ORDER BY query_end_time DESC LIMIT 1);

--Get the dbt run logs for the most recent dbt project object execution
SELECT SYSTEM$GET_DBT_LOG($latest_query_id);
```

```
============================== 15:14:53.100781 | 46d19186-61b8-4442-8339-53c771083f16 ==============================
[0m15:14:53.100781 [info ] [Dummy-1   ]: Running with dbt=1.9.4
...
[0m15:14:58.198545 [debug] [Dummy-1   ]: Command `cli run` succeeded at 15:14:58.198121 after 5.19 seconds
```

To retrieve more than the default 1,000 lines, pass a second argument specifying the maximum number of lines:

Copy code

```
SELECT SYSTEM$GET_DBT_LOG($latest_query_id, 1000000);
```

For more information, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).
