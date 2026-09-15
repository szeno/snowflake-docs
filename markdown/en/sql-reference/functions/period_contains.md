Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_CONTAINS

Returns TRUE if a PERIOD contains another PERIOD, or contains a temporal instant of the same element type.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

PERIOD\_CONTAINS has two overloads: one that tests whether a PERIOD contains another PERIOD, and one that
tests whether a PERIOD contains a single temporal instant.

### PERIOD in a PERIOD

Copy code

```
PERIOD_CONTAINS( <period1>, <period2> )
```

### Instant in a PERIOD

Copy code

```
PERIOD_CONTAINS( <period>, <value> )
```

## Arguments

### PERIOD in a PERIOD

`period1`
:   The outer PERIOD value.

`period2`
:   The inner PERIOD value. Must have the same element type as `period1`.

### Instant in a PERIOD

`period`
:   The PERIOD value to test.

`value`
:   A DATE, TIME, or TIMESTAMP value whose logical type matches the PERIOD element type.

## Returns

BOOLEAN.

## Usage notes

- PERIOD overload: TRUE when `PERIOD_BEGIN(period1) <= PERIOD_BEGIN(period2)` and `PERIOD_END(period2) <= PERIOD_END(period1)`.
- Scalar overload: TRUE when `PERIOD_BEGIN(period) <= value < PERIOD_END(period)` (inclusive beginning bound, exclusive ending bound).
- The exclusive ending bound is not contained. For example, `PERIOD_CONTAINS(PERIOD(DATE) '[2024-01-01, 2024-04-01)', DATE '2024-04-01')` is FALSE.

## Examples

This example shows that a period contains a fully enclosed period and its inclusive beginning bound,
but not its exclusive ending bound:

Copy code

```
SELECT
    PERIOD_CONTAINS(
      PERIOD(DATE) '[2024-01-01, 2024-04-01)',
      PERIOD(DATE) '[2024-02-01, 2024-03-01)'
    ) AS contains_period,
    PERIOD_CONTAINS(
      PERIOD(DATE) '[2024-01-01, 2024-04-01)',
      DATE '2024-01-01'
    ) AS contains_begin,
    PERIOD_CONTAINS(
      PERIOD(DATE) '[2024-01-01, 2024-04-01)',
      DATE '2024-04-01'
    ) AS contains_end;
```

```
+-----------------+----------------+--------------+
| CONTAINS_PERIOD | CONTAINS_BEGIN | CONTAINS_END |
|-----------------+----------------+--------------|
| True            | True           | False        |
+-----------------+----------------+--------------+
```
