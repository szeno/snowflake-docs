# SHOW USER PROCEDURES

Lists all user-defined procedures for which you have access privileges. Use this command to list the user-defined procedures for a specified
database or schema (or the current database/schema for the session), application, or for your entire account.

For a command that lists all procedures, including both built-in and user-defined procedures, see [SHOW PROCEDURES](/sql-reference/sql/show-procedures).

See also:
:   [SHOW PROCEDURES](/sql-reference/sql/show-procedures), [PROCEDURES view](/sql-reference/info-schema/procedures) (Information Schema),
    [PROCEDURES view](/sql-reference/account-usage/procedures) (Account Usage), [SHOW USER PROCEDURES](/sql-reference/sql/show-user-procedures)

## Syntax

Copy code

```
SHOW USER PROCEDURES [ LIKE '<pattern>' ]
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

The command output lists user procedure properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Timestamp at which the procedure was created. |
| `name` | Name of the procedure. |
| `schema_name` | Name of the schema in which the procedure exists. |
| `is_builtin` | `Y` if the procedure is built in; `N` otherwise (always `N` for user-created procedures). |
| `is_aggregate` | Not applicable currently. |
| `is_ansi` | Not applicable currently. |
| `min_num_arguments` | Minimum number of arguments to the procedure. |
| `max_num_arguments` | Maximum number of arguments to the procedure. |
| `arguments` | Data types of the arguments and return value. For [Snowflake Scripting stored procedures](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-arguments), `OUT` is displayed for output arguments. |
| `description` | Description of the procedure. |
| `catalog_name` | Name of the database in which the procedure exists. |
| `is_table_function` | `Y` if the procedure returns a table; `N` otherwise. |
| `valid_for_clustering` | `Y` if the procedure can be used in a CLUSTER BY expression; `N` otherwise. |
| `is_secure` | `Y` if the procedure is a secure procedure; `N` otherwise. |
| `secrets` | Map of [secret](/sql-reference/sql/create-secret) values specified by the procedure’s SECRETS parameter, where map keys are secret variable names and map values are secret object names. |
| `external_access_integrations` | Names of [external access integrations](/developer-guide/external-network-access/external-network-access-overview) specified by the procedure’s EXTERNAL\_ACCESS\_INTEGRATION parameter. |

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

Show procedures that you have privileges to view in the current schema whose names begin with `GET_`:

> Copy code
>
> ```
> SHOW USER PROCEDURES LIKE 'GET_%' IN SCHEMA;
> ```
>
> ```
> -------------------------------+-----------------+-------------+------------+--------------+---------+-------------------+-------------------+---------------------------------------+------------------------+--------------+-------------------+----------------------+-----------+---------+------------------------------+
>           created_on           | name            | schema_name | is_builtin | is_aggregate | is_ansi | min_num_arguments | max_num_arguments | arguments                             | description            | catalog_name | is_table_function | valid_for_clustering | is_secure | secrets | external_access_integrations |
> -------------------------------+-----------------+-------------+------------+--------------+---------+-------------------+-------------------+---------------------------------------+------------------------+--------------+-------------------+----------------------+-----------+---------+------------------------------+
>  2023-01-27 15:01:13.862 -0800 | GET_FILE        | PUBLIC      | N          | N            | N       | 1                 | 1                 | GET_FILE(VARCHAR) RETURN VARCHAR      | user-defined procedure | BOOKS_DB     | N                 | N                    | N         |         |                              |
>  2023-03-23 10:38:10.423 -0700 | GET_NUM_RESULTS | PUBLIC      | N          | N            | N       | 1                 | 1                 | GET_NUM_RESULTS(VARCHAR) RETURN FLOAT | user-defined procedure | BOOKS_DB     | N                 | N                    | N         |         |                              |
>  2023-03-23 09:47:55.840 -0700 | GET_RESULTS     | PUBLIC      | N          | N            | N       | 1                 | 1                 | GET_RESULTS(VARCHAR) RETURN TABLE ()  | user-defined procedure | BOOKS_DB     | Y                 | N                    | N         |         |                              |
> -------------------------------+-----------------+-------------+------------+--------------+---------+-------------------+-------------------+---------------------------------------+------------------------+--------------+-------------------+----------------------+-----------+---------+------------------------------+
> ```
