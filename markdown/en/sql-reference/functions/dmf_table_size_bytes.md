Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# TABLE\_SIZE\_BYTES (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the logical size, in bytes, of the associated table. The value is the same as the `BYTES` column of the
[TABLES](/sql-reference/info-schema/tables) view in the Information Schema.

## Syntax

Not applicable.

## Returns

The function returns a scalar value with a `NUMBER` data type.

Values larger than 9007199254740991 bytes (253 − 1, about 9 PB) are returned as 9007199254740991.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table so it runs at regular intervals,
  see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).
- This function is supported only for table objects. It can’t be associated with a view, materialized view, dynamic table, event
  table, or Apache Iceberg™ table. When you [associate it with a schema](/user-guide/data-quality-schema-level), it applies only to
  tables in the schema.
- You can’t use [FILTER](/user-guide/data-quality-filter) or [WITHIN GROUP](/user-guide/data-quality-group-by) with this function.
- To count the rows in a table rather than measure its size, use [ROW\_COUNT](/sql-reference/functions/dmf_row_count).

## Example

Associate the function with the `events` table, and define an expectation that is violated when the table reaches 1 TB:

Copy code

```
ALTER TABLE logs.public.events
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.TABLE_SIZE_BYTES
    ON ()
    EXPECTATION under_1_tb (VALUE < 1000000000000);
```
