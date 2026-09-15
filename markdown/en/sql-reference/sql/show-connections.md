# SHOW CONNECTIONS

[Business Critical Feature](/user-guide/intro-editions)

This command is part of the [client redirect](/user-guide/client-redirect) feature.
It requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You use client redirect in combination with the
[account replication](/user-guide/account-replication-intro) feature
for business continuity and disaster recovery.

Lists the [connections](/user-guide/client-redirect) for which you have access privileges.

The output returns connection metadata and properties, ordered by connection name (see [Output](#output) in this topic for descriptions of the
output columns). This is important to note if you intend to filter the results using the provided filters.

See also:
:   [CREATE CONNECTION](/sql-reference/sql/create-connection) , [ALTER CONNECTION](/sql-reference/sql/alter-connection) , [DROP CONNECTION](/sql-reference/sql/drop-connection)

## Syntax

Copy code

```
SHOW CONNECTIONS [ LIKE '<pattern>' ]
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

The command output provides connection properties and metadata in the following columns. The command output for organizations that span multiple [region groups](/user-guide/admin-account-identifier#label-region-groups) includes an additional
`region_group` column.

| Column | Description |
| --- | --- |
| `region_group` | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account is located. **Note**: This column is only displayed for organizations that span multiple region groups. |
| `snowflake_region` | Snowflake Region where the account is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| `created_on` | Date and time when the connection was created. |
| `account_name` | Name of the account. An organization administrator can change the account name. |
| `name` | Name of the connection. |
| `comment` | Comment for the connection. |
| `is_primary` | Indicates whether the connection is a primary connection. |
| `primary` | Organization name, account name, and connection name of the primary connection. This value can be copied into the AS REPLICA OF clause of the [CREATE CONNECTION](/sql-reference/sql/create-connection) command when creating secondary connections. |
| `failover_allowed_to_accounts` | A list of any accounts that the primary connection can redirect to. |
| `connection_url` | Connection URL that users pass to a client to establish a connection to Snowflake. |
| `organization_name` | Name of your Snowflake organization. |
| `account_locator` | Account locator in a region. |

Expand

Show lessSee more

For more information about the properties that can be specified for a connection, see [CREATE CONNECTION](/sql-reference/sql/create-connection).

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

Show all the connections whose name starts with `test`:

> Copy code
>
> ```
> SHOW CONNECTIONS LIKE 'test%';
> ```
