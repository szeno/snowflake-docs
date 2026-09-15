Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$TASK\_DEPENDENTS\_ENABLE

Recursively resumes a specified task and all its dependent tasks. This function allows the owner of a [task graph](/user-guide/tasks-graphs#label-task-dag)
(like the role with the OWNERSHIP privilege on the tasks) to resume the tasks by executing a single SQL statement rather than resuming each task individually (using [ALTER TASK](/sql-reference/sql/alter-task) … RESUME).

For more information about tasks, see [Introduction to tasks](/user-guide/tasks-intro).

## Syntax

Copy code

```
SYSTEM$TASK_DEPENDENTS_ENABLE( '<task_name>' )
```

## Arguments

`task_name`
:   Name of a task in a simple task graph. It does not need to be a root task.

## Usage notes

- `task_name` is a string so it must be enclosed in single quotes:
  - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully qualified), that is, `'<db>.<schema>.<task_name>'`.
  - If the task name is case sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, that is, `'"<task_name>"'`.
  - Accounts are currently limited to a maximum of 30,000 resumed tasks (that is, tasks in a `Started` state) .

## Examples

Resume a specified task and all its dependent tasks in a tree where the specified task has a case-insensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('mydb.myschema.mytask');
> ```

Resume a specified task and all its dependent tasks in a tree where the specified task has a case-sensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('mydb.myschema."myTask"');
> ```
