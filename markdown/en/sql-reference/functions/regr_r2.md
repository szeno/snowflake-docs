Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Linear Regression) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# REGR\_R2

Returns the coefficient of determination for non-null pairs in a group. It is computed for non-null pairs using the following formula:

Copy code

```
NULL                 if VAR_POP(x) = 0, else
1                    if VAR_POP(y) = 0 and VAR_POP(x) <> 0, else
POWER(CORR(y,x), 2)
```

Where `x` is the independent variable and `y` is the dependent variable.

## Syntax

**Aggregate function**

Copy code

```
REGR_R2(y, x)
```

**Window function**

Copy code

```
REGR_R2(y, x) OVER ( [ PARTITION BY <expr3> ] )
```

## Arguments

`y`
:   The dependent variable. This must be an expression that can be evaluated to a numeric type.

`x`
:   The independent variable. This must be an expression that can be evaluated to a numeric type.

`expr3`
:   This is the optional expression used to group rows into partitions.

Important

Note the order of the arguments; the dependent variable is first.

## Returns

If any of the input expressions is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Usage notes

- DISTINCT is not supported for this function.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

Copy code

```
CREATE OR REPLACE TABLE aggr(k INT, v DECIMAL(10,2), v2 DECIMAL(10, 2));
INSERT INTO aggr VALUES(1, 10, null);
INSERT INTO aggr VALUES(2, 10, 11), (2, 20, 22), (2, 25, null), (2, 30, 35);
```

Copy code

```
SELECT k, REGR_R2(v, v2) FROM aggr GROUP BY k;
```

```
+---+----------------+
| k | regr_r2(v, v2) |
|---+----------------+
| 1 | [NULL]         |
| 2 | 0.9976905312   |
+---+----------------+
```
