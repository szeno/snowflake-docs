Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_CA\_POSTAL\_CODE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are not a Canadian postal code in the `A1A 1A1` form.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_CA_POSTAL_CODE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The value must be a letter, digit, and letter, then a digit, letter, and digit, with an optional single space between the two
  halves. The first letter cannot be D, F, I, O, Q, U, W, or Z, and the other letters cannot be D, F, I, O, Q, or U.
- Letters are matched case-insensitively.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not verify that the postal code is assigned.

## Example

Measure the number of invalid Canadian postal codes in the `postal_code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_CA_POSTAL_CODE_COUNT(
  SELECT
    postal_code
  FROM crm.tables.addresses
);
```
