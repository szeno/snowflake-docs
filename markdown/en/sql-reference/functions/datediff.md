Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# DATEDIFF

Calculates the difference between two date, time, or timestamp expressions based on the date or time part requested.
The function returns the result of subtracting the second argument from the third argument.

Note

Difference calculations compare the specified date or time part, not the complete date or time. For example, the month
difference between November 28, 2024 and December 5, 2024 is 1, because the difference between the two months November
and December, both in 2024, is 1. To reflect the fact that the difference between the two dates is less than a full
month, calculate the difference in days instead.

You can also use the minus sign (`-`) to calculate the difference between two dates by subtracting one date from
another.

To add units of time to a date, time, or timestamp (for example, add two days to a date) or subtract units of time
from them, you can use the [DATEADD](/sql-reference/functions/dateadd), [TIMEADD](/sql-reference/functions/timeadd), or [TIMESTAMPADD](/sql-reference/functions/timestampadd) function.

See also:
:   [TIMEDIFF](/sql-reference/functions/timediff) , [TIMESTAMPDIFF](/sql-reference/functions/timestampdiff)

## Syntax

**For DATEDIFF:**

Copy code

```
DATEDIFF( <date_or_time_part>, <date_or_time_expr1>, <date_or_time_expr2> )
```

**For minus sign:**

Copy code

```
<date_expr2> - <date_expr1>
```

## Arguments

**For DATEDIFF:**

`date_or_time_part`
:   The unit of time. Must be one of the values listed in [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts) (for example, `month`).
    The value can be a string literal or can be unquoted (for example, `'month'` or `month`).

`date_or_time_expr1`, `date_or_time_expr2`
:   The values to compare. Must be a date, a time, a timestamp, or an expression that can be evaluated to
    a date, a time, or a timestamp. The value `date_or_time_expr1` is subtracted from
    `date_or_time_expr2`.

**For minus sign:**

`date_expr1`, `date_expr2`
:   The values to compare. Must be a date, or an expression that can be evaluated to a date. The value `date_expr1` is
    subtracted from `date_expr2`.

## Returns

**For DATEDIFF:**

Returns an integer representing the difference in the number of units (seconds, days, and so on) between `date_or_time_expr2` and
`date_or_time_expr1`.

Returns NULL if any argument is NULL.

**For minus sign:**

Returns an integer representing the number of days difference between `date_expr2` and
`date_expr1`. (The units are always days.)

Returns an error if `date_expr2` or `date_expr1` is NULL.

## Usage notes

**For both DATEDIFF and minus sign:**

- Output values can be negative, for example, -12 days.

**For DATEDIFF:**

- The function supports units of years, quarters, months, weeks, days, hours, minutes, seconds, milliseconds, microseconds, and nanoseconds.
- If `date_or_time_part` is `week` (or any of its variations), the output is controlled by the [WEEK\_START](/sql-reference/parameters#label-week-start) session parameter. For more details, including examples, see
  [Calendar weeks and weekdays](/sql-reference/functions-date-time#label-calendar-weeks-weekdays).
- The unit (for example, `month`) used to calculate the difference determines which parts of the DATE, TIME, or TIMESTAMP field are
  evaluated. So, the unit determines the precision of the result.

  Smaller units are not used, so values are not rounded. For example, even though the difference between January 1, 2021 and
  February 28, 2021 is closer to two months than to one month, the following returns one month:

  Copy code

  ```
  DATEDIFF(month, '2021-01-01'::DATE, '2021-02-28'::DATE)
  ```

  For a DATE value:

> - `year` uses only the year and disregards all the other parts.
> - `month` uses the month and year.
> - `day` uses the entire date.

For a TIME value:

> - `hour` uses only the hour and disregards all the other parts.
> - `minute` uses the hour and minute.
> - `second` uses the hour, minute, and second, but not the fractional seconds.
> - `millisecond` uses the hour, minute, second, and first three digits of the fractional seconds. Fractional
>   seconds are not rounded. For example, `DATEDIFF(milliseconds, '2024-02-20 21:18:41.0000', '2024-02-20 21:18:42.1239')` returns 1.123 seconds,
>   not 1.124 seconds.
> - `microsecond` uses the hour, minute, second, and first six digits of the fractional seconds. Fractional
>   seconds are not rounded.
> - `nanosecond` uses the hour, minute, second, and all nine digits of the fractional seconds.

For a TIMESTAMP value:

> The rules match the rules for DATE and TIME data types above. Only the specified unit and larger units are used.

**For minus sign:**

- `date_expr1` and `date_expr2` must both be dates. Times and timestamps are not allowed.

## Examples

Calculate the difference in years between two timestamps:

Copy code

```
SELECT DATEDIFF(year, 
                '2020-04-09 14:39:20'::TIMESTAMP, 
                '2023-05-08 23:39:20'::TIMESTAMP) 
  AS diff_years;
```

```
+------------+
| DIFF_YEARS |
|------------|
|          3 |
+------------+
```

Calculate the difference in hours between two timestamps:

Copy code

```
SELECT DATEDIFF(hour, 
               '2023-05-08T23:39:20.123-07:00'::TIMESTAMP, 
               DATEADD(year, 2, ('2023-05-08T23:39:20.123-07:00')::TIMESTAMP)) 
  AS diff_hours;
```

```
+------------+
| DIFF_HOURS |
|------------|
|      17544 |
+------------+
```

Demonstrate how date parts affect DATEDIFF calculations; also, demonstrate use of the minus sign for date
subtraction:

Copy code

```
SELECT column1 date_1, column2 date_2,
       DATEDIFF(year, column1, column2) diff_years,
       DATEDIFF(month, column1, column2) diff_months,
       DATEDIFF(day, column1, column2) diff_days,
       column2::DATE - column1::DATE AS diff_days_via_minus
  FROM VALUES
       ('2015-12-30', '2015-12-31'),
       ('2015-12-31', '2016-01-01'),
       ('2016-01-01', '2017-12-31'),
       ('2016-08-23', '2016-09-07');
```

```
+------------+------------+------------+-------------+-----------+---------------------+
| DATE_1     | DATE_2     | DIFF_YEARS | DIFF_MONTHS | DIFF_DAYS | DIFF_DAYS_VIA_MINUS |
|------------+------------+------------+-------------+-----------+---------------------|
| 2015-12-30 | 2015-12-31 |          0 |           0 |         1 |                   1 |
| 2015-12-31 | 2016-01-01 |          1 |           1 |         1 |                   1 |
| 2016-01-01 | 2017-12-31 |          1 |          23 |       730 |                 730 |
| 2016-08-23 | 2016-09-07 |          0 |           1 |        15 |                  15 |
+------------+------------+------------+-------------+-----------+---------------------+
```

Demonstrate how time parts affect DATEDIFF calculations:

Copy code

```
ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT = 'DY, DD MON YYYY HH24:MI:SS';
```

Copy code

```
SELECT column1 timestamp_1, column2 timestamp_2,
       DATEDIFF(hour, column1, column2) diff_hours,
       DATEDIFF(minute, column1, column2) diff_minutes,
       DATEDIFF(second, column1, column2) diff_seconds
  FROM VALUES
       ('2016-01-01 01:59:59'::TIMESTAMP, '2016-01-01 02:00:00'::TIMESTAMP),
       ('2016-01-01 01:00:00'::TIMESTAMP, '2016-01-01 01:59:00'::TIMESTAMP),
       ('2016-01-01 01:00:59'::TIMESTAMP, '2016-01-01 02:00:00'::TIMESTAMP);
```

```
+---------------------------+---------------------------+------------+--------------+--------------+
| TIMESTAMP_1               | TIMESTAMP_2               | DIFF_HOURS | DIFF_MINUTES | DIFF_SECONDS |
|---------------------------+---------------------------+------------+--------------+--------------|
| Fri, 01 Jan 2016 01:59:59 | Fri, 01 Jan 2016 02:00:00 |          1 |            1 |            1 |
| Fri, 01 Jan 2016 01:00:00 | Fri, 01 Jan 2016 01:59:00 |          0 |           59 |         3540 |
| Fri, 01 Jan 2016 01:00:59 | Fri, 01 Jan 2016 02:00:00 |          1 |           60 |         3541 |
+---------------------------+---------------------------+------------+--------------+--------------+
```

Use the [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) function with the DATEDIFF function to
calculate the difference in years, months, and days between a specified timestamp and the
current timestamp:

Copy code

```
SELECT column1 specified_timestamp,
       column2 timestamp_now,
       DATEDIFF(year, column1, column2) diff_years,
       DATEDIFF(month, column1, column2) diff_months,
       DATEDIFF(day, column1, column2) diff_days,
       column2::DATE - column1::DATE AS diff_days_via_minus
  FROM VALUES
    ('2012-08-23 09:00:00.000 -0700', CURRENT_TIMESTAMP);
```

```
+-------------------------------+-------------------------------+------------+-------------+-----------+---------------------+
| SPECIFIED_TIMESTAMP           | TIMESTAMP_NOW                 | DIFF_YEARS | DIFF_MONTHS | DIFF_DAYS | DIFF_DAYS_VIA_MINUS |
|-------------------------------+-------------------------------+------------+-------------+-----------+---------------------|
| 2012-08-23 09:00:00.000 -0700 | 2024-09-04 17:21:12.189 -0700 |         12 |         145 |      4395 |                4395 |
+-------------------------------+-------------------------------+------------+-------------+-----------+---------------------+
```
