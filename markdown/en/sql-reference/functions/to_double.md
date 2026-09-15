Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_DOUBLE

Converts an expression to a double-precision floating-point number.

For NULL input, the result is NULL.

See also:
:   [TRY\_TO\_DOUBLE](/sql-reference/functions/try_to_double)

## Syntax

Copy code

```
TO_DOUBLE( <expr> [, '<format>' ] )
```

## Arguments

`expr`
:   An expression of a numeric, character, or variant type.

`format`
:   If the expression evaluates to a string, then the function accepts
    an optional format model. Format models are described at
    [SQL format models](/sql-reference/sql-format-models). The format model
    specifies the format of the input string, not the format of the
    output value.

## Returns

This function returns a value of FLOAT data type.

If `expr` is NULL, the function returns NULL.

## Usage notes

- Fixed-point numbers are converted to floating point; the conversion
  cannot fail, but might result in loss of precision.
- Strings are converted as decimal integer or fractional numbers,
  scientific notation and special values (**nan**, **inf**, **infinity**)
  are accepted.
- For VARIANT input:

  - If the variant contains a fixed-point value, the numeric conversion
    will be performed.
  - If the variant contains a floating-point value, the value will be
    preserved unchanged.
  - If the variant contains a string, a string conversion will be
    performed.
  - If the variant contains a Boolean value, the result will be 0 or 1
    (for false and true, correspondingly).
  - If the variant contains JSON **null** value, the output will be
    NULL.
- Conversion of decimal fractions to binary float and back is not precise
  (that is, printing of a floating-point number converted from decimal representation
  might produce a slightly different number). If precise representation of decimal
  fractions is required, use fixed-point numbers.

## Examples

After creating a table with columns of different data types, this script calls
TO\_DOUBLE on each of those columns:

Copy code

```
CREATE OR REPLACE TABLE double_demo (d DECIMAL(7, 2), v VARCHAR, o VARIANT);
INSERT INTO double_demo (d, v, o) SELECT 1.1, '2.2', TO_VARIANT(3.14);
SELECT TO_DOUBLE(d), TO_DOUBLE(v), TO_DOUBLE(o) FROM double_demo;
```

```
+--------------+--------------+--------------+
| TO_DOUBLE(D) | TO_DOUBLE(V) | TO_DOUBLE(O) |
|--------------+--------------+--------------|
|          1.1 |          2.2 |         3.14 |
+--------------+--------------+--------------+
```

The following example shows that converting from a binary float back to a number is not precise:

Copy code

```
SELECT TO_DOUBLE(1.1)::NUMBER(38, 18);
```

```
+--------------------------------+
| TO_DOUBLE(1.1)::NUMBER(38, 18) |
|--------------------------------|
|           1.100000000000000089 |
+--------------------------------+
```
