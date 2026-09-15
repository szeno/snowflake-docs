Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# STARTSWITH

Returns true if `expr1` starts with `expr2`. Both expressions must be text or binary expressions.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

## Syntax

Copy code

```
STARTSWITH( <expr1> , <expr2> )
```

## Returns

Returns a BOOLEAN. The value is TRUE if `expr1` starts with `expr2`. Returns NULL if either
input expression is NULL. Otherwise, returns FALSE.

## Collation details

The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.

This function does not support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

## Examples

Copy code

```
select * from strings;

---------+
    S    |
---------+
 coffee  |
 ice tea |
 latte   |
 tea     |
 [NULL]  |
---------+

select * from strings where startswith(s, 'te');

-----+
  S  |
-----+
 tea |
-----+
```
