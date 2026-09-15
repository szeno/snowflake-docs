# Snowflake Postgres logical replication

Snowflake Postgres allows you to set up logical replication to or from an external source. This may be useful for maintaining a local copy
of your data, an on-premises replica, or streaming data to external analytics, ETL, or change data capture (CDC) platforms.

The following are the default settings for logical replication on your instance and each of these can be adjusted as needed for your
instances by [customizing these configuration parameters](/user-guide/snowflake-postgres/p/managing-instances#custom-configuration-parameters):

Copy code

```
wal_level = logical
max_wal_senders = 10
max_replication_slots = 10
max_logical_replication_workers = 4
```

Using the [`snowflake_admin`](/user-guide/snowflake-postgres/postgres-roles#label-postgres-snowflake-admin-role) role, you can set up
logical replication publications and subscriptions and create replication slots. See more in the [Postgres documentation about logical replication](https://www.postgresql.org/docs/current/logical-replication.html).

Tip

Be sure to also check your instance’s [networking permissions](/user-guide/snowflake-postgres/postgres-network) to and/or from your
external sources or destinations when configuring logical replication.

## Logical replication failover

Snowflake Postgres supports [logical replication failover](https://www.postgresql.org/docs/current/logical-replication-failover.html) for
logical replication subscribers of Snowflake Postgres instances acting as logical replication publisher nodes under the following conditions:

- The Snowflake Postgres publisher node is a primary instance. Logical replication failover with read replicas acting as logical
  replication publisher nodes is not supported by Postgres.
- The Snowflake Postgres publisher primary instance is on Postgres 17 or later.
- If the subscriber was created with Postgres’s [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/current/sql-createsubscription.html),
  it must have been created using the `failover = true` option.
  - To migrate a pre-existing subscription to a failover-enabled subscription, use this process:

Copy code

```
ALTER SUBSCRIPTION subname DISABLE;
ALTER SUBSCRIPTION subname SET (failover = true);
ALTER SUBSCRIPTION subname ENABLE;
```

- Replication slots for non-Postgres subscribers created with [`pg_create_logical_replication_slot()`](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-REPLICATION)
  must use the function’s `failover := true` option. Subscribers using logical replication slots that were not created with that option must
  be rebuilt with a new slot using that option for logical replication failover to work.
- With the above requirements met, logical replication failover will work for:
  - [Postgres major version upgrades](/user-guide/snowflake-postgres/postgres-upgrades), but you must disable the subscription before
    finalizing the upgrade and re-enable it when the upgrade is complete.
  - [Refresh](/user-guide/snowflake-postgres/managing-instances#refresh) and [Modify](/user-guide/snowflake-postgres/managing-instances#modify)
    failovers.
  - Availability failovers on primary instances that have [high availability](/user-guide/snowflake-postgres/high-availability) enabled.
    If a primary instance without high availability enabled experiences an availability issue that requires replacement, the logical
    replication subscription will not survive intact.

Tip

For more about how logical replication failover works in Postgres, see the [Postgres documentation on logical replication failover](https://www.postgresql.org/docs/current/logical-replication-failover.html).
