Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_TIME

A special version of [TO\_TIME , TIME](/sql-reference/functions/to_time) that performs the same operation (i.e.
converts an input expression into a time), but with error-handling
support (i.e. if the conversion cannot be performed, it returns a NULL value
instead of raising an error).

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

See also:
:   [TO\_TIME , TIME](/sql-reference/functions/to_time)

## Syntax

Copy code

```
TRY_TO_TIME( <string_expr> [, <format> ] )
TRY_TO_TIME( '<integer>' )
```

## Arguments

**Required:**

One of:

> `string_expr`
> :   A string that can be converted to a valid time.
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

    The default is the current value of the [TIME\_INPUT\_FORMAT](/sql-reference/parameters#label-time-input-format)
    session parameter (default AUTO).

## Returns

The data type of the returned value is TIME.

## Usage notes

- The display format for times in the output is determined by the [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format)
  session parameter (default `HH24:MI:SS`).
- If the format of the input parameter is a string that contains an integer, the unit of measurement for the value (seconds,
  microseconds, milliseconds, or nanoseconds) is determined as follows:

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

## Examples

This example uses TRY\_TO\_TIME:

Copy code

```
SELECT TRY_TO_TIME('12:30:00'), TRY_TO_TIME('Invalid');
```

```
+-------------------------+------------------------+
| TRY_TO_TIME('12:30:00') | TRY_TO_TIME('INVALID') |
|-------------------------+------------------------|
| 12:30:00                | NULL                   |
+-------------------------+------------------------+
```

See [TO\_TIME , TIME](/sql-reference/functions/to_time) for examples that convert an input expression to a time.
