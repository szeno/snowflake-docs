# Run tasks conditionally

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

By default, a task in a task graph runs after all its predecessors succeed. Add a condition to a task when you want it to run in other
cases, for example to send an alert when a step fails, to skip a step when there’s no new data, or to choose between two branches.

To add a condition, select the task on the canvas, select the **Task** tab in the settings drawer, and then use the **Dependencies**
section:

- **Predecessors condition**: run the task based on how its predecessors finished.
- **Additional conditions**: a Boolean SQL expression that must be true for the task to run. For example,
  `SYSTEM$STREAM_HAS_DATA('my_db.my_schema.orders_stream')` runs the task only when a stream has new data.

If you set both, the task runs only when both are true. Otherwise, it’s skipped.

## Predecessors conditions

| Predecessors condition | The task runs when |
| --- | --- |
| **All succeeded (default)** | Every predecessor succeeded. |
| **All done** | Every predecessor finished, whether it succeeded, failed, was skipped, or was canceled. |
| **At least one failed** | At least one predecessor failed. |
| **All failed** | Every predecessor failed. |
| **At least one succeeded** | At least one predecessor succeeded. |
| **None failed** | No predecessor failed. Each predecessor succeeded or was skipped. |
| **None failed, at least one succeeded** | No predecessor failed, and at least one succeeded. |
| **All skipped** | Every predecessor was skipped. |
| **None skipped** | No predecessor was skipped. |

Expand

Show lessSee more

A task checks its condition after all its predecessors finish. You can’t set a predecessors condition on a task graph’s root task or its
finalizer task. For how conditions affect scheduling, retries, and cost, see
[advanced branching](/user-guide/tasks-graphs#label-task-graph-advanced-branching).

## Branch on a predecessor’s return value

To choose between two paths at run time, have one task set a return value, and give each task that follows it an additional condition that
checks the value. Only the task whose condition is true runs. The other is skipped.

1. In the deciding task, call [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value). For example, a SQL task can run:

   Copy code

   ```
   CALL SYSTEM$SET_RETURN_VALUE(
     IFF((SELECT COUNT(*) FROM my_db.my_schema.raw_orders) > 1000000, 'FULL', 'INCREMENTAL'));
   ```
2. Connect two tasks after the deciding task.
3. In the first task’s **Additional conditions**, enter:

   Copy code

   ```
   SYSTEM$GET_PREDECESSOR_RETURN_VALUE('CHECK_VOLUME_TASK') = 'FULL'
   ```
4. In the second task’s **Additional conditions**, enter:

   Copy code

   ```
   SYSTEM$GET_PREDECESSOR_RETURN_VALUE('CHECK_VOLUME_TASK') = 'INCREMENTAL'
   ```

Pass the task name without the database and schema. Task names are case-sensitive. For more information, see
[Pass return values between tasks](/user-guide/tasks-graphs#label-task-graph-pass-return-values).

To run a task after either branch, such as a task that publishes the results, connect it after both branch tasks and set its
predecessors condition to **None failed, at least one succeeded**. With the default **All succeeded**, it would never run, because one
branch is always skipped.
