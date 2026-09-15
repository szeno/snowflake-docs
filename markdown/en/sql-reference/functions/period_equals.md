Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_EQUALS

Returns TRUE if two PERIOD values have the same beginning and ending bounds.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_EQUALS( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

BOOLEAN.

## Usage notes

- TRUE when `PERIOD_BEGIN(period1) = PERIOD_BEGIN(period2)` and `PERIOD_END(period1) = PERIOD_END(period2)`.

## Examples

This example compares a period with itself (identical bounds) and with a different period:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p_left,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p_right
)
SELECT
    PERIOD_EQUALS(p_left, p_left) AS same,
    PERIOD_EQUALS(p_left, p_right) AS different
  FROM periods;
```

```
+------+-----------+
| SAME | DIFFERENT |
|------+-----------|
| True | False     |
+------+-----------+
```
