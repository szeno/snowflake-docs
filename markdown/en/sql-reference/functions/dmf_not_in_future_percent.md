Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NOT\_IN\_FUTURE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not in the future relative to the scheduled evaluation time. The percentage is
computed over the total row count, including NULL values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NOT_IN_FUTURE_PERCENT(<query>)
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

The function returns a FLOAT value.

## Usage notes

- A value equal to the scheduled evaluation time is not in the future. For a DATE column, values are compared with the date of the
  scheduled evaluation time.

## Example

Measure the percentage of rows in the `event_time` column that are not in the future:

Copy code

```
SELECT SNOWFLAKE.CORE.NOT_IN_FUTURE_PERCENT(
  SELECT
    event_time
  FROM events.tables.activity
);
```
