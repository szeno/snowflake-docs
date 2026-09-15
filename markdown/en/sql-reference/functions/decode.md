Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# DECODE

Compares the select expression to each search expression in order. As soon as
a search expression matches the selection expression, the corresponding result
expression is returned.

Note

DECODE in Snowflake is different from the DECODE function in PostgreSQL,
which converts data into different encodings.

## Syntax

Copy code

```
DECODE( <expr> , <search1> , <result1> [ , <search2> , <result2> ... ] [ , <default> ] )
```

## Arguments

`expr`
:   This is the “select expression”. The “search expressions” are compared to
    this select expression, and if there is a match then `DECODE`
    returns the result that corresponds to that search expression. The select
    expression is typically a column, but can be a subquery, literal, or other
    expression.

`searchN`
:   The search expressions indicate the values to compare to the select
    expression. If one of these search expressions matches, the function returns
    the corresponding `result`. If more than one search expression would
    match, only the first match’s result is returned.

`resultN`
:   The results are the values that will be returned if one of the search
    expressions matches the select expression.

`default`
:   If an optional default is specified, and if none of the search expressions
    match the select expression, then `DECODE` returns this default value.

## Usage notes

- Note that, contrary to [CASE](/sql-reference/functions/case), a NULL value in the select expression
  matches a NULL value in the search expressions.
- The `expr` can include set operators, such as `UNION`,
  `INTERSECT`, `EXCEPT`, and `MINUS`. When using set operators,
  make sure that data types are compatible. For details, see the
  [General usage notes](/sql-reference/operators-query#label-operators-query-general-usage-notes) in the
  [Set operators](/sql-reference/operators-query) topic.

## Collation details

- The collation specifications of the select expression and the search expressions must all be compatible.
- The value returned from the function retains the collation specification of the result with the
  highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation.

## Examples

Create a table and insert rows:

> Copy code
>
> ```
> CREATE TABLE d (column1 INTEGER);
> INSERT INTO d (column1) VALUES
>     (1),
>     (2),
>     (NULL),
>     (4);
> ```

Example with a default value `'other'` (note that NULL equals NULL):

> Copy code
>
> ```
> SELECT column1, decode(column1,
>                        1, 'one',
>                        2, 'two',
>                        NULL, '-NULL-',
>                        'other'
>                       ) AS decode_result
>     FROM d;
> +---------+---------------+
> | COLUMN1 | DECODE_RESULT |
> |---------+---------------|
> |       1 | one           |
> |       2 | two           |
> |    NULL | -NULL-        |
> |       4 | other         |
> +---------+---------------+
> ```

Example without a default value (note that the non-matching value returns NULL):

> Copy code
>
> ```
> SELECT column1, decode(column1,
>                        1, 'one',
>                        2, 'two',
>                        NULL, '-NULL-'
>                        ) AS decode_result
>     FROM d;
> +---------+---------------+
> | COLUMN1 | DECODE_RESULT |
> |---------+---------------|
> |       1 | one           |
> |       2 | two           |
> |    NULL | -NULL-        |
> |       4 | NULL          |
> +---------+---------------+
> ```
