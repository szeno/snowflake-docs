Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_CH\_OASI\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not a Swiss OASI (AHV/AVS) social security number: `756` followed by ten
digits.
The percentage is computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_CH_OASI_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be 13 digits that start with `756`. The digits can be grouped with periods as `756.1234.5678.97`; each period
  is
  optional.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not validate the check digit or verify that the number was issued.

## Example

Measure the percentage of invalid Swiss social security numbers in the `ahv_number` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_CH_OASI_PERCENT(
  SELECT
    ahv_number
  FROM hr.tables.employees
);
```
