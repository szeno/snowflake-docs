Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_UUID\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that are not a UUID in the hyphenated 8-4-4-4-12 hexadecimal form.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_UUID_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are not counted.

## Usage notes

- The function checks the format only; it does not validate the UUID version or variant bits.

## Example

Measure the number of invalid UUIDs in the `request_id` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_UUID_COUNT(
  SELECT
    request_id
  FROM events.tables.requests
);
```
