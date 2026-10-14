Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_CA\_SIN\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are not a Canadian Social Insurance Number (SIN) of nine digits.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_CA_SIN_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The value must be nine digits, optionally written in groups of three separated by a space or a hyphen, such as `046 454 286`
  or
  `046-454-286`.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not validate the check digit or verify that the number was issued.
- Each separator is optional and checked independently, so mixed or partially separated forms such as `046 454-286` are also
  accepted.

## Example

Measure the number of invalid Canadian Social Insurance Numbers in the `sin` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_CA_SIN_COUNT(
  SELECT
    sin
  FROM hr.tables.employees
);
```
