Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# DENSE\_RANK

Returns the rank of a value within a group of values, without gaps in the ranks.

The rank value starts at 1 and continues up sequentially.

If two values are the same, they have the same rank.

## Syntax

Copy code

```
DENSE_RANK() OVER ( [ PARTITION BY <expr1> ]
  ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

None.

The function itself takes no arguments because it returns the rank (relative position) of the current row
within the window, which is ordered by `<expr2>`. The ordering of the window determines the rank, so there
is no need to pass an additional parameter to the DENSE\_RANK function.

## Usage notes

- `expr1`
  The column or expression to partition the window by.

  For example, suppose that within each state or province, you want to rank
  farmers in order by the amount of corn they produced. In this case, you
  partition by state.

  If you want only a single group (e.g. you want to rank all farmers in the U.S.
  regardless of which state they live in), then omit the PARTITION BY clause.
- `expr2`
  The column or expression to order (rank) by.

  For example, if you’re ranking farmers to see who produced the most corn
  (within their state), then you would use the `bushels_produced` column. For details,
  see [Examples](#examples) (in this topic).
- Tie values result in the same rank value, but unlike [RANK](/sql-reference/functions/rank), they do not result in gaps in the sequence.

## Examples

Create a table and data:

Copy code

```
CREATE OR REPLACE TABLE corn_production (farmer_id INTEGER, state VARCHAR, bushels FLOAT);

INSERT INTO corn_production (farmer_id, state, bushels) VALUES
  (1, 'Iowa', 100),
  (2, 'Iowa', 110),
  (3, 'Kansas', 120),
  (4, 'Kansas', 130);
```

Show farmers’ corn production in descending order, along with the rank of each
individual farmer’s production (highest = `1`):

Copy code

```
SELECT state, bushels,
    RANK() OVER (ORDER BY bushels DESC),
    DENSE_RANK() OVER (ORDER BY bushels DESC)
  FROM corn_production;
```

```
+--------+---------+-------------------------------------+-------------------------------------------+
| STATE  | BUSHELS | RANK() OVER (ORDER BY BUSHELS DESC) | DENSE_RANK() OVER (ORDER BY BUSHELS DESC) |
|--------+---------+-------------------------------------+-------------------------------------------|
| Kansas |     130 |                                   1 |                                         1 |
| Kansas |     120 |                                   2 |                                         2 |
| Iowa   |     110 |                                   3 |                                         3 |
| Iowa   |     100 |                                   4 |                                         4 |
+--------+---------+-------------------------------------+-------------------------------------------+
```

Within each state, show farmers’ corn production in descending order, along with the rank of each
individual farmer’s production (highest = `1`):

Copy code

```
SELECT state, bushels,
    RANK() OVER (PARTITION BY state ORDER BY bushels DESC),
    DENSE_RANK() OVER (PARTITION BY state ORDER BY bushels DESC)
  FROM corn_production;
```

```
+--------+---------+--------------------------------------------------------+--------------------------------------------------------------+
| STATE  | BUSHELS | RANK() OVER (PARTITION BY STATE ORDER BY BUSHELS DESC) | DENSE_RANK() OVER (PARTITION BY STATE ORDER BY BUSHELS DESC) |
|--------+---------+--------------------------------------------------------+--------------------------------------------------------------|
| Iowa   |     110 |                                                      1 |                                                            1 |
| Iowa   |     100 |                                                      2 |                                                            2 |
| Kansas |     130 |                                                      1 |                                                            1 |
| Kansas |     120 |                                                      2 |                                                            2 |
+--------+---------+--------------------------------------------------------+--------------------------------------------------------------+
```

The query and output below show how tie values are handled by the RANK and DENSE\_RANK functions. Note that for DENSE\_RANK,
the ranks are `1`, `2`, `3`, `3`, `4`. Unlike with the output from the RANK function, the rank `4` is not skipped
because there was a tie for rank `3`.

Copy code

```
INSERT INTO corn_production (farmer_id, state, bushels) VALUES
  (5, 'Iowa', 110);

SELECT state, bushels,
    RANK() OVER (ORDER BY bushels DESC),
    DENSE_RANK() OVER (ORDER BY bushels DESC)
  FROM corn_production;
```

```
+--------+---------+-------------------------------------+-------------------------------------------+
| STATE  | BUSHELS | RANK() OVER (ORDER BY BUSHELS DESC) | DENSE_RANK() OVER (ORDER BY BUSHELS DESC) |
|--------+---------+-------------------------------------+-------------------------------------------|
| Kansas |     130 |                                   1 |                                         1 |
| Kansas |     120 |                                   2 |                                         2 |
| Iowa   |     110 |                                   3 |                                         3 |
| Iowa   |     110 |                                   3 |                                         3 |
| Iowa   |     100 |                                   5 |                                         4 |
+--------+---------+-------------------------------------+-------------------------------------------+
```
