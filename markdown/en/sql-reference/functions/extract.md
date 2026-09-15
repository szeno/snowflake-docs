Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# EXTRACT

Extracts the specified date or time part from a date, interval, time, or timestamp.

Tip

To extract the date from a timestamp, use the [TO\_DATE](/sql-reference/functions/to_date) function.

Alternatives:
:   [DATE\_PART](/sql-reference/functions/date_part) , [HOUR / MINUTE / SECOND](/sql-reference/functions/hour-minute-second) , [YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER](/sql-reference/functions/year)

## Syntax

Copy code

```
EXTRACT( <date_or_time_part> FROM <date_interval_time_or_timestamp_expr> )
```

Copy code

```
EXTRACT( <date_or_time_part> , <date_interval_time_or_timestamp_expr> )
```

## Arguments

`date_or_time_part`
:   The unit of time. Must be one of the values listed in [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts) (for example, `month`).
    The value can be a string literal or can be unquoted (for example, `'month'` or `month`).

    - When `date_or_time_part` is `week` (or any of its variations), the output is controlled by the [WEEK\_START](/sql-reference/parameters#label-week-start) session parameter.
    - When `date_or_time_part` is `dayofweek` or `yearofweek` (or any of their variations), the output is controlled by the [WEEK\_OF\_YEAR\_POLICY](/sql-reference/parameters#label-week-of-year-policy) and [WEEK\_START](/sql-reference/parameters#label-week-start) session parameters.

    For more information, including examples, see [Calendar weeks and weekdays](/sql-reference/functions-date-time#label-calendar-weeks-weekdays).

`date_interval_time_or_timestamp_expr`
:   A date, an interval, a time, or a timestamp, or an expression that can be evaluated to one of those data types.

## Returns

Returns a value of NUMBER data type.

## Usage notes

- When `date_interval_time_or_timestamp_expr` is a year-month interval value, the supported
  `date_or_time_part` values are `year` and `month`.
- When `date_interval_time_or_timestamp_expr` is a day-time interval value, the supported
  `date_or_time_part` values are `day`, `hour`, `minute`, `second`, and `nanosecond`.
- Currently, when `date_interval_time_or_timestamp_expr` is a DATE value, the following `date_or_time_part`
  values aren’t supported:

  - `epoch_millisecond`
  - `epoch_microsecond`
  - `epoch_nanosecond`

  Other [date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts) (including `epoch_second`) are supported.

## Examples

Specify the `year` part to extract the year from a timestamp:

Copy code

```
SELECT EXTRACT(year FROM TO_TIMESTAMP('2024-04-10T23:39:20.123-07:00')) AS YEAR;
```

```
+------+
| YEAR |
|------|
| 2024 |
+------+
```

Use EXTRACT with the [DECODE](/sql-reference/functions/decode) function and the `dayofweek` part to return the full name of the
current day of the week:

Copy code

```
SELECT DECODE(EXTRACT(dayofweek FROM SYSTIMESTAMP()),
  1, 'Monday',
  2, 'Tuesday',
  3, 'Wednesday',
  4, 'Thursday',
  5, 'Friday',
  6, 'Saturday',
  7, 'Sunday') AS DAYOFWEEK;
```

```
+-----------+
| DAYOFWEEK |
|-----------|
| Thursday  |
+-----------+
```

Note

The output depends on the value returned by the [SYSTIMESTAMP](/sql-reference/functions/systimestamp) function when you run the query. Also, you can use the
[DAYNAME](/sql-reference/functions/dayname) function to extract the three-letter day-of-week name from the specified date or timestamp.
