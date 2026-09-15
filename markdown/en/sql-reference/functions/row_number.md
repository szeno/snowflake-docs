Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# ROW\_NUMBER

Returns a unique row number for each row within a window partition.

The row number starts at 1 and continues up sequentially.

## Syntax

Copy code

```
ROW_NUMBER() OVER (
  [ PARTITION BY <expr1> [, <expr2> ... ] ]
  ORDER BY <expr3> [ , <expr4> ... ] [ { ASC | DESC } [ NULLS { FIRST | LAST } ] ]
  )
```

## Arguments

None.

## Usage notes

- `expr1` and `expr2` specify the column(s) or expression(s)
  to partition by. You can partition by 0, 1, or more expressions.

  For example, suppose that you are selecting data across multiple states
  (or provinces) and you want row numbers from 1 to N within each
  state; in that case, you can partition by the state.

  If you want only a single group, then omit the PARTITION BY clause.
- `expr3` and `expr4` specify the column(s) or expression(s) to
  use to determine the order of the rows. You can order by 1 or more
  expressions.

  For example, if want to list farmers in order by production of corn, then
  use the `bushels_produced` column. For details,
  see [Examples](#examples) (in this topic).

## Examples

The query below shows how to assign row numbers within partitions. In this
case, the partitions are stock exchanges (for example, “N” for “NASDAQ”).

Copy code

```
SELECT
    symbol,
    exchange,
    shares,
    ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY shares) AS row_number
  FROM trades;
```

```
+------+--------+------+----------+
%SYMBOL%EXCHANGE%SHARES%ROW_NUMBER|
+------+--------+------+----------+
|SPY   |C       |   250|         1|
|AAPL  |C       |   250|         2|
|AAPL  |C       |   300|         3|
|SPY   |N       |   100|         1|
|AAPL  |N       |   300|         2|
|SPY   |N       |   500|         3|
|QQQ   |N       |   800|         4|
|QQQ   |N       |  2000|         5|
|YHOO  |N       |  5000|         6|
+------+--------+------+----------+
```
