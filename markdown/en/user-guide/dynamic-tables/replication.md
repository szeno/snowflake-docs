# Replication and failover behavior for dynamic tables

Dynamic tables can be replicated to secondary accounts for disaster recovery using failover groups
or replication groups. After failover, the first refresh on the promoted secondary can be a full refresh, a
reinitialization, or an incremental refresh. The refresh schedule, warehouse assignment, and definition are
preserved. For the eligibility criteria that determine which outcome applies, see
[Continuing incremental refresh after failover](#label-continue-incremental-refresh-eligibility).

When reinitialization does happen, the promoted dynamic table runs a full refresh against the current state of base objects on the secondary. Because replication lag may leave base tables at slightly different points in time, the reinitialized result might differ from the last-known state on the former primary.

## Failover groups and replication groups

Snowflake provides two group-based replication types:
[failover groups](/sql-reference/sql/create-failover-group) support promotion to primary, while
[replication groups](/sql-reference/sql/create-replication-group) provide read-only replication
without failover support.

| Behavior | Failover group | Replication group |
| --- | --- | --- |
| Dynamic tables refresh on secondary | No (read-only until promoted) | No (permanently read-only) |
| Supports failover/promotion | Yes | No |
| Reinitialization required after failover | No, if [eligibility criteria](#label-continue-incremental-refresh-eligibility) are met | N/A (failover not supported) |
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

### Continuing incremental refresh after failover

An INCREMENTAL or ADAPTIVE dynamic table continues incrementally refreshing after failover,
without reinitializing, when all of the following are true:

- The dynamic table is replicated using a failover group.
- The dynamic table’s base objects, including any policies on those base objects, haven’t changed since the
  dynamic table’s last successful refresh in the primary account.
- The base objects are included in the same failover group as the dynamic table.

If any condition isn’t met, the dynamic table reinitializes with a full refresh on the first refresh after
promotion. A dynamic table configured for FULL refresh always runs a full refresh, whether or not failover
occurred. Custom incremental dynamic tables do not reinitialize, and they always refresh
incrementally, subject to the limitations in
[Limitations](/user-guide/dynamic-tables/custom-incrementalization#label-dynamic-tables-custom-incremental-limitations).

Warning

For an INCREMENTAL or ADAPTIVE dynamic table, if it references base objects outside the failover group, or
base objects that rely on database replication instead of a failover group, it can still be replicated, but it
doesn’t meet the eligibility criteria and reinitializes after failover. The dynamic table’s definition
references whatever objects exist with the same names in the promoted account. If the referenced objects were
not replicated (because they belong to a different database or group), the refresh fails with an object-not-found
error instead.

After failover, INCREMENTAL and ADAPTIVE dynamic tables either reinitialize or continue incrementally refreshing,
depending on eligibility. A dynamic table configured for FULL refresh runs a full refresh. Custom incremental
dynamic tables continue incrementally refreshing, subject to their
[replication limitations](/user-guide/dynamic-tables/custom-incrementalization#label-dynamic-tables-custom-incremental-limitations).
The definition, refresh schedule, and warehouse assignment carry over from the primary.

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

Check the refresh history for reinitialization events and their cause:

Copy code

```
SELECT name, refresh_action, refresh_trigger, reinit_reason
  FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY())
  WHERE refresh_action = 'REINITIALIZE'
  ORDER BY data_timestamp DESC;
```

```
+------------------+----------------+-----------------+----------------------------------------------+
| NAME             | REFRESH_ACTION | REFRESH_TRIGGER | REINIT_REASON                                |
|------------------+----------------+-----------------+----------------------------------------------|
| DT_ORDERS        | REINITIALIZE   | SCHEDULED       | Reinitialize after failover group promotion  |
+------------------+----------------+-----------------+----------------------------------------------+
```

This query lists reinitialization events only. If no `REINITIALIZE` row appears after failover, the
dynamic table continued incrementally refreshing. Query `DYNAMIC_TABLE_REFRESH_HISTORY` without the
`refresh_action` filter to confirm that the post-failover `refresh_action` is `INCREMENTAL`.

## What’s next

- To understand how cloned dynamic tables behave after replication, see
  [Clone dynamic tables](/user-guide/dynamic-tables/cloning).
- To learn about suspend and resume behavior, including auto-suspension, see
  [Manage dynamic tables](/user-guide/dynamic-tables/manage).
- To share dynamic tables across accounts without replication, see
  [Share dynamic tables with other accounts](/user-guide/dynamic-tables/sharing).
