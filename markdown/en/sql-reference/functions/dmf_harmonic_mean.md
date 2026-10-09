Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# HARMONIC\_MEAN (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the harmonic mean of the nonzero values for the specified column in a table. Zero values are excluded, because their
reciprocal is undefined; negative values are included.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.HARMONIC_MEAN(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a FLOAT value. The function returns NULL if the column contains no nonzero values.

## Example

Measure the harmonic mean of the `speed` column:

Copy code

```
SELECT SNOWFLAKE.CORE.HARMONIC_MEAN(
  SELECT
    speed
  FROM iot.tables.readings
);
```
