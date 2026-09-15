# Code Conversion - Function References for Teradata

## QUARTERNUMBER\_OF\_YEAR\_UDF

### Definition

UDF (User-Defined Function) that calculates the quarter number of a given date according to the ISO calendar year, similar to Teradata’s QUARTERNUMBER\_OF\_YEAR\_UDF(date, ‘ISO’) function.

Copy code

```
:force:
PUBLIC.QUARTERNUMBER_OF_YEAR_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The method to extract the quarter number.

### Returns

An integer (1-4) indicating which quarter of the year the date falls into.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.QUARTERNUMBER_OF_YEAR_UDF(DATE '2022-01-01'),
PUBLIC.QUARTERNUMBER_OF_YEAR_UDF(DATE '2025-12-31');
```

Output:

Copy code

```
:force:
4, 1
```

## DAYNUMBER\_OF\_YEAR\_UDF

### Definition

Returns the day number within the year for a given timestamp. The day number ranges from 1 to 365 (or 366 in leap years). This function behaves the same way as DAYNUMBER\_OF\_YEAR(DATE, ‘ISO’).

Copy code

```
:force:
PUBLIC.DAYNUMBER_OF_YEAR_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

To get the day number of the year from a date.

### Returns

A whole number from 1 to 365 (or 366 in leap years).

### Example

Input:

Copy code

```
:force:
SELECT DAYNUMBER_OF_YEAR(CURRENT_DATE,'ISO');
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.DAYNUMBER_OF_YEAR_UDF(CURRENT_DATE());
```

## SUBSTR\_UDF (STRING, FLOAT)

Warning

This user-defined function (UDF) accepts two parameters (overloaded function).

### Definition

Retrieves a portion of text from a specified string by using a starting position and length.

Copy code

```
:force:
PUBLIC.SUBSTR_UDF(BASE_EXPRESSION STRING, START_POSITION FLOAT)
```

### Parameters

`BASE_EXPRESSION` is a string parameter that defines the base expression for the operation.

The source text from which you want to extract a portion.

`START_POSITION` - A floating-point number that specifies the starting position in the input string.

The position where you want to begin extracting characters from the string.

### Returns

The substring that must be included.

### Migration example

Input:

Copy code

```
:force:
SELECT SUBSTRING('Hello World!' FROM -2);
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.SUBSTR_UDF('Hello World!', -2);
```

## CHKNUM\_UDF

### Definition

Verify whether a string contains a valid numeric value.

Copy code

```
:force:
PUBLIC.CHKNUM_UDF(NUM STRING);
```

### Parameters

`NUM` A string representing a number

The text string that needs to be validated.

### Returns

Returns 1 if the input parameter is a valid numeric value. If the input is not a valid number (for example, text or special characters), returns 0.

### Example

Copy code

```
:force:
SELECT CHKNUM('1032');
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.CHKNUM_UDF('1032');
```

## TD\_YEAR\_END\_UDF

### Definition

UDF (User-Defined Function) that replicates Teradata’s TD\_YEAR\_END(DATE) or TD\_YEAR\_END(DATE, ‘COMPATIBLE’) function, which returns the last day of the year for a given date.

Copy code

```
:force:
PUBLIC.TD_YEAR_END_UDF(INPUT date)
```

### Parameters

`INPUT` DATE

Get the last day of the current year.

### Returns

The final day of December (December 31st).

### Usage example

Input:

Copy code

```
:force:
SELECT  PUBLIC.TD_YEAR_END_UDF(DATE '2022-01-01'),
PUBLIC.TD_YEAR_END_UDF(DATE '2022-04-12');
```

Output:

Copy code

```
:force:
2022-12-31, 2022-12-31
```

## PERIOD\_OVERLAPS\_UDF

### Definition

A user-defined function (UDF) that implements the OVERLAPS OPERATOR functionality. This function compares two or more time periods and determines whether they have any overlapping time ranges.

Copy code

```
:force:
PERIOD_OVERLAPS_UDF(PERIODS ARRAY)
```

### Parameters

`PERIODS` is an array that contains time periods

All period expressions that will be compared.

### Returns

TRUE if all time periods in the set have at least one point in common (overlap), FALSE otherwise.

### Migration example

Copy code

```
:force:
SELECT
	PERIOD(DATE '2009-01-01', DATE '2010-09-24')
	OVERLAPS
	PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

Output:

Copy code

```
:force:
SELECT
	PUBLIC.PERIOD_OVERLAPS_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

## WEEK\_NUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF

### Definition

Calculates which week number within the current quarter a specified date falls into.

Copy code

```
:force:
PUBLIC.WEEK_NUMBER_OF_QUARTER_COMPATIBLE_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date used to calculate which week of the quarter it falls into.

### Returns

An integer indicating which week of the quarter the date falls in (1-13).

### Usage example

Input:

Copy code

```
:force:
SELECT WEEK_NUMBER_OF_QUARTER_COMPATIBLE_UDF(DATE '2022-05-01', 'COMPATIBLE'),
WEEK_NUMBER_OF_QUARTER_COMPATIBLE_UDF(DATE '2022-07-06', 'COMPATIBLE')
```

Output:

Copy code

```
:force:
5, 1
```

## ROMAN\_NUMERALS\_MONTH\_UDF

### Definition

Converts a date into its corresponding month in Roman numerals.

Copy code

```
:force:
PUBLIC.ROMAN_NUMERALS_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The input date from which to extract the month.

### Returns

A `varchar` representing the month extracted from a given date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.ROMAN_NUMERALS_MONTH_UDF(DATE '2021-10-26');
```

Output:

Copy code

```
:force:
'X'
```

## TD\_YEAR\_BEGIN\_UDF

### Definition

A user-defined function (UDF) that mimics the behavior of TD\_YEAR\_BEGIN or TD\_YEAR\_BEGIN(DATE, ‘COMPATIBLE’) by returning the first day of the year for a given date.

Copy code

```
:force:
PUBLIC.TD_YEAR_BEGIN_UDF(INPUT DATE)
```

### Parameters

`INPUT` DATE

Get the first day of the current year.

### Returns

The first day of January.

### Usage example

Input:

Copy code

```
:force:
SELECT TD_YEAR_BEGIN(DATE '2022-01-01', 'COMPATIBLE'),
TD_YEAR_BEGIN(DATE '2022-04-12');
```

Output:

Copy code

```
:force:
2022-01-01, 2022-01-01
```

## FULL\_MONTH\_NAME\_UDF

### Definition

Returns the full name of a month in your choice of formatting: all uppercase letters, all lowercase letters, or with only the first letter capitalized.

Copy code

```
:force:
PUBLIC.FULL_MONTH_NAME_UDF(INPUT TIMESTAMP_TZ, RESULTCASE VARCHAR)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date format should display the month name.

`RESULTCASE` VARCHAR

The format in which the result should be displayed. Valid options are ‘uppercase’, ‘lowercase’, or ‘firstOnly’.

### Returns

Returns a `varchar` containing the full name of a month

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.FULL_MONTH_NAME_UDF(DATE '2021-10-26', 'uppercase');
SELECT PUBLIC.FULL_MONTH_NAME_UDF(DATE '2021-10-26', 'lowercase');
SELECT PUBLIC.FULL_MONTH_NAME_UDF(DATE '2021-10-26', 'firstOnly');
```

Output:

Copy code

```
:force:
OCTOBER
october
October
```

## TO\_BYTES\_HEX\_UDF

### Definition

Converts a decimal (base 10) number into its hexadecimal (base 16) representation.

Copy code

```
:force:
TO_BYTES_HEX_UDF(INPUT FLOAT)
```

### Parameters

`INPUT` is a floating-point number parameter.

The number that will be converted into hexadecimal format.

### Returns

A string representing the hexadecimal value.

### Usage example

Input:

Copy code

```
:force:
SELECT TO_BYTES_HEX_UDF('448');
```

Output:

Copy code

```
:force:
01c0
```

## PERIOD\_INTERSECT\_UDF

### Definition

A user-defined function (UDF) that replicates the P\_INTERSECT operator. This function compares two or more time periods and identifies where they overlap, returning the common time interval between them.

For more details about the source function, please refer to the [documentation](https://docs.teradata.com/r/SQL-Date-and-Time-Functions-and-Expressions/July-2021/Period-Functions-and-Operators/P_INTERSECT/P_INTERSECT-Syntax).

Copy code

```
:force:
PERIOD_INTERSECT_UDF(PERIODS ARRAY)
```

### Parameters

`PERIODS` is an array that contains time periods.

All period expressions that need to be compared.

### Returns

The section where two time periods intersect or share common dates.

### Migration example

Input:

Copy code

```
:force:
SELECT
	PERIOD(DATE '2009-01-01', DATE '2010-09-24')
	P_INTERSECT
	PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

Output:

Copy code

```
:force:
SELECT
	PUBLIC.PERIOD_INTERSECT_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

## INTERVAL\_TO\_SECONDS\_UDF

### Definition

Converts a time interval into seconds.

Copy code

```
:force:
PUBLIC.INTERVAL_TO_SECONDS_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR())
```

### Parameters

`INPUT_PART` is a variable of type VARCHAR that stores input data.

The time duration that will be converted into seconds.

`INPUT_VALUE` VARCHAR - The input parameter that accepts text data.

The time interval type for conversion. Examples include ‘DAY’, ‘DAY TO HOUR’, and other valid interval types.

### Returns

A decimal number representing the time interval in seconds.

## TIMESTAMP\_ADD\_UDF

### Definition

Combines two timestamps into a single value.

Copy code

```
:force:
PUBLIC.TIMESTAMP_ADD_UDF(FIRST_DATE TIMESTAMP_LTZ, SECOND_DATE TIMESTAMP_LTZ)
```

### Parameters

`FIRST_DATE` is a timestamp field that includes both date and time information, with timezone support (TIMESTAMP\_LTZ)

The initial date when this was added.

`SECOND_DATE` is a timestamp column that includes timezone information (TIMESTAMP\_LTZ) (Timestamp with local time zone)

The date when the item was added for the second time.

### Returns

A timestamp generated by combining the input date parameters.

## INTERVAL\_MULTIPLY\_UDF

### Definition

A user-defined function (UDF) that performs multiplication operations on time intervals.

Copy code

```
:force:
PUBLIC.INTERVAL_MULTIPLY_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR(), INPUT_MULT INTEGER)
```

### Parameters

`INPUT_PART` is a variable of type VARCHAR that stores input data.

The value used for multiplication, specified as ‘YEAR TO MONTH’.

`INPUT_VALUE` VARCHAR

The interval to multiply by.

`INPUT_MULT` is an integer parameter that serves as a multiplier for input values.

The number that will be used in the multiplication operation.

### Returns

The output is calculated by multiplying a time interval by a numeric value.

### Migration example

Input:

Copy code

```
:force:
SELECT INTERVAL '6-10' YEAR TO MONTH * 8;
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.INTERVAL_MULTIPLY_UDF('YEAR TO MONTH', '6-10', 8);
```

## TD\_DAY\_OF\_WEEK\_UDF

### Definition

User-defined function (UDF) that replicates Teradata’s `TD_DAY_OF_WEEK` functionality. For details about the original Teradata function, see [here](https://docs.teradata.com/r/SQL-Date-and-Time-Functions-and-Expressions/July-2021/Calendar-Functions/td_day_of_week/DayOfWeek).

Copy code

```
:force:
PUBLIC.TD_DAY_OF_WEEK_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

Date from which to get the day of the week.

### Returns

An integer from 1 to 7 representing the day of the week, where:

- 1 = Sunday
- 2 = Monday
- 3 = Tuesday
- 4 = Wednesday
- 5 = Thursday
- 6 = Friday
- 7 = Saturday

### Migration example

Input:

Copy code

```
:force:
SELECT td_day_of_week(DATE '2022-03-02');
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.TD_DAY_OF_WEEK_UDF(DATE '2022-03-02');
```

## ISO\_YEAR\_PART\_UDF

### Definition

Calculates the ISO calendar year from a given date. The result can be shortened by specifying the number of digits to keep.

Copy code

```
:force:
PUBLIC.ISO_YEAR_PART_UDF(INPUT TIMESTAMP_TZ, DIGITS INTEGER)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date from which to extract the ISO year.

`DIGITS` A whole number that represents the maximum number of digits to display

The number of decimal places desired in the output.

### Returns

Returns a string (varchar) representing the ISO year of a given date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.ISO_YEAR_PART_UDF(DATE '2021-10-26', 3);
SELECT PUBLIC.ISO_YEAR_PART_UDF(DATE '2021-10-26', 2);
SELECT PUBLIC.ISO_YEAR_PART_UDF(DATE '2021-10-26', 1);
```

Output:

Copy code

```
:force:
'021'
'21'
'1'
```

## DIFF\_TIME\_PERIOD\_UDF

### Definition

Computes the time interval between two dates based on the specified time unit parameter.

Copy code

```
:force:
PUBLIC.DIFF_TIME_PERIOD_UDF(TIME STRING, PERIOD VARCHAR(50))
```

### Parameters

`TIME` is a data type used to store time values in hours, minutes, seconds, and fractions of seconds.

The timestamp that will be used as an anchor point.

`PERIOD` A text field (VARCHAR) that represents a time period

The period column used for expansion.

### Returns

A numerical value indicating the time interval between two dates.

### Usage example

Input:

Copy code

```
:force:
SELECT DIFF_TIME_PERIOD_UDF('SECONDS','2022-11-26 10:15:20.000*2022-11-26 10:15:25.000');
```

Output:

Copy code

```
:force:
5
```

## WEEK\_NUMBER\_OF\_QUARTER\_ISO\_UDF

### Definition

Calculates which week number a date falls into within its quarter, using ISO calendar standards. This function behaves identically to Teradata’s `WEEKNUMBER_OF_QUARTER(DATE, 'ISO')` function.

Copy code

```
:force:
PUBLIC.WEEK_NUMBER_OF_QUARTER_ISO_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date used to calculate which week of the quarter it falls into.

### Returns

An integer indicating which week of the quarter (1-13) this represents.

### Usage example

Input:

Copy code

```
:force:
SELECT WEEKNUMBER_OF_QUARTER(DATE '2022-05-01', 'ISO'),
WEEKNUMBER_OF_QUARTER(DATE '2022-07-06', 'ISO')
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.SUBSTR_UDF('Hello World!', -2);
```

## NVP\_UDF

### Definition

Performs the same function as Teradata’s [NVP function](https://docs.teradata.com/r/SQL-Functions-Expressions-and-Predicates/June-2020/String-Operators-and-Functions/NVP/NVP-Function-Syntax).

Copy code

```
:force:
NVP_UDF(INSTRING VARCHAR, NAME_TO_SEARCH VARCHAR, NAME_DELIMITERS VARCHAR, VALUE_DELIMITERS VARCHAR, OCCURRENCE FLOAT)
```

### Parameters

`INSTRING` VARCHAR

Name-value pairs are data elements that consist of a name and its corresponding value.

`NAME_TO_SEARCH` of type VARCHAR

The name parameter used to search within the Name-Value Pair (NVP) function.

`NAME_DELIMITERS` VARCHAR

The character used to separate names from their corresponding values.

`VALUE_DELIMITERS` VARCHAR

The character used to connect a name with its corresponding value.

`OCCURRENCE` represents a floating-point number that indicates how many times something occurs

The number of matching patterns to search for.

### Returns

A text string (VARCHAR) containing identical data as the input string.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.NVP_UDF('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1);
```

Output:

Copy code

```
:force:
orange chicken
```

## MONTH\_SHORT\_UDF

### Definition

Returns the abbreviated name of a month (three letters) in your choice of uppercase, lowercase, or capitalized format. For example: “Jan”, “jan”, or “JAN”.

Copy code

```
:force:
PUBLIC.MONTH_SHORT_UDF(INPUT TIMESTAMP_TZ, RESULTCASE VARCHAR)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date formatted to display the abbreviated month name.

`RESULTCASE` VARCHAR

The letter case format to be used. Valid options are:

- ‘uppercase’: converts text to all capital letters
- ‘lowercase’: converts text to all small letters
- ‘firstOnly’: capitalizes only the first letter

### Returns

A `varchar` containing the abbreviated name of a month (for example, “Jan”, “Feb”, and so on).

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.MONTH_SHORT_UDF(DATE '2021-10-26', 'uppercase');
SELECT PUBLIC.MONTH_SHORT_UDF(DATE '2021-10-26', 'lowercase');
SELECT PUBLIC.MONTH_SHORT_UDF(DATE '2021-10-26', 'firstOnly');
```

Output:

Copy code

```
:force:
OCT
oct
Oct
```

## DATE\_TO\_INT\_UDF

### Definition

UDF (User-Defined Function) that converts a date value to its numeric representation, similar to Teradata’s DATE-TO-NUMERIC function.

Copy code

```
:force:
PUBLIC.DATE_TO_INT_UDF(DATE_TO_CONVERT DATE)
```

### Parameters

`DATE_TO_CONVERT` represents a date value that needs to be converted

Convert the date value to an integer format.

### Returns

Returns a date value in numeric format.

### Example

Input:

Copy code

```
:force:
SELECT mod(date '2015-11-26', 5890), sin(current_date);

CREATE TABLE SAMPLE_TABLE
(
    VARCHAR_TYPE VARCHAR,
    CHAR_TYPE CHAR(11),
    INTEGER_TYPE INTEGER,
    DATE_TYPE DATE,
    TIMESTAMP_TYPE TIMESTAMP,
    TIME_TYPE TIME,
    PERIOD_TYPE PERIOD(DATE)
);

REPLACE VIEW SAMPLE_VIEW
AS
SELECT
CAST(DATE_TYPE AS SMALLINT),
CAST(DATE_TYPE AS DECIMAL),
CAST(DATE_TYPE AS NUMBER),
CAST(DATE_TYPE AS FLOAT),
CAST(DATE_TYPE AS INTEGER)
FROM SAMPLE_TABLE;
```

Output:

Copy code

```
:force:
SELECT
mod(PUBLIC.DATE_TO_INT_UDF(date '2015-11-26'), 5890),
sin(PUBLIC.DATE_TO_INT_UDF(CURRENT_DATE()));

CREATE TABLE PUBLIC.SAMPLE_TABLE
(
    VARCHAR_TYPE VARCHAR,
    CHAR_TYPE CHAR(11),
    INTEGER_TYPE INTEGER,
    DATE_TYPE DATE,
    TIMESTAMP_TYPE TIMESTAMP,
    TIME_TYPE TIME,
    PERIOD_TYPE VARCHAR(24) COMMENT 'PERIOD(DATE)' /*** MSC-WARNING - MSCEWI1036 - PERIOD DATA TYPE "PERIOD(DATE)" CONVERTED TO VARCHAR ***/
);

CREATE OR REPLACE VIEW PUBLIC.SAMPLE_VIEW
AS
SELECT
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE),
PUBLIC.DATE_TO_INT_UDF(DATE_TYPE)
FROM PUBLIC.SAMPLE_TABLE;
```

## PERIOD\_UDF

### Definition

A user-defined function (UDF) that replicates the P\_INTERSECT operator. This function compares two or more time periods and identifies where they overlap, returning the common time interval between them.

Creates a string representation of a period’s start and end values (for `TIMESTAMP`, `TIME`, or `DATE` data types). This function emulates Teradata’s period value constructor function. The output string follows Snowflake’s default format for `PERIOD` values. To adjust the precision of the output, you can either:

- Modify the session parameter `timestamp_output_format`
- Use the three-parameter version of this UDF

More details about the source function can be found in the [Teradata documentation](https://docs.teradata.com/r/SQL-External-Routine-Programming/July-2021/SQL-Data-Type-Mapping/C-Data-Types/PERIOD-DATE/PERIOD-TIME/PERIOD-TIMESTAMP).

Copy code

```
:force:
PERIOD_UDF(D1 TIMESTAMP_NTZ, D2 TIMESTAMP_NTZ)
PERIOD_UDF(D1 DATE, D2 DATE)
PERIOD_UDF(D1 TIME, D2 TIME)
PERIOD_UDF(D1 TIMESTAMP_NTZ, D2 TIMESTAMP_NTZ, PRECISIONDIGITS INT)
PERIOD_UDF(D1 TIME, D2 TIME, PRECISIONDIGITS INT)
PERIOD_UDF(D1 TIMESTAMP_NTZ)
PERIOD_UDF(D1 DATE)
PERIOD_UDF(D1 TIME)
```

### Parameters

`TIMESTAMP`

The TimeStamp data type represents a specific point in time, including both the date and time components.

`TIME`

The Time data type represents a specific time of day without a date component.

`DATE`

The Date data type represents a calendar date without a time component.

`PRECISIONDIGITS` specifies the number of decimal places to display in numeric values.

The number of digits to display in the time format.

### Returns

Returns a string representation of a `PERIOD` type value

### Usage example

Input:

Copy code

```
:force:
SELECT
PERIOD_UDF('2005-02-03'),
PERIOD_UDF(date '2005-02-03'),
PERIOD_UDF(TIMESTAMP '2005-02-03 12:12:12.340000'),
PERIOD_UDF(TIMESTAMP '2005-02-03 12:12:12.340000');
```

Output:

Copy code

```
:force:
2005-02-03*2005-02-04,
2005-02-03*2005-02-04,
2005-02-03 12:12:12.340000*2005-02-03 12:12:12.340001,
2005-02-03 12:12:12.340000*2005-02-03 12:12:12.340001
```

## DAYNAME\_LONG\_UDF (TIMESTAMP\_TZ, VARCHAR)

Warning

This is the user-defined function (UDF) that accepts <mark style=”color:orange;”>**two**</mark> **different parameter types.**

### Definition

Returns the full name of a weekday in your choice of uppercase, lowercase, or capitalized format (e.g., “MONDAY”, “monday”, or “Monday”).

Copy code

```
:force:
PUBLIC.DAYNAME_LONG_UDF(INPUT TIMESTAMP_TZ, RESULTCASE VARCHAR)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The input date from which to determine the day of the week.

`RESULTCASE` VARCHAR

The expected outcome or scenario that will be demonstrated.

### Returns

Returns a string containing the full name of a day of the week.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2021-10-26', 'uppercase');
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2021-10-26', 'lowercase');
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2021-10-26', 'firstOnly');
```

Output:

Copy code

```
:force:
'TUESDAY'
'tuesday'
'Tuesday'
```

## TD\_DAY\_OF\_WEEK\_COMPATIBLE\_UDF

### Definition

Process a timestamp to determine which day of the week it falls on. This function behaves identically to `DAYNUMBER_OF_WEEK(DATE, 'COMPATIBLE')`.

Copy code

```
:force:
PUBLIC.TD_DAY_OF_WEEK_COMPATIBLE_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The input date used to determine the day of the week.

### Returns

Returns a number from 1 to 7 representing the day of the week, where 1 represents the first day of the week. For example, if January 1st falls on a Wednesday, then Wednesday = 1, Thursday = 2, Friday = 3, Saturday = 4, Sunday = 5, Monday = 6, and Tuesday = 7.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.TD_DAY_OF_WEEK_COMPATIBLE_UDF(DATE '2022-01-01'),
PUBLIC.TD_DAY_OF_WEEK_COMPATIBLE_UDF(DATE '2023-05-05');
```

Output:

Copy code

```
:force:
1, 6
```

## JAROWINKLER\_UDF

### Definition

Calculates how similar two strings are using the Jaro-Winkler algorithm. This algorithm gives a score between 0 (completely different) and 1 (identical).

Copy code

```
:force:
PUBLIC.JAROWINKLER_UDF (string1 VARCHAR, string2 VARCHAR)
```

### Parameters

`string1` of type VARCHAR

The text to be processed

`string2` of type VARCHAR

The text to be processed

### Returns

The function returns a score between 0 (completely different) and 1 (identical).

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.JAROWINKLER_UDF('święta', 'swieta')
```

Output:

Copy code

```
:force:
0.770000
```

## YEAR\_BEGIN\_ISO\_UDF

### Definition

UDF that calculates the first day of the ISO year for a given date. It works by finding the Monday closest to January 1st of the year, using the `DAYOFWEEKISO` function in combination with `PUBLIC.FIRST_DAY_JANUARY_OF_ISO_UDF`. The function either adds or subtracts days to locate this Monday.

Copy code

```
:force:
PUBLIC.YEAR_BEGIN_ISO_UDF(INPUT DATE)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date that represents January 1st of the current year according to the ISO calendar standard.

### Returns

The first day of the year according to the ISO calendar standard.

### Usage example

Input:

Copy code

```
:force:
SELECT  PUBLIC.YEAR_BEGIN_ISO_UDF(DATE '2022-01-01'),
PUBLIC.YEAR_BEGIN_ISO_UDF(DATE '2022-04-12');
```

Output:

Copy code

```
:force:
2021-01-04, 2022-01-03
```

## YEAR\_PART\_UDF

### Definition

Extract the year from a date and truncate it to a specified number of digits.

Copy code

```
:force:
PUBLIC.YEAR_PART_UDF(INPUT TIMESTAMP_TZ, DIGITS INTEGER)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date from which to extract the year.

`DIGITS` A whole number that represents the maximum number of digits to display

The number of decimal places desired in the output.

### Returns

Extracts the year component from a specified date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.YEAR_PART_UDF(DATE '2021-10-26', 3);
SELECT PUBLIC.YEAR_PART_UDF(DATE '2021-10-26', 2);
SELECT PUBLIC.YEAR_PART_UDF(DATE '2021-10-26', 1);
```

Output:

Copy code

```
:force:
'021'
'21'
'1'
```

## YEAR\_WITH\_COMMA\_UDF

### Definition

Extracts the year from a date and adds a comma between the first and second digits. For example, if the year is 2023, it returns “2,023”.

Copy code

```
:force:
PUBLIC.YEAR_WITH_COMMA_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The input date from which to extract the year.

### Returns

Returns the year portion of a date value as a varchar (text) with a comma separator.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.YEAR_WITH_COMMA_UDF(DATE '2021-10-26');
```

Output:

Copy code

```
:force:
'2,021'
```

## MONTHS\_BETWEEN\_UDF

### Definition

Calculate the Number of Months Between Two Dates

Copy code

```
:force:
MONTHS_BETWEEN_UDF(FIRST_DATE TIMESTAMP_LTZ, SECOND_DATE TIMESTAMP_LTZ)
```

### Parameters

`FIRST_DATE` is a timestamp column that includes both date and time information, with timezone support (TIMESTAMP\_LTZ)

The initial date from which the function will begin processing data.

`SECOND_DATE` TIMESTAMP\_LTZ

The ending date that defines when to stop counting.

### Returns

The duration in months between two dates.

### Usage example

Input:

Copy code

```
:force:
SELECT MONTHS_BETWEEN_UDF('2022-02-14', '2021-02-14');
```

Output:

Copy code

```
:force:
12
```

## SECONDS\_PAST\_MIDNIGHT\_UDF

### Definition

Calculate the number of seconds elapsed since midnight for a specified time.

Copy code

```
:force:
PUBLIC.SECONDS_PAST_MIDNIGHT_UDF(INPUT TIME)
```

### Parameters

`INPUT` TIME

The function calculates the total number of seconds elapsed since midnight (00:00:00) until the current time.

### Returns

A `varchar` value representing the number of seconds elapsed since midnight.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.SECONDS_PAST_MIDNIGHT_UDF(TIME'10:30:45');
```

Output:

Copy code

```
:force:
'37845'
```

## CHAR2HEXINT\_UDF

### Definition

Returns a string containing the hexadecimal (base-16) representation of each character in the input string.

Copy code

```
:force:
PUBLIC.CHAR2HEXINT_UDF(INPUT_STRING VARCHAR);
```

### Parameters

`INPUT_STRING` is a variable of type VARCHAR that stores text data.

The input string that needs to be converted.

### Returns

Returns a string containing the hexadecimal representation of the input string.

### Example

Input:

Copy code

```
:force:
SELECT CHAR2HEXINT('1234') from t1;
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.CHAR2HEXINT_UDF('1234') from
t1;
```

### More information from the source function

Function documentation is available in the [Teradata documentation](https://docs.teradata.com/r/SQL-Functions-Expressions-and-Predicates/June-2020/String-Operators-and-Functions/CHAR2HEXINT).

## INTERVAL\_ADD\_UDF

### Definition

UDFs (User-Defined Functions) that handle addition and subtraction operations between an interval value and a column reference of type interval.

Copy code

```
:force:
PUBLIC.INTERVAL_ADD_UDF
(INPUT_VALUE1 VARCHAR(), INPUT_PART1 VARCHAR(30), INPUT_VALUE2 VARCHAR(), INPUT_PART2 VARCHAR(30), OP CHAR, OUTPUT_PART VARCHAR())
```

### Parameters

`INPUT_VALUE1` of type VARCHAR

The input data that will be processed by the system.

`INPUT_PART1` of type VARCHAR

The time unit to be used, such as ‘`HOUR`’.

`INPUT_VALUE2` is a VARCHAR data type parameter.

The name of the referenced column, such as ‘`INTERVAL_HOUR_TYPE`’

`INPUT_PART2` VARCHAR

The data type assigned to the referenced column.

`OP` character

The symbol or operator that is currently being analyzed.

`OUTPUT_PART` VARCHAR

The data type of the returned value.

### Returns

A `varchar` value that represents the result of adding or subtracting two time intervals.

### Migration example

Input:

Copy code

```
:force:
CREATE TABLE INTERVAL_TABLE
(
    INTERVAL_YEAR_TYPE INTERVAL YEAR
);

SELECT INTERVAL_YEAR_TYPE - INTERVAL '7' MONTH FROM INTERVAL_TABLE;
```

Output:

Copy code

```
:force:
CREATE OR REPLACE TABLE INTERVAL_TABLE
(
    INTERVAL_YEAR_TYPE VARCHAR(21) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR DATA TYPE CONVERTED TO VARCHAR ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT
    PUBLIC.INTERVAL_ADD_UDF(INTERVAL_YEAR_TYPE, 'YEAR', '7', 'MONTH', '-', 'YEAR TO MONTH')
    FROM
    INTERVAL_TABLE;
```

## DAY\_OF\_WEEK\_LONG\_UDF

### Definition

A user-defined function (UDF) that converts a timestamp into the full name of the day (for example, “Monday”, “Tuesday”, etc.).

Copy code

```
:force:
PUBLIC.DAY_OF_WEEK_LONG_UDF(INPUT_DATE TIMESTAMP)
```

### Parameters

`INPUT_DATE` represents a timestamp value

The timestamp will be converted into a full day name (for example, “Monday”, “Tuesday”, etc.).

### Returns

The name of the day in English.

## TD\_WEEK\_OF\_CALENDAR\_UDF

### Definition

The user-defined function (UDF) serves as a direct replacement for Teradata’s [TD\_WEEK\_OF\_CALENDAR](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Date-and-Time-Functions-and-Expressions/Calendar-Functions/td_week_of_calendar) function, providing the same functionality in Snowflake.

Copy code

```
:force:
PUBLIC.TD_WEEK_OF_CALENDAR_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

Date used to calculate the number of weeks that have elapsed since January 1, 1900.

### Returns

An integer representing the number of complete weeks between January 1, 1900, and the specified date

### Migration example

Input:

Copy code

```
:force:
SELECT TD_WEEK_OF_CALENDAR(DATE '2023-11-30')
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.TD_WEEK_OF_CALENDAR_UDF(DATE '2023-11-30');
```

## WRAP\_NEGATIVE\_WITH\_ANGLE\_BRACKETS\_UDF

### Definition

Converts negative numbers to use angle brackets (< >) instead of the minus sign (-). This conversion occurs when the PR (parentheses) format element is present in the original Teradata format string.

Copy code

```
:force:
PUBLIC.WRAP_NEGATIVE_WITH_ANGLE_BRACKETS_UDF(INPUT NUMBER, FORMATARG VARCHAR)
```

### Parameters

`INPUT` is a numeric value

The numeric value that will be converted into a text string (varchar).

`FORMATARG` is a parameter of type VARCHAR that specifies the format of the data.

The format parameter specifies how to convert the INPUT value into a text (varchar) representation.

### Returns

A `varchar` containing negative numbers enclosed in angle brackets (< >).

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.WRAP_NEGATIVE_WITH_ANGLE_BRACKETS_UDF(8456, '9999');
SELECT PUBLIC.WRAP_NEGATIVE_WITH_ANGLE_BRACKETS_UDF(-8456, '9999');
```

Output:

Copy code

```
:force:
'8456'
'<8456>'
```

## INSTR\_UDF (STRING, STRING)

Warning

This is the user-defined function (UDF) that accepts <mark style=”color:orange;”>**two**</mark> **different parameter sets**.

### Definition

Finds all instances where search\_string appears within source\_string.

Copy code

```
:force:
PUBLIC.INSTR_UDF(SOURCE_STRING STRING, SEARCH_STRING STRING)
```

### Parameters

`SOURCE_STRING` represents the input string that needs to be processed

The text that will be searched.

`SEARCH_STRING` is a parameter of type STRING that specifies the text to search for.

The text pattern that the function will look for and match.

### Returns

The index position where the pattern is found in the source string (starting from position 1).

### Usage example

Input:

Copy code

```
:force:
SELECT INSTR_UDF('INSTR FUNCTION','N');
```

Output:

Copy code

```
:force:
2
```

## TRANSLATE\_CHK\_UDF

### Definition

Checks whether the code can be successfully converted without generating any errors.

Copy code

```
:force:
PUBLIC.TRANSLATE_CHK_UDF(COL_NAME STRING, SOURCE_REPERTOIRE_NAME STRING)
```

### Parameters

`COL_NAME` is a string variable that represents a column name.

The column that needs to be validated.

`SOURCE_REPERTOIRE_NAME` is a string parameter that specifies the name of the source directory.

The name of the source collection or library.

### Returns

0: The translation was successful and completed without errors.
NULL: No result was returned (null value).

The first character’s position in the string is causing a translation error.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.TRANSLATE_CHK_UDF('ABC', 'UNICODE_TO_LATIN');
```

Output:

Copy code

```
:force:
0
```

## EXPAND\_ON\_UDF

Note

For better readability, we have simplified some sections of the code in this example.

### Definition

Replicates the behavior of Teradata’s expand-on function.

Copy code

```
:force:
PUBLIC.EXPAND_ON_UDF(TIME STRING, SEQ NUMBER, PERIOD STRING)
```

### Parameters

`TIME` is a data type that stores time values as text (STRING).

The time required for the anchor to fully expand.

`SEQ` Sequence Number

The order in which each row’s values are computed.

`PERIOD` A text value representing a time period

The date for the specified time period.

### Returns

A `VARCHAR` value that defines how to calculate the expansion period in the expand-on clause.

### Migration example

Input:

Copy code

```
:force:
SELECT bg FROM table1 EXPAND ON pd AS bg BY ANCHOR ANCHOR_SECOND;
```

Output:

Copy code

```
:force:
WITH
ExpandOnCTE AS
(
SELECT
PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, pd) bg
FROM
table1,
TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', pd))))
)
SELECT
bg
FROM
table1,
ExpandOnCTE;
```

## ROW\_COUNT\_UDF

### Definition

Returns an array containing sequential numbers from 1 to the value returned by DIFF\_TIME\_PERIOD\_UDF.

Copy code

```
:force:
PUBLIC.ROW_COUNT_UDF(NROWS DOUBLE)
```

### Parameters

`NROWS` represents the total number of rows in a dataset as a decimal number (DOUBLE)

The value returned by the DIFF\_TIME\_PERIOD\_UDF function.

### Returns

An array that determines the number of rows required to replicate the functionality of the EXPAND ON clause.

### Usage example

Input:

Copy code

```
:force:
SELECT ROW_COUNT_UDF(DIFF_TIME_PERIOD_UDF('SECONDS','2022-11-26 10:15:20.000*2022-11-26 10:15:25.000'));
```

Output:

Copy code

```
:force:
[1, 2, 3, 4, 5]
```

### Migration example

Input:

Copy code

```
:force:
SELECT NORMALIZE emp_id, duration FROM project EXPAND ON duration AS bg BY ANCHOR ANCHOR_SECOND;
```

Output:

Copy code

```
:force:
WITH ExpandOnCTE AS
(
SELECT
    PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, duration) bg
FROM
    project,
TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', duration))))
)
SELECT NORMALIZE emp_id,
    duration
FROM
    project,
    ExpandOnCTE;
```

## CENTURY\_UDF

### Definition

Calculates the century for a given date.

Copy code

```
:force:
PUBLIC.CENTURY_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The input date used to determine the century.

### Returns

Returns the century number as a varchar for a given date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.CENTURY_UDF(DATE '1915-02-23');
```

Output:

Copy code

```
:force:
'20'
```

## TIME\_DIFFERENCE\_UDF

Warning

This UDF has been deprecated as Snowflake now provides a built-in equivalent function. For more details, please refer to the [TIMEDIFF documentation](/sql-reference/functions/timediff).

### Definition

Calculates the time interval between two given timestamps.

Copy code

```
:force:
PUBLIC.TIME_DIFFERENCE_UDF
(MINUEND TIME, SUBTRAHEND TIME, INPUT_PART VARCHAR)
```

### Parameters

`MINUEND` The time value from which `SUBTRAHEND` will be subtracted.

`SUBTRAHEND` The timestamp value to be subtracted from another timestamp

Time has been subtracted.

`INPUT_PART` is a variable of type VARCHAR that stores input data.

`EXTRACT_PART` is a variable of type VARCHAR that stores the extracted portion of a string.

Extract a numeric value from a time interval.

### Returns

A text value (VARCHAR) representing a specific time.

### Example

Input:

Copy code

```
:force:
select extract(day from (timestampColumn1 - timestampColumn2 day to hour)) from tableName;
```

Output:

Copy code

```
:force:
SELECT
EXTRACT_TIMESTAMP_DIFFERENCE_UDF(timestampColumn1, timestampColumn2, 'DAY TO HOUR', 'DAY')
                                 from
tableName;
```

## INTERVAL\_DIVIDE\_UDF

### Definition

A custom function (UDF) that performs interval division calculations.

Copy code

```
:force:
PUBLIC.INTERVAL_DIVIDE_UDF
(INPUT_PART VARCHAR(30), INPUT_VALUE VARCHAR(), INPUT_DIV INTEGER)
```

### Parameters

`INPUT_PART` is a variable of type VARCHAR that represents the input portion of the data.

The value that specifies the interval type, such as ‘YEAR TO MONTH’.

`INPUT_VALUE` VARCHAR

The time interval to be divided.

`INPUT_DIV` is an integer value that represents the input divisor.

The number that will be divided by another number.

### Returns

The output is calculated by dividing a time interval by a numeric value.

### Migration example

Input:

Copy code

```
:force:
SELECT INTERVAL '6-10' YEAR TO MONTH / 8;
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.INTERVAL_DIVIDE_UDF('YEAR TO MONTH', '6-10', 8);
```

## DAYNUMBER\_OF\_MONTH\_UDF

### Definition

The UDF determines which day of the month a given timestamp falls on. It functions similarly to Teradata’s DAYNUMBER\_OF\_MONTH(DATE, ‘ISO’) function.

Copy code

```
:force:
PUBLIC.DAYNUMBER_OF_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

A date value that will be used to determine the corresponding day of the month.

### Returns

A whole number from 1 to 31 (inclusive).

### Example

Input:

Copy code

```
:force:
SELECT DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'ISO');
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.DAYNUMBER_OF_MONTH_UDF(DATE'2022-12-22');
```

## LAST\_DAY\_DECEMBER\_OF\_ISO\_UDF

### Definition

UDF (User-Defined Function) that processes December 31st and returns the corresponding ISO year. This function is used as a component of the PUBLIC.YEAR\_END\_ISO\_UDF calculation.

Copy code

```
:force:
PUBLIC.LAST_DAY_DECEMBER_OF_ISO_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

To get the last day of December using the ISO year format, use December 31st.

### Returns

A date representing December 31st in ISO year format.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.LAST_DAY_DECEMBER_OF_ISO_UDF(DATE '2022-01-01');
```

Output:

Copy code

```
:force:
2021-12-31
```

## DATEADD\_UDF

Note

For better readability, we have simplified some sections of the code in this example.

### Definition

Function to Calculate the Sum of Two Dates

Copy code

```
:force:
PUBLIC.DATEADD_UDF(FIRST_DATE DATE, SECOND_DATE DATE)
```

### Parameters

`FIRST_DATE` represents a column of type DATE

The initial date value to be included.

`SECOND_DATE` represents a column of type DATE

Add the second date value together with first\_date.

### Returns

The result is a date calculated by combining both input parameters.

### Example

Input:

Copy code

```
:force:
SELECT
    CAST(CAST (COLUMNB AS DATE FORMAT 'MM/DD/YYYY') AS TIMESTAMP(0))
    +
    CAST (COLUMNA AS TIME(0) FORMAT 'HHMISS' )
FROM TIMEDIFF;
```

Output:

Copy code

```
:force:
SELECT
    PUBLIC.DATEADD_UDF(CAST(CAST(COLUMNB AS DATE) !!!RESOLVE EWI!!! /*** SSC-EWI-0033 - FORMAT 'MM/DD/YYYY' REMOVED, SEMANTIC INFORMATION NOT FOUND. ***/!!! AS TIMESTAMP(0)), PUBLIC.TO_INTERVAL_UDF(CAST(COLUMNA AS TIME(0)) !!!RESOLVE EWI!!! /*** SSC-EWI-0033 - FORMAT 'HHMISS' REMOVED, SEMANTIC INFORMATION NOT FOUND. ***/!!!))
    FROM
    TIMEDIFF;
```

## JULIAN\_TO\_DATE\_UDF

### Definition

A user-defined function (UDF) that converts a Julian Date format (YYYYDDD) into a standard Gregorian calendar date (YYYY-MM-DD).

Copy code

```
:force:
PUBLIC.JULIAN_TO_DATE_UDF(JULIAN_DATE CHAR(7))
```

### Parameters

`JULIAN_DATE` CHAR - A character data type used to store dates in Julian format.

The date to be converted from Julian format.

### Returns

Returns the date representation of the Julian date, or null if the conversion cannot be performed.

### Usage example

Input:

Copy code

```
:force:
SELECT JULIAN_TO_DATE_UDF('2022045');
```

Output:

Copy code

```
:force:
'2022-02-14'
```

### Migration example

Input:

Copy code

```
:force:
SELECT TO_DATE('2020002', 'YYYYDDD');
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.JULIAN_TO_DATE_UDF('2020002');
```

## FIRST\_DAY\_JANUARY\_OF\_ISO\_UDF

### Definition

The first day of January in the ISO calendar year, which is used by the `PUBLIC.YEAR_BEGIN_ISO_UDF` function to calculate its result.

Copy code

```
:force:
FUNCTION PUBLIC.FIRST_DAY_JANUARY_OF_ISO_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date that represents January 1st using the ISO calendar year format.

### Returns

A date representing January 1st of the specified ISO calendar year.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.FIRST_DAY_JANUARY_OF_ISO_UDF(DATE '2022-01-01');
```

Output:

Copy code

```
:force:
2021-01-01
```

## TIMESTAMP\_DIFFERENCE\_UDF

### Definition

How to Subtract Two Dates Using a User-Defined Function (UDF)

Copy code

```
:force:
PUBLIC.TIMESTAMP_DIFFERENCE_UDF
(MINUEND TIMESTAMP, SUBTRAHEND TIMESTAMP, INPUT_PART VARCHAR)
```

### Differences between Teradata and Snowflake date time subtraction

Teradata and Snowflake use different methods for date and time calculations. They differ in their syntax, output data types, and precision levels.

- **Syntax:** In Teradata, DATE, TIMESTAMP, and TIME subtraction uses a minus sign and interval to specify the result’s format. For more details, see <https://docs.teradata.com/r/w19R4KsuHIiEqyxz0WYfgA/7kLLsWrP0kHxbk3iida0mA>. Snowflake handles these operations differently using three functions:

  - DATEDIFF (works with all date types)
  - TIMESTAMPDIFF
  - TIMEDIFF
    Each function requires the two dates to compare and the date part to return. For DATE types, you can also use the minus sign, which returns the difference in days.
- **Return Type:** Teradata returns various Interval types (see <https://www.docs.teradata.com/r/T5QsmcznbJo1bHmZT2KnFw/z~5iW7rYVstcmNYbd6Dsjg>). Snowflake’s functions return an Integer representing the number of units. For details, see <https://docs.snowflake.com/en/sql-reference/functions/datediff.html>
- **Rounding:** The way DATEDIFF handles date parts may produce different results than Teradata. Check <https://docs.snowflake.com/en/sql-reference/functions/datediff.html#usage-notes> for specific rounding behavior.

Warning

When performing date calculations, results may differ by one day due to rounding or timezone differences.

### Parameters

`MINUEND` The timestamp value from which `SUBTRAHEND` will be subtracted.

The date being used as the starting point for subtraction.

`SUBTRAHEND` is a timestamp value that will be subtracted from another timestamp.

The date has been removed.

`INPUT_PART` is a variable of type VARCHAR (variable-length character string)

Parts that need to be returned.

### Returns

Format the string value based on the specified `INPUT_PART` parameter.

### Example

Input:

Copy code

```
:force:
select (timestampColumn1 - timestampColumn2 YEAR) from tableName;
```

Copy code

```
:force:
SELECT
(
PUBLIC.TIMESTAMP_DIFFERENCE_UDF(timestampColumn1, timestampColumn2, 'YEAR')) from
tableName;
```

## FIRST\_DAY\_OF\_MONTH\_ISO\_UDF

### Definition

The User-defined function (UDF) returns the first day of a given month in ISO format (YYYY-MM-DD).

Copy code

```
:force:
PUBLIC.FIRST_DAY_OF_MONTH_ISO_UDF(YEAR NUMBER, MONTH NUMBER)
```

### Parameters

`YEAR` is a numeric data type used to store a four-digit year value.

A numeric value representing a calendar year (e.g., 2023).

`MONTH` A numeric value representing a month (1-12)

A numeric value (1-12) representing a calendar month.

### Returns

Returns the first day of the current month in ISO format (YYYY-MM-DD).

### Example

Note

This UDF is a helper function that is used within the [**`DAYNUMBER_OF_MONTH_UDF`**](#daynumber_of_month_udf) function.

## INT\_TO\_DATE\_UDF

### Definition

UDF to Convert Numeric Values to Dates (Teradata Compatibility Function)

Copy code

```
:force:
PUBLIC.INT_TO_DATE_UDF(NUMERIC_EXPRESSION INTEGER)
```

### Parameters

`NUMERIC_EXPRESSION` represents a numeric value or expression that evaluates to an integer

A value that represents a date in a specific format, such as YYYY-MM-DD

### Returns

Number converted to a date format.

### Example

Input:

Copy code

```
:force:
SELECT * FROM table1
WHERE date_column > 1011219
```

Output:

Copy code

```
:force:
SELECT
* FROM
table1
WHERE date_column > PUBLIC.INT_TO_DATE_UDF( 1011219);
```

## NULLIFZERO\_UDF

### Definition

Replaces zero values with NULL in the data to prevent division by zero errors.

Copy code

```
:force:
PUBLIC.NULLIFZERO_UDF(NUMBER_TO_VALIDATE NUMBER)
```

### Parameters

`NUMBER_TO_VALIDATE` NUMBER

The number that needs to be validated.

### Returns

Returns null if the input number is zero; otherwise, returns the original number.

### Usage example

Copy code

```
:force:
SELECT NULLIFZERO_UDF(0);
```

Output:

Copy code

```
:force:
NULL
```

## DATE\_LONG\_UDF

### Definition

Converts a date into the format ‘Day, Month DD, YYYY’ (for example, ‘Monday, January 01, 2024’). This format matches Teradata’s DL date format element.

Copy code

```
:force:
PUBLIC.DATE_LONG_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date should be displayed in a long date format (for example: “September 15, 2023”).

### Returns

A `VARCHAR` data type that represents the Teradata DL format element.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATE_LONG_UDF(DATE '2021-10-26');
```

Output:

Copy code

```
:force:
'Tuesday, October 26, 2021'
```

## TD\_MONTH\_OF\_CALENDAR\_UDF

### Definition

The user-defined function (UDF) serves as a replacement for Teradata’s [TD\_MONTH\_OF\_CALENDAR](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Date-and-Time-Functions-and-Expressions/Calendar-Functions/td_month_of_calendar) function, providing the same functionality.

Copy code

```
:force:
PUBLIC.TD_MONTH_OF_CALENDAR_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

Date used to calculate the number of months elapsed since January 1, 1900.

### Returns

An integer representing the number of months between January 1, 1900 and the specified date

### Migration example

Input:

Copy code

```
:force:
SELECT TD_MONTH_OF_CALENDAR(DATE '2023-11-30')
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.TD_MONTH_OF_CALENDAR_UDF(DATE '2023-11-30');
```

## MONTH\_NAME\_LONG\_UDF

### Definition

A user-defined function (UDF) that converts a timestamp into its corresponding full month name.

Copy code

```
:force:
PUBLIC.MONTH_NAME_LONG_UDF(INPUT_DATE TIMESTAMP)
```

### Parameters

`INPUT` DATE

The timestamp should be converted to display the full month name.

### Returns

The name of the month in English.

## TD\_DAY\_OF\_CALENDAR\_UDF

### Definition

User-defined function (UDF) that replicates Teradata’s `TO_DAY_OF_CALENDAR` functionality

Copy code

```
:force:
PUBLIC.TD_DAY_OF_CALENDAR_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

Date used to calculate the number of days elapsed since January 1, 1900.

### Returns

An integer representing the number of days between January 1, 1900 and the `INPUT` date

### Migration example

Input:

Copy code

```
:force:
SELECT td_day_of_calendar(current_date)
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.TD_DAY_OF_CALENDAR_UDF(CURRENT_DATE());
```

## PERIOD\_TO\_TIME\_UDF

### Definition

Function that converts a Teradata PERIOD value to a TIME value, maintaining Teradata’s casting behavior.

Copy code

```
:force:
PERIOD_TO_TIME_UDF(PERIOD_VAL VARCHAR(22))
```

### Parameters

`PERIOD_VAL` represents a time period value

The time period that needs to be converted.

### Returns

The function returns a `TIME` value representing the `PERIOD`. If the conversion cannot be completed, it returns null.

### Usage example

Input:

Copy code

```
:force:
SELECT PERIOD_TO_TIME_UDF(PERIOD_UDF(CURRENT_TIME()));
```

Output:

Copy code

```
:force:
08:42:04
```

## INSTR\_UDF (STRING, STRING, DOUBLE, DOUBLE)

Warning

This user-defined function (UDF) accepts <mark style=”color:orange;”>**four**</mark> **input parameters**.

### Definition

Finds all instances where search\_string appears within source\_string.

Copy code

```
:force:
PUBLIC.INSTR_UDF(SOURCE_STRING STRING, SEARCH_STRING STRING, POSITION DOUBLE, OCCURRENCE DOUBLE)
```

### Parameters

`SOURCE_STRING` represents the input string that needs to be processed

The text string that will be searched.

`SEARCH_STRING` is a text value that you want to search for.

The text pattern that the function will look for and match.

`POSITION` DOUBLE - A numeric data type that stores decimal numbers with double precision.

The position in the text where the search will begin (starting from position 1).

`OCCURRENCE` DOUBLE - A numeric data type that represents the number of times an event occurs, stored as a double-precision floating-point number.

The occurrence number to search for (for example, 2 finds the second match).

### Returns

The index position where the specified text is found within the source string.

### Usage example

Input:

Copy code

```
:force:
SELECT INSTR_UDF('CHOOSE A CHOCOLATE CHIP COOKIE','CH',2,2);
```

Output:

Copy code

```
:force:
20
```

## ROUND\_DATE\_UDF

### Definition

A user-defined function (UDF) that processes a DATE\_VALUE by rounding the time portion to a specified unit (UNIT\_TO\_ROUND\_BY). This function is similar to the Teradata ROUND(date) function.

Copy code

```
:force:
PUBLIC.ROUND_DATE_UDF(DATE_TO_ROUND TIMESTAMP_LTZ, UNIT_TO_ROUND_BY VARCHAR(5))
```

### Parameters

`DATE_TO_ROUND` TIMESTAMP\_TZ (A timestamp value with timezone information that needs to be rounded)

The date value that needs to be rounded.

`UNIT_TO_ROUND_BY` VARCHAR - Specifies the time unit used for rounding

The time unit used for rounding the date.

### Returns

Returns a date rounded to the specified time unit. The UNIT\_TO\_ROUND\_BY parameter determines how the date will be rounded.

### Migration example

Input:

Copy code

```
:force:
SELECT ROUND(CURRENT_DATE, 'RM') RND_DATE
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.ROUND_DATE_UDF(CURRENT_DATE(), 'RM') RND_DATE;
```

## SUBSTR\_UDF (STRING, FLOAT, FLOAT)

Warning

This is the user-defined function (UDF) that accepts <mark style=”color:orange;”>**three**</mark> **parameters**.

### Definition

Retrieves a portion of text from a specified string by using starting and ending positions.

Copy code

```
:force:
PUBLIC.SUBSTR_UDF(BASE_EXPRESSION STRING, START_POSITION FLOAT, LENGTH FLOAT)
```

### Parameters

`BASE_EXPRESSION` is a string parameter that defines the base expression.

The source text from which you want to extract a portion.

`START_POSITION` is a floating-point number that defines the initial position.

The position where you want to begin extracting characters from the string.

`LENGTH` is a floating-point number that represents the length value.

The position where you want to begin extracting characters from the string.

### Returns

The substring that must be included.

### Usage example

Input:

Copy code

```
:force:
SELECT
    PUBLIC.SUBSTR_UDF('ABC', -1, 1),
    PUBLIC.SUBSTR_UDF('ABC', -1, 2),
    PUBLIC.SUBSTR_UDF('ABC', -1, 3),
    PUBLIC.SUBSTR_UDF('ABC', 0, 1),
    PUBLIC.SUBSTR_UDF('ABC', 0, 2);
```

Output:

Copy code

```
:force:
'','','A','','A'
```

## GETQUERYBANDVALUE\_UDF (VARCHAR)

Warning

This is the user-defined function (UDF) that accepts <mark style=”color:orange;”>**one**</mark> **parameter**.

### Definition

Returns a value from a name-value pair stored in the transaction, session, or profile query band.

Copy code

```
:force:
GETQUERYBANDVALUE_UDF(SEARCHNAME VARCHAR)
```

### Parameters

`SEARCHNAME` VARCHAR - A variable of type VARCHAR used to store search terms or names.

The name to search for within the key-value pairs.

### Returns

The session query band’s “name” key value, or null if not present.

### Usage example

Input:

Copy code

```
:force:
ALTER SESSION SET QUERY_TAG = 'user=Tyrone;role=security';
SELECT GETQUERYBANDVALUE_UDF('role');
```

Output:

Copy code

```
:force:
security
```

### Migration example

Input:

Copy code

```
:force:
SELECT GETQUERYBANDVALUE(1, 'group');
```

Output:

Copy code

```
:force:
/** MSC-ERROR - MSCEWI2084 - TRANSACTION AND PROFILE LEVEL QUERY TAGS NOT SUPPORTED IN SNOWFLAKE, REFERENCING SESSION QUERY TAG INSTEAD **/
SELECT GETQUERYBANDVALUE_UDF('group');
```

## TD\_WEEK\_OF\_YEAR\_UDF

### Definition

User-defined function (UDF) that calculates the full week number of a given date within the year. This function provides the same functionality as Teradata’s `TD_WEEK_OF_YEAR` and `WEEKNUMBER_OF_YEAR` functions.

Copy code

```
:force:
PUBLIC.TD_WEEK_OF_YEAR_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

Date used to calculate the week number.

### Returns

A numerical value indicating which week of the year the specified date falls into.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.TD_WEEK_OF_YEAR_UDF(DATE '2024-05-10'),
PUBLIC.TD_WEEK_OF_YEAR_UDF(DATE '2020-01-03')
```

Output:

Copy code

```
:force:
18, 0
```

## EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF

Note

For better readability, we have simplified the code examples by showing only the most relevant parts.

### Definition

Retrieves the ‘Data’ portion from the result of subtracting `SUBTRAHEND` from `MINUEND`

Copy code

```
:force:
PUBLIC.EXTRACT_TIMESTAMP_DIFFERENCE_UDF
(MINUEND TIMESTAMP, SUBTRAHEND TIMESTAMP, INPUT_PART VARCHAR, EXTRACT_PART VARCHAR)
```

### Differences between Teradata and Snowflake date-time extraction

Teradata and Snowflake functions may have different parameter requirements and return different data types.

- **Parameters:** The key distinction between Teradata and Snowflake’s EXTRACT functions is that Snowflake only works with dates and times, while Teradata also supports intervals. For more details, refer to [Snowflake’s EXTRACT function documentation](https://docs.snowflake.com/en/sql-reference/functions/extract.html) and [Teradata’s EXTRACT function documentation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/SIkE2wnHyQBnU4AGWRZSRw).
- **Return type:** The functions return values differently: Teradata’s EXTRACT returns either an integer or decimal(8, 2), while Snowflake’s EXTRACT returns a number representing the requested date-time part.

Teradata and Snowflake functions may have different input parameters and output types.

### Parameters

`MINUEND` TIMESTAMP

The date being used as the starting point for subtraction.

`SUBTRAHEND` The timestamp value to be subtracted from another timestamp

The date has been removed.

`INPUT_PART` VARCHAR

The formatted varchar must match the original requested part (which is the same as `TIMESTAMP_DIFFERENCE` `INPUT_PART`) and must be one of the following:

- `'DAY TO HOUR'`
- `'DAY TO MINUTE'`
- `'DAY TO SECOND'`
- `'DAY TO MINUTE'`
- `'HOUR TO MINUTE'`
- `'HOUR TO SECOND'`
- `'MINUTE TO SECOND'`

`EXTRACT_PART` is a VARCHAR data type that represents the extracted portion of a string.

The time unit for extraction must be one of the following values: `'DAY'`, `'HOUR'`, `'MINUTE'`, or `'SECOND'`. The requested time unit should fall within the input time interval.

### Returns

The number of requests included in the extraction process.

### Example

Input:

Copy code

```
:force:
select extract(day from (timestampColumn1 - timestampColumn2 day to hour)) from tableName;
```

Output:

Copy code

```
:force:
SELECT
EXTRACT_TIMESTAMP_DIFFERENCE_UDF(timestampColumn1, timestampColumn2, 'DAY TO HOUR', 'DAY')
from
tableName;
```

## JSON\_EXTRACT\_DOT\_NOTATION\_UDF

### Definition

A user-defined function (UDF) that allows you to query JSON objects using dot notation, similar to how you would access nested properties in JavaScript or Python.

Copy code

```
:force:
JSON_EXTRACT_DOT_NOTATION_UDF(JSON_OBJECT VARIANT, JSON_PATH STRING)
```

### Differences between Teradata JSON Entity Reference (dot notation ) and Snowflake JSON query method.

Teradata and Snowflake use different methods to traverse JSON data. Teradata uses a JavaScript-based approach with dot notation, array indexing, and special operators like wildcard access and double dot notation. In contrast, Snowflake has more limited JSON traversal capabilities, only supporting direct member access and array indexing.

### Parameters

`JSON_OBJECT` A data type that represents a JSON object, which can contain nested key-value pairs of varying data types.

The JSON object containing the values you want to extract.

`JSON_PATH` A string parameter that specifies the path to extract data from a JSON document

The location within the JSON\_OBJECT where the values can be found, specified using JSON path notation.

### Returns

The data elements within the JSON\_OBJECT that match the specified JSON\_PATH.

### Migration example

Input:

Copy code

```
:force:
SELECT CAST(varcharColumn AS JSON(2000))..name FROM variantTest;
```

Output:

Copy code

```
:force:
SELECT
JSON_EXTRACT_DOT_NOTATION_UDF(CAST(varcharColumn AS VARIANT), '$..name')
FROM
variantTest;
```

## WEEK\_OF\_MONTH\_UDF

### Definition

Calculates which week of the month a specific date falls into.

Copy code

```
:force:
PUBLIC.WEEK_OF_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date used to determine which week of the month it falls into.

### Returns

A VARCHAR column that displays which week of the month a specific date falls in.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.WEEK_OF_MONTH_UDF(DATE '2021-10-26');
```

Output:

Copy code

```
:force:
'4'
```

## DAYNAME\_LONG\_UDF (TIMESTAMP\_TZ)

Warning

This is the user-defined function (UDF) that accepts <mark style=”color:orange;”>**one**</mark> **parameter**.

### Definition

UDF that creates a variant of the DAYNAME\_LONG\_UDF function which returns day names with the first letter capitalized (default format).

Copy code

```
:force:
PUBLIC.DAYNAME_LONG_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date from which you want to get the day of the week.

### Returns

Returns a string containing the full name of a day of the week.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DAYNAME_LONG_UDF(DATE '2022-06-30');
```

Output:

Copy code

```
:force:
'Thursday'
```

## INTERVAL\_TO\_MONTHS\_UDF

### Definition

Converts a time interval into months.

Copy code

```
:force:
PUBLIC.INTERVAL_TO_MONTHS_UDF
(INPUT_VALUE VARCHAR())
```

### Parameters

`INPUT_VALUE` VARCHAR

The time period that will be changed into months.

### Returns

The number of months to be processed, specified as an integer.

## GETQUERYBANDVALUE\_UDF (VARCHAR, FLOAT, VARCHAR)

Warning

This user-defined function (UDF) accepts three parameters.

### Definition

Returns a value from a name-value pair stored in the transaction, session, or profile query band. The value is associated with a specific name in the query band.

Copy code

```
:force:
GETQUERYBANDVALUE_UDF(QUERYBAND VARCHAR, SEARCHTYPE FLOAT, SEARCHNAME VARCHAR)
```

### Parameters

`QUERYBAND` is a VARCHAR data type that stores query band information.

The query band combines transaction, session, and profile query bands into a single string.

`SEARCHTYPE` is a floating-point number data type.

The maximum depth at which matching pairs will be searched.

0 represents a wildcard value that matches any input.

A transaction represents a single unit of work in a database.

A Session object represents a connection to Snowflake.

3 = Create a profile.

`SEARCHNAME` VARCHAR

The name to search for within the key-value pairs.

### Returns

Returns the value of the ‘name’ key at the specified level in the hierarchy. If no value is found, returns null.

### Usage example

Input:

Copy code

```
:force:
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 0, 'account');
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 2, 'account');
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 0, 'role');
SELECT GETQUERYBANDVALUE_UDF('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 1, 'role');
```

Output:

Copy code

```
:force:
      Matt
      SaraDB
      DbAdmin
      NULL
```

### Migration example

Input:

Copy code

```
:force:
SELECT GETQUERYBANDVALUE('=T> account=Matt;user=Matt200; =S> account=SaraDB;user=Sara;role=DbAdmin;', 0, 'account')
```

Output:

Copy code

```
:force:
WITH
--** MSC-WARNING - MSCEWI2078 - THE EXPAND ON CLAUSE FUNCTIONALITY IS TRANSFORMED INTO A CTE BLOCK **
ExpandOnCTE AS
(
SELECT
PUBLIC.EXPAND_ON_UDF('ANCHOR_SECOND', VALUE, duration) bg
FROM
project,
TABLE(FLATTEN(PUBLIC.ROW_COUNT_UDF(PUBLIC.DIFF_TIME_PERIOD_UDF('ANCHOR_SECOND', duration))))
)
SELECT NORMALIZE emp_id,
duration
FROM
project,
ExpandOnCTE;
```

## JULIAN\_DAY\_UDF

### Definition

Calculates the Julian day number, which represents the continuous count of days since January 1, 4713 BCE (Before Common Era). The Julian day is used in astronomy and calendar calculations.

Copy code

```
:force:
PUBLIC.JULIAN_DAY_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date that will be converted to a Julian day number.

### Returns

A `varchar` value representing the calculated Julian date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.JULIAN_DAY_UDF(DATE '2021-10-26');
```

Output:

Copy code

```
:force:
'2459514'
```

## WEEKNUMBER\_OF\_MONTH\_UDF

### Definition

Identify the week number of the month from a given date.

Copy code

```
:force:
PUBLIC.WEEKNUMBER_OF_MONTH_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date from which to calculate the week of the month.

### Returns

A numeric value representing the week of the month (1-4) for the given date.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.WEEKNUMBER_OF_MONTH_UDF(DATE '2022-05-21')
```

Output:

Copy code

```
:force:
3
```

## JSON\_EXTRACT\_UDF

### Definition

A user-defined function (UDF) that mimics the behavior of `JSONExtract`, `JSONExtractValue`, and `JSONExtractLargeValue` functions. This UDF allows you to extract multiple values from a JSON object.

Copy code

```
:force:
JSON_EXTRACT_UDF(JSON_OBJECT VARIANT, JSON_PATH STRING, SINGLE_VALUE BOOLEAN)
```

### Parameters

`JSON_OBJECT` is a data type that stores JSON-formatted data in a structured format.

The JSON object containing the values you want to extract.

`JSON_PATH` A string that specifies the path to extract data from a JSON document

The location within the JSON\_OBJECT where the desired values can be found, specified using JSON path notation.

`SINGLE_VALUE` A boolean flag that indicates whether to return a single value or multiple values.

BOOLEAN parameter: When set to true, returns a single value (required for JSONExtractValue and JSONExtractLargeValue functions). When set to false, returns an array of values (used with JSONExtract).

### Returns

The data values found at the specified JSON path within the JSON object.

### Migration example

Input:

Copy code

```
:force:
SELECT
    Store.JSONExtract('$..author') as AllAuthors
FROM BookStores;
```

Output:

Copy code

```
:force:
SELECT
    JSON_EXTRACT_UDF(Store, '$..author', FALSE) as AllAuthors
    FROM
    BookStores;
```

## COMPUTE\_EXPAND\_ON\_UDF

### Definition

Determines how to expand data based on the specified time period type.

Copy code

```
:force:
PUBLIC.COMPUTE_EXPAND_ON_UDF(TIME STRING, SEQ NUMBER, PERIOD TIMESTAMP, PERIODTYPE STRING)
```

### Parameters

`TIME` STRING

The timestamp used in the anchor.

`SEQ` sequence number

The order in which each row’s calculations are performed.

`PERIOD` represents a timestamp value that indicates a specific point in time.

The date for the specified time period.

`PERIODTYPE` is a string value that defines the type of time period.

The time period used for the calculation (either ‘`BEGIN`’ or ‘`END`’)

### Returns

A timestamp indicating when each row in the EXPAND-ON operation was processed.

### Example

Warning

This UDF is a derived function that extends the functionality of [EXPAND\_ON\_UDF](#expand_on_udf).

## WEEK\_NUMBER\_OF\_QUARTER\_UDF

### Definition

Returns the week number within the current quarter for a specified date. This function follows the same behavior as Teradata’s `WEEKNUMBER_OF_QUARTER(DATE, 'ISO')` function, using the ISO calendar system.

Copy code

```
:force:
PUBLIC.WEEK_NUMBER_OF_QUARTER_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The date used to calculate which week of the quarter it falls into.

### Returns

An integer indicating which week of the quarter (1-13) is being referenced.

### Usage example

Input:

Copy code

```
:force:
SELECT WEEK_NUMBER_OF_QUARTER_UDF(DATE '2023-01-01'),
WEEK_NUMBER_OF_QUARTER_UDF(DATE '2022-10-27')
```

Output:

Copy code

```
:force:
1, 4
```

## YEAR\_END\_ISO\_UDF

### Definition

User-defined function (UDF) that calculates the last day of the year for a given date using ISO calendar standards, similar to Teradata’s TD\_YEAR\_END function.

Copy code

```
:force:
PUBLIC.YEAR_END_ISO_UDF(INPUT date)
```

### Parameters

`INPUT` DATE

The date that represents the last day of the year according to the ISO calendar standard.

### Returns

The last day of the year according to the ISO calendar system.

### Usage example

Input:

Copy code

```
:force:
SELECT  PUBLIC.YEAR_END_ISO_UDF(DATE '2022-01-01'),
PUBLIC.YEAR_END_ISO_UDF(DATE '2022-04-12');
```

Output:

Copy code

```
:force:
2022-01-02, 2023-01-01
```

## INSERT\_CURRENCY\_UDF

### Definition

Insert the currency symbol directly before the first digit of the number to ensure there are no spaces or symbols between the currency symbol and the number.

Copy code

```
:force:
PUBLIC.INSERT_CURRENCY_UDF(INPUT VARCHAR, CURRENCYINDEX INTEGER, CURRENCYVALUE VARCHAR)
```

### Parameters

`INPUT` VARCHAR

The output of TO\_CHAR when converting a numeric value that requires currency formatting.

`CURRENCYINDEX` is an integer value that represents the index of a currency.

The position in the array where the currency should be inserted.

`CURRENCYVALUE` A VARCHAR field that stores currency values

The text that will be used as the currency value.

### Returns

A `varchar` field containing the currency text at a defined position.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.INSERT_CURRENCY_UDF(to_char(823, 'S999999'), '1', 'CRC');
```

Output:

Copy code

```
:force:
'+CRC823'
```

## INSTR\_UDF (STRING, STRING, INT)

Warning

This user-defined function (UDF) accepts three parameters.

### Definition

Finds all instances where search\_string appears within source\_string.

Copy code

```
:force:
PUBLIC.INSTR_UDF(SOURCE_STRING STRING, SEARCH_STRING STRING, POSITION INT)
```

### Parameters

`SOURCE_STRING` represents a string value that will be used as input

The text that will be searched.

`SEARCH_STRING` is a text value that you want to search for.

The text pattern that the function will look for and match.

`POSITION` is an integer data type that represents a position in a sequence.

The position in the text where the search begins (starting from position 1).

### Returns

The location within the original string where the match is found.

### Usage example

Input:

Copy code

```
:force:
SELECT INSTR_UDF('FUNCTION','N', 3);
```

Output:

Copy code

```
:force:
8
```
