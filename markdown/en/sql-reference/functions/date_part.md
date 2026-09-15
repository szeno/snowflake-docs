Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# DATE\_PART

Extracts the specified date or time part from a date, time, or timestamp.

Alternatives:
:   [EXTRACT](/sql-reference/functions/extract) , [HOUR / MINUTE / SECOND](/sql-reference/functions/hour-minute-second) , [YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER](/sql-reference/functions/year)

## Syntax

Copy code

```
DATE_PART( <date_or_time_part> , <date_interval_time_or_timestamp_expr> )
```

Copy code

```
DATE_PART( <date_or_time_part> FROM <date_interval_time_or_timestamp_expr> )
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

Tip

To extract a full DATE or TIME value instead of a single part from a TIMESTAMP value, you can cast the
TIMESTAMP value to a DATE or TIME value, respectively. For example:

Copy code

```
SELECT '2025-04-08T23:39:20.123-07:00'::TIMESTAMP::DATE AS full_date_value;
```

```
+-----------------+
| FULL_DATE_VALUE |
|-----------------|
| 2025-04-08      |
+-----------------+
```

Copy code

```
SELECT '2025-04-08T23:39:20.123-07:00'::TIMESTAMP::TIME AS full_time_value;
```

```
+-----------------+
| FULL_TIME_VALUE |
|-----------------|
| 23:39:20        |
+-----------------+
```

## Examples

This shows a simple example of extracting part of a DATE:

Copy code

```
SELECT DATE_PART(quarter, '2024-04-08'::DATE);
```

```
+----------------------------------------+
| DATE_PART(QUARTER, '2024-04-08'::DATE) |
|----------------------------------------|
|                                      2 |
+----------------------------------------+
```

This shows an example of extracting part of a TIMESTAMP:

Copy code

```
SELECT TO_TIMESTAMP(
  '2024-04-08T23:39:20.123-07:00') AS "TIME_STAMP1",
  DATE_PART(year, "TIME_STAMP1") AS "EXTRACTED YEAR";
```

```
+-------------------------+----------------+
| TIME_STAMP1             | EXTRACTED YEAR |
|-------------------------+----------------|
| 2024-04-08 23:39:20.123 |           2024 |
+-------------------------+----------------+
```

This shows an example of converting a TIMESTAMP to the number of seconds since
the beginning of the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) (midnight January 1, 1970):

Copy code

```
SELECT TO_TIMESTAMP(
  '2024-04-08T23:39:20.123-07:00') AS "TIME_STAMP1",
  DATE_PART(epoch_second, "TIME_STAMP1") AS "EXTRACTED EPOCH SECOND";
```

```
+-------------------------+------------------------+
| TIME_STAMP1             | EXTRACTED EPOCH SECOND |
|-------------------------+------------------------|
| 2024-04-08 23:39:20.123 |             1712619560 |
+-------------------------+------------------------+
```

This shows an example of converting a TIMESTAMP to the number of milliseconds since
the beginning of the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) (midnight January 1, 1970):

Copy code

```
SELECT TO_TIMESTAMP(
  '2024-04-08T23:39:20.123-07:00') AS "TIME_STAMP1",
  DATE_PART(epoch_millisecond, "TIME_STAMP1") AS "EXTRACTED EPOCH MILLISECOND";
```

```
+-------------------------+-----------------------------+
| TIME_STAMP1             | EXTRACTED EPOCH MILLISECOND |
|-------------------------+-----------------------------|
| 2024-04-08 23:39:20.123 |               1712619560123 |
+-------------------------+-----------------------------+
```
