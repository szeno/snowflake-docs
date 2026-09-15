# SHOW REPLICATION ACCOUNTS

Lists all the accounts in your organization that are enabled for replication and indicates the [region](/user-guide/intro-regions) in
which each account is located.

Note

Use this SQL command instead of [SHOW GLOBAL ACCOUNTS](/sql-reference/sql/show-global-accounts), which is deprecated.

See also:
:   [SHOW REPLICATION DATABASES](/sql-reference/sql/show-replication-databases)

## Syntax

Copy code

```
SHOW REPLICATION ACCOUNTS [ LIKE '<pattern>' ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

## Output

The command output provides replication account properties and metadata in the following columns. The command output for organizations that span multiple [region groups](/user-guide/admin-account-identifier#label-region-groups) includes an additional
`region_group` column.

| Column | Description |
| --- | --- |
| `region_group` | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account is located. **Note**: This column is only displayed for organizations that span multiple region groups. |
| `snowflake_region` | Snowflake Region where the account is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| `created_on` | Date and time when the account was created. |
| `account_name` | Account name in your organization. |
| `account_locator` | Account locator in a region. |
| `comment` | Comment for the account. |
| `organization_name` | Name of your Snowflake organization. |
| `is_org_admin` | Indicates whether the ORGADMIN role is enabled in an account. If TRUE, the role is enabled. |

Expand

Show lessSee more

## Usage notes

- Only account administrators (users with the ACCOUNTADMIN role) can execute this SQL command.
- Returns results only when an account administrator (user with the ACCOUNTADMIN role) executes the command in a replication-enabled
  account.

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

Show all the global accounts whose name starts with `myaccount`:

Copy code

```
SHOW REPLICATION ACCOUNTS LIKE 'myaccount%';
```
