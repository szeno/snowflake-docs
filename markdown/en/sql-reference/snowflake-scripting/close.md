# CLOSE (Snowflake Scripting)

Closes the specified cursor.

For more information on cursors, see [Working with cursors](/developer-guide/snowflake-scripting/cursors).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [DECLARE](/sql-reference/snowflake-scripting/declare), [OPEN](/sql-reference/snowflake-scripting/open), [FETCH](/sql-reference/snowflake-scripting/fetch)

## Syntax

Copy code

```
CLOSE <cursor_name> ;
```

Where:

> `cursor_name`
> :   The name of the cursor.

## Usage notes

- After a cursor is closed, the cursor’s current row pointer is invalid. Re-opening the cursor causes the cursor to start from
  the beginning of the new result set.

## Examples

Copy code

```
CLOSE my_cursor_name;
```

For a more complete example of using a cursor, see
[the introductory cursor example](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-example).

An example using a loop is included in the [documentation on FOR loops](/sql-reference/snowflake-scripting/for#label-snowscript-for-example).
