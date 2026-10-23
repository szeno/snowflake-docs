Categories:
:   [Conversion functions](/sql-reference/functions-conversion), [IPADDRESS functions](/sql-reference/functions-ipaddress)

# TRY\_TO\_IPADDRESS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A special version of [TO\_IPADDRESS](/sql-reference/functions/to_ipaddress) that performs the same operation
(converts an input expression to an [IPADDRESS](/sql-reference/data-types-ipaddress) value)
but with error-handling support. If the conversion can’t be performed, it returns a NULL value
instead of raising an error.

For more information, see the following topics:

- [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions)
- [TO\_IPADDRESS](/sql-reference/functions/to_ipaddress)

## Syntax

Copy code

```
TRY_TO_IPADDRESS( <string_expr> )
```

## Arguments

`string_expr`
:   A string expression that contains a valid IPv4 or IPv6 address.

## Returns

Returns a value of type [IPADDRESS](/sql-reference/data-types-ipaddress) or `NULL` when
`TO_IPADDRESS` would return an error.

## Examples

The following example returns `NULL` because the input string isn’t an IP address:

Copy code

```
SELECT TRY_TO_IPADDRESS('not an ip');
```

```
+-------------------------------+
| TRY_TO_IPADDRESS('NOT AN IP') |
|-------------------------------|
| NULL                          |
+-------------------------------+
```

For examples that convert an input expression to an IPADDRESS value, see [TO\_IPADDRESS](/sql-reference/functions/to_ipaddress).
