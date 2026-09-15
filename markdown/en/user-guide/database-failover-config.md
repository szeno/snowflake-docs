# Failing over databases across multiple accounts

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

This topic describes the steps necessary to fail over your replicated databases across multiple accounts in different [regions](/user-guide/intro-regions) for disaster recovery.

Note

- Only account administrators (users with the ACCOUNTADMIN role) can enable and manage failover for a database.
- Snowflake recommends using the [account replication feature](/user-guide/account-replication-intro) to failover
  databases. [Replication and failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups) enable replication of
  multiple databases and other account objects with point-in-time consistency. Failover groups additionally enable
  failing over a collection of objects as a unit. For a full list of
  [feature availability](/user-guide/account-replication-intro#label-account-replication-feature-availability)
  and [supported objects](/user-guide/account-replication-intro#label-replicated-objects), refer to [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

## Use Snowsight for database replication and failover/failback

Attention

Managing and monitoring replication and failover/failback in Snowsight are only available to accounts
using private connectivity.

For all other accounts, see [Use Snowsight to monitor replication](/user-guide/account-replication-monitor#label-monitor-replication-in-ui) and [Replicating account objects and databases](/user-guide/account-replication-config#label-replication-config).

Account administrators (users with the ACCOUNTADMIN role) can manage replication and failover/failback actions in Snowsight.

See [Web interface for database replication and failover/failback](/user-guide/db-replication-config#label-db-replication-config-ui) for instructions on promoting a local database to serve as the primary database.

## Account identifier for replication and failover SQL commands

The example SQL statements in the instructions below use an [account identifier](/user-guide/admin-account-identifier) in the format,
`organization_name.account_name`. However, account identifiers in the format `snowflake_region.account_locator` are supported.

For more details, see [Account identifiers for replication and failover](/user-guide/admin-account-identifier#label-account-identifier-for-replication).

## Prerequisite requirements

1. Enable replication for a primary database in a set of accounts.
2. Create at least one secondary database (i.e. replica) of the primary database in one or more of the accounts specified in Step 1, and regularly refresh (i.e. synchronize) the replica with the latest updates to the primary database.

For instructions, see [Replicating databases across multiple accounts](/user-guide/db-replication-config).

## Step 1: Viewing all accounts enabled for replication

Query [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) to view the list of accounts in your organization in which replication has been enabled.

Copy code

```
SHOW REPLICATION ACCOUNTS;
```

```
+------------------+---------------------------------+---------------+------------------+---------+-------------------+
| snowflake_region | created_on                      | account_name  | account_locator  | comment | organization_name |
|------------------+---------------------------------+---------------+------------------+---------+-------------------|
| AWS_US_WEST_2    | 2018-11-19 16:11:12.720 -0700   | ACCOUNT1      | MYACCOUNT1       |         | MYORG             |
| AWS_US_EAST_1    | 2019-06-02 14:12:23.192 -0700   | ACCOUNT2      | MYACCOUNT2       |         | MYORG             |
+------------------+---------------------------------+---------------+------------------+---------+-------------------+
```

See the complete list of [Region IDs](/user-guide/admin-account-identifier#label-snowflake-region-ids).

## Step 2: Enabling failover for a primary database

Note

Skip this step if you enabled failover for this primary database in [Replicating databases across multiple accounts](/user-guide/db-replication-config).

Enable failover for a primary database to one or more accounts in your organization using an [ALTER DATABASE … ENABLE FAILOVER TO ACCOUNTS](/sql-reference/sql/alter-database) statement. The replica of this primary database in any one of these accounts (i.e. a secondary database) can be promoted to serve as the primary database.

Note that enabling failover for a primary database can be done either before or after a replica of the primary database has been created in a specified account.

### Example

Enable failover for primary database `mydb1` to accounts `myaccount2` and `myaccount3`. In this example, suppose the primary database
is stored in the `myaccount1` account and all three accounts belong to the organization, `myorg`. The ALTER DATABASE command must be
executed from `myaccount1`.

Copy code

```
ALTER DATABASE mydb1 ENABLE FAILOVER TO ACCOUNTS myorg.myaccount2, myorg.myaccount3;
```

## Step 3: Promoting a replica database to serve as the primary database

Any replica of a primary database can be promoted to serve as the primary database by executing an [ALTER DATABASE … PRIMARY](/sql-reference/sql/alter-database) statement. When promoted, the database becomes writeable. At the same time, the previous primary database becomes a read-only replica database.

Execute the `ALTER DATABASE` statement in the account containing the secondary database that you are promoting.

Note

To promote a secondary database, the role used to perform the operation must have the OWNERSHIP privilege on the database.

### Example

Promote a secondary database to serve as the primary database.

Copy code

```
ALTER DATABASE mydb1 PRIMARY;
```

Verify that the former secondary database was promoted successfully.

Copy code

```
SHOW REPLICATION DATABASES;
```
