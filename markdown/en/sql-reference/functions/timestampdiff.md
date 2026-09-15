Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# TIMESTAMPDIFF

Calculates the difference between two date, time, or timestamp expressions based on the specified date or time part.
The function returns the result of subtracting the second argument from the third argument.

Alternative for [DATEDIFF](/sql-reference/functions/datediff).

## Syntax

Copy code

```
TIMESTAMPDIFF( <date_or_time_part> , <date_or_time_expr1> , <date_or_time_expr2> )
```

## Arguments

`date_or_time_part`
:   The unit of time. Must be one of the values listed in [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts) (for example, `month`).
    The value can be a string literal or can be unquoted (for example, `'month'` or `month`).

`date_or_time_expr1`, `date_or_time_expr2`
:   The values to compare. Must be a date, a time, a timestamp, or an expression that can be evaluated to
    a date, a time, or a timestamp. The value `date_or_time_expr1` is subtracted from
    `date_or_time_expr2`.

## Returns

Returns an integer representing the number of units (seconds, days, etc.) difference between `date_or_time_expr2` and
`date_or_time_expr1`.

## Usage notes

- Output values can be negative, for example, -12 days.

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

## Examples

For example(s), see [DATEDIFF](/sql-reference/functions/datediff). (DATEDIFF, TIMEDIFF, and TIMESTAMPDIFF all use the same basic format.)
