Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# DUPLICATE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of non-NULL rows whose value occurs more than once in the specified column. Every row with a repeated value
is counted, not only the extra copies. NULL values are excluded from both the numerator and the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.DUPLICATE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- DATE
- FLOAT
- NUMBER
- TIMESTAMP\_LTZ
- TIMESTAMP\_NTZ
- TIMESTAMP\_TZ
- VARCHAR

## Returns

The function returns a FLOAT value. The function returns 0 if the column contains no non-NULL values.

## Example

Measure the percentage of duplicate values in the `email` column:

Copy code

```
SELECT SNOWFLAKE.CORE.DUPLICATE_PERCENT(
  SELECT
    email
  FROM crm.tables.contacts
);
```
