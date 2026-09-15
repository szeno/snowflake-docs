Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_OVERLAPS

Returns TRUE if two PERIOD values share any instant.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_OVERLAPS( <period1>, <period2> )
```

## Arguments

`period1`
:   The first PERIOD value.

`period2`
:   The second PERIOD value. Must have the same element type as `period1`.

## Returns

BOOLEAN.

## Usage notes

- TRUE when `PERIOD_BEGIN(period1) < PERIOD_END(period2)` and `PERIOD_BEGIN(period2) < PERIOD_END(period1)`.
- Adjacent periods that meet at a shared boundary (for example, `[a, b)` and `[b, c)`) do not overlap.
- The function is symmetric: `PERIOD_OVERLAPS(p1, p2)` equals `PERIOD_OVERLAPS(p2, p1)`.

## Examples

This example shows two periods that share instants (overlap), and two adjacent periods that meet at a
boundary without overlapping:

Copy code

```
SELECT
    PERIOD_OVERLAPS(
      PERIOD(DATE) '[2024-01-01, 2024-04-01)',
      PERIOD(DATE) '[2024-03-01, 2024-06-01)'
    ) AS overlaps,
    PERIOD_OVERLAPS(
      PERIOD(DATE) '[2024-01-01, 2024-04-01)',
      PERIOD(DATE) '[2024-04-01, 2024-07-01)'
    ) AS adjacent;
```

```
+----------+----------+
| OVERLAPS | ADJACENT |
|----------+----------|
| True     | False    |
+----------+----------+
```
