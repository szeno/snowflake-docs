Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SCHEMA\_CHANGE\_DROP\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the number of columns dropped from the associated table or view since the previous evaluation of the function. On the first
evaluation, the function records a baseline of the object’s columns and returns `0`.

## Syntax

Not applicable.

## Returns

The function returns a scalar value with a `NUMBER` data type.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table or view so it runs at regular
  intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).
- Each dropped column counts as one change.
- Renamed columns aren’t counted. To count renames along with every other kind of schema change, use
  [SCHEMA\_CHANGE\_COUNT](/sql-reference/functions/dmf_schema_change_count).
- Unlike `SCHEMA_CHANGE_COUNT`, this function doesn’t write a row for each change to the
  [DATA\_QUALITY\_MONITORING\_LOGS](/sql-reference/local/data_quality_monitoring_logs) view.
- You can’t use [FILTER](/user-guide/data-quality-filter) or [WITHIN GROUP](/user-guide/data-quality-group-by) with this function.

## Example

Associate the function with the `customers` table, and define an expectation that is violated when a column is dropped:

Copy code

```
ALTER TABLE crm.public.customers
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.SCHEMA_CHANGE_DROP_COUNT
    ON ()
    EXPECTATION no_dropped_columns (VALUE = 0);
```
