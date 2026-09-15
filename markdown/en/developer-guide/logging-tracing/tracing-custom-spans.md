# Adding custom spans to a trace

You can add your own custom spans to traces for finer-grained tracing within the handler for a procedure or function.

By default, when you [have tracing enabled](/developer-guide/logging-tracing/logging-tracing-enabling), Snowflake starts a span for
you (as described in [How Snowflake represents trace events](/developer-guide/logging-tracing/tracing-how-events-work)) and adds all trace events to that span. (This is
known internally as the “auto\_instrumented” span.) Using OpenTelemetry APIs, you can create your own spans. To the new span, you can add
events and attributes using either the OpenTelemetry API or Snowflake API for your language.

You might want to create your own span when, for example, you want to isolate the trace data for computation-heavy actions that happen
within a procedure, such as when you’re using the code to train an ML model.

Custom spans you create match the default behavior of spans created by OpenTelemetry.

## Supported languages

You can add custom spans from code written in the following languages, including when handler code is written with
[Snowpark APIs](/developer-guide/snowpark/index).

| Language/Type | Java | Python | JavaScript | Scala | Snowflake Scripting |
| --- | --- | --- | --- | --- | --- |
| Stored procedure handler | ✔ | ✔ | ✔ | ✔ [[1]](#footnote-1) |  |
| Streamlit app |  | ✔ |  |  |  |
| UDF handler (scalar function) | ✔ | ✔ | ✔ | ✔ [[1]](#footnote-1) |  |
| UDTF handler (table function) | ✔ | ✔ | ✔ | ✔ [[1]](#footnote-1) [[2]](#footnote-2) |  |

Expand

Show lessSee more

[1]
Supported with the Java API.

[2]
Scala UDTF handler written in Snowpark.

## Creating a custom span

To add a custom span with handler code, use the OpenTelemetry API for your handler language within the existing Snowflake telemetry
environment to create a new span, add events and attributes as needed, and then close the span.

1. Use the OpenTelemetry API to create a tracer to manage context for the span.

   From this tracer created from the existing Snowflake telemetry environment, you can create custom spans that use the existing
   infrastructure in which trace data is captured by the event table.
2. From the new tracer, create the custom span with an API that ensures that the new span is the current span.

   By creating the new span in the existing context managed by Snowflake, you ensure that information from the context — including
   the [trace\_id](/developer-guide/logging-tracing/event-table-columns#label-event-table-trace-value) and [parent\_span\_id](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-span) values — is
   passed from the Snowflake default span to other spans.
3. When your code finishes with the custom span, it must close the span before the handler completes execution to have trace data
   captured by the event table.

   This behavior of custom spans matches the default behavior of OpenTelemetry.

For information on adding a custom span with a supported language, see the following topics:

- [Java custom span](/developer-guide/logging-tracing/tracing-java#label-tracing-events-java-custom-span)
- [JavaScript custom span](/developer-guide/logging-tracing/tracing-javascript#label-tracing-events-javascript-custom-span)
- [Python custom span](/developer-guide/logging-tracing/tracing-python#label-tracing-events-python-custom-span)
- [Scala custom span](/developer-guide/logging-tracing/tracing-scala#label-tracing-events-scala-custom-span)

### Python example

Code in the following example uses the [OpenTelemetry Python API](https://opentelemetry-python.readthedocs.io/en/latest/api/index.html) to create the `my.span` span as the current span with
`start_as_current_span`. It then adds an event with attributes to the new span using the [OpenTelemetry Python API](https://opentelemetry-python.readthedocs.io/en/latest/api/index.html).

Event data won’t be captured by the event table unless the span ends before your handler completes execution. In this example, closing the
span happens automatically when the `with` statement concludes.

Copy code

```
CREATE OR REPLACE FUNCTION customSpansPythonExample() RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = 3.12
PACKAGES = ('opentelemetry-api')
HANDLER = 'custom_spans_function'
AS $$
from snowflake import telemetry
from opentelemetry import trace

def custom_spans_function():
  tracer = trace.get_tracer("my.tracer")
  with tracer.start_as_current_span("my.span") as span:
    span.add_event("Event2 in custom span", {"key1": "value1", "key2": "value2"})

  return "success"
$$;
```
