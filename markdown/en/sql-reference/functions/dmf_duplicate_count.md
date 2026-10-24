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
:   Specifies a SQL query that projects exactly one column when you call the function directly. To measure duplicates across multiple
    columns, associate the function with a table by using `ALTER TABLE ... ADD DATA METRIC FUNCTION ... ON (col1, col2)`. For an example,
    see [Examples](/sql-reference/functions/dmf_duplicate_count#label-dmf-duplicate-count-columns-example).

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

## Usage notes

When you call the function directly, the `query` must project exactly one column. If the query projects
more than one column, the call fails with an error similar to the following:

```
Invalid argument types for function 'DUPLICATE_COUNT$V1': (ROW(NUMBER(38,0), VARCHAR(25)))
```

Copy code

```
-- Fails: two columns are projected.
SELECT SNOWFLAKE.CORE.DUPLICATE_COUNT(
  SELECT c_custkey, c_name FROM snowflake_sample_data.tpch_sf1.customer
);

-- Works: one column is projected.
SELECT SNOWFLAKE.CORE.DUPLICATE_COUNT(
  SELECT c_name FROM snowflake_sample_data.tpch_sf1.customer
);
```

To count duplicates for a combination of columns, associate the function with a table as shown in the
[Examples](/sql-reference/functions/dmf_duplicate_count#label-dmf-duplicate-count-columns-example).

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
