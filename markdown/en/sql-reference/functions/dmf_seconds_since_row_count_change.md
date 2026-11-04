Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SECONDS\_SINCE\_ROW\_COUNT\_CHANGE (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the number of seconds since the last committed [DML operation](/sql-reference/sql-dml) that changed the number of rows in
the associated table. Use this function to detect a stalled load: a table in which rows have stopped being added or removed.

## Syntax

To associate the function with a table:

Copy code

```
ALTER TABLE <table>
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.SECONDS_SINCE_ROW_COUNT_CHANGE ON ()
```

## Arguments

None. Specify an empty argument list, `ON ()`.

## Returns

The function returns a NUMBER value: the number of seconds between the commit of the most recent DML operation that changed the
number of rows in the table and the time the function is evaluated. The value is never negative.

The following table shows which DML operations reset the value:

| DML operation | Resets the value |
| --- | --- |
| `INSERT` that adds rows | Yes |
| `DELETE` that removes rows | Yes |
| `TRUNCATE` | Yes |
| `COPY INTO` that loads rows | Yes |
| `MERGE` that changes the net number of rows | Yes |
| `UPDATE` | No |
| `MERGE` that only updates rows | No |
| `INSERT` that adds no rows | No |
| A statement that inserts and deletes the same number of rows | No |
| Transaction that is rolled back | No |

Expand

Show lessSee more

If no DML operation has changed the number of rows since the table was created, the value is the time since the table was created.

If Snowflake doesn’t find a table version that changed the number of rows, the value is the time since the oldest table version it reads.
This happens when only operations that don’t change the number of rows, such as `UPDATE`, have run for longer than the table’s retained
version history, or when more such operations have run than Snowflake reads. In this case, the value is a lower bound: the number of
rows last changed at least that many seconds ago. The function doesn’t indicate whether the value is a lower bound.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table so it runs at regular intervals, see
  [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate). You can’t use the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function with it.
- This function is supported only for standard, transient, and temporary tables. It can’t be associated with a view, materialized
  view, dynamic table, event table, external table, Apache Iceberg™ table, or hybrid table. It also can’t be
  [associated with a schema](/user-guide/data-quality-schema-level).
- You can’t use [FILTER](/user-guide/data-quality-filter) or [WITHIN GROUP](/user-guide/data-quality-group-by) with this function.
- The value is measured when the function is evaluated, not at the scheduled time.
- Use a time-based [schedule](/user-guide/data-quality-working#label-data-quality-schedule), such as `'n MINUTE'` or a cron
  expression, with an interval no longer than the maximum age you want to check for. A time-based schedule evaluates the function
  at regular intervals, so a stalled load is detected even when the table stops changing.
- [FRESHNESS](/sql-reference/functions/dmf_freshness) associated without a column measures the time since any DML operation on the
  table, including operations that don’t change the number of rows. SECONDS\_SINCE\_ROW\_COUNT\_CHANGE measures the time since the number
  of rows last changed.

## Example

Set an hourly schedule for table `raw.sales.orders`, then associate the function with the table and define an expectation that is
violated when the number of rows hasn’t changed for more than one day:

Copy code

```
ALTER TABLE raw.sales.orders SET DATA_METRIC_SCHEDULE = '60 MINUTE';

ALTER TABLE raw.sales.orders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.SECONDS_SINCE_ROW_COUNT_CHANGE
    ON ()
    EXPECTATION loaded_within_a_day (VALUE <= 86400);
```
