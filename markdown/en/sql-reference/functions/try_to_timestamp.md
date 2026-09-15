Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_TIMESTAMP / TRY\_TO\_TIMESTAMP\_\*

A special version of [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](/sql-reference/functions/to_timestamp) that performs the same operation (i.e. converts an input expression into a timestamp), but with error-handling support (i.e. if the conversion cannot be performed, it returns a NULL value instead of raising an error).

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

Note

TRY\_TO\_TIMESTAMP maps to one of the other timestamp functions, based on the
[TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter. The parameter default
is TIMESTAMP\_NTZ so TRY\_TO\_TIMESTAMP maps to TRY\_TO\_TIMESTAMP\_NTZ by default.

See also:
:   [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](/sql-reference/functions/to_timestamp)

## Syntax

Copy code

```
timestampFunction ( <string_expr> [, <format> ] )
timestampFunction ( '<integer>' )
```

Where:

> Copy code
>
> ```
> timestampFunction ::=
>     TRY_TO_TIMESTAMP | TRY_TO_TIMESTAMP_LTZ | TRY_TO_TIMESTAMP_NTZ | TRY_TO_TIMESTAMP_TZ
> ```

## Arguments

**Required:**

One of:

> `string_expr`
> :   A string that can be evaluated to a TIMESTAMP (TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, or TIMESTAMP\_TZ).
>
> `'integer'`
> :   An expression that evaluates to a string containing an integer, for example `'15000000'`. Depending
>     on the magnitude of the string, it can be interpreted as seconds, milliseconds, microseconds, or
>     nanoseconds. For details, see the [Usage Notes](#usage-notes).

**Optional:**

`format`
:   Format specifier for `string_expr` or
    [AUTO](/sql-reference/date-time-input-output#label-date-time-input-output-supported-formats-for-auto-detection).
    For more information, see [Date and time formats in conversion functions](/sql-reference/functions-conversion#label-date-time-format-conversion).

    The default is the current value of the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format)
    session parameter (default AUTO).

## Returns

The data type of the returned value is one of the TIMESTAMP data
types. By default, the data type is TIMESTAMP\_NTZ. You can change
this by setting the session parameter [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping).

## Usage notes

- For timestamps with time zones, the setting of the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter affects the return value. The returned
  timestamp is in the time zone for the session.
- The display format for timestamps in the output is determined by the timestamp output format that corresponds with the
  function ([TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format), [TIMESTAMP\_LTZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-ltz-output-format), [TIMESTAMP\_NTZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-ntz-output-format),
  or [TIMESTAMP\_TZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-tz-output-format)).
- If the format of the input parameter is a string that contains an integer:

  - After the string is converted to an integer, the integer is treated as a number of seconds, milliseconds,
    microseconds, or nanoseconds after the start of the Unix epoch (1970-01-01 00:00:00.000000000 UTC).

    - If the integer is less than 31536000000 (the number of milliseconds in a year), then the value is treated as
      a number of seconds.
    - If the value is greater than or equal to 31536000000 and less than 31536000000000, then the value is treated
      as milliseconds.
    - If the value is greater than or equal to 31536000000000 and less than 31536000000000000, then the value is
      treated as microseconds.
    - If the value is greater than or equal to 31536000000000000, then the value is
      treated as nanoseconds.
  - If more than one row is evaluated (for example, if the input is the column name of a table that contains more than
    one row), each value is examined independently to determine if the value represents seconds, milliseconds, microseconds, or
    nanoseconds.

- When you use the TO\_TIMESTAMP\_NTZ or TRY\_TO\_TIMESTAMP\_NTZ function to convert a timestamp with time zone information, the time zone
  information is lost. If the timestamp is then converted back to a timestamp with time zone information (by using
  the TO\_TIMESTAMP\_TZ function for example), the time zone information is not recoverable.

## Examples

This example uses TRY\_TO\_TIMESTAMP:

Copy code

```
SELECT TRY_TO_TIMESTAMP('2024-01-15 12:30:00'), TRY_TO_TIMESTAMP('Invalid');
```

```
+-----------------------------------------+-----------------------------+
| TRY_TO_TIMESTAMP('2024-01-15 12:30:00') | TRY_TO_TIMESTAMP('INVALID') |
|-----------------------------------------+-----------------------------|
| 2024-01-15 12:30:00.000                 | NULL                        |
+-----------------------------------------+-----------------------------+
```

See [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](/sql-reference/functions/to_timestamp) for examples that convert an input expression to a timestamp.
