Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# TRUNCATE, TRUNC

Truncates a DATE, TIME, or TIMESTAMP value to the specified precision. For example,
truncating a timestamp down to the quarter returns the timestamp corresponding
to midnight of the first day of the original timestamp’s quarter.

This function provides an alternative syntax for [DATE\_TRUNC](/sql-reference/functions/date_trunc) by reversing the
two arguments.

The TRUNCATE and TRUNC functions are synonymous.

Truncation is not the same as extraction. For example:

- Truncating a timestamp down to the quarter using this function returns the timestamp corresponding
  to midnight of the first day of the quarter for the input timestamp.
- Extracting the quarter date part from a timestamp using the [Extract](extract) function returns the
  quarter number of the year in the timestamp.

Note

TRUNC is overloaded. It can also be used with numeric values to [reduce the number of significant digits](/sql-reference/functions/trunc),
such as by truncating a decimal value to an integer. The numeric TRUNC has one required and one optional parameter.
The date/time TRUNC has two required parameters.

Alternatives:
:   [DATE\_TRUNC](/sql-reference/functions/date_trunc)

See also:
:   [DATE\_PART](/sql-reference/functions/date_part) , [EXTRACT](/sql-reference/functions/extract)

## Syntax

Copy code

```
TRUNC( <date_or_time_expr>, <date_or_time_part> )
```

## Arguments

`date_or_time_expr`
:   This argument must evaluate to a date, time, or timestamp.

`date_or_time_part`
:   This argument must be one of the values listed in [Supported date and time parts](/sql-reference/functions-date-time#label-supported-date-time-parts).

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

The following examples demonstrate the TRUNC or TRUNCATE function for date/time values.
For examples of truncating numeric values, see [the numeric form of TRUNC](/sql-reference/functions/trunc).

The function examples use the data in the following table:

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

Truncate a DATE value down to the year, month, and day:

Copy code

```
SELECT mydate AS "DATE",
       TRUNC(mydate, 'year') AS "TRUNCATED TO YEAR",
       TRUNC(mydate, 'month') AS "TRUNCATED TO MONTH",
       TRUNC(mydate, 'day') AS "TRUNCATED TO DAY"
  FROM test_date_trunc;
```

```
+------------+-------------------+--------------------+------------------+
| DATE       | TRUNCATED TO YEAR | TRUNCATED TO MONTH | TRUNCATED TO DAY |
|------------+-------------------+--------------------+------------------|
| 2024-05-09 | 2024-01-01        | 2024-05-01         | 2024-05-09       |
+------------+-------------------+--------------------+------------------+
```

Truncate a TIME value down to the minute:

Copy code

```
SELECT mytime AS "TIME",
       TRUNCATE(mytime, 'minute') AS "TRUNCATED TO MINUTE"
  FROM test_date_trunc;
```

```
+----------+---------------------+
| TIME     | TRUNCATED TO MINUTE |
|----------+---------------------|
| 08:50:48 | 08:50:00            |
+----------+---------------------+
```

Truncate a TIMESTAMP value down to the hour, minute, and second:

Copy code

```
SELECT mytimestamp AS "TIMESTAMP",
       TRUNCATE(mytimestamp, 'hour') AS "TRUNCATED TO HOUR",
       TRUNCATE(mytimestamp, 'minute') AS "TRUNCATED TO MINUTE",
       TRUNCATE(mytimestamp, 'second') AS "TRUNCATED TO SECOND"
  FROM test_date_trunc;
```

```
+-------------------------+-------------------------+-------------------------+-------------------------+
| TIMESTAMP               | TRUNCATED TO HOUR       | TRUNCATED TO MINUTE     | TRUNCATED TO SECOND     |
|-------------------------+-------------------------+-------------------------+-------------------------|
| 2024-05-09 08:50:57.891 | 2024-05-09 08:00:00.000 | 2024-05-09 08:50:00.000 | 2024-05-09 08:50:57.000 |
+-------------------------+-------------------------+-------------------------+-------------------------+
```

Contrast the TRUNC function with the [EXTRACT](/sql-reference/functions/extract) function:

Copy code

```
SELECT TRUNC(mytimestamp, 'quarter') AS "TRUNCATED",
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
