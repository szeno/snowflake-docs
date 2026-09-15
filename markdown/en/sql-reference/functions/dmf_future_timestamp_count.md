Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# FUTURE\_TIMESTAMP\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of column values that are in the future relative to the scheduled evaluation time. Use this function to detect
future-dated records in event or transaction tables.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.FUTURE_TIMESTAMP_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- DATE
- TIMESTAMP\_LTZ
- TIMESTAMP\_TZ

## Returns

The function returns a NUMBER value. NULL values are not counted as future.

## Example

Measure the number of future-dated rows in the `event_time` column:

Copy code

```
SELECT SNOWFLAKE.CORE.FUTURE_TIMESTAMP_COUNT(
  SELECT
    event_time
  FROM events.tables.activity
);
```
