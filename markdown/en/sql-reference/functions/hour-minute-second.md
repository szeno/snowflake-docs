Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# HOUR / MINUTE / SECOND

Extracts the corresponding time part from a time, interval, or timestamp value.

These functions are alternatives to using the [DATE\_PART](/sql-reference/functions/date_part) (or [EXTRACT](/sql-reference/functions/extract)) function with the
equivalent time part (see [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts)).

See also:
:   [YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER](/sql-reference/functions/year)

## Syntax

Copy code

```
HOUR( <time_interval_or_timestamp_expr> )

MINUTE( <time_interval_or_timestamp_expr> )

SECOND( <time_interval_or_timestamp_expr> )
```

## Arguments

`time_interval_or_timestamp_expr`
:   A time, an interval, or a timestamp, or an expression that can be evaluated to one of those data types.
    An interval argument must be a day and time interval, not a year and month interval.

## Returns

This function returns a value of type NUMBER.

## Usage notes

Tip

To extract a full TIME value from a TIMESTAMP value instead of a part, you can cast the
TIMESTAMP value to a TIME value. For example:

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

This example demonstrates the HOUR, MINUTE, and SECOND functions:

Copy code

```
SELECT '2025-04-08T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       HOUR(tstamp) AS "HOUR",
       MINUTE(tstamp) AS "MINUTE",
       SECOND(tstamp) AS "SECOND";
```

```
+-------------------------+------+--------+--------+
| TSTAMP                  | HOUR | MINUTE | SECOND |
|-------------------------+------+--------+--------|
| 2025-04-08 23:39:20.123 |   23 |     39 |     20 |
+-------------------------+------+--------+--------+
```

For more examples, see [Working with date and time values](/sql-reference/date-time-examples).
