# Snowflake Postgres Read Replicas

## Overview

Snowflake Postgres supports creating *replicas*. Replicas are read-only copies
of a *leader instance* that are continually kept synchronized with changes from that
instance. This synchronization is done automatically and transparently to the user.

Replicas are useful for read scaling and offloading certain workloads that could
impact production (such as reporting workloads). Replicas are required to have
the same storage size as their leader but can have a different compute size.

Replicas are provisioned in the same network as their leader instance and, as a result,
inherit all ingress and egress network rules from their leader instance.

Postgres credentials, along with all other data on replicas, are copied and kept
synchronized with the leader instance. The replica inherits the leader’s authentication authority
when created. Separate Postgres access roles are created automatically for the replica; grants on the leader’s
access roles aren’t copied. Grant access using the replica’s qualified role name and generate tokens
for the replica’s instance name. See
[Access roles on replicas and forks](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-replicas-forks).

## Creating a Read Replica

SnowsightSQL

1. In the navigation menu, select **Postgres**.
2. Select the instance you want to create a replica of to load its detail page.
3. In the **Manage** menu at the top right of the detail page, select the *Create replica* option.
4. Make your choices for your new replica’s configuration options.

   ![Create a Snowflake Postgres Replica](/static/images/snowflake-postgres/snowflake-postgres-create-replica.png)
5. Select **Save** to create the replica.

To create a Postgres instance as a replica of an origin instance, specify the AS REPLICA OF clause in the CREATE POSTGRES INSTANCE command.
By default, the COMPUTE\_FAMILY and POSTGRES\_SETTINGS properties are copied from the original Postgres instance.
You can override those settings, and also specify COMMENT and TAG properties for the new instance.

One row with the following columns will be returned:

- `status`
- `host`

**CREATE REPLICA SQL Examples**

Create a replica `my_replica` of the instance `my_origin_instance`.

Copy code

```
CREATE POSTGRES INSTANCE my_replica
  AS REPLICA OF my_origin_instance;
```

Create a replica `my_replica` of the instance `my_origin_instance` with a different compute family.

Copy code

```
CREATE POSTGRES INSTANCE my_replica
  AS REPLICA OF my_origin_instance
  COMPUTE_FAMILY = STANDARD_M;
```

The time needed to create a replica depends on the size of its origin instance. The replica will
display its current state as it is building. See the list of
[instance states](#instance-states) for details about the states the replica will
pass through as it builds.

## Replica behavior and limitations

- Only **10 replicas** can stream changes from a leader instance by default. To allow additional replicas to stream, increase the Postgres `max_wal_senders` setting (see [Snowflake Postgres Server Settings](/user-guide/snowflake-postgres/postgres-server-settings)).
- Leader Postgres instances **cannot be dropped while they have replicas**. All replicas must be removed before the leader can be dropped.
- Postgres server settings applied to a leader instance are copied to all replicas.
- Enable, rename, disable, or drop Postgres access-role users on the leader. These changes
  propagate to replicas, which are read-only. Manage Snowflake grants separately for each
  replica’s access roles.
