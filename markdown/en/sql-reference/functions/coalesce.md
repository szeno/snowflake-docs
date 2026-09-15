Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# COALESCE

Returns the first non-NULL expression among its arguments, or NULL if
all its arguments are NULL.

## Syntax

Copy code

```
COALESCE( <expr1> , <expr2> [ , ... , <exprN> ] )
```

## Usage notes

- Snowflake performs [implicit conversion](/sql-reference/data-type-conversion#label-when-coercion-occurs) of arguments to make
  them compatible. For example, if one of the input expressions is a numeric type, the return type
  is also a numeric type. That is, `SELECT COALESCE('17', 1);` first converts the VARCHAR value `'17'`
  to the NUMBER value `17`, and then returns the first non-NULL value.

  When conversion isn’t possible, implicit conversion fails. For example, `SELECT COALESCE('foo', 1);`
  returns an error because the VARCHAR value `'foo'` can’t be converted to a NUMBER value.

  We recommend passing in arguments of the same type or explicitly converting arguments if needed.

- When implicit conversion converts a non-numeric value to a numeric value, the result is a value
  of type NUMBER(18,5).

  For numeric string arguments that aren’t constants, if NUMBER(18,5) isn’t sufficient to represent
  the numeric value, then [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the argument to a type that
  can represent the value.

## Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The comparisons follow the collation based on the input arguments’ collations and precedences.
- The collation of the result of the function is the highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Examples

The following example shows the values in three columns and then the result
when the COALESCE function is applied to the three columns:

Copy code

```
SELECT column1,
       column2,
       column3,
       COALESCE(column1, column2, column3) AS coalesce_result
  FROM (values
    (1,    2,    3   ),
    (null, 2,    3   ),
    (null, null, 3   ),
    (null, null, null),
    (1,    null, 3   ),
    (1,    null, null),
    (1,    2,    null)
  ) v;
```

```
+---------+---------+---------+-----------------+
| COLUMN1 | COLUMN2 | COLUMN3 | COALESCE_RESULT |
|---------+---------+---------+-----------------|
|       1 |       2 |       3 |               1 |
|    NULL |       2 |       3 |               2 |
|    NULL |    NULL |       3 |               3 |
|    NULL |    NULL |    NULL |            NULL |
|       1 |    NULL |       3 |               1 |
|       1 |    NULL |    NULL |               1 |
|       1 |       2 |    NULL |               1 |
+---------+---------+---------+-----------------+
```
