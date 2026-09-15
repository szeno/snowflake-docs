# Troubleshooting tasks

This section describes a methodical approach to troubleshooting tasks that do not run as expected.

## Task did not run

### Step 1: Verify the task did not run

Query the [TASK\_HISTORY](/sql-reference/functions/task_history) table function to verify the task did not run. It is possible that the task ran successfully but the SQL statement in the task definition failed. In particular, note the scheduled and completed times, as well as any error code and message.

If the task has a predecessor task (in a [task graph](/user-guide/tasks-graphs#label-task-dag)), verify whether the predecessor task completed successfully.

### Step 2: Verify the task was resumed

Snowflake creates all tasks in the SUSPENDED state. Verify the state of the task (or each task in a task graph) is RESUMED (using [DESCRIBE TASK](/sql-reference/sql/desc-task) or [SHOW TASKS](/sql-reference/sql/show-tasks)). Or verify that the task was manually executed using [EXECUTE TASK](/sql-reference/sql/execute-task).

To resume an individual task, execute [ALTER TASK](/sql-reference/sql/alter-task) … RESUME. To recursively enable all dependent tasks tied to a root task, query the [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable) function rather than enabling each task individually.

While you are reviewing the task details, if the task has a schedule, also check the cron expression. Verify that at least one occurrence of the scheduled time has passed.

### Step 3: Verify the permissions granted to the task owner

Verify the task owner (i.e. the role that has the OWNERSHIP privilege on the task) has the following privileges, which are required for the task to run:

| Object | Privilege | Notes |
| --- | --- | --- |
| Account | EXECUTE TASK | Required to run any tasks the role owns. Revoking the EXECUTE TASK privilege on a role prevents all subsequent task runs from starting under that role. |
| Database | USAGE |  |
| Schema | USAGE |  |
| Task | OWNERSHIP |  |
| Warehouse | USAGE |  |

Expand

Show lessSee more

Verify the privileges granted to the role using [SHOW GRANTS](/sql-reference/sql/show-grants) TO ROLE `role_name`.

### Step 4: Verify the condition

If the task includes a WHEN clause with a [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) condition, verify that the specified stream contained change data capture (CDC) records when the task was last scheduled to run. Historical data for a stream can be queried using an [AT | BEFORE](/sql-reference/constructs/at-before) clause.

### Step 5: Check predecessor tasks

If the task is a child task in a task graph, check that the predecessor tasks (parent tasks) ran to completion successfully. If a parent task failed to run to completion, any child tasks are skipped. For more information, see [Create a sequence of tasks with a task graph](/user-guide/tasks-graphs#label-task-dag).

## Task timed out or exceeded the schedule window

There is a 60 minute default limit on a single run of a task. This limitation was implemented as a safeguard against non-terminating tasks. Query the [TASK\_HISTORY](/sql-reference/functions/task_history) table function. If the task was canceled or exceeded the window scheduled for the task, the cause is often an undersized warehouse. Review the warehouse size and consider increasing it to fit within the schedule window or the one-hour limit.

Alternatively, consider increasing the timeout limit for the task by executing [ALTER TASK](/sql-reference/sql/alter-task) … SET USER\_TASK\_TIMEOUT\_MS = *<num>*. To determine if the USER\_TASK\_TIMEOUT\_MS parameter has been set for a specific task, execute the following statement:

Copy code

```
SHOW PARAMETERS LIKE 'USER_TASK_TIMEOUT_MS' IN TASK <task_name>;
```

Where `<task_name>` is the name of the task whose timeout limit you are adjusting. If the statement returns no record, the task currently has the default `3600000` millisecond (60 minute) timeout.

Note that neither increasing the warehouse size nor increasing the timeout limit might help if there are query parallelization issues. Consider looking at alternate ways to rewrite the SQL statement run by the task.
