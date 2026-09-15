Categories:
:   [Conversion functions](/sql-reference/functions-conversion) , [Date & time functions](/sql-reference/functions-date-time)

# TRY\_TO\_DATE

A special version of the [TO\_DATE](/sql-reference/functions/to_date) function
that performs the same operation (i.e. converts an input expression to a date), but
with error-handling support (i.e. if the conversion cannot be performed, it returns a
NULL value instead of raising an error).

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

See also:
:   [TO\_DATE , DATE](/sql-reference/functions/to_date)

## Syntax

Copy code

```
TRY_TO_DATE( <string_expr> [, <format> ] )
TRY_TO_DATE( '<integer>' )
```

## Arguments

**Required:**

One of:

> `string_expr`
> :   String from which to extract a date. For example: `'2024-01-31'`.
>
> `'integer'`
> :   An expression that evaluates to a string containing an integer. For example: `'15000000'`. Depending
>     on the magnitude of the string, it can be interpreted as seconds, milliseconds, microseconds, or
>     nanoseconds. For details, see the [Usage notes](#usage-notes) for this function.

**Optional:**

`format`
:   Date format specifier for `string_expr` or
    [AUTO](/sql-reference/date-time-input-output#label-date-time-input-output-supported-formats-for-auto-detection),
    which specifies that Snowflake should automatically detect the format to use. For more information,
    see [Date and time formats in conversion functions](/sql-reference/functions-conversion#label-date-time-format-conversion).

    The default is the current value of the [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format)
    session parameter (default `AUTO`).

## Returns

The data type of the returned value is DATE.

## Usage notes

- The display format for dates in the output is determined by the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format)
  session parameter (default `YYYY-MM-DD`).
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

## Examples

The following example uses the TRY\_TO\_DATE function:

Copy code

```
SELECT 
  TRY_TO_DATE('2024-05-10') AS valid_date, 
  TRY_TO_DATE('Invalid') AS invalid_date;
```

```
+------------+--------------+
| VALID_DATE | INVALID_DATE |
|------------+--------------|
| 2024-05-10 | NULL         |
+------------+--------------+
```

See [TO\_DATE , DATE](/sql-reference/functions/to_date) for examples that convert an input expression to a date.
