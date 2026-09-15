# SHOW ORGANIZATION ACCOUNTS

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists the [organization account](/user-guide/organization-accounts) of the organization.

Important

Previously, this command was used to list all accounts in the organization, but has been repurposed to list the organization account. If
you want to list all accounts in the organization, use [SHOW ACCOUNTS](/sql-reference/sql/show-accounts).

See also:
:   [CREATE ORGANIZATION ACCOUNT](/sql-reference/sql/create-organization-account), [ALTER ORGANIZATION ACCOUNT](/sql-reference/sql/alter-organization-account)

## Syntax

Copy code

```
SHOW ORGANIZATION ACCOUNTS [ LIKE '<pattern>' ]
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

- Only users with the GLOBALORGADMIN role can run this command, which means it can only be run from the organization account.

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

## Output

The command output provides global account properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `organization_name` | Name of the organization. |
| `account_name` | User-defined name that identifies an account within the organization. |
| `region_group` | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account is located. **Note**: This column is only displayed for organizations that span multiple region groups. |
| `snowflake_region` | Snowflake Region where the account is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| `edition` | [Snowflake Edition](/user-guide/intro-editions) of the account. |
| `account_url` | Preferred Snowflake account URL that includes the values of organization\_name and account\_name. |
| `created_on` | Date and time when the account was created. |
| `comment` | Comment for the account. |
| `account_locator` | System-assigned identifier of the account. |
| `account_locator_url` | Legacy Snowflake account URL syntax that includes the region\_name and account\_locator. |
| `managed_accounts` | Indicates how many [managed accounts](/user-guide/data-sharing-reader-create) have been created by the account. |
| `consumption_billing_entity_name` | Name of the consumption billing entity. |
| `marketplace_consumer_billing_entity_name` | Name of the marketplace consumer billing entity. |
| `marketplace_provider_billing_entity_name` | Name of the marketplace provider billing entity. |
| `old_account_url` | If the original [account URL](/user-guide/organizations-connect#label-connecting-via-url) was saved when the account was renamed, provides the original URL. If the original account URL was dropped, the value is NULL even if the account was renamed. |
| `is_org_admin` | Indicates whether the ORGADMIN role is enabled in an account. If TRUE, the role is enabled. |
| `account_old_url_saved_on` | If the original account URL was saved when the account was renamed, provides the date and time when the original account URL was saved. |
| `account_old_url_last_used` | If the original account URL was saved when the account was renamed, indicates the last time the account was accessed using the original URL. |
| `organization_old_url` | If the account’s organization was changed in a way that created a new [account URL](/user-guide/organizations-connect#label-connecting-via-url) and the original account URL was saved, provides the original account URL. If the original account URL was dropped, the value is NULL even if the organization changed. |
| `organization_old_url_saved_on` | If the account’s organization was changed in a way that created a new account URL and the original account URL was saved, provides the date and time when the original account URL was saved. |
| `organization_old_url_last_used` | If the account’s organization was changed in a way that created a new account URL and the original account URL was saved, indicates the last time the account was accessed using the original account URL. |
| `is_events_account` | Indicates whether an account is an events account. For more information, see [Use logging and event tracing for an app](/developer-guide/native-apps/event-about). |
| `is_organization_account` | Indicates whether an account is the [organization account](/user-guide/organization-accounts). |

Expand

Show lessSee more

## Examples

Show information about the organization account:

Copy code

```
SHOW ORGANIZATION ACCOUNTS;
```
