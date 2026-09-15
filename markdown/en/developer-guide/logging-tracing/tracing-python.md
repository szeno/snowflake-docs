# Emitting trace events in Python

You can use the Snowflake `telemetry` package to emit trace events from a function or procedure handler written in Python.
The package is available from [the Anaconda Snowflake channel](https://repo.anaconda.com/pkgs/snowflake).

You can access stored trace event data by executing a SELECT command on the event table. For more information, see
[Viewing trace data](/developer-guide/logging-tracing/tracing-accessing-events).

Note

For guidelines to keep in mind when adding trace events, see [General guidelines for adding trace events](/developer-guide/logging-tracing/tracing#label-tracing-general-guidelines-adding).

For general information about setting up logging and retrieving messages in Snowflake, see
[Logging messages from functions and procedures](/developer-guide/logging-tracing/logging).

Before logging from code, you must:

- Set up an event table to collect messages logged from handler code.

  For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).
- Be sure you have the trace level set so that the data you want are stored in the event table.

  For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

Note

For guidelines to keep in mind when adding trace events, see [General guidelines for adding trace events](/developer-guide/logging-tracing/tracing#label-tracing-general-guidelines-adding).

## Adding support for the telemetry package

To use telemetry package, you must make the open source
[Snowflake telemetry package](https://github.com/snowflakedb/snowflake-telemetry-python), which is included with Snowflake, available
to your handler code. The package is available from [the Anaconda Snowflake channel](https://repo.anaconda.com/pkgs/snowflake).

By default, the telemetry package is included when you create a Python handler for a stored procedure or function. However, if you
specify a package policy to allow or disallow specific packages explicitly, Snowflake doesn’t automatically include the
`snowflake-telemetry-python` package. In this case, you must specify the package in the PACKAGES clause.

- **For a Streamlit app.** You can add the `snowflake-telemetry-python` package to your app by using Snowsight or an
  `environment.yml.` file.

  Code in the following example uses the PACKAGES clause to reference the telemetry package as well as the Snowpark library (which is
  required for stored procedures written in Python – for more information, see [Writing stored procedures with SQL and Python](/developer-guide/stored-procedure/python/procedure-python-overview)).

  Copy code

  ```
  CREATE OR REPLACE FUNCTION my_function(...)
    RETURNS ...
    LANGUAGE PYTHON
    ...
    PACKAGES = ('snowflake-telemetry-python')
    ...
  ```
- Import the `telemetry` package in your code.

  Copy code

  ```
  from snowflake import telemetry
  ```

## Adding trace events

You can add trace events by calling the `telemetry.add_event` method, passing a name for the event. You can also optionally associate
attributes – key-value pairs – with an event.

The `add_event` method is available in the following form:

Copy code

```
telemetry.add_event(<name>, <attributes>)
```

where

- `name` is a Python string that specifies the name of the trace event.
- `attributes` is an [OpenTelemetry Attributes object](https://github.com/open-telemetry/opentelemetry-python/blob/main/opentelemetry-api/src/opentelemetry/util/types.py) that specifies the attributes for this trace event. This argument is
  optional. Omit the argument if you do not have any attributes to specify for this trace event.

Handler code in the following example adds two events, `FunctionEmptyEvent` and `FunctionEventWithAttributes`. With
`FunctionEventWithAttributes`, the code also adds two attributes: `key1` and `key2`.

Copy code

```
telemetry.add_event("FunctionEmptyEvent")
telemetry.add_event("FunctionEventWithAttributes", {"key1": "value1", "key2": "value2"})
```

Adding these events results in two rows in the event table, each with a different value in the RECORD column:

Copy code

```
{
  "name": "FunctionEmptyEvent"
}
```

Copy code

```
{
  "name": "FunctionEventWithAttributes"
}
```

The `FunctionEventWithAttributes` event row includes the following attributes in the row’s RECORD\_ATTRIBUTES column:

Copy code

```
{
  "key1": "value1",
  "key2": "value2"
}
```

## Adding span attributes

You can set attributes – key-value pairs – associated with spans by calling the `telemetry.set_span_attribute` method.

For details on spans, see [How Snowflake represents trace events](/developer-guide/logging-tracing/tracing-how-events-work).

The `set_span_attribute` method is available in the following form:

Copy code

```
telemetry.set_span_attribute(<key>, <value>)
```

where:

> - `key` is a Python string that specifies the key for an attribute.
> - `value` is an [OpenTelemetry AttributeValue object](https://github.com/open-telemetry/opentelemetry-python/blob/main/opentelemetry-api/src/opentelemetry/util/types.py) that specifies the value of the attribute.

Code in the following example creates four attributes and sets their values:

Copy code

```
// Setting span attributes.
telemetry.set_span_attribute("example.boolean", true);
telemetry.set_span_attribute("example.long", 2);
telemetry.set_span_attribute("example.double", 2.5);
telemetry.set_span_attribute("example.string", "testAttribute");
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

## Python examples

The following sections provide examples of adding support for trace events from Python code.

### Stored procedure example

Copy code

```
CREATE OR REPLACE PROCEDURE do_tracing()
  RETURNS VARIANT
  LANGUAGE PYTHON
  PACKAGES = ('snowflake-snowpark-python', 'snowflake-telemetry-python')
  RUNTIME_VERSION = 3.12
  HANDLER = 'run'
  AS $$
  from snowflake import telemetry
  def run(session):
    telemetry.set_span_attribute("example.proc.do_tracing", "begin")
    telemetry.add_event("event_with_attributes", {"example.key1": "value1", "example.key2": "value2"})
    return "SUCCESS"
  $$;
```

### Streamlit example

Copy code

```
import streamlit as st
from snowflake import telemetry

st.title("Streamlit trace event example")

hifives_val = st.slider("Number of high-fives", min_value=0, max_value=90, value=60)

if st.button("Submit"):
    telemetry.add_event("new_submission", {"high_fives": hifives_val})
```

### UDF example

Copy code

```
CREATE OR REPLACE FUNCTION times_two(x NUMBER)
  RETURNS NUMBER
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'times_two'
AS $$
from snowflake import telemetry
def times_two(x):
  telemetry.set_span_attribute("example.func.times_two", "begin")
  telemetry.add_event("event_without_attributes")
  telemetry.add_event("event_with_attributes", {"example.key1": "value1", "example.key2": "value2"})

  response = 2 * x

  telemetry.set_span_attribute("example.func.times_two.response", response)

  return response
$$;
```

When you call the trace event API from a Python function that processes an input row, the API will be called *for every row* processed
by the UDF.

For example, the following statement calls the Python function defined in the previous example for 50 rows, resulting in 100 trace events
(two for each row):

Copy code

```
select count(times_two(seq8())) from table(generator(rowcount => 50));
```

### UDTF example

Copy code

```
CREATE OR REPLACE FUNCTION digits_of_number(input NUMBER)
  RETURNS TABLE(result NUMBER)
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'TableFunctionHandler'
  AS
$$
from snowflake import telemetry

class TableFunctionHandler:

  def __init__(self):
    telemetry.add_event("test_udtf_init")

  def process(self, input):
    telemetry.add_event("test_udtf_process", {"input": str(input)})
    response = input

    while input > 0:
      response = input % 10
      input /= 10
      yield (response,)

  def end_partition(self):
    telemetry.add_event("test_udtf_end_partition")
$$;
```

When you call the trace event API in the `process()` method of a UDTF handler class, the API will be called *for every row* processed.

For example, the following statement calls the `process()` method defined in the previous example for 50 rows, resulting in 100 trace
events (two for each row) added by the `process()` method:

Copy code

```
select * from table(generator(rowcount => 50)), table(digits_of_number(seq8())) order by 1;
```
