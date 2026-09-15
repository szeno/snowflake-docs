Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# OCTET\_LENGTH

Returns the length of a string or binary value in bytes. This will be the same as LENGTH for ASCII strings and greater than
LENGTH for strings using Unicode code points. For binary, this is always the same as LENGTH.

## Syntax

Copy code

```
OCTET_LENGTH(<string_or_binary>)
```

## Arguments

`string_or_binary`
:   The string or binary value for which the length is returned.

## Examples

Copy code

```
SELECT OCTET_LENGTH('abc'), OCTET_LENGTH('\u0392'), OCTET_LENGTH(X'A1B2');

---------------------+------------------------+-----------------------+
 OCTET_LENGTH('ABC') | OCTET_LENGTH('\U0392') | OCTET_LENGTH(X'A1B2') |
---------------------+------------------------+-----------------------+
 3                   | 2                      | 2                     |
---------------------+------------------------+-----------------------+
```
