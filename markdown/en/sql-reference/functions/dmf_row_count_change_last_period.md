Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ROW\_COUNT\_CHANGE\_LAST\_PERIOD (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the difference between the number of rows in the table in the current window and the average of the same measurement over the baseline.

The current window is the last period: the most recent period of the table’s [data metric schedule](/user-guide/data-quality-working). For details, see [How the comparison works](#label-period-dmf-how).

## Syntax

To associate the function with a table:

Copy code

```
ALTER TABLE <table>
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT_CHANGE_LAST_PERIOD ON ( <time_column> )
```

## Arguments

`time_column`
:   Specifies the column that holds the time of each row, such as the time that the row was loaded or the event time. The function assigns
    each row to a period by this column. The column must have the data type `TIMESTAMP_LTZ`, `TIMESTAMP_NTZ`, or `TIMESTAMP_TZ`. A `TIMESTAMP_NTZ`
    value is read as UTC. The function doesn’t support `DATE` columns.

## Returns

The function returns a `FLOAT` value.

- A positive value means that the measurement went up compared with the baseline, and a negative value means that it went down.
- A value of 0 means that the measurement is the same as the baseline average.
- The function returns `NULL` when the baseline has fewer than two windows of history, that is, until the table has a row earlier than one window before the start of the current window.
- The function returns `NULL` when the result is not finite.
- A scheduled evaluation records a `NULL` result as 0, so a 0 in the results can also mean that there wasn’t enough data.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table so it runs at regular intervals, see
  [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate). You can’t use the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function with it.
- The table must have a [data metric schedule](/user-guide/data-quality-working) that is a cron expression or an interval. You can’t associate
  the function with a table that has the schedule `TRIGGER_ON_CHANGES`.
- Because the result grows with the length of a period, the schedule must fire at evenly spaced times of day. For example,
  `USING CRON */7 * * * * UTC` and `USING CRON 0 9-17 * * * UTC` are rejected. Schedules that fire only on some days, such as
  weekdays or the first day of each month, are allowed. For details, see [UNIQUE\_COUNT\_CHANGE](#label-period-dmf-even).
- You can’t use [FILTER](/user-guide/data-quality-filter) or [WITHIN GROUP](/user-guide/data-quality-group-by) with this function.
- You can’t evaluate this function ad hoc. The [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations) function
  fails for expectations that are defined on this function.
- The result depends on how the table is loaded. If the schedule doesn’t match the load cadence, the value can change even when the
  data doesn’t. For guidance, see [Schedules and the load cadence](#label-period-dmf-cadence).
- This function takes only a time column. It counts every row whose time column isn’t `NULL`, including rows where other columns
  contain `NULL`. A row whose time column is `NULL` isn’t in any period.

## How the comparison works

The period-comparison system DMFs compare the data in the most recent periods of a table’s [data metric schedule](/user-guide/data-quality-working)
with a baseline of the data before them. They have the suffix `_LAST_PERIOD`, `_LAST_TWO_PERIODS`, `_LAST_FOUR_PERIODS`, or
`_LAST_EIGHT_PERIODS`, which sets the length of the window that the function compares.

**Periods**

A period is one interval of the table’s `DATA_METRIC_SCHEDULE`. The boundaries of the periods are the times at which the schedule fires, in the time
zone of the cron expression (UTC for an interval schedule), compared as instants. The function assigns each row to a period by the value of the
time column that you specify.

- The schedule must be a cron expression or an interval. You can’t associate one of these functions with a table whose schedule is
  `TRIGGER_ON_CHANGES`, change the schedule of a table to `TRIGGER_ON_CHANGES` while it has one of these functions, or resume an association on such a
  table. If you clone a table, or create a table with `CREATE TABLE ... LIKE`, into a schema that has the schedule `TRIGGER_ON_CHANGES`, the
  association is suspended. A table that you move into such a schema, for example by renaming it or swapping it, is suspended at its next evaluation.
  `CREATE TABLE ... LIKE` copies the associations but not the table’s `DATA_METRIC_SCHEDULE`, so the new table uses the schedule that it inherits.
- For the functions whose result grows with the length of a period (`ROW_COUNT_CHANGE`, `SUM_CHANGE`,
  `UNIQUE_COUNT_CHANGE`, `NULL_COUNT_CHANGE`, `ZERO_COUNT_CHANGE`, `NEGATIVE_COUNT_CHANGE`, their `_PERCENT` forms, `NEW_VALUE_COUNT`, and
  `MISSING_VALUE_COUNT`), the schedule must fire at evenly spaced times of day, so that the periods within a day have the same length. The minute and hour
  fields of a cron expression must fire at equal gaps through the day, including the gap to the next day. Schedules that skip days,
  such as weekday or monthly schedules, are allowed but can still have periods of different lengths; see [Schedules and the load cadence](#label-period-dmf-cadence).

  - Allowed: `*/5 * * * *`, `*/15 * * * *`, `0,30 * * * *`, `0 * * * *`, `0 */6 * * *`, `0 7 * * *`, and intervals of 5, 15, 30, 60, 720, or 1440 minutes.
    The day-of-month, month, and day-of-week fields only choose the days, so schedules such as `0 9 * * MON-FRI` and `0 9 1 * *` are allowed.
  - Rejected: `*/7 * * * *` (the gap from :56 to :00 is 4 minutes), `0,10,45 * * * *`, `0 */5 * * *`, `0 9-17 * * *` (one 16-hour overnight period
    among 1-hour periods), and `0 6,15 * * *`.

  The check applies when you associate the function, set or unset the schedule, and clone the table or create it with `CREATE TABLE ... LIKE`
  (the copy’s association is suspended). An association whose schedule comes from the database or account, or a table that you move to a schema
  with an uneven schedule, is suspended at its next evaluation. The other period-comparison functions accept any cron expression or interval.
- The time column must have the data type `TIMESTAMP_LTZ`, `TIMESTAMP_NTZ`, or `TIMESTAMP_TZ`, and it should hold the event time or the load time of the
  row. A `TIMESTAMP_NTZ` value is read as UTC, whatever the time zone of the schedule. If a `TIMESTAMP_NTZ` column holds local time, expose it through a view
  that converts it, for example with `CONVERT_TIMEZONE('<zone>', 'UTC', <column>)`. `DATE` columns aren’t supported, because every row would fall at midnight
  and land in the wrong period for any schedule that doesn’t fire at midnight UTC. If a table has no suitable time column, create a view that exposes a load timestamp.

**The current window and the baseline**

The number in the name of the function sets the *current window*: the last 1, 2, 4, or 8 periods. The *baseline* is a run of tiles immediately before
the current window. Each tile is as long as the current window, measured from the start of the current window to the time the evaluation was
scheduled for, so the tiles don’t have to line up with earlier fires of the schedule. The baseline has enough tiles to cover 14 days, rounded up to a
whole tile, and at least two tiles:

*number of tiles* = the larger of 2 and (14 days ÷ *length of the current window*, rounded up)

A short window therefore gets a baseline of about 14 days made of many tiles, and a long window gets a baseline of two tiles that is longer than 14 days:

| Schedule | Function suffix | Current window | Tiles | Baseline |
| --- | --- | --- | --- | --- |
| Every 5 minutes | `_LAST_PERIOD` | 5 minutes | 4,032 | 14 days |
| Hourly | `_LAST_PERIOD` | 1 hour | 336 | 14 days |
| Hourly | `_LAST_EIGHT_PERIODS` | 8 hours | 42 | 14 days |
| Daily | `_LAST_PERIOD` | 1 day | 14 | 14 days |
| Daily | `_LAST_TWO_PERIODS` | 2 days | 7 | 14 days |
| Daily | `_LAST_FOUR_PERIODS` | 4 days | 4 | 16 days |
| Daily | `_LAST_EIGHT_PERIODS` | 8 days | 2 | 16 days |
| Weekdays (`0 9 * * MON-FRI`), Monday run | `_LAST_PERIOD` | 3 days (Friday to Monday) | 5 | 15 days |
| Weekly | `_LAST_PERIOD` | 7 days | 2 | 14 days |
| Weekly | `_LAST_FOUR_PERIODS` | 28 days | 2 | 56 days |
| Monthly (`0 0 1 * *`), run on December 1 | `_LAST_PERIOD` | 30 days (November) | 2 | 60 days |
| Monthly (`0 0 1 * *`), run on December 1 | `_LAST_TWO_PERIODS` | 61 days (October and November) | 2 | 122 days |
| Monthly (`0 0 1 * *`), run on December 1 | `_LAST_FOUR_PERIODS` | 122 days (August to November) | 2 | 244 days |
| Monthly (`0 0 1 * *`), run on December 1 | `_LAST_EIGHT_PERIODS` | 244 days (April to November) | 2 | 488 days |

Expand

Show lessSee more

The table assumes a time zone without daylight saving time, such as UTC.

A monthly window is 28 to 31 days long, and its tiles are as long as the current window, not calendar months. On data that arrives at a steady
rate, the length of the month doesn’t affect the `_CHANGE` and `_CHANGE_PERCENT` functions, because the current window and each tile have the
same length. It affects two cases. If the table is loaded once a month, the tiles don’t line up with the loads, so a tile can contain no load or
two loads. `NEW_VALUE_COUNT` and `MISSING_VALUE_COUNT` compare the current window with the whole baseline, so their results can change with
the length of the month. Longer windows reduce both effects.

A long window needs a long history and reads a lot of data. The volume functions (described below) return `NULL` until the table has a row earlier
than one tile before the current window. For a monthly schedule with `_LAST_EIGHT_PERIODS`, that row must be about 16 months old, and every run
reads the current window and the baseline, about 2 years of data.

- The functions that return a change in a measurement (names that contain `_CHANGE`) cut the baseline into tiles as long as the current window,
  compute the measurement for each tile, and average the tiles. They compare the measurement in the current window with that average.
  - For the *volume functions*, which count rows or values or sum values (`ROW_COUNT_CHANGE`, `SUM_CHANGE`, `UNIQUE_COUNT_CHANGE`, `NULL_COUNT_CHANGE`,
    `ZERO_COUNT_CHANGE`, `NEGATIVE_COUNT_CHANGE`, and their `_PERCENT` forms), a tile with no data counts as 0, because no data is itself a signal,
    for example a load that stopped. The baseline runs back only to the oldest tile that has a row, so a young table has a shorter baseline, and the
    function returns `NULL` if that gives fewer than two tiles. The oldest tile counts in full even when the table’s data starts partway through it,
    so on a young table the baseline average can be lower than the real rate.
  - For the functions that measure a distribution (`AVG`, `MEDIAN`, `MIN`, `MAX`, `STDDEV`, and the `NULL_PERCENT`, `ZERO_PERCENT`, and
    `NEGATIVE_PERCENT` changes), tiles with no rows are skipped, because these measurements have no value on zero rows. The function returns `NULL` when the
    current window or the baseline has no rows, and for `AVG`, `MEDIAN`, `MIN`, `MAX`, and `STDDEV` also when it has no non-`NULL` values.
- `NEW_VALUE_COUNT`, `MISSING_VALUE_COUNT`, `PSI`, `JS_DIVERGENCE`, and `KS_TEST` pool all the rows of the baseline and compare them with the rows
  of the current window. They don’t cut the baseline into tiles, so the two-tile minimum of the volume functions doesn’t apply to them.
- A function with the suffix `_CHANGE_PERCENT` divides the difference by the absolute value of the baseline, so the sign of the result shows the
  direction of the change even when the baseline is negative. It returns `NULL` when the baseline value is 0. Because a scheduled evaluation
  records `NULL` as 0, the function can’t detect a change from a baseline of 0, such as `NULL` values appearing in a column that had none. To detect
  such a change, use the function with the suffix `_CHANGE`.

**Results when there isn’t enough data**

When a function returns `NULL`, for example for a new table, the scheduled evaluation records the result as 0, as for every data metric function. An expectation
such as `VALUE < 100` therefore passes on a table that has no history. `PSI`, `JS_DIVERGENCE`, and `KS_TEST` return `NULL` when the current window or the
baseline has fewer than 100 values that are not `NULL` or `NaN`.

**Value edge cases**

- `NaN` counts as `NULL` in every period-comparison function: aggregate functions skip it, and the `NULL` functions count it.
- A result that isn’t finite, for example a sum that overflows, is `NULL`.
- The values `-0.0` and `0.0` are the same value.
- `AVG`, `MEDIAN`, `MIN`, `MAX`, `STDDEV`, `SUM`, and `KS_TEST`, and the bins of `PSI` and `JS_DIVERGENCE` for numeric, `DATE`, and timestamp values,
  compute with the values as `FLOAT`, so integers larger than about 9e15 lose their lowest digits. The functions that count values compare the
  values as they are.

**Schedules and the load cadence**

The volume functions compare how much data arrived in the current window with the average of the baseline windows, and `NEW_VALUE_COUNT` and
`MISSING_VALUE_COUNT` count values over the whole current window. If the schedule doesn’t match how often the table is loaded, the results can
change from run to run even when the data doesn’t change.

- With a weekday-only schedule, such as `0 9 * * 1-5`, on a table that is loaded only on weekdays, the period that ends on Monday covers Friday to Monday
  (3 days), and its baseline uses 3-day tiles. The other days use 1-day tiles that include empty weekend days. With the same load every weekday,
  `ROW_COUNT_CHANGE_PERCENT_LAST_PERIOD` and `SUM_CHANGE_PERCENT_LAST_PERIOD` read high from Tuesday to Friday and low on Mondays, even though
  the data doesn’t change.
- Steps in the day-of-month field of a cron expression restart each month. For example, `0 0 */6 * *` fires on the 1st, 7th, 13th, 19th, 25th, and
  31st, so periods have different lengths at the end of a month.
- A daily schedule on a table that is quieter on weekends shows a drop on weekend days and a smaller rise on weekdays, because the baseline
  averages both kinds of day.
- Interval schedules, and evenly spaced cron expressions in a time zone without daylight saving time such as UTC, always compare periods
  of equal length. In a time zone with daylight saving time, a period that spans a clock change is an hour shorter or longer.
- When daylight saving time ends and a cron expression fires twice at the same local time, only the later fire is a period boundary. The window of the later
  run therefore also covers the hour of the earlier run.

For the volume functions, `NEW_VALUE_COUNT`, and `MISSING_VALUE_COUNT`, choose a schedule whose period is a multiple of the load cadence, such as
a weekly schedule for a weekly load, or choose a window that spans the cadence, such as `_LAST_TWO_PERIODS` or longer. The functions that measure a distribution aren’t affected by the load cadence,
because they skip empty tiles.

**Schedule changes**

An evaluation steps back on the grid of the schedule that started it. If a run starts late, after you changed the schedule, it still compares the periods it
was scheduled for, and the next run uses the new schedule. A late run fails after you suspend the association.

**Late-arriving rows**

A row whose time falls in a period that was already evaluated isn’t counted for that period. For `ROW_COUNT_CHANGE`, a column that holds the load time
measures arrivals more faithfully than a column that holds the event time.

**Governance policies**

A masking policy on the value column or the time column applies to the evaluation, so a policy that changes times moves rows between periods. A governance
policy that blocks the evaluation makes the evaluation fail, for example an aggregation policy, or a projection policy on the time column for the volume
functions (`ROW_COUNT_CHANGE`, `SUM_CHANGE`, `UNIQUE_COUNT_CHANGE`, `NULL_COUNT_CHANGE`, `ZERO_COUNT_CHANGE`,
`NEGATIVE_COUNT_CHANGE`, and their `_PERCENT` forms). The `ALTER TABLE` command doesn’t reject the association.

**Tables from a share**

A consumer can associate one of these functions with a table that is imported from a share. The imported table can’t have its own `DATA_METRIC_SCHEDULE`, so
its periods follow the schedule that it inherits in the consumer account.

**Cost**

These functions are serverless data metric functions like the others. They have no incremental maintenance: each run reads the current window and the
baseline, which is about 15 days of data for a daily schedule with `_LAST_PERIOD` and grows with the window (see the table in
[How the comparison works](/sql-reference/functions/dmf_zero_percent_change_percent_last_two_periods#label-period-dmf-how)). A run reads only that data if Snowflake can prune the table by the time column, for example when the table is
loaded or clustered in time order. Otherwise, a run can scan the whole table.

## Examples

Set a daily schedule on the table `sales.orders`, then associate the function with it and define an expectation that is violated when
fewer rows were loaded than the baseline average by more than 100:

Copy code

```
ALTER TABLE sales.orders SET
  DATA_METRIC_SCHEDULE = 'USING CRON 0 6 * * * UTC';

ALTER TABLE sales.orders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT_CHANGE_LAST_PERIOD
    ON (loaded_at)
    EXPECTATION row_volume_stable (VALUE >= -100);
```
