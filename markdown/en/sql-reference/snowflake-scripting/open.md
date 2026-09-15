# OPEN (Snowflake Scripting)

Opens a cursor.

For more information on cursors, see [Working with cursors](/developer-guide/snowflake-scripting/cursors).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [DECLARE](/sql-reference/snowflake-scripting/declare), [FETCH](/sql-reference/snowflake-scripting/fetch), [CLOSE](/sql-reference/snowflake-scripting/close)

## Syntax

Copy code

```
OPEN <cursor_name> [ USING (bind_variable_1 [, bind_variable_2 ...] ) ] ;
```

Where:

> `cursor_name`
> :   The name of the cursor.
>
> `bind_variable`
> :   A bind variable holds a value to be used in the cursor’s query definition (e.g. in a `WHERE` clause).
>
>     An example of binding is included in the examples later in this section.

## Usage notes

- The result set of a query can be thought of as a set of rows. Internally, opening a cursor executes the query,
  reads the rows, and positions an internal pointer to the first of the rows.
- As with any SQL query, if the query definition does not contain an
  [ORDER BY](/sql-reference/constructs/order-by) at the outermost level, then the result
  set has no defined order. When the result set for the cursor is created, its order persists until the cursor is
  closed. However, re-declaring or re-opening the cursor might produce the rows in a different order.
- Similarly, if a cursor is closed, and then the underlying table(s) are updated before it is re-opened, the
  result set can also change.

## Examples

Copy code

```
DECLARE
    c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
    OPEN c1;
    ...
```

The following shows how to bind a variable when opening a [cursor](/developer-guide/snowflake-scripting/cursors):

Copy code

```
DECLARE
    price_to_search_for FLOAT;
    price_count INTEGER;
    c2 CURSOR FOR SELECT COUNT(*) FROM invoices WHERE price = ?;
BEGIN
    price_to_search_for := 11.11;
    OPEN c2 USING (price_to_search_for);
```

For a more complete example of using a cursor, see
[the introductory cursor example](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-example).
