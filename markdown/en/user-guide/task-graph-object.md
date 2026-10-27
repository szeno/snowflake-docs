# Declare Task Graph as an object

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A **task graph** is a directed acyclic graph (DAG) of tasks that run together
as a single orchestrated unit. The Task Graph Object introduces a first-class
`TASK GRAPH` database object that encapsulates those tasks, giving a pipeline
a single place for graph-wide settings and the ability to edit a running graph
without suspending it first.

---

## Overview

A task graph lets you build multi-step pipelines (extract, transform,
validate, publish) where each step runs after its predecessors finish, with
branches running in parallel where the dependency structure allows.

If you have used tasks before, you already know most of the building blocks:
a task runs SQL or a stored procedure, on a schedule or when triggered, on
serverless compute or a user-managed warehouse. The Task Graph Object introduces
an explicit **graph object** that encapsulates those tasks and provides:

- A **single place for graph-wide default settings** (schedule, overlap policy,
  retry behavior, and member defaults).
- The ability to **edit a running graph without suspending it first**. Changes
  are staged until you `COMMIT` them.

You create and manage a task graph object with the `TASK GRAPH` SQL commands,
documented in [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph) and
[ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph).

### The Task Graph Object

Historically, a task graph had no object of its own. The graph’s identity and
all of its settings (schedule, overlap policy, retry behavior) lived on the
*root task*, which was simultaneously a step in the pipeline and the
configuration surface for the whole pipeline.

The `TASK GRAPH` object owns:

- **Graph-level properties**: the schedule, the root task, the finalizer, the
  overlap policy, notification integrations, and configuration (`CONFIG`).
- **Member defaults** (`TASK_DEFAULTS`): default settings, such as the
  warehouse or log level, that apply to every member task unless the member
  overrides them.
- **Membership**: the set of tasks reachable from the graph’s root task,
  linked by their `AFTER` (predecessor) relationships.

Member tasks are still ordinary tasks created with `CREATE TASK`.

A task graph has exactly one root task.

### Atomic deployments

**You no longer need to suspend your graph to make changes to it.** You can
alter a running task graph (its properties, its member tasks, even its shape),
and your changes remain as **staged changes** until you `COMMIT` the graph,
at which point subsequent executions use the new version.

This works because a running graph executes against a **committed version**: a
frozen snapshot of the graph’s shape and settings captured when you run
`COMMIT`. Running executions always use the committed version they started
with, so staged edits never disturb a run in progress.

---

## Core concepts

### Graph properties, parameters, and member defaults

Task graphs have three kinds of settings.

**Graph properties** describe the pipeline as a whole and are set directly on
the graph object:

- `SCHEDULE`
- `ROOTS`
- `FINALIZER`
- `OVERLAP_POLICY`
- `ERROR_INTEGRATION`
- `SUCCESS_INTEGRATION`
- `CONFIG`
- `WHEN`

**Graph parameters** also apply to the graph as a whole. They follow the
standard account → database → schema parameter inheritance hierarchy, but
because they describe graph-level behavior they are not meaningful to set on
individual member tasks:

- `TASK_AUTO_RETRY_ATTEMPTS`
- `SUSPEND_TASK_AFTER_NUM_FAILURES`

**Task defaults** (`TASK_DEFAULTS`) supply default values that cascade to every
member task. A task can override any of these by setting the property on itself.
`TASK_DEFAULTS` accepts only these properties:

- `WAREHOUSE`
- Serverless compute sizing: `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`,
  `SERVERLESS_TASK_MIN_STATEMENT_SIZE`, `SERVERLESS_TASK_MAX_STATEMENT_SIZE`,
  `TARGET_COMPLETION_INTERVAL`
- `EXECUTE AS USER`
- `USER_TASK_TIMEOUT_MS`
- `LOG_LEVEL`, `TRACE_LEVEL`
- `COMMENT`

---

## Editing and committing task graphs

Task graphs separate *changing* a graph or its tasks from *releasing* those
changes, so you can edit a running graph without disrupting it.

1. **Change freely.** Once a graph has a committed version, you can alter the
   graph object, alter its member tasks, and add or remove member tasks, whether
   the graph is resumed or suspended. These edits are **staged**: they do not
   affect the committed version, so in-flight and scheduled runs continue
   uninterrupted.
2. **COMMIT to release changes.** `COMMIT` freezes your staged changes into a
   new committed version. The next scheduled run picks up the new version.
3. **REVERT to discard changes.** `REVERT` restores the graph and its members
   to the most recently committed version, discarding all staged edits.

With task graphs you edit and then commit, so CI/CD processes no longer need to
manage suspend/resume state.

### Lifecycle commands at a glance

| Command | Effect |
| --- | --- |
| `ALTER TASK GRAPH <name> COMMIT` | Freeze staged changes into a new committed version. Does not start the schedule. |
| `ALTER TASK GRAPH <name> RESUME` | Start running the graph on its schedule, using the most recently committed version. Requires `SCHEDULE` or `WHEN` to be set. |
| `ALTER TASK GRAPH <name> SUSPEND` | Stop scheduling new runs. |
| `ALTER TASK GRAPH <name> REVERT` | Discard staged changes, restoring the graph and its members to the committed version. |
| `EXECUTE TASK GRAPH <name>` | Trigger one immediate run of the committed version, independent of the schedule. |

Expand

Show lessSee more

A graph must have a committed version before it can run. A typical first
deployment is `COMMIT` followed by `RESUME`.

`RESUME` requires the graph to have a `SCHEDULE` or a `WHEN` condition
set. If you want a graph you only ever trigger manually with
`EXECUTE TASK GRAPH`, omit both: you can still `COMMIT` and run it on
demand. See
[ALTER TASK GRAPH … RESUME](/sql-reference/sql/alter-task-graph#label-alter-task-graph-resume).

### You can’t drop a task that is in a committed version

Important

A task that belongs to a graph’s committed version **can’t be dropped or
replaced** (`DROP TASK`, or `CREATE OR REPLACE TASK`) while it’s still part
of that committed version.

To remove a member task:

1. **Sever it from the graph**: remove the predecessor relationship that
   connects it (for example with `ALTER TASK ... REMOVE AFTER`) so it is no
   longer reachable from the root.
2. **COMMIT** that change.
3. Once the task is no longer part of the committed version, you can drop it.

---

## SQL reference

The task graph SQL commands are documented on dedicated reference pages.
Member tasks are created and altered with the standard
[CREATE TASK](/sql-reference/sql/create-task) /
[ALTER TASK](/sql-reference/sql/alter-task) commands.

- [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph) — create,
  replace, or alter a task graph object
- [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph) — change
  properties, commit, resume, suspend, or revert
- [EXECUTE TASK GRAPH](/sql-reference/sql/execute-task-graph) — trigger
  one immediate run
- [DROP TASK GRAPH](/sql-reference/sql/drop-task-graph) — drop the graph
  object
- [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs) — list graph
  objects
- [DESCRIBE TASK GRAPH](/sql-reference/sql/desc-task-graph) — show the
  full graph definition
- [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks) — list
  tasks in a graph’s committed version
- [DESCRIBE COMMITTED TASK](/sql-reference/sql/desc-committed-task) —
  show a single task’s committed definition

---

## Monitoring task graphs

Use these commands and functions to inspect task graphs and their runs:

- [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs) — list graph
  objects and their properties
- [DESCRIBE TASK GRAPH](/sql-reference/sql/desc-task-graph) — show the
  full definition of a graph
- [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks) — list
  tasks in the committed (running) version
- [DESCRIBE COMMITTED TASK](/sql-reference/sql/desc-committed-task) — show
  a single task’s committed definition
- `GET_DDL('TASK GRAPH', '<name>')` — return a runnable script that recreates
  the member tasks and the graph
- `TASK_GRAPH_CHANGES` — show staged changes waiting for a `COMMIT`

Tip

`SHOW TASKS` reflects your latest (possibly staged) edits.
`SHOW COMMITTED TASKS` reflects what is deployed. If the two differ, you
have staged changes waiting for a `COMMIT`.

### Existing task monitoring surfaces

The existing task monitoring functions and views also cover task graphs:

- [TASK\_HISTORY](/sql-reference/functions/task_history) accepts a `GRAPH_ID`
  argument and returns a `GRAPH_ID` column.
- [CURRENT\_TASK\_GRAPHS](/sql-reference/functions/current_task_graphs) and
  [COMPLETE\_TASK\_GRAPHS](/sql-reference/functions/complete_task_graphs)
  accept a `GRAPH_NAME` argument and return `GRAPH_ID` and `GRAPH_NAME`
  columns.
- The Account Usage and Organization Usage
  [TASK\_HISTORY](/sql-reference/account-usage/task_history),
  [COMPLETE\_TASK\_GRAPHS](/sql-reference/account-usage/complete_task_graphs),
  and [TASK\_VERSIONS](/sql-reference/account-usage/task_versions) views
  return a `GRAPH_ID` column, and COMPLETE\_TASK\_GRAPHS also returns
  `GRAPH_NAME`.

Pass either a graph argument or a root-task argument, not both. For rows
from a task graph, the graph columns are populated and the root-task
columns (`ROOT_TASK_ID`, and `ROOT_TASK_NAME` where it exists) are NULL.
For a root-task-based graph, the reverse is true.

Two additional surfaces are specific to task graph objects:

- [TASK\_GRAPH\_CHANGES](/sql-reference/functions/task_graph_changes) previews
  the uncommitted changes for a graph before you commit them.
- [`SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_ID')`](/sql-reference/functions/system_task_runtime_info)
  and `SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_NAME')` return the
  identity of the current task graph from inside a running task.
