Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# IFF

Returns one of two values depending on whether a Boolean expression evaluates to true or false.
This function is similar to a single-level `if-then-else` expression. It is similar to [CASE](/sql-reference/functions/case),
but only allows a single condition. You can use it to add conditional logic to SQL statements.

## Syntax

Copy code

```
IFF( <condition> , <expr1> , <expr2> )
```

## Arguments

`condition`
:   The condition is an expression that should evaluate to a BOOLEAN value
    (TRUE, FALSE, or NULL).

    If `condition` evaluates to TRUE, returns `expr1`, otherwise
    returns `expr2`.

`expr1`
:   A general expression. The function returns this value if the `condition`
    is true.

`expr2`
:   A general expression. The function returns this value if the `condition`
    is not true (that is, if it is false or NULL).

## Returns

This function can return a value of any type. The function can return NULL if the value of the
expression that is returned is NULL.

## Usage notes

The `condition` can include a SELECT statement containing set
operators, such as UNION, INTERSECT, and EXCEPT (MINUS). When using set operators,
make sure that data types are compatible. For details, see the [General usage notes](/sql-reference/operators-query#label-operators-query-general-usage-notes)
in the [Set operators](/sql-reference/operators-query) topic.

## Collation details

The value returned from the function retains the collation specification of the
highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation
of the `expr1` and `expr2` arguments.

## Examples

The following examples use the `IFF` function.

Return `expr1` because the condition evaluates to true:

Copy code

```
SELECT IFF(TRUE, 'true', 'false');
```

```
+----------------------------+
| IFF(TRUE, 'TRUE', 'FALSE') |
|----------------------------|
| true                       |
+----------------------------+
```

Return `expr2` because the condition evaluates to false:

Copy code

```
SELECT IFF(FALSE, 'true', 'false');
```

```
+-----------------------------+
| IFF(FALSE, 'TRUE', 'FALSE') |
|-----------------------------|
| false                       |
+-----------------------------+
```

Return `expr2` because the condition evaluates to NULL:

Copy code

```
SELECT IFF(NULL, 'true', 'false');
```

```
+----------------------------+
| IFF(NULL, 'TRUE', 'FALSE') |
|----------------------------|
| false                      |
+----------------------------+
```

Return NULL because the value of the expression returned is NULL:

Copy code

```
SELECT IFF(TRUE, NULL, 'false');
```

```
+--------------------------+
| IFF(TRUE, NULL, 'FALSE') |
|--------------------------|
| NULL                     |
+--------------------------+
```

Return `expr1` (`integer`) if the value is an integer, or return
`expr2` (`non-integer`) if the value is not an integer:

Copy code

```
SELECT value, IFF(value::INT = value, 'integer', 'non-integer')
  FROM ( SELECT column1 AS value
           FROM VALUES(1.0), (1.1), (-3.1415), (-5.000), (NULL) )
  ORDER BY value DESC;
```

```
+---------+---------------------------------------------------+
|   VALUE | IFF(VALUE::INT = VALUE, 'INTEGER', 'NON-INTEGER') |
|---------+---------------------------------------------------|
|    NULL | non-integer                                       |
|  1.1000 | non-integer                                       |
|  1.0000 | integer                                           |
| -3.1415 | non-integer                                       |
| -5.0000 | integer                                           |
+---------+---------------------------------------------------+
```

Return `expr1` (`High`) if the value is greater than 50, or return
`expr2` (`Low`) if the value is 50 or lower (or NULL):

Copy code

```
SELECT value, IFF(value > 50, 'High', 'Low')
FROM ( SELECT column1 AS value
         FROM VALUES(22), (63), (5), (99), (NULL) );
```

```
+-------+--------------------------------+
| VALUE | IFF(VALUE > 50, 'HIGH', 'LOW') |
|-------+--------------------------------|
|    22 | Low                            |
|    63 | High                           |
|     5 | Low                            |
|    99 | High                           |
|  NULL | Low                            |
+-------+--------------------------------+
```
