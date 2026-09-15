Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# TIMEADD

Adds the specified value for the specified date or time part to a date, time, or timestamp.

Alias for [DATEADD](/sql-reference/functions/dateadd).

## Syntax

Copy code

```
TIMEADD( <date_or_time_part> , <value> , <date_or_time_expr> )
```

# Arguments

`date_or_time_part`
:   This indicates the units of time that you want to add. For example if you
    want to add two days, then specify `day`. This unit of measure must
    be one of the values listed in [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts).

`value`
:   This is the number of units of time that you want to add. For example,
    if the units of time is `day`, and you want to add two days, specify `2`.
    If you want to subtract two days, specify `-2`.

`date_or_time_expr`
:   `date_or_time_expr` must evaluate to a date, time, or timestamp.
    This is the date, time, or timestamp to which you want to add.
    For example, if you want to add two days to August 1, 2024, then specify
    `'2024-08-01'::DATE`.

    If the data type is TIME, then the `date_or_time_part`
    must be in units of hours or smaller, not days or bigger.

    If the input data type is DATE, and the `date_or_time_part` is hours
    or smaller, the input value will not be rejected, but instead will be
    treated as a TIMESTAMP with hours, minutes, seconds, and fractions of
    a second all initially set to 0 (e.g. midnight on the specified date).

## Returns

If `date_or_time_expr` is a time, then the return data type is a time.

If `date_or_time_expr` is a timestamp, then the return data type is a timestamp.

If `date_or_time_expr` is a date:

> - If `date_or_time_part` is `day` or larger (for example, `month`, `year`),
>   the function returns a DATE value.
> - If `date_or_time_part` is smaller than a day (for example, `hour`, `minute`,
>   `second`), the function returns a TIMESTAMP\_NTZ value, with `00:00:00.000` as the starting
>   time for the date.

## Usage notes

When `date_or_time_part` is `year`, `quarter`, or `month` (or any of their variations),
if the result month has fewer days than the original day of the month, the result day of the month might
be different from the original day.

## Examples

The TIMEADD and TIMESTAMPADD functions are aliases for the DATEADD function. You can use any of these three
functions in the examples to return the same results.

Add years to a date:

Copy code

```
SELECT TO_DATE('2022-05-08') AS original_date,
       DATEADD(year, 2, TO_DATE('2022-05-08')) AS date_plus_two_years;
```

```
+---------------+---------------------+
| ORIGINAL_DATE | DATE_PLUS_TWO_YEARS |
|---------------+---------------------|
| 2022-05-08    | 2024-05-08          |
+---------------+---------------------+
```

Subtract years from a date:

Copy code

```
SELECT TO_DATE('2022-05-08') AS original_date,
       DATEADD(year, -2, TO_DATE('2022-05-08')) AS date_minus_two_years;
```

```
+---------------+----------------------+
| ORIGINAL_DATE | DATE_MINUS_TWO_YEARS |
|---------------+----------------------|
| 2022-05-08    | 2020-05-08           |
+---------------+----------------------+
```

Add two years and two hours to a date. First, set the timestamp output format, create a table,
and insert data:

Copy code

```
ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF9';
CREATE TABLE datetest (d date);
INSERT INTO datetest VALUES ('2022-04-05');
```

Run a query that adds two years and two hours to a date:

Copy code

```
SELECT d AS original_date,
       DATEADD(year, 2, d) AS date_plus_two_years,
       TO_TIMESTAMP(d) AS original_timestamp,
       DATEADD(hour, 2, d) AS timestamp_plus_two_hours
  FROM datetest;
```

```
+---------------+---------------------+-------------------------+--------------------------+
| ORIGINAL_DATE | DATE_PLUS_TWO_YEARS | ORIGINAL_TIMESTAMP      | TIMESTAMP_PLUS_TWO_HOURS |
|---------------+---------------------+-------------------------+--------------------------|
| 2022-04-05    | 2024-04-05          | 2022-04-05 00:00:00.000 | 2022-04-05 02:00:00.000  |
+---------------+---------------------+-------------------------+--------------------------+
```

Add a month to a date in a month with the same or more days than the
resulting month. For example, if the date is January 31, adding a month should not
return February 31.

Copy code

```
SELECT DATEADD(month, 1, '2023-01-31'::DATE) AS date_plus_one_month;
```

```
+---------------------+
| DATE_PLUS_ONE_MONTH |
|---------------------|
| 2023-02-28          |
+---------------------+
```

Add a month to a date in a month with fewer days than the resulting month.
Adding a month to February 28 returns March 28.

Copy code

```
SELECT DATEADD(month, 1, '2023-02-28'::DATE) AS date_plus_one_month;
```

```
+---------------------+
| DATE_PLUS_ONE_MONTH |
|---------------------|
| 2023-03-28          |
+---------------------+
```

Add hours to a time:

Copy code

```
SELECT TO_TIME('05:00:00') AS original_time,
       DATEADD(hour, 3, TO_TIME('05:00:00')) AS time_plus_three_hours;
```

```
+---------------+-----------------------+
| ORIGINAL_TIME | TIME_PLUS_THREE_HOURS |
|---------------+-----------------------|
| 05:00:00      | 08:00:00              |
+---------------+-----------------------+
```
