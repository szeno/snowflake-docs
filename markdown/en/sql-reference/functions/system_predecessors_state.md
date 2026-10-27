Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$PREDECESSORS\_STATE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Indicates whether the predecessors of the current task completed in the states described by a specified condition. Use this function in the
`WHEN` clause of a task in a [task graph](/user-guide/tasks-graphs) to run the task on outcomes other than “all predecessors succeeded.”

For an explanation of how this function changes the way Snowflake schedules tasks in a graph, see
[How advanced branching changes scheduling](/user-guide/tasks-graphs#label-task-graph-advanced-branching-scheduling).

## Syntax

Copy code

```
SYSTEM$PREDECESSORS_STATE('<condition>')
```

## Arguments

`'condition'`
:   The condition to evaluate against the completion states of the current task’s predecessors. Specify one of the following values:

    | Condition | Returns TRUE when |
    | --- | --- |
    | `ALL_SUCCEEDED` | Every predecessor succeeded. This is the default condition that Snowflake applies to a task that doesn’t specify a predecessor condition. |
    | `ALL_FAILED` | Every predecessor failed. |
    | `ALL_DONE` | Every predecessor reached a terminal state, in any combination of `SUCCEEDED`, `FAILED`, `SKIPPED`, and `CANCELLED`. |
    | `ALL_SKIPPED` | Every predecessor was skipped. |
    | `AT_LEAST_ONE_FAILED` | One or more predecessors failed. |
    | `AT_LEAST_ONE_SUCCEEDED` | One or more predecessors succeeded. |
    | `NONE_FAILED` | No predecessor failed. Every predecessor either succeeded or was skipped. |
    | `NONE_FAILED_MIN_ONE_SUCCEEDED` | No predecessor failed, and at least one predecessor succeeded. |
    | `NONE_SKIPPED` | No predecessor was skipped. Every predecessor either succeeded or failed. |

    Expand

    Show lessSee more

    The condition name must be enclosed in single quotes.

## Returns

Returns `TRUE` if the completion states of the current task’s predecessors satisfy the specified condition, and `FALSE` otherwise.

## Usage notes

- You can only call this function from a `WHEN` clause on a child task. Calling it from a root task, a finalizer task, or outside of a task
  fails when you resume the task or commit the task definition.
- Every condition is evaluated after all of the current task’s predecessors reach a terminal state. A task is scheduled once its
  predecessors are done, not as soon as the condition could first be satisfied. For example, a task using `AT_LEAST_ONE_FAILED` doesn’t run
  the moment the first predecessor fails. Snowflake waits for the remaining predecessors to finish, and then the condition returns `TRUE`
  because at least one of them failed.
- The function evaluates the predecessors of the current task only. It doesn’t consider tasks elsewhere in the graph. To check the state
  of a specific named task, use [SYSTEM$TASK\_COMPLETION\_STATE](/sql-reference/functions/system_task_completion_state).
- A task can combine this function with other supported `WHEN` expressions, including
  [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) and [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value). Snowflake
  evaluates the whole expression, so the task runs only when the combined expression is `TRUE`.
- When a task graph contains at least one task that calls this function or
  [SYSTEM$TASK\_COMPLETION\_STATE](/sql-reference/functions/system_task_completion_state), Snowflake schedules every task in the graph, no matter what state the
  predecessors of each task completed in. Tasks in the graph that don’t specify a predecessor condition behave as though their `WHEN`
  clause ends with `AND SYSTEM$PREDECESSORS_STATE('ALL_SUCCEEDED')`. For the full description of this behavior, see
  [How advanced branching changes scheduling](/user-guide/tasks-graphs#label-task-graph-advanced-branching-scheduling).

## Examples

Run a cleanup task only when every predecessor failed:

Copy code

```
CREATE TASK task_cleanup
  WAREHOUSE = my_warehouse
  AFTER task_load_orders, task_load_customers
  WHEN SYSTEM$PREDECESSORS_STATE('ALL_FAILED')
  AS
    INSERT INTO load_alerts VALUES ('All loads failed', CURRENT_TIMESTAMP());
```

Create the same root and child task using the [Python API](/developer-guide/snowflake-python-api/snowflake-python-managing-tasks), setting
the child task’s `predecessors` and `condition` properties directly:

Copy code

```
from snowflake.core.task import Task

task_root = Task(
  name="task_root",
  definition="SELECT 1",
  warehouse="my_warehouse",
)
task_cleanup = Task(
  name="task_cleanup",
  definition="INSERT INTO load_alerts VALUES ('All loads failed', CURRENT_TIMESTAMP())",
  warehouse="my_warehouse",
  predecessors=["task_root"],
  condition="SYSTEM$PREDECESSORS_STATE('ALL_FAILED')",
)

tasks = root.databases["my_db"].schemas["my_schema"].tasks
tasks.create(task_root)
tasks.create(task_cleanup)
```

Run a reporting task after every predecessor reaches a terminal state, whatever that state is:

Copy code

```
CREATE TASK task_report
  WAREHOUSE = my_warehouse
  AFTER task_load_orders, task_load_customers
  WHEN SYSTEM$PREDECESSORS_STATE('ALL_DONE')
  AS
    CALL build_load_report();
```

Run a task when no predecessor failed and at least one produced data, and only when a stream also has data to process:

Copy code

```
CREATE TASK task_transform
  WAREHOUSE = my_warehouse
  AFTER task_load_orders, task_load_customers
  WHEN SYSTEM$PREDECESSORS_STATE('NONE_FAILED_MIN_ONE_SUCCEEDED')
   AND SYSTEM$STREAM_HAS_DATA('my_order_stream')
  AS
    INSERT INTO orders_clean SELECT * FROM my_order_stream;
```
