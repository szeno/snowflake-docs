# Emitting trace events in Java

You can use the `com.snowflake.telemetry.Telemetry` class in the [Snowflake Telemetry API](https://javadoc.io/doc/com.snowflake/telemetry/latest/index.html) library to emit trace events from a function or
procedure handler written in Java. The `Telemetry` class is included with Snowflake.

Note

Using the Snowflake Telemetry Library adds other libraries to your function or procedure’s execution environment. For more information,
see [Snowflake telemetry package dependencies](/developer-guide/logging-tracing/telemetry-package-dependencies).

For information on including the Telemetry library when packaging your code with Maven, see
[Setting up your Java and Scala environment to use the Telemetry class](/developer-guide/logging-tracing/telemetry-build-maven).

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

## Adding support for the telemetry API

To use `Telemetry` methods, you must make the open source [Snowflake telemetry package](https://central.sonatype.com/artifact/com.snowflake/telemetry) available to your handler code.

- In the PACKAGES clause in your CREATE PROCEDURE or CREATE FUNCTION statement, include the `com.snowflake:telemetry` package. The
  PACKAGES clause makes the included Snowflake Telemetry API available to your code.

  Code in the following example uses the PACKAGES clause to reference the Telemetry library as well as the Snowpark library (which is
  required for stored procedures written in Java – for more information, see [Writing Java handlers for stored procedures created with SQL](/developer-guide/stored-procedure/java/procedure-java-overview)).

  Copy code

  ```
  CREATE OR REPLACE PROCEDURE myproc(...)
    RETURNS ...
    LANGUAGE JAVA
    ...
    PACKAGES = ('com.snowflake:snowpark:latest', 'com.snowflake:telemetry:latest')
    ...
  ```
- Import the `com.snowflake.telemetry` package in your Java handler code.

  Copy code

  ```
  import com.snowflake.telemetry.Telemetry;
  ```

## Adding trace events

You can add trace events by calling the `Telemetry.addEvent` method, passing a name for the event. You can also optionally associate
attributes – key-value pairs – with an event.

The `addEvent` method has the following signatures:

Copy code

```
public static void addEvent(String name)
public static void addEvent(String name, Attributes attributes)
```

Code in the following example adds an event called `testEvent`, associating with the event two attributes: `key` and `result`.

Copy code

```
// Adding an event without attributes.
Telemetry.addEvent("testEvent");

// Adding an event with attributes.
Attributes eventAttributes = Attributes.of(
  AttributeKey.stringKey("key"), "run",
  AttributeKey.longKey("result"), Long.valueOf(123));
Telemetry.addEvent("testEventWithAttributes", eventAttributes);
```

Adding these events results in two rows in the event table, each with a different value in the RECORD column:

Copy code

```
{
  "name": "testEvent"
}
```

Copy code

```
{
  "name": "testEventWithAttributes"
}
```

The `testEventWithAttributes` event row includes the following attributes in the row’s RECORD\_ATTRIBUTES column:

Copy code

```
{
  "key": "run",
  "result": 123
}
```

## Adding span attributes

You can set attributes – key-value pairs – associated with spans by calling the `Telemetry.setSpanAttribute` method.

The `setSpanAttribute` method has the following signatures:

Copy code

```
public static void setSpanAttribute(String key, boolean value)
public static void setSpanAttribute(String key, long value)
public static void setSpanAttribute(String key, double value)
public static void setSpanAttribute(String key, String value)
```

For details on spans, see [How Snowflake represents trace events](/developer-guide/logging-tracing/tracing-how-events-work).

Code in the following example creates four attributes and sets their values:

Copy code

```
// Setting span attributes.
Telemetry.setSpanAttribute("example.boolean", true);
Telemetry.setSpanAttribute("example.long", 2L);
Telemetry.setSpanAttribute("example.double", 2.5);
Telemetry.setSpanAttribute("example.string", "testAttribute");
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

Code in the following example uses the [OpenTelemetry API](https://javadoc.io/doc/io.opentelemetry/opentelemetry-api/latest/index.html) and [OpenTelemetry context propagation API](https://www.javadoc.io/doc/io.opentelemetry/opentelemetry-context-prop/latest/index.html) to create a new `my.span`
span. It then adds an event with attributes to the new span. Finally, the code ends the span to have the span’s event data
captured in the event table. If the code doesn’t call the `Span.end` method, data is not captured in the event table.

Copy code

```
CREATE OR REPLACE FUNCTION customSpansJavaExample() RETURNS STRING
  LANGUAGE JAVA
  PACKAGES = ('com.snowflake:telemetry:latest')
  HANDLER = 'MyJavaClass.run'
  as
  $$
  import com.snowflake.telemetry.Telemetry;
  import io.opentelemetry.api.common.AttributeKey;
  import io.opentelemetry.api.common.Attributes;
  import io.opentelemetry.api.GlobalOpenTelemetry;
  import io.opentelemetry.api.trace.Tracer;
  import io.opentelemetry.api.trace.Span;
  import io.opentelemetry.context.Scope;

  class MyJavaClass {
    public static String run() {
      Tracer tracer = GlobalOpenTelemetry.getTracerProvider().get("my.tracer");
      Span span = tracer.spanBuilder("my.span").startSpan();
      try (Scope scope = span.makeCurrent()) {
        // Do processing, adding events that will be captured in a my.span.

        // Add an event with attributes.
        Attributes eventAttributes = Attributes.of(
          AttributeKey.stringKey("key"), "run",
          AttributeKey.longKey("result"), Long.valueOf(123));

        span.addEvent("testEventWithAttributes", eventAttributes);
        span.setAttribute("testAttribute", "value");

      } finally {
        span.end();
      }
      return "success";
    }
  }
  $$;
```

## Java examples

### Stored procedure example

Copy code

```
CREATE OR REPLACE PROCEDURE do_tracing()
  RETURNS STRING
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES=('com.snowflake:snowpark:latest', 'com.snowflake:telemetry:latest')
  HANDLER = 'ProcedureHandler.run'
  AS
  $$
  import com.snowflake.snowpark_java.Session;
  import com.snowflake.telemetry.Telemetry;
  import io.opentelemetry.api.common.AttributeKey;
  import io.opentelemetry.api.common.Attributes;

  public class ProcedureHandler {

    public String run(Session session) {

      // Set span attribute.
      Telemetry.setSpanAttribute("example.proc.do_tracing", "begin");

      // Add an event without attributes.
      Telemetry.addEvent("run_method_start");

      // Add an event with attributes.
      Attributes eventAttributes = Attributes.of(
        AttributeKey.stringKey("example.method.name"), "run",
        AttributeKey.longKey("example.long"), Long.valueOf(123));
      Telemetry.addEvent("event_with_attributes", eventAttributes);

      // Set span attribute.
      Telemetry.setSpanAttribute("example.proc.do_tracing", "complete");

      return "SUCCESS";
    }
  }
  $$;
```

### UDF example

Copy code

```
CREATE OR REPLACE FUNCTION add_two_numbers(A FLOAT, B FLOAT) RETURNS FLOAT
  LANGUAGE JAVA
  PACKAGES=('com.snowflake:telemetry:latest')
  HANDLER = 'ScalarFunctionHandler.run'
  AS
  $$
  import com.snowflake.telemetry.Telemetry;
  import io.opentelemetry.api.common.AttributeKey;
  import io.opentelemetry.api.common.Attributes;
  import io.opentelemetry.api.common.AttributesBuilder;

  class ScalarFunctionHandler {

    public static Double run(Double d0, Double d1) {

      // Set span attribute.
      Telemetry.setSpanAttribute("example.func.add_two_numbers", "begin");

      // Add an event without attributes.
      Telemetry.addEvent("run_method_start");

      // Add an event with attributes.
      Attributes eventAttributes = Attributes.of(
        AttributeKey.stringKey("example.method.name"), "run",
        AttributeKey.longKey("example.long"), Long.valueOf(123));
      Telemetry.addEvent("event_with_attributes", eventAttributes);

      Double response = d0 == null || d1 == null ? null : (d0 + d1);

      // Set span attribute.
      Telemetry.setSpanAttribute("example.func.add_two_numbers.response", response);
      Telemetry.setSpanAttribute("example.func.add_two_numbers", "complete");

      return response;
    }
  }
  $$;
```

### UDTF example

Copy code

```
CREATE OR REPLACE FUNCTION digits_of_number(x int)
  RETURNS TABLE(result INT)
  LANGUAGE JAVA
  PACKAGES = ('com.snowflake:telemetry:latest')
  HANDLER = 'TableFunctionHandler'
  AS
  $$
  import com.snowflake.telemetry.Telemetry;
  import io.opentelemetry.api.common.AttributeKey;
  import io.opentelemetry.api.common.Attributes;
  import io.opentelemetry.api.common.AttributesBuilder;
  import java.util.stream.Stream;

  public class TableFunctionHandler {

    public TableFunctionHandler() {
      // Set span attribute.
      Telemetry.setSpanAttribute("example.func.digits_of_number", "begin");
    }

    static class OutputRow {
      public int result;

      public OutputRow(int result) {
        this.result = result;
      }
    }

    public static Class getOutputClass() {
      return OutputRow.class;
    }

    public Stream<OutputRow> process(int input) {

      // Add an event with attributes.
      Attributes eventAttributes = Attributes.of(
        AttributeKey.longKey("example.received.value"), Long.valueOf(input));
      Telemetry.addEvent("digits_of_number", eventAttributes);

      Stream.Builder<OutputRow> stream = Stream.builder();
      while (input > 0) {

        stream.add(new OutputRow(input %10));
        input /= 10;
      }

      // Set span attribute.
      Telemetry.setSpanAttribute("example.func.digits_of_number", "complete");

      return stream.build();
    }
  }
  $$;
```
