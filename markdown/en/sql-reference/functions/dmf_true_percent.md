Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# TRUE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are `TRUE`. The percentage is computed over the total row count, including `NULL`
values in
the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.TRUE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `BOOLEAN` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- `FALSE` and `NULL` values are not counted.

## Example

Measure the percentage of `TRUE` values in the `is_active` column:

Copy code

```
SELECT SNOWFLAKE.CORE.TRUE_PERCENT(
  SELECT
    is_active
  FROM crm.tables.accounts
);
```
