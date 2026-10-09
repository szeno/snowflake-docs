Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_TIMESTAMP\_STRING\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that can’t be parsed as a timestamp or a date. The percentage is computed over the total row
count, including NULL values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_TIMESTAMP_STRING_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a FLOAT value.

## Usage notes

- A value is valid if `TRY_TO_TIMESTAMP` or `TRY_TO_DATE` can parse it, so the function accepts any format Snowflake accepts when
  casting, which is broader than ISO 8601.

## Example

Measure the percentage of invalid timestamp strings in the `event_time_str` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_TIMESTAMP_STRING_PERCENT(
  SELECT
    event_time_str
  FROM staging.tables.csv_imports
);
```
