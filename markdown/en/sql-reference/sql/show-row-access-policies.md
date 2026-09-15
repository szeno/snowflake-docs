# SHOW ROW ACCESS POLICIES

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists the row access policies for which you have access privileges. Returns information that includes the creation date, database and
schema names, owner, and any available comments.

See also:
:   [Row access policy DDL](/user-guide/security-row-intro#label-security-row-ddl)

## Syntax

Copy code

```
SHOW ROW ACCESS POLICIES [ LIKE '<pattern>' ]
                         [ LIMIT <rows> [ FROM '<name_string>' ] ]
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
| APPLY ROW ACCESS POLICY | Account |  |
| APPLY | Row access policy |  |
| OWNERSHIP | Row access policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on row access policy DDL and privileges, see [Manage row access policies](/user-guide/security-row-intro#label-security-row-mgmt-approach).

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

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example is representative of a user with the ACCOUNTADMIN role executing the query.

> Copy code
>
> ```
> SHOW ROW ACCESS POLICIES;
> ```
>
> ```
> +---------------------------------+------+---------------+-------------+-------------------+--------------+---------+---------+-----------------+
> |          created_on             | name | database_name | schema_name |       kind        |    owner     | comment | options | owner_role_type |
> |---------------------------------+------+---------------+-------------+-------------------+--------------+---------+---------+-----------------+
> | Fri, 23 Jun 1967 00:00:00 -0700  | P1   | RLS_AUTHZ_DB  | S_D_1       | ROW_ACCESS_POLICY | ACCOUNTADMIN |         | ""      | ROLE           |
> | Fri, 23 Jun 1967 00:00:00 -0700  | P2   | RLS_AUTHZ_DB  | S_D_2       | ROW_ACCESS_POLICY | ACCOUNTADMIN |         | ""      | ROLE           |
> +---------------------------------+------+---------------+-------------+-------------------+--------------+---------+---------+-----------------+
> ```

The following example is representative of a role that does not have USAGE on the parent schema in which row access policies exist and is
not the ACCOUNTADMIN role.

> Copy code
>
> ```
> SHOW ROW ACCESS POLICIES;
> ```
>
> ```
> +--------------------------------+------+---------------+-------------+-------------------+--------------+---------+---------+-----------------+
> |         created_on             | name | database_name | schema_name |       kind        |    owner     | comment | options | owner_role_type |
> |--------------------------------+------+---------------+-------------+-------------------+--------------+---------+---------+-----------------+
> +--------------------------------+------+---------------+-------------+-------------------+--------------+---------+---------+-----------------+
> ```
