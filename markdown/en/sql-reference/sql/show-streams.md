# SHOW STREAMS

Lists the streams for which you have access privileges. The command can be used to list streams for the current/specified database
or schema, or across your entire account.

The output returns stream metadata and properties, ordered lexicographically by database, schema, and stream name (see [Output](#output)
in this topic for descriptions of the output columns). This is important to note if you wish to filter the results using the provided
filters.

See also:
:   [CREATE STREAM](/sql-reference/sql/create-stream) , [ALTER STREAM](/sql-reference/sql/alter-stream) , [DROP STREAM](/sql-reference/sql/drop-stream) , [DESCRIBE STREAM](/sql-reference/sql/desc-stream)

## Syntax

Copy code

```
SHOW [ TERSE ] STREAMS [ LIKE '<pattern>' ]
                       [ IN { ACCOUNT | DATABASE [ <db_name> ] | [ SCHEMA ] [ <schema_name> ] | APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> } ]
                       [ STARTS WITH '<name_string>' ]
                       [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind` (rename of `type` column in full set of columns)
    - `database_name`
    - `schema_name`
    - `tableOn` (rename of `table_name` column in full set of columns)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN ACCOUNT | [ DATABASE ] db_name | [ SCHEMA ] schema_name | APPLICATION application_name | APPLICATION PACKAGE application_package_name`
:   Specifies the scope of the command, which determines whether the command lists records only for the current/specified database or
    schema, or across your entire account:

    The `APPLICATION` and `APPLICATION PACKAGE` keywords are not required, but they specify the scope for the named Snowflake Native App.

    The `DATABASE` or `SCHEMA` keyword is not required; you can set the scope by specifying only the database or schema name.
    Likewise, the database or schema name is not required if the session currently has a database in use.

    - If `DATABASE` or `SCHEMA` is specified without a name and the session does not currently have a database in use, the
      parameter has no effect on the output.
    - If `SCHEMA` is specified with a name and the session does not currently have a database in use, the schema name must
      be fully qualified with the database name (e.g. `testdb.testschema`).

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the objects you have privileges to view in the database).
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

The command output provides stream properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the stream was created. |
| `name` | Name of the stream. |
| `database_name` | Database for the schema for the stream. |
| `schema_name` | Schema for the stream. |
| `owner` | Role that owns the stream. |
| `comment` | Comment for the stream. |
| `table_name` | Table whose DML updates are tracked by the stream. |
| `source_type` | Source object for the stream: table, view, directory table, or external table. |
| `base_tables` | Underlying tables for the view. This column applies to streams on views only. |
| `type` | Type of the stream; currently DELTA only. |
| `stale` | Indicates whether the stream was last read before the `stale_after` time (see below). If this is `TRUE`, the stream may be stale. When a stream is stale, it cannot be read. Recreate the stream to resume reading from it. To prevent a stream from becoming stale, consume the stream before `stale_after`. |
| `mode` | Displays `APPEND_ONLY` if the stream is an append-only stream.   Displays `INSERT_ONLY` if the stream only returns information for inserted rows; currently applies to streams on external tables only.   For streams on tables, the column displays `DEFAULT`. |
| `stale_after` | Timestamp when the stream became or may become stale if not consumed.     This value is calculated by adding the retention period for the source table (i.e. the larger of the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) or [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days) parameter setting) to the last time the stream was read. If the data retention period is set at the schema or database level, the current role and account must have access to the relevant object (schema, database, or shared tables/views) to obtain an accurate `stale_after` timestamp.     This time can be inaccurate in a few cases:   - Some time can elapse between when the stream is *permitted* to become stale and when the underlying data is actually dropped. During this period, `stale_after` will be in the past, but reading from the stream may succeed. The duration of this period is subject to change, so you should not depend on it.   - If parameters affecting table retention are increased, streams that are already stale will remain stale, but the `stale_after` time might be in the future. |
| `invalid_reason` | Reason why the stream cannot be queried successfully. This column supports future functionality. Currently, the only value returned is `N/A`. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

For more information about the properties that can be specified for a stream, see [CREATE STREAM](/sql-reference/sql/create-stream).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns source object names for which the current user’s current role has been granted at least one access privilege.
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

Show all the streams whose name starts with `line` that you have privileges to view in the `tpch.public` schema:

> Copy code
>
> ```
> SHOW STREAMS LIKE 'line%' IN tpch.public;
> ```
