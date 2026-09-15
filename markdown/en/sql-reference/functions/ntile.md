Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# NTILE

Divides an ordered data set equally into the number of buckets specified by `constant_value`. Buckets are sequentially numbered 1 through `constant_value`.

## Syntax

Copy code

```
NTILE( <constant_value> ) OVER ( [ PARTITION BY <expr1> ]
  ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

## Arguments

`constant_value`
:   The desired number of buckets; must be a positive integer value.

`expr1`
:   If you wish to partition the data into groups, specify the criterion
    (usually a column) to partition by. For example, you might partition by
    province.

`expr2`
:   The expression (usually a column) by which to order the rows in the window.
    For example, you might order by timestamp.

## Usage notes

If the data is partitioned, then the data is divided into buckets equally
within each partition. For example, if the number of buckets is 3, and if
the data is partitioned by province, then approximately 1/3 of the
rows for each province are put into each bucket.

If the statement has an ORDER BY clause for the output, as well as an ORDER BY
clause for the NTILE function, the two operate independently; the ORDER BY
for the NTILE function influences which rows are assigned to each bucket,
while the ORDER BY for the output determines the order in which the output
rows are shown.

## Examples

Copy code

```
SELECT
    exchange,
    symbol,
    NTILE(4) OVER (PARTITION BY exchange ORDER BY shares) AS ntile_4
  FROM trades
  ORDER BY exchange, NTILE_4;
```

```
+--------+------+-------+
%exchange%symbol%NTILE_4%
+--------+------+-------+
|C       |SPY   |      1|
|C       |AAPL  |      2|
|C       |AAPL  |      3|
|N       |SPY   |      1|
|N       |AAPL  |      1|
|N       |SPY   |      2|
|N       |QQQ   |      2|
|N       |QQQ   |      3|
|N       |YHOO  |      4|
|Q       |MSFT  |      1|
|Q       |YHOO  |      1|
|Q       |MSFT  |      2|
|Q       |YHOO  |      2|
|Q       |QQQ   |      3|
|Q       |QQQ   |      4|
|P       |AAPL  |      1|
|P       |YHOO  |      1|
|P       |MSFT  |      2|
|P       |SPY   |      3|
|P       |MSFT  |      4|
+--------+------+-------+
```
