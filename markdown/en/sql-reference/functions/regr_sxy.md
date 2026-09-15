Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Linear Regression) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# REGR\_SXY

Returns REGR\_COUNT(expr1, expr2) \* COVAR\_POP(expr1, expr2) for non-null
pairs.

## Syntax

**Aggregate function**

Copy code

```
REGR_SXY(y, x)
```

**Window function**

Copy code

```
REGR_SXY(y, x) OVER ( [ PARTITION BY <expr3> ] )
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

SELECT k, REGR_SXY(v, v2) FROM aggr GROUP BY k;
```

```
+---+-----------------+
| k | regr_sxy(v, v2) |
+---+-----------------+
| 1 | [NULL]          |
| 2 | 240             |
+---+-----------------+
```
