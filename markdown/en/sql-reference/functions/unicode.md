Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# UNICODE

Returns the Unicode code point for the first Unicode character in a string. If the string is empty, a value of `0` is returned.

See also:

> [ASCII](/sql-reference/functions/ascii) , [CHAR](/sql-reference/functions/chr)

## Syntax

Copy code

```
UNICODE( <input> )
```

## Arguments

`input`
:   The string for which the Unicode code point for the first character in the string is returned.

## Examples

This example demonstrates the function behavior for single ASCII and Unicode characters, as well as special cases, such as multi-character strings, empty strings,
and `NULL` values. It also demonstrates how the UNICODE and [CHAR](/sql-reference/functions/chr) functions interact:

Copy code

```
SELECT column1, UNICODE(column1), CHAR(UNICODE(column1))
FROM values('a'), ('\u2744'), ('cde'), (''), (null);

+---------+------------------+------------------------+
| COLUMN1 | UNICODE(COLUMN1) | CHAR(UNICODE(COLUMN1)) |
|---------+------------------+------------------------|
| a       |               97 | a                      |
| ❄       |            10052 | ❄                      |
| cde     |               99 | c                      |
|         |                0 |                        |
| NULL    |             NULL | NULL                   |
+---------+------------------+------------------------+
```
