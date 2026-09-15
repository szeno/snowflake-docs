Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# DUPLICATE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of column values that have duplicates, including NULL values. If you specify more than one column argument, returns the
number of rows where the combination of the specified columns is duplicated.

If you want to specify more than one column argument, you can’t call the function directly. For an example of associating the function with
a table so you can specify multiple column arguments, see [Examples](/sql-reference/functions/dmf_duplicate_count#label-dmf-duplicate-count-columns-example).

## Syntax

Copy code

```
SNOWFLAKE.CORE.DUPLICATE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects one or more columns.

## Allowed data types

The columns projected by the `query` must have one of the following data types:

- DATE
- FLOAT
- NUMBER
- TIMESTAMP\_LTZ
- TIMESTAMP\_NTZ
- TIMESTAMP\_TZ
- VARCHAR

## Returns

The function returns a scalar value with a NUMBER data type.

## Example

Determine the number of duplicate US Social Security numbers in the `SSN` column:

Copy code

```
SELECT SNOWFLAKE.CORE.DUPLICATE_COUNT(
  SELECT
    ssn
  FROM hr.tables.empl_info
);
```

Associate the DMF with a table to determine the number of duplicates based on the combination of the `first_name` and `last_name`
columns:

Copy code

```
ALTER TABLE t
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.DUPLICATE_COUNT
    ON (first_name, last_name);
```
