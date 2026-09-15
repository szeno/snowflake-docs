Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_BEGIN

Returns the inclusive beginning bound of a PERIOD value.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_BEGIN( <period> )
```

## Arguments

`period`
:   The PERIOD value to inspect.

## Returns

A DATE, TIME, TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, or TIMESTAMP\_TZ value that matches the element type of the input PERIOD.

## Usage notes

- If the input is NULL, the function returns NULL.

## Examples

This example returns the inclusive beginning bound of a PERIOD(DATE) value. Because a NULL input produces
a NULL result, the second column returns NULL:

Copy code

```
SELECT
    PERIOD_BEGIN(PERIOD(DATE) '[2024-01-01, 2024-12-31)') AS begin_bound,
    PERIOD_BEGIN(CAST(NULL AS PERIOD(DATE))) AS null_input;
```

```
+-------------+------------+
| BEGIN_BOUND | NULL_INPUT |
|-------------+------------|
| 2024-01-01  | NULL       |
+-------------+------------+
```
