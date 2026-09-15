# DROP FAILOVER GROUP

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups) from the account.

See also:
:   [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) , [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) , [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups)

## Syntax

Copy code

```
DROP FAILOVER GROUP [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the failover group.

## Usage notes

- Only an account administrator (user with the ACCOUNTADMIN role) or the group owner (role with the OWNERSHIP privilege on the group) can
  execute this SQL command.
- A primary failover group can only be successfully dropped if no linked secondary failover groups exist.
- A database that is included in a failover group is not dropped when the failover group is dropped.

  - If a secondary failover group is dropped, any database previously included in the group loses read-only protection and becomes writable.
  - If the secondary failover group is re-created from the same primary failover group as before, the databases in the group are
    overwritten by the databases in the primary failover group during the first refresh. These databases are read-only.
- To retrieve the set of accounts in your organization that are enabled for replication, use
  [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).
- To retrieve the list of failover groups in your organization, use [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups#label-show-failover-groups).

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

### Executed on source account

Drop a failover group named `myfg` in the source account.

Copy code

```
DROP FAILOVER GROUP IF EXISTS myfg;
```
