Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NAN\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are NaN (not a number).

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NAN_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `FLOAT`
- `VARCHAR`

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- For a `FLOAT` column, the function counts the IEEE 754 NaN value. Infinity and negative infinity are not counted.
- For a `VARCHAR` column, the function counts the text `NaN`. The match is case-insensitive and ignores leading and trailing
  ASCII whitespace.

## Example

Measure the number of NaN values in the `reading` column:

Copy code

```
SELECT SNOWFLAKE.CORE.NAN_COUNT(
  SELECT
    reading
  FROM iot.tables.sensor_readings
);
```
