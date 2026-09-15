# Code Conversion - General Function References

## INTERVAL\_MULTIPLY\_UDF (VARCHAR, VARCHAR, INTEGER)

### Definition

This user-defined function (UDF) is used to multiply a time interval by a factor of N.

Copy code

```
:force:
INTERVAL_MULTIPLY_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR(), INPUT_MULT INTEGER)
```

### Parameters

`INPUT_PART` VARCHAR

The format of the operation. For example: `DAY`, `HOUR TO SECOND`, `YEAR TO MONTH`.

`INPUT_VALUE` VARCHAR

The interval of time to be multiplied.

`INPUT_MULT` INTEGER

The factor by which to multiply the interval.

### Returns

Returns a varchar with the result of the multiplication.

### Usage example

Input:

Copy code

```
:force:
SELECT INTERVAL_MULTIPLY_UDF('DAY', '2', 100);
```

Output:

Copy code

```
:force:
200
```

## TRUNC\_UDF (TIMESTAMP\_LTZ, VARCHAR)

### Definition

This user-defined function (UDF) reproduces the Teradata and Oracle TRUNC(Date) functionality when the format parameter is specified.

Copy code

```
:force:
TRUNC_UDF(DATE_TO_TRUNC TIMESTAMP_LTZ, DATE_FMT VARCHAR(5))
```

### Parameters

`DATE_TO_TRUNC` TIMESTAMP\_LTZ

A `timestamp_ltz` value to truncate which must be a date, timestamp, or timestamp with timezone.

`DATE_FMT` VARCHAR

A varchar value that should be one of the date formats supported by the `trunc` function.

### Returns

Returns a date truncated using the format specified.

### Usage example

Input:

Copy code

```
:force:
SELECT TRUNC_UDF(TIMESTAMP '2015-08-18 12:30:00', 'Q')
```

Output:

Copy code

```
:force:
2015-07-01
```

## INTERVAL\_TO\_SECONDS\_UDF (VARCHAR, VARCHAR)

### Definition

This user-defined function (UDF) is used to determine the quantity of seconds from an interval which is also correlated to the processed time type. This is an auxiliary function.

Copy code

```
:force:
INTERVAL_TO_SECONDS_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR())
```

### Parameters

`INPUT_PART` VARCHAR

The related type of the second parameter. For example, `DAY`, `DAY TO HOUR`, `HOUR`, `MINUTE`.

`INPUT_VALUE` VARCHAR

The value to be converted to seconds.

### Returns

Returns a decimal value type with the number of seconds.

### Usage example

Input:

Copy code

```
:force:
SELECT INTERVAL_TO_SECONDS_UDF('DAY', '1');
```

Output:

Copy code

```
:force:
86400.000000
```

## DATEDIFF\_UDF (DATE, STRING)

### Definition

This user-defined function (UDF) is used to generate the difference between an interval value and a date.

Copy code

```
:force:
DATEDIFF_UDF(D DATE, INTERVAL_VALUE STRING)
```

### Parameters

`D` DATE

The date to be used to process the difference with the interval.

`INTERVAL_VALUE` STRING

The interval value that will be used to create the difference from.

### Returns

Returns a date with the resulting value of the subtraction of time.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEDIFF_UDF('2024-01-30', 'INTERVAL ''2-1'' YEAR(2) TO MONTH');
```

Output:

Copy code

```
:force:
2021-12-30
```

## SECONDS\_TO\_INTERVAL\_UDF (VARCHAR, NUMBER)

### Definition

This user-defined function (UDF) is used to transform seconds into intervals. This is an auxiliary function.

Copy code

```
:force:
SECONDS_TO_INTERVAL_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE NUMBER)
```

### Parameters

`INPUT_PART` VARCHAR

The related type of the second parameter. For example, `DAY`, `DAY TO HOUR`, `HOUR`, `MINUTE`, `MINUTE TO SECOND`.

`INPUT_VALUE` VARCHAR

The seconds to be converted to intervals.

### Returns

Returns a varchar representing the converted time interval.

### Usage example

Input:

Copy code

```
:force:
SELECT SECONDS_TO_INTERVAL_UDF('DAY TO SECOND', '86400');
```

Output:

Copy code

```
:force:
1 000:000:000
```

## DATEADD\_UDF (STRING, DATE)

### Definition

This user-defined function (UDF) is used to add a date with an interval of time.

Copy code

```
:force:
DATEADD_UDF(INTERVAL_VALUE STRING,D DATE)
```

### Parameters

`INTERVAL_VALUE` STRING

The interval of time to be added.

`D` DATE

The date to be added with the interval of time.

### Returns

Returns a date with the addition of the interval of time and the date.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEADD_UDF('INTERVAL ''2-1'' YEAR(2) TO MONTH', '2024-01-30');
```

Output:

Copy code

```
:force:
2026-02-28
```

## DATEDIFF\_UDF (STRING, DATE)

### Definition

This user-defined function (UDF) is used to generate the difference between an interval value and a date.

Copy code

```
:force:
DATEDIFF_UDF(INTERVAL_VALUE STRING,D DATE)
```

### Parameters

`INTERVAL_VALUE` STRING

The interval value that will be used to create the difference from.

`D` DATE

The date to be used to process the difference with the interval.

### Returns

Returns a date with the resulting value of the subtraction of time.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEDIFF_UDF('INTERVAL ''2-1'' YEAR(2) TO MONTH', '2024-01-30');
```

Output:

Copy code

```
:force:
2021-12-30
```

## DATEADD\_UDF (DATE, STRING)

### Definition

This user-defined function (UDF) is used to add a date with an interval of time.

Copy code

```
:force:
DATEADD_UDF(D DATE, INTERVAL_VALUE STRING)
```

### Parameters

`D` DATE

The date to be added with the interval of time.

`INTERVAL_VALUE` STRING

The interval of time to be added.

### Returns

Returns a date with the addition of the interval of time and the date.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEADD_UDF('2024-01-30', 'INTERVAL ''1-1'' YEAR(2) TO MONTH');
```

Output:

Copy code

```
:force:
2025-02-28
```

## TO\_INTERVAL\_UDF (TIME)

### Definition

This user-defined function (UDF) is used to generate a separate interval of time from the current time.

Copy code

```
:force:
TO_INTERVAL_UDF(D2 TIME)
```

### Parameters

`D2` TIME

The input time to convert into a separate interval.

### Returns

Returns a string with the information of the input time separated.

### Usage example

Input:

Copy code

```
:force:
SELECT TO_INTERVAL_UDF(CURRENT_TIME);
```

Output:

Copy code

```
:force:
INTERVAL '4 HOURS,33 MINUTES,33 SECOND'
```

## INTERVAL\_TO\_MONTHS\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) is used to generate an integer with the quantity of a month from an interval. This is an auxiliary function.

Copy code

```
:force:
INTERVAL_TO_MONTHS_UDF
(INPUT_VALUE VARCHAR())
```

### Parameters

`INPUT_VALUE` VARCHAR

The interval value to be transformed into months.

### Returns

Returns an integer with the processed information about months.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.INTERVAL_TO_MONTHS_UDF('1-6');
```

Output:

Copy code

```
:force:
18
```

## DATEDIFF\_UDF (STRING, TIMESTAMP)

### Definition

This user-defined function (UDF) is used to subtract an interval of time with a timestamp.

Copy code

```
:force:
DATEDIFF_UDF(INTERVAL_VALUE STRING, D TIMESTAMP)
```

### Parameters

`INTERVAL_VALUE` STRING

The interval of time to be subtracted.

`D` TIMESTAMP

The timestamp to be subtracted with the interval of time.

### Returns

Returns a date with the subtraction of the interval of time and the date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF('INTERVAL ''1-1'' YEAR(2) TO MONTH', TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'));
```

Output:

Copy code

```
:force:
2022-12-31 05:09:09.799
```

## MONTHS\_TO\_INTERVAL\_UDF (VARCHAR, NUMBER)

### Definition

This user-defined function (UDF) is used to transform month values to intervals. This is an auxiliary function.

Copy code

```
:force:
MONTHS_TO_INTERVAL_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE NUMBER)
```

### Parameters

`INPUT_PART` VARCHAR

The related type of the second parameter. For example, `YEAR TO MONTH`, `YEAR`, `MONTH`.

`INPUT_VALUE` VARCHAR

The month to be converted to intervals.

### Returns

Returns a varchar with the input value transformed to an interval.

### Usage example

Input:

Copy code

```
:force:
SELECT MONTHS_TO_INTERVAL_UDF('YEAR TO MONTH', 2);
```

Output:

Copy code

```
:force:
2
```

## DATEDIFF\_UDF (TIMESTAMP, STRING)

### Definition

This user-defined function (UDF) is used to subtract a timestamp with an interval of time.

Copy code

```
:force:
DATEDIFF_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
```

### Parameters

`D` TIMESTAMP

The timestamp that will be subtracted with the interval of time.

`INTERVAL_VALUE` STRING

The interval of time to be subtracted.

### Returns

Returns a date with the subtraction of the interval of time and the date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF(TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'), 'INTERVAL ''1-1'' YEAR(2) TO MONTH');
```

Output:

Copy code

```
:force:
2022-12-31 05:09:09.799
```

## TRUNC\_UDF (NUMBER)

### Definition

This user-defined function (UDF) reproduces the Teradata and Oracle `TRUNC(Numeric)` functionality when a scale is **not** specified.

Copy code

```
:force:
TRUNC_UDF(INPUT NUMBER)
```

### Parameters

`INPUT` NUMBER

The number to truncate.

### Returns

Returns an int as the input truncated to zero decimal places.

### Usage example

Input:

Copy code

```
:force:
SELECT TRUNC_UDF(25122.3368)
```

Output:

Copy code

```
:force:
25122
```

## TRUNC\_UDF (NUMBER, NUMBER)

### Definition

This user-defined function (UDF) reproduces the Teradata and Oracle `TRUNC(Numeric)` functionality when a scale is specified.

Copy code

```
:force:
TRUNC_UDF(INPUT NUMBER, SCALE NUMBER)
```

### Parameters

`INPUT` NUMBER

The number to truncate.

`SCALE` NUMBER

The amount of places to truncate (between -38 and 38).

### Returns

Returns an int as the input truncated to scale places.

### Usage example

Input:

Copy code

```
:force:
SELECT TRUNC_UDF(25122.3368, -2);
```

Output:

Copy code

```
:force:
25100
```

## INTERVAL\_ADD\_UDF (VARCHAR, VARCHAR, VARCHAR, VARCHAR, CHAR, VARCHAR)

### Definition

This user-defined function (UDF) is used to add or subtract intervals with a specific time type.

Copy code

```
:force:
INTERVAL_ADD_UDF
(INPUT_VALUE1 VARCHAR(), INPUT_PART1 VARCHAR(30), INPUT_VALUE2 VARCHAR(), INPUT_PART2 VARCHAR(30), OP CHAR, OUTPUT_PART VARCHAR())
```

### Parameters

`INPUT_VALUE1` VARCHAR

The quantity referenced to a time type.

`INPUT_PART1` VARCHAR

The time type of the *`INPUT_VALUE1`*. For example: `HOUR`.

`INPUT_VALUE2` VARCHAR

The second quantity referenced to a time type.

`INPUT_PART2` VARCHAR

The time type of the *`INPUT_VALUE2`*. For example: `HOUR`.

`OP` CHAR

The operation. It can be a ‘+’ or a ‘-’.

`OUTPUT_PART` VARCHAR

The time type of the output operation.

### Returns

Returns a varchar with the result of the indicated operation and values.

### Usage example

Input:

Copy code

```
:force:
SELECT INTERVAL_ADD_UDF('7', 'HOUR', '1', 'HOUR', '+', 'HOUR');
```

Output:

Copy code

```
:force:
8
```

## DATEADD\_UDF (STRING, TIMESTAMP)

### Definition

This user-defined function (UDF) is used to add a timestamp with an interval of time.

Copy code

```
:force:
DATEADD_UDF(INTERVAL_VALUE STRING,D TIMESTAMP)
```

### Parameters

`INTERVAL_VALUE` STRING

The interval of time to be added.

`D` TIMESTAMP

The timestamp to be added with the interval of time.

### Returns

Returns a date with the addition of the interval of time and the date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEADD_UDF('INTERVAL ''1-1'' YEAR(2) TO MONTH', TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'));
```

Output:

Copy code

```
:force:
2025-02-28 05:09:09.799
```

## TRUNC\_UDF (TIMESTAMP\_LTZ)

### Definition

This user-defined function (UDF) reproduces the Teradata and Oracle TRUNC(Date) functionality when the format parameter is **not** specified.

Copy code

```
:force:
TRUNC_UDF(DATE_TO_TRUNC TIMESTAMP_LTZ)
```

### Parameters

`DATE_TO_TRUNC` TIMESTAMP\_LTZ

A `timestamp_ltz` value to truncate which must be a date, timestamp, or timestamp with timezone.

### Returns

Returns a date part of `DATE_TO_TRUNC`.

### Usage example

Input:

Copy code

```
:force:
SELECT TRUNC_UDF(TIMESTAMP '2015-08-18 12:30:00')
```

Output:

Copy code

```
:force:
2015-08-18
```

## DATEADD\_UDF (TIMESTAMP, STRING)

### Definition

This user-defined function (UDF) is used to add a timestamp with an interval of time.

Copy code

```
:force:
DATEADD_UDF(D TIMESTAMP, INTERVAL_VALUE STRING)
```

### Parameters

`D` TIMESTAMP

The timestamp to be added with the interval of time.

`INTERVAL_VALUE` STRING

The interval of time to be added.

### Returns

Returns a date with the addition of the interval of time and the date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEADD_UDF(TO_TIMESTAMP('2024-01-31 05:09:09.799 -0800'), 'INTERVAL ''1-1'' YEAR(2) TO MONTH');
```

Output:

Copy code

```
:force:
2025-02-28 05:09:09.799
```

## LOG\_INFO\_UDP (VARCHAR)

### Definition

This user-defined stored procedure (UDP) is used to log messages using the Snowflake [SYSTEM$LOG](/developer-guide/logging-tracing/logging-snowflake-scripting) functions.

Copy code

```
:force:
LOG_INFO_UDP(MESSAGE VARCHAR)
```

### Parameters

`MESSAGE` VARCHAR

The message to be logged.

### Returns

A success message indicating the log operation was completed.

### Usage example

Input:

Copy code

```
:force:
CALL PUBLIC.LOG_INFO_UDP('My log message');
```

Output:

| RESULT |
| --- |
| ‘Message logged successfully’ |

Expand

Show lessSee more
