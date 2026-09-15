Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# TIME\_SLICE

Calculates the beginning or end of a “slice” of time, where the length of the slice is a multiple of a standard unit of time
(minute, hour, day, etc.).

This function can be used to calculate the start and end times of fixed-width “buckets” into which data can be categorized.

See also:
:   [DATE\_TRUNC](/sql-reference/functions/date_trunc)

## Syntax

Copy code

```
TIME_SLICE( <date_or_time_expr> , <slice_length> , <date_or_time_part> [ , <start_or_end> ] )
```

## Arguments

**Required:**

`date_or_time_expr`
:   The function returns the start or end of the slice that contains this date or time. The expression must
    be of type DATE or TIMESTAMP\_NTZ.

`slice_length`
:   This indicates the width of the slice (i.e. how many units of
    time are contained in the slice). For example, if the unit is MONTH and the `slice_length`
    is 2, then each slice is 2 months wide. The `slice_length` must be an integer
    greater than or equal to 1.

`date_or_time_part`
:   Time unit for the slice length. The value must be a string containing one of the values listed
    below:

    - If input expression is a DATE: YEAR, QUARTER, MONTH, WEEK, DAY.
    - If input expression is a TIMESTAMP\_NTZ: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND.

    The values are case-insensitive.

**Optional:**

`start_or_end`
:   This is an optional constant parameter that determines whether the start or end of the slice should be returned.

    Supported values are ‘START’ or ‘END’. The values are case-insensitive.

    The default value is ‘START’.

## Returns

The data type of the return value is identical to the data type of the input `date_or_time_expr`
(i.e. either TIMESTAMP\_NTZ or DATE).

## Usage notes

- All slices are aligned relative to midnight January 1, 1970 (1970-01-01 00:00:00).

  Most slices start on an integer multiple of the slice length relative to January 1, 1970. For example, if you choose
  a slice length of 15 years, then each slice will start on one of the following boundaries:

  - January 1, 1970.
  - January 1, 1985.
  - January 1, 2000.
  - January 1, 2015.
  - Etc.

  Dates prior to January 1, 1970 are also valid; for example, a 15-year slice can start on January 1, 1955.

  The one exception is that, for slices measured in weeks, the starts of the slices are aligned with the beginning of
  the week that contains January 1, 1970. January 1, 1970 was a Thursday. So, for example, if your
  [WEEK\_START](/sql-reference/parameters#label-week-start) session parameter specifies that your calendar weeks start on Monday, and if your slices
  are 2 weeks, then your slices will start on one of the following boundaries:

  - December 29, 1969 (Monday).
  - January 12, 1970 (Monday).
  - January 25, 1970 (Monday).
  - Etc.

  If your calendar weeks start on Sunday, then your slices will start on:

  - December 28, 1969 (Sunday).
  - January 11, 1970 (Sunday).
  - January 25, 1970 (Sunday).
  - Etc.

  For more details about how calendar weeks are handled, including examples, see [Calendar weeks and weekdays](/sql-reference/functions-date-time#label-calendar-weeks-weekdays).
- Although the parameters to TIME\_SLICE must be of type DATE or TIMESTAMP\_NTZ, you can use casting to process
  TIMESTAMP\_LTZ values. For TIMESTAMP\_LTZ values, cast the input to TIMESTAMP\_NTZ first and then cast back
  to TIMESTAMP\_LTZ. However, in this case, slices crossing daylight saving time boundaries can be either one hour
  longer or one hour shorter than slices that do not cross daylight saving time boundaries.
- The end of each slice is the same as the beginning of the following slice. For example, if the slice is
  2 months and the start of the slice is 2019-01-01, then the end of the slice will be 2019-03-01, not
  2019-02-28. In other words, the slice contains dates or timestamps greater than or equal to the start
  and less than (but not equal to) the end.

## Examples

Find the start and end of a 4-month slice containing a date:

> Copy code
>
> ```
> SELECT '2019-02-28'::DATE AS "DATE",
>        TIME_SLICE("DATE", 4, 'MONTH', 'START') AS "START OF SLICE",
>        TIME_SLICE("DATE", 4, 'MONTH', 'END') AS "END OF SLICE";
> +------------+----------------+--------------+
> | DATE       | START OF SLICE | END OF SLICE |
> |------------+----------------+--------------|
> | 2019-02-28 | 2019-01-01     | 2019-05-01   |
> +------------+----------------+--------------+
> ```

Find the start of 8-hour slices corresponding to two timestamps:

> Copy code
>
> ```
> SELECT '2019-02-28T01:23:45.678'::TIMESTAMP_NTZ AS "TIMESTAMP 1",
>        '2019-02-28T12:34:56.789'::TIMESTAMP_NTZ AS "TIMESTAMP 2",
>        TIME_SLICE("TIMESTAMP 1", 8, 'HOUR') AS "SLICE FOR TIMESTAMP 1",
>        TIME_SLICE("TIMESTAMP 2", 8, 'HOUR') AS "SLICE FOR TIMESTAMP 2";
> +-------------------------+-------------------------+-------------------------+-------------------------+
> | TIMESTAMP 1             | TIMESTAMP 2             | SLICE FOR TIMESTAMP 1   | SLICE FOR TIMESTAMP 2   |
> |-------------------------+-------------------------+-------------------------+-------------------------|
> | 2019-02-28 01:23:45.678 | 2019-02-28 12:34:56.789 | 2019-02-28 00:00:00.000 | 2019-02-28 08:00:00.000 |
> +-------------------------+-------------------------+-------------------------+-------------------------+
> ```

Group data into “buckets” based on the date or timestamp (e.g. group data into buckets that are two weeks wide):

> This example uses the table and data created below:
>
> Copy code
>
> ```
> CREATE TABLE accounts (ID INT, billing_date DATE, balance_due NUMBER(11, 2));
>
> INSERT INTO accounts (ID, billing_date, balance_due) VALUES
>     (1, '2018-07-31', 100.00),
>     (2, '2018-08-01', 200.00),
>     (3, '2018-08-25', 400.00);
> ```
>
> This query shows the bucketed data:
>
> Copy code
>
> ```
> SELECT
>        TIME_SLICE(billing_date, 2, 'WEEK', 'START') AS "START OF SLICE",
>        TIME_SLICE(billing_date, 2, 'WEEK', 'END')   AS "END OF SLICE",
>        COUNT(*) AS "NUMBER OF LATE BILLS",
>        SUM(balance_due) AS "SUM OF MONEY OWED"
>     FROM accounts
>     WHERE balance_due > 0    -- bill hasn't yet been paid
>     GROUP BY "START OF SLICE", "END OF SLICE";
> +----------------+--------------+----------------------+-------------------+
> | START OF SLICE | END OF SLICE | NUMBER OF LATE BILLS | SUM OF MONEY OWED |
> |----------------+--------------+----------------------+-------------------|
> | 2018-07-23     | 2018-08-06   |                    2 |            300.00 |
> | 2018-08-20     | 2018-09-03   |                    1 |            400.00 |
> +----------------+--------------+----------------------+-------------------+
> ```
>
> Note that the GROUP BY clause needs both the start of the slice and the end of the slice because the compiler
> expects the GROUP BY clause to contain all non-aggregate expressions of the projection clause.
