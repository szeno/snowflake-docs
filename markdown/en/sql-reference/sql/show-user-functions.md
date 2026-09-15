# SHOW USER FUNCTIONS

Lists all user-defined functions (UDFs) for which you have access privileges. Use this command to list the UDFs for a specified
database or schema (or the current database/schema for the session), or across your entire account.

For a command that lists all functions, including built-in functions, see [SHOW FUNCTIONS](/sql-reference/sql/show-functions).

See also:
:   [SHOW FUNCTIONS](/sql-reference/sql/show-functions), [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions), [FUNCTIONS view](/sql-reference/info-schema/functions) (Information Schema),
    [FUNCTIONS view](/sql-reference/account-usage/functions) (Account Usage)

## Syntax

Copy code

```
SHOW USER FUNCTIONS [ LIKE '<pattern>' ]
  [ IN
    {
      ACCOUNT                                         |

      DATABASE                                        |
      DATABASE <database_name>                        |

      SCHEMA                                          |
      SCHEMA <schema_name>                            |
      <schema_name>

      APPLICATION <application_name>                  |
      APPLICATION PACKAGE <application_package_name>  |
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

    `APPLICATION application_name`, `APPLICATION PACKAGE application_package_name`
    :   Returns records for the named Snowflake Native App or application package.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

## Output

The command output provides user function properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Timestamp at which the user-defined function (UDF) was created. |
| `name` | Name of the UDF. |
| `schema_name` | Name of the schema in which the UDF exists. |
| `is_builtin` | Always `N` for user-defined functions. See [SHOW FUNCTIONS](/sql-reference/sql/show-functions) for a command to list all functions, including built-in functions. |
| `is_aggregate` | `Y` if the function is an aggregate function; `N` otherwise. |
| `is_ansi` | Not applicable currently. |
| `min_num_arguments` | Minimum number of arguments to the UDF. |
| `max_num_arguments` | Maximum number of arguments to the UDF. |
| `arguments` | Data types of the arguments and return value. |
| `description` | Description of the UDF. |
| `catalog_name` | Name of the database in which the UDF exists. |
| `is_table_function` | `Y` if the UDF is a table function; `N` otherwise. |
| `valid_for_clustering` | `Y` if the UDF can be used in a CLUSTER BY expression; `N` otherwise. |
| `is_secure` | `Y` if the UDF is a secure UDF; `N` otherwise. |
| `secrets` | Map of [secret](/sql-reference/sql/create-secret) values specified by the function’s SECRETS parameter, where map keys are secret variable names and map values are secret object names. |
| `external_access_integrations` | Names of [external access integrations](/developer-guide/external-network-access/external-network-access-overview) specified by the function’s EXTERNAL\_ACCESS\_INTEGRATION parameter. |
| `is_external_function` | `Y` if the function is an external function; *N* otherwise. See [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions) for a command to list external functions. |
| `language` | Programming language of the UDF (for example, `PYTHON` or `SQL`). |
| `is_memoizable` | `Y` if the function is [memoizable](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable); `N` otherwise. |
| `is_data_metric` | `Y` if the function is a [data metric function](/user-guide/data-quality-intro); `N` otherwise. |

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

Show all the UDFs that you have privileges to view in the current database:

> Copy code
>
> ```
> SHOW USER FUNCTIONS LIKE 'ALLOWED_REGIONS%' IN SCHEMA;
> ```
>
> ```
> ---------------------------------+--------------------------+-------------+------------+--------------+---------+-------------------+-------------------+-----------------------------------------+-----------------------+----------------+-------------------+----------------------+-----------+---------+-----------------------------+----------------------+----------+---------------+----------------+
>           created_on             |           name           | schema_name | is_builtin | is_aggregate | is_ansi | min_num_arguments | max_num_arguments |                arguments                |      description      |  catalog_name  | is_table_function | valid_for_clustering | is_secure | secrets | external_access_integration | is_external_function | language | is_memoizable | is_data_metric |
> ---------------------------------+--------------------------+-------------+------------+--------------+---------+-------------------+-------------------+-----------------------------------------+-----------------------+----------------+-------------------+----------------------+-----------+---------+-----------------------------+----------------------+----------+---------------+----------------+
>  Fri, 23 Jun 1967 00:00:00 -0700 | ALLOWED_REGIONS          | PUBLIC      | N          | N            | N       | 0                 | 0                 | ALLOWED_REGIONS() RETURN ARRAY          | user-defined function | MEMO_FUNC_TEST | N                 | N                    | N         |         |                             | N                    | SQL      | Y             | N              |
>  Fri, 23 Jun 1967 00:00:00 -0700 | ALLOWED_REGIONS_NON_MEMO | PUBLIC      | N          | N            | N       | 0                 | 0                 | ALLOWED_REGIONS_NON_MEMO() RETURN ARRAY | user-defined function | MEMO_FUNC_TEST | N                 | N                    | N         |         |                             | N                    | SQL      | N             | N              |
> ---------------------------------+--------------------------+-------------+------------+--------------+---------+-------------------+-------------------+-----------------------------------------+-----------------------+----------------+-------------------+----------------------+-----------+---------+-----------------------------+----------------------+----------+---------------+----------------+
> ```
