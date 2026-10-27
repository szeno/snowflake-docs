Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# TASK\_GRAPH\_CHANGES

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This table function previews the uncommitted changes for a [task graph object](/user-guide/task-graph-object) — the difference between the live
(possibly-staged) definition of the graph and its latest committed
version. Use it before running
[`ALTER TASK GRAPH ... COMMIT`](/sql-reference/sql/alter-task-graph#label-alter-task-graph-commit)
to see exactly what a commit would change.

## Syntax

Copy code

```
TASK_GRAPH_CHANGES(
      TASK_GRAPH_NAME => '<string>' )
```

## Arguments

`TASK_GRAPH_NAME => string`
:   Required. A string specifying the name of the task graph object to compare. Can be unqualified (resolved against the current database and schema) or fully qualified.

## Output

The function returns one row for each added, removed, or changed entity:

| Column Name | Data Type | Description |
| --- | --- | --- |
| ENTITY\_TYPE | TEXT | `TASK_GRAPH` for a change to the graph’s own properties, such as `SCHEDULE`, `FINALIZER`, or `TASK_DEFAULTS`. `TASK` for a change to a member task. |
| ENTITY\_NAME | TEXT | Name of the task graph or task that changed. |
| BEFORE | TEXT | DDL for the entity in the committed version. NULL if the entity was added. |
| AFTER | TEXT | DDL for the entity with its uncommitted changes. NULL if the entity was removed. |

Expand

Show lessSee more

## Usage notes

- The task graph must have been committed at least once. If it hasn’t, the function returns an
  error.
- Only entities you’re authorized to see are included; member tasks you don’t have privileges
  on are omitted from the comparison rather than causing an error.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA
  schema in use or the function name must be fully qualified. For
  more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Preview the uncommitted changes for a task graph before committing them:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(INFORMATION_SCHEMA.TASK_GRAPH_CHANGES(TASK_GRAPH_NAME => 'my_pipeline'));
> ```

List only the member tasks that changed:

> Copy code
>
> ```
> SELECT entity_name
>   FROM TABLE(INFORMATION_SCHEMA.TASK_GRAPH_CHANGES(TASK_GRAPH_NAME => 'my_db.my_schema.my_pipeline'))
>   WHERE entity_type = 'TASK';
> ```
