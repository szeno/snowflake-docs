# SHOW TASK GRAPHS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the [Task Graph Object](/user-guide/task-graph-object)s for which you have access privileges, surfacing graph-wide properties and `TASK_DEFAULTS`.

See also:
:   [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph), [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph), [DESCRIBE TASK GRAPH](/sql-reference/sql/desc-task-graph), [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks)

## Syntax

Copy code

```
SHOW TASK GRAPHS [ LIKE '<pattern>' ]
                 [ IN { ACCOUNT | DATABASE [ <db_name> ] | [ SCHEMA ] [ <schema_name> ] } ]
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

`IN ACCOUNT | DATABASE [ db_name ] | [ SCHEMA ] [ schema_name ]`
:   Optionally specifies the scope of the command: the current or specified database or schema, or your entire account.

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

The output returns graph metadata and graph-wide properties in the following columns:

| Column Name | Description |
| --- | --- |
| created\_on | Date and time when the graph was created. |
| name | Name of the graph. |
| id | Unique identifier for the graph. |
| database\_name | Database that contains the graph. |
| schema\_name | Schema that contains the graph. |
| comment | Comment for the graph. |
| owner | Role that owns the graph (that is, has the OWNERSHIP privilege on the graph). |
| owner\_role\_type | Type of the role that owns the graph, either `ROLE` or `DATABASE_ROLE`. |
| schedule | Schedule for periodically running the graph. NULL if no schedule is set. |
| state | Current state of the graph: `STARTED` or `SUSPENDED`. |
| task\_defaults | JSON object holding the graph’s `TASK_DEFAULTS`. NULL if none are set. |
| has\_pending\_changes | Whether the graph has staged changes that have not yet been committed. Compare against [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks) to see what would change on the next commit, or use [TASK\_GRAPH\_CHANGES](/sql-reference/functions/task_graph_changes) to preview the diff. |
| overlap\_policy | Overlap policy for graph runs. |
| config | Graph-level configuration string, if set. |
| success\_integration | Name of the notification integration used to send success notifications for the graph, if set. |
| error\_integration | Name of the notification integration used to send error notifications for the graph, if set. |
| last\_suspended\_on | Date and time when the graph was last suspended. NULL if the graph has never been suspended. |
| last\_suspended\_reason | Reason the graph was last suspended. NULL if the graph has never been suspended. |
| condition | Text of the `WHEN` condition for the graph, if set. |
| created\_by\_user | Name of the user who created the graph. NULL if the information isn’t available. |

Expand

Show lessSee more

## Usage notes

- [DESCRIBE TASK GRAPH](/sql-reference/sql/desc-task-graph) returns the same columns for a single graph.
- The command lists only the task graphs for which your role has at least one privilege, such as MONITOR.
- To see the member tasks in a graph’s committed version, use [SHOW COMMITTED TASKS](/sql-reference/sql/show-committed-tasks).

## Examples

Copy code

```
SHOW TASK GRAPHS IN SCHEMA;
SHOW TASK GRAPHS IN DATABASE my_db;
SHOW TASK GRAPHS IN ACCOUNT;
```
