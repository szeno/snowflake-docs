Categories:
:   [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# BITOR

Returns the bitwise OR of two numeric or binary expressions.

Aliases:
:   BIT\_OR

See also:
:   [BITOR\_AGG](/sql-reference/functions/bitor_agg)

## Syntax

Copy code

```
BITOR( <expr1> , <expr2> [ , '<padside>' ] )
```

## Arguments

`expr1`
:   This expression must evaluate to an INTEGER value, a BINARY value, or a value of a data type
    that can be cast to an INTEGER value.

`expr2`
:   This expression must evaluate to an INTEGER value, a BINARY value, or a value of a data type
    that can be cast to an INTEGER value.

`'padside'`
:   When two BINARY argument values are not the same length, specifies which side to pad the value
    with the shorter length. Specify one of the following case-insensitive values:

    - LEFT - Pad the value on the left.
    - RIGHT - Pad the value on the right.

    The shorter value is padded with zeros so that it equals the length of the larger value.

    This argument is valid only when BINARY expressions are specified.

    If the length of two BINARY values are different, this argument is required.

## Returns

Returns an INTEGER value, a BINARY value, or NULL:

- When the input expressions contain INTEGER values, returns an INTEGER value that represents the bitwise OR
  of the input expressions.
- When the input expressions contain BINARY values, returns a BINARY value that represents the bitwise OR
  of the input expressions.
- If either input value is NULL, returns NULL.

## Usage notes

- Both input expressions must evaluate to a value of the same data type, either INTEGER
  or BINARY.
- If the data type of either argument is [numeric](/sql-reference/data-types-numeric)
  but not INTEGER (e.g. FLOAT, DECIMAL, etc.), then the argument is cast to an INTEGER value.
- If the data type of either argument is a string (e.g. VARCHAR), then the
  argument is cast to an INTEGER value if possible. For example, the string `12.3`
  is cast to `12`. If the value cannot be cast to an INTEGER value, then the
  value is treated as NULL.
- The function does not implicitly cast arguments to BINARY values.

## Examples

The following sections contain examples for INTEGER argument values and BINARY argument values.

# Using BITAND, BITOR, and BITXOR with INTEGER argument values

Create a simple table and insert the data:

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
       BITAND(bit1, bit2),
       BITOR(bit1, bit2),
       BITXOR(bit1, BIT2)
  FROM bits
  ORDER BY bit1;
```

```
+------+-------+--------------------+-------------------+--------------------+
| BIT1 |  BIT2 | BITAND(BIT1, BIT2) | BITOR(BIT1, BIT2) | BITXOR(BIT1, BIT2) |
|------+-------+--------------------+-------------------+--------------------|
|    0 | 65504 |                  0 |             65504 |              65504 |
|    1 |     1 |                  1 |                 1 |                  0 |
|    2 |     4 |                  0 |                 6 |                  6 |
|    4 |     2 |                  0 |                 6 |                  6 |
|   16 |    24 |                 16 |                24 |                  8 |
| NULL |  NULL |               NULL |              NULL |               NULL |
+------+-------+--------------------+-------------------+--------------------+
```

## Using BITAND, BITOR, and BITXOR with BINARY argument values

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

Run a query on BINARY columns of the same length:

Copy code

```
SELECT bit1,
       bit2,
       BITAND(bit1, bit2),
       BITOR(bit1, bit2),
       BITXOR(bit1, bit2)
  FROM bits;
```

```
+------+------+--------------------+-------------------+--------------------+
| BIT1 | BIT2 | BITAND(BIT1, BIT2) | BITOR(BIT1, BIT2) | BITXOR(BIT1, BIT2) |
|------+------+--------------------+-------------------+--------------------|
| 1010 | 0101 | 0000               | 1111              | 1111               |
| 1100 | 0011 | 0000               | 1111              | 1111               |
| BCBC | EEFF | ACBC               | FEFF              | 5243               |
| NULL | NULL | NULL               | NULL              | NULL               |
+------+------+--------------------+-------------------+--------------------+
```

If you try to run a query on BINARY columns of different lengths without specifying the `'padside'`
argument, an error is returned:

Copy code

```
SELECT bit1,
       bit3,
       BITAND(bit1, bit3),
       BITOR(bit1, bit3),
       BITXOR(bit1, bit3)
  FROM bits;
```

```
100544 (22026): The lengths of two variable-sized fields do not match: first length 2, second length 4
```

Run a query on BINARY columns of different lengths, and pad the smaller argument value on the left:

Copy code

```
SELECT bit1,
       bit3,
       BITAND(bit1, bit3, 'LEFT'),
       BITOR(bit1, bit3, 'LEFT'),
       BITXOR(bit1, bit3, 'LEFT')
  FROM bits;
```

```
+------+----------+----------------------------+---------------------------+----------------------------+
| BIT1 | BIT3     | BITAND(BIT1, BIT3, 'LEFT') | BITOR(BIT1, BIT3, 'LEFT') | BITXOR(BIT1, BIT3, 'LEFT') |
|------+----------+----------------------------+---------------------------+----------------------------|
| 1010 | 11001010 | 00001010                   | 11001010                  | 11000000                   |
| 1100 | 01011010 | 00001000                   | 01011110                  | 01010110                   |
| BCBC | ABCDABCD | 0000A88C                   | ABCDBFFD                  | ABCD1771                   |
| NULL | NULL     | NULL                       | NULL                      | NULL                       |
+------+----------+----------------------------+---------------------------+----------------------------+
```

Run a query on BINARY columns of different lengths, and pad the smaller argument value on the right:

Copy code

```
SELECT bit1,
       bit3,
       BITAND(bit1, bit3, 'RIGHT'),
       BITOR(bit1, bit3, 'RIGHT'),
       BITXOR(bit1, bit3, 'RIGHT')
  FROM bits;
```

```
+------+----------+-----------------------------+----------------------------+-----------------------------+
| BIT1 | BIT3     | BITAND(BIT1, BIT3, 'RIGHT') | BITOR(BIT1, BIT3, 'RIGHT') | BITXOR(BIT1, BIT3, 'RIGHT') |
|------+----------+-----------------------------+----------------------------+-----------------------------|
| 1010 | 11001010 | 10000000                    | 11101010                   | 01101010                    |
| 1100 | 01011010 | 01000000                    | 11011010                   | 10011010                    |
| BCBC | ABCDABCD | A88C0000                    | BFFDABCD                   | 1771ABCD                    |
| NULL | NULL     | NULL                        | NULL                       | NULL                        |
+------+----------+-----------------------------+----------------------------+-----------------------------+
```
