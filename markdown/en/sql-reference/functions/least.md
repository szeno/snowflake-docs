Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# LEAST

Returns the smallest value from a list of expressions. LEAST supports all data types, including VARIANT.

See also:
:   [LEAST\_IGNORE\_NULLS](/sql-reference/functions/least_ignore_nulls)

## Syntax

Copy code

```
LEAST(( <expr1> [ , <expr2> ... ] )
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

The following examples use the LEAST function:

Copy code

```
SELECT LEAST(1, 3, 0, 4);
```

```
+-------------------+
| LEAST(1, 3, 0, 4) |
|-------------------|
|                 0 |
+-------------------+
```

Copy code

```
SELECT col_1,
       col_2,
       col_3,
       LEAST(col_1, col_2, col_3) AS least
  FROM (SELECT 1 AS col_1, 2 AS col_2, 3 AS col_3
    UNION ALL
    SELECT 2, 4, -1
    UNION ALL
    SELECT 3, 6, NULL);
```

```
+-------+-------+-------+-------+
| COL_1 | COL_2 | COL_3 | LEAST |
|-------+-------+-------+-------|
|     1 |     2 |     3 |     1 |
|     2 |     4 |    -1 |    -1 |
|     3 |     6 |  NULL |  NULL |
+-------+-------+-------+-------+
```
