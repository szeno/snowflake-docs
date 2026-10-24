Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NULL\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the total number of NULL values for the specified column in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NULL_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects exactly one column.

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

The `query` must project exactly one column. If the query projects more than one column, the call fails
with an error similar to the following:

```
Invalid argument types for function 'NULL_COUNT$V1': (ROW(NUMBER(38,0), VARCHAR(25)))
```

To fix the error, project one column, or call the function once for each column:

Copy code

```
-- Fails: two columns are projected.
SELECT SNOWFLAKE.CORE.NULL_COUNT(
  SELECT c_custkey, c_name FROM snowflake_sample_data.tpch_sf1.customer
);

-- Works: one column is projected.
SELECT SNOWFLAKE.CORE.NULL_COUNT(
  SELECT c_name FROM snowflake_sample_data.tpch_sf1.customer
);
```

When you call a system DMF manually, you don’t need to specify whichever allowed data type you are using. You only need to specify the
query for the column that you want to measure. Snowflake matches the allowed data type for the function with the data type for the column.

## Example

Measure the number of NULL values for the SSN column (that is, US Social Security number):

Copy code

```
SELECT SNOWFLAKE.CORE.NULL_COUNT(
  SELECT
    ssn
  FROM hr.tables.empl_info
);
```

```
+----------------------------------------------------------------+
| SNOWFLAKE.CORE.NULL_COUNT(SELECT ssn FROM hr.tables.empl_info) |
+----------------------------------------------------------------+
| 5                                                              |
+----------------------------------------------------------------+
```
