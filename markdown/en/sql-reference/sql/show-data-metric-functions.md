# SHOW DATA METRIC FUNCTIONS

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists the [data metric functions](/user-guide/data-quality-intro) (DMFs) for which you have access privileges.

You can use this command to list the DMFs in the current database and schema for the session, a specified database or
schema, or your entire account.

See also:
:   [CREATE DATA METRIC FUNCTION](/sql-reference/sql/create-data-metric-function) , [ALTER FUNCTION (DMF)](/sql-reference/sql/alter-function-dmf), [DESCRIBE FUNCTION (DMF)](/sql-reference/sql/desc-function-dmf) , [DROP FUNCTION (DMF)](/sql-reference/sql/drop-function-dmf)

## Syntax

Copy code

```
SHOW DATA METRIC FUNCTIONS
  [ LIKE '<pattern>' ]
  [ IN
      {
        ACCOUNT                  |

        DATABASE                 |
        DATABASE <database_name> |

        SCHEMA                   |
        SCHEMA <schema_name>     |
        <schema_name>
      }
  ]
  [ STARTS WITH '<name_string>' ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

## Output

The command output provides DMF properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Timestamp at which the function was created. |
| `name` | Name of the function. |
| `schema_name` | Name of the schema that the function exists in. NULL for built-in functions. |
| `is_builtin` | `Y` if the function is a built-in function; `N` otherwise. |
| `is_aggregate` | `Y` if the function is an aggregate function; `N` otherwise. |
| `is_ansi` | `Y` if the function is defined as part of the ANSI SQL standard; `N` otherwise. |
| `min_num_arguments` | Minimum number of arguments. |
| `max_num_arguments` | Maximum number of arguments. |
| `arguments` | Shows the data types of the arguments and of the return value. |
| `description` | Description of the function. |
| `catalog_name` | Name of the database that the function exists in. NULL for built-in functions. |
| `is_table_function` | `Y` if the function is a table function; `N` otherwise. |
| `valid_for_clustering` | `Y` if the function can be used in a CLUSTER BY expression; `N` otherwise. |
| `is_secure` | `Y` if the function is a secure function; `N` otherwise. |
| `is_external_function` | `Y` if the function is an external function; `N` otherwise. |
| `language` | - For built-in functions, this column shows `SQL`. - For user-defined functions, this column shows the language in which the function was written, such as `JAVASCRIPT` or `SQL`. See [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions). - For external functions, this column shows `EXTERNAL`. |
| `is_memoizable` | `Y` if the function is memoizable; `N` otherwise. |
| `is_data_metric` | `Y` if the function is a DMF; `N` otherwise. |

Expand

Show lessSee more

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Data metric function |  |

Expand

Show lessSee more

## Usage notes

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example lists the DMFs that you have the privileges to view in the `dmfs` schema of the
`governance` database:

Copy code

```
USE SCHEMA governance.dmfs;

SHOW DATA METRIC FUNCTIONS;
```

```
+--------------------------+------------------------+-------------+------------+--------------+---------+-------------------+-------------------+--------------------------------------------------------------------------------------------+-----------------------+--------------+-------------------+----------------------+-----------+----------------------+----------+---------------+----------------+
| created_on               | name                   | schema_name | is_builtin | is_aggregate | is_ansi | min_num_arguments | max_num_arguments | arguments                                                                                  | description           | catalog_name | is_table_function | valid_for_clustering | is_secure | is_external_function | language | is_memoizable | is_data_metric |
+--------------------------+------------------------+-------------+------------+--------------+---------+-------------------+-------------------+--------------------------------------------------------------------------------------------+-----------------------+--------------+-------------------+----------------------+-----------+----------------------+----------+---------------+----------------+
| 2023-12-11T23:30:02.785Z | COUNT_POSITIVE_NUMBERS | DMFS        | N          | N            | N       | 1                 | 1                 | "COUNT_POSITIVE_NUMBERS(TABLE(NUMBER, NUMBER, NUMBER)) RETURNS NUMBER"                     | user-defined function | GOVERNANCE   | N                 | N                    | N         | N                    | SQL      | N             | Y              |
+--------------------------+------------------------+-------------+------------+--------------+---------+-------------------+-------------------+--------------------------------------------------------------------------------------------+-----------------------+--------------+-------------------+----------------------+-----------+----------------------+----------+---------------+----------------+
```
