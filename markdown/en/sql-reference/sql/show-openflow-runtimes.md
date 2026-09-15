# SHOW OPENFLOW RUNTIMES

See also:
:   [CREATE OPENFLOW RUNTIME](/sql-reference/sql/create-openflow-runtime), [ALTER OPENFLOW RUNTIME](/sql-reference/sql/alter-openflow-runtime), [DROP OPENFLOW RUNTIME](/sql-reference/sql/drop-openflow-runtime), [DESCRIBE OPENFLOW RUNTIME](/sql-reference/sql/desc-openflow-runtime)

Lists gen 2 runtimes for which you have access privileges. The command can list runtimes for the
current or specified database or schema, or across your account. Output is ordered lexicographically
by database, schema, and runtime name.

## Syntax

Copy code

```
SHOW OPENFLOW RUNTIMES
  [ LIKE '<pattern>' ]
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

`IN ACCOUNT | [ DATABASE ] db_name | [ SCHEMA ] schema_name`
:   Specifies the scope of the command:

    - `ACCOUNT` — runtimes across the account that you can access.
    - `DATABASE` or `DATABASE db_name` — runtimes in the current or specified database.
    - `SCHEMA` or `SCHEMA schema_name` — runtimes in the current or specified schema. If the session has
      no database in use, qualify the schema name (`db_name.schema_name`).

    Default: `DATABASE` when a database is in use; otherwise `ACCOUNT`.

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

To list runtimes in one deployment, filter on the `deployment` column in the result set. `IN DEPLOYMENT` is not supported.

## Output

The command output provides runtime properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Runtime identifier. |
| `status` | `CREATING`, `ACTIVE`, `SUSPENDED`, `TERMINATED`, and other states. |
| `deployment` | Parent deployment name. |
| `min_nodes` | Minimum autoscaling bound. |
| `max_nodes` | Maximum autoscaling bound. |
| `node_type` | `SMALL`, `MEDIUM`, or `LARGE`. The node type, set at creation. |
| `node_type_tier` | Current instance tier. One of: `S1`, `S2`, `S3` (SMALL node type), `M4`, `M6` (MEDIUM node type), `L8` (LARGE node type). |
| `display_name` | UI display name. |
| `external_access_integrations` | External access integration names (Snowflake deployments). |
| `initially_suspended` | Whether the runtime was created in a suspended state. |
| `database_name` | Containing database. |
| `schema_name` | Containing schema. |
| `execute_as_role` | Execute-as role bound to the runtime. Connectors that use `SNOWFLAKE_MANAGED` authentication run with this role’s privileges. |
| `key` | Internal identifier for the runtime. |
| `owner` | Role that owns the runtime. |
| `comment` | Comment for the runtime. |
| `created_on` | Date and time when the runtime was created. |
| `updated_on` | Date and time when the runtime was last updated. |

Expand

Show lessSee more

## Usage notes

- Results are scoped to the privileges available in your current session. If you don’t see an
  expected runtime, verify that the role you’re using (or one of your active secondary roles)
  has been granted at least one privilege on the object. To check whether any of your granted
  roles can see it, run `USE SECONDARY ROLES ALL` and retry the query.
