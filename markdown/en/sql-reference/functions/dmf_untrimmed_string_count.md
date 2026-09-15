Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# UNTRIMMED\_STRING\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that have leading or trailing whitespace. Use this function to catch data that could
break joins or lookups.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.UNTRIMMED_STRING_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are excluded from the count.

## Example

Measure the number of untrimmed values in the `name` column:

Copy code

```
SELECT SNOWFLAKE.CORE.UNTRIMMED_STRING_COUNT(
  SELECT
    name
  FROM customers.tables.directory
);
```
