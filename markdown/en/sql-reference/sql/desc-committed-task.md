# DESCRIBE COMMITTED TASK

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Describes the committed definition of a task that belongs to a
[task graph](/user-guide/task-graph-object): the definition that runs.
[DESCRIBE TASK](/sql-reference/sql/desc-task) shows the latest definition,
including changes that haven’t been committed yet.

DESCRIBE can be abbreviated to DESC.

See also:
:   [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks), [DESCRIBE TASK](/sql-reference/sql/desc-task), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs), [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph)

## Syntax

Copy code

```
DESC[RIBE] COMMITTED TASK <name>
```

## Parameters

`name`
:   Specifies the identifier for the task to describe.

## Output

Returns the same columns as
[SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks#label-show-committed-tasks-output).

## Usage notes

- If the task isn’t part of a committed task graph version, the command
  returns no rows.

## Examples

Copy code

```
DESCRIBE COMMITTED TASK t_a;
```
