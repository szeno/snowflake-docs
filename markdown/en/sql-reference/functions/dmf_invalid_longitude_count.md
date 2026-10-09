Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_LONGITUDE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of column values that are not a valid longitude: values outside the range -180 to 180.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_LONGITUDE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a NUMBER value. NULL values are not counted.

## Usage notes

- The range is inclusive, so -180 and 180 are valid.

## Example

Measure the number of invalid longitude values in the `longitude` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_LONGITUDE_COUNT(
  SELECT
    longitude
  FROM geo.tables.locations
);
```
