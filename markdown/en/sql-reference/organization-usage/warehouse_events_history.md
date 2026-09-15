Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# WAREHOUSE\_EVENTS\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to return the events that have been triggered for the single-cluster and multi-cluster warehouses
in your account.

Supported events include:

- Creating, dropping, or altering a warehouse, including resizing the warehouse.
- Resuming or suspending a warehouse.
- Resuming, suspending, or resizing a cluster in a warehouse (single-cluster and multi-cluster warehouses).
- Stopping or starting additional clusters in a warehouse (multi-cluster warehouses only).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column name | Data Type | Description |
| --- | --- | --- |
| TIMESTAMP | TIMESTAMP\_LTZ | The timestamp when the event is triggered. |
| WAREHOUSE\_ID | NUMBER | The unique warehouse ID (assigned by Snowflake) that corresponds to the warehouse name in your account. |
| WAREHOUSE\_NAME | VARCHAR | The name of the warehouse in your account. |
| CLUSTER\_NUMBER | NUMBER | If an event was triggered for a specific cluster in a multi-cluster warehouse, the number of the cluster (starting with 1) for which the event was triggered; if the event was triggered for all clusters in the warehouse or is not applicable for a single-cluster warehouse, NULL is displayed. |
| EVENT\_NAME | VARCHAR | Name of the event. For the list of possible values, see below. |
| EVENT\_REASON | VARCHAR | The cause of the event. For the list of possible values, see below. |
| EVENT\_STATE | VARCHAR | State of an event that might take time to complete: STARTED or COMPLETED. |
| USER\_NAME | VARCHAR | User who initiated the event. |
| ROLE\_NAME | VARCHAR | Role that was active in the session at the time the event was initiated. |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| SIZE | VARCHAR | Current size of the warehouse at the time of the event. This value is only available for WAREHOUSE\_CONSISTENT events. Otherwise, this value is NULL. |
| CLUSTER\_COUNT | VARCHAR | Number of warehouse clusters at the time of the event. This value is only available for WAREHOUSE\_CONSISTENT events. Otherwise, this value is NULL. |
| WAREHOUSE\_TYPE | VARCHAR | One of `STANDARD` or `SNOWPARK-OPTIMIZED`. This value is only available for WAREHOUSE\_CONSISTENT events. Otherwise, this value is NULL. |
| RESOURCE\_CONSTRAINT | VARCHAR | One of:   - `STANDARD_GEN_1`   - `STANDARD_GEN_2`   - `MEMORY_1X`   - `MEMORY_1X_x86`   - `MEMORY_16X`   - `MEMORY_16X_x86`   - `MEMORY_64X`   - `MEMORY_64X_x86`   This value is only available for WAREHOUSE\_CONSISTENT events. Otherwise, this value is NULL. It’s also NULL for standard warehouses created before the release of the STANDARD\_GEN\_2 feature. |

Expand

Show lessSee more

### EVENT\_NAME descriptions

The following sections describe the valid values for the EVENT\_NAME column for warehouse-related and cluster-related events.

# Warehouse-related events

The following table describes the valid values for the EVENT\_NAME column for warehouse-related events:

|  |  |
| --- | --- |
| Cluster number | None (N/A) |
| Event state | COMPLETED or STARTED |
| Event reason | CONVERT\_TO\_SNOWPARK\_OPTIMIZED, CONVERT\_TO\_STANDARD, or CONVERT\_RESOURCE\_CONSTRAINT |

Expand

Show lessSee more

Cost impact: Newly added resources start metering when they are provisioned. Removed resources stop metering after they finish processing any currently executing queries.

Tip

For information about cost implications of changing the RESOURCE\_CONSTRAINT property, see
[considerations for changing RESOURCE\_CONSTRAINT while a warehouse is running or suspended](/user-guide/warehouses-gen2#label-gen-2-standard-warehouses-altering).

|  |  |
| --- | --- |
| Cluster number | None (N/A) |
| Event state | COMPLETED or STARTED |
| Event reason | None (N/A) |

Expand

Show lessSee more

Cost impact: None if the cluster is created with INITIALLY\_SUSPENDED = TRUE. Otherwise, metering starts
when all compute resources are provisioned for the warehouse or the warehouse starts processing statements (if the
warehouse starts processing statements before the resources are fully provisioned).

|  |  |
| --- | --- |
| Cluster number | None (N/A) |
| Event state | COMPLETED or STARTED |
| Event reason | None (N/A) |

Expand

Show lessSee more

Cost impact: Metering on the compute resources for the warehouse stops after all currently executing queries complete.

|  |  |
| --- | --- |
| Cluster number | None (N/A) |
| Event state | COMPLETED or STARTED |
| Event reason | None (N/A) |

Expand

Show lessSee more

Cost impact: Depends on the event(s) that are triggered by the ALTER statement.

|  |  |
| --- | --- |
| Cluster number | None (N/A) |
| Event state | STARTED |
| Event reason | WAREHOUSE\_RESIZE |

Expand

Show lessSee more

Cost impact: Resizing a running warehouse adds or removes compute resources in each cluster in the warehouse. Newly added resources
start metering when they are provisioned. Removed resources stop metering after they finish processing any currently
executing queries.

Resizing a suspended warehouse does not provision any new resources for the warehouse.

|  |  |
| --- | --- |
| Cluster number | None (applies to all clusters) |
| Event state | STARTED |
| Event reason | WAREHOUSE\_AUTORESUME or WAREHOUSE\_RESUME |

Expand

Show lessSee more

Cost impact: Metering begins after all the compute resources are provisioned for the warehouse.

|  |  |
| --- | --- |
| Cluster number | None (applies to all clusters) |
| Event state | STARTED |
| Event reason | WAREHOUSE\_AUTOSUSPEND or WAREHOUSE\_SUSPEND |

Expand

Show lessSee more

Cost impact: Metering on the compute resources for the warehouse stops after all running statements complete.

|  |  |
| --- | --- |
| Cluster number | NULL |
| Event state | COMPLETED |
| Event reason | NULL |

Expand

Show lessSee more

Cost impact: None. Metering occurs for the warehouse event that is logged with the STARTED state before the
WAREHOUSE\_CONSISTENT event.

For more information, see the cost impact of the warehouse events described in the previous rows.

|  |  |  |
| --- | --- | --- |
| Cluster number | NULL |  |
| Event state | COMPLETED |  |
| Event reason | NULL | NULL |
| Event reason | NULL | NULL |

Expand

Show lessSee more

## Cluster-related events

The following table describes the valid values for the EVENT\_NAME column for cluster-related events:

|  |  |
| --- | --- |
| Cluster number | Number of the converted cluster (always `1` for a single-cluster warehouse) |
| Event state | COMPLETED or STARTED |
| Event reason | CONVERT\_TO\_SNOWPARK\_OPTIMIZED or CONVERT\_TO\_STANDARD |

Expand

Show lessSee more

Cost impact: Newly added resources start metering when they are provisioned. Removed resources stop metering after they finish processing any currently executing queries.

Tip

For information about cost implications of changing the RESOURCE\_CONSTRAINT property, see
[considerations for changing RESOURCE\_CONSTRAINT while a warehouse is running or suspended](/user-guide/warehouses-gen2#label-gen-2-standard-warehouses-altering).

|  |  |
| --- | --- |
| Cluster number | Number of the resumed cluster (always `1` for a single-cluster warehouse) |
| Event state | STARTED |
| Event reason | - WAREHOUSE\_AUTORESUME or WAREHOUSE\_RESUME (single-cluster warehouse) - MULTICLUSTER\_SPINUP (multi-cluster warehouse) |

Expand

Show lessSee more

Cost impact: Metering starts on the compute resources for the cluster after they are provisioned.

|  |  |
| --- | --- |
| Cluster number | Number of the suspended cluster (always `1` for a single-cluster warehouse) |
| Event state | STARTED |
| Event reason: | - WAREHOUSE\_AUTOSUSPEND or WAREHOUSE\_SUSPEND (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN (multi-cluster warehouse) - RESOURCE\_MONITOR\_SUSPEND |

Expand

Show lessSee more

Cost impact: Metering stops on the compute resources for the cluster after all currently executing queries complete.

|  |  |
| --- | --- |
| Cluster number | Number of the resized cluster (always `1` for a single-cluster warehouse) |
| Event state | STARTED |
| Event reason | - WAREHOUSE\_AUTORESUME or WAREHOUSE\_RESUME (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN or MULTICLUSTER\_SPINUP (multi-cluster warehouse) - WAREHOUSE\_RESIZE |

Expand

Show lessSee more

Cost impact: Depends on whether compute resources are added or removed due to resizing. Newly added resources
start metering when they are provisioned. Removed resources stop metering after they finish processing any currently
executing queries.

|  |  |
| --- | --- |
| Cluster number | Number of the cluster that was started |
| Event state | STARTED |
| Event reason | - WAREHOUSE\_RESIZE (single-cluster warehouse) - MULTICLUSTER\_SPINUP (multi-cluster warehouse) |

Expand

Show lessSee more

Cost impact: Metering starts on the compute resources for the cluster after they are provisioned.

|  |  |
| --- | --- |
| Cluster number | Number of the cluster that was shut down |
| Event state | STARTED |
| Event reason | - WAREHOUSE\_RESIZE (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN (multi-cluster warehouse) |

Expand

Show lessSee more

Cost impact: Metering stops on the compute resources for the cluster after all currently executing queries complete.

|  |  |  |
| --- | --- | --- |
| Cluster number | Number of the cluster that was shut down |  |
| Event state | STARTED |  |
| Event reason | - WAREHOUSE\_RESIZE (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN (multi-cluster warehouse) | - WAREHOUSE\_RESIZE (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN (multi-cluster warehouse) |
| Event reason | - WAREHOUSE\_RESIZE (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN (multi-cluster warehouse) | - WAREHOUSE\_RESIZE (single-cluster warehouse) - MULTICLUSTER\_SPINDOWN (multi-cluster warehouse) |

Expand

Show lessSee more

### EVENT\_REASON descriptions

The following table describes the valid values for the EVENT\_REASON column:

| EVENT\_REASON | Description |
| --- | --- |
| WAREHOUSE\_AUTORESUME | A suspended warehouse was resumed automatically because AUTO\_RESUME is enabled for the warehouse and a SQL statement was submitted to the warehouse. |
| WAREHOUSE\_RESUME | A suspended warehouse was resumed manually by a user. |
| WAREHOUSE\_AUTOSUSPEND | A running warehouse was suspended automatically because AUTO\_SUSPEND is enabled for the warehouse and the defined period of inactivity for AUTO\_SUSPEND has passed. |
| WAREHOUSE\_SUSPEND | A running warehouse was suspended manually by a user. |
| WAREHOUSE\_RESIZE | A warehouse was resized. |
| RESOURCE\_MONITOR\_SUSPEND | A warehouse was suspended because the credit quota for the resource monitor for the warehouse was reached. |
| MULTICLUSTER\_SPINUP | A new or suspended cluster was provisioned in a multi-cluster warehouse; not applicable to single-cluster warehouses. |
| MULTICLUSTER\_SPINDOWN | A running cluster was shut down in a multi-cluster warehouse; not applicable to single-cluster warehouses. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- An event can produce multiple rows in the view if it triggers additional, related events.
- The value for the EVENT\_REASON, USER\_NAME, ROLE\_NAME, and QUERY\_ID columns is NULL for a WAREHOUSE\_CONSISTENT event.
- The WAREHOUSE\_CONSISTENT event might share the same timestamp with another warehouse event and be listed out of order.

# Warehouse event that indicates that an operation has completed

Events that create a warehouse, change the size of the warehouse or the number of clusters, or suspend a warehouse are not atomic
operations. This means that some small amount of time is required for these operations to fully complete.

For example, if a warehouse is suspended using an ALTER WAREHOUSE … SUSPEND statement, any queries that are currently executing on the
warehouse must complete (or time out) before it can be suspended. In some cases, multiple warehouse events might be in-flight
(for example, resize and suspend). When all warehouse events have completed, the warehouse is in a *consistent* state.

If a warehouse event is logged with the STARTED state in the EVENT\_STATE column, it is never
logged with a COMPLETED state. Instead, an event logged with the STARTED state is always followed by a subsequent WAREHOUSE\_CONSISTENT
event. If multiple warehouse events are logged with the STARTED event state, those events coalesce to the same WAREHOUSE\_CONSISTENT event.

If a warehouse event is logged with the COMPLETED state in the EVENT\_STATE column, no subsequent WAREHOUSE\_CONSISTENT event follows
unless another pending event is logged with a STARTED state.

## Examples

### View events history for the previous week

View the events history for warehouse `my_wh` for the previous week by executing the following statement:

Copy code

```
SELECT account_name, timestamp, warehouse_name, cluster_number,
       event_name, event_reason, event_state,
       size, cluster_count
  FROM SNOWFLAKE.ORGANIZATION_USAGE.WAREHOUSE_EVENTS_HISTORY
  WHERE warehouse_name = 'MY_WH'
  AND timestamp > DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY timestamp DESC;
```

### Example events history results

#### Events history for a statement with no pending changes

An ALTER WAREHOUSE statement is logged with the COMPLETED state when there are no additional changes pending. For example,
the following statement updates the comment for warehouse `my_wh`:

Copy code

```
ALTER WAREHOUSE my_wh SET
  COMMENT = 'Updated comment for warehouse';
```

This statement results in the following row in the WAREHOUSE\_EVENTS\_HISTORY view:

| TIMESTAMP | WAREHOUSE\_NAME | EVENT\_NAME | EVENT\_STATE | SIZE | CLUSTER\_COUNT |
| --- | --- | --- | --- | --- | --- |
| 2024-04-26 16:42:13.513 +0000 | MY\_WH | ALTER\_WAREHOUSE | COMPLETED | NULL | NULL |

Expand

Show lessSee more

#### Events history for a statement that is followed by a WAREHOUSE\_CONSISTENT event

When an ALTER WAREHOUSE statement changes the warehouse size, additional events follow. For example, resize warehouse
`my_wh`:

Copy code

```
ALTER WAREHOUSE my_wh SET
  WAREHOUSE_SIZE = 'SMALL';
```

This statement results in the following rows in the WAREHOUSE\_EVENTS\_HISTORY view:

| TIMESTAMP | WAREHOUSE\_NAME | EVENT\_NAME | EVENT\_STATE | SIZE | CLUSTER\_COUNT |
| --- | --- | --- | --- | --- | --- |
| 2024-05-29 15:13:05.874 +0000 | MY\_WH | ALTER\_WAREHOUSE | STARTED | NULL | NULL |
| 2024-05-29 15:13:05.874 +0000 | MY\_WH | RESIZE\_WAREHOUSE | STARTED | NULL | NULL |
| 2024-05-29 15:13:06.036 +0000 | MY\_WH | WAREHOUSE\_CONSISTENT | COMPLETED | SMALL | 1 |
| 2024-05-29 15:13:06.036 +0000 | MY\_WH | RESIZE\_CLUSTER | COMPLETED | NULL | NULL |

Expand

Show lessSee more

#### Events history for a Snowflake-initiated warehouse event

When Snowflake resumes a multi-cluster warehouse, the following warehouse events are logged:

| TIMESTAMP | WAREHOUSE\_NAME | EVENT\_NAME | EVENT\_STATE | SIZE | CLUSTER\_COUNT |
| --- | --- | --- | --- | --- | --- |
| 2024-04-23 17:04:11.618 +0000 | MY\_WH | SPINUP\_CLUSTER | STARTED | NULL | NULL |
| 2024-04-23 17:04:11.657 +0000 | MY\_WH | RESUME\_CLUSTER | STARTED | NULL | NULL |
| 2024-04-23 17:04:11.657 +0000 | MY\_WH | WAREHOUSE\_CONSISTENT | COMPLETED | LARGE | 5 |

Expand

Show lessSee more
