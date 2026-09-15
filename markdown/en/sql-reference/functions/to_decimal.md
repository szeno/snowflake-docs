Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC

Converts an input expression to a fixed-point number.

These functions are synonymous.

See also:
:   [TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC](/sql-reference/functions/try_to_decimal)

## Syntax

Copy code

```
TO_DECIMAL( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )

TO_NUMBER( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )

TO_NUMERIC( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )
```

## Arguments

**Required:**

`expr`
:   An expression of a numeric, character, or variant type.

**Optional:**

`format`
:   The SQL format model used to parse the input `expr` and return. For more
    information, see [SQL format models](/sql-reference/sql-format-models).

`precision`
:   The maximum number of decimal digits in the resulting number, from 1
    to 38. In Snowflake, precision isn’t used to determine the
    number of bytes that are needed to store the number and doesn’t have any effect
    on efficiency, so the default is the maximum (38).

`scale`
:   The number of fractional decimal digits (from 0 to `precision` - 1).
    0 indicates no fractional digits; that is, an integer number. The default scale
    is 0.

## Returns

The function returns a value of type NUMBER with the following defaults:

- If the `precision` isn’t specified, then it defaults to 38.
- If the `scale` isn’t specified, then it defaults to 0.

For NULL input, returns NULL.

## Usage notes

- For fixed-point numbers:

  - Numbers with different scales are converted by either adding zeros to the right (if the scale needs to be increased) or by
    reducing the number of fractional digits by rounding (if the scale needs to be decreased).
  - Note that casts of fixed-point numbers to fixed-point numbers that increase scale might fail.
- For floating-point numbers:

  - Numbers are converted if they are within the representable range, given the scale.
  - The conversion between binary and decimal fractional numbers is not precise. This might result in loss of precision or
    out-of-range errors.
  - Values of infinity and NaN (not-a-number) result in conversion errors.
- Strings are converted as decimal, integer, fractional, or floating-point numbers.

  - For fractional input, the precision is deduced as the number of digits after the point.
  - For floating-point input, omitting the mantissa or exponent is allowed and is interpreted as 0. Thus, `E` is parsed as 0.
- For VARIANT input:

  - If the variant contains a fixed-point or a floating-point numeric value, an appropriate numeric conversion is performed.
  - If the variant contains a string, a string conversion is performed.
  - If the variant contains a Boolean value, the result is 0 or 1 (for false and true, correspondingly).
  - If the variant contains JSON `null` value, the output is NULL.

## Examples

Create a table with a VARCHAR column, then retrieve the string values from the table and pass those values
to the TO\_NUMBER function with different `precision` and `scale` values.

Copy code

```
CREATE OR REPLACE TABLE number_conv(expr VARCHAR);
INSERT INTO number_conv VALUES ('12.3456'), ('98.76546');

SELECT expr,
       TO_NUMBER(expr),
       TO_NUMBER(expr, 10, 1),
       TO_NUMBER(expr, 10, 8)
  FROM number_conv;
```

The query returns the following output:

```
+----------+-----------------+------------------------+------------------------+
| EXPR     | TO_NUMBER(EXPR) | TO_NUMBER(EXPR, 10, 1) | TO_NUMBER(EXPR, 10, 8) |
|----------+-----------------+------------------------+------------------------|
| 12.3456  |              12 |                   12.3 |            12.34560000 |
| 98.76546 |              99 |                   98.8 |            98.76546000 |
+----------+-----------------+------------------------+------------------------+
```

Try a query on the same table using the TO\_NUMBER function to return a number with the `precision` of `10`
and the scale of `9`.

Copy code

```
SELECT expr, TO_NUMBER(expr, 10, 9) FROM number_conv;
```

With the `precision` argument set to `10`, the maximal number of decimal digits in the results is 10.
Because both values in the table have two digits before the decimal point and `scale` is set to `9`,
the query returns an error because the results would return 11 digits.

```
100039 (22003): Numeric value '12.3456' is out of range
```

Use different [format elements](/sql-reference/sql-format-models) with the TO\_DECIMAL
function in a query:

Copy code

```
SELECT column1,
       TO_DECIMAL(column1, '99.9') as D0,
       TO_DECIMAL(column1, '99.9', 9, 5) as D5,
       TO_DECIMAL(column1, 'TM9', 9, 5) as TD5
  FROM VALUES ('1.0'), ('-12.3'), ('0.0'), ('- 0.1');
```

The query returns the following output:

```
+---------+-----+-----------+-----------+
| COLUMN1 |  D0 |        D5 |       TD5 |
|---------+-----+-----------+-----------|
| 1.0     |   1 |   1.00000 |   1.00000 |
| -12.3   | -12 | -12.30000 | -12.30000 |
| 0.0     |   0 |   0.00000 |   0.00000 |
| - 0.1   |   0 |  -0.10000 |  -0.10000 |
+---------+-----+-----------+-----------+
```

The output shows that the `TM9` text-minimal format element prints precisely the number of
digits in the fractional part based on the specified scale. For more information, see
[Text-minimal numeric formats](/sql-reference/sql-format-models#label-text-minimal-numeric-formats).

Convert a number that uses a comma to separate groups of digits:

Copy code

```
SELECT column1,
       TO_DECIMAL(column1, '9,999.99', 6, 2) as convert_number
  FROM VALUES ('3,741.72');
```

The query returns the following output:

```
+----------+----------------+
| COLUMN1  | CONVERT_NUMBER |
|----------+----------------|
| 3,741.72 |        3741.72 |
+----------+----------------+
```

Convert a currency value that uses a comma to separate groups of digits:

Copy code

```
SELECT column1,
       TO_DECIMAL(column1, '$9,999.99', 6, 2) as convert_currency
  FROM VALUES ('$3,741.72');
```

The query returns the following output:

```
+-----------+------------------+
| COLUMN1   | CONVERT_CURRENCY |
|-----------+------------------|
| $3,741.72 |          3741.72 |
+-----------+------------------+
```

Use the [X format element](/sql-reference/sql-format-models#label-fixed-position-numeric-formats) with the TO\_DECIMAL function
to convert a hexadecimal value to a decimal value:

Copy code

```
SELECT TO_DECIMAL('ae5', 'XXX');
```

The query returns the following output:

```
+--------------------------+
| TO_DECIMAL('AE5', 'XXX') |
|--------------------------|
|                     2789 |
+--------------------------+
```

The number of digits in the format element must be equal to or greater than the number of digits in the
expression. For example, try to run the following query:

Copy code

```
SELECT TO_DECIMAL('ae5', 'XX');
```

The query returns an error:

```
100140 (22007): Can't parse 'ae5' as number with format 'XX'
```
