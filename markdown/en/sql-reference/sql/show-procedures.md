# SHOW PROCEDURES

Lists all stored procedures that you have privileges to access, including built-in and user-defined procedures.

For a command that lists only user-defined procedures, see [SHOW USER PROCEDURES](/sql-reference/sql/show-user-procedures).

See also:
:   [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) , [CREATE PROCEDURE](/sql-reference/sql/create-procedure) , [DROP PROCEDURE](/sql-reference/sql/drop-procedure) , [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure)

## Syntax

Copy code

```
SHOW PROCEDURES [ LIKE '<pattern>' ]
  [ IN
    {
      ACCOUNT                                         |

      CLASS <class_name>                              |

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

- If you specify `CLASS`, the command only returns the following columns:

  ```
  | name | min_num_arguments | max_num_arguments | arguments | descriptions | language |
  ```

## Output

The command output provides procedure properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Timestamp at which the stored procedure was created. |
| `name` | Name of the stored procedure. |
| `schema_name` | Name of the schema in which the stored procedure exists. |
| `is_builtin` | `Y` if the stored procedure is built-in (rather than user-defined); `N` otherwise. |
| `is_aggregate` | Not applicable currently. |
| `is_ansi` | `Y` if the stored procedure is defined in the ANSI standard; `N` otherwise. |
| `min_num_arguments` | Minimum number of arguments. |
| `max_num_arguments` | Maximum number of arguments. |
| `arguments` | Data types of the arguments and of the return types. Optional arguments are displayed with the `DEFAULT` keyword. For [Snowflake Scripting stored procedures](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-arguments), `OUT` is displayed for output arguments. |
| `description` | Description of the stored procedure. |
| `catalog_name` | Name of the database in which the stored procedure exists. |
| `is_table_function` | `Y` if the stored procedure returns tabular data; `N` otherwise. |
| `valid_for_clustering` | Not applicable currently. |
| `is_secure` | `Y` if the stored procedure is a secure stored procedure; `N` otherwise. |

Expand

Show lessSee more

## Examples

Show all procedures:

Copy code

```
SHOW PROCEDURES;
```

This example shows how to use `SHOW PROCEDURE` on a stored procedure that has a parameter. This also shows how to limit the list of
procedures to those that match the specified regular expression.

Copy code

```
SHOW PROCEDURES LIKE 'area_of_%';
+-------------------------------+----------------+--------------------+------------+--------------+---------+-------------------+-------------------+------------------------------------+------------------------+-----------------------+-------------------+----------------------+-----------+
| created_on                    | name           | schema_name        | is_builtin | is_aggregate | is_ansi | min_num_arguments | max_num_arguments | arguments                          | description            | catalog_name          | is_table_function | valid_for_clustering | is_secure |
|-------------------------------+----------------+--------------------+------------+--------------+---------+-------------------+-------------------+------------------------------------+------------------------+-----------------------+-------------------+----------------------+-----------|
| 1967-06-23 00:00:00.123 -0700 | AREA_OF_CIRCLE | TEMPORARY_DOC_TEST | N          | N            | N       |                 1 |                 1 | AREA_OF_CIRCLE(FLOAT) RETURN FLOAT | user-defined procedure | TEMPORARY_DOC_TEST_DB | N                 | N                    | N         |
+-------------------------------+----------------+--------------------+------------+--------------+---------+-------------------+-------------------+------------------------------------+------------------------+-----------------------+-------------------+----------------------+-----------+
```

The output columns are similar to the output columns for [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and
[SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions). For stored procedures, some of these columns are not currently meaningful
(e.g. `is_aggregate`, `valid_for_clustering`), but are reserved for future use.
