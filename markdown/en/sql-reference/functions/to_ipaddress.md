Categories:
:   [Conversion functions](/sql-reference/functions-conversion), [IPADDRESS functions](/sql-reference/functions-ipaddress)

# TO\_IPADDRESS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Converts the input expression to an [IPADDRESS](/sql-reference/data-types-ipaddress) value.

See also:

- [TRY\_TO\_IPADDRESS](/sql-reference/functions/try_to_ipaddress)

## Syntax

Copy code

```
TO_IPADDRESS( <string_expr> )
```

## Arguments

`string_expr`
:   A string expression that contains a valid IPv4 or IPv6 address.

## Returns

The return type is [IPADDRESS](/sql-reference/data-types-ipaddress).

For `NULL` input, the output is `NULL`.

If the input isn’t a valid IP address, the function raises an error.

## Usage notes

- For the accepted input formats and the canonical output form, see [Accepted input and canonical output](/sql-reference/data-types-ipaddress#label-ipaddress-type-format).

## Examples

The following example converts a string to an IPADDRESS value:

Copy code

```
SELECT TO_IPADDRESS('192.0.2.1');
```

```
+---------------------------+
| TO_IPADDRESS('192.0.2.1') |
|---------------------------|
| 192.0.2.1                 |
+---------------------------+
```

The following example converts an IPv6 address that contains leading zeros and returns its RFC 5952
canonical form:

Copy code

```
SELECT TO_IPADDRESS('2001:0db8:0000:0000:0000:0000:0000:0001');
```

```
+---------------------------------------------------------+
| TO_IPADDRESS('2001:0DB8:0000:0000:0000:0000:0000:0001') |
|---------------------------------------------------------|
| 2001:db8::1                                             |
+---------------------------------------------------------+
```
