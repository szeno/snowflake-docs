# SHOW TYPES

Lists the [user-defined types](/sql-reference/data-types-user-defined) for which you have access privileges.
Use this command to list the user-defined types for a specified schema or database, the current schema or
database for the session, or your entire account.

See also:
:   [CREATE TYPE](/sql-reference/sql/create-type) , [ALTER TYPE](/sql-reference/sql/alter-type) , [DESCRIBE TYPE](/sql-reference/sql/desc-type) , [DROP TYPE](/sql-reference/sql/drop-type) , [UNDROP TYPE](/sql-reference/sql/undrop-type)

## Syntax

Copy code

```
SHOW TYPES [ LIKE '<pattern>' ]
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
:   Optionally specifies the scope of the command. Specify one of the following parameters:

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

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

## Output

The command output provides user-defined type properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the user-defined type. |
| `type` | Snowflake type definition that is the base type for the user-defined type. |
| `created_on` | Date and time when the user-defined type was created. |
| `database_name` | Database in which the user-defined type is stored. |
| `schema_name` | Schema in which the user-defined type is stored. |
| `owner` | Name of the role that owns the user-defined type (that is, the role that has the OWNERSHIP privilege on the user-defined type). |
| `comment` | The comment set for the type, if any (otherwise `NULL`). |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | User-defined type |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

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

- Executing the command for schema-level objects only returns an object if the current role also has at least one privilege on the
  parent database and schema.

## Examples

Use the SHOW TYPES command to list details about the `age` user-defined type:

Copy code

```
SHOW TYPES LIKE 'age';
```

```
+------+-------------+-------------------------------+---------------+----------------+--------------+---------+
| name | type        | created_on                    | database_name | schema_name    | owner        | comment |
|------+-------------+-------------------------------+---------------+----------------+--------------+---------|
| AGE  | NUMBER(3,0) | 2025-10-28 09:09:43.279 -0700 | MY_DB         | MY_SCHEMA      | MY_ROLE      | NULL    |
+------+-------------+-------------------------------+---------------+----------------+--------------+---------+
```
