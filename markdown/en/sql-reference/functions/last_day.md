Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# LAST\_DAY

Returns the last day of the specified date part for a date or timestamp. This function is commonly used to return the
last day of the month for a date or timestamp.

See also:
:   [NEXT\_DAY](/sql-reference/functions/next_day) , [PREVIOUS\_DAY](/sql-reference/functions/previous_day)

## Syntax

Copy code

```
LAST_DAY( <date_or_timestamp_expr> [ , <date_part> ] )
```

## Arguments

`date_or_timestamp_expr`
:   A date or a timestamp, or an expression that can be evaluated to a date or a timestamp.

`date_part`
:   The date part for which the last day is returned. Possible values are `year`, `quarter`, `month`,
    or `week` (or any of their supported variations). For more information, see [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts).

    When `date_part` is `week` (or any of its variations), the output is controlled by the [WEEK\_START](/sql-reference/parameters#label-week-start)
    session parameter. For more details, including examples, see [Calendar weeks and weekdays](/sql-reference/functions-date-time#label-calendar-weeks-weekdays).

    For more information, including examples, see [Calendar weeks and weekdays](/sql-reference/functions-date-time#label-calendar-weeks-weekdays).

    Default: `month`

## Returns

This function returns a value of type DATE, even if `date_or_timestamp_expr` is a timestamp.

## Examples

Return the last day of the month for the specified date (from a timestamp):

Copy code

```
SELECT TO_DATE('2025-05-08T23:39:20.123-07:00') AS "DATE",
       LAST_DAY("DATE") AS "LAST DAY OF MONTH";
```

```
+------------+-------------------+
| DATE       | LAST DAY OF MONTH |
|------------+-------------------|
| 2025-05-08 | 2025-05-31        |
+------------+-------------------+
```

Return the last day of the year for the specified date (from a timestamp):

Copy code

```
SELECT TO_DATE('2024-05-08T23:39:20.123-07:00') AS "DATE",
       LAST_DAY("DATE", 'year') AS "LAST DAY OF YEAR";
```

```
+------------+------------------+
| DATE       | LAST DAY OF YEAR |
|------------+------------------|
| 2024-05-08 | 2024-12-31       |
+------------+------------------+
```
