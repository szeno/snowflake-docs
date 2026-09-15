# Logging messages from functions and procedures

You can log messages (such as warning or error messages) from a stored procedure, UDF, or UDTF, including those you write
[using Snowpark APIs](/developer-guide/snowpark/index). You can access the logged messages from an event table (a type of
predefined table that captures events, including logged messages). For a list of supported handler languages, see
[Supported languages](#label-logging-supported-languages).

For example, in a Java UDF, you can use the [SLF4J API](http://www.slf4j.org/) to log messages. Later, you can access those logged messages in an event
table.

Note

Before you can collect log messages, you must [enable telemetry data collection](/developer-guide/logging-tracing/logging-tracing-enabling).
When you [instrument your code](#label-logging-handler-code), Snowflake generates the data and collects it in an event table.

## Logging example

The Python code in the following example imports the `logging` module, gets a logger, and logs a message at the `INFO` level.

Note

A message logged from a method that processes an input row will be logged *for every row* processed by the UDF. If the UDF is executed in a
large table, this can result in a large number of messages in the event table.

Copy code

```
import logging

logger = logging.getLogger("mylog")

def test_logging(self):
    logger.info("This is an INFO test.")
```

## Getting started

To get started logging from handler code, follow these high-level steps:

1. [Set up an event table.](/developer-guide/logging-tracing/event-table-setting-up)

   Snowflake will use your event table to store messages logged from your handler code. An event table has
   columns [predefined by Snowflake](/developer-guide/logging-tracing/event-table-columns).
2. Get acquainted with the logging API for the handler language you’ll be using.

   see [Supported languages](#label-logging-supported-languages) for a list of handler languages, then view
   [content about how to log from your language](#label-logging-handler-code).
3. Add logging code to your handler.
4. Learn how to [retrieve logging data](/developer-guide/logging-tracing/logging-accessing-messages) from the event table.

## Level for log messages

You can manage the level of log event data stored in the event table by setting the log level. Before logging, use this setting to make
sure you’re capturing the log message severity.

For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

## Supported languages

You can log messages from code written in the following languages, including when handler code is written with
[Snowpark APIs](/developer-guide/snowpark/index).

| Language / Type | Java | JavaScript | Python | Scala | SQL |
| --- | --- | --- | --- | --- | --- |
| Stored procedure handler | ✔ | ✔ | ✔ | ✔ | ✔ \*\* |
| Streamlit app |  |  | ✔ |  |  |
| UDF handler (scalar function) | ✔ | ✔ | ✔ | ✔ |  |
| UDTF handler (table function) | ✔ | ✔ | ✔ | ✔ \* |  |

Expand

Show lessSee more

**Legend**

\*:
:   Scala UDTF handler written in Snowpark.

\*\*:
:   Snowflake Scripting used to write stored procedures.

Note

Logging is not supported for [Request and response translators in external functions](/sql-reference/external-functions-translators).

### Logging from handler code

To log messages, you can use functions common to your handler code language. Snowflake intercepts messages and stores them in the
event table you create.

For example, in a Java UDF, you can use the [SLF4J API](http://www.slf4j.org/) to log messages. Later, you can access those logged messages in an event table.

If you plan to log messages when errors occur, you should log them from within the construct for handling errors in the language
that you are using. For example, in a Java UDF, call the method for logging a message in the `catch` block where you handle
the exception.

The following table lists handler languages supported for logging, along with links to content on logging from code.

| Language | Logging Library | Documentation |
| --- | --- | --- |
| Java | SLF4J API | [Logging messages in Java](/developer-guide/logging-tracing/logging-java) |
| JavaScript | Snowflake JavaScript API `snowflake` object | [Logging messages in JavaScript](/developer-guide/logging-tracing/logging-javascript) |
| Python | Standard Library `logging` module | [Logging messages in Python](/developer-guide/logging-tracing/logging-python) |
| Scala | SLF4J API | [Logging messages in Scala](/developer-guide/logging-tracing/logging-scala) |
| Snowflake Scripting | Snowflake SYSTEM$LOG function. | [Logging messages in Snowflake Scripting](/developer-guide/logging-tracing/logging-snowflake-scripting) |

Expand

Show lessSee more

## Viewing log messages

You can view the log messages either through Snowsight or by querying the event table in which log entries are stored. For more
information, see [Viewing log messages](/developer-guide/logging-tracing/logging-accessing-messages).
