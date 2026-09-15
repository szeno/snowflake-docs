Categories:
:   [Query syntax](/sql-reference/constructs)

# HAVING

Filters rows produced by [GROUP BY](/sql-reference/constructs/group-by) that do not satisfy a predicate.

## Syntax

Copy code

```
SELECT ...
FROM ...
GROUP BY ...
HAVING <predicate>
[ ... ]
```

## Parameters

`predicate`
:   A [Boolean expression](/sql-reference/data-types-logical).

## Usage notes

- The condition specified by the HAVING clause applies to expressions produced by the [GROUP BY](/sql-reference/constructs/group-by).
  Therefore, the same restrictions that apply to [GROUP BY](/sql-reference/constructs/group-by) expressions also apply to the HAVING
  clause. The predicate can only refer to:

  - Constants.
  - Expressions that appear in [GROUP BY](/sql-reference/constructs/group-by).
  - [Aggregate functions](/sql-reference/functions-aggregation).
- Expressions in the [SELECT](/sql-reference/sql/select) list can be referred to by the column alias defined in the list.

## Examples

Find the departments that have fewer than 10 employees:

> Copy code
>
> ```
> SELECT department_id
> FROM employees
> GROUP BY department_id
> HAVING count(*) < 10;
> ```
