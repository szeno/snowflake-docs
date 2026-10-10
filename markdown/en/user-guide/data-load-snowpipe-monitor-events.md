# Monitor events for Snowpipe

Snowpipe can record events in your active event table as it processes files and as the state of a pipe changes. Use these events to do the following:

- Follow each file through a pipe, from the moment that Snowpipe receives it until it loads or fails.
- Find out when a Google Cloud Storage or Microsoft Azure notification channel can’t be read, which usually means a configuration problem such as missing permissions.
- See when a pipe pauses, resumes, stops, or is throttled.
- Measure how long Snowpipe takes to load each file.
- Get alerted when a pipe or a file has an error.

Pipes that load Apache Iceberg™ tables record the same events as pipes that load standard tables.

Note

Recording events in an event table incurs costs. For more information, see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

## Before you begin

Make sure that you have the following:

- **An active event table**: Snowflake writes Snowpipe events to the active event table that’s associated with the pipe. By default, that’s the account’s event table, `SNOWFLAKE.TELEMETRY.EVENTS`. If you associate a different event table with the account, or with the database that contains the pipe, pipe events go there instead. Notification channel events always go to the account’s event table. To find the account’s event table, run `SHOW PARAMETERS LIKE 'EVENT_TABLE' IN ACCOUNT;`. For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).
- **Privileges to set the event level**: To set the `LOG_EVENT_LEVEL` parameter, you need the `MODIFY LOG EVENT LEVEL` privilege on the account. To set it on a pipe, you also need the `OPERATE` or `OWNERSHIP` privilege on the pipe and the `USAGE` privilege on the database and schema that contain the pipe. To set it on a database or schema, you also need the `MODIFY` privilege on that database or schema. For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).
- **Privileges to query events**: To query `SNOWFLAKE.TELEMETRY.EVENTS`, use a role that’s granted the `SNOWFLAKE.EVENTS_ADMIN` application role. For read-only access that can’t delete events, use a role that’s granted the `SNOWFLAKE.EVENTS_VIEWER` application role, and query the `SNOWFLAKE.TELEMETRY.EVENTS_VIEW` view instead. For more information, see [Roles for access to the default event table and EVENTS\_VIEW](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).

## Enable Snowpipe events

Snowpipe records events only when the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter is set to a level other than `OFF`, which is the default. If `LOG_LEVEL` was set before the [2026\_02 behavior change bundle](/release-notes/bcr-bundles/2026_02/bcr-2229), `LOG_EVENT_LEVEL` was initialized to the same value, so Snowpipe might already record events. To check the account-level value, run `SHOW PARAMETERS LIKE 'LOG_EVENT_LEVEL' IN ACCOUNT;`.

You can set `LOG_EVENT_LEVEL` on the account, a database, a schema, or an individual pipe. A pipe that doesn’t have its own setting inherits the level from its schema, its database, or the account, in that order:

Copy code

```
-- Capture ERROR events for all pipes, and for other objects that record events.
ALTER ACCOUNT SET LOG_EVENT_LEVEL = ERROR;

-- Capture INFO events, and more severe events, for one pipe.
ALTER PIPE mydb.myschema.orders_pipe SET LOG_EVENT_LEVEL = INFO;
```

Keep the following in mind when you choose where to set the level:

- An account-level setting also records events from tasks, dynamic tables, and other features that write events to the event table, and those extra events add cost. To record events only for Snowpipe, set the level on individual pipes.
- A level that you set on a pipe applies only to that pipe, so set it again on pipes that you create or recreate later. To cover future pipes too, set the level on the schema or database that contains them. That setting also applies to other objects in the schema or database that record events.
- A level that you set on a pipe doesn’t record `notification_received` or `notification_channel_errored` events, because those events belong to a notification channel rather than a pipe. To record them, set `LOG_EVENT_LEVEL` on the account.

Snowpipe records events at the level that you set and at every more severe level. The following table shows the Snowpipe events that each level captures:

| Level | Events captured |
| --- | --- |
| `ERROR` | Files that failed to load, pipes that stopped or stalled because of an error, and notification channel errors (only when you set the level on the account) |
| `WARN` | The `ERROR` events, plus throttled pipes, cloned pipes, and pipes that Snowflake stopped (`STOPPED_BY_SNOWFLAKE_ADMIN` or `STOPPED_FEATURE_DISABLED`) |
| `INFO` | The `WARN` events, plus pipes that were paused or resumed |
| `DEBUG` | The `INFO` events, plus every file that Snowpipe receives, skips, and loads |
| `TRACE` | The `DEBUG` events, plus every event notification that Snowflake receives (only when you set the level on the account) |

Expand

Show lessSee more

`DEBUG` and `TRACE` record at least one event for each file, so they produce many more events, and higher costs, than the other levels. For continuous monitoring, start with `ERROR` or `WARN`, and use `DEBUG` when you need to follow individual files.

## Query Snowpipe events

The following examples query the default event table, `SNOWFLAKE.TELEMETRY.EVENTS`. Keep the following in mind:

- If you use a different event table, replace the table name. If the database that contains a pipe has its own event table, that pipe’s events go there, but notification channel events still go to the account’s event table. In that case, query both tables. To find a database’s event table, run `SHOW PARAMETERS LIKE 'EVENT_TABLE' IN DATABASE mydb;`.
- Examples that read fields from the `VALUE` column use `PARSE_JSON`. State values are uppercase, such as `RECEIVED`, `INGESTED`, and `FAILED`.
- Pipe names in event attributes are uppercase, unless you created the pipe with a quoted name.
- The `TIMESTAMP` column is a `TIMESTAMP_NTZ` value in UTC, so the examples compare it with `SYSDATE()`, which returns the current UTC time. Comparing it with `CURRENT_TIMESTAMP()` shifts the time range by your session’s offset from UTC.
- For the fields that each type of event records, see [Snowpipe event types](#label-snowpipe-events-types).

### Find recent errors

The following query returns the Snowpipe errors from the last 24 hours, including files that failed to load, notification channel errors, and pipes that stopped or stalled because of an error:

Copy code

```
SELECT timestamp,
       record:"name"::STRING AS event_name,
       resource_attributes:"snow.pipe.name"::STRING AS pipe_name,
       resource_attributes:"snow.notification_channel.name"::STRING AS notification_channel,
       record_attributes:"snow.file.path"::STRING AS file_path,
       value AS details
  FROM SNOWFLAKE.TELEMETRY.EVENTS
  WHERE record_type = 'EVENT'
    AND record:"name" IN ('file_lifecycle', 'notification_channel_errored', 'pipe_lifecycle')
    AND record:"severity_text" = 'ERROR'
    AND timestamp >= DATEADD('hour', -24, SYSDATE())
  ORDER BY timestamp DESC;
```

### Follow a file through a pipe

With `LOG_EVENT_LEVEL` set to `DEBUG` or `TRACE`, the following query returns the `file_lifecycle` events for a single file, in order:

Copy code

```
SELECT timestamp,
       resource_attributes:"snow.pipe.name"::STRING AS pipe_name,
       PARSE_JSON(value):state::STRING AS state,
       PARSE_JSON(value):first_error_message::STRING AS first_error_message
  FROM SNOWFLAKE.TELEMETRY.EVENTS
  WHERE record_type = 'EVENT'
    AND record:"name" = 'file_lifecycle'
    AND record_attributes:"snow.file.path" = '2026/10/02/orders_0001.json'
    AND timestamp >= DATEADD('day', -14, SYSDATE())
  ORDER BY timestamp;
```

For a file that loaded successfully, the query returns a `RECEIVED` state followed by an `INGESTED` state. For a file that failed, the last state is `FAILED`, and `first_error_message` shows the first error. If the pipe ignored the file because it already processed a file with the same path and name, the state is `SKIPPED`.

### Measure how long files take to load

With `LOG_EVENT_LEVEL` set to `DEBUG` or `TRACE`, the following query compares when Snowpipe received each file with when it loaded the file:

Copy code

```
SELECT record_attributes:"snow.file.path"::STRING AS file_path,
       MIN(IFF(PARSE_JSON(value):state::STRING = 'RECEIVED', timestamp, NULL)) AS received_at,
       MAX(IFF(PARSE_JSON(value):state::STRING = 'INGESTED', timestamp, NULL)) AS ingested_at,
       DATEDIFF('second', received_at, ingested_at) AS load_seconds
  FROM SNOWFLAKE.TELEMETRY.EVENTS
  WHERE record_type = 'EVENT'
    AND record:"name" = 'file_lifecycle'
    AND resource_attributes:"snow.database.name" = 'MYDB'
    AND resource_attributes:"snow.schema.name" = 'MYSCHEMA'
    AND resource_attributes:"snow.pipe.name" = 'ORDERS_PIPE'
    AND timestamp >= DATEADD('hour', -24, SYSDATE())
  GROUP BY file_path
  ORDER BY load_seconds DESC NULLS LAST;
```

To measure load times without recording `DEBUG` events, compare the `PIPE_RECEIVED_TIME` and `FIRST_COMMIT_TIME` columns of the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history).

## Get alerted about Snowpipe problems

To get notified as soon as Snowpipe records an error, create an [alert on new data](/user-guide/alerts#label-alerts-create-streaming) that checks the event table. You can also get notified through [error notifications](/user-guide/data-load-snowpipe-errors), which don’t need an event table. The following table compares the two options:

| Characteristic | Error notifications | Alert on Snowpipe events |
| --- | --- | --- |
| What it reports | Errors in files that fail to load | Errors in files, errors reading a Google Cloud Storage or Microsoft Azure notification channel, and pipes that stop or stall because of an error. If you also include `WARN` events in the alert’s condition, it reports throttled pipes and pipes that Snowflake stops. If you include `INFO` events, it also reports pipes that are paused or resumed. |
| Where it sends notifications | The messaging service of the cloud platform that hosts your Snowflake account | Any destination that a notification integration supports, such as email |
| Requirements | An error notification integration on the pipe. To report every file that contains an error, the pipe needs `ON_ERROR = SKIP_FILE`, which is the default. | `LOG_EVENT_LEVEL` set to `ERROR` or more verbose, change tracking on the event table, and a notification integration |
| Cost | No event logging or alert compute | Event logging, and the compute that the alert uses |

Expand

Show lessSee more

Use error notifications if you need to know only about files that fail to load, and you already consume messages from Amazon SNS, Google Cloud Pub/Sub, or Azure Event Grid. Use an alert on Snowpipe events in any of the following cases: you also want to know when a pipe stops or a notification channel fails, you want email notifications, or you want one alert to cover every pipe instead of setting an error notification integration on each pipe.

If a pipe uses `ON_ERROR = CONTINUE`, neither option reports the rows that Snowpipe skips: Snowpipe sends an error notification for a file only if no rows from it load, and a partially loaded file records an `INGESTED` event. To find partially loaded files, query the copy history for the `Partially loaded` status. To run the query on a schedule, use a [scheduled alert](/user-guide/alerts#label-alerts-type-scheduled).

Neither option tells you when event notifications stop arriving. For an alert that catches that problem, see [Get alerted when a pipe stops loading files](#label-snowpipe-events-alerts-idle).

### Create an alert on Snowpipe errors

Before you create the alert, complete the following steps:

1. Make sure that change tracking is enabled on the event table that the alert queries. It’s already enabled on `SNOWFLAKE.TELEMETRY.EVENTS`. For an event table that you created, run `ALTER TABLE mydb.myschema.my_events SET CHANGE_TRACKING = TRUE;`.
2. Set up an [email notification integration](/user-guide/notifications/email-notifications) that sets `DEFAULT_RECIPIENTS` to the addresses that should receive the alert. The example alert in this section doesn’t specify recipients, so it can’t send email unless the integration sets `DEFAULT_RECIPIENTS`.
3. Use a role that has the privileges to create an alert and to query the event table, as described in [Before you begin](#label-snowpipe-events-before-you-begin). For more information, see [Granting the privileges to create alerts](/user-guide/alerts#label-alerts-privileges-granting) and [Roles for access to the default event table and EVENTS\_VIEW](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).
4. If the database that contains a pipe has its own event table, create an alert on that table too, because that pipe’s events don’t go to the account’s event table.

The following example sends an email through the `my_email_integration` notification integration whenever Snowpipe records an `ERROR` event:

Copy code

```
CREATE OR REPLACE ALERT mydb.myschema.snowpipe_error_alert
  WAREHOUSE = my_warehouse
  IF (EXISTS (
    SELECT *
      FROM SNOWFLAKE.TELEMETRY.EVENTS
      WHERE record_type = 'EVENT'
        AND record:"name" IN ('file_lifecycle', 'notification_channel_errored', 'pipe_lifecycle')
        AND record:"severity_text" = 'ERROR'
  ))
  THEN
    CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
      SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('Snowpipe recorded an error. Check the event table for details.'),
      '{"my_email_integration": {}}'
    );

ALTER ALERT mydb.myschema.snowpipe_error_alert RESUME;
```

Because the alert has no schedule, Snowflake evaluates its condition whenever new rows arrive in the event table, which can be often. An alert that uses a warehouse incurs at least one minute of warehouse cost each time it runs. To reduce that cost, omit `WAREHOUSE` to create a [serverless alert](/user-guide/alerts#label-alerts-serverless-compute), which requires the `EXECUTE MANAGED ALERT` privilege on the account.

This alert catches only `ERROR` events. A pipe that Snowflake stops with `STOPPED_BY_SNOWFLAKE_ADMIN` or `STOPPED_FEATURE_DISABLED` records a `WARN` event, and so does a throttled pipe. To be alerted about them too, set `LOG_EVENT_LEVEL` to `WARN`, add `'pipe_throttled'` to the list of event names, and change the severity condition to `record:"severity_text" IN ('WARN', 'ERROR')`. With `WARN` events included, the alert can also fire when someone clones a database or schema that contains pipes, because each cloned pipe records a `pipe_lifecycle` event with the `STOPPED_CLONED` state.

### Get alerted when a pipe stops loading files

Error notifications and Snowpipe events report only problems that Snowflake detects. If event notifications stop arriving, for example after someone deletes the event notification on your bucket, Snowflake doesn’t record an error. To catch that problem, create a [scheduled alert](/user-guide/alerts) that calls [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) and checks whether `lastIngestedTimestamp` is older than the longest normal gap between your files. This alert doesn’t query the event table, so it works even if `LOG_EVENT_LEVEL` is `OFF`. The role that owns the alert needs the `MONITOR` or `OWNERSHIP` privilege on the pipe, or the `MONITOR EXECUTION` privilege on the account. For example, the following alert checks every hour and sends an email through the `my_email_integration` notification integration if `orders_pipe` hasn’t loaded a file in the last two hours:

Copy code

```
CREATE OR REPLACE ALERT mydb.myschema.orders_pipe_idle_alert
  WAREHOUSE = my_warehouse
  SCHEDULE = '60 MINUTE'
  IF (EXISTS (
    SELECT 1
      FROM (SELECT PARSE_JSON(SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe')) AS pipe_status)
      WHERE pipe_status:lastIngestedTimestamp::TIMESTAMP_LTZ < DATEADD('hour', -2, CURRENT_TIMESTAMP())
  ))
  THEN
    CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
      SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('orders_pipe has not loaded a file in the last 2 hours.'),
      '{"my_email_integration": {}}'
    );

ALTER ALERT mydb.myschema.orders_pipe_idle_alert RESUME;
```

If the pipe hasn’t loaded any files yet, for example right after you create or recreate it, `SYSTEM$PIPE_STATUS` doesn’t return `lastIngestedTimestamp`, and this alert doesn’t send an email. While the pipe stays idle, the alert sends an email every hour. To stop the emails while you investigate, run `ALTER ALERT mydb.myschema.orders_pipe_idle_alert SUSPEND;`.

## Snowpipe event types

The `name` key in the `RECORD` column identifies the type of each Snowpipe event:

| Event | When Snowpipe records it | Severity |
| --- | --- | --- |
| [file\_lifecycle](#label-snowpipe-events-file-lifecycle) | When Snowpipe receives a file, skips it, loads it, or fails to load it | `DEBUG` when a file is received, skipped, or loaded; `ERROR` when it fails to load |
| [notification\_received](#label-snowpipe-events-notification-received) | When Snowflake receives an event notification | `TRACE` |
| [notification\_channel\_errored](#label-snowpipe-events-notification-channel-errored) | When Snowflake can’t read messages from a notification channel | `ERROR` |
| [pipe\_lifecycle](#label-snowpipe-events-pipe-lifecycle) | When the state of a pipe changes | `INFO` when you pause or resume a pipe; `WARN` or `ERROR` when it stops or stalls |
| [pipe\_throttled](#label-snowpipe-events-pipe-throttled) | When Snowflake temporarily stops adding files to a pipe’s queue because of a rate limit | `WARN` |

Expand

Show lessSee more

### file\_lifecycle

Snowpipe records a `file_lifecycle` event at each step of a file’s progress through a pipe. The `RECORD_ATTRIBUTES` column contains the path of the file in `snow.file.path`.

When Snowpipe receives a request to load a file, it records an event with a `state` value of `RECEIVED`. If the pipe already processed a file with the same path and name, the state is `SKIPPED` instead. `SKIPPED` doesn’t mean that the file had errors: a file that doesn’t load because of errors, including under `ON_ERROR = SKIP_FILE`, has the `FAILED` state, as shown later in this section. The following example shows a `RECEIVED` or `SKIPPED` event:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.database.name": "<MY_DB_NAME>",
    "snow.schema.name": "<MY_SCHEMA_NAME>",
    "snow.pipe.name": "<MY_PIPE_NAME>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "file_lifecycle",
    "severity_text": "DEBUG"
  },
  "RECORD_ATTRIBUTES": {
    "snow.file.path": "<a/path/to/a/file>"
  },
  "VALUE": {
    "notification_channel": "<notification_channel>",
    "file_content_key": "<file_content_key>",
    "last_modified_time": "<last_modified_time>",
    "state": "<RECEIVED_or_SKIPPED>"
  }
}
```

After Snowpipe loads the file, it records an event with a `state` value of `INGESTED`. Snowpipe also records `INGESTED` for a file that loads partially, for example with `ON_ERROR = CONTINUE`. The following example shows an `INGESTED` event:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.database.name": "<MY_DB_NAME>",
    "snow.schema.name": "<MY_SCHEMA_NAME>",
    "snow.pipe.name": "<MY_PIPE_NAME>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "file_lifecycle",
    "severity_text": "DEBUG"
  },
  "RECORD_ATTRIBUTES": {
    "snow.file.path": "<a/path/to/a/file>"
  },
  "VALUE": {
    "notification_channel": "<notification_channel>",
    "file_content_key": "<file_content_key>",
    "state": "INGESTED"
  }
}
```

If Snowpipe doesn’t load the file because of errors, it records an `ERROR` event with a `state` value of `FAILED`. The event includes the first error in the file, where the error occurred, and how many errors the file contains:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.database.name": "<MY_DB_NAME>",
    "snow.schema.name": "<MY_SCHEMA_NAME>",
    "snow.pipe.name": "<MY_PIPE_NAME>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "file_lifecycle",
    "severity_text": "ERROR"
  },
  "RECORD_ATTRIBUTES": {
    "snow.file.path": "<a/path/to/a/file>"
  },
  "VALUE": {
    "notification_channel": "<notification_channel>",
    "file_content_key": "<file_content_key>",
    "first_error_message": "<first_error_message>",
    "first_error_line_number": "<some_number>",
    "first_error_character_pos": "<some_character_pos>",
    "error_count": "<error_count>",
    "error_limit": "<error_limit>",
    "state": "FAILED"
  }
}
```

### notification\_received

Snowflake records a `notification_received` event when it receives an event notification from your cloud storage service. The `RESOURCE_ATTRIBUTES` column identifies the notification channel rather than a pipe, because one channel can serve several pipes. The following example shows a `notification_received` event:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.notification_channel.name": "<notification_channel_name>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "notification_received",
    "severity_text": "TRACE"
  },
  "VALUE": {
    "file_path": "<a/path/to/a/file>",
    "file_content_key": "<file_content_key>",
    "upstream_event_time": "<upstream_event_time>"
  }
}
```

### notification\_channel\_errored

Snowflake records a `notification_channel_errored` event when it can’t read messages from a notification channel. Snowflake records this event for Google Cloud Storage and Microsoft Azure notification channels. The error usually means a configuration problem, such as missing permissions on the notification channel. The following example shows a `notification_channel_errored` event:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.notification_channel.name": "<notification_channel_name>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "notification_channel_errored",
    "severity_text": "ERROR"
  },
  "VALUE": {
    "first_error_message": "<error_message>"
  }
}
```

### pipe\_lifecycle

Snowpipe records a `pipe_lifecycle` event when the [state of a pipe](/sql-reference/functions/system_pipe_status#label-snowpipe-status) changes. When you pause or resume the pipe itself with `PIPE_EXECUTION_PAUSED`, the event has `INFO` severity:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.database.name": "<MY_DB_NAME>",
    "snow.schema.name": "<MY_SCHEMA_NAME>",
    "snow.pipe.name": "<MY_PIPE_NAME>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "pipe_lifecycle",
    "severity_text": "INFO"
  },
  "VALUE": {
    "state": "<RUNNING_or_PAUSED>"
  }
}
```

When a pipe stops processing files, its state starts with `STOPPED_` or `STALLED_`, and the event includes an error message:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.database.name": "<MY_DB_NAME>",
    "snow.schema.name": "<MY_SCHEMA_NAME>",
    "snow.pipe.name": "<MY_PIPE_NAME>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "pipe_lifecycle",
    "severity_text": "<WARN_or_ERROR>"
  },
  "VALUE": {
    "state": "<pipe_status>",
    "error_message": "<error_message>"
  }
}
```

The severity depends on why the pipe stopped:

- `WARN`: `STOPPED_BY_SNOWFLAKE_ADMIN`, `STOPPED_CLONED`, or `STOPPED_FEATURE_DISABLED`.
- `ERROR`: `STOPPED_STAGE_ALTERED`, `STOPPED_STAGE_DROPPED`, `STOPPED_NOTIFICATION_INTEGRATION_DROPPED`, `STOPPED_MISSING_PIPE`, `STOPPED_MISSING_TABLE`, `STALLED_COMPILATION_ERROR`, `STALLED_INITIALIZATION_ERROR`, `STALLED_EXECUTION_ERROR`, `STALLED_INTERNAL_ERROR`, or `STALLED_STAGE_PERMISSION_ERROR`.

For what each state means and how to fix it, see [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states).

### pipe\_throttled

Snowpipe records a `pipe_throttled` event when Snowflake temporarily stops adding files to a pipe’s queue, because the account, the pipe, or the target table exceeded the rate at which Snowpipe accepts new files. The event lists the files that Snowflake didn’t add to the queue. For a pipe that uses automated loading, Snowflake retries these files from the event notifications later, so they load after a delay. If you call the Snowpipe REST API, throttled requests fail with HTTP error `429`, so submit those files again. If `pipe_throttled` events continue, contact [Snowflake Support](/user-guide/contacting-support). The following example shows a `pipe_throttled` event:

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "snow.database.name": "<MY_DB_NAME>",
    "snow.schema.name": "<MY_SCHEMA_NAME>",
    "snow.pipe.name": "<MY_PIPE_NAME>"
  },
  "RECORD_TYPE": "EVENT",
  "RECORD": {
    "name": "pipe_throttled",
    "severity_text": "WARN"
  },
  "VALUE": {
    "throttled_files": "<throttled_file_name_list>"
  }
}
```

## Event table columns for Snowpipe events

Snowpipe events populate the following columns in the event table, and leave all other columns `NULL`:

| Column | Data type | Description |
| --- | --- | --- |
| `TIMESTAMP` | `TIMESTAMP_NTZ` | The UTC time when the event was created. |
| `RESOURCE_ATTRIBUTES` | `OBJECT` | The object that the event is about: the database, schema, and pipe, or the notification channel. See the next table. |
| `RECORD_TYPE` | `STRING` | The type of record. For Snowpipe events, this value is always `EVENT`. |
| `RECORD` | `OBJECT` | The name of the event, in the `name` key, and its severity, in the `severity_text` key. |
| `RECORD_ATTRIBUTES` | `OBJECT` | For `file_lifecycle` events, the path of the file, in the `snow.file.path` key. |
| `VALUE` | `VARIANT` | Details that depend on the event type, such as the state of a file or a pipe, or an error message. For examples, see [Snowpipe event types](#label-snowpipe-events-types). |

Expand

Show lessSee more

The `RESOURCE_ATTRIBUTES` column contains the following keys:

| Key | Data type | Description | Example |
| --- | --- | --- | --- |
| `snow.database.name` | `VARCHAR` | The name of the database that contains the pipe. | `"MYDB"` |
| `snow.schema.name` | `VARCHAR` | The name of the schema that contains the pipe. | `"MYSCHEMA"` |
| `snow.pipe.name` | `VARCHAR` | The name of the pipe. | `"ORDERS_PIPE"` |
| `snow.notification_channel.name` | `VARCHAR` | For notification events, the name of the notification channel that received the message or encountered the error. | `"arn:aws:sqs:us-west-2:123456789012:sf-snowpipe-AIDA3"` |

Expand

Show lessSee more
