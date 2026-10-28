Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ROW\_COUNT\_DIFFERENCE (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the number of rows in the associated table minus the number of rows in a reference table. Use this function to check that
a table, such as a copy or the output of a pipeline, has the same number of rows as the table it is loaded from.

You associate the function with the table you want to check and specify the reference table as a reference-table argument.

## Syntax

To associate the function with a table:

Copy code

```
ALTER TABLE <table>
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT_DIFFERENCE
    ON ( <column>, TABLE( <ref_table>( <ref_column> ) ) )
```

## Arguments

`column`
:   Specifies one column in the associated table. The function uses the column only to identify the table, and ignores its values.

`TABLE(ref_table(ref_column))`
:   Specifies the reference table and one of its columns:

    - `ref_table`: The fully qualified name of the reference table (for example,
      `my_db.my_schema.my_table`).
    - `ref_column`: One column in the reference table. The function uses the column only to identify
      the table, and ignores its values.

## Allowed data types

The columns specified in the `column` and `ref_column`
arguments can have any data type. The two columns don’t need to have the same data type.

## Returns

The function returns a NUMBER value: the number of rows in the associated table minus the number of rows in the reference table.

- A value of 0 means that both tables have the same number of rows.
- A negative value means that the associated table has fewer rows than the reference table.
- A positive value means that the associated table has more rows than the reference table.

The function counts every row, including rows where the specified columns contain NULL.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table so it runs at regular intervals, see
  [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate). You can’t use the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function with it.
- You must specify the `TABLE(...)` argument and exactly one column for each table. Otherwise, the `ALTER TABLE` command fails.
- This function uses a reference-table argument, so you can’t use [FILTER](/user-guide/data-quality-filter) with it. You also
  can’t use [WITHIN GROUP](/user-guide/data-quality-group-by).
- The value is signed, so an expectation can tell a table that has fewer rows from one that has more. To allow a difference of up to
  `n` rows in either direction, use an expectation such as
  `VALUE BETWEEN -n AND n`.
- The [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations) function doesn’t evaluate expectations that are
  defined on this function.
- To count the rows in a single table, use [ROW\_COUNT](/sql-reference/functions/dmf_row_count).

## Examples

Associate the function with table `analytics.orders_copy`, and define an expectation that is violated when the table has a
different number of rows than `raw.sales.orders`:

Copy code

```
ALTER TABLE analytics.orders_copy
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT_DIFFERENCE
    ON (order_id, TABLE(raw.sales.orders(order_id)))
    EXPECTATION row_counts_match (VALUE = 0);
```
