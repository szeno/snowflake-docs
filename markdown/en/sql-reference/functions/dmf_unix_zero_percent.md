Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# UNIX\_ZERO\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are equal to the Unix epoch, `1970-01-01`. The percentage is computed over the
total row
count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.UNIX_ZERO_PERCENT(<query>)
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

- A value at the Unix epoch often means that a timestamp conversion failed and defaulted to zero.
- For a `DATE` column, the function counts the date `1970-01-01`. For a `TIMESTAMP_LTZ` or `TIMESTAMP_TZ` column, the function
  counts values
  at the instant `1970-01-01 00:00:00 UTC`, whatever their time zone offset. For example, `1969-12-31 16:00:00 -08:00` is
  counted, but
  `1970-01-01 00:00:00 +05:00` isn’t.
- The result does not depend on the `TIMESTAMP_INPUT_FORMAT` session parameter.

## Example

Measure the percentage of Unix-epoch timestamps in the `created_at` column:

Copy code

```
SELECT SNOWFLAKE.CORE.UNIX_ZERO_PERCENT(
  SELECT
    created_at
  FROM crm.tables.accounts
);
```
