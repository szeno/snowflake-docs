Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LOG, SYSTEM$LOG\_<level> (for Snowflake Scripting)

Logs a message at the specified severity level.

## Syntax

Copy code

```
SYSTEM$LOG('<level>', <message>);

SYSTEM$LOG_TRACE(<message>);
SYSTEM$LOG_DEBUG(<message>);
SYSTEM$LOG_INFO(<message>);
SYSTEM$LOG_WARN(<message>);
SYSTEM$LOG_ERROR(<message>);
SYSTEM$LOG_FATAL(<message>);
```

## Arguments

`'level'`
:   The severity level at which to log the message. You can specify one of the following strings:

    - ‘trace’
    - ‘debug’
    - ‘info’
    - ‘warn’
    - ‘error’
    - ‘fatal’

`message`
:   An expression that resolves to the message to log. If the message is not a string, the function converts the message to a string.

## Examples

Code in the following example uses the SYSTEM$LOG function to log messages at each of the supported levels. Note that a message logged
from code that processes an input row will be logged *for every row* processed by the handler. If the handler is executed in a large table,
this can result in a large number of messages in the event table.

Copy code

```
-- The following calls are equivalent.
-- Both log information-level messages.
SYSTEM$LOG('info', 'Information-level message');
SYSTEM$LOG_INFO('Information-level message');

-- The following calls are equivalent.
-- Both log error messages.
SYSTEM$LOG('error', 'Error message');
SYSTEM$LOG_ERROR('Error message');

-- The following calls are equivalent.
-- Both log warning messages.
SYSTEM$LOG('warning', 'Warning message');
SYSTEM$LOG_WARN('Warning message');

-- The following calls are equivalent.
-- Both log debug messages.
SYSTEM$LOG('debug', 'Debug message');
SYSTEM$LOG_DEBUG('Debug message');

-- The following calls are equivalent.
-- Both log trace messages.
SYSTEM$LOG('trace', 'Trace message');
SYSTEM$LOG_TRACE('Trace message');

-- The following calls are equivalent.
-- Both log fatal messages.
SYSTEM$LOG('fatal', 'Fatal message');
SYSTEM$LOG_FATAL('Fatal message');
```
