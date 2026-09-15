Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# MAX (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the maximum value for the specified column in a table.

The MAX system data metric function is optimized to calculate the maximum value for a single column and provides greater performance when
compared to calling the [MAX](/sql-reference/functions/max) function.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.MAX(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns either a NUMBER or FLOAT value.

## Example

Measure the maximum value for the `salary` column in a table:

Copy code

```
SELECT SNOWFLAKE.CORE.MAX(
  SELECT
    salary
  FROM hr.tables.empl_info);
```

```
+------------------------------------------------------------+
| SNOWFLAKE.CORE.MAX(SELECT salary FROM hr.tables.empl_info) |
+------------------------------------------------------------+
| 325000                                                     |
+------------------------------------------------------------+
```
