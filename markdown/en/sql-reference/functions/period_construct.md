Categories:
:   [Period functions](/sql-reference/functions-period)

# PERIOD\_CONSTRUCT

Constructs a PERIOD value from a beginning bound and an ending bound of the same temporal element type.

See also:
:   [PERIOD data type](/sql-reference/data-types-period) , [Period functions](/sql-reference/functions-period)

## Syntax

Copy code

```
PERIOD_CONSTRUCT( <begin>, <end> )
```

## Arguments

`begin`
:   The inclusive beginning bound. Must be a DATE, TIME, TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, or TIMESTAMP\_TZ value.

`end`
:   The exclusive ending bound. Must have the same logical type as `begin`.

## Returns

A PERIOD value whose element type matches the type of the input bounds. For TIME and TIMESTAMP inputs, the result scale is the maximum of the input scales.

## Usage notes

- The `begin` and `end` arguments must be temporal values (DATE, TIME, or TIMESTAMP). A VARCHAR argument isn’t implicitly converted and raises an error; cast the string explicitly, for example `DATE '2024-01-01'` or `'2024-01-01'::DATE`.
- If `begin` is greater than or equal to `end`, Snowflake raises an error.
- If either argument is NULL, the function returns NULL.
- To create a PERIOD value from a string instead of two bound expressions, use the typed literal syntax, for example `PERIOD(DATE) '[2024-01-01, 2024-12-31)'`. For more information, see [Typed literal](/sql-reference/data-types-period#label-period-datatype-typed-literal).

## Examples

This example constructs a PERIOD(DATE) value from two DATE bounds. Because a NULL bound produces a
NULL result, the second column returns NULL:

Copy code

```
SELECT
    PERIOD_CONSTRUCT(DATE '2024-01-01', DATE '2024-12-31') AS date_period,
    PERIOD_CONSTRUCT(CAST(NULL AS DATE), DATE '2024-12-31') AS null_input;
```

```
+--------------------------+------------+
| DATE_PERIOD              | NULL_INPUT |
|--------------------------+------------|
| [2024-01-01, 2024-12-31) | NULL       |
+--------------------------+------------+
```
