Categories:
:   [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# BITSHIFTLEFT

Shifts the bits for a numeric or binary expression `n` positions to the left.

Aliases:
:   BIT\_SHIFTLEFT

See also:
:   [BITSHIFTRIGHT](/sql-reference/functions/bitshiftright)

## Syntax

Copy code

```
BITSHIFTLEFT( <expr1> , <n> )
```

## Arguments

`expr1`
:   This expression must evaluate to an INTEGER value, a BINARY value, or a value of a data type
    that can be cast to an INTEGER value.

`n`
:   The number of bits to shift by.

## Returns

Returns an INTEGER value, a BINARY value, or NULL:

- When the input expression contains an INTEGER value, returns a signed 128-bit (16-byte) integer,
  regardless of the size or data type of the input data value.
- When the input expression contains a BINARY value, returns a BINARY value.
- If any argument is NULL, returns NULL.

## Usage notes

- If the data type of any argument is [numeric](/sql-reference/data-types-numeric)
  but not INTEGER (e.g. FLOAT, DECIMAL, etc.), then that argument is cast to an INTEGER value.
- If the data type of any argument is a string (e.g. VARCHAR), then the
  argument is cast to an INTEGER value if possible. For example, the string `12.3`
  is cast to `12`. If the value cannot be cast to an INTEGER value, then the
  value is treated as NULL.
- If a signed INTEGER value is returned, and the value of the high bit changes (from 0 to 1, or from 1 to 0),
  the sign of the result is reversed. For example, `BITSHIFTLEFT(1, 127)` returns a negative number.
- If a signed INTEGER value is returned, bits that are shifted past the end of the 128-bit output value
  are dropped.
- The function does not implicitly cast arguments to BINARY values.

## Examples

The following sections contain examples for INTEGER argument values and BINARY argument values.

### Using BITSHIFTLEFT and BITSHIFTRIGHT with INTEGER argument values

Create a simple table and data:

Copy code

```
CREATE OR REPLACE TABLE bits (ID INTEGER, bit1 INTEGER, bit2 INTEGER);
```

Copy code

```
INSERT INTO bits (ID, bit1, bit2) VALUES 
  (   11,    1,     1),    -- Bits are all the same.
  (   24,    2,     4),    -- Bits are all different.
  (   42,    4,     2),    -- Bits are all different.
  ( 1624,   16,    24),    -- Bits overlap.
  (65504,    0, 65504),    -- Lots of bits (all but the low 6 bits).
  (    0, NULL,  NULL)     -- No bits.
  ;
```

Run the query:

Copy code

```
SELECT bit1, 
       bit2, 
       BITSHIFTLEFT(bit1, 1), 
       BITSHIFTRIGHT(bit2, 1)
  FROM bits
  ORDER BY bit1;
```

```
+------+-------+-----------------------+------------------------+
| BIT1 |  BIT2 | BITSHIFTLEFT(BIT1, 1) | BITSHIFTRIGHT(BIT2, 1) |
|------+-------+-----------------------+------------------------|
|    0 | 65504 |                     0 |                  32752 |
|    1 |     1 |                     2 |                      0 |
|    2 |     4 |                     4 |                      2 |
|    4 |     2 |                     8 |                      1 |
|   16 |    24 |                    32 |                     12 |
| NULL |  NULL |                  NULL |                   NULL |
+------+-------+-----------------------+------------------------+
```

### Using BITSHIFTLEFT with BINARY argument values

Create a simple table and insert the data:

Copy code

```
CREATE OR REPLACE TABLE bits (ID INTEGER, bit1 BINARY(2), bit2 BINARY(2), bit3 BINARY(4));

INSERT INTO bits VALUES
  (1, x'1010', x'0101', x'11001010'),
  (2, x'1100', x'0011', x'01011010'),
  (3, x'BCBC', x'EEFF', x'ABCDABCD'),
  (4, NULL, NULL, NULL);
```

Note

The BINARY values are inserted using the `x'value'` notation, where `value` contains
hexadecimal digits. For more information, see [Binary input and output](/sql-reference/binary-input-output).

Run the query:

Copy code

```
SELECT bit1,
       bit3,
       BITSHIFTLEFT(bit1, 1),
       BITSHIFTLEFT(bit3, 1),
       BITSHIFTLEFT(bit1, 8),
       BITSHIFTLEFT(bit3, 16)
  FROM bits;
```

```
+------+----------+-----------------------+-----------------------+-----------------------+------------------------+
| BIT1 | BIT3     | BITSHIFTLEFT(BIT1, 1) | BITSHIFTLEFT(BIT3, 1) | BITSHIFTLEFT(BIT1, 8) | BITSHIFTLEFT(BIT3, 16) |
|------+----------+-----------------------+-----------------------+-----------------------+------------------------|
| 1010 | 11001010 | 2020                  | 22002020              | 1000                  | 10100000               |
| 1100 | 01011010 | 2200                  | 02022020              | 0000                  | 10100000               |
| BCBC | ABCDABCD | 7978                  | 579B579A              | BC00                  | ABCD0000               |
| NULL | NULL     | NULL                  | NULL                  | NULL                  | NULL                   |
+------+----------+-----------------------+-----------------------+-----------------------+------------------------+
```
