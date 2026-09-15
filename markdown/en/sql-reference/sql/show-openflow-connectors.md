# SHOW OPENFLOW CONNECTORS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector), [DROP OPENFLOW CONNECTOR](/sql-reference/sql/drop-openflow-connector), [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions), [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector), [SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector)

Lists gen 2 connectors for which you have access privileges. The command can list connectors for
the current or specified database or schema, or across your account. Output is ordered
lexicographically by database, schema, and connector name.

## Syntax

Copy code

```
SHOW OPENFLOW CONNECTORS
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

    - `ACCOUNT` — connectors across the account that you can access.
    - `DATABASE` or `DATABASE db_name` — connectors in the current or specified database.
    - `SCHEMA` or `SCHEMA schema_name` — connectors in the current or specified schema. If the session
      has no database in use, qualify the schema name (`db_name.schema_name`).

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

To list connectors in one runtime, filter the `SHOW` result on the runtime column (for example,
query the result set with `->>`).

## Output

The command output provides connector properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Connector identifier. |
| `status` | Current lifecycle state. |
| `runtime` | Parent runtime name. |
| `connector_definition` | Name of the connector definition the connector was created from, such as `OPENFLOW_POSTGRES_CDC`. |
| `display_name` | UI display name. |
| `database_name` | Containing database. |
| `schema_name` | Containing schema. |
| `owner` | Role that owns the connector. |
| `default_version` | Default version setting for the connector, such as `LAST`. Set it with `ALTER OPENFLOW CONNECTOR ... SET DEFAULT_VERSION`. |
| `default_version_name` | Version that `default_version` currently resolves to, such as `VERSION$4`. Empty if the connector has no committed version. |
| `default_version_alias` | Alias of the default version, if one is assigned. |
| `default_version_location_uri` | Stage URI of the default version contents. |
| `default_version_source_location_uri` | Stage URI the default version was created from, if it was added from a stage. |
| `live_version_location_uri` | Stage URI of the writable live version. |
| `comment` | Comment for the connector. |
| `created_on` | Date and time when the connector was created. |
| `updated_on` | Date and time when the connector was last updated. |
| `connector_url` | URL of the connector canvas in the Openflow UI. |

Expand

Show lessSee more

## Usage notes

- Results are scoped to the privileges available in your current session. If you don’t see an
  expected connector, verify that the role you’re using (or one of your active secondary roles)
  has been granted at least one privilege on the object. To check whether any of your granted
  roles can see it, run `USE SECONDARY ROLES ALL` and retry the query.
