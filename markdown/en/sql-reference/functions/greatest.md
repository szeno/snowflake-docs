Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# GREATEST

Returns the largest value from a list of expressions. GREATEST supports all data types, including VARIANT.

See also:
:   [GREATEST\_IGNORE\_NULLS](/sql-reference/functions/greatest_ignore_nulls)

## Syntax

Copy code

```
GREATEST( <expr1> [ , <expr2> ... ] )
```

# Arguments

`<exprN>`
:   The arguments must include at least one expression. All the expressions
    should be of the same type or compatible types.

## Returns

The first argument determines the return type:

- If the first type is numeric, then the return type is ‘widened’
  according to the numeric types in the list of all arguments.
- If the first type is not numeric, then all other arguments must be
  convertible to the first type.

If any argument is NULL, returns NULL.

# Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The comparisons follow the collation based on the input arguments’ collations and precedences.
- The collation of the result of the function is the highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Examples

The following examples use the GREATEST function:

Copy code

```
CREATE TABLE test_table_1_greatest (
  col_1 INTEGER, 
  col_2 INTEGER, 
  col_3 INTEGER, 
  col_4 FLOAT);
INSERT INTO test_table_1_greatest (col_1, col_2, col_3, col_4) VALUES
  (1, 2,    3,  4.00),
  (2, 4,   -1, -2.00),
  (3, 6, NULL, 13.45);
```

Copy code

```
SELECT col_1,
       col_2,
       col_3,
       GREATEST(col_1, col_2, col_3) AS greatest
  FROM test_table_1_greatest
  ORDER BY col_1;
```

```
+-------+-------+-------+----------+
| COL_1 | COL_2 | COL_3 | GREATEST |
|-------+-------+-------+----------|
|     1 |     2 |     3 |        3 |
|     2 |     4 |    -1 |        4 |
|     3 |     6 |  NULL |     NULL |
+-------+-------+-------+----------+
```

Copy code

```
SELECT col_1,
       col_4,
       GREATEST(col_1, col_4) AS greatest
  FROM test_table_1_greatest
  ORDER BY col_1;
```

```
+-------+-------+----------+
| COL_1 | COL_4 | GREATEST |
|-------+-------+----------|
|     1 |  4    |     4    |
|     2 | -2    |     2    |
|     3 | 13.45 |    13.45 |
+-------+-------+----------+
```
