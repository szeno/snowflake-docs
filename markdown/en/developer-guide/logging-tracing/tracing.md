# Trace events for functions and procedures

You can emit trace events from the handler code for a procedure, UDF, or UDTF, including those you write
[using Snowpark APIs](/developer-guide/snowpark/index). For a list of supported handler languages, see
[Supported languages](#label-tracing-supported-languages).

Note

Before you can collect trace event data, you must [enable telemetry data collection](/developer-guide/logging-tracing/logging-tracing-enabling).
When you [instrument your code](#label-tracing-handler-code), Snowflake generates the data and collects it in an event table.

Trace events are a type of telemetry data (like log messages) that can capture when something has happened in the system or the
application. Unlike log messages, trace events have a structured payload, which makes them a good choice for data analysis. For example,
you can use trace events to capture some numbers that are calculated during the execution of your function, and analyze these numbers
afterwards.

In a procedure or UDF, you can associate attributes (key-value pairs) that should be captured as part of the trace events. For example,
if you want to capture the names and values of parameters in a trace event, you can add a trace event named `parameters` and set the
names and values of the parameters as attributes of the event.

When a procedure or function executes successfully, Snowflake emits the trace events that were added. Snowflake makes these trace events
available in the active event table associated with the account. For an explanation of event tables, see
[Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

You can [access trace event data](/developer-guide/logging-tracing/tracing-accessing-events) for analysis in the following ways:

- Execute a SELECT command on the event table.
- View trace entries in Snowsight.

## Trace example

Python code in the following example sets a `example.proc.do_tracing` attribute on the span with a value of `begin`. It also
emits within the span an `event_with_attributes` event with `example.key1` and `example.key2` attributes.

Copy code

```
CREATE OR REPLACE PROCEDURE do_tracing()
RETURNS VARIANT
LANGUAGE PYTHON
PACKAGES=('snowflake-snowpark-python')
RUNTIME_VERSION = 3.12
HANDLER='run'
AS $$
from snowflake import telemetry
def run(session):
  telemetry.set_span_attribute("example.proc.do_tracing", "begin")
  telemetry.add_event("event_with_attributes", {"example.key1": "value1", "example.key2": "value2"})
  return "SUCCESS"
$$;
```

## Getting started

To get started with event traces from handler code, follow these high-level steps:

1. [Set up an event table.](/developer-guide/logging-tracing/event-table-setting-up)

   Snowflake uses your event table to store event data emitted by your handler code. An event table has
   columns [predefined by Snowflake](/developer-guide/logging-tracing/event-table-columns).
2. Get acquainted with the event trace API for the handler language you’ll be using.

   see [Supported languages](#label-tracing-supported-languages) for a list of handler languages, then view
   [content about how to emit trace events from your language](#label-tracing-handler-code).
3. Add event trace code to your handler.
4. Learn how to [retrieve event trace data](/developer-guide/logging-tracing/tracing-accessing-events) from the event table.

## Level for trace events

You can manage the verbosity of trace event data stored in the event table by setting the trace level. Before tracing, use this setting
to ensure that you’re capturing the log message severity. If you find that event data isn’t being written to the table, check the trace
level to ensure that Snowflake is capturing the data you want.

For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

## Supported languages

You can trace events from code written in the following languages, including when handler code is written with
[Snowpark APIs](/developer-guide/snowpark/index).

| Language / Type | Java | Python | JavaScript | Scala | Snowflake Scripting |
| --- | --- | --- | --- | --- | --- |
| Stored procedure handler | ✔ | ✔ | ✔ | ✔ | ✔ |
| Streamlit app |  | ✔ |  |  |  |
| UDF handler (scalar function) | ✔ | ✔ | ✔ | ✔ |  |
| UDTF handler (table function) | ✔ | ✔ | ✔ | ✔ \* |  |

Expand

Show lessSee more

\*:
:   Scala UDTF handler written in Snowpark.

### Event tracing from handler code

To trace events, you can use a Snowflake-provided library designed for the handler code you’re using. Snowflake intercepts trace events and
stores them in the event table you create.

The following table lists handler languages supported for logging, along with links to content on logging from code.

| Language | Telemetry Library | Documentation |
| --- | --- | --- |
| Java | Snowflake `Telemetry` class. | [Emitting trace events in Java](/developer-guide/logging-tracing/tracing-java) |
| JavaScript | Snowflake JavaScript API. | [Emitting trace events in JavaScript](/developer-guide/logging-tracing/tracing-javascript) |
| Python | Snowflake `telemetry` package. | [Emitting trace events in Python](/developer-guide/logging-tracing/tracing-python) |
| Scala | Snowflake `Telemetry` class. | [Emitting trace events in Scala](/developer-guide/logging-tracing/tracing-scala) |
| Snowflake Scripting | Snowflake SQL functions. | [Emitting trace events in Snowflake Scripting](/developer-guide/logging-tracing/tracing-snowflake-scripting) |

Expand

Show lessSee more

### SQL statement tracing

By default when [tracing is enabled](/developer-guide/logging-tracing/logging-tracing-enabling), Snowflake traces SQL statements
executed in conjunction with other traced code, such as within the handler for a stored procedure or user-defined function.

By default, Snowflake traces SQL in the following contexts:

- SQL executed within a stored procedure
- SQL that executes a stored procedure
- SQL that executes one or more user defined functions
- SQL executed by DBT
- SQL executed by Streamlit
- SQL executed by a Notebook
- SQL executed in Snowpark Container Services when the code context is a Python or Go connector

Note that the following are not supported:

- SQL statements in a Snowflake Native App
- Direct execution of SQL in worksheets or workspaces

For a traced SQL statement, you can find emitted data in the event table, including in the following columns:

- In the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source), the `snow.executable.type` property
  value is `QUERY`.
- In the [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-span), the `name` property value is the type of SQL statement whose
  execution was traced, such as SELECT, CALL, or INSERT.
- In the [RECORD\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-attributes-span), the following properties contain values related to
  SQL tracing:
  - `db.query.table.names`
  - `db.query.view.names`
  - `db.query.executable.names`
  - `db.query.text` (if enabled)

You can specify whether the SQL text itself (up to 1024 characters) should be included among trace data captured in an event table. You
might want to omit the SQL text if it can contain sensitive information or if it would not be useful.

- To capture SQL text when tracing, set the [SQL\_TRACE\_QUERY\_TEXT](/sql-reference/parameters#label-sql-trace-query-text) parameter to `"ON"` (you must use the ACCOUNTADMIN
  role to set this parameter).

### General guidelines for adding trace events

When calling the trace event APIs to add trace events and set span attributes, note the following:

- A span can hold a maximum number of 128 trace events and a maximum number of 128 span attributes.
- If you add a trace event that has the same name as an event that you added earlier, a new event record is created.
- If you set a span attribute that has the same key as a span attribute that you set earlier, the value for that key is overwritten.

## Viewing collected event data

You can view trace data either through Snowsight or by querying the event table in which trace data is stored. For more information,
see [Viewing trace data](/developer-guide/logging-tracing/tracing-accessing-events).
