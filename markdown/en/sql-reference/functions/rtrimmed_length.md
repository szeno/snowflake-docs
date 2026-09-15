Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# RTRIMMED\_LENGTH

Returns the length of its argument, minus trailing whitespace, but including leading whitespace.

## Syntax

Copy code

```
RTRIMMED_LENGTH( <string_expr> )
```

## Usage notes

- Equivalent to `{fn LENGTH(str)}` in ODBC.
- Not equivalent to [LENGTH, LEN](/sql-reference/functions/length) in Snowflake.

## Examples

Copy code

```
SELECT RTRIMMED_LENGTH(' ABCD ');

+---------------------------+
| RTRIMMED_LENGTH(' ABCD ') |
|---------------------------|
|                         5 |
+---------------------------+
```
