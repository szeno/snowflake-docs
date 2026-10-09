Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NOT\_NULL\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of column values that are not NULL for the specified column in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NOT_NULL_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- DATE
- FLOAT
- NUMBER
- TIMESTAMP\_LTZ
- TIMESTAMP\_NTZ
- TIMESTAMP\_TZ
- VARCHAR

## Returns

The function returns a NUMBER value.

## Example

Measure the number of non-NULL values for the SSN column:

Copy code

```
SELECT SNOWFLAKE.CORE.NOT_NULL_COUNT(
  SELECT
    ssn
  FROM hr.tables.empl_info
);
```
