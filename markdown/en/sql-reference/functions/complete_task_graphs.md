Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# COMPLETE\_TASK\_GRAPHS

Returns the status of a completed *graph* run. The function returns details for runs that executed
successfully, failed, or were cancelled in the past 60 minutes. A graph is currently defined as a single scheduled task or a
[task graph](/user-guide/tasks-graphs#label-task-dag) composed of a scheduled root task and one or more dependent tasks (i.e. tasks that have one or more defined predecessor tasks). For the
purposes of this function, *root task* refers to either the single scheduled task or the root task in a [task graph](/user-guide/tasks-graphs#label-task-dag).

To retrieve the details for graph runs that are currently executing, or are next scheduled to run within the next 8 days, query the
[CURRENT\_TASK\_GRAPHS](/sql-reference/functions/current_task_graphs) table function.

The function returns the graph run details for your entire Snowflake account or a specified root task.

## Syntax

Copy code

```
COMPLETE_TASK_GRAPHS(
      [ RESULT_LIMIT => <integer> ]
      [, ROOT_TASK_NAME => '<string>' ]
      [, ERROR_ONLY => { TRUE | FALSE } ] )
```

## Arguments

All the arguments are optional.

`RESULT_LIMIT => integer`
:   A number specifying the maximum number of rows returned by the function. Note that the results are returned in descending COMPLETED\_TIME
    order. If the number of matching rows is greater than the result limit, the graph executions with the most recent completed timestamp are
    returned, up to the specified limit.

    Range: `1` to `10000`

    Default: `1000`

`ROOT_TASK_NAME => string`
:   A case-insensitive string specifying the name of the root task. Only non-qualified task names are supported. Only graph runs for the
    specified task are returned. Note that if multiple tasks have the same name, the function returns the graph runs for each of these tasks.

`ERROR_ONLY => { TRUE | FALSE }`
:   When set to TRUE, this function returns only graph runs that failed or were cancelled.

## Usage notes

- To view a task graph within this function, the invoking role requires at least one of the following privileges:

  - OWNERSHIP privilege on the task (that is, the task owner).
  - MONITOR or OPERATE privileges on the task.
  - The global MONITOR EXECUTION privilege.
  - The ACCOUNTADMIN role.

  The role must also have the USAGE privilege on the database and schema that store the task, otherwise the DATABASE\_NAME and SCHEMA\_NAME values in the output are NULL.
- This function returns a maximum of 10,000 rows, set in the `RESULT_LIMIT` argument value. The default value is `1000`. To avoid
  this limitation, use the [COMPLETE\_TASK\_GRAPHS view](/sql-reference/account-usage/complete_task_graphs) (Account Usage).
- When the COMPLETE\_TASK\_GRAPHS function is queried, its task name and result limit arguments are applied first
  followed by the WHERE and LIMIT clause, respectively, if specified. In addition, the function returns records in descending
  COMPLETED\_TIME order.

  In practice, if many task graphs completed running in your account in the previous hour, the results returned by the function might not
  include an expected record, especially if the RESULT\_LIMIT value is relatively low.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function
  name must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

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
| SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the root task was scheduled to start. Tasks start with a brief queueing period before they begin to run. For more information, see [Task graph duration](/user-guide/tasks-graphs#label-task-graph-duration). |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | Time when the query in the root task definition started to run. This timestamp aligns with the start time for the query returned by QUERY\_HISTORY. |
| NEXT\_SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the standalone or root task (in a [task graph](/user-guide/tasks-graphs#label-task-dag)) is next scheduled to start running, assuming the current run of the standalone task or [task graph](/user-guide/tasks-graphs#label-task-dag) started at the SCHEDULED\_TIME time completes in time. |
| COMPLETED\_TIME | TIMESTAMP\_LTZ | Time when the last task in the [task graph](/user-guide/tasks-graphs#label-task-dag) completed. |
| ROOT\_TASK\_ID | TEXT | Unique identifier for the root task in a [task graph](/user-guide/tasks-graphs#label-task-dag). This ID matches the ID column value in the SHOW TASKS output for the same task. |
| GRAPH\_VERSION | NUMBER | Integer identifying the version of the [task graph](/user-guide/tasks-graphs#label-task-dag) that was run, or is scheduled to be run. |
| RUN\_ID | NUMBER | Time when the standalone or root task in a [task graph](/user-guide/tasks-graphs#label-task-dag) is/was originally scheduled to start running. Format is epoch time (in milliseconds).     *Original* scheduled time refers to rare instances when the system might reschedule the same task to run at a different time to retry it or rebalance the load. If that happens, RUN\_ID shows the original scheduled run time and SCHEDULED\_TIME shows the rescheduled run time.     Note that RUN\_ID may not be a unique identifier for the current task/graph run before retry. You can use GRAPH\_RUN\_GROUP\_ID column as a replacement for RUN\_ID. |
| ATTEMPT\_NUMBER | NUMBER | Integer representing the number of attempts to run this task. Initially one. |
| CONFIG | TEXT | Displays the graph level configuration used during the graph run if explicitly set. Otherwise displays NULL. |
| GRAPH\_RUN\_GROUP\_ID | TEXT | Identifier for the graph run. When a graph run has multiple task runs, each task run will show the same GRAPH\_RUN\_GROUP\_ID. The combination of GRAPH\_RUN\_GROUP\_ID, and ATTEMPT\_NUMBER can be used to uniquely identify a graph run. |
| BACKFILL\_INFO | OBJECT | Reserved for future use. The returned value for all rows is NULL. |

Expand

Show lessSee more

## Examples

Retrieve the 1000 most recent completed graph executions in the account. Note that the maximum number of rows returned by the function is
limited to 1000 by default. To change the number of rows returned, modify the RESULT\_LIMIT argument value:

> Copy code
>
> ```
> select *
>   from table(information_schema.complete_task_graphs())
>   order by scheduled_time;
> ```

Retrieve the 10 most recent completed graph runs for a specified task graph within the last hour:

> Copy code
>
> ```
> select *
>   from table(information_schema.complete_task_graphs (
>     result_limit => 10,
>     root_task_name=>'MYTASK'));
> ```
