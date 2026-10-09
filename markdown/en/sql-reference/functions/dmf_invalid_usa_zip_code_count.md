Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_USA\_ZIP\_CODE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that are not a U.S. ZIP Code in 5-digit (`12345`) or ZIP+4 (`12345-6789`) form.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_USA_ZIP_CODE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are not counted.

## Usage notes

- The function checks the format only; it does not verify that the ZIP Code is assigned.

## Example

Measure the number of invalid ZIP Codes in the `zip_code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_USA_ZIP_CODE_COUNT(
  SELECT
    zip_code
  FROM crm.tables.addresses
);
```
