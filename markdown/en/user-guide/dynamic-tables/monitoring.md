# Monitor dynamic tables

You need the MONITOR or OWNERSHIP privilege on a dynamic table to view its metadata.

## Choose a monitoring approach

Snowflake provides several monitoring surfaces. Use the following table to choose the right one for your situation.

| Approach | Best for | Data retention | Setup effort |
| --- | --- | --- | --- |
| SHOW DYNAMIC TABLES | Quick status checks, viewing refresh mode and warehouse | Current snapshot | None |
| INFORMATION\_SCHEMA.DYNAMIC\_TABLES() | Fleet-level health, lag metrics, last refresh outcome | 7 days | None |
| INFORMATION\_SCHEMA.DYNAMIC\_TABLE\_REFRESH\_HISTORY() | Per-refresh diagnostics: state, error, duration, trigger | 7 days | None |
| DYNAMIC\_TABLE\_REFRESH\_HISTORY Account Usage view | Historical trend analysis beyond 7 days | 365 days | None |
| INFORMATION\_SCHEMA.DYNAMIC\_TABLE\_GRAPH\_HISTORY() | Pipeline dependency snapshots and topology changes | 7 days | None |
| Event table + alerts | Automated failure notifications | Configurable | Medium |
| Pipeline spans | Pipeline-level tracing and root cause analysis | Configurable | Medium |

Expand

Show lessSee more

For quick, ad-hoc checks, start with SHOW DYNAMIC TABLES or the DYNAMIC\_TABLES table function. For automated alerting
on refresh failures, set up an event table alert. For historical analysis beyond 7 days, use the Account Usage view.

## Check refresh status

### Check status with SHOW DYNAMIC TABLES

SHOW DYNAMIC TABLES returns the current state of your dynamic tables, including refresh mode, warehouse, scheduling
state, and last data timestamp. It is the only source for the `refresh_mode`, `refresh_mode_reason`, and `warehouse`
columns.

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_%' IN SCHEMA mydb.myschema;
```

```
+---------------------------+------------+---------------+-------------+------+-------+----------+------------+--------------+---------------------+--------------+---------+------+---------------------------+
| CREATED_ON                | NAME       | DATABASE_NAME | SCHEMA_NAME | ROWS | BYTES | OWNER    | TARGET_LAG | REFRESH_MODE | REFRESH_MODE_REASON | WAREHOUSE    | COMMENT | TEXT | SCHEDULING_STATE          |
|---------------------------+------------+---------------+-------------+------+-------+----------+------------+--------------+---------------------+--------------+---------+------+---------------------------|
| 2025-01-15 08:32:28 +0000 | DT_ORDERS  | MY_DB         | MY_SCHEMA   |    4 |  2048 | ORGADMIN | 10 minutes | INCREMENTAL  | NULL                | TRANSFORM_WH |         |  ... | RUNNING                   |
+---------------------------+------------+---------------+-------------+------+-------+----------+------------+--------------+---------------------+--------------+---------+------+---------------------------+
```

Note

SHOW DYNAMIC TABLES uses the scheduling state values RUNNING and SUSPENDED.
The DYNAMIC\_TABLE\_GRAPH\_HISTORY function uses ACTIVE and SUSPENDED instead. Both labels refer to the same operational state.

### Check fleet health with the DYNAMIC\_TABLES function

The [DYNAMIC\_TABLES](/sql-reference/functions/dynamic_tables) function returns lag metrics and the last refresh outcome for all
dynamic tables in your account. Use it to identify tables that aren’t meeting their freshness targets.

Copy code

```
SELECT
  name,
  database_name,
  schema_name,
  scheduling_state,
  last_completed_refresh_state,
  target_lag_sec,
  time_within_target_lag_ratio,
  maximum_lag_sec
FROM
  TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLES())
ORDER BY
  name;
```

```
+--------------------+---------------+-------------+--------------------+-------------------------------+----------------+-------------------------------+-----------------+
| NAME               | DATABASE_NAME | SCHEMA_NAME | SCHEDULING_STATE   | LAST_COMPLETED_REFRESH_STATE  | TARGET_LAG_SEC | TIME_WITHIN_TARGET_LAG_RATIO  | MAXIMUM_LAG_SEC |
|--------------------+---------------+-------------+--------------------+-------------------------------+----------------+-------------------------------+-----------------|
| DT_ORDERS_DAILY    | MY_DB         | MY_SCHEMA   | {"state":"RUNNING"}| SUCCEEDED                     |           1800 |                         0.999 |             125 |
| DT_ORDERS          | MY_DB         | MY_SCHEMA   | {"state":"RUNNING"}| SUCCEEDED                     |            600 |                         0.998 |              42 |
+--------------------+---------------+-------------+--------------------+-------------------------------+----------------+-------------------------------+-----------------+
```

A `time_within_target_lag_ratio` below 0.90 means the dynamic table isn’t meeting its freshness target most of
the time. Investigate the refresh history and consider adjusting the target lag or warehouse size.

## View per-refresh history

The [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) function returns one row per refresh, including the
outcome, error details, duration, and trigger. Use it to investigate specific failures or track refresh trends.

Copy code

```
SELECT
  name,
  state,
  state_code,
  state_message,
  refresh_action,
  refresh_trigger,
  data_timestamp,
  refresh_start_time,
  refresh_end_time,
  DATEDIFF('second', refresh_start_time, refresh_end_time) AS duration_sec
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME_PREFIX => 'MY_DB.MY_SCHEMA'
))
ORDER BY data_timestamp DESC
LIMIT 10;
```

```
+--------------------+-----------------+------------------------------+----------------------------------------------------------------+-----------------+-----------------+---------------------+-------------------------+-------------------------+--------------+
| NAME               | STATE           | STATE_CODE                   | STATE_MESSAGE                                                  | REFRESH_ACTION  | REFRESH_TRIGGER | DATA_TIMESTAMP      | REFRESH_START_TIME      | REFRESH_END_TIME        | DURATION_SEC |
|--------------------+-----------------+------------------------------+----------------------------------------------------------------+-----------------+-----------------+---------------------+-------------------------+-------------------------+--------------|
| DT_ORDERS          | SUCCEEDED       |                              |                                                                | INCREMENTAL     | SCHEDULED       | 2025-04-12 09:01:30 | 2025-04-12 09:01:30     | 2025-04-12 09:01:36     |            6 |
| DT_ORDERS_DAILY    | SUCCEEDED       |                              |                                                                | INCREMENTAL     | SCHEDULED       | 2025-04-12 09:01:36 | 2025-04-12 09:01:36     | 2025-04-12 09:01:48     |           12 |
| DT_ORDERS          | FAILED          | 100038                       | Numeric value 'Good' is not recognized.                        | INCREMENTAL     | SCHEDULED       | 2025-04-12 09:00:00 | 2025-04-12 09:00:00     | 2025-04-12 09:00:05     |            5 |
| DT_ORDERS_DAILY    | UPSTREAM_FAILED | UPSTREAM_FAILURE             | Skipped refreshing because an input dynamic table failed.      | NO_DATA         | SCHEDULED       | 2025-04-12 09:00:00 | 2025-04-12 09:00:05     | 2025-04-12 09:00:05     |            0 |
+--------------------+-----------------+------------------------------+----------------------------------------------------------------+-----------------+-----------------+---------------------+-------------------------+-------------------------+--------------+
```

To filter for only failed refreshes, pass `ERROR_ONLY => TRUE`:

Copy code

```
SELECT
  name,
  state,
  state_code,
  state_message,
  data_timestamp
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME_PREFIX => 'MY_DB.MY_SCHEMA',
  ERROR_ONLY => TRUE
))
ORDER BY data_timestamp DESC;
```

```
+--------------------+-----------------+------------------------------+----------------------------------------------------------------+---------------------+
| NAME               | STATE           | STATE_CODE                   | STATE_MESSAGE                                                  | DATA_TIMESTAMP      |
|--------------------+-----------------+------------------------------+----------------------------------------------------------------+---------------------|
| DT_ORDERS          | FAILED          | 100038                       | Numeric value 'Good' is not recognized.                        | 2025-04-12 09:00:00 |
| DT_ORDERS_DAILY    | UPSTREAM_FAILED | UPSTREAM_FAILURE             | Skipped refreshing because an input dynamic table failed.      | 2025-04-12 09:00:00 |
+--------------------+-----------------+------------------------------+----------------------------------------------------------------+---------------------+
```

Important

The DYNAMIC\_TABLE\_REFRESH\_HISTORY table function retains data for 7 days. For trend analysis
or investigating failures that occurred more than 7 days ago, query the
[DYNAMIC\_TABLE\_REFRESH\_HISTORY Account Usage view](/sql-reference/account-usage/dynamic_table_refresh_history),
which retains data for 365 days.

## Monitor pipeline health with DYNAMIC\_TABLE\_GRAPH\_HISTORY

The [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) function returns the dependency graph of your dynamic
tables, including upstream inputs, scheduling state, and target lag. Use it to understand your pipeline topology and
detect configuration changes over time.

Copy code

```
SELECT
  name,
  scheduling_state,
  target_lag_sec,
  target_lag_type,
  inputs,
  valid_from,
  valid_to
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY(
  NAME => 'MY_DB.MY_SCHEMA.DT_ORDERS_DAILY'
))
ORDER BY valid_from DESC;
```

```
+--------------------+------------------+----------------+-----------------+-------------------------------+-------------------------+-------------------------+
| NAME               | SCHEDULING_STATE | TARGET_LAG_SEC | TARGET_LAG_TYPE | INPUTS                        | VALID_FROM              | VALID_TO                |
|--------------------+------------------+----------------+-----------------+-------------------------------+-------------------------+-------------------------|
| DT_ORDERS_DAILY    | ACTIVE           |           1800 | USER_DEFINED    | ["MY_DB.MY_SCHEMA.DT_ORDERS"] | 2025-04-10 08:00:00     | NULL                    |
+--------------------+------------------+----------------+-----------------+-------------------------------+-------------------------+-------------------------+
```

Each row represents a snapshot of a dynamic table’s properties. When you change a property (for example, the target
lag), a new row appears with an updated `valid_from` timestamp and the previous row gets a `valid_to` value.

To view the full dependency tree for a pipeline, query all dynamic tables that list a given table in their `inputs`
array:

Copy code

```
SELECT
  name,
  inputs,
  scheduling_state,
  target_lag_sec
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY())
WHERE name = 'MY_DB.MY_SCHEMA.DT_ORDERS_DAILY'
   OR ARRAY_CONTAINS('MY_DB.MY_SCHEMA.DT_ORDERS_DAILY'::VARIANT, inputs);
```

```
+----------------------------------+-------------------------------+------------------+----------------+
| NAME                             | INPUTS                        | SCHEDULING_STATE | TARGET_LAG_SEC |
|----------------------------------+-------------------------------+------------------+----------------|
| MY_DB.MY_SCHEMA.DT_ORDERS_DAILY  | ["MY_DB.MY_SCHEMA.DT_ORDERS"] | ACTIVE           |           1800 |
+----------------------------------+-------------------------------+------------------+----------------+
```

### View the pipeline graph in Snowsight

In Snowsight, the lineage graph visualizes upstream and downstream dependencies:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Transformation** » **Dynamic tables**.
3. Select your dynamic table. The **Graph** view is displayed by default.
4. Select any dynamic table in the graph to view its lag metrics and configuration in the **Details** pane.

If a refresh failed with an UPSTREAM\_FAILED status, the graph highlights which upstream dynamic table
caused the failure.

## Dynamic tables in ACCESS\_HISTORY

Dynamic table refresh operations are recorded in the [ACCESS\_HISTORY](/sql-reference/account-usage/access_history) view:

- **Refresh reads:** The base tables read during a refresh appear in the `base_objects_accessed` field.
- **Refresh writes:** The dynamic table being refreshed appears in `object_modified_by_ddl` as a DDL ALTER operation
  with `dynamicTableAction = 'REFRESH'`.
- **User queries:** SELECT queries against a dynamic table are recorded as standard table access.

## Set up alerts with the event table

When a dynamic table refreshes, Snowflake can record a `refresh.status` event in the
[active event table](/developer-guide/logging-tracing/event-table-setting-up). You can create an alert that monitors
the event table and sends a notification when a refresh fails.

Note

Logging events for dynamic tables incurs costs. See [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

### Set the event severity level

You must set the LOG\_EVENT\_LEVEL parameter before events are captured. If you don’t set it, no events are
recorded.

Events are captured at the following levels:

- `ERROR`: Refresh failure events only.
- `WARN`: Refresh failures and upstream failure events.
- `INFO`: All refresh events, including successes.

Set the level on the account, database, schema, or a specific dynamic table. For example, run
`ALTER DYNAMIC TABLE dt_orders SET LOG_EVENT_LEVEL = WARN` to capture WARN and ERROR events for a
specific table, or `ALTER DATABASE mydb SET LOG_EVENT_LEVEL = INFO` to capture all events for every
supported object in a database.

Important

Setting LOG\_EVENT\_LEVEL at the database, schema, or account level affects all object types that
support event logging (dynamic tables, stored procedures, UDFs, tasks), not just dynamic tables.

### Query the event table

After you set the severity level, query the event table to see refresh events. Filter on
`resource_attributes:"snow.executable.type" = 'DYNAMIC_TABLE'` to isolate dynamic table events.

Copy code

```
SELECT
    timestamp,
    resource_attributes:"snow.executable.name"::VARCHAR AS dt_name,
    resource_attributes:"snow.query.id"::VARCHAR AS query_id,
    record:"severity_text"::VARCHAR AS severity,
    value:state::VARCHAR AS state,
    value:message::VARCHAR AS error_message
  FROM my_event_table
  WHERE
    resource_attributes:"snow.executable.type" = 'DYNAMIC_TABLE' AND
    resource_attributes:"snow.database.name" = 'MY_DB' AND
    record:"name" = 'refresh.status' AND
    value:state = 'FAILED'
  ORDER BY timestamp DESC;
```

```
+-------------------------+------------+--------------------------------------+----------+--------+---------------------------------------------------------------------------------+
| TIMESTAMP               | DT_NAME    | QUERY_ID                             | SEVERITY | STATE  | ERROR_MESSAGE                                                                   |
|-------------------------+------------+--------------------------------------+----------+--------+---------------------------------------------------------------------------------|
| 2025-02-17 21:40:45.444 | DT_ORDERS  | 01ba7614-0107-e56c-0000-a995024f304a | ERROR    | FAILED | SQL compilation error:                                                          |
|                         |            |                                      |          |        | Object 'MY_DB.MY_SCHEMA.RAW_ORDERS' does not exist or not authorized.           |
+-------------------------+------------+--------------------------------------+----------+--------+---------------------------------------------------------------------------------+
```

To query for upstream failures instead, change the filter to `value:state = 'UPSTREAM_FAILURE'`. (The event table uses `UPSTREAM_FAILURE`; the DYNAMIC\_TABLE\_REFRESH\_HISTORY function uses `UPSTREAM_FAILED`.)

### Create an alert on refresh failures

An alert on new data triggers when new rows matching a condition are inserted into the event table. The following
example sends a Slack notification when any dynamic table in `mydb` fails to refresh.

Note

To create an alert on new data, you need a role with the required privileges to query the event table.

- For the [default event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default)
  (SNOWFLAKE.TELEMETRY.EVENTS), see [Event table default roles](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).
- For a custom event table, see [Event table access control](/developer-guide/logging-tracing/event-table-operations#label-event-table-access-control-privileges).

To create an alert that fires when dynamic table refreshes fail, use the Snowflake alerts feature with a condition
query against the event table. Filter on `resource_attributes:"snow.executable.type" = 'DYNAMIC_TABLE'` and
`record:"severity_text" = 'ERROR'` to detect failures, then send a notification (for example, through a Slack integration).

For alert creation syntax, scheduling options, and notification integration setup, see
[Setting up alerts](/user-guide/alerts).

Note

The `timestamp` column in the event table stores values in UTC. If you use a scheduled alert with a timestamp filter
instead of an alert on new data, convert the current timestamp to UTC:

Copy code

```
timestamp > DATEADD('minute', -5, CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP()))
```

### Event table column reference

When a dynamic table refreshes, a row with the following values is inserted into the event table.

#### Key columns

| Column | Data type | Description |
| --- | --- | --- |
| `timestamp` | TIMESTAMP\_NTZ | The UTC timestamp when the event was created. |
| `observed_timestamp` | TIMESTAMP\_NTZ | Currently the same as `timestamp`. |
| `resource_attributes` | OBJECT | Attributes that identify the dynamic table. See [Key-value pairs in `resource_attributes`](#key-value-pairs-in-resource_attributes). |
| `record_type` | STRING | `EVENT` for dynamic table refreshes. |
| `record` | OBJECT | Details about the refresh status. See [Key-value pairs in `record`](#key-value-pairs-in-record). |
| `value` | VARIANT | The refresh state and, for failures, the error message. See [Key-value pairs in `value`](#key-value-pairs-in-value). |

Expand

Show lessSee more

#### Key-value pairs in `resource_attributes`

| Attribute | Type | Description | Example |
| --- | --- | --- | --- |
| `snow.database.name` | VARCHAR | Database containing the dynamic table. | `MY_DB` |
| `snow.schema.name` | VARCHAR | Schema containing the dynamic table. | `MY_SCHEMA` |
| `snow.executable.name` | VARCHAR | Name of the dynamic table. | `DT_ORDERS` |
| `snow.executable.type` | VARCHAR | Object type. Always `DYNAMIC_TABLE` for these events. | `DYNAMIC_TABLE` |
| `snow.query.id` | VARCHAR | Query ID of the refresh. | `01ba7614-0107-e56c-0000-a995024f304a` |
| `snow.warehouse.name` | VARCHAR | Warehouse used for the refresh. | `TRANSFORM_WH` |
| `snow.owner.name` | VARCHAR | Role with OWNERSHIP on the dynamic table. | `DATA_ADMIN` |
| `snow.owner.type` | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. | `ROLE` |
| `snow.database.id` | INTEGER | Internal ID of the database. | `12345` |
| `snow.schema.id` | INTEGER | Internal ID of the schema. | `12345` |
| `snow.executable.id` | INTEGER | Internal ID of the dynamic table. | `12345` |
| `snow.owner.id` | INTEGER | Internal ID of the owner role. | `12345` |
| `snow.warehouse.id` | INTEGER | Internal ID of the warehouse. | `12345` |

Expand

Show lessSee more

#### Key-value pairs in `record`

| Key | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | VARCHAR | Event name. Always `refresh.status` for dynamic table refreshes. | `refresh.status` |
| `severity_text` | VARCHAR | `INFO` (refresh succeeded), `ERROR` (refresh failed), or `WARN` (upstream dynamic table failed). | `ERROR` |

Expand

Show lessSee more

#### Key-value pairs in `value`

| Key | Type | Description | Example |
| --- | --- | --- | --- |
| `state` | VARCHAR | `SUCCEEDED`, `FAILED`, or `UPSTREAM_FAILURE`. | `FAILED` |
| `message` | VARCHAR | Error message when `state` is `FAILED`. NULL otherwise. | `SQL compilation error: Object does not exist.` |

Expand

Show lessSee more

## Trace pipelines with spans

In addition to events, Snowflake can record pipeline spans for dynamic table refreshes. Events record
individual refresh outcomes. Spans add pipeline-level context: correlated trace IDs, skip reasons, and dependency topology.

Spans capture states for which events are not emitted, including `SKIPPED` refreshes
due to upstream skips or scheduler load shedding.

Note

Recording spans for dynamic tables incurs costs. See [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

### Enable pipeline spans

Set the TRACE\_LEVEL parameter to `ALWAYS` at the schema or database level, for example
`ALTER SCHEMA mydb.myschema SET TRACE_LEVEL = 'ALWAYS'`.

### Query span data

Filter for rows where `record_type = 'SPAN'` and `record:"name" = 'table_refresh'`:

Copy code

```
SELECT
    resource_attributes:"snow.executable.name"::STRING AS dt_name,
    record_attributes:"snow.dynamic_table.state"::STRING AS state,
    record_attributes:"snow.dynamic_table.state_reason"::STRING AS state_reason,
    record_attributes:"snow.dynamic_table.data_timestamp"::STRING AS data_timestamp,
    trace:"trace_id"::STRING AS trace_id,
    trace:"span_id"::STRING AS span_id,
    record:"status":"code"::STRING AS status_code
  FROM my_event_table
  WHERE record_type = 'SPAN'
    AND record:"name" = 'table_refresh'
  ORDER BY start_timestamp ASC;
```

```
+------------+-----------+-----------------+-------------------------+-----------------------------------+----------+-------------------+
| DT_NAME    | STATE     | STATE_REASON    | DATA_TIMESTAMP          | TRACE_ID                          | SPAN_ID  | STATUS_CODE       |
|------------+-----------+-----------------+-------------------------+-----------------------------------+----------+-------------------|
| DT_ORDERS  | SUCCEEDED | NULL            | 2026-02-13T10:00:00.000 | abc123def456abc123def456abc12345  | f1e2d3c4 | STATUS_CODE_OK    |
| DT_CUSTOMERS | SUCCEEDED | NULL            | 2026-02-13T10:00:00.000 | abc123def456abc123def456abc12345  | b5a6c7d8 | STATUS_CODE_OK    |
| DT_ENRICHED | FAILED    | QUERY_FAILURE   | 2026-02-13T10:00:00.000 | abc123def456abc123def456abc12345  | a1b2c3d4 | STATUS_CODE_ERROR |
| DT_SUMMARY | SKIPPED   | UPSTREAM_FAILURE| 2026-02-13T10:00:00.000 | abc123def456abc123def456abc12345  | c9d0e1f2 | STATUS_CODE_ERROR |
+------------+-----------+-----------------+-------------------------+-----------------------------------+----------+-------------------+
```

#### Span attributes (`record_attributes`)

| Attribute | Type | Description |
| --- | --- | --- |
| `snow.dynamic_table.state` | STRING | `SUCCEEDED`, `FAILED`, or `SKIPPED`. |
| `snow.dynamic_table.state_reason` | STRING | Why the refresh was skipped or failed. NULL on success. Values: `QUERY_FAILURE`, `UPSTREAM_FAILURE`, `UPSTREAM_SKIP`, `NOT_EFFECTIVE_TICK_TO_REFRESH`. |
| `snow.dynamic_table.data_timestamp` | STRING | The transactional timestamp when the refresh was evaluated. All data in base tables that arrived before this timestamp is included in the dynamic table. |

Expand

Show lessSee more

### Correlate spans across a pipeline

When a refresh cycle includes multiple dynamic tables, all spans share the same `trace:"trace_id"`. Each span also
includes a `record:"links"` array that lists the `span_id` of each upstream dependency.

To retrieve all spans from a single refresh cycle, use the `trace:"trace_id"` value from the span query output:

Copy code

```
SELECT
    trace:"span_id"::STRING AS span_id,
    resource_attributes:"snow.executable.name"::STRING AS dt_name,
    record_attributes:"snow.dynamic_table.state"::STRING AS state,
    record_attributes:"snow.dynamic_table.state_reason"::STRING AS state_reason,
    start_timestamp,
    timestamp AS end_timestamp,
    DATEDIFF('second', start_timestamp, timestamp) AS duration_sec,
    record:"links" AS upstream_links
  FROM my_event_table
  WHERE record_type = 'SPAN'
    AND record:"name" = 'table_refresh'
    AND trace:"trace_id" = 'abc123def456abc123def456abc12345'
  ORDER BY start_timestamp ASC;
```

```
+----------+---------+-----------+-----------------+-------------------------+-------------------------+--------------+---------------------------------------------+
| SPAN_ID  | DT_NAME | STATE     | STATE_REASON    | START_TIMESTAMP         | END_TIMESTAMP           | DURATION_SEC | UPSTREAM_LINKS                              |
|----------+---------+-----------+-----------------+-------------------------+-------------------------+--------------+---------------------------------------------|
| f1e2d3c4 | DT_ORDERS    | SUCCEEDED | NULL            | 2026-02-13 10:01:00.000 | 2026-02-13 10:01:30.000 |           30 | []                                          |
| b5a6c7d8 | DT_CUSTOMERS | SUCCEEDED | NULL            | 2026-02-13 10:01:31.000 | 2026-02-13 10:02:00.000 |           29 | [{"span_id": "f1e2d3c4", ...}]              |
| a1b2c3d4 | DT_ENRICHED  | FAILED    | QUERY_FAILURE   | 2026-02-13 10:02:01.000 | 2026-02-13 10:02:20.000 |           19 | [{"span_id": "b5a6c7d8", ...}]              |
| c9d0e1f2 | DT_SUMMARY   | SKIPPED   | UPSTREAM_FAILURE| 2026-02-13 10:02:20.000 | 2026-02-13 10:02:20.000 |            0 | [{"span_id": "a1b2c3d4", ...}]              |
+----------+---------+-----------+-----------------+-------------------------+-------------------------+--------------+---------------------------------------------+
```

In this example, DT\_ORDERS and DT\_CUSTOMERS succeeded, DT\_ENRICHED failed due to a query error, and DT\_SUMMARY was automatically skipped
because its upstream dependency failed. The `UPSTREAM_LINKS` column shows each dynamic table’s direct dependencies
by `span_id`.

### Trace the root cause of a failure

When a downstream dynamic table is skipped or fails, trace its upstream dependencies through the span links
to find the root cause:

Copy code

```
WITH pipeline AS (
  SELECT
    trace:"span_id"::STRING AS span_id,
    resource_attributes:"snow.executable.name"::STRING AS dt_name,
    record_attributes:"snow.dynamic_table.state"::STRING AS state,
    record_attributes:"snow.dynamic_table.state_reason"::STRING AS state_reason,
    resource_attributes:"snow.query.id"::STRING AS query_id,
    record:"links" AS upstream_links
  FROM my_event_table
  WHERE record_type = 'SPAN'
    AND record:"name" = 'table_refresh'
    AND record_attributes:"snow.dynamic_table.data_timestamp" = '2026-02-13T10:00:00.000'
),
target_links AS (
  SELECT f.value:"span_id"::STRING AS upstream_span_id
  FROM pipeline,
  LATERAL FLATTEN(input => upstream_links) f
  WHERE dt_name = 'DT_SUMMARY'
)
SELECT
  p.dt_name AS upstream_dt,
  p.state AS upstream_state,
  p.state_reason AS upstream_reason,
  p.query_id AS upstream_query_id
FROM target_links tl
JOIN pipeline p ON tl.upstream_span_id = p.span_id;
```

```
+-------------+----------------+-----------------+--------------------------------------+
| UPSTREAM_DT | UPSTREAM_STATE | UPSTREAM_REASON | UPSTREAM_QUERY_ID                    |
|-------------+----------------+-----------------+--------------------------------------|
| DT_ENRICHED | FAILED         | QUERY_FAILURE   | 01ba7614-0107-e56c-0000-a995024f304a |
+-------------+----------------+-----------------+--------------------------------------+
```

Use the `query_id` to investigate the failed query further with
[GET\_QUERY\_OPERATOR\_STATS](/sql-reference/functions/get_query_operator_stats) or
the [query history](/sql-reference/account-usage/query_history).

Dynamic table pipeline spans follow the OpenTelemetry data model. You can export them from the event table into
OpenTelemetry-compatible tools for visualization.

## Monitor dynamic tables in Snowsight

List and inspect dynamic tablesView refresh history

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Catalog** » **Database Explorer**.
3. Select a database and schema, then select the **Dynamic Tables** tab.
4. Select a dynamic table to view its details:
   - **Table Details**: Scheduling state, last refresh status, current and target lag, refresh mode, tags, and
     privileges.
   - **Columns**: Column names and types.
   - **Data Preview**: Up to 100 rows of data.
   - **Graph**: The pipeline dependency graph for this dynamic table.
   - **Refresh History**: Per-refresh status, duration, lag metrics, and rows changed.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Transformation** » **Dynamic tables**.
3. View the scheduling state and last refresh status for all dynamic tables. Filter by database or schema to narrow
   results.
4. Select a dynamic table and go to the **Refresh History** tab to see per-refresh details including
   status, duration, and lag.

## What’s next

- To troubleshoot skipped or failed refreshes, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- To look up specific error codes from failed refreshes, see [Error code reference for dynamic tables](/user-guide/dynamic-tables/error-codes).
- To diagnose slow refreshes and optimize performance, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- To understand how target lag affects refresh scheduling, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).
- To manage costs, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
