Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# TASK\_HISTORY

You can use this table function to query the history of [task](/user-guide/tasks-intro) usage within a specified date range.
The function returns the history of task usage for your entire Snowflake account, a specified task, or task graph.

This function can return all executions run in the past seven days or the next scheduled execution within the next eight days.

## Syntax

Copy code

```
TASK_HISTORY(
      [ SCHEDULED_TIME_RANGE_START => <constant_expr> ]
      [, SCHEDULED_TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <integer> ]
      [, TASK_NAME => '<string>' ]
      [, DATABASE_NAME => '<string>' ]
      [, SCHEMA_NAME => '<string>' ]
      [, ERROR_ONLY => { TRUE | FALSE } ]
      [, ROOT_TASK_ID => '<string>'] )
```

## Arguments

All the arguments are optional.

`SCHEDULED_TIME_RANGE_START => constant_expr` , `SCHEDULED_TIME_RANGE_END => constant_expr`
:   Time range (in [TIMESTAMP\_LTZ format](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations)), within the last 7 days, in which the task execution was scheduled. If the time range does not fall
    within the last 7 days, an error is returned.

    - If `SCHEDULED_TIME_RANGE_END` is not specified, the function returns those tasks that have already completed, are currently
      running, or are scheduled in the future.
    - If `SCHEDULED_TIME_RANGE_END` is [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp), the function returns those tasks that have
      already completed or are currently running. Note that a task that is executed immediately before the current time might still be
      identified as scheduled.
    - To query only those tasks that have already completed or are currently running, include `WHERE query_id IS NOT NULL` as a filter.
      The QUERY\_ID column in the TASK\_HISTORY output is populated only when a task has started running.

    Note

    If no start or end time is specified, the most recent tasks are returned, up to the specified RESULT\_LIMIT value.

`RESULT_LIMIT => integer`
:   A number specifying the maximum number of rows returned by the function.

    If the number of matching rows is greater than this limit, the task executions with the most recent timestamp are returned, up to the specified limit.

    Range: `1` to `10000`

    Default: `100`.

`TASK_NAME => string`
:   A case-insensitive string specifying a task. Only non-qualified task names are supported. Only executions of the specified task are returned. Note that if multiple tasks have the same name, the function returns the history for each of these tasks.

`DATABASE_NAME => string`
:   A string specifying which database to filter tasks by. Note that your role must have the USAGE privilege on the database. Use double quotes within the string to match case-sensitively.

`SCHEMA_NAME => string`
:   A string specifying which schema to filter tasks by. If you provide this argument, then you must also specify DATABASE\_NAME. Note that your role must have the USAGE privilege on the schema and database. Use double quotes within the string to match case-sensitively.

`ERROR_ONLY => { TRUE | FALSE }`
:   When set to TRUE, this function returns only task runs that failed or were cancelled.

    Default: `FALSE`.

`ROOT_TASK_ID =>string`
:   Unique identifier for the root task in a task graph. This ID matches the ID column value in the SHOW TASKS output for the same task.
    Specify the ROOT\_TASK\_ID to show the history of the root task and any child tasks that are part of the task graph.

## Usage notes

- Use function arguments such as DATABASE\_NAME, SCHEMA\_NAME, and TASK\_NAME to filter results whenever possible. These filters are applied before the RESULT\_LIMIT (default: 100 rows), so using them ensures you get the most relevant results rather than filtering a potentially truncated result set with a WHERE clause.
- If you provide SCHEMA\_NAME, you must also provide DATABASE\_NAME to qualify it.
- To view a task graph within this function, the invoking role requires at least one of the following privileges:

  - OWNERSHIP privilege on the task (that is, the task owner).
  - MONITOR or OPERATE privileges on the task.
  - The global MONITOR EXECUTION privilege.
  - The ACCOUNTADMIN role.

  The role must also have the USAGE privilege on the database and schema that store the task, otherwise the DATABASE\_NAME and SCHEMA\_NAME values in the output are NULL.
- This function returns a maximum of 10,000 rows, set in the `RESULT_LIMIT` argument value. The default value is `100`. To avoid
  this limitation, use the [TASK\_HISTORY view](/sql-reference/account-usage/task_history) (Account Usage).
- Note that when the TASK\_HISTORY function is queried, its task name, time range, and result limit arguments are applied first
  followed by the WHERE and LIMIT clause, respectively, if specified. In addition, the TASK\_HISTORY function returns records in descending
  SCHEDULED\_TIME order. Tasks in a SUCCEEDED, FAILED, or CANCELLED state are usually scheduled earlier, so they are generally returned
  later in the search results.
- In practice, if you have many tasks running in your account, the results returned by the function could include fewer than expected
  completed tasks or only scheduled tasks. To query the history of tasks that have already run, use a combination of
  the `SCHEDULED_TIME_RANGE_START => constant_expr` and `SCHEDULED_TIME_RANGE_END => constant_expr` arguments.
- When calling an information schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully qualified. For more information, see [Snowflake Information Schema](/sql-reference/info-schema).
- Tasks run during a cloud services failure might appear as duplicate entries in the results of this function. During a cloud services
  failure, Snowflake might rerun a task causing the task to have two UUIDs with different task SCHEDULED\_TIME.
  [TASK\_HISTORY view](/sql-reference/account-usage/task_history) only displays the final UUID of the rerun task.
- All tasks in a task graph run show the same task history output.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_ID | TEXT | ID of the SQL statement executed by the task. Can be joined with the QUERY\_HISTORY view for additional details about the execution of the statement or stored procedure. |
| NAME | TEXT | Name of the task. |
| DATABASE\_NAME | TEXT | Name of the database that contains the task. |
| SCHEMA\_NAME | TEXT | Name of the schema that contains the task. |
| QUERY\_TEXT | TEXT | Text of the SQL statement. |
| CONDITION\_TEXT | TEXT | Text of WHEN condition the task evaluates when determining whether to run. |
| STATE | TEXT | Status of the task:   - `SCHEDULED`: scheduled for execution. - `EXECUTING`: currently executing. - `SUCCEEDED`: execution successful. - `FAILED`: execution failed. The timed-out tasks always have a `FAILED` state in the task history. - [FAILED\_AND\_AUTO\_SUSPENDED](/user-guide/tasks-intro#label-tasks-automatically-suspend): task failed, and was automatically suspended. - `CANCELLED`: execution cancelled. - `SKIPPED`: indicates that a task run began, but the optional `WHEN` parameter in the task definition returned a FALSE value; therefore, the run did not resume the warehouse (if the task uses customer-managed compute resources) or execute the SQL code in the task definition. |
| ERROR\_CODE | NUMBER | Error code, if the statement returned an error. |
| ERROR\_MESSAGE | TEXT | Error message, if the statement returned an error. |
| SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the task is/was scheduled to start running. Tasks start with a brief queueing period before they begin to run. For more information, see [Task duration](/user-guide/tasks-intro#label-task-duration). |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | Time when the query in the task definition started to run, or NULL if SCHEDULED\_TIME is in the future or the current scheduled run has not started yet. This timestamp aligns with the start time for the query returned by QUERY\_HISTORY. |
| NEXT\_SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the standalone or root task (in a [task graph](/user-guide/tasks-graphs#label-task-dag)) is next scheduled to start running, assuming the current run of the standalone task or task graph started at the SCHEDULED\_TIME time completes in time. |
| COMPLETED\_TIME | TIMESTAMP\_LTZ | Time when the task completed, or NULL if SCHEDULED\_TIME is in the future or if the task is still running. |
| ROOT\_TASK\_ID | TEXT | Unique identifier for the root task in a task graph. This ID matches the ID column value in the SHOW TASKS output for the same task. |
| GRAPH\_VERSION | NUMBER | Integer identifying the version of the task graph that was run, or is scheduled to be run. Each incremental increase in the value represents one or more modifications to tasks in the task graph. If the root task is recreated (using CREATE OR REPLACE TASK), then the version number restarts from 1. |
| RUN\_ID | NUMBER | Time when the standalone or root task in a [task graph](/user-guide/tasks-graphs#label-task-dag) is/was originally scheduled to start running. Format is epoch time (in milliseconds).     *Original* scheduled time refers to rare instances when the system might reschedule the same task to run at a different time to retry it or rebalance the load. If that happens, RUN\_ID shows the original scheduled run time and SCHEDULED\_TIME shows the rescheduled run time.     Note that RUN\_ID may not be a unique identifier for the current task/graph run before retry. You can use GRAPH\_RUN\_GROUP\_ID column as a replacement for RUN\_ID. |
| RETURN\_VALUE | TEXT | Value set for the predecessor task in a task graph. The return value is explicitly set by calling the [System\_Set\_Return\_Value](system_set_return_value) function by the predecessor task. |
| SCHEDULED\_FROM | TEXT | One of:  - `SCHEDULE`: The task was scheduled to run normally, as described in SCHEDULE or AFTER clauses of [CREATE TASK](/sql-reference/sql/create-task). - `EXECUTE_TASK`: The task was scheduled to run with [EXECUTE TASK](/sql-reference/sql/execute-task). - `MANUAL RETRY`: The task was scheduled to run with [EXECUTE TASK … RETRY LAST](/sql-reference/sql/execute-task). - `AUTOMATIC RETRY`: The task was configured to retry on failure and the previous execution failed. For more information, see [Automatically retry failed task runs](/user-guide/tasks-intro#label-tasks-automatically-retry). - `TRIGGER` : The task was run because the stream, in the `WHEN` clause of the task, contained new data.  For runs of child tasks in a task graph, the column returns the same value as the root task run. |
| ATTEMPT\_NUMBER | NUMBER | Integer representing the number of attempts to run this task. Initially one. |
| CONFIG | TEXT | Configuration that the task execution used. This includes dynamic configurations specified with [EXECUTE TASK … USING CONFIG](/sql-reference/sql/execute-task). If no configuration is set, the column displays NULL. |
| QUERY\_HASH | TEXT | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_HASH\_VERSION | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_HASH`. |
| QUERY\_PARAMETERIZED\_HASH | TEXT | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| QUERY\_PARAMETERIZED\_HASH\_VERSION | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_PARAMETERIZED_HASH`. |
| GRAPH\_RUN\_GROUP\_ID | TEXT | Identifier for the graph run. When a graph run has multiple task runs, each task run will show the same GRAPH\_RUN\_GROUP\_ID. The combination of GRAPH\_RUN\_GROUP\_ID, and ATTEMPT\_NUMBER can be used to uniquely identify a graph run. |
| BACKFILL\_INFO | OBJECT | Reserved for future use. The returned value for all rows is NULL. |
| SPCS\_JOB\_ID | NUMBER | ID of the Snowpark Container Services (SPCS) job associated with this task run. NULL if the task did not run as a container job. |

Expand

Show lessSee more

## Examples

Retrieve the 100 most recent task executions (completed, still running, or scheduled in the future) in the account. Note that the maximum
number of rows returned by the function is limited to 100 by default:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY())
>   ORDER BY SCHEDULED_TIME;
> ```

Retrieve the execution history for tasks in the account within a specified 30-minute block of time within a specific 7-day period:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(
>     SCHEDULED_TIME_RANGE_START=>TO_TIMESTAMP_LTZ('2024-11-9 12:00:00.000 -0700'),
>     SCHEDULED_TIME_RANGE_END=>TO_TIMESTAMP_LTZ('2024-11-9 12:30:00.000 -0700')));
> ```

Retrieve the 10 most recent executions of a specified task (completed, still running, or scheduled in the future) scheduled within the last hour:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(
>     SCHEDULED_TIME_RANGE_START=>DATEADD('hour',-1,current_timestamp()),
>     RESULT_LIMIT => 10,
>     TASK_NAME=>'mytask'));
> ```
>
> Note
>
> To retrieve only tasks that are completed or still running, filter the query using `WHERE query_id IS NOT NULL`. Note that this filter is applied after `RESULT_LIMIT` already reduces the results returned, so the query could return 9 tasks if 1 task was scheduled but had not started yet.

Retrieve the execution history of all tasks in the task graph of the specified root task.

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(ROOT_TASK_ID=>'d4b89013-c942-465c-bcb8-e7037a932b04'));
> ```

Retrieve the execution history of all tasks in the task graph of the most recently queried root task:

> Copy code
>
> ```
> DESC TASK my_task
> SET task_id=(SELECT "id" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())));
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(ROOT_TASK_ID=>$task_id));
> ```

Retrieve the execution history for tasks in a specified database (case-insensitive):

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(
>     DATABASE_NAME => 'MY_DATABASE'));
> ```

Retrieve the execution history for tasks in a specified schema within that database (both case-insensitive):

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(
>     DATABASE_NAME => 'MY_DATABASE',
>     SCHEMA_NAME => 'MY_SCHEMA'));
> ```

Use double quotes to match the database and schema names case-sensitively:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(
>     DATABASE_NAME => '"my_db"',
>     SCHEMA_NAME => '"my_schema"'));
> ```
