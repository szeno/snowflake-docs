Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC

A special version of [TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](/sql-reference/functions/to_decimal) that performs the same operation
of converting an input expression to a fixed-point number, but has error-handling support so that
the function returns NULL if the conversion can’t be performed.

These functions are synonymous.

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

## Syntax

Copy code

```
TRY_TO_DECIMAL( <string_expr> [, '<format>' ] [, <precision> [, <scale> ] ] )

TRY_TO_NUMBER( <string_expr> [, '<format>' ] [, <precision> [, <scale> ] ] )

TRY_TO_NUMERIC( <string_expr> [, '<format>' ] [, <precision> [, <scale> ] ] )
```

## Arguments

**Required:**

`string_expr`
:   An expression of type VARCHAR.

**Optional:**

`format`
:   The SQL format model used to parse the input `expr` and return. For more
    information, see [SQL format models](/sql-reference/sql-format-models).

`precision`
:   The maximal number of decimal digits in the resulting number; from 1
    to 38. In Snowflake, precision is not used to determine the
    number of bytes that are needed to store the number and doesn’t have any effect
    on efficiency, so the default is the maximum (38).

`scale`
:   The number of fractional decimal digits (from 0 to `precision` - 1).
    0 indicates no fractional digits (i.e. an integer number). The default scale
    is 0.

## Returns

The function returns a value of type NUMBER with the following defaults:

- If the `precision` isn’t specified, then it defaults to 38.
- If the `scale` isn’t specified, then it defaults to 0.

If the conversion can’t be performed or the input is NULL, returns NULL.

## Usage notes

The input must be a string expression.

## Examples

The following example fails because the last column (`dec_with_range_error`)
doesn’t store enough significant digits to hold the value that it is asked
to hold:

Copy code

```
SELECT column1 AS orig_string,
       TO_DECIMAL(column1) AS dec,
       TO_DECIMAL(column1, 10, 2) AS dec_with_scale,
       TO_DECIMAL(column1, 4, 2) AS dec_with_range_err
  FROM VALUES ('345.123');
```

```
100039 (22003): Numeric value '345.123' is out of range
```

The following query is the same as the preceding query, except that it uses
TRY\_TO\_DECIMAL rather than TO\_DECIMAL, so it converts the
out-of-range value to NULL:

Copy code

```
SELECT column1 AS orig_string,
       TRY_TO_DECIMAL(column1) AS dec,
       TRY_TO_DECIMAL(column1, 10, 2) AS dec_with_scale,
       TRY_TO_DECIMAL(column1, 4, 2) AS dec_with_range_err
  FROM VALUES ('345.123');
```

```
+-------------+-----+----------------+--------------------+
| ORIG_STRING | DEC | DEC_WITH_SCALE | DEC_WITH_RANGE_ERR |
|-------------+-----+----------------+--------------------|
| 345.123     | 345 |         345.12 |               NULL |
+-------------+-----+----------------+--------------------+
```

The following example fails because the input string contains a dollar sign (`$`) and
a comma to separate groups of digits, not just digits and decimal points. However,
the format specifier for the last column doesn’t tell the TO\_DECIMAL function
to expect the dollar sign and comma:

Copy code

```
SELECT column1 AS orig_string,
       TO_DECIMAL(column1, '$9,999.00') AS num,
       TO_DECIMAL(column1, '$9,999.00', 6, 2) AS num_with_scale,
       TO_DECIMAL(column1, 6, 2) AS num_with_format_err
  FROM VALUES ('$7,543.21');
```

```
100038 (22018): Numeric value '$7,543.21' is not recognized
```

The following query is the same as the preceding query, except that it uses
TRY\_TO\_DECIMAL rather than TO\_DECIMAL, so it converts the input
to NULL:

Copy code

```
SELECT column1 AS orig_string,
       TRY_TO_DECIMAL(column1, '$9,999.00') AS num,
       TRY_TO_DECIMAL(column1, '$9,999.00', 6, 2) AS num_with_scale,
       TRY_TO_DECIMAL(column1, 6, 2) AS num_with_format_err
  FROM VALUES ('$7,543.21');
```

```
+-------------+------+----------------+---------------------+
| ORIG_STRING |  NUM | NUM_WITH_SCALE | NUM_WITH_FORMAT_ERR |
|-------------+------+----------------+---------------------|
| $7,543.21   | 7543 |        7543.21 |                NULL |
+-------------+------+----------------+---------------------+
```

The following example fails because the input expression contains characters that aren’t digits:

Copy code

```
SELECT column1 AS orig_string,
       TO_DECIMAL(column1) AS num
  FROM VALUES ('aaa');
```

```
100038 (22018): Numeric value 'aaa' is not recognized
```

The following query is the same as the preceding query, except that it uses TRY\_TO\_DECIMAL rather than TO\_DECIMAL,
so it converts the input to NULL:

Copy code

```
SELECT column1 AS orig_string,
       TRY_TO_DECIMAL(column1) AS num
  FROM VALUES ('aaa');
```

```
+-------------+------+
| ORIG_STRING | NUM  |
|-------------+------|
| aaa         | NULL |
+-------------+------+
```

You can perform the conversion if you specify the [X format element](/sql-reference/sql-format-models#label-fixed-position-numeric-formats)
with the TO\_DECIMAL or TRY\_TO\_DECIMAL function to convert a hexadecimal value to a decimal value:

Copy code

```
SELECT column1 AS orig_string,
       TO_DECIMAL(column1, 'XXX') AS to_decimal_num,
       TRY_TO_DECIMAL(column1, 'XXX') AS try_to_decimal_num
  FROM VALUES ('aaa');
```

```
+-------------+----------------+--------------------+
| ORIG_STRING | TO_DECIMAL_NUM | TRY_TO_DECIMAL_NUM |
|-------------+----------------+--------------------|
| aaa         |           2730 |               2730 |
+-------------+----------------+--------------------+
```

For additional examples, see [TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC](/sql-reference/functions/to_decimal).
