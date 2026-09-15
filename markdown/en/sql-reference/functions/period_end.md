Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_END

Returns the exclusive ending bound of a PERIOD value.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_END( <period> )
```

## Arguments

`period`
:   The PERIOD value to inspect.

## Returns

A DATE, TIME, TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, or TIMESTAMP\_TZ value that matches the element type of the input PERIOD.

## Usage notes

- The ending bound is exclusive: it is not contained in the PERIOD.
- If the input is NULL, the function returns NULL.

## Examples

This example returns the exclusive ending bound of a PERIOD(DATE) value. Because a NULL input produces a
NULL result, the second column returns NULL:

Copy code

```
SELECT
    PERIOD_END(PERIOD(DATE) '[2024-01-01, 2024-12-31)') AS end_bound,
    PERIOD_END(CAST(NULL AS PERIOD(DATE))) AS null_input;
```

```
+------------+------------+
| END_BOUND  | NULL_INPUT |
|------------+------------|
| 2024-12-31 | NULL       |
+------------+------------+
```
