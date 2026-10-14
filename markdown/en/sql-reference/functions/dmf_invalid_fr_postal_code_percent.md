Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_FR\_POSTAL\_CODE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not a French postal code: five digits with a prefix that is in use. The
percentage
is computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_FR_POSTAL_CODE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be five digits that start with `01` to `95`, `97`, or `98`, or with the reserved military prefix `00`. Values
  that
  start with `96` or `99` are counted.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not verify that the postal code is assigned.

## Example

Measure the percentage of invalid French postal codes in the `postal_code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_FR_POSTAL_CODE_PERCENT(
  SELECT
    postal_code
  FROM crm.tables.addresses
);
```
