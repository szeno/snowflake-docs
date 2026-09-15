Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window)

# PERCENTILE\_DISC

Returns a percentile value based on a discrete distribution of the input
column (specified in `order_by_expr`). The returned value is that
whose row has the smallest CUME\_DIST value that is greater than or equal to
the given percentile. NULL values are ignored in the calculation.

See also:
:   [PERCENTILE\_CONT](/sql-reference/functions/percentile_cont)

## Syntax

**Aggregate function**

Copy code

```
PERCENTILE_DISC( <percentile> ) WITHIN GROUP (ORDER BY <order_by_expr> )
```

**Window function**

Copy code

```
PERCENTILE_DISC( <percentile> )
  WITHIN GROUP (ORDER BY <order_by_expr> )
  OVER ( [ PARTITION BY <expr3> ] )
```

## Arguments

`percentile`
:   The percentile of the value that you want to find. The percentile must be a
    constant between 0.0 and 1.0. For example, if you want to find the value
    at the 90th percentile, specify 0.9.

`order_by_expr`
:   The expression (typically a column name) by which to order the values. For
    example, if you want to want to find the student whose math SAT score is at
    the 90th percentile, then specify the column containing the math SAT score.

    Note that this is also implicitly the column from which the returned value
    is chosen. For example, if you order by math SAT scores, then the result
    is one of the math SAT scores. You cannot order by one column and get
    a percentile value for a different column.

`expr3`
:   This is the optional expression used to group rows into partitions.

## Returns

Returns the value that is at the specified percentile.

## Usage notes

- The `percentile` argument to the function must be a constant.
- DISTINCT is not supported for this function.
- The function PERCENTILE\_CONT interpolates between the two closest
  values, while the function PERCENTILE\_DISC chooses the closest value
  rather than interpolating.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

The following example shows the values at the 25th percentile (0.25) within
various groups:

Create and populate a table with values:

Copy code

```
CREATE OR REPLACE TABLE aggr (k INT, v DECIMAL(10,2));

INSERT INTO aggr (k, v) VALUES
  (0,  0),
  (0, 10),
  (0, 20),
  (0, 30),
  (0, 40),
  (1, 10),
  (1, 20),
  (2, 10),
  (2, 20),
  (2, 25),
  (2, 30),
  (3, 60),
  (4, NULL);
```

Run a query and show the output:

Copy code

```
SELECT k, PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY v)
  FROM aggr
  GROUP BY k
  ORDER BY k;
```

```
+---+-------------------------------------------------+
| K | PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY V) |
|---+-------------------------------------------------|
| 0 |                                           10.00 |
| 1 |                                           10.00 |
| 2 |                                           10.00 |
| 3 |                                           60.00 |
| 4 |                                            NULL |
+---+-------------------------------------------------+
```
