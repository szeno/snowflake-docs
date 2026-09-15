Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_CHAR , TO\_VARCHAR

Converts the input expression to a string. For NULL input, the output is NULL.

These functions are synonymous.

## Syntax

Copy code

```
TO_CHAR( <expr> )
TO_CHAR( <numeric_expr> [, '<format>' ] )
TO_CHAR( <date_or_time_expr> [, '<format>' ] )
TO_CHAR( <binary_expr> [, '<format>' ] )

TO_VARCHAR( <expr> )
TO_VARCHAR( <numeric_expr> [, '<format>' ] )
TO_VARCHAR( <date_or_time_expr> [, '<format>' ] )
TO_VARCHAR( <binary_expr> [, '<format>' ] )
```

## Arguments

**Required:**

`expr`
:   An expression of any data type.

`numeric_expr`
:   A numeric expression.

`date_or_time_expr`
:   An expression of type DATE, TIME, or TIMESTAMP.

`binary_expr`
:   An expression of type BINARY or VARBINARY.

**Optional:**

`format`
:   The format of the output string:

    - For `numeric_expr`, specifies the SQL format model used to
      interpret the numeric expression. For more information, see
      [SQL format models](/sql-reference/sql-format-models).
    - For `date_or_time_expr`, specifies the expected format to parse
      or produce a string. For more information, see [Date and time formats in conversion functions](/sql-reference/functions-conversion#label-date-time-format-conversion).

      The default is the current value of the following session
      parameters:

      - [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) (for DATE inputs)
      - [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format) (for TIME inputs)
      - [TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format) (for TIMESTAMP inputs)
    - For `binary_expr`, specifies the format in which to produce
      the string (e.g. ‘HEX’, ‘BASE64’ or ‘UTF-8’).

      For more information, see
      [Overview of supported binary formats](/sql-reference/binary-input-output#label-overview-of-supported-binary-formats).

## Returns

This function returns a value of VARCHAR data type or NULL.

## Usage notes

- For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing
  a JSON document or JSON elementary value (unless VARIANT or OBJECT
  contains an XML tag, in which case the output is a string containing
  an XML document):
  - A string stored in VARIANT is preserved as is (i.e. it is not converted to
    a JSON string).
  - A JSON **null** value is converted to a string containing the word “null”.

## Examples

The following examples convert numbers, timestamps, and dates to strings.

### Examples that convert numbers

Convert numeric values to strings in the specified [formats](/sql-reference/sql-format-models):

Copy code

```
CREATE OR REPLACE TABLE convert_numbers_to_strings(column1 NUMBER);

INSERT INTO convert_numbers_to_strings VALUES
  (-12.391),
  (0),
  (-1),
  (0.10),
  (0.01),
  (3987),
  (1.111);

SELECT column1 AS orig_value,
       TO_CHAR(column1, '">"$99.0"<"') AS D2_1,
       TO_CHAR(column1, '">"B9,999.0"<"') AS D4_1,
       TO_CHAR(column1, '">"TME"<"') AS TME,
       TO_CHAR(column1, '">"TM9"<"') AS TM9,
       TO_CHAR(column1, '">"0XXX"<"') AS X4,
       TO_CHAR(column1, '">"S0XXX"<"') AS SX4
  FROM convert_numbers_to_strings;
```

```
+------------+----------+------------+-------------+------------+--------+---------+
| ORIG_VALUE | D2_1     | D4_1       | TME         | TM9        | X4     | SX4     |
|------------+----------+------------+-------------+------------+--------+---------|
|    -12.391 | >-$12.4< | >   -12.4< | >-1.2391E1< | >-12.391<  | >FFF4< | >-000C< |
|      0.000 | >  $0.0< | >      .0< | >0E0<       | >0.000<    | >0000< | >+0000< |
|     -1.000 | > -$1.0< | >    -1.0< | >-1E0<      | >-1.000<   | >FFFF< | >-0001< |
|      0.100 | >  $0.1< | >      .1< | >1E-1<      | >0.100<    | >0000< | >+0000< |
|      0.010 | >  $0.0< | >      .0< | >1E-2<      | >0.010<    | >0000< | >+0000< |
|   3987.000 | > $##.#< | > 3,987.0< | >3.987E3<   | >3987.000< | >0F93< | >+0F93< |
|      1.111 | >  $1.1< | >     1.1< | >1.111E0<   | >1.111<    | >0001< | >+0001< |
+------------+----------+------------+-------------+------------+--------+---------+
```

The output illustrates how the values are converted to strings based on the specified formats:

- The `>` and `<` symbols are string literals that are included in the output. They make it easier
  to see where spaces are inserted.
- The `D2_1` column shows the values with a `$` printed before the digits.

  - For the `3987` value, there are more digits in the integer part of the number than there are digit positions
    in the format, so all digits are printed as `#` to indicate overflow.
  - For the `0.10`, `0.01`, and `1.111` values, there are more digits in the fractional part of the number
    than there are digit positions in the format, so the fractional values are truncated.
- The `D4_1` column shows that zero values are represented as spaces in the integer parts of the
  numbers.

  - For the `0`, `0.10`, and `0.01` values, a space replaces the zero before the separator.
  - For the `0.10`, `0.01`, and `1.111` values, there are more digits in the fractional part of
    the number than there are digit positions in the format, so the fractional values are truncated.
- The `TME` column shows the values in scientific notation.
- The `TM9` column shows the values as integers or decimal fractions, based on the value of the number.
- The `X4` column shows the values as hexadecimal digits without the fractional parts.
- The `SX4` column shows the values as hexadecimal digits of the absolute value of the numbers and
  includes the numeric sign (`+` or `-`).

This example converts a logarithmic value to a string:

Copy code

```
SELECT TO_VARCHAR(LOG(3,4));
```

```
+----------------------+
| TO_VARCHAR(LOG(3,4)) |
|----------------------|
| 1.261859507          |
+----------------------+
```

### Examples that convert timestamps and dates

Convert a TIMESTAMP value to a string in the specified format:

Copy code

```
SELECT TO_VARCHAR('2024-04-05 01:02:03'::TIMESTAMP, 'mm/dd/yyyy, hh24:mi hours');
```

```
+---------------------------------------------------------------------------+
| TO_VARCHAR('2024-04-05 01:02:03'::TIMESTAMP, 'MM/DD/YYYY, HH24:MI HOURS') |
|---------------------------------------------------------------------------|
| 04/05/2024, 01:02 hours                                                   |
+---------------------------------------------------------------------------+
```

Convert a DATE value to a string in the default format:

Copy code

```
SELECT TO_VARCHAR('03-April-2024'::DATE);
```

```
+-----------------------------------+
| TO_VARCHAR('03-APRIL-2024'::DATE) |
|-----------------------------------|
| 2024-04-03                        |
+-----------------------------------+
```

Convert a DATE value to a string in the specified format:

Copy code

```
SELECT TO_VARCHAR('03-April-2024'::DATE, 'yyyy.mm.dd');
```

```
+-------------------------------------------------+
| TO_VARCHAR('03-APRIL-2024'::DATE, 'YYYY.MM.DD') |
|-------------------------------------------------|
| 2024.04.03                                      |
+-------------------------------------------------+
```
