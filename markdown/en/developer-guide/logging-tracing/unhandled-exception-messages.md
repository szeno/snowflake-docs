# Capturing messages from unhandled exceptions

By default, when you’ve [set up an event table](/developer-guide/logging-tracing/event-table-setting-up), Snowflake automatically logs
unhandled exceptions in procedure and UDF handlers in the event table. Capturing these messages does not require that you add handler
code specific to logging or tracing. You can disable this feature so that unhandled exceptions aren’t automatically logged.

Important

Error messages can contain sensitive information. Consider disabling this feature if you don’t want potentially sensitive
information captured in an event table. To learn more, see [Protecting sensitive data](#label-unhandled-exception-protect-sensitive-data).

## Configuring logging and tracing to capture unhandled exceptions

Set log or trace level so that Snowflake captures entries for unhandled exceptions. You can have entries captured as log entries, trace
event entries, or both.

- To capture messages as log entries, [set the log level](/developer-guide/logging-tracing/telemetry-levels) to `ERROR` or
  more verbose.
- To capture messages as trace event entries, [set the trace level](/developer-guide/logging-tracing/telemetry-levels) to
  `ALWAYS` or `ON_EVENT`.

## Data captured for unhandled exceptions

You can capture message data as a log entry, a trace event, or both. The captured data will differ between log and trace event entries.

### Data captured in a log entry

By default, Snowflake records the following in the event table for unhandled exceptions in procedure and UDF handlers:

| Column | Data |
| --- | --- |
| [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column) | A `severity_text` attribute whose value is the highest-severity error level for the current language runtime. For example, for a handler written in Python, the value is `FATAL`. |
| [RECORD\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-attributes-column) | The following attributes are recorded for an unhandled exception.   - `exception.message` – The error message. - `exception.type` – The name of the exception’s class. - `exception.stacktrace` – The exception’s stack trace formatted by a language runtime. - `exception.escaped` – `true` if this entry is from an unhandled exception. |
| [VALUE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-value-column) | The string `exception`. |

Expand

Show lessSee more

#### Example

Code in the following example queries an event table for log data recorded for an unhandled exception from a UDF handler.

For more about querying an event table for log data, see [Viewing log messages](/developer-guide/logging-tracing/logging-accessing-messages).

Copy code

```
SET event_table_name = 'my_db.public.my_event_table';

SELECT
  RECORD['severity_text'] AS severity,
  RECORD_ATTRIBUTES['exception.message'] AS error_message,
  RECORD_ATTRIBUTES['exception.type'] AS exception_type,
  RECORD_ATTRIBUTES['exception.stacktrace'] AS stacktrace
FROM
  my_event_table
WHERE
  RECORD_TYPE = 'LOG';
```

The following is possible output from the query.

```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| SEVERITY | ERROR_MESSAGE                                        | EXCEPTION_TYPE | STACKTRACE                                                                                                                                          |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| "FATAL"  | "could not convert string to float: '$1,000,000.00'" | "ValueError"   | "Traceback (most recent call last):\n  File \"_udf_code.py\", line 6, in compute\nValueError: could not convert string to float: '$1,000,000.00'\n" |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

### Data captured in a trace event entry

By default, Snowflake records the following in the event table for unhandled exceptions in procedure and UDF handlers:

| Column | Data |
| --- | --- |
| [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column) | A `name` attribute whose value is `exception` and a `status` attribute whose value is `STATUS_CODE_ERROR`. |
| [RECORD\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-attributes-column) | The following attributes are recorded for an unhandled exception.   - `exception.message` – The error message. - `exception.type` – The name of the exception’s class. - `exception.stacktrace` – The exception’s stack trace formatted by a language runtime. - `exception.escaped` – `true` if this entry is from an unhandled exception. |

Expand

Show lessSee more

#### Examples

Code in the following examples query an event table for trace event data recorded for an unhandled exception from a UDF handler.

For more about querying an event table for trace event data, see [Viewing trace data](/developer-guide/logging-tracing/tracing-accessing-events).

##### Span example

Copy code

```
SET event_table_name = 'my_db.public.my_event_table';

SELECT
  RECORD['status']['code'] AS span_status
FROM
  my_event_table
WHERE
  record_type = 'SPAN';
```

The following is possible output from the query.

```
-----------------------
| SPAN_STATUS         |
-----------------------
| "STATUS_CODE_ERROR" |
-----------------------
```

##### Span event example

Copy code

```
SET event_table_name = 'my_db.public.my_event_table';

SELECT
  RECORD['name'] AS event_name,
  RECORD_ATTRIBUTES['exception.message'] AS error_message,
  RECORD_ATTRIBUTES['exception.type'] AS exception_type,
  RECORD_ATTRIBUTES['exception.stacktrace'] AS stacktrace
FROM
  my_event_table
WHERE
  RECORD_TYPE = 'SPAN_EVENT';
```

The following is possible output from the query.

```
-----------------------------------------------------------------------------------------------------------------------------------------
| EVENT_NAME  | ERROR_MESSAGE                                        | EXCEPTION_TYPE | STACKTRACE                                      |
-----------------------------------------------------------------------------------------------------------------------------------------
| "exception" | "could not convert string to float: '$1,000,000.00'" | "ValueError"   | "  File \"_udf_code.py\", line 6, in compute\n" |
-----------------------------------------------------------------------------------------------------------------------------------------
```

## Protecting sensitive data

Given that log and trace messages from unhandled exceptions can include sensitive data, consider doing the following to protect that data:

- Take steps to protect sensitive data, such as by doing the following:

  - Improve your exception handling code to minimize the risk of unhandled exceptions.
  - Apply [row access policies](/user-guide/security-row-intro) to your event table to restrict access to rows that contain
    personally identifiable information (PII).
  - [Create a view](/sql-reference/sql/create-view) on top of the event table and
    [apply masking policies](/sql-reference/sql/create-masking-policy) to it to mask or delete personally identifiable
    information (PII).
- Turn off unhandled exception logging by setting the [ENABLE\_UNHANDLED\_EXCEPTIONS\_REPORTING](/sql-reference/parameters#label-disable-unhandled-exceptions-reporting) parameter to `false`.
