# How Snowflake represents trace events

Internally, Snowflake uses the [OpenTelemetry](https://opentelemetry.io/) data model to represent trace events inside an object called a span. A [span](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/api.md#span)
describes an operation, such as the invocation of a stored procedure or the execution of a UDF over a set of rows. A span includes the
start time and end time of the operation.

Tip

For guidelines to keep in mind when adding trace events, see [General guidelines for adding trace events](/developer-guide/logging-tracing/tracing#label-tracing-general-guidelines-adding).

## How Snowflake emits trace events

For a stored procedure or UDF, Snowflake may execute it in parallel when it is called, where each parallel execution unit executes on a different
set of rows. Any trace events that are emitted are scoped to their execution unit and are wrapped inside the same span.

For a Streamlit app, each user session is captured in a single span.

Trace events are emitted only after their execution unit completes. If the execution unit fails before completion, trace events from that
execution unit are not guaranteed to be emitted.

Trace events from different execution units are stored in separate rows of the event table (in other words, in different spans).

Note

Because UDFs are applied per input table row, calls to trace event APIs in your UDF are executed for each input table row. Adding a trace
event for every row is inadvisable in most cases. There is a limit of 128 events per execution unit.

## Example: Emitting events from a Java procedure

The following example illustrates how you can emit events from handler code. It also shows how the generated event data is stored in an
event table.

### Stored procedure with Java handler

The Java code in the following example illustrates how you can add events to a span, along with attribute data. For more information about
APIs for handler languages, see [Event tracing from handler code](/developer-guide/logging-tracing/tracing#label-tracing-handler-code).

Copy code

```
CREATE OR REPLACE PROCEDURE test_stored_proc()
RETURNS STRING
LANGUAGE JAVA
RUNTIME_VERSION = '11'
PACKAGES=('com.snowflake:snowpark:latest', 'com.snowflake:telemetry:latest')
HANDLER = 'MyClass.run'
AS
$$
  import com.snowflake.snowpark_java.Session;
  import com.snowflake.telemetry.Telemetry;
  import io.opentelemetry.api.common.AttributeKey;
  import io.opentelemetry.api.common.Attributes;
  import io.opentelemetry.api.common.AttributesBuilder;

  public class MyClass {

    public String run(Session session) {
      // Adding an event without attributes.
      Telemetry.addEvent("testEvent");

      // Adding an event with attributes.
      Attributes eventAttributes = Attributes.of(
          AttributeKey.stringKey("key"), "run",
          AttributeKey.longKey("result"), Long.valueOf(123));
      Telemetry.addEvent("testEventWithAttributes", eventAttributes);

      // Setting span attributes of different types.
      Telemetry.setSpanAttribute("example.boolean", true);
      Telemetry.setSpanAttribute("example.long", 2L);
      Telemetry.setSpanAttribute("example.double", 2.5);
      Telemetry.setSpanAttribute("example.string", "testAttribute");

      return "SUCCESS";
    }
  }
$$;
```

### Span data recorded

After the function or procedure executes successfully, Snowflake renders the OpenTelemetry span object as objects in columns of the
event table, as shown in the following tables.

A span can have its own attributes. Since a span represents a stored procedure and UDF execution unit, you might find it useful to set
span-level attributes for later data analysis. For more information about how to set span attributes, see the content
specific to the language in which you’re writing handler code. For a list of these languages, see [Event tracing from handler code](/developer-guide/logging-tracing/tracing#label-tracing-handler-code).

A span can hold a maximum number of 128 trace events and a maximum number of 128 span attributes.

- If the number of trace events exceeds the limit, events are dropped as follows, depending on the handler language:

  - For Python handlers, events are dropped in the order in which they were added (in other words, in first-in-first-out order).
  - For handlers written in Java, JavaScript, Scala, and Snowflake Scripting, new events are dropped once the limit has been reached.
- If the number of span attributes exceeds the limit, no more span attributes can be added.

Note

As of November 2022, all `dropped_*_count` keys are not set for JavaScript because the OpenTelemetry JavaScript Tracing SDK does
not report on dropped counts.

| Description | Data |
| --- | --- |
| Span recorded by Snowflake for the execution of the procedure containing the handler code. | - Start timestamp from the START\_TIMESTAMP column:   `2023-03-21 23:12:06.231`   - Finish timestamp from the TIMESTAMP column:   `2023-03-21 23:12:06.944`   - Data from the RECORD column:   Copy code  ``` {   "kind": "SPAN_KIND_INTERNAL",   "name": "snow.auto_instrumented",   "status": {     "code": "STATUS_CODE_UNSET"   } } ``` |
| Attributes added by handler code for the span. | - Data from the RECORD\_ATTRIBUTES column:   Copy code  ``` {   "example.boolean": true,   "example.double": 2.5,   "example.long": 2,   "example.string": "testAttribute" } ``` |

Expand

Show lessSee more

### Event data recorded

The span contains a list of trace events with timestamps that capture when the trace
events were added. Not shown here: The span has a `trace_id` which is the query ID without dashes. The span also has system-generated
values for the `span_id` and `name` keys. Events that are part of the span share the same `span_id`.

The following data was recorded for the event `testEvent`.

| Description | Data |
| --- | --- |
| Event name | - Timestamp from the TIMESTAMP column:   `2023-03-21 23:12:06.939`   - Data from the RECORD column:   Copy code  ``` {   "dropped_attributes_count": 0,   "name": "testEvent" } ``` |

Expand

Show lessSee more

The following data recorded for the event `testEventWithAttributes`.

| Description | Data |
| --- | --- |
| Event name | - Timestamp from the TIMESTAMP column:   `2023-03-21 23:12:06.940`   - Data from the RECORD column:   Copy code  ``` {   "dropped_attributes_count": 0,   "name": "testEventWithAttributes" } ``` |
| Event attributes | - Data from the RECORD\_ATTRIBUTES column:   Copy code  ``` {   "key": "run",   "result": 123 } ``` |

Expand

Show lessSee more
