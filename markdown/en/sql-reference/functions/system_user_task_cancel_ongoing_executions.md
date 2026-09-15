Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$USER\_TASK\_CANCEL\_ONGOING\_EXECUTIONS

Cancels a run of the specified task that the system has already started to process (that is, a run with an EXECUTING state in the [TASK\_HISTORY](/sql-reference/functions/task_history) output).

## Syntax

Copy code

```
SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS( '<task_name>' )
```

## Arguments

`task_name`
:   Name of the task.

## Usage notes

- Only the task owner (that is, the role with the OWNERSHIP privilege on the task) or a role with the OPERATE privilege on the task can call this function.
- `task_name` is a string so it must be enclosed in single quotes:

  - The entire name must be enclosed in single quotes, including the database and schema (if the name is fully-qualified); for example: `'<db>.<schema>.<task_name>'`.
  - If the task name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case or characters. The double quotes must be enclosed within the single quotes; for example: `'"<task_name>"'`.
- This function returns a success message before the current run of the specified task is actually canceled.
- If the current run of the specified task is almost completed, this function might not cancel the run.
- This function only cancels the current run of the specified task. Additional tasks in a [task graph](/user-guide/tasks-graphs#label-task-dag) that includes this
  task might also be running. To cancel these runs, you must call this function and specify the name of each additional child task separately.
- If a task is replaced using CREATE OR REPLACE TASK, this function will not be able to cancel the ongoing executions of the previous task.

  To stop an ongoing task run after you replace it with CREATE OR REPLACE TASK:

  1. Find the query ID of the ongoing run; for example:

     Copy code

     ```
     select name, query_id, state, scheduled_time, error_message
     from table(information_schema.task_history(task_name => 'my_task'));
     ```
  2. Cancel the query using the [SYSTEM$CANCEL\_QUERY](/sql-reference/functions/system_cancel_query) function with the query ID, for example:

     Copy code

     ```
     select system$cancel_query('query_id');
     ```
  3. Monitor the task run for a few seconds until the cancel completes, for example:

     Copy code

     ```
     select name, query_id, state, scheduled_time, error_message
     from table(information_schema.task_history(task_name => 'my_task'));
     ```
- To check if a task run has been cancelled or completed, or if any child tasks are currently running, query the
  [TASK\_HISTORY](/sql-reference/functions/task_history) function.
- To prevent future runs of the task from starting, we recommend first suspending the task (using [ALTER TASK … SUSPEND](/sql-reference/sql/alter-task)) and then executing this function.

  Note that if the task is not suspended when this function is executed, it currently takes several minutes for the Snowflake cloud services to begin scheduling executions of this task again.

## Examples

Cancel the current run of a task with a case-insensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('mydb.myschema.mytask');
> ```

Cancel the current run of a task with a case-sensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('mydb.myschema."myTask"');
> ```

The following example shows a successful cancellation of a task run:

Copy code

```
SELECT SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('my_task');

+------------------------------------------------------------------------------------+
| SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('my_task')                              |
|------------------------------------------------------------------------------------|
| Marked 1 task runs for cancellation. It may take a few seconds for cancellation to |
| complete. Query ids canceled: [2036a04c-9c46-4c6b-b354-67a44b5e0b50]               |
+------------------------------------------------------------------------------------+
```

The following example shows that the task has no currently running executions, so the function doesn’t cancel any runs:

Copy code

```
SELECT SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('my_task');

+------------------------------------------------------------------------------------+
| SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('my_task') |
|------------------------------------------------------------------------------------|
| Task MY_TASK has no currently running executions. If the task was dropped or       |
| replaced after a previous execution started, use SYSTEM$CANCEL_QUERY along with    |
| the query id to cancel the run.                                                    |
|------------------------------------------------------------------------------------|
```
