Categories:
:   [Conversion functions](/sql-reference/functions-conversion) , [Date & time functions](/sql-reference/functions-date-time)

# TO\_DATE , DATE

Converts an input expression to a date:

- For a VARCHAR expression, the result of converting the string to a date.
- For a TIMESTAMP expression, the date from the timestamp.
- For a VARIANT expression:

  - If the VARIANT contains a string, a string conversion is performed.
  - If the VARIANT contains a date, the date value is preserved as is.
  - If the VARIANT contains a JSON null value, the output is NULL.
- For NULL input, the output is NULL.

For all other values, a conversion error is generated.

See also:
:   [TRY\_TO\_DATE](/sql-reference/functions/try_to_date)

## Syntax

Copy code

```
TO_DATE( <string_expr> [, <format> ] )
TO_DATE( <timestamp_expr> )
TO_DATE( '<integer>' )
TO_DATE( <variant_expr> )

DATE( <string_expr> [, <format> ] )
DATE( <timestamp_expr> )
DATE( '<integer>' )
DATE( <variant_expr> )
```

## Arguments

**Required:**

One of:

> `string_expr`
> :   String from which to extract a date. For example: `'2024-01-31'`.
>
> `timestamp_expr`
> :   A TIMESTAMP expression. The DATE portion of the TIMESTAMP value is extracted.
>
> `'integer'`
> :   An expression that evaluates to a string containing an integer. For example: `'15000000'`. Depending
>     on the magnitude of the string, it can be interpreted as seconds, milliseconds, microseconds, or
>     nanoseconds. For details, see the [Usage notes](#usage-notes) for this function.
>
> `variant_expr`
> :   An expression of type VARIANT.
>
>     The VARIANT must contain one of the following:
>
>     - A string from which to extract a date.
>     - A date.
>     - A string containing an integer that represents the number of seconds or milliseconds.
>
>     Although TO\_DATE accepts a TIMESTAMP value, it does not accept a TIMESTAMP value inside a VARIANT.

**Optional:**

`format`
:   Date format specifier for `string_expr` or
    [AUTO](/sql-reference/date-time-input-output#label-date-time-input-output-supported-formats-for-auto-detection),
    which specifies that Snowflake automatically detects the format to use. For more information,
    see [Date and time formats in conversion functions](/sql-reference/functions-conversion#label-date-time-format-conversion).

    The default is the current value of the [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format)
    session parameter (default `AUTO`).

## Returns

The data type of the returned value is DATE. If the input is NULL, returns NULL.

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

The following examples use the TO\_DATE and DATE functions.

### Basic example

Copy code

```
SELECT TO_DATE('2024-05-10'), DATE('2024-05-10');
```

```
+-----------------------+--------------------+
| TO_DATE('2024-05-10') | DATE('2024-05-10') |
|-----------------------+--------------------|
| 2024-05-10            | 2024-05-10         |
+-----------------------+--------------------+
```

### Example that extracts the date from a timestamp

The TO\_DATE function accepts TIMESTAMP values and strings in TIMESTAMP format, but discards the time
information (hours, minutes, and so on).

Create and load the table:

Copy code

```
CREATE OR REPLACE TABLE date_from_timestamp(ts TIMESTAMP);

INSERT INTO date_from_timestamp(ts)
  VALUES (TO_TIMESTAMP('2024.10.02 04:00:00', 'YYYY.MM.DD HH:MI:SS'));
```

Query the TIMESTAMP value in the table:

Copy code

```
SELECT ts FROM date_from_timestamp;
```

```
+-------------------------+
| TS                      |
|-------------------------|
| 2024-10-02 04:00:00.000 |
+-------------------------+
```

Query the TIMESTAMP value in the table using the TO\_DATE function:

Copy code

```
SELECT TO_DATE(ts) FROM date_from_timestamp;
```

```
+-------------+
| TO_DATE(TS) |
|-------------|
| 2024-10-02  |
+-------------+
```

### Examples that use different input formats

The following examples use the TO\_DATE and DATE functions with different input format
specifications. The date format in the returned output is determined by the
setting of the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) session parameter.

Copy code

```
SELECT TO_DATE('2024.05.10', 'YYYY.MM.DD'), DATE('2024.05.10', 'YYYY.MM.DD');
```

```
+-------------------------------------+----------------------------------+
| TO_DATE('2024.05.10', 'YYYY.MM.DD') | DATE('2024.05.10', 'YYYY.MM.DD') |
|-------------------------------------+----------------------------------|
| 2024-05-10                          | 2024-05-10                       |
+-------------------------------------+----------------------------------+
```

Copy code

```
SELECT TO_DATE('2024-05-10', 'AUTO'), DATE('2024-05-10', 'AUTO');
```

```
+-------------------------------+----------------------------+
| TO_DATE('2024-05-10', 'AUTO') | DATE('2024-05-10', 'AUTO') |
|-------------------------------+----------------------------|
| 2024-05-10                    | 2024-05-10                 |
+-------------------------------+----------------------------+
```

Copy code

```
SELECT TO_DATE('05/10/2024', 'MM/DD/YYYY'), DATE('05/10/2024', 'MM/DD/YYYY');
```

```
+-------------------------------------+----------------------------------+
| TO_DATE('05/10/2024', 'MM/DD/YYYY') | DATE('05/20/2024', 'MM/DD/YYYY') |
|-------------------------------------+----------------------------------|
| 2024-05-10                          | 2024-05-20                       |
+-------------------------------------+----------------------------------+
```

### Examples that use different output formats

The following examples show the results of queries when the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format)
session parameter is set to `DD-MON-YYYY`:

Copy code

```
ALTER SESSION SET DATE_OUTPUT_FORMAT = 'DD-MON-YYYY';
```

Copy code

```
SELECT TO_DATE('2024-05-10', 'YYYY-MM-DD'), DATE('2024-05-10', 'YYYY-MM-DD');
```

```
+-------------------------------------+----------------------------------+
| TO_DATE('2024-05-10', 'YYYY-MM-DD') | DATE('2024-05-10', 'YYYY-MM-DD') |
|-------------------------------------+----------------------------------|
| 10-May-2024                         | 10-May-2024                      |
+-------------------------------------+----------------------------------+
```

Copy code

```
SELECT TO_DATE('05/10/2024', 'MM/DD/YYYY'), DATE('05/10/2024', 'MM/DD/YYYY');
```

```
+-------------------------------------+----------------------------------+
| TO_DATE('05/10/2024', 'MM/DD/YYYY') | DATE('05/10/2024', 'MM/DD/YYYY') |
|-------------------------------------+----------------------------------|
| 10-May-2024                         | 10-May-2024                      |
+-------------------------------------+----------------------------------+
```

### Examples that use a string that contains an integer

When the input is a string that contains an integer, the magnitude of that integer affects whether it is interpreted
as seconds, milliseconds, etc. The following example shows how the function chooses the units to use (seconds, milliseconds,
microseconds, or nanoseconds), based on the magnitude of the value.

Create and load the table:

Copy code

```
CREATE OR REPLACE TABLE demo1 (
  description VARCHAR,
  value VARCHAR -- string rather than bigint
);

INSERT INTO demo1 (description, value) VALUES
  ('Seconds',      '31536000'),
  ('Milliseconds', '31536000000'),
  ('Microseconds', '31536000000000'),
  ('Nanoseconds',  '31536000000000000');
```

Pass the strings to the function:

Copy code

```
SELECT description,
       value,
       TO_TIMESTAMP(value),
       TO_DATE(value)
  FROM demo1
  ORDER BY value;
```

```
+--------------+-------------------+-------------------------+----------------+
| DESCRIPTION  | VALUE             | TO_TIMESTAMP(VALUE)     | TO_DATE(VALUE) |
|--------------+-------------------+-------------------------+----------------|
| Seconds      | 31536000          | 1971-01-01 00:00:00.000 | 1971-01-01     |
| Milliseconds | 31536000000       | 1971-01-01 00:00:00.000 | 1971-01-01     |
| Microseconds | 31536000000000    | 1971-01-01 00:00:00.000 | 1971-01-01     |
| Nanoseconds  | 31536000000000000 | 1971-01-01 00:00:00.000 | 1971-01-01     |
+--------------+-------------------+-------------------------+----------------+
```
