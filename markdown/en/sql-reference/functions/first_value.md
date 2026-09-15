Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# FIRST\_VALUE

Returns the first value within an ordered group of values.

See also:
:   [LAST\_VALUE](/sql-reference/functions/last_value) , [NTH\_VALUE](/sql-reference/functions/nth_value)

## Syntax

Copy code

```
FIRST_VALUE( <expr> ) [ { IGNORE | RESPECT } NULLS ]
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2>  [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`expr`
:   The expression that determines the return value.

`expr1`
:   The expression by which to partition the rows. You can specify a single expression or a comma-separated list of expressions.
    For example:

    Copy code

    ```
    PARTITION BY column_1, column_2
    ```

`expr2`
:   The expression by which to order the rows. You can specify a single expression or a comma-separated list of expressions.
    For example:

    Copy code

    ```
    ORDER BY column_3, column_4
    ```

`{ IGNORE | RESPECT } NULLS`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    - `IGNORE NULLS` returns the first non-NULL value.
    - `RESPECT NULLS` returns a NULL value if it is the first value in the expression.

    Default: `RESPECT NULLS`

## Usage notes

- This function is a rank-related function, so it must specify a window. A window clause consists of the following subclauses:

> - `PARTITION BY expr1` subclause (optional).
> - `ORDER BY expr2` subclause (required). For details about additional supported ordering options (sort order, ordering
>   of NULL values, and so on), see the documentation for the [ORDER BY](/sql-reference/constructs/order-by) clause, which follows
>   the same rules.
> - `window_frame` subclause (optional).

- The order of rows in a window (and thus the result of the query) is fully deterministic only if the keys in the ORDER BY clause
  make each row unique. Consider the following example:

  Copy code

  ```
  ... OVER (PARTITION BY p ORDER BY o COLLATE 'lower') ...
  ```

  The query result can vary if any partition contains values of column `o` that are identical, or would be identical
  in a case-insensitive comparison.
- The ORDER BY clause inside the OVER clause controls the order of rows only within the window, not the order of rows in the output
  of the entire query. To control output order, use a separate ORDER BY clause at the outermost level of the query.

- The optional `window_frame` specifies the subset of rows within the window for which the function is calculated. If no `window_frame` is specified, the default is the entire window:

  `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`

  Note that this deviates from the ANSI standard, which specifies the following default for window frames:

  `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Examples

This example shows a query that uses the FIRST\_VALUE function to find the cheapest menu item
in each category. The query contains two ORDER BY clauses: one to control the order of rows
in each partition, and one to sort the output of the full query. To create and load the table that is used in this example, see [Create and load the menu\_items table](/sql-reference/functions/stddev#label-create-and-load-menu-items-table).

Copy code

```
SELECT menu_category, menu_item_name, menu_price_usd,
       FIRST_VALUE(menu_item_name) OVER (PARTITION BY menu_category ORDER BY menu_price_usd) AS cheapest_item
  FROM menu_items
  WHERE menu_category IN ('Beverage', 'Dessert', 'Snack')
  ORDER BY menu_category, menu_price_usd
  LIMIT 12;
```

```
+---------------+--------------------+----------------+---------------+
| MENU_CATEGORY | MENU_ITEM_NAME     | MENU_PRICE_USD | CHEAPEST_ITEM |
|---------------+--------------------+----------------+---------------|
| Beverage      | Bottled Water      |           2.00 | Bottled Water |
| Beverage      | Iced Tea           |           3.00 | Bottled Water |
| Beverage      | Bottled Soda       |           3.00 | Bottled Water |
| Beverage      | Lemonade           |           3.50 | Bottled Water |
| Dessert       | Popsicle           |           3.00 | Popsicle      |
| Dessert       | Ice Cream Sandwich |           4.00 | Popsicle      |
| Dessert       | Mango Sticky Rice  |           5.00 | Popsicle      |
| Dessert       | Sugar Cone         |           6.00 | Popsicle      |
| Dessert       | Waffle Cone        |           6.00 | Popsicle      |
| Dessert       | Two Scoop Bowl     |           7.00 | Popsicle      |
| Snack         | Spring Mix Salad   |           6.00 | Fried Pickles |
| Snack         | Fried Pickles      |           6.00 | Fried Pickles |
+---------------+--------------------+----------------+---------------+
```

The following example also uses the `menu_items` table to compare three related functions: FIRST\_VALUE,
[NTH\_VALUE](/sql-reference/functions/nth_value), and [LAST\_VALUE](/sql-reference/functions/last_value):

- The query creates a sliding window frame that is three rows wide, which contains:

  - The row that precedes the current row.
  - The current row.
  - The row that follows the current row.
- The `2` in the call `NTH_VALUE(menu_price_usd, 2)` specifies the second row in the window frame
  (which, in this case, is also the current row).
- When the current row is the very first row in the window frame, there is no preceding row to reference, so
  FIRST\_VALUE returns a NULL for that row.
- Frame boundaries sometimes extend beyond the rows in a partition, but non-existent rows are not included in window function
  calculations. For example, when the current row is the very first row in the partition and the window frame is
  `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`, there is no preceding row to reference, so the FIRST\_VALUE function returns the
  value of the first row in the partition.
- The results never match for all three functions, given the data in the table. These functions select the *first*,
  *last*, or *nth* value for each row in the frame, and the selection of values applies separately to each partition.

Copy code

```
SELECT menu_category, menu_item_name, menu_price_usd,
       FIRST_VALUE(menu_price_usd) OVER (PARTITION BY menu_category ORDER BY menu_price_usd
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS first_val,
       NTH_VALUE(menu_price_usd, 2) OVER (PARTITION BY menu_category ORDER BY menu_price_usd
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS nth_val,
       LAST_VALUE(menu_price_usd) OVER (PARTITION BY menu_category ORDER BY menu_price_usd
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS last_val
  FROM menu_items
  WHERE menu_category = 'Dessert'
  ORDER BY menu_price_usd;
```

```
+---------------+--------------------+----------------+-----------+---------+----------+
| MENU_CATEGORY | MENU_ITEM_NAME     | MENU_PRICE_USD | FIRST_VAL | NTH_VAL | LAST_VAL |
|---------------+--------------------+----------------+-----------+---------+----------|
| Dessert       | Popsicle           |           3.00 |      3.00 |    4.00 |     4.00 |
| Dessert       | Ice Cream Sandwich |           4.00 |      3.00 |    4.00 |     5.00 |
| Dessert       | Mango Sticky Rice  |           5.00 |      4.00 |    5.00 |     6.00 |
| Dessert       | Sugar Cone         |           6.00 |      6.00 |    6.00 |     7.00 |
| Dessert       | Waffle Cone        |           6.00 |      5.00 |    6.00 |     6.00 |
| Dessert       | Two Scoop Bowl     |           7.00 |      6.00 |    7.00 |     7.00 |
+---------------+--------------------+----------------+-----------+---------+----------+
```

This example demonstrates the difference between IGNORE NULLS and RESPECT NULLS. The sample
data includes rows where the cost value is NULL. With the default RESPECT NULLS behavior, if
the first row in the ordered partition has a NULL value, FIRST\_VALUE returns NULL. With IGNORE
NULLS, FIRST\_VALUE skips NULL values and returns the first non-NULL value.

Copy code

```
SELECT item_name, item_cost, item_price,
       FIRST_VALUE(item_cost) RESPECT NULLS
         OVER (ORDER BY item_price) AS first_cost_respect,
       FIRST_VALUE(item_cost) IGNORE NULLS
         OVER (ORDER BY item_price) AS first_cost_ignore
  FROM VALUES
    ('Pretzel', NULL, 3.00),
    ('Corn Dog', NULL, 4.00),
    ('Hot Dog', 1.50, 5.00),
    ('Sandwich', 2.50, 6.00)
  AS menu(item_name, item_cost, item_price)
  ORDER BY item_price;
```

```
+-----------+-----------+------------+--------------------+-------------------+
| ITEM_NAME | ITEM_COST | ITEM_PRICE | FIRST_COST_RESPECT | FIRST_COST_IGNORE |
|-----------+-----------+------------+--------------------+-------------------|
| Pretzel   |      NULL |       3.00 |               NULL |              1.50 |
| Corn Dog  |      NULL |       4.00 |               NULL |              1.50 |
| Hot Dog   |      1.50 |       5.00 |               NULL |              1.50 |
| Sandwich  |      2.50 |       6.00 |               NULL |              1.50 |
+-----------+-----------+------------+--------------------+-------------------+
```
