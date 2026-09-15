Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Rounding and Truncation)

# FLOOR

Returns values from `input_expr` rounded to the nearest equal or smaller integer, or to the nearest equal or smaller value with the specified number of places after the decimal point.

See also:
:   [CEIL](/sql-reference/functions/ceil) , [ROUND](/sql-reference/functions/round) , [TRUNCATE , TRUNC](/sql-reference/functions/trunc)

## Syntax

Copy code

```
FLOOR( <input_expr> [, <scale_expr> ] )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type should be one of the numeric data types, such as DECFLOAT,
    FLOAT, or NUMBER.

`scale_expr`
:   The number of digits the output should include after the decimal point.

    The default `scale_expr` is zero, meaning that the function removes all digits after the decimal point.

    For information about negative scales, see the Usage Notes below.

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

- The data type returned by FLOOR(3.14::FLOAT, 1) is FLOAT.
- The NUMBER returned by FLOOR(3.14, 1) has scale 1 and precision at least 3.
- The NUMBER returned by FLOOR(-9.99, 0) has scale 0 and precision at least 2.
- The NUMBER returned by FLOOR(33.33, -1) has scale 0 and precision at least 3.

## Usage notes

- If `scale_expr` is negative, then it specifies the number of places before the decimal point to
  which to adjust the number. For example, if the scale is -2, then the result is a multiple of 100.
- If `scale_expr` is larger than the input expression scale, the function does not have any effect.
- If either the `input_expr` or the `scale_expr` is NULL, then the result is NULL.
- When negative numbers are rounded down, the value is further from 0. For example, FLOOR(-1.1) is -2, not -1.
- If rounding the number downward brings the number outside of the range of values of the data type, an error is returned.

## Examples

This example demonstrates the function without the `scale_expr`
parameter:

> Copy code
>
> ```
> SELECT FLOOR(135.135), FLOOR(-975.975);
> +----------------+-----------------+
> | FLOOR(135.135) | FLOOR(-975.975) |
> |----------------+-----------------|
> |            135 |            -976 |
> +----------------+-----------------+
> ```

This example demonstrates the function with the `scale_expr` parameter,
including with the scale set to negative numbers:

> Create and fill a table:
>
> > Copy code
> >
> > ```
> > CREATE TABLE test_floor (n FLOAT, scale INTEGER);
> > INSERT INTO test_floor (n, scale) VALUES
> >    (-975.975, -1),
> >    (-975.975,  0),
> >    (-975.975,  2),
> >    ( 135.135, -2),
> >    ( 135.135,  0),
> >    ( 135.135,  1),
> >    ( 135.135,  3),
> >    ( 135.135, 50),
> >    ( 135.135, NULL)
> >    ;
> > ```
>
> Output:
>
> > Copy code
> >
> > ```
> > SELECT n, scale, FLOOR(n, scale)
> >   FROM test_floor
> >   ORDER BY n, scale;
> > +----------+-------+-----------------+
> > |        N | SCALE | FLOOR(N, SCALE) |
> > |----------+-------+-----------------|
> > | -975.975 |    -1 |        -980     |
> > | -975.975 |     0 |        -976     |
> > | -975.975 |     2 |        -975.98  |
> > |  135.135 |    -2 |         100     |
> > |  135.135 |     0 |         135     |
> > |  135.135 |     1 |         135.1   |
> > |  135.135 |     3 |         135.135 |
> > |  135.135 |    50 |         135.135 |
> > |  135.135 |  NULL |            NULL |
> > +----------+-------+-----------------+
> > ```
