# SHOW COMMITTED TASKS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the tasks in the **committed version** of one or more
[task graphs](/user-guide/task-graph-object): the definitions that run.
[SHOW TASKS](/sql-reference/sql/show-tasks) shows the latest definitions,
including changes that haven’t been committed yet.

See also:
:   [DESCRIBE COMMITTED TASK](/sql-reference/sql/desc-committed-task), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs), [SHOW TASKS](/sql-reference/sql/show-tasks), [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph)

## Syntax

Copy code

```
SHOW COMMITTED TASKS [ LIKE '<pattern>' ]
                     [ IN { GRAPH <graph_name> | ACCOUNT | DATABASE [ <db_name> ] | [ SCHEMA ] [ <schema_name> ] } ]
                     [ STARTS WITH '<name_string>' ]
                     [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN GRAPH graph_name`
:   Lists the committed tasks of the specified task graph.

`IN ACCOUNT | DATABASE [ db_name ] | [ SCHEMA ] [ schema_name ]`
:   Lists the committed tasks of every task graph in the current or specified database or schema, or in your entire account.

    Default: `DATABASE` if the session has a current database; otherwise `ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

| Column | Description |
| --- | --- |
| created\_on | Date and time when the task was created. |
| name | Name of the task. |
| id | Unique identifier for the task. |
| database\_name | Database that contains the task. |
| schema\_name | Schema that contains the task. |
| owner | Role that owns the task. |
| owner\_role\_type | Type of the role that owns the task, either `ROLE` or `DATABASE_ROLE`. |
| graph\_id | Unique identifier for the task graph that the committed version belongs to. |
| graph\_name | Name of the task graph that the committed version belongs to. |
| version | Committed version of the graph that this row describes. |
| comment | Comment for the task. |
| warehouse | Warehouse that provides compute for the task. NULL for serverless tasks. |
| predecessors | JSON array of the fully qualified names of the task’s predecessors. |
| definition | SQL statement that the task runs. |
| condition | Text of the task’s `WHEN` condition, if set. |
| task\_relations | JSON object describing the task’s relationships. See [SHOW TASKS](/sql-reference/sql/show-tasks#label-show-tasks-output). |
| scheduling\_mode | Reserved. See [SHOW TASKS](/sql-reference/sql/show-tasks#label-show-tasks-output). |
| target\_completion\_interval | Target completion interval for serverless tasks, if set. |
| execute\_as\_user | User that the task runs as, if set with `EXECUTE AS USER`. |
| task\_parameters | JSON object holding the task’s parameter values, including those inherited from `TASK_DEFAULTS`. |
| graph\_version\_created\_by\_user | Name of the user who committed this version of the graph. NULL if the information isn’t available. |
| created\_by\_user | Name of the user who created the task. NULL if the information isn’t available. |

Expand

Show lessSee more

The output has no `state` column. A task graph’s state is shown by
[SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs).

## Usage notes

- If a task’s row here differs from its row in `SHOW TASKS`, the task has
  changes that haven’t been committed. To list them, use
  [TASK\_GRAPH\_CHANGES](/sql-reference/functions/task_graph_changes).

## Examples

Copy code

```
-- The committed tasks of one graph
SHOW COMMITTED TASKS IN GRAPH my_pipeline;

-- Broader scopes
SHOW COMMITTED TASKS IN SCHEMA;
SHOW COMMITTED TASKS IN DATABASE my_db;
SHOW COMMITTED TASKS IN ACCOUNT;
```
