# Period functions

Snowflake provides scalar functions for constructing, inspecting, comparing, and combining
[PERIOD](/sql-reference/data-types-period) values. PERIOD values are half-open
ranges `[begin, end)`: the beginning bound is inclusive and the ending bound is exclusive.

Unless noted otherwise:

- Both PERIOD arguments must have the same element type (for example, both PERIOD(DATE)).
- A NULL input produces a NULL result.
- Predicate functions return BOOLEAN.
- Set-operation functions return PERIOD (or NULL when the result would be empty).

## Constructor and accessors

> - [PERIOD\_CONSTRUCT](/sql-reference/functions/period_construct)
> - [PERIOD\_BEGIN](/sql-reference/functions/period_begin)
> - [PERIOD\_END](/sql-reference/functions/period_end)

## Boolean predicates

> - [PERIOD\_OVERLAPS](/sql-reference/functions/period_overlaps)
> - [PERIOD\_CONTAINS](/sql-reference/functions/period_contains)
> - [PERIOD\_EQUALS](/sql-reference/functions/period_equals)
> - [PERIOD\_PRECEDES](/sql-reference/functions/period_precedes)
> - [PERIOD\_SUCCEEDS](/sql-reference/functions/period_succeeds)
> - [PERIOD\_IMMEDIATELY\_PRECEDES](/sql-reference/functions/period_immediately_precedes)
> - [PERIOD\_IMMEDIATELY\_SUCCEEDS](/sql-reference/functions/period_immediately_succeeds)
> - [PERIOD\_MEETS](/sql-reference/functions/period_meets)

## Set operations

> - [PERIOD\_INTERSECT](/sql-reference/functions/period_intersect)
> - [PERIOD\_LDIFF](/sql-reference/functions/period_ldiff)
> - [PERIOD\_RDIFF](/sql-reference/functions/period_rdiff)

## Examples

Because PERIOD values are half-open, two back-to-back periods meet without overlapping. The earlier
period doesn’t contain the shared boundary instant (its exclusive ending bound), but the later period
does (its inclusive beginning bound):

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p1,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p2
)
SELECT
    PERIOD_OVERLAPS(p1, p2) AS overlaps,
    PERIOD_MEETS(p1, p2) AS meets,
    PERIOD_CONTAINS(p1, DATE '2024-04-01') AS p1_contains_boundary,
    PERIOD_CONTAINS(p2, DATE '2024-04-01') AS p2_contains_boundary
  FROM periods;
```

```
+----------+-------+----------------------+----------------------+
| OVERLAPS | MEETS | P1_CONTAINS_BOUNDARY | P2_CONTAINS_BOUNDARY |
|----------+-------+----------------------+----------------------|
| False    | True  | False                | True                 |
+----------+-------+----------------------+----------------------+
```

For a full table-based walkthrough that stores, queries, orders, and combines PERIOD values, see
[Examples for the PERIOD data type](/sql-reference/data-types-period#label-period-datatype-examples).

## List of functions

| Function | Description |
| --- | --- |
| [PERIOD\_BEGIN](/sql-reference/functions/period_begin) | Returns the inclusive beginning bound of a PERIOD. |
| [PERIOD\_CONSTRUCT](/sql-reference/functions/period_construct) | Builds a PERIOD from beginning and ending temporal values. |
| [PERIOD\_CONTAINS](/sql-reference/functions/period_contains) | Tests whether a PERIOD contains another PERIOD or a temporal instant. |
| [PERIOD\_END](/sql-reference/functions/period_end) | Returns the exclusive ending bound of a PERIOD. |
| [PERIOD\_EQUALS](/sql-reference/functions/period_equals) | Tests whether two PERIOD values have the same bounds. |
| [PERIOD\_IMMEDIATELY\_PRECEDES](/sql-reference/functions/period_immediately_precedes) | Tests whether the first PERIOD ends exactly where the second begins. |
| [PERIOD\_IMMEDIATELY\_SUCCEEDS](/sql-reference/functions/period_immediately_succeeds) | Tests whether the first PERIOD begins exactly where the second ends. |
| [PERIOD\_INTERSECT](/sql-reference/functions/period_intersect) | Returns the overlapping sub-range of two PERIOD values, or NULL if disjoint. |
| [PERIOD\_LDIFF](/sql-reference/functions/period_ldiff) | Returns the portion of the first PERIOD before the second begins, or NULL. |
| [PERIOD\_MEETS](/sql-reference/functions/period_meets) | Tests whether two PERIOD values are adjacent in either order. |
| [PERIOD\_OVERLAPS](/sql-reference/functions/period_overlaps) | Tests whether two PERIOD values share any instant. |
| [PERIOD\_PRECEDES](/sql-reference/functions/period_precedes) | Tests whether the first PERIOD ends at or before the second begins. |
| [PERIOD\_RDIFF](/sql-reference/functions/period_rdiff) | Returns the portion of the first PERIOD after the second ends, or NULL. |
| [PERIOD\_SUCCEEDS](/sql-reference/functions/period_succeeds) | Tests whether the first PERIOD begins at or after the second ends. |

Expand

Show lessSee more
