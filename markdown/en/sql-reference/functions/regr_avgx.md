Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Linear Regression) , [Window functions](/sql-reference/functions-window)

# REGR\_AVGX

Returns the average of the independent variable for non-null pairs in a group, where `x` is the independent variable and `y` is the dependent variable.

## Syntax

**Aggregate function**

Copy code

```
REGR_AVGX(y, x)
```

**Window function**

Copy code

```
REGR_AVGX(y, x) OVER ( [ PARTITION BY <expr3> ] )
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
- In order for a row to be included in the average, BOTH the x and y values
  must be non-NULL.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

Copy code

```
CREATE OR REPLACE TABLE aggr(k int, v decimal(10,2), v2 decimal(10, 2));
INSERT INTO aggr VALUES(1, 10, NULL);
INSERT INTO aggr VALUES(2, 10, 11), (2, 20, 22), (2, 25, NULL), (2, 30, 35);
```

Copy code

```
SELECT k, REGR_AVGX(v, v2) FROM aggr GROUP BY k;

---+------------------+
 k | regr_avgx(v, v2) |
---+------------------+
 1 | [NULL]           |
 2 | 22.666666667     |
---+------------------+
```
