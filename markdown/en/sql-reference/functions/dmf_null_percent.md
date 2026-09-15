Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NULL\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of columns values that are NULL for the specified column in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NULL_PERCENT(<query>)
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

The function returns a NUMBER value.

## Example

Measure the percent of NULL values for the SSN column (i.e. US social security number):

Copy code

```
SELECT SNOWFLAKE.CORE.NULL_PERCENT(
  SELECT
    ssn
  FROM hr.tables.empl_info
);
```

```
+----------------------------------------------------------------+
| SNOWFLAKE.CORE.NULL_COUNT(SELECT ssn FROM hr.tables.empl_info) |
+----------------------------------------------------------------+
| 1                                                              |
+----------------------------------------------------------------+
```
