# Bitwise expression functions

This family of functions can be used to perform bitwise operations on numbers or a group of numeric records.

| Function Name | Syntax | Summary Description |
| --- | --- | --- |
| [BITAND](/sql-reference/functions/bitand) | `BITAND(a, b)` | Bitwise AND of two numeric or binary expressions (`a` and `b`). |
| [BITAND\_AGG](/sql-reference/functions/bitand_agg) | `BITAND_AGG(a)` | Bitwise AND value of all non-NULL numeric records in a group `a`. |
| [BITNOT](/sql-reference/functions/bitnot) | `BITNOT(a)` | Bitwise negation of `a` numeric or binary expression. |
| [BITOR](/sql-reference/functions/bitor) | `BITOR(a, b)` | Bitwise OR of two numeric or binary expressions (`a` and `b`). |
| [BITOR\_AGG](/sql-reference/functions/bitor_agg) | `BITOR_AGG(a)` | Bitwise OR value of all non-NULL numeric records in a group `a`. |
| [BITSHIFTLEFT](/sql-reference/functions/bitshiftleft) | `BITSHIFTLEFT(a, n)` | Shift the bits for `a` numeric or binary expression `n` positions to the left. |
| [BITSHIFTRIGHT](/sql-reference/functions/bitshiftright) | `BITSHIFTRIGHT(a, n)` | Shift the bits for `a` numeric or binary expression `n` positions to the right, with sign extension. |
| [BITXOR](/sql-reference/functions/bitxor) | `BITXOR(a, b)` | Bitwise XOR of two numeric or binary expressions (`a` and `b`). |
| [BITXOR\_AGG](/sql-reference/functions/bitxor_agg) | `BITXOR_AGG(a)` | Bitwise XOR value of all non-NULL numeric records in a group `a`. |
| [GETBIT](/sql-reference/functions/getbit) | `GETBIT(a, n)` | Return the bit at position `n` in `a` numeric expression. |

Expand

Show lessSee more
