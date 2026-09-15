# SHOW OPENFLOW CONNECTOR DEFINITIONS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector), [DROP OPENFLOW CONNECTOR](/sql-reference/sql/drop-openflow-connector), [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors), [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector), [SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector)

Lists gen 2 connector definition IDs available in the account—the values used in
`FROM DEFINITION` when you `CREATE OPENFLOW CONNECTOR`. Each **gen 2** entry in the Openflow
connector catalog corresponds to one of these IDs.

## Syntax

Copy code

```
SHOW OPENFLOW CONNECTOR DEFINITIONS
  [ LIKE '<pattern>' ]
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

## Example

Copy code

```
SHOW OPENFLOW CONNECTOR DEFINITIONS LIKE '%POSTGRES%';
```

The `name` column in the output is the definition ID (for example, `OPENFLOW_POSTGRES_CDC`).

## Output

| Column | Description |
| --- | --- |
| `name` | Connector definition ID (for example, `OPENFLOW_POSTGRES_CDC`). |
| `provider` | Provider of the connector definition. |
| `version` | Version of the connector definition. |
| `description` | Brief description of what the connector does. |
| `display_name` | Display name shown in the Openflow connector catalog. |
| `categories` | JSON array of category tags. |
| `min_runtime_node_type` | Minimum runtime node type required to run this connector. |
| `max_node_count` | Maximum number of runtime nodes supported. |

Expand

Show lessSee more
