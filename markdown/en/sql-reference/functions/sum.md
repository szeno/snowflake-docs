Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window function syntax and usage](/sql-reference/functions-window-syntax) (General)

# SUM

Returns the sum of non-NULL records for `expr`. You can use the DISTINCT keyword to compute the sum of unique
non-null values. If all records inside a group are NULL, the function returns NULL.

See also:
:   [COUNT](/sql-reference/functions/count) , [MAX](/sql-reference/functions/max) , [MIN](/sql-reference/functions/min)

## Syntax

**Aggregate function**

Copy code

```
SUM( [ DISTINCT ] <expr1> )
```

**Window function**

Copy code

```
SUM( [ DISTINCT ] <expr1> ) OVER (
                                 [ PARTITION BY <expr2> ]
                                 [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                 )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`expr1`
:   This is an expression that evaluates to a numeric data type (INTEGER, FLOAT, DECIMAL, etc.).

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the optional expression to order by within each partition. (This does not control the order of the
    entire query output.)

## Usage notes

- Numeric values are summed into an equivalent or larger data type.
- When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast
  cannot be performed, an error is returned.
- When this function is called as a window function with an OVER clause that contains an ORDER BY clause:
  - A window frame is required. If no window frame is specified explicitly, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](/sql-reference/functions-window-syntax).
  - The DISTINCT keyword cannot be used.

## Examples

Copy code

```
CREATE OR REPLACE TABLE sum_example (k INT, d DECIMAL(10,5),
  s1 VARCHAR(10), s2 VARCHAR(10));

INSERT INTO sum_example VALUES
  (1, 1.1, '1.1', 'one'),
  (1, 10, '10', 'ten'),
  (2, 2.2, '2.2', 'two'),
  (2, NULL, NULL, 'null'),
  (3, NULL, NULL, 'null'),
  (NULL, 9, '9.9', 'nine');

SELECT *
  FROM sum_example;
```

```
+------+----------+------+------+
|    K |        D | S1   | S2   |
|------+----------+------+------|
|    1 |  1.10000 | 1.1  | one  |
|    1 | 10.00000 | 10.0 | ten  |
|    2 |  2.20000 | 2.2  | two  |
|    2 |     NULL | NULL | null |
|    3 |     NULL | NULL | null |
| NULL |  9.00000 | 9.9  | nine |
+------+----------+------+------+
```

Copy code

```
SELECT SUM(d), SUM(s1)
  FROM sum_example;
```

```
+----------+---------+
|   SUM(D) | SUM(S1) |
|----------+---------|
| 22.30000 |    23.2 |
+----------+---------+
```

Copy code

```
SELECT k, SUM(d), SUM(s1)
  FROM sum_example
  GROUP BY k;
```

```
+------+----------+---------+
|    K |   SUM(D) | SUM(S1) |
|------+----------+---------|
|    1 | 11.10000 |    11.1 |
|    2 |  2.20000 |     2.2 |
|    3 |     NULL |    NULL |
| NULL |  9.00000 |     9.9 |
+------+----------+---------+
```

Copy code

```
SELECT SUM(s2)
  FROM sum_example;
```

```
100038 (22018): Numeric value 'one' is not recognized
```

The script below shows the use of this function (and some other aggregate window functions):

Copy code

```
CREATE OR REPLACE TABLE example_cumulative (p INT, o INT, i INT);

INSERT INTO example_cumulative VALUES
  (  0, 1, 10), (0, 2, 20), (0, 3, 30),
  (100, 1, 10), (100, 2, 30), (100, 2, 5), (100, 3, 11), (100, 3, 120),
  (200, 1, 10000), (200, 1, 200), (200, 1, 808080), (200, 2, 33333), (200, 3, NULL), (200, 3, 4),
  (300, 1, NULL), (300, 1, NULL);
```

Copy code

```
SELECT
    p, o, i,
    COUNT(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS count_i_rows_pre,
    SUM(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_i_rows_pre,
    AVG(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS avg_i_rows_pre,
    MIN(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS min_i_rows_pre,
    MAX(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS max_i_rows_pre
  FROM example_cumulative
  ORDER BY p, o;
```

```
+-----+---+--------+------------------+----------------+----------------+----------------+----------------+
|   P | O |      I | COUNT_I_ROWS_PRE | SUM_I_ROWS_PRE | AVG_I_ROWS_PRE | MIN_I_ROWS_PRE | MAX_I_ROWS_PRE |
|-----+---+--------+------------------+----------------+----------------+----------------+----------------|
|   0 | 1 |     10 |                1 |             10 |         10.000 |             10 |             10 |
|   0 | 2 |     20 |                2 |             30 |         15.000 |             10 |             20 |
|   0 | 3 |     30 |                3 |             60 |         20.000 |             10 |             30 |
| 100 | 1 |     10 |                1 |             10 |         10.000 |             10 |             10 |
| 100 | 2 |     30 |                2 |             40 |         20.000 |             10 |             30 |
| 100 | 2 |      5 |                3 |             45 |         15.000 |              5 |             30 |
| 100 | 3 |     11 |                4 |             56 |         14.000 |              5 |             30 |
| 100 | 3 |    120 |                5 |            176 |         35.200 |              5 |            120 |
| 200 | 1 |  10000 |                1 |          10000 |      10000.000 |          10000 |          10000 |
| 200 | 1 |    200 |                2 |          10200 |       5100.000 |            200 |          10000 |
| 200 | 1 | 808080 |                3 |         818280 |     272760.000 |            200 |         808080 |
| 200 | 2 |  33333 |                4 |         851613 |     212903.250 |            200 |         808080 |
| 200 | 3 |   NULL |                4 |         851613 |     212903.250 |            200 |         808080 |
| 200 | 3 |      4 |                5 |         851617 |     170323.400 |              4 |         808080 |
| 300 | 1 |   NULL |                0 |           NULL |           NULL |           NULL |           NULL |
| 300 | 1 |   NULL |                0 |           NULL |           NULL |           NULL |           NULL |
+-----+---+--------+------------------+----------------+----------------+----------------+----------------+
```
