# SHOW CLASSES

Lists all available classes.

See also:
:   [SHOW FUNCTIONS](/sql-reference/sql/show-functions) , [SHOW PROCEDURES](/sql-reference/sql/show-procedures) , [SHOW ROLES](/sql-reference/sql/show-roles)

    [Snowflake classes](/sql-reference/snowflake-db-classes)

## Syntax

Copy code

```
SHOW CLASSES [ LIKE '<pattern>' ]
             [ IN DATABASE [ <db_name> ] ]
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

`IN DATABASE db_name`
:   Specifies the scope of the command, which determines whether the command lists records only for the current/specified database or
    across your entire account.

    The `DATABASE` keyword is not required; you can set the scope by specifying only the database name. Likewise, the database name
    is not required if the session currently has a database in use.

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

## Usage notes

- The `owner` and `owner_role_type` columns don’t return a value.

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

Show all classes in the Snowflake database:

Copy code

```
SHOW CLASSES IN DATABASE SNOWFLAKE;

+-------------------------------+-----------------------+---------------+-------------+---------+---------+-------+------------------+-----------------+
| created_on                    | name                  | database_name | schema_name | version | comment | owner | is_service_class | owner_role_type |
|-------------------------------+-----------------------+---------------+-------------+---------+---------+-------|------------------|-----------------+
| 2023-04-17 11:48:31.222 -0700 | ANOMALY_DETECTION     | SNOWFLAKE     | ML          | NULL    | NULL    |       | false            |                 |
| 2023-05-26 10:01:24.852 -0700 | FORECAST              | SNOWFLAKE     | ML          | NULL    | NULL    |       | false            |                 |
+-------------------------------+-----------------------+---------------+-------------+---------+---------+-------+------------------+-----------------+
```
