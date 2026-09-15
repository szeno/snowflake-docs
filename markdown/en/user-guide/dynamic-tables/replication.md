# Replication and failover behavior for dynamic tables

Dynamic tables can be replicated to secondary accounts for disaster recovery using failover groups
or replication groups. After failover, dynamic tables reinitialize on the promoted secondary. The refresh schedule, warehouse assignment, and definition are preserved.
After failover, the promoted dynamic table runs a full refresh against the current state of base objects on the secondary. Because replication lag may leave base tables at slightly different points in time, the reinitialized result might differ from the last-known state on the former primary.

## Failover groups and replication groups

Snowflake provides two group-based replication types:
[failover groups](/sql-reference/sql/create-failover-group) support promotion to primary, while
[replication groups](/sql-reference/sql/create-replication-group) provide read-only replication
without failover support.

| Behavior | Failover group | Replication group |
| --- | --- | --- |
| Dynamic tables refresh on secondary | No (read-only until promoted) | No (permanently read-only) |
| Supports failover/promotion | Yes | No |
| Reinitialization required after failover | Yes | N/A (failover not supported) |
| Edition requirement | Business Critical (or higher) | Standard (or higher) |

Expand

Show lessSee more

## Configure a failover group with dynamic tables

Place the dynamic table, its base tables, and all upstream dynamic tables in the same failover
group:

Copy code

```
CREATE FAILOVER GROUP myfg
  OBJECT_TYPES = DATABASES
  ALLOWED_DATABASES = analytics_db
  ALLOWED_ACCOUNTS = myorg.secondary_account
  REPLICATION_SCHEDULE = '10 MINUTE';
```

Warning

If a dynamic table references base objects outside the failover group, it can still be replicated. However, after failover, the dynamic table’s definition references whatever objects exist with the same names in the promoted account. If the referenced objects were not replicated (because they belong to a different database or group), the refresh fails with an object-not-found error.

After failover, dynamic tables on the promoted secondary reinitialize with a full refresh. The
definition, refresh schedule, and warehouse assignment carry over from the primary.

## Dynamic tables on read-only secondaries

While a secondary account remains a read-only replica, dynamic tables do not refresh. Data arrives
only through the replication schedule from the primary account.

Replicated dynamic tables on secondaries are automatically suspended with one of the following
scheduling state reason codes. These codes appear in the `scheduling_state` column of the
DYNAMIC\_TABLE\_GRAPH\_HISTORY table function output:

| Reason code | Meaning |
| --- | --- |
| `RG_REPLICA` | The dynamic table is a replica in a replication group. |
| `FG_REPLICA` | The dynamic table is a replica in a failover group. |
| `UPSTREAM_FG_REPLICA` | The dynamic table was suspended because an upstream dependency is a replica in a failover group. |

Expand

Show lessSee more

You can’t manually refresh a dynamic table on a read-only secondary. Attempting to do so returns
an error.

### Create dynamic tables downstream of replicated dynamic tables

After failover or when referencing a replicated dynamic table from a different database on the same
account, you can create a new dynamic table that reads from the replicated dynamic table. The
replicated table acts as a pipeline boundary, so the downstream dynamic table refreshes
independently from the upstream pipeline’s schedule.

## Monitor replicated dynamic tables

After a failover, use the following queries to check the state of your dynamic tables on the
promoted secondary.

Check the scheduling state for replication-specific suspension reasons:

Copy code

```
SELECT name, scheduling_state
  FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY());
```

```
+------------------+------------------+
| NAME             | SCHEDULING_STATE |
|------------------+------------------|
| DT_ORDERS       | SUSPENDED        |
| DT_ORDERS_DAILY | SUSPENDED        |
+------------------+------------------+
```

Check the refresh history for reinitialization events:

Copy code

```
SELECT name, refresh_action, refresh_trigger, state_message
  FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY())
  WHERE refresh_action = 'REINITIALIZE'
  ORDER BY data_timestamp DESC;
```

```
+------------------+----------------+-----------------+-------------------------------------+
| NAME             | REFRESH_ACTION | REFRESH_TRIGGER | STATE_MESSAGE                       |
|------------------+----------------+-----------------+-------------------------------------|
| DT_ORDERS       | REINITIALIZE   | SCHEDULED       | Reinitialize after database failover|
+------------------+----------------+-----------------+-------------------------------------+
```

## What’s next

- To understand how cloned dynamic tables behave after replication, see
  [Clone dynamic tables](/user-guide/dynamic-tables/cloning).
- To learn about suspend and resume behavior, including auto-suspension, see
  [Manage dynamic tables](/user-guide/dynamic-tables/manage).
- To share dynamic tables across accounts without replication, see
  [Share dynamic tables with other accounts](/user-guide/dynamic-tables/sharing).
