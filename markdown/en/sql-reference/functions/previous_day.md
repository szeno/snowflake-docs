Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# PREVIOUS\_DAY

Returns the date of the first specified day of week (DOW) that occurs before the input date.

See also:
:   [LAST\_DAY](/sql-reference/functions/last_day) , [NEXT\_DAY](/sql-reference/functions/next_day)

## Syntax

Copy code

```
PREVIOUS_DAY( <date_or_timestamp_expr> , <dow> )
```

## Arguments

`date_or_timestamp_expr`
:   A date or a timestamp, or an expression that can be evaluated to a date or a timestamp.

`dow_string`
:   Specifies the day of week used to calculate the date for the previous day. The value can be a string literal or an expression that returns a string. The string
    must start with the first two characters (case-insensitive) of the day name:

    > - `su` (Sunday)
    > - `mo` (Monday)
    > - `tu` (Tuesday)
    > - `we` (Wednesday)
    > - `th` (Thursday)
    > - `fr` (Friday)
    > - `sa` (Saturday)

    Any leading spaces and trailing characters, including spaces, in the string are ignored.

## Returns

This function returns a value of type DATE, even if `date_or_timestamp_expr` is a timestamp.

## Examples

Return the date of the previous Friday that occurred before the current date:

Copy code

```
SELECT CURRENT_DATE() AS "Today's Date",
       PREVIOUS_DAY("Today's Date", 'Friday') AS "Previous Friday";
```

```
+--------------+-----------------+
| Today's Date | Previous Friday |
|--------------+-----------------|
| 2025-05-06   | 2025-05-02      |
+--------------+-----------------+
```

Your output will be different because the example uses the [CURRENT\_DATE](/sql-reference/functions/current_date) function.
