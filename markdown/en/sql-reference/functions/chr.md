Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# CHR , CHAR

Converts a Unicode code point (including 7-bit ASCII) into the character that matches the input Unicode. If an invalid code point is specified, an error is returned.

CHAR is an alias for CHR.

See also:
:   [ASCII](/sql-reference/functions/ascii) , [UNICODE](/sql-reference/functions/unicode)

## Syntax

Copy code

```
CHR( <input> )
```

## Arguments

`input`
:   The Unicode code point for which the character is returned.

## Returns

The data type of the returned value is VARCHAR.

## Examples

This example demonstrates the function behavior for some valid Unicode code points:

> Copy code
>
> ```
> SELECT column1, CHR(column1)
> FROM (VALUES(83), (33), (169), (8364), (0), (null));
> ```

This shows the output for the preceding query:

> Copy code
>
> ```
> +---------+--------------+
> | COLUMN1 | CHR(COLUMN1) |
> |---------+--------------|
> |      83 | S            |
> |      33 | !            |
> |     169 | ©            |
> |    8364 | €            |
> |       0 |              |
> |    NULL | NULL         |
> +---------+--------------+
> ```

This example demonstrates the function behavior for an invalid Unicode code point:

> Copy code
>
> ```
> SELECT column1, CHR(column1)
> FROM (VALUES(-1));
> ```

This shows the output for the preceding query:

> Copy code
>
> ```
> FAILURE: Invalid character code -1 in the CHR input
> ```

This example demonstrates the function behavior for another invalid Unicode code point:

> Copy code
>
> ```
> SELECT column1, CHR(column1)
> FROM (VALUES(999999999999));
> ```

This shows the output for the preceding query:

> Copy code
>
> ```
> FAILURE: Invalid character code 999999999999 in the CHR input
> ```
