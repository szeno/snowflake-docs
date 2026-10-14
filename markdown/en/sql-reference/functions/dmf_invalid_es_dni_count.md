Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_ES\_DNI\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are not a Spanish DNI number: eight digits followed by a check letter.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_ES_DNI_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The value must be eight digits followed by one of the 23 DNI check letters. The letters I, O, and U are never used.
- Letters are matched case-insensitively.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- Foreigner identity numbers (NIE), which start with X, Y, or Z, are counted.
- The function checks the format only; it does not verify that the check letter matches the digits.

## Example

Measure the number of invalid Spanish DNI numbers in the `dni` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_ES_DNI_COUNT(
  SELECT
    dni
  FROM hr.tables.employees
);
```
