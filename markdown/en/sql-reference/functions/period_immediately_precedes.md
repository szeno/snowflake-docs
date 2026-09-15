Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_IMMEDIATELY\_PRECEDES

Returns TRUE if the first PERIOD ends exactly where the second PERIOD begins.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_IMMEDIATELY_PRECEDES( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

BOOLEAN.

## Usage notes

- TRUE when `PERIOD_END(period1) = PERIOD_BEGIN(period2)`.

## Examples

This example shows a period that ends exactly where the second begins, and one that ends elsewhere:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p_left,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p_right,
    PERIOD(DATE) '[2024-01-01, 2024-07-01)' AS p_long
)
SELECT
    PERIOD_IMMEDIATELY_PRECEDES(p_left, p_right) AS immediately_precedes,
    PERIOD_IMMEDIATELY_PRECEDES(p_left, p_long) AS not_adjacent
  FROM periods;
```

```
+----------------------+--------------+
| IMMEDIATELY_PRECEDES | NOT_ADJACENT |
|----------------------+--------------|
| True                 | False        |
+----------------------+--------------+
```
