Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# UNIQUE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the total number of unique non-NULL values for the specified columns in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.UNIQUE_COUNT(<query>)
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

The function returns a scalar value with a NUMBER data type.

## Usage notes

When you call a system DMF manually, you don’t need to specify whichever allowed data type you are using. You only need to specify the
query for the column that you want to measure. Snowflake matches the allowed data type for the function with the data type for the column.

## Example

Measure the number of unique non-NULL values for the SSN column (that is, US Social Security number):

Copy code

```
SELECT SNOWFLAKE.CORE.UNIQUE_COUNT(
  SELECT
    ssn
  FROM hr.tables.empl_info
);
```

```
+------------------------------------------------------------------+
| SNOWFLAKE.CORE.UNIQUE_COUNT(SELECT ssn FROM hr.tables.empl_info) |
+------------------------------------------------------------------+
| 42                                                               |
+------------------------------------------------------------------+
```
