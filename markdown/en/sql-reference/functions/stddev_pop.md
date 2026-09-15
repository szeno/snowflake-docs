Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window function syntax and usage](/sql-reference/functions-window-syntax) (General)

# STDDEV\_POP

Returns the population standard deviation (square root of variance) of non-NULL values.

See also [STDDEV](/sql-reference/functions/stddev), which returns the sample standard deviation (square root of variance).

## Syntax

**Aggregate function**

Copy code

```
STDDEV_POP( [ DISTINCT ] <expr1>)
```

**Window function**

Copy code

```
STDDEV_POP( [ DISTINCT ] <expr1> ) OVER (
                                        [ PARTITION BY <expr2> ]
                                        [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                        )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`expr1`
:   An expression that evaluates to a numeric value. This is the expression on which the standard deviation is calculated.

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the optional expression to order by within each partition.

## Returns

The data type of the returned value is DOUBLE.

If all records inside a group are NULL, this function returns NULL.

## Usage notes

- When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast
  cannot be performed, an error is returned.
- When this function is called as a window function and the OVER clause contains an ORDER BY clause:
  - The DISTINCT keyword is prohibited and results in a SQL compilation error.
  - A window frame must be specified. If you do not specify a window frame, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see
    [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Aggregate function examples

The following example calculates the standard deviation for a small population of integers:

> Copy code
>
> ```
> CREATE TABLE t1 (c1 INTEGER);
> INSERT INTO t1 (c1) VALUES
>     (6),
>    (10),
>    (14)
>    ;
> SELECT STDDEV_POP(c1) FROM t1;
> ```
>
> ```
> +----------------+
> | STDDEV_POP(C1) |
> |----------------|
> |    3.265986375 |
> +----------------+
> ```

Note that the functions STDDEV and STDDEV\_SAMP do not return the same result as STDDEV\_POP.

The following example assumes that you have a table named `menu` that lists food items for sale in a cafe.
The following output shows the 6 rows in the table that belong to the `Dessert` category. Other rows also exist
for other categories, such as `Main` and `Beverage`.

> ```
> +---------+--------------------+---------------+-------------------+----------------+
> | MENU_ID | MENU_ITEM_NAME     | ITEM_CATEGORY | COST_OF_GOODS_USD | SALE_PRICE_USD |
> |---------+--------------------+---------------+-------------------+----------------|
> |   10002 | Sugar Cone         | Dessert       |            2.5000 |         6.0000 |
> |   10003 | Waffle Cone        | Dessert       |            2.5000 |         6.0000 |
> |   10004 | Two Scoop Bowl     | Dessert       |            3.0000 |         7.0000 |
> |   10008 | Ice Cream Sandwich | Dessert       |            1.0000 |         4.0000 |
> |   10009 | Mango Sticky Rice  | Dessert       |            1.2500 |         5.0000 |
> |   10010 | Popsicle           | Dessert       |            0.5000 |         3.0000 |
> +---------+--------------------+---------------+-------------------+----------------+
> ```

To find the population standard deviation for the cost of goods sold and the sale price (for the `Dessert` rows
only), run this query:

> Copy code
>
> ```
> SELECT item_category, STDDEV_POP(cost_of_goods_usd) stddev_cogs, STDDEV_POP(sale_price_usd) stddev_price
>   FROM menu
>   WHERE item_category='Dessert'
>   GROUP BY 1;
> ```
>
> ```
> +---------------+--------------+--------------+
> | ITEM_CATEGORY |  STDDEV_COGS | STDDEV_PRICE |
> |---------------+--------------+--------------|
> | Dessert       | 0.9176131477 |  1.343709625 |
> +---------------+--------------+--------------+
> ```

## Window function example

The following example uses the same `menu` table but runs the STDDEV\_POP function as a window function.

The window function partitions rows by the `item_category` column. Therefore, the standard deviation is
calculated once for each item category, and that value is repeated in the result for each row in the group.
In this example, the rows must be grouped by both the item category and the cost of goods sold.
(Note that the 6 `Dessert` rows are now grouped into 5 rows because two rows have the same cost of goods value.)

> Copy code
>
> ```
> SELECT item_category, cost_of_goods_usd, STDDEV_POP(cost_of_goods_usd) OVER(PARTITION BY item_category) stddev_cogs
>   FROM menu
>   GROUP BY 1,2
>   ORDER BY item_category;
> ```
>
> ```
> +---------------+-------------------+--------------+
> | ITEM_CATEGORY | COST_OF_GOODS_USD |  STDDEV_COGS |
> |---------------+-------------------+--------------|
> | Beverage      |            0.5000 | 0.1027402334 |
> | Beverage      |            0.7500 | 0.1027402334 |
> | Beverage      |            0.6500 | 0.1027402334 |
> | Dessert       |            2.5000 | 0.9433981132 |
> | Dessert       |            3.0000 | 0.9433981132 |
> | Dessert       |            1.0000 | 0.9433981132 |
> | Dessert       |            0.5000 | 0.9433981132 |
> | Dessert       |            1.2500 | 0.9433981132 |
> | Main          |            4.5000 | 3.352193642  |
> | Main          |            8.0000 | 3.352193642  |
> | Main          |            2.0000 | 3.352193642  |
> | Main          |            3.5000 | 3.352193642  |
> ...
> ```
