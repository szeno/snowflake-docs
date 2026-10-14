Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NOT\_TUESDAY\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that do not fall on a Tuesday. The percentage is computed over the total row count,
including
`NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NOT_TUESDAY_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `DATE`
- `TIMESTAMP_LTZ`
- `TIMESTAMP_TZ`

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The day of the week is determined with [DAYOFWEEKISO](/sql-reference/functions/year), so the result does not depend on the
  `WEEK_START` session parameter.
- For a `TIMESTAMP_LTZ` value, the day is determined in the session time zone. For a `TIMESTAMP_TZ` value, the day is
  determined from
  the value’s own time zone offset.

## Example

Measure the percentage of dates that are not a Tuesday in the `run_date` column:

Copy code

```
SELECT SNOWFLAKE.CORE.NOT_TUESDAY_PERCENT(
  SELECT
    run_date
  FROM etl.tables.batch_runs
);
```
