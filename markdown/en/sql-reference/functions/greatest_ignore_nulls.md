Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# GREATEST\_IGNORE\_NULLS

Returns the largest non-NULL value from a list of expressions. GREATEST\_IGNORE\_NULLS supports all data types,
including VARIANT.

See also:
:   [GREATEST](/sql-reference/functions/greatest)

## Syntax

Copy code

```
GREATEST_IGNORE_NULLS( <expr1> [ , <expr2> ... ] )
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

If all arguments are NULL, returns NULL.

# Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The comparisons follow the collation based on the input arguments’ collations and precedences.
- The collation of the result of the function is the highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Examples

Create a table and insert some values:

Copy code

```
CREATE TABLE test_greatest_ignore_nulls (
  col_1 INTEGER,
  col_2 INTEGER,
  col_3 INTEGER,
  col_4 FLOAT);

INSERT INTO test_greatest_ignore_nulls (col_1, col_2, col_3, col_4) VALUES
  (1, 2,    3,  4.25),
  (2, 4,   -1,  NULL),
  (3, 6, NULL,  -2.75);
```

Run a SELECT statement that returns the greatest non-null value in each row of the table:

Copy code

```
SELECT col_1,
       col_2,
       col_3,
       col_4,
       GREATEST_IGNORE_NULLS(col_1, col_2, col_3, col_4) AS greatest_ignore_nulls
 FROM test_greatest_ignore_nulls
 ORDER BY col_1;
```

```
+-------+-------+-------+-------+-----------------------+
| COL_1 | COL_2 | COL_3 | COL_4 | GREATEST_IGNORE_NULLS |
|-------+-------+-------+-------+-----------------------|
|     1 |     2 |     3 |  4.25 |                  4.25 |
|     2 |     4 |    -1 |  NULL |                  4    |
|     3 |     6 |  NULL | -2.75 |                  6    |
+-------+-------+-------+-------+-----------------------+
```
