Categories:
:   [Query syntax](/sql-reference/constructs)

# GROUP BY CUBE

GROUP BY CUBE is an extension of the [GROUP BY](/sql-reference/constructs/group-by) clause, similar to
[GROUP BY ROLLUP](/sql-reference/constructs/group-by-rollup). Like ROLLUP, CUBE produces aggregated rows at
multiple levels. However, while ROLLUP creates aggregations that follow a natural hierarchy (for example,
city rolls up to state, and state rolls up to country), CUBE creates aggregations for all possible combinations of the specified
columns. These include both the hierarchical aggregations that ROLLUP would produce and additional
“cross-tabulation” rows that aggregate across each individual dimension independently.

CUBE can be combined with other GROUP BY expressions. For example, you can write
`GROUP BY x, CUBE(y, z)` to group by column `x` in combination with cube
aggregations on `y` and `z`.

A CUBE grouping is equivalent to a series of grouping sets and is essentially a shorter specification. The `N` elements of a CUBE
specification correspond to `2^N GROUPING SETS`.

## See also

- [GROUPING](/sql-reference/functions/grouping) (Utility function to identify which grouping level produced each row)
- [GROUP BY GROUPING SETS](/sql-reference/constructs/group-by-grouping-sets)
- [GROUP BY ROLLUP](/sql-reference/constructs/group-by-rollup)

## Syntax

Copy code

```
SELECT ...
FROM ...
[ ... ]
GROUP BY [ groupItem [ , groupItem [ , ... ] ] , ] CUBE ( groupItem [ , groupItem [ , ... ] ] )
[ ... ]
```

Where:

> Copy code
>
> ```
> groupItem ::= { <column_alias> | <position> | <expr> }
> ```

## Parameters

`column_alias`
:   Column alias appearing in the query block’s [SELECT](/sql-reference/sql/select) list.

`position`
:   Position of an expression in the [SELECT](/sql-reference/sql/select) list.

`expr`
:   Any expression on tables in the current scope.

## Usage notes

- Snowflake allows up to 7 elements (equivalent to 128 grouping sets) in each cube.

## Examples

Start by creating and loading a table with information about sales from
a chain store that has branches in different cities and states/territories.

> Copy code
>
> ```
> -- Create some tables and insert some rows.
> CREATE TABLE products (product_ID INTEGER, wholesale_price REAL);
> INSERT INTO products (product_ID, wholesale_price) VALUES 
>     (1, 1.00),
>     (2, 2.00);
>
> CREATE TABLE sales (product_ID INTEGER, retail_price REAL, 
>     quantity INTEGER, city VARCHAR, state VARCHAR);
> INSERT INTO sales (product_id, retail_price, quantity, city, state) VALUES 
>     (1, 2.00,  1, 'SF', 'CA'),
>     (1, 2.00,  2, 'SJ', 'CA'),
>     (2, 5.00,  4, 'SF', 'CA'),
>     (2, 5.00,  8, 'SJ', 'CA'),
>     (2, 5.00, 16, 'Miami', 'FL'),
>     (2, 5.00, 32, 'Orlando', 'FL'),
>     (2, 5.00, 64, 'SJ', 'PR');
> ```

Run a cube query that shows profit by city, state, and total across all states.
The example below shows a query that has three “levels”:

- Each city.
- Each state.
- All revenue combined.

This example uses `ORDER BY state, city NULLS LAST` to ensure that each state’s rollup comes immediately after all of
the cities in that state, and that the final rollup appears at the end of the output.

> Copy code
>
> ```
> SELECT state, city, SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit 
>  FROM products AS p, sales AS s
>  WHERE s.product_ID = p.product_ID
>  GROUP BY CUBE (state, city)
>  ORDER BY state, city NULLS LAST
>  ;
> +-------+---------+--------+
> | STATE | CITY    | PROFIT |
> |-------+---------+--------|
> | CA    | SF      |     13 |
> | CA    | SJ      |     26 |
> | CA    | NULL    |     39 |
> | FL    | Miami   |     48 |
> | FL    | Orlando |     96 |
> | FL    | NULL    |    144 |
> | PR    | SJ      |    192 |
> | PR    | NULL    |    192 |
> | NULL  | Miami   |     48 |
> | NULL  | Orlando |     96 |
> | NULL  | SF      |     13 |
> | NULL  | SJ      |    218 |
> | NULL  | NULL    |    375 |
> +-------+---------+--------+
> ```

Some rollup rows contain NULL values. For example, the last row in the table contains a NULL value for the city and
a NULL value for the state because the data is for all cities and states, not a specific city and state.

The [GROUPING](/sql-reference/functions/grouping) utility function can help distinguish between NULL values
that result from the cube aggregation versus actual NULL values in the data.

Both GROUP BY CUBE and GROUP BY ROLLUP produce one row for each city/state pair, and both GROUP BY clauses also produce
rollup rows for each individual state and for all states combined. The difference between the two GROUP BY clauses is that
GROUP BY CUBE also produces an output row for each city name (`Miami`, `SJ`, and so on).

Take care when using GROUP BY CUBE on hierarchical data. In this example, the row for `SJ` contains totals for both the city
named `SJ` in the state of `CA` and the city named `SJ` in the territory of `PR`, even though the only relationship between those
cities is that they have the same name. In general, use GROUP BY ROLLUP to analyze hierarchical data, and GROUP BY CUBE to
analyze data across independent axes.
