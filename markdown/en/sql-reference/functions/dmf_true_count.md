Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# TRUE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are `TRUE`.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.TRUE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `BOOLEAN` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- `FALSE` and `NULL` values are not counted.

## Example

Measure the number of `TRUE` values in the `is_active` column:

Copy code

```
SELECT SNOWFLAKE.CORE.TRUE_COUNT(
  SELECT
    is_active
  FROM crm.tables.accounts
);
```
