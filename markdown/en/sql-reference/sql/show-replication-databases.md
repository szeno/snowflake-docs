# SHOW REPLICATION DATABASES

Lists all the primary and secondary databases (that is to say, all the databases for which replication has been enabled) in your account
and indicates the [region](/user-guide/intro-regions) in which each account is located.

See also:
:   [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts)

## Syntax

Copy code

```
SHOW REPLICATION DATABASES [ LIKE '<pattern>' ]
                           [ WITH PRIMARY <account_identifier>.<primary_db_name> ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`WITH PRIMARY {account_identifier}.{primary_db_name}`
:   Specifies the scope of the command, which determines whether the command lists records only for the specified primary database.
    The `account_identifier` can be in the form `org_name.account_name` or `snowflake_region.account_locator`.
    See [Account identifiers for replication and failover](/user-guide/admin-account-identifier#label-account-identifier-for-replication) for details.

## Output

The command output provides primary and secondary database properties and metadata in the following columns. The command output for organizations that span multiple [region groups](/user-guide/admin-account-identifier#label-region-groups) includes an additional
`region_group` column.

| Column | Description |
| --- | --- |
| `region_group` | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account is located. **Note**: This column is only displayed for organizations that span multiple region groups. |
| `snowflake_region` | Snowflake Region where the account that stores the database is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| `created_on` | Date and time when the database was created. |
| `account_name` | Name of the account in which the database is stored. |
| `name` | Name of the database. |
| `comment` | Comment for the database. |
| `is_primary` | Whether the database is a primary database; otherwise, is a secondary database. |
| `primary` | Fully-qualified name of a primary database, including the region, account, and database name. |
| `replication_allowed_to_accounts` | Where `IS_PRIMARY` is TRUE, shows the fully-qualified names of accounts where replication has been enabled for this primary database. A secondary database can be created in each of these accounts. |
| `failover_allowed_to_accounts` | Where `IS_PRIMARY` is TRUE, shows the fully-qualified names of accounts where failover has been enabled for this primary database. A secondary database can be created in each of these accounts for business continuity and disaster recovery. |
| `organization_name` | Name of your Snowflake organization. |
| `account_locator` | Account locator in a region. |

Expand

Show lessSee more

## Usage notes

- Returns results for a role with any privilege on the database (for example, USAGE or MONITOR).

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

Show all the replication databases whose name starts with `mydb`:

Copy code

```
SHOW REPLICATION DATABASES LIKE 'mydb%';
```

Show all the secondary databases for the `myorg.account1.mydb1` org, account, and primary database, respectively:

Copy code

```
SHOW REPLICATION DATABASES WITH PRIMARY myorg.account1.mydb1;
```
