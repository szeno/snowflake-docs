Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# CASE

Works like a cascading “if-then-else” statement. In the more general form,
a series of conditions are evaluated in sequence. When a condition evaluates
to TRUE, the evaluation stops and the associated result (after THEN) is
returned. If none of the conditions evaluate to TRUE, then the result after
the optional ELSE is returned, if present; otherwise NULL is returned.

In the second, “shorthand” form, the expression after CASE is compared to
each of the WHEN expressions in sequence, until one matches; then the
associated result (after THEN) is returned. If none of the expressions
match, the result after the optional ELSE is returned, if present;
otherwise NULL is returned.

Note that in the second form, a NULL CASE expression matches none of
the WHEN expressions, even if one of the WHEN expressions is also NULL.

See also:
:   [IFF](/sql-reference/functions/iff)

## Syntax

Copy code

```
CASE
    WHEN <condition1> THEN <result1>
  [ WHEN <condition2> THEN <result2> ]
  [ ... ]
  [ ELSE <result3> ]
END

CASE <expr>
    WHEN <value1> THEN <result1>
  [ WHEN <value2> THEN <result2> ]
  [ ... ]
  [ ELSE <result3> ]
END
```

## Arguments

`condition#`
:   In the first form of `CASE`, each condition is an expression that
    should evaluate to a BOOLEAN value (True, False, or NULL).

`expr`
:   A general expression.

`value`
:   In the second form of `CASE`, each `value` is a potential match
    for `expr`. The `value` can be a literal or an expression.
    The `value` must be the same data type as the `expr`, or
    must be a data type that can be cast to the data type of the `expr`.

`result#`
:   In the first form of the `CASE` clause, if `condition#` is true,
    then the function returns the corresponding `result#`. If more than
    one condition is true, then the result associated with the first true
    condition is returned.

    In the second form of the `CASE` statement, if `value#` matches the
    `expr`, then the corresponding `result` is returned. If more
    than one `value` matches the `expr`, then the first matching
    value’s `result` is returned.

    The result should be an expression that evaluates to a single value.

    In both forms of `CASE`, if the optional `ELSE` clause is present, and
    if no matches are found, then the function returns the result in the
    `ELSE` clause. If no `ELSE` clause is present, and no matches are found,
    then the result is NULL.

## Usage notes

- Note that, contrary to [DECODE](/sql-reference/functions/decode), a NULL value in the condition
  does not match a NULL value elsewhere in the condition.
  For example `WHEN <null_expr> = NULL THEN 'Return me!'` does not
  return “Return me!”. If you want to compare to NULL values, use
  `IS NULL` rather than `= NULL`.
- The `condition#`, `expr`, `value`, and
  `result` can all be general expressions and thus can include
  subqueries that include set operators, such
  as `UNION`, `INTERSECT`, `EXCEPT`, and `MINUS`.
  When using set operators, make sure that data types are compatible. For
  details, see the [General usage notes](/sql-reference/operators-query#label-operators-query-general-usage-notes) in the
  [Set operators](/sql-reference/operators-query) topic.

## Collation details

In the first form of `CASE`, each expression is independent, and the collation specifications in different
branches are independent. For example, in the following, the collation specifications in
`condition1` are independent of the collation specification(s) in `condition2`,
and those collation specifications do not need to be identical or even compatible.

Copy code

```
CASE
    WHEN <condition1> THEN <result1>
  [ WHEN <condition2> THEN <result2> ]
```

In the second form of `CASE`, although all collation-related operations must use compatible collation specifications,
the collation specifications do not need to be identical. For example, in the following statement, the collation
specifications of both `value1` and `value2` must be compatible with the collation specification of
`expr`, but the collation specifications of `value1` and `value2` do not need to be identical
to each other or to the collation specification of `expr`.

> Copy code
>
> ```
> CASE <expr>
>     WHEN <value1> THEN <result1>
>   [ WHEN <value2> THEN <result2> ]
>   ...
> ```

The value returned from the function has the
highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the `THEN`/`ELSE`
arguments.

## Examples

This example shows a typical use of CASE:

Copy code

```
SELECT
    column1,
    CASE
        WHEN column1=1 THEN 'one'
        WHEN column1=2 THEN 'two'
        ELSE 'other'
    END AS result
FROM (values(1),(2),(3)) v;
```

```
+---------+--------+
| COLUMN1 | RESULT |
|---------+--------|
|       1 | one    |
|       2 | two    |
|       3 | other  |
+---------+--------+
```

This example shows that if none of the values match, and there is no ELSE clause,
then the value returned is NULL:

Copy code

```
SELECT
    column1,
    CASE
        WHEN column1=1 THEN 'one'
        WHEN column1=2 THEN 'two'
    END AS result
FROM (values(1),(2),(3)) v;
```

```
+---------+--------+
| COLUMN1 | RESULT |
|---------+--------|
|       1 | one    |
|       2 | two    |
|       3 | NULL   |
+---------+--------+
```

This example handles NULL explicitly.

Copy code

```
SELECT
    column1,
    CASE
        WHEN column1 = 1 THEN 'one'
        WHEN column1 = 2 THEN 'two'
        WHEN column1 IS NULL THEN 'NULL'
        ELSE 'other'
    END AS result
FROM VALUES (1), (2), (NULL);
```

```
+---------+--------+
| COLUMN1 | RESULT |
|---------+--------|
|       1 | one    |
|       2 | two    |
|    NULL | NULL   |
+---------+--------+
```

The following examples combine CASE with collation:

Copy code

```
SELECT CASE COLLATE('m', 'upper')
    WHEN 'M' THEN TRUE
    ELSE FALSE
END;
```

```
+----------------------------+
| CASE COLLATE('M', 'UPPER') |
|     WHEN 'M' THEN TRUE     |
|     ELSE FALSE             |
| END                        |
|----------------------------|
| True                       |
+----------------------------+
```

Copy code

```
SELECT CASE 'm'
    WHEN COLLATE('M', 'lower') THEN TRUE
    ELSE FALSE
END;
```

```
+------------------------------------------+
| CASE 'M'                                 |
|     WHEN COLLATE('M', 'LOWER') THEN TRUE |
|     ELSE FALSE                           |
| END                                      |
|------------------------------------------|
| True                                     |
+------------------------------------------+
```
