# DROP TASK GRAPH

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Drops a [Task Graph Object](/user-guide/task-graph-object).

See also:
:   [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph), [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs)

Important

Dropping the graph object does **not** drop its member tasks. The graph must be suspended before it can be dropped.

## Syntax

Copy code

```
DROP TASK GRAPH [ IF EXISTS ] <name>
```

## Parameters

`name`
:   String that specifies the identifier of the task graph to drop.

## Usage notes

- A task that belongs to a graph’s committed version can’t be dropped or replaced while it’s still part of that committed version. To remove a member task, sever its predecessor relationship, `COMMIT` that change, and then drop the task — see [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph).
- Dropping the graph object leaves the member tasks in place as ordinary tasks. Drop them separately if you no longer need them.
- A dropped task graph can’t be restored with UNDROP.

## Examples

Copy code

```
ALTER TASK GRAPH my_pipeline SUSPEND;
DROP TASK GRAPH my_pipeline;
```
