Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Logarithmic)

# LOG

Returns the logarithm of a numeric expression.

See also:
:   [natural log (ln)](/sql-reference/functions/ln)

## Syntax

Copy code

```
LOG(<base>, <expr>)
```

## Arguments

`base`
:   The “base” to use (e.g. 10 for base 10 arithmetic).

    This can be of any numeric data type (INTEGER, fixed-point, or floating
    point).

    `base` should be greater than 0.

    `base` should not be exactly 1.0.

`expr`
:   The value for which you want to know the log.

    This can be of any numeric data type (INTEGER, fixed-point, or floating
    point).

    `expr` should be greater than 0.

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Usage notes

- If `base` is 1 or less than or equal to 0, an error is returned.
- If `expr` is less than or equal to 0, an error is returned.

## Examples

Copy code

```
SELECT x, y, log(x, y) FROM tab;

--------+--------+-------------+
   X    |   Y    |  LOG(X, Y)  |
--------+--------+-------------+
 2      | 0.5    | -1          |
 2      | 1      | 0           |
 2      | 8      | 3           |
 2      | 16     | 4           |
 10     | 10     | 1           |
 10     | 20     | 1.301029996 |
 10     | [NULL] | [NULL]      |
 [NULL] | 10     | [NULL]      |
 [NULL] | [NULL] | [NULL]      |
--------+--------+-------------+
```
