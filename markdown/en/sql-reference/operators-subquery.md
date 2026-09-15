# Subquery operators

A [subquery](/user-guide/querying-subqueries) is a query within another query. Subquery operators
perform operations on the values produced by subqueries.

Snowflake supports the following subquery operators:

- [ALL / ANY](#label-operators-subquery-all-any)
- [[ NOT ] EXISTS](#label-operators-subquery-exists)
- [[ NOT ] IN](#label-operators-subquery-in)

## ALL / ANY

The ALL and ANY keywords can be used to apply a comparison operator to the values produced by a subquery (which can return more than one row).

### Syntax

Copy code

```
<expr> comparisonOperator { ALL | ANY } ( <query> )
```

Where:

Copy code

```
comparisonOperator ::=
  { = | != | > | >= | < | <= }
```

### Usage notes

- The expression is compared with the operator for each value that the subquery returns:

  - If ALL is specified, then the result is TRUE if every row of the subquery satisfies the condition; otherwise, it returns FALSE.
  - If ANY is specified, then the result is TRUE if any row of the subquery satisfies the condition; otherwise, it returns FALSE.
- ANY/ALL subqueries are currently supported only in a [WHERE](/sql-reference/constructs/where) clause.
- ANY/ALL subqueries can’t appear as an argument to an [OR](/sql-reference/operators-logical) operator.
- The subquery must contain only one item in its [SELECT](/sql-reference/sql/select) list.

### Examples

Use a `!= ALL` subquery to find the departments that have no employees:

Copy code

```
SELECT department_id
  FROM departments d
  WHERE d.department_id != ALL (
    SELECT e.department_id
      FROM employees e);
```

## [ NOT ] EXISTS

An EXISTS subquery is a Boolean expression that can appear in a [WHERE](/sql-reference/constructs/where) or [HAVING](/sql-reference/constructs/having) clause,
or in any function that operates on a Boolean expression:

- An EXISTS expression evaluates to TRUE if any rows are produced by the subquery.
- A NOT EXISTS expression evaluates to TRUE if no rows are produced by the subquery.

### Syntax

Copy code

```
[ NOT ] EXISTS ( <query> )
```

### Usage notes

- [Correlated](/user-guide/querying-subqueries#label-correlated-vs-uncorrelated-subqueries) EXISTS subqueries are currently supported only in a
  [WHERE](/sql-reference/constructs/where) clause.
- Correlated EXISTS subqueries cannot appear as an argument to an [OR](/sql-reference/operators-logical) operator.
- Uncorrelated EXISTS subqueries are supported anywhere that a Boolean expression is allowed.

### Examples

Use a correlated NOT EXISTS subquery to find the departments that have no employees:

Copy code

```
SELECT department_id
  FROM departments d
  WHERE NOT EXISTS (
    SELECT 1
      FROM employees e
      WHERE e.department_id = d.department_id);
```

## [ NOT ] IN

The IN and NOT IN operators check whether an expression is included in the values produced by a subquery.

### Syntax

Copy code

```
<expr> [ NOT ] IN ( <query> )
```

### Usage notes

- IN is shorthand for `= ANY`, and is subject to the same restrictions as ANY subqueries.
- NOT IN is shorthand for `!= ALL`, and is subject to the same restrictions as ALL subqueries.
- [NOT] IN can also be used as an operator in expressions that don’t involve a subquery. For details, see
  [[ NOT ] IN](/sql-reference/functions/in).

### Examples

Use a NOT IN subquery that is equivalent to the `!= ALL` subquery example (earlier in this topic)
to find the departments that have no employees:

Copy code

```
SELECT department_id
  FROM departments d
  WHERE d.department_id NOT IN (
    SELECT e.department_id
      FROM employees e);
```
