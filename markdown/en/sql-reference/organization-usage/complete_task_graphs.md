Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# COMPLETE\_TASK\_GRAPHS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

You can use the Organization Usage view to query the status of completed *graph* runs, such as runs that executed successfully, failed, or
were cancelled. A graph is currently defined as a single scheduled task or a [task graph](/user-guide/tasks-graphs#label-task-dag) composed of a
scheduled root task and one or more child tasks. For the purposes of this function, *root task* refers to either the single scheduled task
or the root task in a task graph.

The view avoids the 10,000 row limitation of the [COMPLETE\_TASK\_GRAPHS](/sql-reference/functions/complete_task_graphs).

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
| ROOT\_TASK\_NAME | TEXT | Name of the root task. |
| DATABASE\_NAME | TEXT | Name of the database that contains the graph. |
| SCHEMA\_NAME | TEXT | Name of the schema that contains the graph. |
| STATE | TEXT | State of the graph run:   - `SUCCEEDED`: All tasks in the graph ran successfully to completion, or the root task run succeeded and one or more child task runs were skipped. - `FAILED`: One or more task runs in the graph failed, or the root task run succeeded and one or more child task runs failed. - `CANCELLED`: One or more task runs in the graph were cancelled, or the root task run succeeded and one or more child task runs were cancelled.   Note that if the state of the root task run is SKIPPED, the function does not return a row for the run. |
| SCHEDULED\_FROM | TEXT | One of:  - `SCHEDULE`: The task was scheduled to run normally, as described in SCHEDULE or AFTER clauses of [CREATE TASK](/sql-reference/sql/create-task). - `EXECUTE_TASK`: The task was scheduled to run with [EXECUTE TASK](/sql-reference/sql/execute-task). - `MANUAL RETRY`: The task was scheduled to run with [EXECUTE TASK … RETRY LAST](/sql-reference/sql/execute-task). - `AUTOMATIC RETRY`: The task was configured to retry on failure and the previous execution failed. For more information, see [Automatically retry failed task runs](/user-guide/tasks-intro#label-tasks-automatically-retry). - `TRIGGER` : The task was run because the stream, in the `WHEN` clause of the task, contained new data.  For runs of child tasks in a task graph, the column returns the same value as the root task run. |
| FIRST\_ERROR\_TASK\_NAME | TEXT | Name of the first task in the graph that returned an error; returns NULL if no task produced an error. |
| FIRST\_ERROR\_CODE | NUMBER | Error code of the error returned by the task named in FIRST\_ERROR\_TASK\_NAME; returns NULL if no task produced an error. |
| FIRST\_ERROR\_MESSAGE | TEXT | Error message of the error returned by the task named in FIRST\_ERROR\_TASK\_NAME; returns NULL if no task produced an error. |
| SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the root task was scheduled to start running. Note that we make a best effort to ensure absolute precision, but only guarantee that tasks do not execute *before* the scheduled time. |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | Time when the query in the root task definition started to run. This timestamp aligns with the start time for the query returned by QUERY\_HISTORY. |
| NEXT\_SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the standalone or root task (in a [DAG](/user-guide/tasks-graphs#label-task-dag) of tasks) is next scheduled to start running, assuming the current run of the standalone task or [DAG](/user-guide/tasks-graphs#label-task-dag) started at the SCHEDULED\_TIME time completes in time. |
| COMPLETED\_TIME | TIMESTAMP\_LTZ | Time when the last task in the [DAG](/user-guide/tasks-graphs#label-task-dag) was completed. |
| ROOT\_TASK\_ID | TEXT | Unique identifier for the root task in a [DAG](/user-guide/tasks-graphs#label-task-dag). This ID matches the ID column value in the SHOW TASKS output for the same task. |
| GRAPH\_VERSION | NUMBER | Integer identifying the version of the [DAG](/user-guide/tasks-graphs#label-task-dag) that was run, or is scheduled to be run. |
| RUN\_ID | NUMBER | Time when the standalone or root task in a [DAG](/user-guide/tasks-graphs#label-task-dag) is/was originally scheduled to start running. Format is epoch time (in milliseconds).     *Original* scheduled time refers to rare instances when the system may reschedule the same task to run at a different time to retry it or rebalance the load. If that happens, RUN\_ID shows the original scheduled run time and SCHEDULED\_TIME shows the rescheduled run time.     Note that RUN\_ID may not be a unique identifier for the current task/graph run prior to retry. You may use GRAPH\_RUN\_GROUP\_ID column as a replacement for RUN\_ID. |
| ATTEMPT\_NUMBER | NUMBER | Integer representing the number of attempts to run this task. Initially one. |
| CONFIG | TEXT | Displays the graph level configuration used during the graph run if explicitly set. Otherwise displays NULL. |
| GRAPH\_RUN\_GROUP\_ID | TEXT | Identifier for the graph run. When a graph run has multiple task runs, each task run will show the same GRAPH\_RUN\_GROUP\_ID. The combination of GRAPH\_RUN\_GROUP\_ID, and ATTEMPT\_NUMBER can be used to uniquely identify a graph run. |
| BACKFILL\_INFO | OBJECT | Reserved for future use. The returned value for all rows is NULL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.

## Examples

Retrieve records for the 10 most recent task graph runs completed in your organization:

Copy code

```
SELECT account_name, root_task_name, state
FROM snowflake.organization_usage.complete_task_graphs
  LIMIT 10;
```
