# SHOW FAILOVER GROUPS

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists the primary and secondary [failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups) in your account,
as well as the failover groups in other accounts that are associated with your account.

For the other accounts:

- Lists the primary failover groups enabled for replication and failover to this account.
- Lists the secondary failover groups linked to groups in this account.

See also:
:   [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) , [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) , [DROP FAILOVER GROUP](/sql-reference/sql/drop-failover-group)

## Syntax

Copy code

```
SHOW FAILOVER GROUPS [ IN ACCOUNT <account> ]
```

## Parameters

`account`
:   Specifies the identifier for the account. Account name is a unique identifier within your organization. For more details about account
    name, see [Format 1 (preferred): Account name in your organization](/user-guide/admin-account-identifier#label-account-name).

## Usage notes

- Executing this command requires a role with any one of the following privileges on a failover group:

  - FAILOVER
  - MONITOR
  - OWNERSHIP
  - REPLICATE
- The output of SHOW FAILOVER GROUPS only includes groups of type `FAILOVER`.

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

The command returns the following columns:

| Column | Description |
| --- | --- |
| `region_group` | Region group where the account is located. **Note:** this column is only visible to organizations that span multiple [Region groups](/user-guide/admin-account-identifier#label-region-groups). |
| `snowflake_region` | Snowflake Region where the account is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| `created_on` | Date and time failover group was created. |
| `account_name` | Name of the account. |
| `name` | Name of the failover group. |
| `type` | Type of group. Valid value is `FAILOVER`. |
| `comment` | Comment string. |
| `is_primary` | Indicates whether the failover group is the primary group. |
| `primary` | Name of the primary group. |
| `object_types` | List of specified object types enabled for replication and failover. |
| `allowed_integration_types` | A list of integration types that are enabled for replication.  Snowflake always includes this column in the output even if integrations were not specified in the CREATE FAILOVER GROUP or ALTER FAILOVER GROUP command. |
| `allowed_accounts` | List of accounts enabled for replication and failover. |
| `organization_name` | Name of your Snowflake organization. |
| `account_locator` | Account locator in a region. |
| `replication_schedule` | Scheduled interval for refresh; NULL if no replication schedule is set. |
| `secondary_state` | Current state of scheduled refresh. Valid values are `started` or `suspended`. NULL if no replication schedule is set. |
| `next_scheduled_refresh` | Date and time of the next scheduled refresh. |
| `owner` | Name of the role with the OWNERSHIP privilege on the failover group. NULL if the failover group is in a different region. |
| `is_listing_auto_fulfillment_group` | TRUE if the replication group is used for [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment). FALSE otherwise. |
| `is_optimized_refresh_enabled` | [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all Business Critical Edition (or higher) accounts.  TRUE if [optimized refresh](/user-guide/account-replication-config#label-optimized-refresh) is enabled for the failover group. FALSE otherwise. When TRUE, subsequent refreshes for the group run as optimized refresh; when FALSE, they run as Replication Classic. |

Expand

Show lessSee more

## Examples

List failover groups in account `myaccount1`.

Copy code

```
SHOW FAILOVER GROUPS IN ACCOUNT myaccount1;

+------------------+-------------------------------+--------------+------+----------+---------+------------+-----------------------+---------------------------------------------+---------------------------+----------------------------------------------+-------------------+-------------------+----------------------+-----------------+-------------------------------+------------+-----------------------------------+
| snowflake_region | created_on                    | account_name | name | type     | comment | is_primary | primary               | object_types                                | allowed_integration_types |  allowed_accounts                            | organization_name | account_locator   | replication_schedule | secondary_state | next_scheduled_refresh        | owner      | is_listing_auto_fulfillment_group |
+------------------+-------------------------------+--------------+------+----------+---------+------------+-----------------------+---------------------------------------------+---------------------------+----------------------------------------------+-------------------+-------------------+----------------------+-----------------+-------------------------------+------------+-----------------------------------+
| AWS_US_EAST_1    | 2021-10-25 19:08:15.209 -0700 | MYACCOUNT1   | MYFG | FAILOVER |         | true       | MYORG.MYACCOUNT1.MYFG | DATABASES, ROLES, USERS, WAREHOUSES, SHARES |                           | MYORG.MYACCOUNT1.MYFG,MYORG.MYACCOUNT2.MYFG  | MYORG             | MYACCOUNT1LOCATOR | 10 MINUTE            | NULL            |                               | MYROLE     | false                             |
+------------------+-------------------------------+--------------+------+----------+---------+------------+-----------------------+---------------------------------------------+---------------------------+----------------------------------------------+-------------------+-------------------+----------------------+-----------------+-------------------------------+------------+-----------------------------------+
| AWS_US_WEST_2    | 2021-10-25 19:08:15.209 -0700 | MYACCOUNT2   | MYFG | FAILOVER |         | false      | MYORG.MYACCOUNT1.MYFG |                                             |                           |                                              | MYORG             | MYACCOUNT2LOCATOR | 10 MINUTE            | STARTED         | 2022-03-06 12:10:35.280 -0800 | NULL       | false                             |
+------------------+-------------------------------+--------------+------+----------+---------+------------+-----------------------+---------------------------------------------+---------------------------+----------------------------------------------+-------------------+-------------------+----------------------+-----------------+-------------------------------+------------+-----------------------------------+
```
