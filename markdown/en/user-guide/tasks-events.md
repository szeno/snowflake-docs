# Monitor events for task executions

You can configure Snowflake to record an event that provides information about the status of the task execution. The event is
recorded in the [active event table](/developer-guide/logging-tracing/event-table-setting-up) associated with the task.

For example, suppose that you have [associated an event table with a database](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-object). When a
task in that database executes, Snowflake records an event to that event table.

You can set up an [alert on new data](/user-guide/alerts#label-alerts-type-streaming) to monitor the event table. You can configure the alert
to [send a notification](/user-guide/notifications/about-notifications) when a task execution fails.

The next sections explain how to set up the event logging to capture the events, how to set up the alert, and how to interpret
the events recorded in the event table:

- [Set the severity level of the events to capture](#label-task-monitor-events-level)
- [Set up an alert on new data for task completion events](#label-task-monitor-events-alert)
- [Query the event table for task completion events](#label-task-monitor-events-query)
- [Information logged for task events](#label-task-monitor-events-table-reference)

Note

Logging events for tasks incurs costs. See [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

## Limitations

- Task events aren’t supported for Snowflake Native Apps.

### Set the severity level of the events to capture

To set up task events to be recorded to the event table,
[set the severity level of events](/developer-guide/logging-tracing/telemetry-levels) that you want captured in the event
table:

- `ERROR`: Events for failed task runs.
- `INFO`: Events for successful and failed task runs.

To set the level, set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter for the account or object. You can set the level for:

- All objects in the account,
- All objects in a database or schema.
- A specific task.

Note

If the severity level is not set on the account or object, no events will be captured.

For example:

- To capture ERROR-level task events for all supported objects in the account, execute
  [ALTER ACCOUNT SET LOG\_EVENT\_LEVEL](/sql-reference/sql/alter-account):

  Copy code

  ```
  ALTER ACCOUNT SET LOG_EVENT_LEVEL = ERROR;
  ```

  Setting `LOG_EVENT_LEVEL` at the account level applies to log events (record type EVENT) for supported workloads in the account, including tasks. It does not replace [LOG\_LEVEL](/sql-reference/parameters#label-log-level) for log messages from logging APIs. For more information, see [Parameters](/sql-reference/parameters).
- To capture INFO-level task events for all supported objects in the database `my_db`, execute
  [ALTER DATABASE … SET LOG\_EVENT\_LEVEL](/sql-reference/sql/alter-database):

  Copy code

  ```
  ALTER DATABASE my_db SET LOG_EVENT_LEVEL = INFO;
  ```

  Similar to the case of setting the level on the account, setting the level on the database affects log events for supported object types in the database.
- To capture ERROR-level events for the task `my_task`, execute
  [ALTER TASK … SET LOG\_EVENT\_LEVEL](/sql-reference/sql/alter-task):

  Copy code

  ```
  ALTER TASK my_task SET LOG_EVENT_LEVEL = ERROR;
  ```

### Set up an alert on new data for task completion events

After you set the severity level for logging events, you can set up an alert on new data to monitor the event table for new events
that indicate a failure in a task completion. An alert on new data is triggered when new rows in the event table are inserted
and meet the condition specified in the alert.

Note

To create the alert on new data, you must use a role that has been granted the required privileges to query the event table.

- If the alert condition queries the default event table ([SNOWFLAKE.TELEMETRY.EVENTS](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default))
  predefined view ([SNOWFLAKE.TELEMETRY.EVENTS\_VIEW view](/sql-reference/telemetry/events_view)),
  see [Roles for access to the default event table and EVENTS\_VIEW](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).

  To manage access to the EVENTS\_VIEW view, see [Manage access to the EVENTS\_VIEW view](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-event-view-manage-access).
- If the alert condition queries a custom event table, see [Access control privileges for event tables](/developer-guide/logging-tracing/event-table-operations#label-event-table-access-control-privileges).

  To manage access to a custom event table, see [Managing access to event table data](/developer-guide/logging-tracing/event-table-operations#label-event-table-access-views).

In the alert condition, to query for task completion events, select rows where
`resource_attributes:"snow.executable.type" = 'TASK'`. To narrow down the list of events, you can filter on the following
columns:

- To restrict the results to tasks in a specific database, use `resource_attributes:"snow.database.name"`.
- To return events where the task execution failed, use `value:state = 'FAILED'`.

For information on the values logged for a task execution event, see
[Information logged for task events](#label-task-monitor-events-table-reference).

For example, the following statement creates an alert on new data that performs an action when task completions fail for tasks
in the database `my_db`. The example assumes that:

- Your active event table is the [default event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default) (SNOWFLAKE.TELEMETRY.EVENTS).
- You have [set up a webhook notification integration](/user-guide/notifications/webhook-notifications) for that Slack
  channel.

Copy code

```
CREATE ALERT my_alert_on_task_failures
  IF( EXISTS(
    SELECT * FROM SNOWFLAKE.TELEMETRY.EVENT_TABLE
      WHERE resource_attributes:"snow.executable.type" = 'task'
        AND resource_attributes:"snow.database.name" = 'my_db'
        AND record:"severity_text" = 'ERROR'
        AND value:"state" = 'FAILED'))
  THEN
    BEGIN
      LET result_str VARCHAR;
      (SELECT ARRAY_TO_STRING(ARRAY_AGG(name)::ARRAY, ',') INTO :result_str
         FROM (
           SELECT resource_attributes:"snow.executable.name"::VARCHAR name
             FROM TABLE(RESULT_SCAN(SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID()))
             LIMIT 10
         )
      );
      CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
        SNOWFLAKE.NOTIFICATION.TEXT_PLAIN(:result_str),
        '{"my_slack_integration": {}}'
      );
    END;
```

### Query the event table for task completion events

You can also query the event table for events that indicate that a task completion failed.

For information on the role that you need to use to query the event table and the conditions that you can use to filter the
results, see [Set up an alert on new data for task completion events](#label-task-monitor-events-alert).

For example, to get the timestamp, task name, query ID, and error message for errors with tasks in the database `my_db`:

Copy code

```
SELECT
    timestamp,
    resource_attributes:"snow.executable.name"::VARCHAR AS task_name,
    resource_attributes:"snow.query.id"::VARCHAR AS query_id,
    value:message::VARCHAR AS error
  FROM my_event_table
  WHERE
    resource_attributes:"snow.executable.type" = 'TASK' AND
    resource_attributes:"snow.database.name" = 'MY_DB' AND
    value:state = 'FAILED'
  ORDER BY timestamp DESC;
```

```
+-------------------------+-----------+--------------------------------------+------------------------------------------------------+
| TIMESTAMP               | TASK_NAME | QUERY_ID                             | ERROR                                                |
|-------------------------+-----------+--------------------------------------+------------------------------------------------------|
| 2025-02-18 00:21:19.461 | T1        | 01ba76b5-0107-e56d-0000-a995024f4222 | 002003: SQL compilation error:                       |
|                         |           |                                      | Object 'MY_TABLE' does not exist or not authorized.  |
+-------------------------+-----------+--------------------------------------+------------------------------------------------------+
```

The following example retrieves all columns for errors with tasks in the schema `my_schema`:

Copy code

```
SELECT *
  FROM my_event_table
  WHERE
    resource_attributes:"snow.executable.type" = 'FAILED' AND
    resource_attributes:"snow.schema.name" = 'MY_SCHEMA' AND
    value:state = 'FAILED'
  ORDER BY timestamp DESC;
```

```
+-------------------------+-----------------+-------------------------+-------+----------+------------------------------------------------------------+-------+------------------+-------------+-------------------------------+-------------------+------------------------------------------------------------------------------------------------------+-----------+
| TIMESTAMP               | START_TIMESTAMP | OBSERVED_TIMESTAMP      | TRACE | RESOURCE | RESOURCE_ATTRIBUTES                                        | SCOPE | SCOPE_ATTRIBUTES | RECORD_TYPE | RECORD                        | RECORD_ATTRIBUTES | VALUE                                                                                                | EXEMPLARS |
|-------------------------+-----------------+-------------------------+-------+----------+------------------------------------------------------------+-------+------------------+-------------+-------------------------------+-------------------+------------------------------------------------------------------------------------------------------+-----------|
| 2025-02-18 00:21:19.461 | NULL            | 2025-02-18 00:21:19.461 | NULL  | NULL     | {                                                          | NULL  | NULL             | EVENT       | {                             | NULL              | {                                                                                                    | NULL      |
|                         |                 |                         |       |          |   "snow.database.id": 49,                                  |       |                  |             |   "name": "execution.status", |                   |   "message": "002003: SQL compilation error:\nObject 'EMP_TABLE' does not exist or not authorized.", |           |
|                         |                 |                         |       |          |   "snow.database.name": "MY_DB",                        |       |                  |                |   "severity_text": "ERROR"    |                   |   "state": "FAILED"                                                                                  |           |
|                         |                 |                         |       |          |   "snow.executable.id": 518,                               |       |                  |             | }                             |                   | }                                                                                                    |           |
|                         |                 |                         |       |          |   "snow.executable.name": "T1",                            |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.executable.type": "TASK",                          |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.owner.id": 2601,                                   |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.owner.name": "DATA_ADMIN",                         |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.owner.type": "ROLE",                               |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.query.id": "01ba76b5-0107-e56d-0000-a995024f4222", |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.schema.id": 411,                                   |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.schema.name": "MY_SCHEMA",                      |       |                  |             |                               |                   |                                                                                                      |              |
|                         |                 |                         |       |          |   "snow.warehouse.id": 41,                                 |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          |   "snow.warehouse.name": "INTAKE_WAREHOUSE"                |       |                  |             |                               |                   |                                                                                                      |           |
|                         |                 |                         |       |          | }                                                          |       |                  |             |                               |                   |                                                                                                      |           |
+-------------------------+-----------------+-------------------------+-------+----------+------------------------------------------------------------+-------+------------------+-------------+-------------------------------+-------------------+------------------------------------------------------------------------------------------------------+-----------+
```

### Information logged for task events

When a task runs, an event is logged to the event table. The following sections describe the event table row that represents the
event:

- [Event table column values](#label-task-monitor-events-columns)
- [Key-value pairs in the column](#label-task-monitor-events-resource-attributes)
- [Key-value pairs in the column](#label-task-monitor-events-record)

## Event table column values

When a task completes or fails, a row with the following values is inserted into the event table.

Note

If a column is not listed below, the column value is NULL for the event.

| Column | Data type | Description |
| --- | --- | --- |
| `timestamp` | TIMESTAMP\_NTZ | The UTC timestamp when an event was created. |
| `observed_timestamp` | TIMESTAMP\_NTZ | A UTC time used for logs. Currently, this is the same value that is in the `timestamp` column. |
| `resource_attributes` | OBJECT | [Attributes](#label-task-monitor-events-resource-attributes) that identify the task that was executed. |
| `record_type` | STRING | The event type, which is `EVENT` for task executions. |
| `record` | OBJECT | [Details](#label-task-monitor-events-record) about the status of the task execution. |
| `value` | VARIANT | The [status](#label-task-monitor-events-value) of the task execution and, if the execution failed, the error message for the failure. |

Expand

Show lessSee more

## Key-value pairs in the `resource_attributes` column

The `resource_attributes` column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:

| Attribute name | Attribute type | Description | Example |
| --- | --- | --- | --- |
| `snow.database.id` | INTEGER | The internal/system-generated identifier of the database containing the task. | `12345` |
| `snow.database.name` | VARCHAR | The name of the database containing the task. | `MY_DATABASE` |
| `snow.executable.id` | INTEGER | The internal/system-generated identifier of the task that executed. | `12345` |
| `snow.executable.name` | VARCHAR | The name of the task that executed. | `MY_TASK` |
| `snow.executable.type` | VARCHAR | The type of the object. The value is `TASK` for task events. | `TASK` |
| `snow.owner.id` | INTEGER | The internal/system-generated identifier of the role with the OWNERSHIP privilege on the task. | `12345` |
| `snow.owner.name` | VARCHAR | The name of the role with the OWNERSHIP privilege on the task. | `MY_ROLE` |
| `snow.owner.type` | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. | `ROLE` |
| `snow.query.id` | VARCHAR | ID of the query that executed the task. | `01ba7614-0107-e56c-0000-a995024f304a` |
| `snow.schema.id` | INTEGER | The internal/system-generated identifier of the schema containing the task. | `12345` |
| `snow.schema.name` | VARCHAR | The name of the schema containing the task. | `MY_SCHEMA` |
| `snow.warehouse.id` | INTEGER | The internal/system-generated identifier of the warehouse used to execute the task. | `12345` |
| `snow.warehouse.name` | VARCHAR | The name of the warehouse used to execute the task. | `MY_WAREHOUSE` |

Expand

Show lessSee more

## Key-value pairs in the `record` column

The `record` column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:

| Key | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | VARCHAR | The name of the event. The value is `execution.status` for task executions. | `execution.status` |
| `severity_text` | VARCHAR | The severity level of the event, which is one of the following values:   - `INFO`: The task execution succeeded. - `ERROR`: The task execution failed. | `INFO` |

Expand

Show lessSee more

## Key-value pairs in the `value` column

The `value` column contains an [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value with the following key-value pairs:

| Key | Type | Description | Example |
| --- | --- | --- | --- |
| `state` | VARCHAR | The state of the task execution, which can be one of the following values:   - `SUCCEEDED`: The task execution succeeded. - `ERROR`: The task execution failed. | `SUCCEEDED` |
| `message` | VARCHAR | If the value in `state` is `ERROR`, this column includes the error message. |  |

Expand

Show lessSee more
