Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_PERM\_ID\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that are not a PermID: the literal `1-` followed by 1 to 15 digits.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_PERM_ID_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are not counted.

## Usage notes

- The function checks the format only; it does not verify that the identifier was issued.

## Example

Measure the number of invalid PermIDs in the `perm_id` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_PERM_ID_COUNT(
  SELECT
    perm_id
  FROM finance.tables.organizations
);
```
