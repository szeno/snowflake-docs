Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)

# GROUPING

Describes which of a list of expressions are grouped in a row produced by a [GROUP BY](/sql-reference/constructs/group-by) query.

Aliases:
:   [GROUPING\_ID](/sql-reference/functions/grouping_id)

## Syntax

Copy code

```
GROUPING( <expr1> [ , <expr2> , ... ] )
```

## Usage notes

GROUPING is not an aggregate function, but rather a utility function that can be used alongside aggregation, to determine the level of aggregation a row was generated for:

- GROUPING(`expr`) returns 0 for a row that is grouped on `expr`, and 1 for a row that is not grouped on `expr`.
- GROUPING(`expr1`, `expr2` , … , `exprN`) returns the integer representation of a bit-vector containing GROUPING(`expr1`) , GROUPING(`expr2`) , … , GROUPING(`exprN`).

## Examples

Group by sets:

> Create and populate a table with values:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE TABLE aggr2(col_x int, col_y int, col_z int);
> > INSERT INTO aggr2 VALUES(1, 2, 1), (1, 2, 3);
> > INSERT INTO aggr2 VALUES(2, 1, 10), (2, 2, 11), (2, 2, 3);
> > ```
>
> Show the values in the table:
>
> > Copy code
> >
> > ```
> > SELECT * FROM aggr2 ORDER BY col_x, col_y, col_z;
> > +-------+-------+-------+
> > | COL_X | COL_Y | COL_Z |
> > |-------+-------+-------|
> > |     1 |     2 |     1 |
> > |     1 |     2 |     3 |
> > |     2 |     1 |    10 |
> > |     2 |     2 |     3 |
> > |     2 |     2 |    11 |
> > +-------+-------+-------+
> > ```
>
> Output:
>
> > Copy code
> >
> > ```
> > SELECT col_x, col_y, sum(col_z), 
> >        grouping(col_x), grouping(col_y), grouping(col_x, col_y)
> >     FROM aggr2 GROUP BY GROUPING SETS ((col_x), (col_y), ())
> >     ORDER BY 1, 2;
> > +-------+-------+------------+-----------------+-----------------+------------------------+
> > | COL_X | COL_Y | SUM(COL_Z) | GROUPING(COL_X) | GROUPING(COL_Y) | GROUPING(COL_X, COL_Y) |
> > |-------+-------+------------+-----------------+-----------------+------------------------|
> > |     1 |  NULL |          4 |               0 |               1 |                      1 |
> > |     2 |  NULL |         24 |               0 |               1 |                      1 |
> > |  NULL |     1 |         10 |               1 |               0 |                      2 |
> > |  NULL |     2 |         18 |               1 |               0 |                      2 |
> > |  NULL |  NULL |         28 |               1 |               1 |                      3 |
> > +-------+-------+------------+-----------------+-----------------+------------------------+
> > ```
