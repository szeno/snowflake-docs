# SHOW GIT REPOSITORIES

Lists the [Git repository clones](/developer-guide/git/git-overview) that you have privileges to access.

The [SHOW STAGES](/sql-reference/sql/show-stages) command also lists Snowflake Git repositories. In the SHOW STAGES output, a Snowflake Git
repository has the value `GIT REPOSITORY` in its `type` column.

See also:
:   [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository), [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository), [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository), [DROP GIT REPOSITORY](/sql-reference/sql/drop-git-repository),
    [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches), [SHOW GIT TAGS](/sql-reference/sql/show-git-tags)

## Syntax

Copy code

```
SHOW GIT REPOSITORIES [ LIKE '<pattern>' ]
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

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Output

The command output provides Git repository clone properties in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date the Git repository clone was created. |
| `name` | Name of the Git repository clone. |
| `database_name` | Name of the database containing this Git repository clone. |
| `schema_name` | Name of the schema containing this Git repository clone. |
| `origin` | URL of the remote Git repository’s origin. |
| `api_integration` | Name of the API integration included in this Git repository clone. |
| `git_credentials` | Name of the secret object in this Git repository clone. |
| `owner` | Role used when this Git repository clone was created. |
| `owner_role_type` | Type of role that owns the object, either ROLE or DATABASE\_ROLE. |
| `comment` | Comment specified when this Git repository clone was created. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Git repository | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | Schema |  |

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

## Examples

The following example lists repositories in the current schema.

Copy code

```
SHOW GIT REPOSITORIES;
```

The preceding command generates output such as the following:

```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| CREATED_ON                    | NAME                 | DATABASE_NAME | SCHEMA_NAME | ORIGIN                                                  | API_INTEGRATION     | GIT_CREDENTIALS              | OWNER        | OWNER_ROLE_TYPE | COMMENT |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-06-28 08:46:10.886 -0700 | SNOWFLAKE_EXTENSIONS | MY_DB         | MAIN        | https://github.com/my-account/snowflake-extensions.git  | GIT_API_INTEGRATION | MY_DB.MAIN.EXTENSIONS_SECRET | ACCOUNTADMIN | ROLE            |         |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-06-28 08:46:10.886 -0700 | SNOWFLAKE_AI         | MY_DB         | MAIN        | https://github.com/my-account/snowflake-AI.git          | GIT_API_INTEGRATION | MY_DB.MAIN.AI_SECRET         | ACCOUNTADMIN | ROLE            |         |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
