Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_INTERSECT

Returns the overlapping sub-range of two PERIOD values, or NULL if the periods are disjoint.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_INTERSECT( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

A PERIOD value of the same element type, or NULL when the inputs do not overlap.

## Usage notes

- The result is `[GREATEST(begin1, begin2), LEAST(end1, end2))` when that range is non-empty.
- If the periods are disjoint or only meet at a boundary, the function returns NULL.

## Examples

This example returns the overlapping sub-range of two periods that overlap, and NULL for two adjacent
periods that only meet at a boundary:

Copy code

```
SELECT
    PERIOD_INTERSECT(
      PERIOD(DATE) '[2024-01-01, 2024-07-01)',
      PERIOD(DATE) '[2024-04-01, 2024-10-01)'
    ) AS overlap,
    PERIOD_INTERSECT(
      PERIOD(DATE) '[2024-01-01, 2024-04-01)',
      PERIOD(DATE) '[2024-04-01, 2024-07-01)'
    ) AS adjacent;
```

```
+--------------------------+----------+
| OVERLAP                  | ADJACENT |
|--------------------------+----------|
| [2024-04-01, 2024-07-01) | NULL     |
+--------------------------+----------+
```
