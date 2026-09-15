Categories:
:   [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# GETBIT

Given an INTEGER value, returns the value of a bit at a specified position.

## Syntax

Copy code

```
GETBIT( <integer_expr>, <bit_position> )
```

## Arguments

`integer_expr`
:   This expression must evaluate to a data type that can be cast to an INTEGER value.

`bit_position`
:   The position of the bit (starting from 0 for the least significant bit up to 127 for the most significant bit) for which
    to retrieve the value.

## Returns

The function returns the value of the bit (0 or 1) at the specified position.

## Examples

The following example returns the values of the bits at positions 100, 3, 2, 1, and 0 for an INTEGER value.

Copy code

```
SELECT GETBIT(11, 100), GETBIT(11, 3), GETBIT(11, 2), GETBIT(11, 1), GETBIT(11, 0);
```

```
+-----------------+---------------+---------------+---------------+---------------+
| GETBIT(11, 100) | GETBIT(11, 3) | GETBIT(11, 2) | GETBIT(11, 1) | GETBIT(11, 0) |
|-----------------+---------------+---------------+---------------+---------------|
|               0 |             1 |             0 |             1 |             1 |
+-----------------+---------------+---------------+---------------+---------------+
```
