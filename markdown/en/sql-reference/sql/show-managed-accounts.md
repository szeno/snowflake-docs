# SHOW MANAGED ACCOUNTS

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire about
enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists the managed accounts created for your account. Currently used by data providers to create reader accounts for their consumers. For
more details, see [Manage reader accounts](/user-guide/data-sharing-reader-create).

See also:
:   [CREATE MANAGED ACCOUNT](/sql-reference/sql/create-managed-account) , [DROP MANAGED ACCOUNT](/sql-reference/sql/drop-managed-account)

## Syntax

Copy code

```
SHOW MANAGED ACCOUNTS [ LIKE '<pattern>' ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

## Usage notes

- The command can be executed by users with the ACCOUNTADMIN role (or a role that has been granted the MONITOR USAGE global privilege).

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

## Output

The command output provides managed account properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `account_name` | Name of the account. |
| `cloud` | Cloud in which the managed account is located. For reader accounts, this is always the same as the cloud for the provider account. |
| `region` | Region in which the managed account is located. For reader accounts, this is always the same as the region for the provider account. |
| `account_locator` | Legacy identifier for the account. |
| `created_on` | Date and time when the managed account was created. |
| `account_url` | [Account URL](/user-guide/organizations-connect#label-connecting-via-url) that is used to connect to the account, in the account name format. The [account identifier](/user-guide/admin-account-identifier) in this format follows the pattern `<orgname>-<account_name>`. |
| `account_locator_url` | Account URL that is used to connect to the account, in the legacy account locator format. |
| `is_reader` | Specifies whether the managed account is a reader account (for sharing data). |
| `comment` | Comment for the managed account. |
| `region_group` | Region group in which the managed account is located. |
| `old_account_url` | If the original [account URL](/user-guide/organizations-connect#label-connecting-via-url) was saved when the account was renamed, provides the original URL. If the original account URL was dropped, the value is NULL even if the account was renamed. |
| `account_old_url_saved_on` | If the original account URL was saved when the account was renamed, provides the date and time when the original account URL was saved. |
| `account_old_url_last_used` | If the original account URL was saved when the account was renamed, indicates the last time the account was accessed using the original URL. |
| `organization_old_url` | If the account’s organization was changed in a way that created a new [account URL](/user-guide/organizations-connect#label-connecting-via-url) and the original account URL was saved, provides the original account URL. If the original account URL was dropped, the value is NULL even if the organization changed. |
| `organization_old_url_saved_on` | If the account’s organization was changed in a way that created a new account URL and the original account URL was saved, provides the date and time when the original account URL was saved. |
| `organization_old_url_last_used` | If the account’s organization was changed in a way that created a new account URL and the original account URL was saved, indicates the last time the account was accessed using the original account URL. |

Expand

Show lessSee more

## Examples

Copy code

```
SHOW MANAGED ACCOUNTS;
```

```
+--------------+-------+-----------+---------+-------------------------------+--------------------------------------------+----------------------------------------+-----------+---------+----------------+
| name         | cloud | region    | locator | created_on                    | url                                        |  account_locator_url                   | is_reader | comment |  region_group  |
|--------------+-------+-----------+---------+-------------------------------+--------------------------------------------+----------------------------------------+-----------+---------|----------------|
| ACCT1        | aws   | us-west-2 | RE47190 | 2018-05-30 14:38:54.479 -0700 | https://bazco-acct1.snowflakecomputing.com  |  https://re47190.snowflakecomputing.com | true    |         |     PUBLIC     |
+--------------+-------+-----------+---------+-------------------------------+--------------------------------------------+----------------------------------------+-----------+---------+----------------+
```
