Categories:
:   [Query syntax](/sql-reference/constructs)

# GROUP BY ROLLUP

GROUP BY ROLLUP is an extension of the [GROUP BY](/sql-reference/constructs/group-by) clause that produces
aggregated rows at multiple levels of a hierarchy (in addition to the detailed grouped rows). For example,
if you group by city and state, ROLLUP produces aggregations for each city/state combination, each state
total, and a grand total across all states. These aggregations are computed using the same aggregate
functions specified in the SELECT clause.

ROLLUP can be combined with other GROUP BY expressions. For example, you can write
`GROUP BY x, ROLLUP(y, z)` to group by column `x` in combination with rollup
aggregations on `y` and `z`.

You can think of rollup as generating multiple result sets, each of which
(after the first) is the aggregate of the previous result set. So, for example,
if you own a chain of retail stores, you might want to see the profit for:

- Each store.
- Each city (large cities might have multiple stores).
- Each state.
- Everything (all stores in all states).

You could create separate reports to get that information, but it is more
efficient to scan the data once.

If you are familiar with the concept of [grouping sets](/sql-reference/constructs/group-by-grouping-sets),
you can think of a ROLLUP grouping as equivalent to a series of grouping sets,
but essentially a shorter specification. The `N` elements of
a ROLLUP specification correspond to `N+1 GROUPING SETS`.

## See also

- [GROUPING](/sql-reference/functions/grouping) (Utility function to identify which grouping level produced each row)
- [GROUP BY GROUPING SETS](/sql-reference/constructs/group-by-grouping-sets)
- [GROUP BY CUBE](/sql-reference/constructs/group-by-cube)

## Syntax

Copy code

```
SELECT ...
FROM ...
[ ... ]
GROUP BY [ groupItem [ , groupItem [ , ... ] ] , ] ROLLUP ( groupItem [ , groupItem [ , ... ] ] )
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

- As the query is aggregated at higher and higher levels, it shows NULL values
  in more columns of each row. This is appropriate. In the following example,
  for the aggregate at the state level, the `city` column is NULL;
  that’s because the value in the `profit` column does not correspond to one
  city. Similarly, in the final total, which aggregates data from all the
  states and all the cities, the revenue is not from one specific state or one
  specific city, so both the `state` and `city` columns in that row are NULL.
- The query should list the “most significant level” first in the parentheses
  after the ROLLUP. For example, states contain cities, so if you are rolling up
  data across states and cities, the clause should be `GROUP BY ROLLUP (state, city)`

  If you reverse the order of the column names, you get a result that is
  probably not what you want. In the following example, if you reversed the order
  of `city` and `state` in the ROLLUP clause, the result would be incorrect,
  at least in part because both California and Puerto Rico have a city named San Jose (`SJ`),
  and you probably would not want to combine the revenue from the two different San Jose cities,
  except in the final total of all revenue. (An alternative way to avoid combining data from
  different cities with the same name is to create a unique ID for each city and use the ID
  rather than the name in the query.)
- The [GROUPING](/sql-reference/functions/grouping) utility function can help distinguish
  between NULL values that result from the rollup aggregation versus actual NULL values in the data.
  GROUPING returns `0` for a row grouped on a specified column and `1` for a row where the column
  shows NULL because of aggregation.

## Examples

Start by creating and loading a table with information about sales at
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

Run a rollup query that shows profit by city, state, and total across all
states. The query produces three “levels” of aggregation:

- Each city.
- Each state.
- All revenue combined across all states.

The query uses `ORDER BY state, city NULLS LAST` to ensure that each state’s rollup comes immediately after all of
the cities in that state, and that the final rollup appears at the end of the output.

> Copy code
>
> ```
> SELECT state, city, SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit 
>  FROM products AS p, sales AS s
>  WHERE s.product_ID = p.product_ID
>  GROUP BY ROLLUP (state, city)
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
> | NULL  | NULL    |    375 |
> +-------+---------+--------+
> ```

Some rollup rows contain NULL values. For example, the last row in the table contains a NULL value for the city and
a NULL value for the state because the data is for all cities and states, not a specific city and state.
