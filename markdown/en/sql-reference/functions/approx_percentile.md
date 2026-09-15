Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Percentile Estimation) , [Window functions](/sql-reference/functions-window)

# APPROX\_PERCENTILE

Returns an approximated value for the desired percentile (that is, if column `c` has `n` numbers,
APPROX\_PERCENTILE(c, p) returns a number such that approximately `n * p` of the numbers in `c`
are smaller than the returned number).

This function uses an improved version of the t-Digest algorithm. For more information, see
[Estimating Percentile Values](/user-guide/querying-approximate-percentile-values).

See also:
:   [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) , [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine) , [APPROX\_PERCENTILE\_ESTIMATE](/sql-reference/functions/approx_percentile_estimate)

## Syntax

**Aggregate function**

Copy code

```
APPROX_PERCENTILE( <expr> , <percentile> )
```

**Window function**

Copy code

```
APPROX_PERCENTILE( <expr> , <percentile> ) OVER ( [ PARTITION BY <expr3> ] )
```

## Arguments

`expr`
:   A valid expression, such as a column name, that evaluates to a numeric value.

`percentile`
:   A constant real value greater than or equal to `0.0` and less than `1.0`.
    This indicates the percentile (from 0 to 99.999…).
    For example, the value 0.65 indicates the 65th percentile.

`expr3`
:   This is the optional expression used to group rows into partitions.

## Returns

The output is returned as a DOUBLE value.

## Usage notes

- Percentile works only on numeric values, so `expr` should produce
  values that are numbers or can be cast to numbers.
- The values returned are not necessarily in the data set.
- The value returned is an approximation. The size of the data set and the
  skew in the data set affect the accuracy of the approximation.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

- Decimal-float ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)) values aren’t supported.

## Examples

Demonstrate the APPROX\_PERCENTILE function:

Create and populate a table with values:

Copy code

```
CREATE TABLE testtable (c1 INTEGER);

INSERT INTO testtable (c1) VALUES
  (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
```

Run queries and show the output:

Copy code

```
SELECT APPROX_PERCENTILE(c1, 0.1)
  FROM testtable;
```

```
+----------------------------+
| APPROX_PERCENTILE(C1, 0.1) |
|----------------------------|
|                        1.5 |
+----------------------------+
```

Copy code

```
SELECT APPROX_PERCENTILE(c1, 0.5)
  FROM testtable;
```

```
+----------------------------+
| APPROX_PERCENTILE(C1, 0.5) |
|----------------------------|
|                        5.5 |
+----------------------------+
```

Note that the value returned in this case is higher than any value actually
in the data set:

Copy code

```
SELECT APPROX_PERCENTILE(c1, 0.999)
  FROM testtable;
```

```
+------------------------------+
| APPROX_PERCENTILE(C1, 0.999) |
|------------------------------|
|                         10.5 |
+------------------------------+
```
