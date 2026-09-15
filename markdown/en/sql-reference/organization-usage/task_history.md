Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TASK\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view enables you to retrieve the history of [task](/user-guide/tasks-intro) usage.
The view displays one row for each run of a task in the history.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Name of the task. |
| QUERY\_TEXT | VARCHAR | Text of the SQL statement. |
| CONDITION\_TEXT | VARCHAR | Text of WHEN condition the task evaluates when determining whether to run. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the task. |
| TASK\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the task. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the task. |
| TASK\_DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the task. |
| SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the task is/was scheduled to start running. Note that we make a best effort to ensure absolute precision, but only guarantee that tasks do not execute *before* the scheduled time. |
| COMPLETED\_TIME | TIMESTAMP\_LTZ | Time when the task completed. |
| STATE | VARCHAR | Status of the completed task: SUCCEEDED, FAILED, CANCELLED, or SKIPPED. Note that the view does not return SCHEDULED or EXECUTING task runs. To retrieve the task history details for runs in a scheduled or executing state, query the [TASK\_HISTORY](/sql-reference/functions/task_history) table function in the Information Schema. The timed-out tasks always have a `FAILED` state in the task history. |
| RETURN\_VALUE | VARCHAR | Value set for the predecessor task in a [task graph](/user-guide/tasks-graphs#label-task-dag). The return value is explicitly set by calling the [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value) function by the predecessor task. |
| QUERY\_ID | VARCHAR | ID of the SQL statement executed by the task. Can be joined with the QUERY\_HISTORY view for additional details about the execution of the statement or stored procedure. |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | Time when the query in the task definition started to run. This timestamp aligns with the start time for the query returned by QUERY\_HISTORY. |
| ERROR\_CODE | VARCHAR | Error code, if the statement returned an error. |
| ERROR\_MESSAGE | VARCHAR | Error message, if the statement returned an error. |
| GRAPH\_VERSION | NUMBER | Integer identifying the version of the task graph that was run, or is scheduled to be run. Each incremental increase in the value represents one or more modifications to tasks in the task graph. If the root task is recreated (using CREATE OR REPLACE TASK), then the version number restarts from 1. |
| RUN\_ID | NUMBER | Time when the standalone or root task in a task graph is/was originally scheduled to start running. Format is epoch time (in milliseconds).     *Original* scheduled time refers to rare instances when the system may reschedule the same task to run at a different time to retry it or rebalance the load. If that happens, RUN\_ID shows the original scheduled run time and SCHEDULED\_TIME shows the rescheduled run time.     Note that RUN\_ID may not be a unique identifier for the current task/graph run prior to retry. You may use GRAPH\_RUN\_GROUP\_ID column as a replacement for RUN\_ID. |
| ROOT\_TASK\_ID | VARCHAR | Unique identifier for the root task in a task graph. This ID matches the ID column value in the SHOW TASKS output for the same task. |
| SCHEDULED\_FROM | VARCHAR | One of:  - `SCHEDULE`: The task was scheduled to run normally, as described in SCHEDULE or AFTER clauses of [CREATE TASK](/sql-reference/sql/create-task). - `EXECUTE_TASK`: The task was scheduled to run with [EXECUTE TASK](/sql-reference/sql/execute-task). - `MANUAL RETRY`: The task was scheduled to run with [EXECUTE TASK … RETRY LAST](/sql-reference/sql/execute-task). - `AUTOMATIC RETRY`: The task was configured to retry on failure and the previous execution failed. For more information, see [Automatically retry failed task runs](/user-guide/tasks-intro#label-tasks-automatically-retry). - `TRIGGER` : The task was run because the stream, in the `WHEN` clause of the task, contained new data.  For runs of child tasks in a task graph, the column returns the same value as the root task run. |
| ATTEMPT\_NUMBER | NUMBER | Integer representing the number of attempts to run this task. Initially one. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance which the object belongs to. |
| CONFIG | VARCHAR | Displays the graph level configuration if set for the root task, otherwise displays NULL. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_HASH\_VERSION | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_HASH`. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| QUERY\_PARAMETERIZED\_HASH\_VERSION | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_PARAMETERIZED_HASH`. |
| GRAPH\_RUN\_GROUP\_ID | VARCHAR | Identifier for the graph run. When a graph run has multiple task runs, each task run will show the same GRAPH\_RUN\_GROUP\_ID. The combination of GRAPH\_RUN\_GROUP\_ID, and ATTEMPT\_NUMBER can be used to uniquely identify a graph run. |
| BACKFILL\_INFO | OBJECT | Reserved for future use. The returned value for all rows is NULL. |
| SPCS\_JOB\_ID | NUMBER | ID of the Snowpark Container Services (SPCS) job associated with this task run. NULL if the task did not run as a container job. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- For increased performance, filter queries on the COMPLETED\_TIME or SCHEDULED\_TIME column.

## Examples

Retrieve records for the 10 most recent completed task runs:

> Copy code
>
> ```
> SELECT account_name, query_text, completed_time
> FROM snowflake.organization_usage.task_history
> ORDER BY completed_time DESC
> LIMIT 10;
> ```

Retrieve records for task runs completed in the past hour:

> Copy code
>
> ```
> SELECT account_name, query_text, completed_time
> FROM snowflake.organization_usage.task_history
> WHERE completed_time > DATEADD(hours, -1, CURRENT_TIMESTAMP());
> ```
