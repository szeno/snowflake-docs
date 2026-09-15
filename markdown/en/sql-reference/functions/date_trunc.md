Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# DATE\_TRUNC

Truncates a DATE, TIME, or TIMESTAMP value to the specified precision. For example,
truncating a timestamp down to the quarter returns the timestamp corresponding
to midnight of the first day of the original timestamp’s quarter.

This function provides an alternative syntax for [TRUNCATE, TRUNC](/sql-reference/functions/trunc2) by reversing the
two arguments.

Truncation is not the same as extraction. For example:

- Truncating a timestamp down to the quarter using this function returns the timestamp corresponding
  to midnight of the first day of the quarter for the input timestamp.
- Extracting the quarter date part from a timestamp using the [Extract](extract) function returns the
  quarter number of the year in the timestamp.

Alternatives:
:   [TRUNCATE, TRUNC](/sql-reference/functions/trunc2)

See also:
:   [DATE\_PART](/sql-reference/functions/date_part) , [EXTRACT](/sql-reference/functions/extract)

## Syntax

Copy code

```
DATE_TRUNC( <date_or_time_part>, <date_or_time_expr> )
```

## Arguments

`date_or_time_part`
:   This argument must be one of the values listed in [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts).

`date_or_time_expr`
:   This argument must evaluate to a date, time, or timestamp.

## Returns

The returned value is the same type as the input value.

For example, if the input value is a TIMESTAMP, then the returned value is a TIMESTAMP.

## Usage notes

- When `date_or_time_part` is `week` (or any of its variations), the output is controlled
  by the [WEEK\_START](/sql-reference/parameters#label-week-start) session parameter. For more details, including examples, see
  [Calendar weeks and weekdays](/sql-reference/functions-date-time#label-calendar-weeks-weekdays).
- For TIME values, you can’t specify a `date_or_time_part` that is outside the scope of the TIME type.
  For example, you can truncate a TIMESTAMP value to a `day`, `week`, `year`, and so on because the TIMESTAMP type
  encodes date/times with the required precision. However, trying to truncate a TIME value to a `day`, `week`, `year`,
  and so on causes an error.

## Examples

The DATE\_TRUNC function examples use the data in the following table:

Copy code

```
CREATE OR REPLACE TABLE test_date_trunc (
 mydate DATE,
 mytime TIME,
 mytimestamp TIMESTAMP);

INSERT INTO test_date_trunc VALUES (
  '2024-05-09',
  '08:50:48',
  '2024-05-09 08:50:57.891 -0700');

SELECT * FROM test_date_trunc;
```

```
+------------+----------+-------------------------+
| MYDATE     | MYTIME   | MYTIMESTAMP             |
|------------+----------+-------------------------|
| 2024-05-09 | 08:50:48 | 2024-05-09 08:50:57.891 |
+------------+----------+-------------------------+
```

The following examples show date truncation. In all cases, the returned value
is of the same data type as the input value, but with zeros for the portions,
such as fractional seconds, that were truncated.

Truncate a date down to the year, month, and day:

Copy code

```
SELECT mydate AS "DATE",
       DATE_TRUNC('year', mydate) AS "TRUNCATED TO YEAR",
       DATE_TRUNC('month', mydate) AS "TRUNCATED TO MONTH",
       DATE_TRUNC('week', mydate) AS "TRUNCATED TO WEEK",
       DATE_TRUNC('day', mydate) AS "TRUNCATED TO DAY"
  FROM test_date_trunc;
```

```
+------------+-------------------+--------------------+-------------------+------------------+
| DATE       | TRUNCATED TO YEAR | TRUNCATED TO MONTH | TRUNCATED TO WEEK | TRUNCATED TO DAY |
|------------+-------------------+--------------------+-------------------+------------------|
| 2024-05-09 | 2024-01-01        | 2024-05-01         | 2024-05-06        | 2024-05-09       |
+------------+-------------------+--------------------+-------------------+------------------+
```

Truncate a time down to the minute:

Copy code

```
SELECT mytime AS "TIME",
       DATE_TRUNC('minute', mytime) AS "TRUNCATED TO MINUTE"
  FROM test_date_trunc;
```

```
+----------+---------------------+
| TIME     | TRUNCATED TO MINUTE |
|----------+---------------------|
| 08:50:48 | 08:50:00            |
+----------+---------------------+
```

Truncate a TIMESTAMP down to the hour, minute, and second:

Copy code

```
SELECT mytimestamp AS "TIMESTAMP",
       DATE_TRUNC('hour', mytimestamp) AS "TRUNCATED TO HOUR",
       DATE_TRUNC('minute', mytimestamp) AS "TRUNCATED TO MINUTE",
       DATE_TRUNC('second', mytimestamp) AS "TRUNCATED TO SECOND"
  FROM test_date_trunc;
```

```
+-------------------------+-------------------------+-------------------------+-------------------------+
| TIMESTAMP               | TRUNCATED TO HOUR       | TRUNCATED TO MINUTE     | TRUNCATED TO SECOND     |
|-------------------------+-------------------------+-------------------------+-------------------------|
| 2024-05-09 08:50:57.891 | 2024-05-09 08:00:00.000 | 2024-05-09 08:50:00.000 | 2024-05-09 08:50:57.000 |
+-------------------------+-------------------------+-------------------------+-------------------------+
```

Contrast the DATE\_TRUNC function with the [EXTRACT](/sql-reference/functions/extract) function:

Copy code

```
SELECT DATE_TRUNC('quarter', mytimestamp) AS "TRUNCATED",
       EXTRACT('quarter', mytimestamp) AS "EXTRACTED"
  FROM test_date_trunc;
```

```
+-------------------------+-----------+
| TRUNCATED               | EXTRACTED |
|-------------------------+-----------|
| 2024-04-01 00:00:00.000 |         2 |
+-------------------------+-----------+
```
