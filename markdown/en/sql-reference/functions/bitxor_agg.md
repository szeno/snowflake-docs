Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Bitwise) , [Window functions](/sql-reference/functions-window) (General) , [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# BITXOR\_AGG

Returns the bitwise XOR value of all non-NULL numeric records in a group.

In each bit position, if an even number of rows have that bit set to 1, then the function returns 0 for that bit, and
if an odd number of rows have that bit set to 1, then the function returns 1 for that bit.

If all records inside the group are NULL, or if the group is empty, the function returns NULL.

Aliases:
:   BITXORAGG , BIT\_XOR\_AGG, BIT\_XORAGG

See also:
:   [BITAND\_AGG](/sql-reference/functions/bitand_agg) , [BITOR\_AGG](/sql-reference/functions/bitor_agg)

    [BITXOR](/sql-reference/functions/bitxor)

## Syntax

**Aggregate function**

Copy code

```
BITXOR_AGG( [ DISTINCT ] <expr1> )
```

**Window function**

Copy code

```
BITXOR_AGG( [ DISTINCT ] <expr1> ) OVER ( [ PARTITION BY <expr2> ] )
```

## Arguments

`expr1`
:   This expression must evaluate to a [numeric](/sql-reference/data-types-numeric) value or a value
    of a data type that can be cast to a numeric value.

`expr2`
:   This expression is used to group the rows in partitions.

## Returns

The data type of the returned value is `NUMBER(38, 0)`.

## Usage notes

- Numeric values are aggregated to the nearest INTEGER data type. Decimal and floating-point values are rounded to the
  nearest integer before aggregation.
- Aggregating a character/text column (data type VARCHAR, CHAR, STRING, etc.) implicitly casts the input values
  to FLOAT, then rounds the values to the nearest integer. If the cast is not possible, the value is treated as NULL.
- The DISTINCT keyword can be specified for these functions, but it does not have any effect.
- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

Create the table and load the data:

Copy code

```
CREATE OR REPLACE TABLE bitwise_example
  (k INT, d DECIMAL(10,5), s1 VARCHAR(10), s2 VARCHAR(10));

INSERT INTO bitwise_example VALUES
  (15, 1.1, '12', 'one'),
  (26, 2.9, '10', 'two'),
  (12, 7.1, '7.9', 'two'),
  (14, NULL, NULL, 'null'),
  (8, NULL, NULL, 'null'),
  (NULL, 9.1, '14', 'nine');
```

Display the data:

Copy code

```
SELECT k AS k_col, d AS d_col, s1, s2
  FROM bitwise_example
  ORDER BY k_col;
```

```
+-------+---------+------+------+
| K_COL |   D_COL | S1   | S2   |
|-------+---------+------+------|
|     8 |    NULL | NULL | null |
|    12 | 7.10000 | 7.9  | two  |
|    14 |    NULL | NULL | null |
|    15 | 1.10000 | 12   | one  |
|    26 | 2.90000 | 10   | two  |
|  NULL | 9.10000 | 14   | nine |
+-------+---------+------+------+
```

Query the data:

Copy code

```
SELECT BITXOR_AGG(k),
    BITXOR_AGG(d),
    BITXOR_AGG(s1)
  FROM bitwise_example;
```

```
+---------------+---------------+----------------+
| BITXOR_AGG(K) | BITXOR_AGG(D) | BITXOR_AGG(S1) |
|---------------+---------------+----------------|
|            31 |            12 |              0 |
+---------------+---------------+----------------+
```

Query the data and use a GROUP BY clause:

Copy code

```
SELECT s2,
    BITXOR_AGG(k),
    BITXOR_AGG(d)
  FROM bitwise_example
  GROUP BY s2
  ORDER BY 3;
```

```
+------+---------------+---------------+
| S2   | BITXOR_AGG(K) | BITXOR_AGG(D) |
|------+---------------+---------------|
| one  |            15 |             1 |
| two  |            22 |             4 |
| nine |          NULL |             9 |
| null |             6 |          NULL |
+------+---------------+---------------+
```

If you pass this function strings that can’t be converted to NUMBER values, an error is returned:

Copy code

```
SELECT BITXOR_AGG(s2)
  FROM bitwise_example;
```

```
100038 (22018): Numeric value 'one' is not recognized
```
