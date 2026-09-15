Categories:
:   [Window functions](/sql-reference/functions-window) (Ranking)

# PERCENT\_RANK

Returns the relative rank of a value within a group of values, specified as a percentage ranging from 0.0 to 1.0.

## Syntax

Copy code

```
PERCENT_RANK()
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <fixedRangeFrame> ] )
```

Where:

> Copy code
>
> ```
> fixedRangeFrame ::=
>     {
>        RANGE UNBOUNDED PRECEDING
>      | RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
>      | RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
>     }
> ```

## Usage notes

- `expr1` specifies the column (or expression) to partition by.

  For example, suppose that within each state or province, you want to rank
  farmers in order by the amount of corn they produced. In this case, you
  partition by state.

  If you want only a single group (e.g. you want to rank all farmers in the U.S.
  regardless of which state they live in), then omit the `PARTITION BY` clause.
- `expr2` specifies the column (or expression) that you want to rank by.

  For example, if you’re ranking farmers to see who produced the most corn
  (within their state), then you would use the `bushels_produced` column. For details,
  see [Examples](#examples) (in this topic).
- PERCENT\_RANK is calculated as:
  If n is 1:

  `PERCENT_RANK = 0`

  If n is greater than 1:

  `PERCENT_RANK = (r - 1) / (n - 1)`

  where `r` is the [RANK](/sql-reference/functions/rank) of the row and `n` is the number of rows in the window partition.
- Values range from 0.0 to 1.0. You can multiply by 100 to get a true percent.
- PERCENT\_RANK supports range-based window frames with fixed boundaries only. For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Examples

Copy code

```
SELECT
    exchange,
    symbol,
    PERCENT_RANK() OVER (PARTITION BY exchange ORDER BY price) AS percent_rank
  FROM trades;
```

```
+--------+------+------------+
%exchange%symbol%PERCENT_RANK%
+--------+------+------------+
|C       |SPY   |         0.0|
|C       |AAPL  |         0.5|
|C       |AAPL  |         1.0|
|N       |YHOO  |         0.0|
|N       |QQQ   |         0.2|
|N       |QQQ   |         0.4|
|N       |SPY   |         0.6|
|N       |SPY   |         0.6|
|N       |AAPL  |         1.0|
|Q       |YHOO  |         0.0|
|Q       |YHOO  |         0.2|
|Q       |MSFT  |         0.4|
|Q       |MSFT  |         0.6|
|Q       |QQQ   |         0.8|
|Q       |QQQ   |         1.0|
|P       |YHOO  |         0.0|
|P       |MSFT  |        0.25|
|P       |MSFT  |         0.5|
|P       |SPY   |        0.75|
|P       |AAPL  |         1.0|
+--------+------+------------+
```
