Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_LATITUDE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of column values that are not a valid latitude: values outside the range -90 to 90.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_LATITUDE_COUNT(<query>)
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

- The range is inclusive, so -90 and 90 are valid.

## Example

Measure the number of invalid latitude values in the `latitude` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_LATITUDE_COUNT(
  SELECT
    latitude
  FROM geo.tables.locations
);
```
