Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_PRECEDES

Returns TRUE if the first PERIOD ends at or before the second PERIOD begins.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_PRECEDES( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

BOOLEAN.

## Usage notes

- TRUE when `PERIOD_END(period1) <= PERIOD_BEGIN(period2)`.
- Adjacent periods that meet also precede: `PERIOD_PRECEDES([a, b), [b, c))` is TRUE.

## Examples

This example shows a period that precedes another (it ends at or before the second begins), and one
that doesn’t:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p_left,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p_right,
    PERIOD(DATE) '[2024-01-01, 2024-07-01)' AS p_long
)
SELECT
    PERIOD_PRECEDES(p_left, p_right) AS precedes_true,
    PERIOD_PRECEDES(p_long, p_right) AS precedes_false
  FROM periods;
```

```
+---------------+----------------+
| PRECEDES_TRUE | PRECEDES_FALSE |
|---------------+----------------|
| True          | False          |
+---------------+----------------+
```
