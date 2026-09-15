Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Rounding and Truncation)

# ROUND

Returns rounded values for `input_expr`.

See also:
:   [CEIL](/sql-reference/functions/ceil) , [FLOOR](/sql-reference/functions/floor) , [TRUNCATE , TRUNC](/sql-reference/functions/trunc)

## Syntax

Copy code

```
ROUND( <input_expr> [ , <scale_expr> [ , '<rounding_mode>' ] ] )
```

Copy code

```
ROUND( EXPR => <input_expr> ,
       SCALE => <scale_expr>
       [ , ROUNDING_MODE => '<rounding_mode>'  ] )
```

## Arguments

**Required:**

`input_expr` OR `EXPR => input_expr`
:   The value or expression to operate on. The data type must be one of the numeric data types, such as DECFLOAT,
    FLOAT, or NUMBER.

    If you specify the `EXPR =>` named argument, you must also specify the `SCALE =>` named argument.

**Optional:**

`scale_expr` OR `SCALE => scale_expr`
:   The number of digits the output includes after the decimal point.

    The default `scale_expr` is zero, meaning that the function removes all digits after the decimal point.

    For information about negative numbers, see [Usage notes](#label-round-function-usage-notes).

    If you specify the `SCALE =>` named argument, you must specify `EXPR =>` as the preceding named argument.

`'rounding_mode'` OR `ROUNDING_MODE => 'rounding_mode'`
:   The rounding mode to use. You can specify one of the following values:

    - `HALF_AWAY_FROM_ZERO`. This mode rounds the value [half away from zero](https://en.wikipedia.org/wiki/Rounding#Rounding_half_away_from_zero).
    - `HALF_TO_EVEN`. This mode rounds the value [half to even](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even).

    Default: `HALF_AWAY_FROM_ZERO`

    If you specify the `ROUNDING_MODE =>` named argument, you must specify both `EXPR =>` and `SCALE =>` as preceding named arguments.

    Note

    If you specify either value for the `rounding_mode` argument, the data type of `input_expr` must be
    [one of the data types for a fixed-point number](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers).

    [Data types for floating point numbers](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) (for example, FLOAT) aren’t supported
    with this argument.

## Returns

The return type is based on the input type:

- If the input expression is a FLOAT, the returned type is a FLOAT.
- If the input expression is DECFLOAT, the returned type is DECFLOAT.
- If the input expression is a NUMBER, the returned type is a NUMBER.
  - If the input scale is constant:

    - If the input scale is positive, the returned type has a scale equal to the input scale and has a precision large enough to
      encompass any possible result.
    - If the input scale is negative, the returned type has a scale of 0.
  - If the input scale isn’t constant, the returned type’s scale is the same as the input expression’s.

If the scale is zero, then the value is effectively an INTEGER.

For example:

- The data type returned by `ROUND(3.14::FLOAT, 1)` is FLOAT.
- The NUMBER returned by `ROUND(3.14, 1)` has scale 1 and precision at least 3.
- The NUMBER returned by `ROUND(-9.99, 0)` has scale 0 and precision at least 2.
- The NUMBER returned by `ROUND(33.33, -1)` has scale 0 and precision at least 3.

If either the `input_expr` or the `scale_expr` is NULL, the function returns NULL.

## Usage notes

- When you mix arguments by position and by name, all of the positional arguments must come before
  all of the named arguments.
- When you specify an argument by name, you can’t use double quotes around the argument name.

- If `scale_expr` is negative, it specifies the number of places before the decimal point to
  which to adjust the number. For example, if the scale is -2, the result is a multiple of 100.
- If `scale_expr` is larger than the input expression scale, the function doesn’t have any effect.
- By default, half-points are rounded away from zero for decimals. For example, -0.5 is rounded to -1.0.

  To change the rounding mode to round the value [half to even](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even) (for example, to round -0.5 to 0), specify
  `'HALF_TO_EVEN'` for the `rounding_mode` argument.

  Note

  If you specify the `rounding_mode` argument, the data type of the `input_expr` argument must be
  [one of the data types for a fixed-point number](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers).
- Floating point numbers are approximate values. A floating point number might not round as expected.
- If rounding brings the number outside of the range of values of the data type, the function returns an error.

## Examples

The following example shows a simple use of ROUND, with the default number of decimal places (0):

Copy code

```
SELECT ROUND(135.135), ROUND(-975.975);
```

```
+----------------+-----------------+
| ROUND(135.135) | ROUND(-975.975) |
|----------------+-----------------|
|            135 |            -976 |
+----------------+-----------------+
```

The next example queries the data in the following table:

Copy code

```
CREATE TABLE test_ceiling (n FLOAT, scale INTEGER);

INSERT INTO test_ceiling (n, scale) VALUES
  (-975.975, -1),
  (-975.975,  0),
  (-975.975,  2),
  ( 135.135, -2),
  ( 135.135,  0),
  ( 135.135,  1),
  ( 135.135,  3),
  ( 135.135, 50),
  ( 135.135, NULL);
```

Query the table and use a range of values for the `scale_expr` argument:

Copy code

```
SELECT n, scale, ROUND(n, scale)
  FROM test_ceiling
  ORDER BY n, scale;
```

```
+----------+-------+-----------------+
|        N | SCALE | ROUND(N, SCALE) |
|----------+-------+-----------------|
| -975.975 |    -1 |        -980     |
| -975.975 |     0 |        -976     |
| -975.975 |     2 |        -975.98  |
|  135.135 |    -2 |         100     |
|  135.135 |     0 |         135     |
|  135.135 |     1 |         135.1   |
|  135.135 |     3 |         135.135 |
|  135.135 |    50 |         135.135 |
|  135.135 |  NULL |            NULL |
+----------+-------+-----------------+
```

The next two examples show the difference between using the default rounding mode (`'HALF_AWAY_FROM_ZERO'`) and the rounding
mode `'HALF_TO_EVEN'`. Both examples call the ROUND function twice, first with the default rounding behavior, then with `'HALF_TO_EVEN'`.

The first example uses a positive input value of 2.5:

Copy code

```
SELECT ROUND(2.5, 0), ROUND(2.5, 0, 'HALF_TO_EVEN');
```

```
+---------------+-------------------------------+
| ROUND(2.5, 0) | ROUND(2.5, 0, 'HALF_TO_EVEN') |
|---------------+-------------------------------|
|             3 |                             2 |
+---------------+-------------------------------+
```

The second example uses a negative input value of -2.5:

Copy code

```
SELECT ROUND(-2.5, 0), ROUND(-2.5, 0, 'HALF_TO_EVEN');
```

```
+----------------+--------------------------------+
| ROUND(-2.5, 0) | ROUND(-2.5, 0, 'HALF_TO_EVEN') |
|----------------+--------------------------------|
|             -3 |                             -2 |
+----------------+--------------------------------+
```

The next two examples demonstrate how to specify the arguments to the function by name, rather than by position:

Copy code

```
SELECT ROUND(
  EXPR => -2.5,
  SCALE => 0) AS named_arguments;
```

```
+-----------------+
| NAMED_ARGUMENTS |
|-----------------|
|              -3 |
+-----------------+
```

Copy code

```
SELECT ROUND(
  EXPR => -2.5,
  SCALE => 0,
  ROUNDING_MODE => 'HALF_TO_EVEN') AS named_with_rounding_mode;
```

```
+--------------------------+
| NAMED_WITH_ROUNDING_MODE |
|--------------------------|
|                       -2 |
+--------------------------+
```

The next example shows that FLOAT values aren’t always stored exactly. As you can see below, in some cases .005 is
rounded to .01, while in other cases it is rounded to 0. The difference isn’t in the rounding; the difference is
actually in the underlying representation of the floating point number, because 1.005 is stored as a number very slightly
smaller than 1.005 (approximately 1.004999). The DECIMAL value, however is stored as an exact number, and is rounded
to .01 as expected in all cases.

Create and load a table:

Copy code

```
CREATE OR REPLACE TEMP TABLE rnd1(f float, d DECIMAL(10, 3));

INSERT INTO rnd1 (f, d) VALUES
  ( -10.005,  -10.005),
  (  -1.005,   -1.005),
  (   1.005,    1.005),
  (  10.005,   10.005);
```

Show examples of the difference between rounded FLOAT values and rounded DECIMAL values:

Copy code

```
SELECT f,
       ROUND(f, 2),
       d,
       ROUND(d, 2)
  FROM rnd1
  ORDER BY 1;
```

```
+---------+-------------+---------+-------------+
|       F | ROUND(F, 2) |       D | ROUND(D, 2) |
|---------+-------------+---------+-------------|
| -10.005 |      -10.01 | -10.005 |      -10.01 |
|  -1.005 |       -1    |  -1.005 |       -1.01 |
|   1.005 |        1    |   1.005 |        1.01 |
|  10.005 |       10.01 |  10.005 |       10.01 |
+---------+-------------+---------+-------------+
```
