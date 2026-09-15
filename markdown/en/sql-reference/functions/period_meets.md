Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_MEETS

Returns TRUE if two PERIOD values are adjacent in either order.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_MEETS( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

BOOLEAN.

## Usage notes

- TRUE when `PERIOD_END(period1) = PERIOD_BEGIN(period2)` or `PERIOD_END(period2) = PERIOD_BEGIN(period1)`.
- Equivalent to `PERIOD_IMMEDIATELY_PRECEDES(period1, period2) OR PERIOD_IMMEDIATELY_SUCCEEDS(period1, period2)`.

## Examples

This example shows two adjacent periods that meet at `2024-04-01`, and a pair that share a begin
bound and so don’t meet:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p_left,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p_right,
    PERIOD(DATE) '[2024-01-01, 2024-07-01)' AS p_long
)
SELECT
    PERIOD_MEETS(p_left, p_right) AS adjacent,
    PERIOD_MEETS(p_left, p_long) AS not_adjacent
  FROM periods;
```

```
+----------+--------------+
| ADJACENT | NOT_ADJACENT |
|----------+--------------|
| True     | False        |
+----------+--------------+
```
