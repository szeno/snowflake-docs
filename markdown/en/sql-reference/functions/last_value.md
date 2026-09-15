Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# LAST\_VALUE

Returns the last value within an ordered group of values.

See also:
:   [FIRST\_VALUE](/sql-reference/functions/first_value) , [NTH\_VALUE](/sql-reference/functions/nth_value)

## Syntax

Copy code

```
LAST_VALUE( <expr> ) [ { IGNORE | RESPECT } NULLS ]
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] )
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

    - `IGNORE NULLS` returns the last non-NULL value.
    - `RESPECT NULLS` returns a NULL value if it is the last value in the expression.

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

- The optional `window_frame` specifies the subset of rows within the window for which the function is calculated.
  If no window frame is specified, the default frame is the entire window:

  `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`

  This behavior *differs* from the ANSI standard, which specifies the following default for window frames:

  `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Examples

The first example returns LAST\_VALUE results for `column2` partitioned by `column1`:

Copy code

```
SELECT
    column1,
    column2,
    LAST_VALUE(column2) OVER (PARTITION BY column1 ORDER BY column2) AS column2_last
  FROM VALUES
    (1, 10), (1, 11), (1, 12),
    (2, 20), (2, 21), (2, 22);
```

```
+---------+---------+--------------+
| COLUMN1 | COLUMN2 | COLUMN2_LAST |
|---------+---------+--------------|
|       1 |      10 |           12 |
|       1 |      11 |           12 |
|       1 |      12 |           12 |
|       2 |      20 |           22 |
|       2 |      21 |           22 |
|       2 |      22 |           22 |
+---------+---------+--------------+
```

The following example returns the results of three related functions: [FIRST\_VALUE](/sql-reference/functions/first_value),
[NTH\_VALUE](/sql-reference/functions/nth_value), and LAST\_VALUE.

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
