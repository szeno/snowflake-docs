# SHOW AUTHENTICATION POLICIES

Lists [authentication policy](/user-guide/authentication-policies) information, including the creation date, database and
schema names, owner, and any available comments.

See also:
:   [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy), [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy), [DESCRIBE AUTHENTICATION POLICY](/sql-reference/sql/desc-authentication-policy), [DROP AUTHENTICATION POLICY](/sql-reference/sql/drop-authentication-policy)

## Syntax

Copy code

```
SHOW AUTHENTICATION POLICIES
  [ LIKE '<pattern>' ]
  [ IN
       {
         ACCOUNT                                         |

         DATABASE                                        |
         DATABASE <database_name>                        |

         SCHEMA                                          |
         SCHEMA <schema_name>                            |

         APPLICATION <application_name>                  |
         APPLICATION PACKAGE <application_package_name>  |
       }
    |
    ON
       {
         ACCOUNT           |
         USER <user_name>  |
       }
  ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> ]
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

`[ ON ... ]`
:   Lists the policies that are effective on the specified object. This command considers precedence.
    For example, listing policies on a user will show the account or built-in policy that is effective
    for the user if there is no policy set specifically on the user. Specify one of the following:

    `ACCOUNT`
    :   Returns policies effective on the account.

    `USER user_name`
    :   Returns policies effective on the specified user.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY AUTHENTICATION POLICY | Account | Only the SECURITYADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |
| OWNERSHIP | Authentication policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

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

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Output

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the authentication policy was created. |
| `name` | Name of the authentication policy. |
| `database_name` | Name of the database where the authentication policy was created. NULL for the built-in system policy. |
| `schema_name` | Name of the schema where the authentication policy was created. NULL for the built-in system policy. |
| `kind` | `AUTHENTICATION_POLICY` |
| `owner` | Role that owns the authentication policy. |
| `comment` | Comment that was defined for the authentication policy when it was created or altered. |
| `owner_role_type` | Role type of the owner. |
| `options` | For SHOW AUTHENTICATION POLICIES ON, details about how the policy is set. |
| `set_on` | For SHOW AUTHENTICATION POLICIES ON, the object type where the policy is set: USER, ACCOUNT, or SYSTEM. |

Expand

Show lessSee more

## Examples

The following example returns one authentication policy, which belongs to the current database and schema:

Copy code

```
SHOW AUTHENTICATION POLICIES;
```

```
+-------------------------------+------------------------------+---------------+----------------+-----------------------+--------------+---------------------------------------------------------------+-----------------+---------+
| created_on                    | name                         | database_name | schema_name    | kind                  | owner        | comment                                                       | owner_role_type | options |
|-------------------------------+------------------------------+---------------+----------------+-----------------------+--------------+---------------------------------------------------------------+-----------------+---------|
| 2025-09-10 16:38:57.530 -0700 | RESTRICT_CLIENT_TYPES_POLICY | CLIENTS_DB    | CLIENTS_SCHEMA | AUTHENTICATION_POLICY | CLIENTS_ROLE | Auth policy that only allows access through the web interface | ROLE            |         |
+-------------------------------+------------------------------+---------------+----------------+-----------------------+--------------+---------------------------------------------------------------+-----------------+---------+
```

The following example returns all of the authentication policies in the account:

Copy code

```
SHOW AUTHENTICATION POLICIES IN ACCOUNT;
```

```
+-------------------------------+------------------------------+---------------+----------------+-----------------------+--------------+---------------------------------------------------------------+-----------------+---------+
| created_on                    | name                         | database_name | schema_name    | kind                  | owner        | comment                                                       | owner_role_type | options |
|-------------------------------+------------------------------+---------------+----------------+-----------------------+--------------+---------------------------------------------------------------+-----------------+---------|
| 2025-09-10 16:38:57.530 -0700 | RESTRICT_CLIENT_TYPES_POLICY | CLIENTS_DB    | CLIENTS_SCHEMA | AUTHENTICATION_POLICY | CLIENTS_ROLE | Auth policy that only allows access through the web interface | ROLE            |         |
| 2025-06-25 13:37:11.092 -0700 | MULTIPLE_AUTH_MODES          | POLICY1_DB    | POLICY1_SCHEMA | AUTHENTICATION_POLICY | POLICY1_ROLE |                                                               | ROLE            |         |
+-------------------------------+------------------------------+---------------+----------------+-----------------------+--------------+---------------------------------------------------------------+-----------------+---------+
```
