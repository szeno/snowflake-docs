Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# CASE\_FORMAT\_VIOLATION\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that have inconsistent casing. A value is considered a violation if it is not entirely
uppercase, not entirely lowercase, and not title-case. Use this function to validate casing conventions in codes, status fields,
or identifiers.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.CASE_FORMAT_VIOLATION_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are excluded from the count.

## Example

Measure the number of values in the `status` column with inconsistent casing:

Copy code

```
SELECT SNOWFLAKE.CORE.CASE_FORMAT_VIOLATION_COUNT(
  SELECT
    status
  FROM orders.tables.events
);
```
