Categories:
:   [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# BITSHIFTRIGHT

Shifts the bits for a numeric or binary expression `n` positions to the right.

Aliases:
:   BIT\_SHIFTRIGHT

See also:
:   [BITSHIFTLEFT](/sql-reference/functions/bitshiftleft)

## Syntax

Copy code

```
BITSHIFTRIGHT( <expr1> , <n> )
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

- If the data type of the argument is [numeric](/sql-reference/data-types-numeric)
  but not INTEGER (e.g. FLOAT, DECIMAL, etc.), then the argument is cast to an INTEGER value.
- If the data type of the argument is a string (e.g. VARCHAR), then the
  argument is cast to an INTEGER value if possible. For example, the string `12.3`
  is cast to `12`. If the value cannot be cast to an INTEGER value, then the
  value is treated as NULL.
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

### Using BITSHIFTRIGHT with BINARY argument values

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
       BITSHIFTRIGHT(bit1, 1),
       BITSHIFTRIGHT(bit3, 1),
       BITSHIFTRIGHT(bit1, 8),
       BITSHIFTRIGHT(bit3, 16)
  FROM bits;
```

```
+------+----------+------------------------+------------------------+------------------------+-------------------------+
| BIT1 | BIT3     | BITSHIFTRIGHT(BIT1, 1) | BITSHIFTRIGHT(BIT3, 1) | BITSHIFTRIGHT(BIT1, 8) | BITSHIFTRIGHT(BIT3, 16) |
|------+----------+------------------------+------------------------+------------------------+-------------------------|
| 1010 | 11001010 | 0808                   | 08800808               | 0010                   | 00001100                |
| 1100 | 01011010 | 0880                   | 00808808               | 0011                   | 00000101                |
| BCBC | ABCDABCD | 5E5E                   | 55E6D5E6               | 00BC                   | 0000ABCD                |
| NULL | NULL     | NULL                   | NULL                   | NULL                   | NULL                    |
+------+----------+------------------------+------------------------+------------------------+-------------------------+
```
