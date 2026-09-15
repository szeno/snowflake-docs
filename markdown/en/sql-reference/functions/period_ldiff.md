Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_LDIFF

Returns the portion of the first PERIOD that lies before the second PERIOD begins, or NULL when there is no such remainder.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_LDIFF( <period1>, <period2> )
```

## Arguments

`period1`
:   The PERIOD value to subtract from.

`period2`
:   The PERIOD value that may cut the right side of `period1`. Must have the same element type.

## Returns

A PERIOD value of the same element type, or NULL.

## Usage notes

- Returns `[PERIOD_BEGIN(period1), PERIOD_BEGIN(period2))` when `PERIOD_BEGIN(period1) < PERIOD_BEGIN(period2) < PERIOD_END(period1)`.
- Otherwise returns NULL (for example, when the second period does not start inside the first).

## Examples

This example returns the portion of the first period before the second begins. When the second
period doesn’t start inside the first, the function returns NULL:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-07-01)' AS p_long,
    PERIOD(DATE) '[2024-04-01, 2024-10-01)' AS p_mid,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p_right
)
SELECT
    PERIOD_LDIFF(p_long, p_mid) AS left_remainder,
    PERIOD_LDIFF(p_right, p_long) AS no_remainder
  FROM periods;
```

```
+--------------------------+--------------+
| LEFT_REMAINDER           | NO_REMAINDER |
|--------------------------+--------------|
| [2024-01-01, 2024-04-01) | NULL         |
+--------------------------+--------------+
```
