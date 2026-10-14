Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_NL\_BSN\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are not a Dutch citizen service number (BSN) of eight or nine digits.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_NL_BSN_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The value must be eight or nine digits, without spaces or other separators. The eight-digit form is the nine-digit number
  with its
  leading zero omitted.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not apply the eleven-test (elfproef) or verify that the number was issued.

## Example

Measure the number of invalid Dutch citizen service numbers in the `bsn` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_NL_BSN_COUNT(
  SELECT
    bsn
  FROM hr.tables.employees
);
```
