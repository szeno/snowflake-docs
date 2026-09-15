# SHOW EVENT TABLES

Lists the [event tables](/developer-guide/logging-tracing/event-table-setting-up) for which you have access privileges, including
dropped tables that are still within the Time Travel retention period and, therefore, can be undropped. The command can be used to list
event tables for the current/specified database or schema, or across your entire account.

The output returns table metadata and properties, ordered lexicographically by database, schema, and event table name (see
[Output](#output) in this topic for descriptions of the output columns). This is important to note if you wish to filter the results using
the provided filters.

See also:
:   [CREATE EVENT TABLE](/sql-reference/sql/create-event-table), [ALTER TABLE (event tables)](/sql-reference/sql/alter-table-event-table), [DROP TABLE](/sql-reference/sql/drop-table),
    [UNDROP TABLE](/sql-reference/sql/undrop-table)

    [TABLES view](/sql-reference/info-schema/tables) (Information Schema)

## Syntax

Copy code

```
SHOW [ TERSE ] EVENT TABLES [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE [ <db_name> ] | SCHEMA [ <schema_name> ] } ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Optionally returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `database_name`
    - `schema_name`

    Default: No value (all columns are included in the output)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN ACCOUNT | DATABASE [ db_name ] | SCHEMA [ schema_name ]`
:   Optionally specifies the scope of the command, which determines whether the command lists records only for the current/specified database or schema, or across your entire account.

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the objects you have privileges to view in the current
      database).
    - No database: `ACCOUNT` is the default (i.e. the command returns the objects you have privileges to view in your account).

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

The command output provides table properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the event table was created. |
| `name` | Name of the event table. |
| `database_name` | Database in which the event table is stored. |
| `schema_name` | Schema in which the event table is stored. |
| `owner` | Role that owns the event table. |
| `comment` | Comment for the event table. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

For more information about the properties that can be specified for an event table, see [CREATE EVENT TABLE](/sql-reference/sql/create-event-table).

## Usage notes

- If an account (or database or schema) has a large number of event tables, then searching the entire account (or table or schema)
  can consume a significant amount of compute resources.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Show all the event tables whose name starts with `mylogs` that you have privileges to view in the `tpch.public`
schema:

> Copy code
>
> ```
> SHOW EVENT TABLES LIKE 'mylogs%' IN tpch.public;
> ```
