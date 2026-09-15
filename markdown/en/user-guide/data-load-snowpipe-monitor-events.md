# Monitor events for Snowpipe

You can configure Snowflake to record events that provide detailed information about the status of your pipes. These events are captured in the active event table associated with the pipe.

By monitoring these events, you can gain insights into the following areas:

- Pipe status changes: Track the operational state of your Snowpipes.
- File processing progress: Understand the journey of files through the Snowpipe system.
- Periodic, aggregated, ingestion statistics digest: Get summarized statistics on data ingestion.

Additionally, you can configure alerts for the following critical conditions:

- High volume of incoming files
- High ingestion latencies
- Pipe errors
- File errors

The following sections explain how to enable event logging for Snowpipe, configure the severity level for log events, and interpret the events recorded in the event table:

- Snowpipe event types: Learn about the different categories of events and their details.
- Set the severity level of events to capture: Configure which events are recorded based on their importance.
- Query the event table for Snowpipe events: Discover how to retrieve and analyze event data.
- Information logged for Snowpipe events: Understand the structure and meaning of the data within the event table columns.

Caution

Logging events for Snowpipe incurs costs. For more information, see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

## Snowpipe event types

Snowpipe events are identified by the `name` attribute within the `RECORD` column of your event table.

### file\_lifecycle

`file_lifecycle` events track a file’s journey through the Snowpipe system. The state of a file can be `RECEIVED`, `INGESTED`, or `ERRORED`.

`RECEIVED`: An event is emitted when Snowpipe receives a file request. The pipe might skip this file if it was previously processed; in such cases, the `skipped` attribute indicates this.

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
    "state": "<received_or_skipped>"
  }
}
```

`INGESTED`: An event is emitted after the file is successfully ingested by Snowpipe.

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
    "state": "ingested"
  }
}
```

`ERRORED`: An event is emitted if the file failed to be ingested by Snowpipe.

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
    "file_state": "FAILED"
  }
}
```

### notification\_received

This event is emitted when Snowflake receives a notification message.

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "notification_channel_name": "<notification_channel_name>"
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

This event is emitted when an error occurs while Snowflake is reading messages from a notification channel. This typically indicates a user configuration error, such as an authorization issue.

Copy code

```
{
  "TIMESTAMP": "<some_timestamp>",
  "RESOURCE_ATTRIBUTES": {
    "notification_channel_name": "<notification_channel_name>"
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

This event is emitted when the [status of a pipe](/sql-reference/functions/system_pipe_status#label-snowpipe-status) changes. The new status can be `RUNNING`, `PAUSED`, `STOPPED`, or `STALLED`.

For RUNNING or PAUSED pipe statuses:

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
    "state": "<running_or_paused>"
  }
}
```

For STOPPED\_\* or STALLED\_\* pipe statuses: These statuses indicate that a pipe has unexpectedly stopped processing files.

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

The `severity_text` for `STOPPED_*` or `STALLED_*` states depends on the specific reason:

`WARN` if the pipe stopped because of the following reasons:

- `STOPPED_BY_SNOWFLAKE_ADMIN`
- `STOPPED_CLONED`
- `STOPPED_FEATURE_DISABLED`

`ERROR` if the pipe stopped because of the following reasons:

- `STOPPED_STAGE_ALTERED`
- `STOPPED_STAGE_DROPPED`
- `STOPPED_FILE_FORMAT_DROPPED`
- `STOPPED_NOTIFICATION_INTEGRATION_DROPPED`
- `STOPPED_MISSING_PIPE`
- `STOPPED_MISSING_TABLE`
- `STALLED_COMPILATION_ERROR`
- `STALLED_INITIALIZATION_ERROR`
- `STALLED_EXECUTION_ERROR`
- `STALLED_INTERNAL_ERROR`
- `STALLED_STAGE_PERMISSION_ERROR`

### pipe\_throttled

This event is emitted if a Snowpipe is throttled.

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

## Set the severity level of events to capture

To enable Snowpipe events to be recorded in an event table, you must set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter at either the pipe level or the account level. `LOG_EVENT_LEVEL` determines which log events are captured based on their severity. For more information, see [Parameters](/sql-reference/parameters) and [New LOG\_EVENT\_LEVEL parameter to control events](/release-notes/bcr-bundles/2026_02/bcr-2229).

- `ERROR`: Use for events that signal a change that requires human intervention to resolve.
- `WARN`: Use for events that signal an issue that can be resolved without human intervention.
- `INFO`: Use for user-initiated events that are generally useful and aren’t high- volume events.
- `DEBUG`: Use for high-volume events.
- `TRACE`: The lowest level of logging, that captures very detailed information.

Caution

If the severity level isn’t set at the account level or pipe level, no events are captured.

**Examples:**

To capture ERROR-level events for all objects in an account, run the following code:

Copy code

```
ALTER ACCOUNT <my_account_name> SET LOG_EVENT_LEVEL = ERROR;
```

To capture INFO-level events for a specific pipe, run the following code:

Copy code

```
ALTER PIPE <my_pipe_name> SET LOG_EVENT_LEVEL = INFO;
```

## Severity level for each event type

The following table summarizes the default or recommended severity for each Snowpipe event type when you use `LOG_EVENT_LEVEL`:

| Event | Severity |
| --- | --- |
| file\_lifecycle - RECEIVED, INGESTED | DEBUG |
| file\_lifecycle - ERRORED | ERROR |
| notification\_received | TRACE |
| notification\_channel\_errored | ERROR |
| pipe\_lifecycle - RUNNING, PAUSED | INFO |
| pipe\_lifecycle - STOPPED | WARN or ERROR (see the following section) |
| pipe\_throttled | WARN |

Expand

Show lessSee more

**pipe\_lifecycle - STOPPED severity details:**

`WARN` if the pipe stopped because of the following reasons:

- `STOPPED_BY_SNOWFLAKE_ADMIN`
- `STOPPED_CLONED`
- `STOPPED_FEATURE_DISABLED`

`ERROR` if the pipe stopped because of the following reasons:

- `STOPPED_STAGE_ALTERED`
- `STOPPED_STAGE_DROPPED`
- `STOPPED_FILE_FORMAT_DROPPED`
- `STOPPED_NOTIFICATION_INTEGRATION_DROPPED`
- `STOPPED_MISSING_PIPE`
- `STOPPED_MISSING_TABLE`
- `STALLED_COMPILATION_ERROR`
- `STALLED_INITIALIZATION_ERROR`
- `STALLED_EXECUTION_ERROR`
- `STALLED_INTERNAL_ERROR`
- `STALLED_STAGE_PERMISSION_ERROR`

## Query the event table for Snowpipe events

Before you query, ensure that you have set up an event table and configured the severity level you want for events to be captured.

The following example query shows how to retrieve Snowpipe events, such as those generated during file ingestion:

Copy code

```
SELECT
    record_type,
    record:"name" AS event_name,
    record:"severity_text" AS log_level,
    resource_attributes:"snow.database.name" AS database_name,
    resource_attributes:"snow.schema.name" AS schema_name,
    resource_attributes:"snow.pipe.name" AS pipe_name,
    record_attributes,
    PARSE_JSON(value):file_content_key AS file_content_key,
    PARSE_JSON(value):state AS state
FROM {my_event_table_name}
ORDER BY state;
```

**Example output (successful file ingestion):**

The following output shows both RECEIVED and INGESTED events for a file, which indicates successful processing:

| SCOPE | RECORD\_TYPE | EVENT\_NAME | LOG\_LEVEL | DATABASE\_NAME | SCHEMA\_NAME | PIPE\_NAME | RECORD\_ATTRIBUTES | FILE\_CONTENT\_KEY | STATE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [NULL] | EVENT | “file\_lifecycle” | “DEBUG” | “TESTDB” | “TESTSH” | “MYPIPE” | { “snow.file.path”: “data\_0\_0\_0.event” } | “ba1f2511fc30423bdbb183fe33f3dd0f” | “INGESTED” |
| [NULL] | EVENT | “file\_lifecycle” | “DEBUG” | “TESTDB” | “TESTSH” | “MYPIPE” | { “snow.file.path”: “data\_0\_0\_0.event” } | “ba1f2511fc30423bdbb183fe33f3dd0f” | “RECEIVED” |

Expand

Show lessSee more

## Information logged for Snowpipe events

The following sections describe the key columns and their contents within the event table for Snowpipe events. If a column isn’t explicitly listed in the following sections, its value is NULL for Snowpipe events.

## Event table column values

| Column | Data Type | Description |
| --- | --- | --- |
| timestamp | TIMESTAMP\_NTZ | The UTC timestamp when the event was created. |
| resource\_attributes | OBJECT | Attributes that identify the Snowpipe event, such as database, schema, and pipe names. |
| record\_type | STRING | The type of event recorded. For Snowpipe events, this value is always EVENT. |
| record | OBJECT | Contains detailed information about the status of running the Snowpipe event, including name and severity\_text. |
| value | VARIANT | Additional information specific to the Snowpipe event. If the Snowpipe task failed, this includes the error message. |

Expand

Show lessSee more

## Key-value pairs in the resource\_attributes column

The `resource_attributes` column contains an OBJECT value with the following key-value pairs:

| Attribute Name | Attribute Type | Description | Example |
| --- | --- | --- | --- |
| snow.database.name | VARCHAR | The name of the database associated with the pipe. | “MY\_DATABASE” |
| snow.schema.name | VARCHAR | The name of the schema associated with the pipe. | “MY\_SCHEMA\_NAME” |
| snow.pipe.name | VARCHAR | The name of the pipe. | “MY\_PIPE\_NAME” |
| notification\_channel\_name | VARCHAR | The name of the notification channel that received the message or encountered an error. | “arn:aws:sqs:us-west-2:774383465531:sf-snowpipe-AIDA3” |

Expand

Show lessSee more

## Key-value pairs in the record column

The `record` column contains an OBJECT value with the following key-value pairs:

| Key | Type | Description | Example |
| --- | --- | --- | --- |
| name | VARCHAR | The name of the event. | “pipe\_lifecycle” |
| severity\_text | VARCHAR | The severity level of the event. | “INFO” |

Expand

Show lessSee more
