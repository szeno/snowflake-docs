# Notebook replication

Feature — Generally Available

- Notebook replication requires Standard Edition (SE) or later.
- Failover and failback require Business Critical Edition or later. To inquire about upgrading, please contact [Snowflake Support](/user-guide/contacting-support).

Replication supports business continuity in case of disasters, outages, or unavailability by making notebooks and other important objects available across accounts. A replication group, configured by an administrator, replicates account objects and databases from a primary account to one or more secondary accounts on a defined schedule.

Notebooks are replicated when they are part of a database included in a replication or failover group. In the secondary account, replicated content is read-only; notebooks are executable but cannot be edited.

Database replication can be configured as a failover group to support high availability. When a secondary failover group is promoted to primary, all contained objects, including notebooks, become writable in the new primary account.

For more information, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

## Enable replication

A user with the ORGADMIN role must enable replication for each source and target account in the organization:

Copy code

```
USE ROLE ORGADMIN;
SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER(
    '<organization_name>.<account_name>',
    'ENABLE_ACCOUNT_DATABASE_REPLICATION',
    'true');
```

For more information, see [Prerequisite: Enable replication for accounts in the organization](/user-guide/account-replication-config#label-enabling-accounts-for-replication).

## Create a replication group in the primary account

To replicate a notebook, specify the database that contains the notebook in the replication group:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE REPLICATION GROUP myrg
    OBJECT_TYPES = DATABASES
    ALLOWED_DATABASES = db1
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

In this example:

- `ALLOWED_DATABASES` - the name of the database that contains the notebook.
- `ALLOWED_ACCOUNTS` - the secondary account to replicate to.
- `REPLICATION_SCHEDULE` - how frequently replication occurs (for example, ’10 MINUTE’ or ’1 HOUR’).

### Replicate a warehouse

To run a replicated notebook as intended in the secondary account, any associated objects such as warehouses, EAIs, and tasks must be replicated or recreated separately.

To replicate a warehouse, include the warehouse in the OBJECT\_TYPES parameter in the replication/failover group.

Copy code

```
-- Create a new warehouse if required
CREATE WAREHOUSE IF NOT EXISTS mywarehouse
  WAREHOUSE_SIZE = 'X-SMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  COMMENT = 'Warehouse for Snowflake Notebooks';

-- Set up warehouse replication
CREATE REPLICATION GROUP mywarehouserg
  OBJECT_TYPES = WAREHOUSES
  ALLOWED_ACCOUNTS = myorg.myaccount2
  REPLICATION_SCHEDULE = '10 MINUTE';
```

For more information on syntax and options, see [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group#label-replication-group-single-database).

## Secondary account behavior

In a secondary account, you can create new notebooks only in non-replicated databases. These notebooks are not included in the replication group and are fully read-write.

Replicated notebooks are read-only. However, users can change associated compute resources and external access integrations (EAIs). These resources must be created or replicated separately. If they are not available, the notebook will not have those resources attached.

Create a replication group in the target account as a replica of the replication group `myrg` in the source account:

Copy code

```
CREATE REPLICATION GROUP myrg
    AS REPLICA OF myorg.myaccount1.myrg;
```

You can also create a replication group for warehouses if necessary. Note that all warehouses in the account will be replicated:

Copy code

```
CREATE REPLICATION GROUP mywarehouserg
    AS REPLICA OF myorg.myaccount1.mywarehouserg;
```

The replication group can also be [refreshed manually](/sql-reference/sql/alter-replication-group#label-executed-from-the-target-account) by running the following command:

Copy code

```
ALTER REPLICATION GROUP myrg REFRESH;
```

## Create a failover group

To allow promotion of the secondary account to primary during an outage, use a failover group:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE FAILOVER GROUP myfg
  OBJECT_TYPES = DATABASES
  ALLOWED_DATABASES = db1
  ALLOWED_ACCOUNTS = myorg.myaccount2
  REPLICATION_SCHEDULE = '10 MINUTE';
```

In this example, `ALLOWED_DATABASES` is the database to be created in the failover group. The replicated notebook in the failover group is read-only, but still executable. If you [promote the failover group to primary](/user-guide/account-replication-failover-failback#label-replication-promote-failover-group), the notebook becomes read-write.

## Considerations

- Scheduled notebooks in a secondary account are paused until failover. After failover, scheduling resumes.
- For replication and task behavior, see [Replication considerations](/user-guide/account-replication-considerations#label-replication-and-tasks).
- Notebook results are only stored in the account where the notebook was run. Notebook results are not replicated.

## Limitations

- Git integration is not currently supported after failover. For notebooks in a promoted secondary account to be able to reconnect to Git, you must reconfigure Git.

### Container Runtime notebooks

Notebooks that use Container Runtime are not fully replicated. Specifically, compute pools are not replicated and must be created manually in the secondary account.

To run a Container Runtime notebook in the secondary account:

1. Identify the compute pool used in the source account.
2. Create a compute pool with the same name and configuration in the secondary account:
   For example, if a replicated notebook references a compute pool named `compute_pool`, create that compute pool in the secondary account:

Copy code

```
-- In the secondary account, create a new compute pool with a matching name and configuration

CREATE COMPUTE POOL compute_pool
  MIN_NODES = 1
  MAX_NODES = 10
  INSTANCE_FAMILY = CPU_X64_XS;
```

Once created, the replicated notebook can use the compute pool to run in the secondary account.
