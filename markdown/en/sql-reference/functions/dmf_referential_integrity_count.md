Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# REFERENTIAL\_INTEGRITY\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of rows in the source table where the column value does not have a corresponding match in the referenced table.
These unmatched rows are known as *orphaned rows* and represent violations of referential integrity.

If you specify more than one column argument, returns the count of rows where the combination of the specified source columns does
not match any row in the referenced table based on the corresponding reference columns.

## Syntax

Copy code

```
SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT ON ( <column>, TABLE(<ref_table>(<ref_column>)) )
```

For compound (multi-column) keys:

Copy code

```
SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT ON (
  <column1>, <column2>, ...,
  TABLE(<ref_table>(<ref_column1>, <ref_column2>, ...))
)
```

## Arguments

`column`
:   Specifies one or more columns in the source table whose values are checked for referential integrity against the referenced table.
    When multiple source columns are specified, they form a compound key.

`TABLE(ref_table(ref_column))`
:   Specifies the referenced (parent) table and column(s) to validate against, using the `TABLE(...)` syntax:

    - `ref_table` — The fully qualified name of the referenced table (for example, `my_db.my_schema.my_table`).
    - `ref_column` — One or more columns in the referenced table that correspond to the source columns.

    The number and order of source columns must match the number and order of reference columns.

## Allowed data types

The columns specified in the `column` and `ref_column` arguments can contain any of the following data types:

- DATE
- FLOAT
- NUMBER
- TIMESTAMP\_LTZ
- TIMESTAMP\_NTZ
- TIMESTAMP\_TZ
- VARCHAR

## Returns

The function returns a NUMBER value.

- A return value of **0** means every row in the source table has a corresponding match in the referenced table. Referential
  integrity is fully satisfied.
- A return value of **N > 0** means there are N rows in the source table that do not have a matching row in the referenced table.
  These N rows are considered orphaned.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table or view so it runs at regular
  intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate). You can use the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function
  to run the REFERENTIAL\_INTEGRITY\_COUNT function against a table without associating it.
- NULL values in the source column are **not** counted as violations. Rows where the source column value is NULL are excluded
  from the referential integrity check. This follows standard Foreign Key (FK) constraint semantics, where a NULL foreign key is
  considered valid. If you need to monitor NULL values in the source column, use the
  [NULL\_COUNT](/sql-reference/functions/dmf_null_count) DMF alongside this function.
- The number and order of source columns must match the reference columns. This is validated when you associate the function.
- Renaming a column that is specified in the REFERENTIAL\_INTEGRITY\_COUNT function breaks the association between the function
  and the column’s table or view. If you rename the column, you must re-associate the function with the table or view.
- You cannot associate this function with the same column and reference table combination more than once.

## Examples

### Single-column referential integrity check

Associate the function with table `salesorders` so it returns the count of rows where `sp_id` does not exist in the `sp_id`
column of the `salespeople` table:

Copy code

```
ALTER TABLE salesorders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT
    ON (sp_id, TABLE(my_db.sch1.salespeople(sp_id)));
```

### Compound key referential integrity check

Associate the function with table `order_items` so it returns the count of rows where the combination of `order_id` and
`product_id` does not have a matching row in the `order_products` table:

Copy code

```
ALTER TABLE order_items
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT
    ON (order_id, product_id, TABLE(my_db.sch1.order_products(order_id, product_id)));
```

### Drop the association

Remove the referential integrity check from the `salesorders` table:

Copy code

```
ALTER TABLE salesorders
  DROP DATA METRIC FUNCTION SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT
    ON (sp_id, TABLE(my_db.sch1.salespeople(sp_id)));
```

### Associate with an expectation

Associate the function and define an expectation that referential integrity should be fully satisfied (zero orphaned rows):

Copy code

```
ALTER TABLE salesorders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT
    ON (sp_id, TABLE(my_db.sch1.salespeople(sp_id)))
    EXPECTATION no_orphans (VALUE = 0);
```

### Add an expectation to an existing association

If the DMF is already associated, add an expectation using `MODIFY`:

Copy code

```
ALTER TABLE salesorders
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.REFERENTIAL_INTEGRITY_COUNT
    ON (sp_id, TABLE(my_db.sch1.salespeople(sp_id)))
    ADD EXPECTATION no_orphans (VALUE = 0);
```
