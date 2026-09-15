Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_IMMEDIATELY\_SUCCEEDS

Returns TRUE if the first PERIOD begins exactly where the second PERIOD ends.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_IMMEDIATELY_SUCCEEDS( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

BOOLEAN.

## Usage notes

- TRUE when `PERIOD_END(period2) = PERIOD_BEGIN(period1)`.

## Examples

This example shows a period that begins exactly where the second ends, and one that begins elsewhere:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p_left,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p_right
)
SELECT
    PERIOD_IMMEDIATELY_SUCCEEDS(p_right, p_left) AS immediately_succeeds,
    PERIOD_IMMEDIATELY_SUCCEEDS(p_left, p_right) AS not_adjacent
  FROM periods;
```

```
+----------------------+--------------+
| IMMEDIATELY_SUCCEEDS | NOT_ADJACENT |
|----------------------+--------------|
| True                 | False        |
+----------------------+--------------+
```
