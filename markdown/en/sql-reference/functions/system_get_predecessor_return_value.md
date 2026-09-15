Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE

Retrieves the return value for the predecessor task in a [task graph](/user-guide/tasks-graphs#label-task-dag). The return value is explicitly set by the predecessor task by calling the [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value) function.

## Syntax

Copy code

```
SYSTEM$GET_PREDECESSOR_RETURN_VALUE('<task_name>')
```

## Arguments

`'task_name'`
:   Identifier for the predecessor task that sets the return value to be retrieved.

    - If the task has multiple predecessor tasks that are enabled, this argument is required.
    - If the task has only one predecessor task that is enabled, the argument is optional.
      If this argument is omitted, the function retrieves the return value for the only enabled predecessor task.
    - If the immediate predecessor task name does not match the requested task name, but an ancestor predecessor does match the task name,
      the return value of the matching ancestor is returned.
    - The task name argument should not include the database name or schema name. All tasks in a graph are required to be within the same schema, so there should be no need to reference a task in a different schema. For example, you should use `MYTASK` as an input to this function, instead of using `MYDATABASE.MYSCHEMA.MYTASK`.

## Usage notes

- Task names are case sensitive.
- When a task name is specified, it must match an enabled predecessor, otherwise the call will fail.

## Examples

See complete examples for this function in [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value).
