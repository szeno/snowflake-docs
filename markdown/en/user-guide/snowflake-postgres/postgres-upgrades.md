# Snowflake Postgres version upgrades

Postgres uses an X.Y versioning scheme, with X being the major version and Y being the minor version within that major version.

## Postgres major version upgrades

Snowflake Postgres allows you to schedule your major version upgrades via an instance [Modify](/user-guide/snowflake-postgres/managing-instances#label-sfpg-modify) action, which requires
[failover maintenance](/user-guide/snowflake-postgres/postgres-maintenance#label-sfpg-maintenance-failover).

To initiate a major version upgrade, you must use a role that has been granted the OWNERSHIP or OPERATE privilege on the instance.

Note

You can only upgrade to a newer major version. You can’t downgrade to a previous major version.

You can combine a major version upgrade with an instance resize by selecting a new instance size,
storage size, or both along with the new version number.

Tip

Since upgrade maintenance failovers can take longer than other instance [Modify](/user-guide/snowflake-postgres/managing-instances#label-sfpg-modify) maintenance failovers (see below) and
you can’t downgrade an instance to a prior major version, Snowflake strongly recommends that you fully test major version upgrades
with a [Fork](/user-guide/snowflake-postgres/managing-instances#label-sfpg-fork) of your instance before proceeding with major version upgrades of active production instances.

SnowsightSQL

1. In the navigation menu, select **Postgres**.
2. Select your Snowflake Postgres instance.
3. In the **Manage** menu at the top right, select **Modify**.
4. If a newer version is available, you will be able to select it from the Postgres version dropdown menu.
5. Select the **Save** button to confirm the change.

![Modify a Snowflake Postgres instance with a major version upgrade](/static/images/snowflake-postgres/snowflake-pg-upgrade-version.png)

You can initiate a major version upgrade with the [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance) command by setting the POSTGRES\_VERSION parameter to the desired version.

This will upgrade an instance named `my_instance` to Postgres 18:

Copy code

```
ALTER POSTGRES INSTANCE my_instance
  SET POSTGRES_VERSION = 18;
```

To have the upgrade proceed as soon as the upgrade replacement instance is ready, regardless of the currently set maintenance window:

Copy code

```
ALTER POSTGRES INSTANCE my_instance
  SET POSTGRES_VERSION = 18
  APPLY IMMEDIATELY;
```

This will both upgrade the instance to Postgres 18 and change its storage size to 100GB:

Copy code

```
ALTER POSTGRES INSTANCE my_instance
  SET POSTGRES_VERSION = 18
      STORAGE_SIZE_GB = 100;
```

Let’s say today’s date is March 18, 2026, and you want to have the upgrade maintenance failover happen tomorrow at 10pm:

Copy code

```
ALTER POSTGRES INSTANCE my_instance
  SET POSTGRES_VERSION = 18
  APPLY ON '2026-03-19 22:00:00';
```

Note

If you have no maintenance window set, and have not specified a run time with `APPLY ON '<timestamp>'` when creating the upgrade action
via SQL, the upgrade maintenance failover will proceed as soon as the new instance is populated and ready, just as when using
APPLY IMMEDIATELY when creating the upgrade action via SQL.

When using `APPLY ON '<timestamp>` to schedule the upgrade maintenance failover for a specified future time, that time can be at most
three days from the current time.

### How major version upgrade maintenances work

Postgres major version upgrades work differently than other instance management operations. Once you initiate the process, Snowflake Postgres
will execute the following steps:

1. Just as with other [Modify](/user-guide/snowflake-postgres/managing-instances#label-sfpg-modify) actions, a hidden replica is provisioned for the upgrade.
2. When the scheduled maintenance time arrives:

   - The current primary instance is locked to prevent writes.
   - The hidden replica is upgraded using [pg\_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html). The duration depends
     on the *number of objects* in your database, not data size.
3. Fail over to the newly upgraded instance once the upgrade is complete.

**Important Notes**:

- Major Version changes can affect application compatibility. We recommend testing your application against the new PostgreSQL version
  before upgrading.
- Read Replicas can’t have their major versions upgraded separately from their primary instances. Instead they are automatically
  upgraded when performing a major version upgrade on their primary, but only once their primary is upgraded and a fresh backup is taken. Until then, replicas will remain available but in a stale state.
- HA instances (if present) are also automatically upgraded after their primary is upgraded and a fresh backup is taken. Until then, the
  primary will not have a valid HA instance present.
- The service interruption from the maintenance failover will be longer than that required for other [Modify](/user-guide/snowflake-postgres/managing-instances#label-sfpg-modify) actions, but
  should typically last no longer than a few minutes.
- If an upgrade fails, your instance will automatically revert back to the original instance.

## Postgres minor version upgrades

Snowflake will automatically upgrade your database with new minor versions of Postgres over time.

With each Postgres release we examine all security related issues and bugs. For any deemed critical, we will prioritize your upgrade to
ensure that your data is safe. If an emergency update is required, we’ll perform that update during your maintenance window.

For non-critical fixes we gradually update databases by one of the following:

- Updating your instance during Instance Management operations that require instance replacement, such as resource changes
- Updating your High Availability standby after an HA failover. If an HA failover occurs the newly build HA instance will receive
  the latest point release.

An instance [Refresh](/user-guide/snowflake-postgres/managing-instances#label-sfpg-refresh) will also ensure your instance and HA instance (if present) will be upgraded to the latest available minor
version.
