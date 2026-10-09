Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_USA\_PHONE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that are not a U.S. phone number, with or without a `+1` country code, parentheses, and
space, period, or hyphen separators.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_USA_PHONE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are not counted.

## Usage notes

- Area codes and central-office codes must begin with 2-9, per the North American Numbering Plan.
- The function checks the format only; it does not verify that a number is assigned or reachable.

## Example

Measure the number of invalid phone numbers in the `phone` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_USA_PHONE_COUNT(
  SELECT
    phone
  FROM crm.tables.contacts
);
```
