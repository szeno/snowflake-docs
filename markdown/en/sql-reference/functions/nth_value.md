Categories:
:   [Window function syntax and usage](/sql-reference/functions-window-syntax) (Ranking)

# NTH\_VALUE

Returns the nth value (up to 1000) within an ordered group of values.

See also:
:   [FIRST\_VALUE](/sql-reference/functions/first_value) , [LAST\_VALUE](/sql-reference/functions/last_value)

## Syntax

Copy code

```
NTH_VALUE( <expr> , <n> ) [ FROM { FIRST | LAST } ] [ { IGNORE | RESPECT } NULLS ]
  OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`n`
:   This specifies which value of N to use when looking for the Nth value.

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

`FROM { FIRST | LAST }`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    - `FROM FIRST` starts from the beginning of the ordered list and moves forward.
    - `FROM LAST` starts from the end of the ordered list and moves backward.

    Default: `FROM FIRST`

`{ IGNORE | RESPECT } NULLS`
:   Whether to ignore or respect NULL values when an `expr` contains NULL values:

    - `IGNORE NULLS` skips NULL values in the expression.
    - `RESPECT NULLS` returns a NULL value if it is the nth value in the expression.

    Default: `RESPECT NULLS`

## Usage notes

- Input value `n` can’t be greater than 1000.

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

- The optional `window_frame` (cumulative or sliding) specifies the subset of rows within the window for which the function
  is calculated. If no `window_frame` is specified, the default is the entire window:

  `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`

  Note that this deviates from the ANSI standard, which specifies the following default for window frames:

  `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Examples

Copy code

```
SELECT column1,
       column2,
       NTH_VALUE(column2, 2) OVER (PARTITION BY column1 ORDER BY column2) AS column2_2nd
  FROM VALUES
    (1, 10), (1, 11), (1, 12),
    (2, 20), (2, 21), (2, 22);
```

```
+---------+---------+-------------+
| COLUMN1 | COLUMN2 | COLUMN2_2ND |
|---------+---------+-------------|
|       1 |      10 |          11 |
|       1 |      11 |          11 |
|       1 |      12 |          11 |
|       2 |      20 |          21 |
|       2 |      21 |          21 |
|       2 |      22 |          21 |
+---------+---------+-------------+
```

The following example returns the results of three related functions: [FIRST\_VALUE](/sql-reference/functions/first_value),
NTH\_VALUE, and [LAST\_VALUE](/sql-reference/functions/last_value).

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
