Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Rounding and Truncation)

# TRUNCATE , TRUNC

Rounds the input expression down to the nearest (or equal) value closer to zero.
Depending on the value you specify as the scale parameter, the transformation can remove:

- All the digits after the decimal point, producing an integer value. This is the default
  and most common use of TRUNC for numbers.
- Some of the significant digits after the decimal point, producing a less precise value.
- All the significant digits after the decimal point and some significant digits
  to the left of the decimal point, producing a value that is a multiple of 10, 100, or other power of 10.

The TRUNCATE and TRUNC functions are synonymous.

Note

TRUNC is overloaded. It can also be used with date/time values to [truncate dates, times, and timestamps](/sql-reference/functions/trunc2)
to a specified part. The numeric TRUNC has one required and one optional parameter. The date/time TRUNC has two required parameters.

See also:
:   [CEIL](/sql-reference/functions/ceil) , [FLOOR](/sql-reference/functions/floor) , [ROUND](/sql-reference/functions/round)

## Syntax

Copy code

```
TRUNCATE( <input_expr> [ , <scale_expr> ] )

TRUNC( <input_expr> [ , <scale_expr> ] )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be one of the numeric data types, such as DECFLOAT,
    FLOAT, or NUMBER.

`scale_expr`
:   The number of digits to include after the decimal point.

    The default `scale_expr` is zero, meaning that the function removes all digits after the decimal point.

    For information about negative scales, see the [Usage notes](#label-trunc-usage-notes) below.

## Returns

- If the input is a NUMBER value, the data type of the returned value is NUMBER(precision, scale).

  If the input scale was greater than or equal to zero, then the output scale generally matches the input scale.

  If the input scale was negative, then the output scale is 0.

  For example:

  - The data type returned by `TRUNCATE(3.14, 1)` is `NUMBER(4, 1)`.
  - The data type returned by `TRUNCATE(3.14, 0)` is `NUMBER(4, 0)`.
  - The data type returned by `TRUNCATE(33.33, -1)` is `NUMBER(5, 0)`.

  If the scale is zero, then the value is effectively an integer.
- If the input is a FLOAT value, the data type of the returned value is FLOAT.
- If the input is a DECFLOAT value, the data type of the returned value is DECFLOAT.

## Usage notes

- If `scale_expr` is negative, then it specifies the number of places before the decimal point to
  which to adjust the number. For example, if the scale is -2, then the result is a multiple of 100.
- If `scale_expr` is larger than the input expression scale, the function does not have any effect.
- If either the `input_expr` or the `scale_expr` is NULL, then the result is NULL.
- Truncation is performed towards 0, not towards the smaller number. For example, `TRUNCATE(-9.6)` results in `-9`, not `-10`.

## Examples

The following examples demonstrate the TRUNC function for numeric values.
For examples of truncating dates, times, and timestamps, see [the date/time form of TRUNC](/sql-reference/functions/trunc2).

The examples use data from this sample table. The table contains two different decimal numbers,
-975.975 and 135.135, along with different values to use for the scale parameter with the TRUNC function.

Copy code

```
CREATE TABLE numeric_trunc_demo (n FLOAT, scale INTEGER);
INSERT INTO numeric_trunc_demo (n, scale) VALUES
   (-975.975, -1), (-975.975,  0), (-975.975,  2),
   ( 135.135, -2), ( 135.135,  0), ( 135.135,  1),
   ( 135.135,  3), ( 135.135, 50), ( 135.135, NULL);
```

When you don’t specify a scale parameter, the default behavior for TRUNC
with a numeric parameter is to return the integer value that’s equal to
the parameter or closer to zero. Specifying a scale parameter of 0
does the same thing.

Copy code

```
SELECT DISTINCT n, TRUNCATE(n)
  FROM numeric_trunc_demo ORDER BY n;
```

```
+----------+-------------+
|        N | TRUNCATE(N) |
|----------+-------------|
| -975.975 |        -975 |
|  135.135 |         135 |
+----------+-------------+
```

The following example shows the results of calling the TRUNC function with
zero, positive, or negative scale parameters applied to a positive and a negative
number.

- Specifying a zero scale parameter removes all the digits after the decimal point, producing an integer value.
- Specifying a positive scale parameter leaves the specified number of significant digits after the decimal point.
- Specifying a negative scale parameter turns that many digits into zeroes to the left of the decimal point.
- Specifying a scale that is greater than +38 or less than -38 is the same as specifying +38 or -38.

Copy code

```
SELECT n, scale, TRUNC(n, scale)
  FROM numeric_trunc_demo ORDER BY n, scale;
```

```
+----------+-------+-----------------+
|        N | SCALE | TRUNC(N, SCALE) |
|----------+-------+-----------------|
| -975.975 |    -1 |        -970     |
| -975.975 |     0 |        -975     |
| -975.975 |     2 |        -975.97  |
|  135.135 |    -2 |         100     |
|  135.135 |     0 |         135     |
|  135.135 |     1 |         135.1   |
|  135.135 |     3 |         135.135 |
|  135.135 |    50 |         135.135 |
|  135.135 |  NULL |            NULL |
+----------+-------+-----------------+
```
