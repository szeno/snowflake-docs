Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_UUID

A special version of [TO\_UUID](/sql-reference/functions/to_uuid) that performs the same operation
— that is, converts an input expression to a [UUID](/sql-reference/data-types-uuid) value —
but with error handling support. If the conversion can’t be performed, it returns a NULL value
instead of raising an error.

For more information, see the following topics:

- [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions)
- [TO\_UUID](/sql-reference/functions/to_uuid)

## Syntax

Copy code

```
TRY_TO_UUID( <string_expr> )
```

## Arguments

`string_expr`
:   A string expression in UUID format.

## Returns

Returns a value of type [UUID](/sql-reference/data-types-uuid) or NULL when
TO\_UUID would return an error.

## Examples

The following example returns NULL because the input string isn’t a UUID:

Copy code

```
SELECT TRY_TO_UUID('not a uuid');
```

```
+--------------------------------------+
| TRY_TO_UUID('NOT A UUID')            |
|--------------------------------------|
| NULL                                 |
+--------------------------------------+
```

For examples that convert an input expression to a UUID value, see [TO\_UUID](/sql-reference/functions/to_uuid).
