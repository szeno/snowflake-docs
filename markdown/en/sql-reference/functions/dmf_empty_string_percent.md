Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# EMPTY\_STRING\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are empty strings (`''`). Whitespace-only strings are not counted; use
[BLANK\_PERCENT](/sql-reference/functions/dmf_blank_percent) to measure both. The percentage is computed over the total row count,
including NULL values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.EMPTY_STRING_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a FLOAT value.

## Example

Measure the percentage of empty strings in the `middle_name` column:

Copy code

```
SELECT SNOWFLAKE.CORE.EMPTY_STRING_PERCENT(
  SELECT
    middle_name
  FROM hr.tables.empl_info
);
```
