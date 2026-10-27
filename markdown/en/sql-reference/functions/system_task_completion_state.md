Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$TASK\_COMPLETION\_STATE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the state that a specified task in the current [task graph](/user-guide/tasks-graphs) run completed in. Use this function in the
`WHEN` clause of a task to branch on the outcome of a specific task rather than on the outcome of all of the current task’s predecessors.

To evaluate the states of all of the current task’s predecessors at once, use [SYSTEM$PREDECESSORS\_STATE](/sql-reference/functions/system_predecessors_state).

## Syntax

Copy code

```
SYSTEM$TASK_COMPLETION_STATE('<task_name>')
```

## Arguments

`'task_name'`
:   Identifier for the task whose completion state you want to retrieve.

    - The task name only, without the database name or schema name. All tasks in a task graph must be in the same schema, so there’s no need
      to reference a task in a different schema. For example, use `MYTASK` rather than `MYDATABASE.MYSCHEMA.MYTASK`.
    - The task must be in the same task graph as the task that calls the function. If the task isn’t in the graph, the call fails.
    - For a deterministic result, the task must be a direct or indirect predecessor of the calling task. For details, see
      [Task ordering and determinism](#label-task-completion-state-determinism).

## Returns

Returns one of the following states. Except for `NOT_EXECUTED`, these states match the `STATE` values that the
[TASK\_HISTORY view](/sql-reference/account-usage/task_history) view reports for a completed task run:

| State | Description |
| --- | --- |
| `SUCCEEDED` | The task ran and completed successfully. |
| `FAILED` | The task ran and failed. |
| `SKIPPED` | The task was scheduled, but the conditions of its `WHEN` clause weren’t met, so it didn’t run. |
| `CANCELLED` | The task was canceled. |
| `NOT_EXECUTED` | The specified task hasn’t completed yet in the current run. |

Expand

Show lessSee more

## Usage notes

- You can call this function from a `WHEN` clause on a child task or a finalizer task. Calling it from a root task or outside of a task
  fails when you resume the task or commit the task definition.
- Task names are case-sensitive. Tasks created using `CREATE TASK` without quotes are
  [stored and resolved in uppercase](/sql-reference/identifiers-syntax), so pass the uppercase form of the name. For example, a task
  created with `CREATE TASK task_a` is referenced as `SYSTEM$TASK_COMPLETION_STATE('TASK_A')`.
- The state is scoped to the current task graph run. When a graph run is
  [retried](/user-guide/tasks-graphs#label-task-graph-advanced-branching-retries), the function returns the most recent completion state
  for the task across the attempts in that run.
- When a task graph contains at least one task that calls this function or
  [SYSTEM$PREDECESSORS\_STATE](/sql-reference/functions/system_predecessors_state), Snowflake schedules every task in the graph, no matter what state the
  predecessors of each task completed in. For the full description of this behavior, see
  [How advanced branching changes scheduling](/user-guide/tasks-graphs#label-task-graph-advanced-branching-scheduling).

### Task ordering and determinism

You can pass the name of any task in the graph, but Snowflake only guarantees a deterministic result for a task that is a direct or
indirect predecessor of the calling task. A predecessor always reaches a terminal state before the calling task evaluates its WHEN clause,
so its state is settled.

A task that isn’t a predecessor of the calling task has no such ordering guarantee. It might still be queued, running, or already
complete when the calling task evaluates its condition, so the returned state can vary between runs of the same graph. Branching on a
non-predecessor task can therefore produce different results for identical input data.

If you need to branch on the outcome of another task, make that task a predecessor of the branching task so that the ordering is
guaranteed.

## Examples

Run a task only when a specific upstream task failed, even though its other predecessors succeeded:

Copy code

```
CREATE TASK task_handle_order_failure
  WAREHOUSE = my_warehouse
  AFTER task_load_orders, task_load_customers
  WHEN SYSTEM$TASK_COMPLETION_STATE('TASK_LOAD_ORDERS') = 'FAILED'
  AS
    INSERT INTO load_alerts VALUES ('Order load failed', CURRENT_TIMESTAMP());
```

Take a different path depending on whether an upstream task was skipped:

Copy code

```
CREATE TASK task_backfill
  WAREHOUSE = my_warehouse
  AFTER task_load_orders
  WHEN SYSTEM$TASK_COMPLETION_STATE('TASK_LOAD_ORDERS') = 'SKIPPED'
  AS
    CALL backfill_orders();
```

Require that a predecessor actually completed in this graph run, excluding the `NOT_EXECUTED` state that the function returns for a task
that hasn’t completed yet:

Copy code

```
CREATE TASK task_reconcile
  WAREHOUSE = my_warehouse
  AFTER task_load_orders, task_load_customers
  WHEN SYSTEM$PREDECESSORS_STATE('ALL_DONE')
   AND SYSTEM$TASK_COMPLETION_STATE('TASK_LOAD_ORDERS') != 'NOT_EXECUTED'
  AS
    CALL reconcile_orders();
```
