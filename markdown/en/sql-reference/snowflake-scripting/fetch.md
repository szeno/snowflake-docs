# FETCH (Snowflake Scripting)

Uses the specified cursor to fetch one or more rows.

For more information on cursors, see [Working with cursors](/developer-guide/snowflake-scripting/cursors).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [DECLARE](/sql-reference/snowflake-scripting/declare), [OPEN](/sql-reference/snowflake-scripting/open), [CLOSE](/sql-reference/snowflake-scripting/close)

## Syntax

Copy code

```
FETCH <cursor_name> INTO <variable> [, <variable> ... ] ;
```

Where:

> `cursor_name`
> :   The name of the cursor.
>
> `variable`
> :   The name of the variable into which to retrieve the value of one column of the current row.
>
>     You should have one variable for each column defined in the cursor declaration.
>
>     The variable must already have been [declared](/developer-guide/snowflake-scripting/variables#label-snowscript-declare-variable).
>
>     The variable’s data type must be compatible with the value to be fetched.

## Usage notes

- The number of `variable`s should match the number of expressions selected in the `SELECT` clause of
  the cursor declaration.
- If you try to `FETCH` a row after the last row, you get NULL values.
- A RESULTSET or CURSOR does not necessarily cache all the rows of the result set at the time that the query is executed.
  FETCH operations can experience latency.

## Examples

Copy code

```
FETCH my_cursor_name INTO my_variable_name ;
```

For a more complete example of using a cursor, see
[the introductory cursor example](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-example).

An example using a loop is included in the documentation for [FOR loops](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for).
