Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# LAG

Accesses data in a previous row in the same result set without having to join the table to itself.

See also:
:   [LEAD](/sql-reference/functions/lead)

## Syntax

Copy code

```
LAG ( <expr> [ , <offset> , <default> ] ) [ { IGNORE | RESPECT } NULLS ]
    OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

## Arguments

`expr`
:   The expression to be returned based on the specified offset.

`offset`
:   The number of rows backward from the current row from which to obtain a value. For example, an `offset` of 2 returns
    the `expr` value with an interval of 2 rows.

    Note that setting a negative offset has the same effect as using the [LEAD](/sql-reference/functions/lead) function.

    Default is 1.

`default`
:   The expression to return when the offset goes out of the bounds of the window. Supports any expression whose type is compatible with `expr`.

    Default is NULL.

`{ IGNORE | RESPECT } NULLS`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    - `IGNORE NULLS` excludes any row whose expression evaluates to NULL when offset rows are counted.
    - `RESPECT NULLS` includes any row whose expression evaluates to NULL when offset rows are counted.

    Default: `RESPECT NULLS`

## Usage notes

- The PARTITION BY clause partitions the result set produced by the FROM clause into partitions to which the function is applied.
  For more information, see [Window function syntax and usage](/sql-reference/functions-window-syntax).
- The ORDER BY clause orders the data within each partition.

## Examples

Create the table and load the data:

Copy code

```
CREATE OR REPLACE TABLE sales(
  emp_id INTEGER,
  year INTEGER,
  revenue DECIMAL(10,2));
```

Copy code

```
INSERT INTO sales VALUES
  (0, 2010, 1000),
  (0, 2011, 1500),
  (0, 2012, 500),
  (0, 2013, 750);
INSERT INTO sales VALUES
  (1, 2010, 10000),
  (1, 2011, 12500),
  (1, 2012, 15000),
  (1, 2013, 20000);
INSERT INTO sales VALUES
  (2, 2012, 500),
  (2, 2013, 800);
```

This query shows the difference between this year’s revenue and the previous year’s revenue:

Copy code

```
SELECT emp_id, year, revenue,
       revenue - LAG(revenue, 1, 0) OVER (PARTITION BY emp_id ORDER BY year) AS diff_to_prev
  FROM sales
  ORDER BY emp_id, year;
```

```
+--------+------+----------+--------------+
| EMP_ID | YEAR |  REVENUE | DIFF_TO_PREV |
|--------+------+----------+--------------|
|      0 | 2010 |  1000.00 |      1000.00 |
|      0 | 2011 |  1500.00 |       500.00 |
|      0 | 2012 |   500.00 |     -1000.00 |
|      0 | 2013 |   750.00 |       250.00 |
|      1 | 2010 | 10000.00 |     10000.00 |
|      1 | 2011 | 12500.00 |      2500.00 |
|      1 | 2012 | 15000.00 |      2500.00 |
|      1 | 2013 | 20000.00 |      5000.00 |
|      2 | 2012 |   500.00 |       500.00 |
|      2 | 2013 |   800.00 |       300.00 |
+--------+------+----------+--------------+
```

Create another table and load the data:

Copy code

```
CREATE OR REPLACE TABLE t1 (
  col_1 NUMBER,
  col_2 NUMBER);
```

Copy code

```
INSERT INTO t1 VALUES
  (1, 5),
  (2, 4),
  (3, NULL),
  (4, 2),
  (5, NULL),
  (6, NULL),
  (7, 6);
```

This query shows how the IGNORE NULLS clause affects the output.
All rows (except the first) contain non-NULL values even if the preceding row contained NULL.
If the preceding row contained NULL, then the current row uses the most recent non-NULL value.

Copy code

```
SELECT col_1,
       col_2,
       LAG(col_2) IGNORE NULLS OVER (ORDER BY col_1)
  FROM t1
  ORDER BY col_1;
```

```
+-------+-------+-----------------------------------------------+
| COL_1 | COL_2 | LAG(COL_2) IGNORE NULLS OVER (ORDER BY COL_1) |
|-------+-------+-----------------------------------------------|
|     1 |     5 |                                          NULL |
|     2 |     4 |                                             5 |
|     3 |  NULL |                                             4 |
|     4 |     2 |                                             4 |
|     5 |  NULL |                                             2 |
|     6 |  NULL |                                             2 |
|     7 |     6 |                                             2 |
+-------+-------+-----------------------------------------------+
```
