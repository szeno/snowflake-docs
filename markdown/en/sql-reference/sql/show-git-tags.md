# SHOW GIT TAGS

Lists the tags in the specified Snowflake [Git repository clone](/developer-guide/git/git-overview).

See also:
:   [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository), [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository), [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository), [DROP GIT REPOSITORY](/sql-reference/sql/drop-git-repository),
    [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches), [SHOW GIT REPOSITORIES](/sql-reference/sql/show-git-repositories)

## Syntax

Copy code

```
SHOW GIT TAGS [ LIKE '<pattern>' ] IN [ GIT REPOSITORY ] <repository_name>
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN [ GIT REPOSITORY ] repository_name`
:   Specifies the Git repository clone containing the tags to show.

## Output

The command output provides Git tags properties in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the tag. |
| `path` | Path of the tag. |
| `commit_hash` | Commit hash of the tag. |
| `author` | Author of the tag. |
| `message` | Commit message for the tag. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| READ | Git repository | Git repository clone containing the tags to show |

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

The following example lists tags in the Git repository clone `snowflake_extensions`.

Copy code

```
SHOW GIT TAGS IN snowflake_extensions;
```

The preceding command generates output such as the following:

```
-----------------------------------------------------------------------------------------------------------------------------------------------
| name    | path          | commit_hash                              | author                                     | message                   |
-----------------------------------------------------------------------------------------------------------------------------------------------
| example | /tags/example | 16e262d401297cd097d5d6c266c80ff9f7e1e4be | Gladys Kravits (gladyskravits@example.com) | Example code for preview. |
-----------------------------------------------------------------------------------------------------------------------------------------------
```
