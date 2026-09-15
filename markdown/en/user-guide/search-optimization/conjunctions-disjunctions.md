# How conjunctions (AND) and disjunctions (OR) work with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Search optimization can accelerate queries using [conjunctions](#label-search-optimization-service-queries-and) (AND operator)
and [disjunctions](#label-search-optimization-service-queries-or) (OR operator) of supported predicates.

## Conjunctions of supported predicates (AND)

For queries that use conjunctions of predicates (i.e., AND), query performance can be improved by search optimization if
any of the predicates [would benefit](/user-guide/search-optimization/queries-that-benefit).

For example, suppose that a query has:

> `where condition_x and condition_y`

Search optimization can improve performance if either condition separately returns a few rows (i.e., `condition_x`
returns a few rows or `condition_y` returns a few rows).

If `condition_x` returns a few rows but `condition_y` returns many rows, the query performance can still
benefit from search optimization.

### Examples

If predicates are individually supported by the search optimization service, then they can be joined by the conjunction
`AND` and still be supported by the search optimization service:

Copy code

```
SELECT id, c1, c2, c3
  FROM test_table
  WHERE c1 = 1
    AND c3 = TO_DATE('2004-03-09')
  ORDER BY id;
```

DELETE and UPDATE (and MERGE) can also use the search optimization service:

Copy code

```
DELETE FROM test_table WHERE id = 3;
```

Copy code

```
UPDATE test_table SET c1 = 99 WHERE id = 4;
```

## Disjunctions of supported predicates (OR)

For queries that use disjunctions of predicates (i.e., OR), query performance can be improved by search optimization if
all predicates [would benefit](/user-guide/search-optimization/queries-that-benefit).

For example, suppose that a query has:

> `where condition_x or condition_y`

Search optimization can improve performance if each condition separately returns a few rows (i.e., `condition_x` returns
a few rows and `condition_y` returns a few rows).

If `condition_x` returns a few rows but `condition_y` returns many rows, the query performance does not
benefit from search optimization.

In the case of disjunctions, each predicate in isolation is not decisive in the query. All predicates must be evaluated
to determine whether search optimization can improve performance.
