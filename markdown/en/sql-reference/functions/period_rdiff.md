Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_RDIFF

Returns the portion of the first PERIOD that lies after the second PERIOD ends, or NULL when there is no such remainder.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_RDIFF( <period1>, <period2> )
```

## Arguments

`period1`
:   The PERIOD value to subtract from.

`period2`
:   The PERIOD value that may cut the left side of `period1`. Must have the same element type.

## Returns

A PERIOD value of the same element type, or NULL.

## Usage notes

- Returns `[PERIOD_END(period2), PERIOD_END(period1))` when `PERIOD_BEGIN(period1) < PERIOD_END(period2) < PERIOD_END(period1)`.
- Otherwise returns NULL (for example, when the second period does not end inside the first).

## Examples

This example returns the portion of the first period after the second ends. When the second period
doesn’t end inside the first, the function returns NULL:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-07-01)' AS p_long,
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p_left
)
SELECT
    PERIOD_RDIFF(p_long, p_left) AS right_remainder,
    PERIOD_RDIFF(p_left, p_long) AS no_remainder
  FROM periods;
```

```
+--------------------------+--------------+
| RIGHT_REMAINDER          | NO_REMAINDER |
|--------------------------+--------------|
| [2024-04-01, 2024-07-01) | NULL         |
+--------------------------+--------------+
```
