# Emitting trace events in Scala

You can use the `com.snowflake.telemetry.Telemetry` class in the [Snowflake Telemetry API](https://javadoc.io/doc/com.snowflake/telemetry/latest/index.html) library to emit trace events from a function or
procedure handler written in Scala. The `Telemetry` class is included with Snowflake.

Snowflake currently supports the following versions of Scala:

- 2.13
- 2.12

For more information, see [Writing code to support different Scala versions](/developer-guide/scala-version-differences).

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
[Trace events for functions and procedures](/developer-guide/logging-tracing/tracing).

Before logging from code, you must:

- Set up an event table to collect messages logged from handler code.

  For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).
- Be sure you have the trace level set so that the data you want are stored in the event table.

  For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

## Adding support for the Telemetry API

To use `Telemetry` methods, you must make the open source [Snowflake telemetry package](https://central.sonatype.com/artifact/com.snowflake/telemetry) available to your handler code.

- In the PACKAGES clause in your CREATE PROCEDURE or CREATE FUNCTION statement, include the `com.snowflake:telemetry` package. The
  PACKAGES clause makes the included Snowflake Telemetry API available to your code.

  Code in the following example uses the PACKAGES clause to reference the Telemetry library as well as the Snowpark library (which is
  required for stored procedures written in Scala – for more information, see [Writing Scala handlers for stored procedures created with SQL](/developer-guide/stored-procedure/scala/procedure-scala-overview)).

  Scala 2.12Scala 2.13

  Copy code

  ```
  CREATE OR REPLACE PROCEDURE myproc(...)
    RETURNS ...
    LANGUAGE SCALA
    ...
    PACKAGES = ('com.snowflake:snowpark_2.12:latest', 'com.snowflake:telemetry:latest')
    ...
  ```

  Copy code

  ```
  CREATE OR REPLACE PROCEDURE myproc(...)
    RETURNS ...
    LANGUAGE SCALA
    ...
    PACKAGES = ('com.snowflake:snowpark_2.13:latest', 'com.snowflake:telemetry:latest')
    ...
  ```
- Import the `com.snowflake.telemetry` package in your handler code.

  Copy code

  ```
  import com.snowflake.telemetry.Telemetry
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

Code in the following example adds an event called `testEvent`, associating with the event two attributes: `key` and
`result`.

Copy code

```
// Adding an event without attributes.
Telemetry.addEvent("testEvent")

// Adding an event with attributes.
Attributes eventAttributes = Attributes.of(
  AttributeKey.stringKey("key"), "run",
  AttributeKey.longKey("result"), Long.valueOf(123))
Telemetry.addEvent("testEventWithAttributes", eventAttributes)
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
Telemetry.setSpanAttribute("example.boolean", true)
Telemetry.setSpanAttribute("example.long", 2L)
Telemetry.setSpanAttribute("example.double", 2.5)
Telemetry.setSpanAttribute("example.string", "testAttribute")
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
span. It then adds an event to the new span. Finally, the code ends the span to have the span’s event data captured in the event table.
If the code doesn’t call the `Span.end` method, data is not captured in the event table.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION testScalaUserSpans(x VARCHAR) RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:telemetry:latest')
  HANDLER = 'TestScalaClass.run'
  AS
  $$
  class TestScalaClass {
    import com.snowflake.telemetry.Telemetry
    import io.opentelemetry.api.GlobalOpenTelemetry
    import io.opentelemetry.api.trace.Tracer
    import io.opentelemetry.api.trace.Span
    import io.opentelemetry.context.Scope

    def run(x: String): String = {
      val tracer: Tracer = GlobalOpenTelemetry.getTracerProvider().get("my.tracer")
      val span: Span = tracer.spanBuilder("my.span").startSpan()
      span.addEvent("test event from scala")
      span.end()
      return x
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION testScalaUserSpans(x VARCHAR) RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:telemetry:latest')
  HANDLER = 'TestScalaClass.run'
  AS
  $$
  class TestScalaClass {
    import com.snowflake.telemetry.Telemetry
    import io.opentelemetry.api.GlobalOpenTelemetry
    import io.opentelemetry.api.trace.Tracer
    import io.opentelemetry.api.trace.Span
    import io.opentelemetry.context.Scope

    def run(x: String): String = {
      val tracer: Tracer = GlobalOpenTelemetry.getTracerProvider().get("my.tracer")
      val span: Span = tracer.spanBuilder("my.span").startSpan()
      span.addEvent("test event from scala")
      span.end()
      return x
    }
  }
  $$;
```

## Examples

### Stored procedure example

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE do_tracing()
  RETURNS STRING
  LANGUAGE SCALA
  RUNTIME_VERSION = '2.12'
  PACKAGES=('com.snowflake:snowpark_2.12:latest', 'com.snowflake:telemetry:latest')
  HANDLER = 'ProcedureHandler.run'
  AS
  $$
  import com.snowflake.snowpark_java.Session
  import com.snowflake.telemetry.Telemetry
  import io.opentelemetry.api.common.AttributeKey
  import io.opentelemetry.api.common.Attributes

  class ProcedureHandler {

    def run(session: Session): String = {

      // Set span attribute.
      Telemetry.setSpanAttribute("example.proc.do_tracing", "begin")

      // Add an event without attributes.
      Telemetry.addEvent("run_method_start")

      // Add an event with attributes.
      val eventAttributes: Attributes = Attributes.of(
        AttributeKey.stringKey("example.method.name"), "run")
      Telemetry.addEvent("event_with_attributes", eventAttributes)

      // Set span attribute.
      Telemetry.setSpanAttribute("example.proc.do_tracing", "complete")

      return "SUCCESS"
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE PROCEDURE do_tracing()
  RETURNS STRING
  LANGUAGE SCALA
  RUNTIME_VERSION = '2.13'
  PACKAGES=('com.snowflake:snowpark_2.13:latest', 'com.snowflake:telemetry:latest')
  HANDLER = 'ProcedureHandler.run'
  AS
  $$
  import com.snowflake.snowpark_java.Session
  import com.snowflake.telemetry.Telemetry
  import io.opentelemetry.api.common.AttributeKey
  import io.opentelemetry.api.common.Attributes

  class ProcedureHandler {

    def run(session: Session): String = {

      // Set span attribute.
      Telemetry.setSpanAttribute("example.proc.do_tracing", "begin")

      // Add an event without attributes.
      Telemetry.addEvent("run_method_start")

      // Add an event with attributes.
      val eventAttributes: Attributes = Attributes.of(
        AttributeKey.stringKey("example.method.name"), "run")
      Telemetry.addEvent("event_with_attributes", eventAttributes)

      // Set span attribute.
      Telemetry.setSpanAttribute("example.proc.do_tracing", "complete")

      return "SUCCESS"
    }
  }
  $$;
```
