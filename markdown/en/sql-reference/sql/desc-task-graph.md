# DESCRIBE TASK GRAPH

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Describes a [task graph](/user-guide/task-graph-object), including its
graph-wide properties and `TASK_DEFAULTS`.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph), [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs), [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks)

## Syntax

Copy code

```
DESC[RIBE] TASK GRAPH <name>
```

## Parameters

`name`
:   Specifies the identifier for the task graph to describe.

## Output

Returns one row with the same columns as
[SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs#label-show-task-graphs-output).

## Usage notes

- The output describes the graph object. To see the committed definition of
  its member tasks, use [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks) or
  [DESCRIBE COMMITTED TASK](/sql-reference/sql/desc-committed-task).

## Examples

Copy code

```
DESCRIBE TASK GRAPH my_pipeline;
```
