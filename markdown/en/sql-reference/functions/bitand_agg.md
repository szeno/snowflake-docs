Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Bitwise) , [Window functions](/sql-reference/functions-window) (General) , [Bitwise expression functions](/sql-reference/expressions-byte-bit)

# BITAND\_AGG

Returns the bitwise AND value of all non-NULL numeric records in a group.

For each bit position, if all rows have the bit set to 1, then the bit is set to 1 in the result.
If any rows have that bit set to zero, the result is zero.

If all records inside the group are NULL, or if the group is empty, the function returns NULL.

Aliases:
:   BITANDAGG , BIT\_AND\_AGG , BIT\_ANDAGG

See also:
:   [BITOR\_AGG](/sql-reference/functions/bitor_agg) , [BITXOR\_AGG](/sql-reference/functions/bitxor_agg) ,

    [BITAND](/sql-reference/functions/bitand)

## Syntax

**Aggregate function**

Copy code

```
BITAND_AGG( <expr1> )
```

**Window function**

Copy code

```
BITAND_AGG( <expr1> ) OVER ( [ PARTITION BY <expr2> ] )
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
SELECT BITAND_AGG(k),
    BITAND_AGG(d),
    BITAND_AGG(s1)
  FROM bitwise_example;
```

```
+---------------+---------------+----------------+
| BITAND_AGG(K) | BITAND_AGG(D) | BITAND_AGG(S1) |
|---------------+---------------+----------------|
|             8 |             1 |              8 |
+---------------+---------------+----------------+
```

Query the data and use a GROUP BY clause:

Copy code

```
SELECT s2,
    BITAND_AGG(k),
    BITAND_AGG(d)
  FROM bitwise_example
  GROUP BY s2
  ORDER BY 3;
```

```
+------+---------------+---------------+
| S2   | BITAND_AGG(K) | BITAND_AGG(D) |
|------+---------------+---------------|
| one  |            15 |             1 |
| two  |             8 |             3 |
| nine |          NULL |             9 |
| null |             8 |          NULL |
+------+---------------+---------------+
```

If you pass this function strings that can’t be converted to NUMBER values, an error is returned:

Copy code

```
SELECT BITAND_AGG(s2)
  FROM bitwise_example;
```

```
100038 (22018): Numeric value 'one' is not recognized
```
