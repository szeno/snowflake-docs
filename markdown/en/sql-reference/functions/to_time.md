Categories:
:   [Conversion functions](/sql-reference/functions-conversion) , [Date & time functions](/sql-reference/functions-date-time)

# TO\_TIME , TIME

Converts an input expression into a time.

See also:
:   [TRY\_TO\_TIME](/sql-reference/functions/try_to_time)

## Syntax

Copy code

```
TO_TIME( <string_expr> [, <format> ] )
TO_TIME( <timestamp_expr> )
TO_TIME( '<integer>' )
TO_TIME( <variant_expr> )

TIME( <string_expr> )
TIME( <timestamp_expr> )
TIME( '<integer>' )
TIME( <variant_expr> )
```

## Arguments

**Required:**

`string_expr` or `timestamp_expr` or `'integer'` or `variant_expr`
:   Expression to be converted into a time:

    - For `string_expr`, the string to convert to a time.
    - For `timestamp_expr`, the timestamp to convert to a time. The function returns the time portion of the input value.
    - For `'integer'`, a string containing an integer to convert to a time. The integer is treated as a number of seconds, milliseconds,
      microseconds, or nanoseconds after the start of the Unix epoch. See the [Usage Notes](#usage-notes).

      For this timestamp, the function gets the number of seconds after the start of the Unix epoch. The function performs a
      [modulo operation](https://en.wikipedia.org/wiki/Modulo_operation) to get the remainder from dividing this number by the
      number of seconds in a day (`86400`):

      `number_of_seconds % 86400`

      The function interprets this remainder as the number of seconds after midnight.

      For example, suppose that the value is `'31536002789'`.

      1. Based on the magnitude of this value, the function uses milliseconds as the unit of time and determines that the value
         represents `1971-01-01 00:00:02.789`.
      2. The function gets the number of seconds after the Unix epoch for this value (`31536002`).
      3. The function gets the remainder from dividing that number by the number of seconds in a day (`31536002 % 86400`).
      4. The function uses the remainder (`2`) as the number of seconds after midnight. The resulting time is `00:00:02`.
    - For `variant_expr`:

      - If the VARIANT contains a string in TIME format (such as `HH:MI:SS`), a string conversion is performed.
      - If the VARIANT contains a string in INTEGER format, a string conversion is performed and the value is
        treated as the number of seconds since midnight (modulus 86400 if necessary).
      - If the VARIANT contains a JSON null value, the output is NULL.

    For all other values, a conversion error is generated.

**Optional:**

`format`
:   Time format specifier for `string_expr` or
    [AUTO](/sql-reference/date-time-input-output#label-date-time-input-output-supported-formats-for-auto-detection),
    which specifies that Snowflake automatically detects the format to use. For more information,
    see [Date and time formats in conversion functions](/sql-reference/functions-conversion#label-date-time-format-conversion).

    Default: The current value of the [TIME\_INPUT\_FORMAT](/sql-reference/parameters#label-time-input-format)
    session parameter (default AUTO)

## Returns

The data type of the returned value is TIME. If the input is NULL, returns NULL.

## Usage notes

- The display format for times in the output is determined by the [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format)
  session parameter (default `HH24:MI:SS`).
- If the format of the input parameter is a string that contains an integer, the unit of measurement for the value (seconds,
  microseconds, milliseconds, or nanoseconds) is determined as follows:

> - After the string is converted to an integer, the integer is treated as a number of seconds, milliseconds,
>   microseconds, or nanoseconds after the start of the Unix epoch (1970-01-01 00:00:00.000000000 UTC).
>
>   - If the integer is less than 31536000000 (the number of milliseconds in a year), then the value is treated as
>     a number of seconds.
>   - If the value is greater than or equal to 31536000000 and less than 31536000000000, then the value is treated
>     as milliseconds.
>   - If the value is greater than or equal to 31536000000000 and less than 31536000000000000, then the value is
>     treated as microseconds.
>   - If the value is greater than or equal to 31536000000000000, then the value is
>     treated as nanoseconds.
> - If more than one row is evaluated (for example, if the input is the column name of a table that contains more than
>   one row), each value is examined independently to determine if the value represents seconds, milliseconds, microseconds, or
>   nanoseconds.

- Unlike the TO\_TIME function, the TIME function does not support the optional `format` parameter.

## Examples

These examples use the TO\_TIME and TIME functions.

Copy code

```
SELECT TO_TIME('13:30:00'), TIME('13:30:00');
```

```
+---------------------+------------------+
| TO_TIME('13:30:00') | TIME('13:30:00') |
|---------------------+------------------|
| 13:30:00            | 13:30:00         |
+---------------------+------------------+
```

Copy code

```
SELECT TO_TIME('13:30:00.000'), TIME('13:30:00.000');
```

```
+-------------------------+----------------------+
| TO_TIME('13:30:00.000') | TIME('13:30:00.000') |
|-------------------------+----------------------|
| 13:30:00                | 13:30:00             |
+-------------------------+----------------------+
```

This example shows how to use the TO\_TIME function to process field separators
other than the default colons. The example uses the period character as
the separator between hours and minutes, and between minutes and seconds:

Copy code

```
SELECT TO_TIME('11.15.00', 'HH24.MI.SS');
```

```
+-----------------------------------+
| TO_TIME('11.15.00', 'HH24.MI.SS') |
|-----------------------------------|
| 11:15:00                          |
+-----------------------------------+
```

This example demonstrates how the TO\_TIME function interprets a string containing an integer:

Copy code

```
CREATE OR REPLACE TABLE demo1_time (
  description VARCHAR,
  value VARCHAR -- string rather than bigint
);

INSERT INTO demo1_time (description, value) VALUES
  ('Seconds',      '31536001'),
  ('Milliseconds', '31536002400'),
  ('Microseconds', '31536003600000'),
  ('Nanoseconds',  '31536004900000000');
```

Copy code

```
SELECT description,
       value,
       TO_TIMESTAMP(value),
       TO_TIME(value)
  FROM demo1_time
  ORDER BY value;
```

```
+--------------+-------------------+-------------------------+----------------+
| DESCRIPTION  | VALUE             | TO_TIMESTAMP(VALUE)     | TO_TIME(VALUE) |
|--------------+-------------------+-------------------------+----------------|
| Seconds      | 31536001          | 1971-01-01 00:00:01.000 | 00:00:01       |
| Milliseconds | 31536002400       | 1971-01-01 00:00:02.400 | 00:00:02       |
| Microseconds | 31536003600000    | 1971-01-01 00:00:03.600 | 00:00:03       |
| Nanoseconds  | 31536004900000000 | 1971-01-01 00:00:04.900 | 00:00:04       |
+--------------+-------------------+-------------------------+----------------+
```
