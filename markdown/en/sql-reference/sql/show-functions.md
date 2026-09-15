# SHOW FUNCTIONS

Lists all functions that you have privileges to access, including built-in, user-defined, and external functions.

For a command that lists only user-defined functions, see [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions).

See also:
:   [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) , [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions) , [SHOW FUNCTIONS IN MODEL](/sql-reference/sql/show-functions-in-model) , [CREATE FUNCTION](/sql-reference/sql/create-function) , [DROP FUNCTION](/sql-reference/sql/drop-function) , [ALTER FUNCTION](/sql-reference/sql/alter-function) ,
    [DESCRIBE FUNCTION](/sql-reference/sql/desc-function)

## Syntax

Copy code

```
SHOW FUNCTIONS [ LIKE '<pattern>' ]
  [ IN
    {
      ACCOUNT                       |

      CLASS <class_name>            |

      DATABASE                      |
      DATABASE <database_name>      |

      SCHEMA                        |
      SCHEMA <schema_name>          |
      <schema_name>
    }
  ]
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

    `CLASS class_name`
    :   Returns records for the specified class (`class_name`).

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully-qualified `schema_name` (e.g. `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

## Output

The command output provides function properties and metadata in the following columns:

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

## Usage notes

- If you specify `CLASS`, the command only returns the following columns:

  ```
  | name | min_num_arguments | max_num_arguments | arguments | descriptions | language |
  ```

- The output of this command might include objects with names like `SN_TEMP_OBJECT_n` (where `n` is a number). These are
  temporary objects that are created by the [Snowpark](/developer-guide/snowpark/index) library on behalf of the user.

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

Show all functions:

Copy code

```
SHOW FUNCTIONS;
```

Show only functions matching the specified regular expression:

Copy code

```
SHOW FUNCTIONS LIKE 'SQUARE';
```

```
------------+--------+-------------+------------+--------------+---------+-------------------+-------------------+----------------------------------------------------------------------+------------------------------------------------------------+----------+---------------+----------------+
 created_on | name   | schema_name | is_builtin | is_aggregate | is_ansi | min_num_arguments | max_num_arguments |                               arguments                              |                      description                           | language | is_memoizable | is_data_metric |
------------+--------+-------------+------------+--------------+---------+-------------------+-------------------+----------------------------------------------------------------------+------------------------------------------------------------+----------+---------------+----------------+
            | SQUARE |             | Y          | N            | Y       | 1                 | 1                 | SQUARE(NUMBER(38,0)) RETURN NUMBER(38,0), SQUARE(FLOAT) RETURN FLOAT | Compute the square of the input expression.                | SQL      | N             | N              |
------------+--------+-------------+------------+--------------+---------+-------------------+-------------------+----------------------------------------------------------------------+------------------------------------------------------------+----------+---------------+----------------+
```
