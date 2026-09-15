Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window)

# MEDIAN

Determines the median of a set of values.

## Syntax

**Aggregate function**

Copy code

```
MEDIAN( <expr> )
```

**Window function**

Copy code

```
MEDIAN( <expr> ) OVER ( [ PARTITION BY <expr2> ] )
```

## Argument

`expr`
:   The expression must evaluate to a numeric data type (INTEGER, FLOAT,
    DECIMAL, or equivalent).

## Returns

Returns a FLOAT or DECIMAL (fixed-point) number, depending upon the
input.

## Usage notes

- If the number of non-NULL values is an odd number greater than or equal to 1,
  this returns the median (“center”) value of the non-NULL values.
- If the number of non-NULL values is an even number, this returns a value
  equal to the average of the two center values. For example, if the
  values are 1, 3, 5, and 20, then this returns 4 (the average of 3 and 5).
- If all values are NULL, this returns NULL.
- If the number of non-NULL values is 0, this returns NULL.
- DISTINCT is not supported for this function.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

This shows how to use the function.

Create an empty table.

Copy code

```
CREATE OR REPLACE TABLE aggr (k INT, v DECIMAL(10,2));
```

Get the MEDIAN value for column v. The function returns NULL because
there are no rows.

Copy code

```
SELECT MEDIAN(v)
  FROM aggr;
```

```
+------------+
| MEDIAN (V) |
|------------|
|       NULL |
+------------+
```

Insert some rows:

Copy code

```
INSERT INTO aggr VALUES (1, 10), (1, 20), (1, 21);
INSERT INTO aggr VALUES (2, 10), (2, 20), (2, 25), (2, 30);
INSERT INTO aggr VALUES (3, NULL);
```

Get the MEDIAN value for each group. Note that because the number of
values in group k = 2 is an even number, the returned value for that group
is the mid-point between the two middle numbers.

Copy code

```
SELECT k, MEDIAN(v)
  FROM aggr
  GROUP BY k
  ORDER BY k;
```

```
+---+-----------+
| K | MEDIAN(V) |
|---+-----------|
| 1 |  20.00000 |
| 2 |  22.50000 |
| 3 |      NULL |
+---+-----------+
```
