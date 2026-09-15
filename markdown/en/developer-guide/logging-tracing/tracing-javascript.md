# Emitting trace events in JavaScript

You can use the `snowflake` class in the [Snowflake JavaScript API](/developer-guide/stored-procedure/stored-procedures-api) to emit trace events
from a function or procedure handler written in JavaScript. The JavaScript API is already available to your JavaScript handler code.

Before emitting trace events, be sure you have the trace level set so that the data you want are stored in the event table. For more
information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

Note

Before you can begin emitting trace events, you must set up an event table. For more information, see
[Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

You can access stored trace event data by executing a SELECT command on the event table. For more information, see
[Viewing trace data](/developer-guide/logging-tracing/tracing-accessing-events).

For general information about setting up logging and retrieving messages in Snowflake, see
[Trace events for functions and procedures](/developer-guide/logging-tracing/tracing).

Note

For guidelines to keep in mind when adding trace events, see [General guidelines for adding trace events](/developer-guide/logging-tracing/tracing#label-tracing-general-guidelines-adding).

## Adding trace events

You can add trace events by calling the `snowflake.addEvent` function, passing a name for the event. You can also optionally associate
attributes – key-value pairs – with an event.

The `addEvent` method is available in the following form:

Copy code

```
snowflake.addEvent(name [, { key:value [, key:value] } ] );
```

Handler code in the following example adds two events, `name_a` and `name_b`. With `name_b`, the code also adds two
attributes, `score` and `pass`.

Copy code

```
create procedure PI_JS()
  returns double
  language javascript
  as
  $$
    snowflake.addEvent('name_a');  // add an event without attributes
    snowflake.addEvent('name_b', {'score': 89, 'pass': true});
    return 3.14;
  $$
  ;
```

Setting these attributes results in two rows in the event table, each with a different value in the RECORD column:

Copy code

```
{
  "name": "name_a"
}
```

Copy code

```
{
  "name": "name_b"
}
```

The `name_b` event row includes the following attributes in the row’s RECORD\_ATTRIBUTES column:

Copy code

```
{
  "score": 89,
  "pass": true
}
```

## Adding span attributes

You can set attributes – key-value pairs – associated with spans by calling the `snowflake.setSpanAttribute` function.

The `setSpanAttribute` function is available in the following form:

Copy code

```
snowflake.setSpanAttribute(key, value);
```

For details on spans, see [How Snowflake represents trace events](/developer-guide/logging-tracing/tracing-how-events-work).

Code in the following example creates four attributes and sets their values:

Copy code

```
// Setting span attributes.
snowflake.setSpanAttribute("example.boolean", true);
snowflake.setSpanAttribute("example.long", 2L);
snowflake.setSpanAttribute("example.double", 2.5);
snowflake.setSpanAttribute("example.string", "testAttribute");
```

Setting these attributes results in the following in the event table’s RECORD\_ATTRIBUTES column:

Copy code

```
{
  "example.boolean": true,
  "example.long": 2,
  "example.double": 2.5,
  "example.string": "testAttribute"
}
```

## Adding custom spans

You can add custom spans that are separate from the default span created by Snowflake. For details on custom spans, see
[Adding custom spans to a trace](/developer-guide/logging-tracing/tracing-custom-spans).

Code in the following example uses the [OpenTelemetry API](https://open-telemetry.github.io/opentelemetry-js/modules/_opentelemetry_api.html) to create a new
`example_custom_span` span. It then adds an event and attribute to the new span. Finally, the code ends the span to have the span’s
event data captured in the event table. If the code doesn’t call the `Span.end` method, data is not captured in the event table.

Copy code

```
CREATE OR REPLACE FUNCTION javascript_custom_span()
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
const { trace } = opentelemetry;
const tracer = trace.getTracer("example_tracer");
// Alternatively, const tracer = opentelemetry.trace.getTracer("example_tracer");

tracer.startActiveSpan("example_custom_span", (span) => {
  span.addEvent("testEventWithAttributes");
  span.setAttribute("testAttribute", "value");

  span.end();
});
$$;
```
