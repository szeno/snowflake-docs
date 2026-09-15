Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_UUID

Converts the input expression to a [UUID](/sql-reference/data-types-uuid) value.

See also:

- [TRY\_TO\_UUID](/sql-reference/functions/try_to_uuid)

## Syntax

Copy code

```
TO_UUID( <string_expr> )
```

## Arguments

`string_expr`
:   A string expression in UUID format.

## Returns

The return type is [UUID](/sql-reference/data-types-uuid).

For NULL input, the output is NULL.

## Examples

The following example converts a string to a UUID value:

Copy code

```
SELECT TO_UUID('c73d9175-0a1d-48c6-8d30-df165461328b');
```

```
+-------------------------------------------------+
| TO_UUID('C73D9175-0A1D-48C6-8D30-DF165461328B') |
|-------------------------------------------------|
| c73d9175-0a1d-48c6-8d30-df165461328b            |
+-------------------------------------------------+
```
