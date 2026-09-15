# SHOW TAGS

Lists the tag information.

See also:
:   [CREATE TAG](/sql-reference/sql/create-tag) , [ALTER TAG](/sql-reference/sql/alter-tag) , [DROP TAG](/sql-reference/sql/drop-tag) , [UNDROP TAG](/sql-reference/sql/undrop-tag)

## Syntax

Copy code

```
SHOW TAGS [ LIKE '<pattern>' ]
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

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Schema | This privilege must match the schema containing the tag. |
| APPLY TAG | Account |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on tag DDL and privileges, see [Access control privileges](/user-guide/object-tagging/work#label-object-tags-privileges).

## Usage notes

- The ALLOWED\_VALUES column specifies the possible string values that can be assigned to the tag when the tag is set
  on an [object](/user-guide/object-tagging/introduction#label-object-tag-supported-objects) or NULL if the tag does not have any specified allowed values. For details, see
  [Set a list of allowed tag values](/user-guide/object-tagging/work#label-object-tagging-specify-tag-values).

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

Show tags in a given schema:

> Copy code
>
> ```
> SHOW TAGS IN SCHEMA my_db.my_schema;
> ```
>
> ```
> ------------------------------+----------------+---------------+-------------+--------------+--------------------+----------------+-----------------+
>                    created_on | name           | database_name | schema_name | owner        | comment            | allowed_values | owner_role_type |
> ------------------------------+----------------+---------------+-------------+--------------+--------------------+----------------+-----------------+
> 2021-03-20 21:09:38.317 +0000 | CLASSIFICATION | MY_DB         | MY_SCHEMA   | ACCOUNTADMIN | secure information | [NULL]         | ROLE            |
> 2021-03-20 21:08:59.000 +0000 | COST_CENTER    | MY_DB         | MY_SCHEMA   | ACCOUNTADMIN | cost_center tag    | [NULL]         | ROLE            |
> ------------------------------+----------------+---------------+-------------+--------------+--------------------+----------------+-----------------+
> ```
