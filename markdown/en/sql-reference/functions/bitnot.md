Categories:
:   [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# BITNOT

Returns the bitwise negation of a numeric or binary expression.

Aliases:
:   BIT\_NOT

## Syntax

Copy code

```
BITNOT( <expr> )
```

## Arguments

`expr`
:   This expression must evaluate to an INTEGER value, a BINARY value, or a value of a data type
    that can be cast to an INTEGER value.

## Returns

Returns an INTEGER value, a BINARY value, or NULL:

- When the input expression contains an INTEGER value, returns an INTEGER value that represents the bitwise
  negation of the input expression.
- When the input expression contains a BINARY value, returns a BINARY value that represents the bitwise
  negation of the input expression.
- If the input value is NULL, returns NULL.

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

### Using BITNOT with INTEGER argument values

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
       BITNOT(bit1), 
       BITNOT(bit2)
  FROM bits
  ORDER BY bit1;
```

```
+------+-------+--------------+--------------+
| BIT1 |  BIT2 | BITNOT(BIT1) | BITNOT(BIT2) |
|------+-------+--------------+--------------|
|    0 | 65504 |           -1 |       -65505 |
|    1 |     1 |           -2 |           -2 |
|    2 |     4 |           -3 |           -5 |
|    4 |     2 |           -5 |           -3 |
|   16 |    24 |          -17 |          -25 |
| NULL |  NULL |         NULL |         NULL |
+------+-------+--------------+--------------+
```

### Using BITNOT with BINARY argument values

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
       bit2,
       bit3,
       BITNOT(bit1),
       BITNOT(bit2),
       BITNOT(bit3)
  FROM bits;
```

```
+------+------+----------+--------------+--------------+--------------+
| BIT1 | BIT2 | BIT3     | BITNOT(BIT1) | BITNOT(BIT2) | BITNOT(BIT3) |
|------+------+----------+--------------+--------------+--------------|
| 1010 | 0101 | 11001010 | EFEF         | FEFE         | EEFFEFEF     |
| 1100 | 0011 | 01011010 | EEFF         | FFEE         | FEFEEFEF     |
| BCBC | EEFF | ABCDABCD | 4343         | 1100         | 54325432     |
| NULL | NULL | NULL     | NULL         | NULL         | NULL         |
+------+------+----------+--------------+--------------+--------------+
```
