Categories:
:   [Window functions](/sql-reference/functions-window) (Ranking)

# CUME\_DIST

Finds the cumulative distribution of a value with regard to other values within the same window partition.

## Syntax

Copy code

```
CUME_DIST() OVER ( [ PARTITION BY <partition_expr> ]
  ORDER BY <order_expr> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

## Arguments

`partition_expr`
:   This is the optional expression to use to group rows into partitions.

`order_expr`
:   This expression specifies the order of the rows within each partition.

## Returns

The data type of the returned value is DOUBLE.

## Usage notes

The CUME\_DIST function does not support explicit window frames.

## Examples

Copy code

```
SELECT
    symbol,
    exchange,
    CUME_DIST() OVER (PARTITION BY exchange ORDER BY price) AS cume_dist
  FROM trades;
```

```
+------+--------+------------+
%symbol%exchange|CUME_DIST   |
+------+--------+------------+
|SPY   |C       |0.3333333333|
|AAPL  |C       |         1.0|
|AAPL  |C       |         1.0|
|YHOO  |N       |0.1666666667|
|QQQ   |N       |         0.5|
|QQQ   |N       |         0.5|
|SPY   |N       |0.8333333333|
|SPY   |N       |0.8333333333|
|AAPL  |N       |         1.0|
|YHOO  |Q       |0.3333333333|
|YHOO  |Q       |0.3333333333|
|MSFT  |Q       |0.6666666667|
|MSFT  |Q       |0.6666666667|
|QQQ   |Q       |         1.0|
|QQQ   |Q       |         1.0|
|YHOO  |P       |         0.2|
|MSFT  |P       |         0.6|
|MSFT  |P       |         0.6|
|SPY   |P       |         0.8|
|AAPL  |P       |         1.0|
+------+--------+------------+
```
