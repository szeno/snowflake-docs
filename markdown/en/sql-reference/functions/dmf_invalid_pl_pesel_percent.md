Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_PL\_PESEL\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not a Polish PESEL number: eleven digits that encode a possible birth date. The
percentage is computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_PL_PESEL_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be eleven digits. The third and fourth digits are the birth month, offset by century: `01` to `12`, `21` to
  `32`,
  `41` to `52`, `61` to `72`, or `81` to `92`. The fifth and sixth digits are the day, `01` to `31`.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The day is not checked against the month, so a date such as February 31 is accepted.
- The function checks the format only; it does not validate the check digit or verify that the number was issued.

## Example

Measure the percentage of invalid Polish PESEL numbers in the `pesel` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_PL_PESEL_PERCENT(
  SELECT
    pesel
  FROM hr.tables.employees
);
```
