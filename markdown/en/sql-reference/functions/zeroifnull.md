Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# ZEROIFNULL

Returns 0 if its argument is null; otherwise, returns its argument.

## Syntax

Copy code

```
ZEROIFNULL( <expr> )
```

## Arguments

`expr`
:   The input should be an expression that evaluates to a numeric value (or NULL).

## Returns

If the value of the input expressions is NULL, this returns 0.
Otherwise, this returns the value of the input expression.

The data type of the return value is `NUMBER(p, s)`. The exact values of ‘p’ (precision) and ‘s’ (scale) depend
upon the input expression. For example, if the input expression is 3.14159, then the data type of the output value
will be `NUMBER(7, 5)`.

## Examples

The following example shows the output of the function for various input values:

> Copy code
>
> ```
> SELECT column1, ZEROIFNULL(column1) 
>     FROM VALUES (1), (null), (5), (0), (3.14159);
> +---------+---------------------+
> | COLUMN1 | ZEROIFNULL(COLUMN1) |
> |---------+---------------------|
> | 1.00000 |             1.00000 |
> |    NULL |             0.00000 |
> | 5.00000 |             5.00000 |
> | 0.00000 |             0.00000 |
> | 3.14159 |             3.14159 |
> +---------+---------------------+
> ```
