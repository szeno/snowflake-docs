Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)

# GROUPING\_ID

Describes which of a list of expressions are grouped in a row produced by a [GROUP BY](/sql-reference/constructs/group-by) query.

Alias for [GROUPING](/sql-reference/functions/grouping).

## Syntax

Copy code

```
GROUPING_ID( <expr1> [ , <expr2> , ... ] )
```

## Usage notes

GROUPING\_ID is not an aggregate function, but rather a utility function that can be used alongside aggregation, to determine the level of aggregation a row was generated for:

- GROUPING\_ID(`expr`) returns 0 for a row that is grouped on `expr`, and 1 for a row that is not grouped on `expr`.
- GROUPING\_ID(`expr1`, `expr2` , … , `exprN`) returns the integer representation of a bit-vector containing GROUPING\_ID(`expr1`) , GROUPING\_ID(`expr2`) , … , GROUPING\_ID(`exprN`).

## Examples

The examples use the following table and data:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE aggr2(col_x int, col_y int, col_z int);
> INSERT INTO aggr2 VALUES (1, 2, 1), 
>                          (1, 2, 3);
> INSERT INTO aggr2 VALUES (2, 1, 10), 
>                          (2, 2, 11), 
>                          (2, 2, 3);
> ```

This example groups on col\_x. Calling `GROUPING_ID(col_x)` returns 0, indicating that col\_x is indeed one of
the grouping columns.

> Copy code
>
> ```
> SELECT col_x, sum(col_z), GROUPING_ID(col_x)
>     FROM aggr2 
>     GROUP BY col_x
>     ORDER BY col_x;
> +-------+------------+--------------------+
> | COL_X | SUM(COL_Z) | GROUPING_ID(COL_X) |
> |-------+------------+--------------------|
> |     1 |          4 |                  0 |
> |     2 |         24 |                  0 |
> +-------+------------+--------------------+
> ```

This query groups by sets:

> Copy code
>
> ```
> SELECT col_x, col_y, sum(col_z), 
>        GROUPING_ID(col_x), 
>        GROUPING_ID(col_y), 
>        GROUPING_ID(col_x, col_y)
>     FROM aggr2 
>     GROUP BY GROUPING SETS ((col_x), (col_y), ())
>     ORDER BY col_x ASC, col_y DESC;
> +-------+-------+------------+--------------------+--------------------+---------------------------+
> | COL_X | COL_Y | SUM(COL_Z) | GROUPING_ID(COL_X) | GROUPING_ID(COL_Y) | GROUPING_ID(COL_X, COL_Y) |
> |-------+-------+------------+--------------------+--------------------+---------------------------|
> |     1 |  NULL |          4 |                  0 |                  1 |                         1 |
> |     2 |  NULL |         24 |                  0 |                  1 |                         1 |
> |  NULL |  NULL |         28 |                  1 |                  1 |                         3 |
> |  NULL |     2 |         18 |                  1 |                  0 |                         2 |
> |  NULL |     1 |         10 |                  1 |                  0 |                         2 |
> +-------+-------+------------+--------------------+--------------------+---------------------------+
> ```
