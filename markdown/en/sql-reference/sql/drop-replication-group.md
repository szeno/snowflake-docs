# DROP REPLICATION GROUP

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups) from the account.

See also:
:   [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group) , [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group) , [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups)

## Syntax

Copy code

```
DROP REPLICATION GROUP [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the replication group.

## Usage notes

- Only a user with a role with the OWNERSHIP privilege on the group can execute this SQL command.
- A primary replication group can only be successfully dropped if no linked secondary replication groups exist.
- A database that is included in a replication group is not dropped when the replication group is dropped.

  - If a secondary replication group is dropped, any database previously included in the group loses read-only protection and becomes writable.
  - If the secondary replication group is re-created from the same primary replication group as before, the databases in the group are
    overwritten by the databases in the primary replication group during the first refresh. These databases are read-only.
- To retrieve the set of accounts in your organization that are enabled for replication, use
  [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).
- To retrieve the list of replication groups in your organization, use [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups). The
  `allowed_accounts` column lists all target accounts enabled for object replication from a source account.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop the replication group `myrg`:

Copy code

```
DROP REPLICATION GROUP myrg;
```
