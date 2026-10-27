# Oct 23, 2026: Atomic deployments, centralized configuration, and advanced branching for task graphs (*Preview*)

With this preview release, you can manage task graph settings centrally, update pipelines without suspending them, and control when
tasks run based on upstream outcomes.

## Centralized configuration and atomic deployments

The new `TASK GRAPH` SQL commands let you:

- Define the schedule, retry behavior, and default settings for member tasks in one place.
- Update the graph and its member tasks without suspending the pipeline.
- Stage changes and commit them together as a new version.

Subsequent runs use the newly committed version. Runs already in progress continue using the version they started with.

For more information, see [Create and manage task graphs with SQL](/user-guide/task-graph-object).

## Advanced branching

By default, a child task in a task graph runs only when all of its predecessors succeed. Advanced branching lets a task run on other
outcomes, such as when all of its predecessors failed, when at least one succeeded, or when a specific upstream task reached a
particular state. Use it to build error handling, fallback paths, and cleanup logic directly into a task graph.

Two new system functions support advanced branching in a task’s `WHEN` clause:

- [SYSTEM$PREDECESSORS\_STATE](/sql-reference/functions/system_predecessors_state) evaluates predecessor completion states against a condition, such as
  `ALL_FAILED` or `ALL_DONE`.
- [SYSTEM$TASK\_COMPLETION\_STATE](/sql-reference/functions/system_task_completion_state) returns the completion state of a specific task in the graph, such as
  `SUCCEEDED`, `FAILED`, or `SKIPPED`.

A task evaluates these conditions after all of its resumed predecessors finish.

For more information, see [Control when tasks run with advanced branching](/user-guide/tasks-graphs#label-task-graph-advanced-branching).
