# Mar 13, 2026: New OVERLAP\_POLICY parameter for task graphs

The new `OVERLAP_POLICY` parameter for task graphs replaces the deprecated `ALLOW_OVERLAPPING_EXECUTION` parameter
and provides more granular control over concurrent task graph execution. You can set this parameter on a root task using
[CREATE TASK](/sql-reference/sql/create-task) or [ALTER TASK](/sql-reference/sql/alter-task).

`OVERLAP_POLICY` supports three values:

- `NO_OVERLAP` (default): Executes tasks serially. The next run of a root task is scheduled only after all child tasks finish running.
- `ALLOW_CHILD_OVERLAP`: Allows child task parallelism. A new instance of the task graph can start while child tasks from a
  previous run are still executing. Root tasks never overlap with this policy.
- `ALLOW_ALL_OVERLAP`: Allows true parallelism. Multiple instances of the entire task graph, including the root task,
  can run concurrently.

For backward compatibility, `ALLOW_OVERLAPPING_EXECUTION = TRUE` maps to `OVERLAP_POLICY = ALLOW_CHILD_OVERLAP`, and
`ALLOW_OVERLAPPING_EXECUTION = FALSE` maps to `OVERLAP_POLICY = NO_OVERLAP`.

For more information, see [Create a sequence of tasks with a task graph](/user-guide/tasks-graphs).
