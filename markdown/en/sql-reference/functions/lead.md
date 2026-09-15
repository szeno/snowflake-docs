Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# LEAD

Accesses data in a subsequent row in the same result set without having to join the table to itself.

See also:
:   [LAG](/sql-reference/functions/lag)

## Syntax

Copy code

```
LEAD ( <expr> [ , <offset> , <default> ] ) [ { IGNORE | RESPECT } NULLS ]
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

## Arguments

`expr`
:   The string expression to be returned.

`offset`
:   The number of rows forward from the current row from which to obtain a value. For example, an `offset` of 2 returns the
    `expr` value with an interval of 2 rows.

    Note that setting a negative offset has the same effect as using the [LAG](/sql-reference/functions/lag) function.

    Default is 1. If `IGNORE NULLS` is specified, maximum is 1,000,000.

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

Copy code

```
CREATE OR REPLACE TABLE sales(
  emp_id INTEGER,
  year INTEGER,
  revenue DECIMAL(10,2));

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

SELECT emp_id,
       year,
       revenue,
       LEAD(revenue) OVER (PARTITION BY emp_id ORDER BY year) - revenue AS diff_to_next
  FROM sales
  ORDER BY emp_id, year;
```

```
+--------+------+----------+--------------+
| EMP_ID | YEAR |  REVENUE | DIFF_TO_NEXT |
|--------+------+----------+--------------|
|      0 | 2010 |  1000.00 |       500.00 |
|      0 | 2011 |  1500.00 |     -1000.00 |
|      0 | 2012 |   500.00 |       250.00 |
|      0 | 2013 |   750.00 |         NULL |
|      1 | 2010 | 10000.00 |      2500.00 |
|      1 | 2011 | 12500.00 |      2500.00 |
|      1 | 2012 | 15000.00 |      5000.00 |
|      1 | 2013 | 20000.00 |         NULL |
|      2 | 2012 |   500.00 |       300.00 |
|      2 | 2013 |   800.00 |         NULL |
+--------+------+----------+--------------+
```

Copy code

```
CREATE OR REPLACE TABLE t1 (
  c1 NUMBER,
  c2 NUMBER);

INSERT INTO t1 VALUES
  (1,5),
  (2,4),
  (3,NULL),
  (4,2),
  (5,NULL),
  (6,NULL),
  (7,6);

SELECT c1,
       c2,
       LEAD(c2) IGNORE NULLS OVER (ORDER BY c1)
  FROM t1;
```

```
+----+------+------------------------------------------+
| C1 | C2   | LEAD(C2) IGNORE NULLS OVER (ORDER BY C1) |
|----+------+------------------------------------------|
|  1 |  5   |                                        4 |
|  2 |  4   |                                        2 |
|  3 | NULL |                                        2 |
|  4 |  2   |                                        6 |
|  5 | NULL |                                        6 |
|  6 | NULL |                                        6 |
|  7 |  6   |                                     NULL |
+----+------+------------------------------------------+
```
