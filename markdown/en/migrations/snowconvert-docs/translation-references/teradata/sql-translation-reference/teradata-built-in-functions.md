# Teradata - Built-in Functions

This page provides a description of the translation for the built-in functions in Teradata to Snowflake

Note

This page only lists the functions that are already transformed, if a function from the Teradata documentation is not listed there then it should be taken as unsupported.

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../../general/built-in-functions).

Note

Some Teradata functions do not have a direct equivalent in Snowflake so they are transformed into a functional equivalent UDF, these can be easily spotted by the \_UDF postfix in the name of the function. For more information on the UDFs used, check this [git repository](https://github.com/MobilizeNet/SnowConvert_Support_Library/tree/main/UDFs).

## Aggregate Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| AVG | AVG |  |
| CORR | CORR |  |
| COUNT | COUNT |  |
| COVAR\_POP | COVAR\_POP |  |
| COVAR\_SAMP | COVAR\_SAMP |  |
| GROUPING | GROUPING |  |
| KURTOSIS | KURTOSIS |  |
| MAXIMUM  MAX | MAX |  |
| MINIMUM  MIN | MIN |  |
| PIVOT | PIVOT | Check [PIVOT.](#pivot) |
| REGR\_AVGX | REGR\_AVGX |  |
| REGR\_AVGY | REGR\_AVGY |  |
| REGR\_COUNT | REGR\_COUNT |  |
| REGR\_INTERCEPT | REGR\_INTERCEPT |  |
| REGR\_R2 | REGR\_R2 |  |
| REGR\_SLOPE | REGR\_SLOPE |  |
| REGR\_SXX | REGR\_SXX |  |
| REGR\_SXY | REGR\_SXY |  |
| REGR\_SYY | REGR\_SYY |  |
| SKEW | SKEW |  |
| STDDEV\_POP | STDDEV\_POP |  |
| STDDEV\_SAMP | STDDEV\_SAMP |  |
| SUM | SUM |  |
| UNPIVOT | UNPIVOT | Unpivot with multiple functions not supported in Snowflake |
| VAR\_POP | VAR\_POP |  |
| VAR\_SAMP | VAR\_SAMP |  |

Expand

Show lessSee more

> See [Aggregate functions​](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Aggregate-Functions)

## Arithmetic, Trigonometric, Hyperbolic Operators/Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ABS | ABS |  |
| CEILING | CEIL |  |
| DEGREES | DEGREES |  |
| EXP | EXP |  |
| FLOOR | FLOOR |  |
| ***HYPERBOLIC***  ACOSH  ASINH  ATANH  COSH  SINH  TANH | ***HYPERBOLIC***  ACOSH  ASINH  ATANH  COSH  SINH  TANH |  |
| LOG | LOG |  |
| LN | LN |  |
| MOD | MOD |  |
| NULLIFZERO(param) | CASE WHEN param=0 THEN null ELSE param END |  |
| POWER | POWER |  |
| RANDOM | RANDOM |  |
| RADIANS | RADIANS |  |
| ROUND | ROUND |  |
| SIGN | SIGN |  |
| SQRT | SQRT |  |
| TRUNC | TRUNC\_UDF |  |
| ***TRIGONOMETRIC***  ACOS  ASIN  ATAN  ATAN2  COS  SIN  TAN | ***TRIGONOMETRIC***  ACOS  ASIN  ATAN  ATAN2  COS  SIN  TAN |  |
| ZEROIFNULL | ZEROIFNULL |  |

Expand

Show lessSee more

> See [Arithmetic, Trigonometric, Hyperbolic Operators/Functions](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Arithmetic-Trigonometric-Hyperbolic-Operators/Functions)​

## Attribute Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| BIT\_LENGTH | BIT\_LENGTH |  |
| BYTE  BYTES | LENGTH |  |
| CHAR  CHARS  CHARACTERS | LEN |  |
| CHAR\_LENGTH  CHARACTER\_LENGTH | LEN |  |
| MCHARACTERS | LENGTH |  |
| OCTECT\_LENGTH | OCTECT\_LENGTH |  |

Expand

Show lessSee more

> See [Attribute functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Attribute-Functions)

## Bit/Byte Manipulation Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| BITAND | BITAND |  |
| BITNOT | BITNOT |  |
| BITOR | BITOR |  |
| BITXOR | BITXOR |  |
| GETBIT | GETBIT |  |

Expand

Show lessSee more

> See [Bit/Byte functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Bit/Byte-Manipulation-Functions)

## Built-In (System Functions)

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ACCOUNT | CURRENT\_ACCOUNT |  |
| CURRENT\_DATE  CURDATE | CURRENT\_DATE |  |
| CURRENT\_ROLE | CURRENT\_ROLE |  |
| CURRENT\_TIME CURTIME | CURRENT\_TIME |  |
| CURRENT\_TIMESTAMP | CURRENT\_TIMESTAMP |  |
| DATABASE | CURRENT\_DATABASE |  |
| DATE | CURRENT\_DATE |  |
| NOW | CURRENT\_TIMESTAMP |  |
| PROFILE | CURRENT\_ROLE | Check [SSC-EWI-TD0068](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0068) for more details on this transformation |
| SESSION | CURRENT\_SESSION |  |
| TIME | CURRENT\_TIME |  |
| USER | CURRENT\_USER |  |

Expand

Show lessSee more

> See [Built-In Functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Built-In-Functions)

## Business Calendars

| Teradata | Snowflake | Note |
| --- | --- | --- |
| DAYNUMBER\_OF\_MONTH(DatetimeValue, ‘COMPATIBLE’) | DAYOFMONTH |  |
| DAYNUMBER\_OF\_MONTH(DatetimeValue, ‘ISO’) | DAYNUMBER\_OF\_MONTH\_ISO\_UDF |  |
| DAYNUMBER\_OF\_MONTH(DatetimeValue, ‘TERADATA’) | DAYOFMONTH |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘ISO’) | DAYOFWEEKISO |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘COMPATIBLE’) | DAY\_OF\_WEEK\_COMPATIBLE\_UDF |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘TERADATA’) DAYNUMBER\_OF\_WEEK(DatetimeValue) | TD\_DAY\_OF\_WEEK\_UDF |  |
| DAYNUMBER\_OF\_YEAR(DatetimeValue, ‘ISO’) | PUBLIC.DAY\_OF\_YEAR\_ISO\_UDF |  |
| DAYNUMBER\_OF\_YEAR(DatetimeValue) | DAYOFYEAR |  |
| QUARTERNUMBER\_OF\_YEAR | QUARTER |  |
| TD\_SUNDAY(DateTimeValue) | PREVIOUS\_DAY(DateTimeValue, ‘Sunday’) |  |
| WEEKNUMBER\_OF\_MONTH | WEEKNUMBER\_OF\_MONTH\_UDF |  |
| WEEKNUMBER\_OF\_QUARTER(dateTimeValue) | WEEKNUMBER\_OF\_QUARTER\_UDF |  |
| WEEKNUMBER\_OF\_QUARTER(dateTimeValue, ‘ISO’) | WEEKNUMBER\_OF\_QUARTER\_ISO\_UDF |  |
| WEEKNUMBER\_OF\_QUARTER(dateTimeValue, ‘COMPATIBLE’) | WEEKNUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF |  |
| WEEKNUMBER\_OF\_YEAR(DateTimeValue, ‘ISO’) | WEEKISO |  |
| YEARNUMBER\_OF\_CALENDAR(DATETIMEVALUE, ‘COMPATIBLE’) | YEAR |  |
| YEARNUMBER\_OF\_CALENDAR(DATETIMEVALUE, ‘ISO’) | YEAROFWEEKISO |  |

Expand

Show lessSee more

> See [Business Calendars](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Date-and-Time-Functions-and-Expressions-17.20/Business-Calendars)

## Calendar Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| DAYNUMBER\_OF\_WEEK(DatetimeValue) | TD\_DAY\_OF\_WEEK\_UDF |  |
| DAYNUMBER\_OF\_WEEK(DatetimeValue, ‘COMPATIBLE’) | DAY\_OF\_WEEK\_COMPATIBLE\_UDF |  |
| QuarterNumber\_Of\_Year(DatetimeValue, ‘ISO’) | QUARTER\_OF\_YEAR\_ISO\_UDF(DatetimeValue) |  |
| TD\_DAY\_OF\_CALENDAR | TD\_DAY\_OF\_CALENDAR\_UDF |  |
| TD\_DAY\_OF\_MONTH DAYOFMONTH | DAYOFMONTH |  |
| TD\_DAY\_OF\_WEEK DAYOFWEEK | TD\_DAY\_OF\_WEEK\_UDF |  |
| TD\_DAY\_OF\_YEAR | DAYOFYEAR |  |
| TD\_MONTH\_OF\_CALENDAR(DateTimeValue) MONTH\_CALENDAR(DateTimeValue) | TD\_MONTH\_OF\_CALENDAR\_UDF(DateTimeValue) |  |
| TD\_WEEK\_OF\_CALENDAR(DateTimeValue) WEEK\_OF\_CALENDAR(DateTimeValue) | TD\_WEEK\_OF\_CALENDAR\_UDF(DateTimeValue) |  |
| TD\_WEEK\_OF\_YEAR | WEEK\_OF\_YEAR\_UDF |  |
| TD\_YEAR\_BEGIN(DateTimeValue) | YEAR\_BEGIN\_UDF(DateTimeValue) |  |
| TD\_YEAR\_BEGIN(DateTimeValue, ‘ISO’) | YEAR\_BEGIN\_ISO\_UDF(DateTimeValue) |  |
| TD\_YEAR\_END(DateTimeValue) | YEAR\_END\_UDF(DateTimeValue) |  |
| TD\_YEAR\_END(DateTimeValue, ‘ISO’) | YEAR\_END\_ISO\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_MONTH(DateTimeValue) | WEEKNUMBER\_OF\_MONTH\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_QUARTER(DateTimeValue) | WEEKNUMBER\_OF\_QUARTER\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_QUARTER(DateTimeValue, ‘ISO’) | WEEKNUMBER\_OF\_QUARTER\_ISO\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_QUARTER(DateTimeValue, ‘COMPATIBLE’) | WEEKNUMBER\_OF\_QUARTER\_COMPATIBLE\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_YEAR(DateTimeValue) | WEEK\_OF\_YEAR\_UDF(DateTimeValue) |  |
| WEEKNUMBER\_OF\_YEAR(DateTimeValue, ‘COMPATIBLE’) | WEEK\_OF\_YEAR\_COMPATIBLE\_UDF(DateTimeValue) |  |

Expand

Show lessSee more

> See [Calendar Functions](https://docs.teradata.com/r/WX0vkeB8F3JQXZ0HTR~d0Q/~8TzAjUr3AFwohWtu8ndxQ)

## Case Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| COALESCE | COALESCE | Check [Coalesce](#coalesce). |
| NULLIF | NULLIF |  |

Expand

Show lessSee more

> See [case functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/CASE-Expressions)

## Comparison Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| DECODE | DECODE |  |
| GREATEST | GREATEST |  |
| LEAST | LEAST |  |

Expand

Show lessSee more

> See [comparison functions](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Comparison-Operators-and-Functions)

## Data type conversions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| CAST | CAST |  |
| CAST(DatetimeValue AS INT) | DATE\_TO\_INT\_UDF |  |
| CAST (VarcharValue AS INTERVAL) | INTERVAL\_UDF | Check [Cast to INTERVAL datatype](#cast-to-interval-datatype) |
| TRYCAST | TRY\_CAST |  |
| FROM\_BYTES | TO\_NUMBER TO\_BINARY | [FROM\_BYTES](#from_bytes) with ASCII parameter not supported in Snowflake. |

Expand

Show lessSee more

> See [Data Type Conversions](https://docs.teradata.com/reader/~_sY_PYVxZzTnqKq45UXkQ/iZ57TG_CtznEu1JdSbFNsQ)

## Data Type Conversion Functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| TO\_BYTES(Input, ‘Base10’) | INT2HEX\_UDF(Input) |  |
| TO\_NUMBER | TO\_NUMBER |  |
| TO\_CHAR | TO\_CHAR or equivalent expression | Check [TO\_CHAR](#to_char). |
| TO\_DATE | TO\_DATE |  |
| TO\_DATE(input, ‘YYYYDDD’) | JULIAN\_TO\_DATE\_UDF |  |

Expand

Show lessSee more

> See [Data Type Conversion Functions](https://docs.teradata.com/r/Teradata-VantageTM-Data-Types-and-Literals/March-2019/Data-Type-Conversion-Functions)

## DateTime and Interval functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ADD\_MONTHS | ADD\_MONTHS |  |
| EXTRACT | EXTRACT |  |
| LAST\_DAY | LAST\_DAY |  |
| MONTH | MONTH |  |
| MONTHS\_BETWEEN | MONTHS\_BETWEEN\_UDF |  |
| NEXT\_DAY | NEXT\_DAY |  |
| OADD\_MONTHS | ADD\_MONTHS |  |
| ROUND(Numeric) | ROUND |  |
| ROUND(Date) | ROUND\_DATE\_UDF |  |
| TRUNC(Date) | TRUNC\_UDF |  |
| YEAR | YEAR |  |

Expand

Show lessSee more

> See [DateTime and Interval Functions and Expressions](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/JhmMJqd9vWURvHYeTRgQLQ)

## Hash functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| HASH\_MD5 | MD5 |  |
| HASHAMP  HASHBACKAM  HASHBUCKET  HASHROW | Not supported | Check notes on [the architecture differences between Teradata and Snowflake](#architecture-differences-between-teradata-and-snowflake) |

Expand

Show lessSee more

> See [Hash functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw)

## JSON functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| NEW JSON | TO\_JSON(PARSE\_JSON()**)** | Check [NEW JSON](#new-json) |
| JSON\_CHECK | CHECK\_JSON | Check JSON\_CHECK |
| JSON\_TABLE | Equivalent query | Check [JSON\_TABLE](#json_table) |
| JSONExtract  JSONExtractValue JSONExtractLargeValue | JSON\_EXTRACT\_UDF | Check [JSON\_EXTRACT](#json_extract) |

Expand

Show lessSee more

> See [JSON documentation](https://docs.teradata.com/r/C8cVEJ54PO4~YXWXeXGvsA/_aeoMCG0XgMNegNj0oy5cg)

## Null-Handling functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| NVL | NVL |  |
| NVL2 | NVL2 |  |

Expand

Show lessSee more

> See [Null-Handling functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/4di35TY_6SqRNEGk4vv0ww)

## Ordered Analytical/Window Aggregate functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| CSUM(col1, col2) | SUM(col\_1) OVER (PARTITION BY null ORDER BY col\_2 ROWS UNBOUNDED PRECEDING) |  |
| CUME\_DIST | CUME\_DIST |  |
| DENSE\_RANK | DENSE\_RANK |  |
| FIRST\_VALUE | FIRST\_VALUE |  |
| LAG | LAG |  |
| LAST\_VALUE | LAST\_VALUE |  |
| LEAD | LEAD |  |
| MAVG(csales, 2, cdate, csales) | AVG(csales) OVER ( ORDER BY cdate, csales ROWS 1 PRECEDING) |  |
| MEDIAN | MEDIAN |  |
| MSUM(csales, 2, cdate, csales) | SUM(csales) OVER(ORDER BY cdate, csales ROWS 1 PRECEDING) |  |
| PERCENT\_RANK | PERCENT\_RANK |  |
| PERCENTILE\_CONT | PERCENTILE\_CONT |  |
| PERCENTILE\_DISC | PERCENTILE\_DISC |  |
| QUANTILE | QUANTILE |  |
| RANK | RANK |  |
| ROW\_NUMBER | ROW\_NUMBER |  |

Expand

Show lessSee more

> See [Window functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/qbFqalW6IF5Fryz47~iqJQ)

## Period functions and operators

| Teradata | Snowflake | Note |
| --- | --- | --- |
| BEGIN | PERIOD\_BEGIN\_UDF |  |
| END | PERIOD\_END\_UDF |  |
| INTERVAL | TIMESTAMPDIFF |  |
| LAST | PERIOD\_LAST\_UDF |  |
| LDIFF | PERIOD\_LDIFF\_UDF |  |
| OVERLAPS | PUBLIC.PERIOD\_OVERLAPS\_UDF |  |
| PERIOD | PERIOD\_UDF |  |
| PERIOD(datetimeValue, UNTIL\_CHANGED)  PERIOD(datetimeValue, UNTIL\_CLOSED) | PERIOD\_UDF(datetimeValue, ’9999-12-31 23:59:59.999999’) | See notes about [ending bound constants](#ending-bound-constants-until_changed-and-until_closed) |
| RDIFF | PERIOD\_RDIFF\_UDF |  |

Expand

Show lessSee more

> See [Period Functions and Operators](https://docs.teradata.com/r/Teradata-Database-SQL-Functions-Operators-Expressions-and-Predicates/June-2017/Period-Functions-and-Operators)

## Query band functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| GETQUERYBANDVALUE | GETQUERYBANDVALUE\_UDF | Check G[ETQUERYBANDVALUE](#getquerybandvalue) |

Expand

Show lessSee more

> See [Query band functions](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Application-Programming-Reference-17.20/Workload-Management-Query-Band-APIs/Open-APIs-SQL-Interfaces)

## Regex functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| REGEXP\_INSTR | REGEXP\_INSTR | Check [Regex functions](#regex-functions) |
| REGEXP\_REPLACE | REGEXP\_REPLACE | Check [Regex functions](#regex-functions) |
| REGEXP\_SIMILAR | REGEXP\_LIKE | Check [Regex functions](#regex-functions) |
| REGEXP\_SUBSTR | REGEXP\_SUBSTR | Check [Regex functions](#regex-functions) |

Expand

Show lessSee more

> See [Regex functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/yL2xT~elOTehmwVmwVBRHA)

## String operators and functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ASCII | ASCII |  |
| CHAR2HEXINT | CHAR2HEXINT\_UDF |  |
| CHR | CHR/CHAR |  |
| CHAR\_LENGTH | LEN |  |
| CONCAT | CONCAT |  |
| EDITDISTANCE | EDITDISTANCE |  |
| INDEX | CHARINDEX | Check notes about [implicit conversion](#implicit-conversion) |
| INITCAP | INITCAP |  |
| INSTR | REGEXP\_INSTR |  |
| INSTR(StringValue, StringValue ,NumericNegativeValue, NumericValue) | INSTR\_UDF(StringValue, StringValue ,NumericNegativeValue, NumericValue) |  |
| LEFT | LEFT |  |
| LENGTH | LENGTH |  |
| LOWER | LOWER |  |
| LPAD | LPAD |  |
| LTRIM | LTRIM |  |
| OREPLACE | REPLACE |  |
| OTRANSLATE | TRANSLATE |  |
| POSITION | POSITION | Check notes about [implicit conversion](#implicit-conversion) |
| REVERSE | REVERSE |  |
| RIGHT | RIGHT |  |
| RPAD | RPAD |  |
| RTRIM | RTRIM |  |
| SOUNDEX | SOUNDEX\_P123 |  |
| STRTOK | STRTOK |  |
| STRTOK\_SPLIT\_TO\_TABLE | STRTOK\_SPLIT\_TO\_TABLE | Check [Strtok\_split\_to\_table](#strtok_split_to_table) |
| SUBSTRING | SUBSTR/SUBSTR\_UDF | Check [Substring](#substring) |
| TRANSLATE\_CHK | TRANSLATE\_CHK\_UDF |  |
| TRIM(LEADING ’0’ FROM aTABLE) | LTRIM(aTABLE, ’0’) |  |
| TRIM(TRAILING ’0’ FROM aTABLE) | RTRIM(aTABLE, ’0’) |  |
| TRIM(BOTH ’0’ FROM aTABLE) | TRIM(aTABLE, ’0’) |  |
| TRIM(CAST(numericValue AS FORMAT ’999’)) | LPAD(numericValue, 3, 0) |  |
| UPPER | UPPER |  |

Expand

Show lessSee more

> See [String operators and functions](https://docs.teradata.com/reader/756LNiPSFdY~4JcCCcR5Cw/5nyfztBE7gDQVCVU2MFTnA)​​​

## St\_Point functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| ST\_SPHERICALDISTANCE | HAVERSINE ST\_DISTANCE |  |

Expand

Show lessSee more

See [St\_Point functions](https://docs.teradata.com/r/W1AEeHO2cxTi3Sn7dtj8hg/JDVMx04qe~mo1mIm2h7NWQ)

## Table operators

| Teradata | Snowflake | Note |
| --- | --- | --- |
| TD\_UNPIVOT | Equivalent query | Check [Td\_unpivot](#td_unpivot) |

Expand

Show lessSee more

> See [Table Operators](https://docs.teradata.com/r/Teradata-Database-SQL-Functions-Operators-Expressions-and-Predicates/June-2017/Table-Operators)

## XML functions

| Teradata | Snowflake | Note |
| --- | --- | --- |
| XMLAGG | LISTAGG | Check [Xmlagg](#xmlagg) |
| XMLQUERY | Not Supported |  |

Expand

Show lessSee more

> See [XML functions](https://docs.teradata.com/r/JTydkOYDksSy26sxlEtMvg/GhlIYri~mxyncdX5BV3jWA)

## Extensibility UDFs

This section contains UDFs and other extensibility functions that are not offered as system built-in functions by Teradata but are transformed

| Teradata | Snowflake | Note |
| --- | --- | --- |
| CHKNUM | CHKNUM\_UDF | Check [this UDF download page](https://downloads.teradata.com/download/extensibility/isnumeric-udf) |

Expand

Show lessSee more

## Notes

### Architecture differences between Teradata and Snowflake

Teradata has a shared-nothing architecture with Access Module Processors (AMP) where each AMP manages their own share of disk storage and is accessed through hashing when doing queries. To take advantage of parallelism the stored information should be evenly distributed among AMPs and to do this Teradata offers a group of hash-related functions that can be used to determine how good the actual primary indexes are.

On the other hand, Snowflake architecture is different, and it manages how the data is stored on its own, meaning users do not need to worry about optimizing their data distribution.

### Ending bound constants (UNTIL\_CHANGED and UNTIL\_CLOSED)

Both UNTIL\_CHANGED and UNTIL\_CLOSED are Teradata constants that represent an undefined ending bound for periods. Internally, these constants are represented as the maximum value a timestamp can have i.e ’9999-12-31 23:59:59.999999’. During the migration of the PERIOD function, the ending bound is checked if present to determine if it is one of these constants and to replace it with varchar of value ’9999-12-31 23:59:59.999999’ in case it is, Snowflake then casts the varchar to date or timestamp depending on the type of the beginning bound when calling PERIOD\_\_\_UDF.

### Implicit conversion

Some Teradata string functions like INDEX or POSITION accept non-string data types and implicitly convert them to string, this can cause inconsistencies in the results of those functions between Teradata and Snowflake. For example, the following Teradata code:

Copy code

```
 SELECT INDEX(35, '5');
```

Returns 4, while the CHARINDEX equivalent in Snowflake:

Copy code

```
 SELECT CHARINDEX('5', 35);
```

Returns 2, this happens because Teradata has its own [default formats](https://docs.teradata.com/r/S0Fw2AVH8ff3MDA0wDOHlQ/Xh8u4~A7KI46wOdMG9DSHQ) which are used during implicit conversion. In the above example, Teradata [interprets the numeric constant](https://docs.teradata.com/r/T5QsmcznbJo1bHmZT2KnFw/TEOJhlyP6az05SdTK9JHMg) 35 as BYTEINT and uses BYTEINT default format`'-999'` for the implicit conversion to string, causing the converted value to be `' 35'`. On the other hand, Snowflake uses its own [default formats](https://docs.snowflake.com/en/sql-reference/sql-format-models.html#default-formats-for-parsing), creating inconsistencies in the result.

To solve this, the following changes are done to those function parameters:

- If the parameter does **not** have a cast with format, then a Snowflake `TO_VARCHAR` function with the default Teradata format equivalent in Snowflake is added instead.
- If the parameter does have a cast with format, then the format is converted to its Snowflake equivalent and the`TO_VARCHAR`function is added.
  - As a side note, Teradata ignores the sign of a number if it is not explicitly put inside a format, while Snowflake always adds spaces to insert the sign even when not specified, for those cases a check is done to see if the sign was specified and to remove it from the Snowflake string in case it was not.

After these changes, the resulting code would be:

Copy code

```
 SELECT CHARINDEX( '5', TO_VARCHAR(35, 'MI999'));
```

Which returns 4, the same as the Teradata code.

## Known Issues

No issues were found.

## Related EWIs

No related EWIs.

## COALESCE

### Description

The coalesce function is used to return the first non-null element in a list. For more information check [COALESCE](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/Wo3afkb7dFsUUAO5AwQOkQ).

Copy code

```
COALESCE(element_1, element_2 [, element_3, ..., element_n])
```

Both Teradata and Snowflake COALESCE functions allow mixing numeric with string and date with timestamp parameters. However, they handle these two cases differently:

- Numeric along with string parameters: Teradata converts all numeric parameters to varchar while Snowflake does the opposite
- Timestamp along with date parameters: Teradata converts all timestamps to date while Snowflake does the opposite

To ensure functional equivalence in the first case, all numeric parameters are cast to`string`using`to_varchar`function, this takes the format of the numbers into account. In the second case, all timestamps are casted to date using `to_date`, Teradata ignores the format of timestamps when casting them so it is removed during transformation.

### Sample Source Patterns

#### Numeric mixed with string parameters

##### *Teradata*

**Query**

Copy code

```
 SELECT COALESCE(125, 'hello', cast(850 as format '-999'));
```

**Result**

Copy code

```
COLUMN1|
-------+
125    |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
 COALESCE(TO_VARCHAR(125), 'hello', TO_VARCHAR(850, '9000'));
```

**Result**

Copy code

```
COLUMN1|
-------+
125    |
```

#### Timestamp mixed with date parameters

##### *Teradata*

**Query**

Copy code

```
SELECT COALESCE(cast(TIMESTAMP '2021-09-14 10:14:59' as format 'HH:MI:SSBDD-MM-YYYY'), current_date);
```

**Result**

Copy code

```
COLUMN1    |
-----------+
2021-09-14 |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
 COALESCE(TO_DATE(TIMESTAMP '2021-09-14 10:14:59' !!!RESOLVE EWI!!! /*** SSC-EWI-TD0025 - OUTPUT FORMAT 'HH:MI:SSBDD-MM-YYYY' NOT SUPPORTED. ***/!!!), CURRENT_DATE());
```

**Result**

Copy code

```
COLUMN1    |
-----------+
2021-09-14 |
```

### Known Issues

No known issues\_.\_

### Related EWIs

- [SSC-EWI-TD0025](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0025): Output format not supported.

## CURRENT\_TIMESTAMP

### Severity

Low

### Description

Fractional seconds are only displayed if it is explicitly set in the TIME\_OUTPUT\_FORMAT session parameter.

#### Input code:

Copy code

```
SELECT current_timestamp(4) at local;
```

#### Output code:

Copy code

```
SELECT
CURRENT_TIMESTAMP(4);
```

### Recommendations

- Check if the TIME\_OUTPUT\_\_\_FORMAT session parameter is set to get the behavior that you want.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## DAYNUMBER\_OF\_MONTH

### Description

Returns the number of days elapsed from the beginning of the month to the given date. For more information check [DAYNUMBER\_OF\_MONTH](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/msvzanlVHZUHwFv5LYpqzg).

Copy code

```
DAYNUMBER_OF_MONTH(expression [, calendar_name])
```

Both Teradata and Snowflake handle the DAYNUMBER\_OF\_MONTH function in the same way, except in one case:

- The ISO calendar: An ISO month has 4 or 5 complete weeks. For more information check [About ISO Computation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/RdZQp3YPJ1WrBpj8b3uljA).

To ensure functional equivalence, a user-defined function (UDF) is added for the ISO calendar case.

### Sample Source Patterns

#### *Teradata*

**Query**

Copy code

```
SELECT
    DAYNUMBER_OF_MONTH (DATE'2022-12-22'),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', NULL),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'Teradata'),
    DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'COMPATIBLE');
```

**Result**

Copy code

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
22     |22     |22     |22     |
```

#### *Snowflake*

**Query**

Copy code

```
SELECT
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22'),
    DAYOFMONTH(DATE'2022-12-22');
```

**Result**

Copy code

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
22     |22     |22     |22     |
```

#### ISO calendar

##### *Teradata*

**Query**

Copy code

```
SELECT DAYNUMBER_OF_MONTH (DATE'2022-12-22', 'ISO');
```

**Result**

Copy code

```
COLUMN1|
-------+
25     |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
PUBLIC.DAYNUMBER_OF_MONTH_UDF(DATE'2022-12-22');
```

**Result**

Copy code

```
COLUMN1|
-------+
25     |
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## FROM\_BYTES

Translation specification for transforming the TO\_CHAR function into an equivalent function concatenation in Snowflake

### Description

The FROM\_BYTES function encodes a sequence of bits into a sequence of characters representing its encoding. For more information check [FROM\_BYTES(Encoding)](https://www.docs.teradata.com/r/Teradata-VantageTM-Data-Types-and-Literals/March-2019/Data-Type-Conversion-Functions/FROM_BYTES).

Snowflake does not have support for FROM\_BYTES function, however, some workarounds can be done for the most common occurrences of this function.

### Sample Source Patterns

#### Teradata

##### Query

Copy code

```
 SELECT
FROM_BYTES('5A1B'XB, 'base10'), --returns '23067'
FROM_BYTES('5A3F'XB, 'ASCII'), --returns 'Z\ESC '
FROM_BYTES('5A1B'XB, 'base16'); -- returns '5A1B'
```

##### Result

Copy code

```
COLUMN1    | COLUMN2    | COLUMN3 |
-----------+------------+---------+
23067      |  Z\ESC     | 5A1B    |
```

##### Snowflake

##### Query

Copy code

```
 SELECT
--returns '23067'
TO_NUMBER('5A1B', 'XXXX'),
--returns 'Z\ESC '
!!!RESOLVE EWI!!! /*** SSC-EWI-0031 - FROM_BYTES FUNCTION NOT SUPPORTED ***/!!!
FROM_BYTES(TO_BINARY('5A3F'), 'ASCII'),
TO_BINARY('5A1B', 'HEX'); -- returns '5A1B'
```

##### Result

Copy code

```
COLUMN1    | COLUMN2    | COLUMN3 |
-----------+------------+---------+
23067      |  Z\ESC     | 5A1B    |
```

Note

Some parts in the output code are omitted for clarity reasons.

### Known Issues

1. TO\_NUMBER format parameter must match with the digits on the input string.
2. There is no functional equivalent built-in function for FROM\_BYTES when encoding to ANSI

### Related EWIs

1. [SSC-EWI-0031](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0031): FUNCTION NOT SUPPORTED

## GETQUERYBANDVALUE

Translation specification for the transformation of GetQueryBandValue to Snowflake

### Description

The GetQueryBandValue function searches a name key inside of the query band and returns its associated value if present. It can be used to search inside the transaction, session, profile, or any of the key-value pairs of the query band.

For more information on this function check [GetQueryBandValue](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Application-Programming-Reference-17.20/Workload-Management-Query-Band-APIs/Open-APIs-SQL-Interfaces/GetQueryBandValue) in the Teradata documentation.

Copy code

```
[SYSLIB.]GetQueryBandValue([QueryBandIn,] SearchType, Name);
```

### Sample Source Patterns

#### Setup data

##### Teradata

##### Query

Copy code

```
 SET QUERY_BAND = 'hola=hello;adios=bye;' FOR SESSION;
```

##### *Snowflake*

##### Query

Copy code

```
 ALTER SESSION SET QUERY_TAG = 'hola=hello;adios=bye;';
```

#### GetQueryBandValue with QueryBandIn parameter

##### *Teradata*

##### Query

Copy code

```
 SELECT
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'account') as Example1,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'account') as Example2,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 2, 'account') as Example3,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 3, 'account') as Example4,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'role') as Example5,
GETQUERYBANDVALUE('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'role') as Example6;
```

##### Result

Copy code

```
+----------+----------+----------+----------+----------+----------+
| EXAMPLE1 | EXAMPLE2 | EXAMPLE3 | EXAMPLE4 | EXAMPLE5 | EXAMPLE6 |
+----------+----------+----------+----------+----------+----------+
| Mark200  | Mark200  | SaraDB   | Peter3   | DbAdmin  |          |
+----------+----------+----------+----------+----------+----------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'account') as Example1,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'account') as Example2,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 2, 'account') as Example3,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 3, 'account') as Example4,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 0, 'role') as Example5,
GETQUERYBANDVALUE_UDF('=T> user=Mark;account=Mark200; =S> user=Sara;account=SaraDB;role=DbAdmin =P> user=Peter;account=Peter3;', 1, 'role') as Example6;
```

##### Result

Copy code

```
+----------+----------+----------+----------+----------+----------+
| EXAMPLE1 | EXAMPLE2 | EXAMPLE3 | EXAMPLE4 | EXAMPLE5 | EXAMPLE6 |
+----------+----------+----------+----------+----------+----------+
| Mark200  | Mark200  | SaraDB   | Peter3   | DbAdmin  |          |
+----------+----------+----------+----------+----------+----------+
```

#### GetQueryBandValue without QueryBandIn parameter

##### *Teradata*

##### Query

Copy code

```
 SELECT
GETQUERYBANDVALUE(2, 'hola') as Example1,
GETQUERYBANDVALUE(2, 'adios') as Example2;
```

##### Result

Copy code

```
+----------+----------+
| EXAMPLE1 | EXAMPLE2 |
+----------+----------+
| hello    | bye      |
+----------+----------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
GETQUERYBANDVALUE_UDF('hola') as Example1,
GETQUERYBANDVALUE_UDF('adios') as Example2;
```

##### Result

Copy code

```
+----------+----------+
| EXAMPLE1 | EXAMPLE2 |
+----------+----------+
| hello    | bye      |
+----------+----------+
```

Note

Some parts in the output code are omitted for clarity reasons.

### Known Issues

**1. GetQueryBandValue without QueryBandIn parameter only supported for session**

Teradata allows defining query bands at transaction, session or profile levels. If GetQueryBandValue is called without specifying an input query band Teradata will automatically check the transaction, session or profile query bands depending on the value of the SearchType parameter.

In Snowflake the closest equivalent to query bands are query tags, which can be specified for session, user and account.

Due to these differences, the implementation of GetQueryBandValue without QueryBandIn parameter only considers the session query tag and may not work as expected for other search types.

### Related EWIs

No related EWIs.

## HASHBUCKET

### Description

HASHBUCKET is a Teradata system function used to determine the hash bucket number for data distribution across Access Module Processors (AMPs). It is commonly used in combination with HASHROW to evaluate how evenly data is distributed across AMPs based on the primary index. For more information, see [HASHBUCKET](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw).

Copy code

```
HASHBUCKET(HASHROW(column1 [, column2, ...]))
HASHBUCKET()
HASHBUCKET(byte_expression)
```

HASHBUCKET is not translated to Snowflake because it is specific to Teradata’s shared-nothing AMP architecture. While Snowflake provides a [HASH](https://docs.snowflake.com/en/sql-reference/functions/hash) function, the two are not functionally equivalent:

- **Different algorithms**: Teradata and Snowflake use completely different hashing algorithms.
- **Different value ranges**: HASHBUCKET returns values in the range 0–1,048,575, while Snowflake HASH returns signed 64-bit integers (a far larger and different value range).
- **Different NULL handling**: HASHBUCKET(HASHROW(NULL)) returns 0, while Snowflake HASH(NULL) returns a non-NULL hash value.

### Sample Source Patterns

#### HASHBUCKET with HASHROW (single column)

##### *Teradata*

Copy code

```
 SELECT HASHBUCKET(HASHROW(col1)) FROM my_table;
```

##### *Snowflake*

Copy code

```
 SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHBUCKET FUNCTION NOT SUPPORTED ***/!!!
   HASHBUCKET(
              !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHROW FUNCTION NOT SUPPORTED ***/!!!
              HASHROW(col1))
 FROM
   my_table;
```

#### HASHBUCKET with HASHROW (multiple columns)

##### *Teradata*

Copy code

```
 SELECT HASHBUCKET(HASHROW(a, b, c)) FROM my_table;
```

##### *Snowflake*

Copy code

```
 SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHBUCKET FUNCTION NOT SUPPORTED ***/!!!
   HASHBUCKET(
              !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHROW FUNCTION NOT SUPPORTED ***/!!!
              HASHROW(a, b, c))
 FROM
   my_table;
```

#### HASHBUCKET with no arguments

##### *Teradata*

Copy code

```
 SELECT HASHBUCKET() + 1 FROM my_table;
```

##### *Snowflake*

Copy code

```
 SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - HASHBUCKET FUNCTION NOT SUPPORTED ***/!!!
   HASHBUCKET() + 1
 FROM
   my_table;
```

### Recommendations

The appropriate replacement depends on how HASHBUCKET is used in the source code:

- **Data distribution or skew analysis** — Teradata uses `HASHBUCKET(HASHROW(col))` to evaluate how evenly data is distributed across AMPs. In Snowflake, data distribution is managed automatically through [micro-partitioning](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions). To analyze clustering quality, use [SYSTEM$CLUSTERING\_INFORMATION](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information) instead.
- **Custom bucketing or partitioning logic** — If the source code uses hash bucket numbers to route or partition data, consider using Snowflake’s [HASH](https://docs.snowflake.com/en/sql-reference/functions/hash) function with `MOD()` to distribute values across a fixed number of buckets: `ABS(MOD(HASH(col), num_buckets))`. Note that this will not produce the same bucket assignments as Teradata.
- **Max bucket number constant** — `HASHBUCKET()` with no arguments returns the maximum hash bucket number (1,048,575) in Teradata. If this value is used as a constant in calculations, replace it with the literal value `1048575`.
- **Code that needs any hash value** — If the specific bucket numbers do not matter and only the distribution property is needed (e.g., sampling, random assignment), Snowflake’s [HASH](https://docs.snowflake.com/en/sql-reference/functions/hash) function can be used directly.
- **Code that depends on exact Teradata bucket values** — If the logic relies on specific bucket numbers (e.g., hardcoded ranges, lookups against pre-computed buckets), there is no automated migration path. The hashing algorithm is proprietary to Teradata and cannot be reproduced in Snowflake. This code requires manual redesign.

### Known Issues

No known issues.

### Related EWIs

- [SSC-EWI-0031](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0031): Function not supported.

## HASHROW

### Description

HASHROW is a Teradata system function that generates a hash value for one or more columns. It is typically used as the argument to [HASHBUCKET](#hashbucket) for data distribution analysis. Like HASHBUCKET, HASHROW is tied to Teradata’s AMP architecture and has no Snowflake equivalent. For more information, see [Hash functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw).

See [HASHBUCKET](#hashbucket) for conversion examples and recommendations.

### Related EWIs

- [SSC-EWI-0031](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0031): Function not supported.

## HASHAMP

### Description

HASHAMP is a Teradata system function that returns the AMP number associated with a hash bucket value. Like HASHBUCKET and HASHROW, it is tied to Teradata’s AMP architecture and has no Snowflake equivalent. For more information, see [Hash functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw).

See [HASHBUCKET](#hashbucket) for conversion examples and recommendations.

### Related EWIs

- [SSC-EWI-0031](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0031): Function not supported.

## HASHBAKAMP

### Description

HASHBAKAMP is a Teradata system function that returns the fallback AMP number for a given hash bucket value. Like HASHBUCKET and HASHROW, it is tied to Teradata’s AMP architecture and has no Snowflake equivalent. For more information, see [Hash functions](https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/jslafnqlE8bGpg~wXQiEFw).

See [HASHBUCKET](#hashbucket) for conversion examples and recommendations.

### Related EWIs

- [SSC-EWI-0031](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0031): Function not supported.

## JSON\_CHECK

### Description

The JSON\_CHECK function checks a string for valid JSON.

For more information, see the [Teradata JSON\_CHECK documentation](https://docs.teradata.com/r/Teradata-Database-JSON-Data-Type/June-2017/JSON-Functions-and-Operators/JSON_CHECK).

Copy code

```
[TD_SYSFNLIB.]JSON_CHECK(string_expr);
```

### Sample Source Pattern

#### Basic Source Pattern

##### Teradata

**Query**

Copy code

```
SELECT JSON_CHECK('{"key": "value"}');
```

##### Snowflake Scripting

**Query**

Copy code

```
SELECT
IFNULL(CHECK_JSON('{"key": "value"}'), 'OK');
```

#### JSON\_CHECK inside CASE transformation

##### Teradata

**Query**

Copy code

```
SELECT CASE WHEN JSON_CHECK('{}') = 'OK' then 'OKK' ELSE 'NOT OK' END;
```

##### Snowflake Scripting

**Query**

Copy code

```
SELECT
CASE
WHEN UPPER(RTRIM(IFNULL(CHECK_JSON('{}'), 'OK'))) = UPPER(RTRIM('OK'))
THEN 'OKK' ELSE 'NOT OK'
END;
```

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## JSON\_EXTRACT

Translation reference to convert the Teradata functions JSONExtractValue, JSONExtractLargeValue and JSONExtract to Snowflake Scripting.

### Description

As per Teradata’s documentation, these functions use the [JSONPath Query Syntax](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type/March-2019/Operations-on-the-JSON-Type/JSONPath-Request-Syntax) to request information about a portion of a JSON instance. The entity desired can be any portion of a JSON instance, such as a name/value pair, an object, an array, an array element, or a value.

For more information, see the [Teradata JSONExtract function comparison](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type/March-2019/JSON-Methods/Comparison-of-JSONExtract-and-JSONExtractValue).

Copy code

```
JSON_expr.JSONExtractValue(JSONPath_expr);

JSON_expr.JSONExtractLargeValue(JSONPath_expr);

JSON_expr.JSONExtract(JSONPath_expr);
```

The JSON\_EXTRACT\_UDF is a Snowflake implementation of the JSONPath specification that uses a modified version of the original JavaScript implementation developed by [Stefan Goessner](https://goessner.net/index.html).

#### Sample Source Pattern

##### Teradata

##### Query

Copy code

```
 SELECT
    Store.JSONExtract('$..author') as AllAuthors,
    Store.JSONExtractValue('$..book[2].title') as ThirdBookTitle,
    Store.JSONExtractLargeValue('$..book[2].price') as ThirdBookPrice
FROM BookStores;
```

##### Snowflake Scripting

##### Query

Copy code

```
 SELECT
    JSON_EXTRACT_UDF(Store, '$..author', FALSE) as AllAuthors,
    JSON_EXTRACT_UDF(Store, '$..book[2].title', TRUE) as ThirdBookTitle,
    JSON_EXTRACT_UDF(Store, '$..book[2].price', TRUE) as ThirdBookPrice
    FROM
    BookStores;
```

Note

Some parts in the output code are omitted for clarity reasons.

### Known Issues

#### 1. Elements inside JSONs may not retain their original order.

Elements inside a JSON are ordered by their keys when inserted in a table. Thus, the query results might differ. However, this does not affect the order of arrays inside the JSON.

For example, if the original JSON is:

Copy code

```
{
  "firstName": "Peter",
  "lastName": "Andre",
  "age": 31,
  "cities": ["Los Angeles", "Lima", "Buenos Aires"]
}
```

Using the Snowflake [PARSE\_JSON()](https://docs.snowflake.com/en/sql-reference/functions/parse_json.html) that interprets an input string as a JSON document, producing a VARIANT value. The inserted JSON will be:

Copy code

```
{
  "age": 31,
  "cities": ["Los Angeles", "Lima", "Buenos Aires"],
  "firstName": "Peter",
  "lastName": "Andre"
}
```

Note how “age” is now the first element. However, the array of “cities” maintains its original order.

### Related EWIs

No related EWIs.

## JSON\_TABLE

Translation specification for the transformation of JSON\_TABLE into a equivalent query in Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Creates a table based on the contents of a JSON document. See [JSON\_TABLE documentation](https://docs.teradata.com/r/Teradata-VantageTM-JSON-Data-Type-17.20/JSON-Shredding/JSON_TABLE).

Copy code

```
[TD_SYSFNLIB.]JSON_TABLE(
  ON (json_documents_retrieving_expr)
  USING
      ROWEXPR (row_expr_literal)
      COLEXPR (column_expr_literal)
  [AS] correlation_name [(column_name [,...])]
)
```

The conversion of JSON\_TABLE has the considerations shown below:

- ROW\_NUMBER() is an equivalent of ordinal columns in Snowflake.
- In Teradata, the second column of JSON\_TABLE must be JSON type because the generated columns replace the second column, for that reason, the assumption is that the column has the right type, and it is used for the transformation.

### Sample Source Patterns

#### Setup data

##### Teradata

##### Query

Copy code

```
 create table myJsonTable(
 col1 integer,
 col2 JSON(1000)
 );

insert into myJsonTable values(1,
new json('{
"name": "Matt",
"age" : 30,
"songs" : [
	{"name" : "Late night", "genre" : "Jazz"},
	{"name" : "Wake up", "genre" : "Rock"},
	{"name" : "Who am I", "genre" : "Rock"},
	{"name" : "Raining", "genre" : "Blues"}
]
}'));
```

##### *Snowflake*

##### Query

Copy code

```
 CREATE OR REPLACE TABLE myJsonTable (
 col1 integer,
 col2 VARIANT
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO myJsonTable
VALUES (1, TO_JSON(PARSE_JSON('{
"name": "Matt",
"age" : 30,
"songs" : [
	{"name" : "Late night", "genre" : "Jazz"},
	{"name" : "Wake up", "genre" : "Rock"},
	{"name" : "Who am I", "genre" : "Rock"},
	{"name" : "Raining", "genre" : "Blues"}
]
}')));
```

#### Pattern code 1

##### *Teradata*

##### Query

Copy code

```
 SELECT * FROM
JSON_TABLE(ON (SELECT COL1, COL2 FROM myJsonTable WHERE col1 = 1)
USING rowexpr('$.songs[*]')
colexpr('[ {"jsonpath" : "$.name",
            "type" : "CHAR(20)"},
            {"jsonpath" : "$.genre",
             "type" : "VARCHAR(20)"}]')) AS JT(ID, "Song name", Genre);
```

##### Result

Copy code

```
ID | Song name  | Genre |
---+------------+-------+
1  | Late night | Jazz  |
---+------------+-------+
1  | Wake up    | Rock  |
---+------------+-------+
1  | Who am I   | Rock  |
---+------------+-------+
1  | Raining    | Blues |
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
* FROM
(
SELECT
COL1 AS ID,
rowexpr.value:name :: CHAR(20) AS "Song name",
rowexpr.value:genre :: VARCHAR(20) AS Genre
FROM
myJsonTable,
TABLE(FLATTEN(INPUT => COL2:songs)) rowexpr
WHERE col1 = 1
) JT;
```

##### Result

Copy code

```
ID | Song name  | Genre |
---+------------+-------+
1  | Late night | Jazz  |
---+------------+-------+
1  | Wake up    | Rock  |
---+------------+-------+
1  | Who am I   | Rock  |
---+------------+-------+
1  | Raining    | Blues |
```

### Known Issues

**1. The JSON path in COLEXPR can not have multiple asterisk accesses**

The columns JSON path cannot have multiple lists with asterisk access, for example: `$.Names[*].FullNames[*]`. On the other hand, the JSON path of ROWEXP can have it.

**2. JSON structure defined in the COLEXPR literal must be a valid JSON**

When it is not the case the user will be warned about the JSON being badly formed.

### Related EWIs

No related EWIs.

## NEW JSON

### Description

Allocates a new instance of a JSON datatype. For more information check [NEW JSON Constructor Expression.](https://docs.teradata.com/r/Teradata-Database-JSON-Data-Type/June-2017/The-JSON-Data-Type/About-JSON-Type-Constructor/NEW-JSON-Constructor-Expression)

Copy code

```
NEW JSON ( [ JSON_string_spec | JSON_binary_data_spec ] )

JSON_string_spec := JSON_String_literal [, { LATIN | UNICODE | BSON | UBJSON } ]

JSON_binary_data_spec := JSON_binary_literal [, { BSON | UBJSON } ]
```

The second parameter of the NEW JSON function is always omitted since Snowflake works only with UTF-8.

### Sample Source Patterns

#### NEW JSON with string data

##### *Teradata*

**Query**

Copy code

```
SELECT NEW JSON ('{"name" : "cameron", "age" : 24}'),
NEW JSON ('{"name" : "cameron", "age" : 24}', LATIN);
```

**Result**

| COLUMN1 | COLUMN2 |
| --- | --- |
| {“age”:24,”name”:”cameron”} | {“age”:24,”name”:”cameron”} |

Expand

Show lessSee more

##### *Snowflake*

**Query**

Copy code

```
SELECT
TO_JSON(PARSE_JSON('{"name" : "cameron", "age" : 24}')),
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0039 - INPUT FORMAT 'LATIN' NOT SUPPORTED ***/!!!
TO_JSON(PARSE_JSON('{"name" : "cameron", "age" : 24}'));
```

**Result**

| COLUMN1 | COLUMN2 |
| --- | --- |
| {“age”:24,”name”:”cameron”} | {“age”:24,”name”:”cameron”} |

Expand

Show lessSee more

### Known Issues

**1. The second parameter is not supported**

The second parameter of the function used to specify the format of the resulting JSON is not supported because Snowflake only supports UTF-8, this may result in functional differences for some uses of the function.

**2. JSON with BINARY data is not supported**

Snowflake does not support parsing binary data to create a JSON value, the user will be warned when a NEW JSON with binary data is found.

### Related EWIs

1. [SSC-EWI-TD0039](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0039): Input format not supported.

## NVP

### Description

Extracts the value of the key-value pair where the key matches the nth occurrence of the specified name to search. See [NVP](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/String-Operators-and-Functions/NVP).

Copy code

```
[TD_SYSFNLIB.] NVP (
in_string,
name_to_search
[, name_delimiters ]
[, value_delimiters ]
[, occurrence ]
)
```

### Sample Source Patterns

#### NVP basic case

##### *Teradata*

**Query**

Copy code

```
SELECT
NVP('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1),
NVP('Hello=bye|name=Lucas|Hello=world!', 'Hello', '|', '=', 2),
NVP('Player=Mario$Game&Tenis%Player/Susana$Game=Chess', 'Player', '% $', '= & /', 2);
```

**Result**

Copy code

```
COLUMN1        | COLUMN2 | COLUMN3 |
---------------+---------+---------+
orange chicken | world!  | Susana  |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
PUBLIC.NVP_UDF('entree=-orange chicken&entree+.honey salmon', 'entree', '&', '=- +.', 1),
PUBLIC.NVP_UDF('Hello=bye|name=Lucas|Hello=world!', 'Hello', '|', '=', 2),
PUBLIC.NVP_UDF('Player=Mario$Game&Tenis%Player/Susana$Game=Chess', 'Player', '% $', '= & /', 2);
```

**Result**

Copy code

```
COLUMN1        | COLUMN2 | COLUMN3 |
---------------+---------+---------+
orange chicken | world!  | Susana  |
```

#### NVP with optional parameters ignored

##### *Teradata*

**Query**

Copy code

```
SELECT
NVP('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color'),
NVP('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', 2),
NVP('City=Los Angeles#Color=Green#Color=Blue#City=San Jose', 'City', '#', '=');
```

**Result**

Copy code

```
COLUMN1 | COLUMN2 | COLUMN3     |
--------+---------+-------------+
Green   | Blue    | Los Angeles |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
    PUBLIC.NVP_UDF('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', '&', '=', 1),
    PUBLIC.NVP_UDF('City=Los Angeles&Color=Green&Color=Blue&City=San Jose', 'Color', '&', '=', 2),
    PUBLIC.NVP_UDF('City=Los Angeles#Color=Green#Color=Blue#City=San Jose', 'City', '#', '=', 1);
```

**Result**

Copy code

```
COLUMN1 | COLUMN2 | COLUMN3     |
--------+---------+-------------+
Green   | Blue    | Los Angeles |
```

#### NVP with spaces in delimiters

##### *Teradata*

**Query**

Copy code

```
SELECT
NVP('store = whole foods&&store: ?Bristol farms','store', '&&', '\ =\  :\ ?', 2),
NVP('Hello = bye|name = Lucas|Hello = world!', 'Hello', '|', '\ =\ ', 2);
```

**Result**

Copy code

```
COLUMN1       | COLUMN2 |
--------------+---------+
Bristol farms | world!  |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', '\\ =\\  :\\ ?', 2),
PUBLIC.NVP_UDF('Hello = bye|name = Lucas|Hello = world!', 'Hello', '|', '\\ =\\ ', 2);
```

**Result**

Copy code

```
COLUMN1       | COLUMN2 |
--------------+---------+
Bristol farms | world!  |
```

#### NVP with non-literal delimiters

##### *Teradata*

**Query**

Copy code

```
SELECT NVP('store = whole foods&&store: ?Bristol farms','store', '&&', valueDelimiter, 2);
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
PUBLIC.NVP_UDF('store = whole foods&&store: ?Bristol farms', 'store', '&&', valueDelimiter, 2) /*** SSC-FDM-TD0008 - WHEN NVP_UDF FOURTH PARAMETER IS NON-LITERAL AND IT CONTAINS A BACKSLASH, THAT BACKSLASH NEEDS TO BE ESCAPED ***/;
```

### Known Issues

**1. Delimiters with spaces (\ ) need to have the backslash escaped in Snowflake**

In Teradata, delimiters including space specify them using “\ “ (see [NVP with spaces in delimiters](#nvp-with-spaces-in-delimiters)), as shown in the examples, in Teradata it is not necessary to escape the backslash, however, it is necessary in Snowflake. Escaping the backslashes in the delimiter can be done automatically but only if the delimiter values are literal strings, otherwise the user will be warned that the backslashes could not be escaped and that it may cause different results in Snowflake.

### Related EWIs

1. [SSC-FDM-TD0008](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0008): Non-literal delimiters with spaces need their backslash escaped in Snowflake.

## OVERLAPS

### Description

According to Teradata’s documentation, the OVERLAPS operator compares two or more period expressions. If they overlap, it returns true.

For more information, see the [Teradata OVERLAPS documentation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/3VIgdwHNVU~tsnNiIR1aEw).

Copy code

```
period_expression
OVERLAPS
period_expression
```

The PERIOD\_OVERLAPS\_UDF is a Snowflake implementation of the OVERLAPS operator in Teradata.

### Sample Source Pattern

#### Teradata

**Query**

Copy code

```
SELECT
    PERIOD(DATE '2009-01-01', DATE '2010-09-24')
    OVERLAPS
    PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

#### Snowflake Scripting

**Query**

Copy code

```
SELECT
    PUBLIC.PERIOD_OVERLAPS_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

### Known Issues

#### 1. Unsupported Period Expressions

The *PERIOD(TIME WITH TIME ZONE)* and *PERIOD(TIMESTAMP WITH TIME ZONE)* expressions are not supported yet.

### Related EWIs

1. [SSC-EWI-TD0053](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead

## P\_INTERSECT

### Description

According to Teradata’s documentation, the P\_INTERSECT operator compares two or more period expressions. If they overlap, it returns the common portion of the period expressions.

For more information, see the [Teradata P\_INTERSECT documentation](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/iW6iefgeyOypFOMY2qGG_A).

Copy code

```
period_expression
P_INTERSECT
period_expression
```

The PERIOD\_INTERSECT\_UDF is a Snowflake implementation of the P\_INTERSECT operator in Teradata.

### Sample Source Pattern

#### Teradata

**Query**

Copy code

```
SELECT
    PERIOD(DATE '2009-01-01', DATE '2010-09-24')
    P_INTERSECT
    PERIOD(DATE '2009-02-01', DATE '2009-06-24');
```

#### Snowflake Scripting

**Query**

Copy code

```
SELECT
    PUBLIC.PERIOD_INTERSECT_UDF(ARRAY_CONSTRUCT(PUBLIC.PERIOD_UDF(DATE '2009-01-01', DATE '2010-09-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!, PUBLIC.PERIOD_UDF(DATE '2009-02-01', DATE '2009-06-24') !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!)) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!;
```

### Known Issues

#### 1. Unsupported Period Expressions

The *PERIOD(TIME WITH TIME ZONE)* and *PERIOD(TIMESTAMP WITH TIME ZONE)* expressions are not supported yet.

### Related EWIs

1. [SSC-EWI-TD0053](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0053): Snowflake does not support the period datatype, all periods are handled as varchar instead

## PIVOT

Translation specification for the PIVOT function from Teradata to Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description

The pivot function is used to transform rows of a table into columns. For more information check the [PIVOT Teradata documentation.](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/Aggregate-Functions/PIVOT)

Copy code

```
PIVOT ( pivot_spec )
  [ WITH with_spec [,...] ]
  [AS] derived_table_name [ ( cname [,...] ) ]

pivot_spec := aggr_fn_spec [,...] FOR for_spec

aggr_fn_spec := aggr_fn ( cname ) [ [AS] pvt_aggr_alias ]

for_spec := { cname IN ( expr_spec_1 [,...] ) |
( cname [,...] ) IN ( expr_spec_2 [,...] ) |
cname IN ( subquery )
}

expr_spec_1 := expr [ [AS] expr_alias_name ]

expr_spec_2 := ( expr [,...] ) [ [AS] expr_alias_name ]

with_spec := aggr_fn ( { cname [,...] | * } ) [AS] aggr_alias
```

### Sample Source Patterns

#### Setup data

##### Teradata

##### Query

Copy code

```
 CREATE TABLE star1(
	country VARCHAR(20),
	state VARCHAR(10),
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
);

insert into star1 values ('USA', 'CA', 2001, 'Q1', 30, 15);
insert into star1 values ('Canada', 'ON', 2001, 'Q2', 10, 0);
insert into star1 values ('Canada', 'BC', 2001, 'Q3', 10, 0);
insert into star1 values ('USA', 'NY', 2001, 'Q1', 45, 25);
insert into star1 values ('USA', 'CA', 2001, 'Q2', 50, 20);
```

##### *Snowflake*

##### Query

Copy code

```
 CREATE OR REPLACE TABLE star1 (
	country VARCHAR(20),
	state VARCHAR(10),
	yr INTEGER,
	qtr VARCHAR(3),
	sales INTEGER,
	cogs INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO star1
VALUES ('USA', 'CA', 2001, 'Q1', 30, 15);

INSERT INTO star1
VALUES ('Canada', 'ON', 2001, 'Q2', 10, 0);

INSERT INTO star1
VALUES ('Canada', 'BC', 2001, 'Q3', 10, 0);

INSERT INTO star1
VALUES ('USA', 'NY', 2001, 'Q1', 45, 25);

INSERT INTO star1
VALUES ('USA', 'CA', 2001, 'Q2', 50, 20);
```

#### Basic PIVOT transformation

##### *Teradata*

##### Query

Copy code

```
 SELECT *
FROM star1 PIVOT (
	SUM(sales) FOR qtr
    IN ('Q1',
    	'Q2',
        'Q3')
)Tmp;
```

##### Result

Copy code

```
Country | State | yr   | cogs | 'Q1' | 'Q2' | 'Q3' |
--------+-------+------+------+------+------+------+
Canada	| BC	| 2001 | 0    | null | null | 10   |
--------+-------+------+------+------+------+------+
USA 	| NY	| 2001 | 25   | 45   | null | null |
--------+-------+------+------+------+------+------+
Canada 	| ON 	| 2001 | 0    | null | 10   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 20   | null | 50   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 15   | 30   | null | null |
--------+-------+------+------+------+------+------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
	*
FROM
	star1 PIVOT(
	SUM(sales) FOR qtr IN ('Q1',
	   	'Q2',
	       'Q3'))Tmp;
```

##### Result

Copy code

```
Country | State | yr   | cogs | 'Q1' | 'Q2' | 'Q3' |
--------+-------+------+------+------+------+------+
Canada	| BC	| 2001 | 0    | null | null | 10   |
--------+-------+------+------+------+------+------+
USA 	| NY	| 2001 | 25   | 45   | null | null |
--------+-------+------+------+------+------+------+
Canada 	| ON 	| 2001 | 0    | null | 10   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 20   | null | 50   | null |
--------+-------+------+------+------+------+------+
USA 	| CA 	| 2001 | 15   | 30   | null | null |
--------+-------+------+------+------+------+------+
```

#### PIVOT with aliases transformation

##### *Teradata*

##### Query

Copy code

```
 SELECT *
FROM star1 PIVOT (
	SUM(sales) as ss1 FOR qtr
    IN ('Q1' AS Quarter1,
    	'Q2' AS Quarter2,
        'Q3' AS Quarter3)
)Tmp;
```

##### Result

Copy code

```
Country | State | yr   | cogs | Quarter1_ss1 | Quarter2_ss1 | Quarter3_ss1 |
--------+-------+------+------+--------------+--------------+--------------+
Canada	| BC	| 2001 | 0    | null 	     | null         | 10           |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| NY	| 2001 | 25   | 45 	     | null 	    | null         |
--------+-------+------+------+--------------+--------------+--------------+
Canada 	| ON 	| 2001 | 0    | null 	     | 10 	    | null 	   |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 20   | null         | 50           | null         |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 15   | 30           | null         | null         |
--------+-------+------+------+--------------+--------------+--------------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
	*
FROM
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	star1 PIVOT(
	SUM(sales) FOR qtr IN (
	                       !!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	                       'Q1',
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	   	'Q2',
	!!!RESOLVE EWI!!! /*** SSC-EWI-0015 - PIVOT/UNPIVOT RENAME COLUMN NOT SUPPORTED ***/!!!
	       'Q3'))Tmp;
```

##### Result

Copy code

```
 Country | State | yr   | cogs | Quarter1_ss1 | Quarter2_ss1 | Quarter3_ss1 |
--------+-------+------+------+--------------+--------------+--------------+
Canada	| BC	| 2001 | 0    | null 	     | null         | 10           |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| NY	| 2001 | 25   | 45 	     | null 	    | null         |
--------+-------+------+------+--------------+--------------+--------------+
Canada 	| ON 	| 2001 | 0    | null 	     | 10 	    | null 	   |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 20   | null         | 50           | null         |
--------+-------+------+------+--------------+--------------+--------------+
USA 	| CA 	| 2001 | 15   | 30           | null         | null         |
--------+-------+------+------+--------------+--------------+--------------+
```

### Known Issues

**1. WITH clause not supported**

Using the WITH clause is not currently supported.

**2. Pivot over multiple pivot columns not supported**

The PIVOT function is transformed into the PIVOT function in Snowflake, which only supports applying the function over a single column.

**3. Pivot with multiple aggregate functions not supported**

The PIVOT function in Snowflake only supports applying one aggregate function over the data.

**4. Subquery in the IN clause not supported**

The IN clause of the Snowflake PIVOT function does not accept subqueries.

**5. Aliases only supported if all IN clause elements have it and table specification is present**

For the column names with aliases to be equivalent, all the values specified in the IN clause must have one alias specified and the table specification must be present in the input code, this is necessary so the alias list for the resulting table can be created.

### Related EWIs

1. [SSC-EWI-0015](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0015): The input pivot/unpivot statement format is not supported

## RANK

Translation specification for the transformation of the RANK() function

### Description

RANK sorts a result set and identifies the numeric rank of each row in the result. The only argument for RANK is the sort column or columns, and the function returns an integer that represents the rank of each row in the result. ([RANK in Teradata](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Ordered-Analytical/Window-Aggregate-Functions/RANK-Teradata))

#### Teradata syntax

Copy code

```
 RANK ( sort_expression [ ASC | DESC ] [,...] )
```

#### Snowflake syntax

Copy code

```
 RANK() OVER
(
    [ PARTITION BY <expr1> ]
    ORDER BY <expr2> [ { ASC | DESC } ]
    [ <window_frame> ]
)
```

### Sample Source Pattern

#### Setup data

##### Teradata

##### Query

Copy code

```
 CREATE TABLE Sales (
  Product VARCHAR(255),
  Sales INT
);

INSERT INTO Sales (Product, Sales) VALUES ('A', 100);
INSERT INTO Sales (Product, Sales) VALUES ('B', 150);
INSERT INTO Sales (Product, Sales) VALUES ('C', 200);
INSERT INTO Sales (Product, Sales) VALUES ('D', 150);
INSERT INTO Sales (Product, Sales) VALUES ('E', 120);
INSERT INTO Sales (Product, Sales) VALUES ('F', NULL);
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE TABLE Sales (
  Product VARCHAR(255),
  Sales INT
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO Sales (Product, Sales)
VALUES ('A', 100);

INSERT INTO Sales (Product, Sales)
VALUES ('B', 150);

INSERT INTO Sales (Product, Sales)
VALUES ('C', 200);

INSERT INTO Sales (Product, Sales)
VALUES ('D', 150);

INSERT INTO Sales (Product, Sales)
VALUES ('E', 120);

INSERT INTO Sales (Product, Sales)
VALUES ('F', NULL);
```

#### RANK() using ASC, DESC, and DEFAULT order

##### Teradata

Warning

Notice that Teradata’s ordering default value when calling RANK() is DESC. However, the default in Snowflake is ASC. Thus, DESC is added in the conversion of RANK() when no order is specified.

##### Query

Copy code

```
 SELECT
  Sales,
  RANK(Sales ASC) AS SalesAsc,
  RANK(Sales DESC) AS SalesDesc,
  RANK(Sales) AS SalesDefault
FROM
  Sales;
```

##### Result

| SALES | SALESASC | SALESDESC | SALESDEFAULT |
| --- | --- | --- | --- |
| NULL | 6 | 6 | 6 |
| 200 | 5 | 1 | 1 |
| 150 | 3 | 2 | 2 |
| 150 | 3 | 2 | 2 |
| 120 | 2 | 4 | 4 |
| 100 | 1 | 5 | 5 |

##### Snowflake

##### Query

Copy code

```
 SELECT
  Sales,
  RANK() OVER (
  ORDER BY
    Sales ASC) AS SalesAsc,
    RANK() OVER (
    ORDER BY
    Sales DESC NULLS LAST) AS SalesDesc,
    RANK() OVER (
    ORDER BY
    Sales DESC NULLS LAST) AS SalesDefault
    FROM
    Sales;
```

##### Result

| SALES | SALESASC | SALESDESC | SALESDEFAULT |
| --- | --- | --- | --- |
| NULL | 6 | 6 | 6 |
| 200 | 5 | 1 | 1 |
| 150 | 3 | 2 | 2 |
| 150 | 3 | 2 | 2 |
| 120 | 2 | 4 | 4 |
| 100 | 1 | 5 | 5 |

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## Regex functions

### Description

Both Teradata and Snowflake offer support for functions that apply regular expressions over varchar inputs. See the [Teradata documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates/March-2019/Regular-Expression-Functions) and [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/functions-regexp.html) for more details.

Copy code

```
REGEXP_SUBSTR(source. regexp [, position, occurrence, match])
REGEXP_REPLACE(source. regexp [, replace_string, position, occurrence, match])
REGEXP_INSTR(source. regexp [, position, occurrence, return_option, match])
REGEXP_SIMILAR(source. regexp [, match])
REGEXP_SPLIT_TO_TABLE(inKey. source. regexp, match)
```

### Sample Source Patterns

#### Setup data

##### Teradata

**Query**

Copy code

```
CREATE TABLE regexpTable
(
    col1 CHAR(35)
);

INSERT INTO regexpTable VALUES('hola');
```

##### *Snowflake*

**Query**

Copy code

```
CREATE OR REPLACE TABLE regexpTable
(
    col1 CHAR(35)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO regexpTable
VALUES ('hola');
```

#### Regex transformation example

##### *Teradata*

**Query**

Copy code

```
SELECT
REGEXP_REPLACE(col1,'.*(h(i|o))','ha', 1, 0, 'x'),
REGEXP_SUBSTR(COL1,'.*(h(i|o))', 2, 1, 'x'),
REGEXP_INSTR(COL1,'.*(h(i|o))',1, 1, 0, 'x'),
REGEXP_SIMILAR(COL1,'.*(h(i|o))', 'xl')
FROM regexpTable;
```

**Result**

Copy code

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
hala   |null   |1      |0      |
```

##### *Snowflake*

**Query**

Copy code

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "regexpTable" **
SELECT
REGEXP_REPLACE(col1, '.*(h(i|o))', 'ha', 1, 0),
REGEXP_SUBSTR(COL1, '.*(h(i|o))', 2, 1),
REGEXP_INSTR(COL1, '.*(h(i|o))', 1, 1, 0),
--** SSC-FDM-TD0016 - VALUE 'l' FOR PARAMETER 'match_arg' IS NOT SUPPORTED IN SNOWFLAKE **
REGEXP_LIKE(COL1, '.*(h(i|o))')
FROM
regexpTable;
```

**Result**

Copy code

```
COLUMN1|COLUMN2|COLUMN3|COLUMN4|
-------+-------+-------+-------+
hala   |null   |1      |FALSE  |
```

### Known Issues

**1. Snowflake only supports POSIX regular expressions**

The user will be warned when a non-POSIX regular expression is found.

**2. Teradata “match\_arg” option ‘l’ is unsupported in Snowflake**

The option ‘l’ has no counterpart in Snowflake and the user will be warned if they are found.

**3. Fixed size of the CHAR datatype may cause different behavior**

Some regex functions in Teradata will try to match the whole column of CHAR datatype in a table even if some of the characters in the column were left empty due to a smaller string being inserted. In Snowflake this does not happen because the CHAR datatype is of variable size.

**4. REGEXP\_SPLIT\_TO\_TABLE not supported**

The function is currently not supported by Snowflake.

### Related EWIs

1. [SSC-FDM-0007](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007): Element with missing dependencies.
2. [SSC-FDM-TD0016](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0016): Value ‘l’ for parameter ‘match\_arg’ is not supported in Snowflake.

## STRTOK\_SPLIT\_TO\_TABLE

### Description

Split a string into a table using the provided delimiters. For more information check [STRTOK\_SPLIT\_TO\_TABLE](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Functions-Expressions-and-Predicates-17.20/String-Operators-and-Functions/STRTOK_SPLIT_TO_TABLE).

Copy code

```
[TD_SYSFNLIB.] STRTOK_SPLIT_TO_TABLE ( inkey, instring, delimiters )
  RETURNS ( outkey, tokennum, token )
```

### Sample Source Patterns

#### Setup data

##### Teradata

**Query**

Copy code

```
CREATE TABLE strtokTable
(
	col1 INTEGER,
	col2 VARCHAR(100)
);

INSERT INTO strtokTable VALUES(4, 'hello-world-split-me');
INSERT INTO strtokTable VALUES(1, 'string$split$by$dollars');
```

##### *Snowflake*

**Query**

Copy code

```
CREATE OR REPLACE TABLE strtokTable
(
	col1 INTEGER,
	col2 VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO strtokTable
VALUES (4, 'hello-world-split-me');

INSERT INTO strtokTable
VALUES (1, 'string$split$by$dollars');
```

#### STRTOK\_SPLIT\_TO\_TABLE transformation

##### *Teradata*

**Query**

Copy code

```
SELECT outkey, tokennum, token FROM table(STRTOK_SPLIT_TO_TABLE(strtokTable.col1, strtokTable.col2, '-$')
RETURNS (outkey INTEGER, tokennum INTEGER, token VARCHAR(100))) AS testTable
ORDER BY outkey, tokennum;
```

**Result**

Copy code

```
outkey |tokennum | token  |
-------+---------+--------+
1      |1        |string  |
-------+---------+--------+
1      |2        |split   |
-------+---------+--------+
1      |3        |by      |
-------+---------+--------+
1      |4        |dollars |
-------+---------+--------+
4      |1        |hello   |
-------+---------+--------+
4      |2        |world   |
-------+---------+--------+
4      |3        |split   |
-------+---------+--------+
4      |4        |me      |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
CAST(strtokTable.col1 AS INTEGER) AS outkey,
CAST(INDEX AS INTEGER) AS tokennum,
CAST(VALUE AS VARCHAR) AS token
FROM
strtokTable,
table(STRTOK_SPLIT_TO_TABLE(strtokTable.col2, '-$')) AS testTable
ORDER BY outkey, tokennum;
```

**Result**

Copy code

```
outkey |tokennum | token  |
-------+---------+--------+
1      |1        |string  |
-------+---------+--------+
1      |2        |split   |
-------+---------+--------+
1      |3        |by      |
-------+---------+--------+
1      |4        |dollars |
-------+---------+--------+
4      |1        |hello   |
-------+---------+--------+
4      |2        |world   |
-------+---------+--------+
4      |3        |split   |
-------+---------+--------+
4      |4        |me      |
```

### Known Issues

No known issues.

### Related EWIs

No related EWIs.

## SUBSTRING

### Description

Extracts a substring from a given input string. For more information check [SUBSTRING/SUBSTR.](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/lxOd~YrdVkJGt0_anAEXFQ)

Copy code

```
SUBSTRING(string_expr FROM n1 [FOR n2])

SUBSTR(string_expr, n1, [, n2])
```

When the value to start getting the substring (n1) is less than one SUBSTR\_UDF is inserted instead.

### Sample Source Patterns

#### SUBSTRING transformation

##### *Teradata*

**Query**

Copy code

```
SELECT SUBSTR('Hello World!', 2, 6),
SUBSTR('Hello World!', -2, 6),
SUBSTRING('Hello World!' FROM 2 FOR 6),
SUBSTRING('Hello World!' FROM -2 FOR 6);
```

**Result**

Copy code

```
COLUMN1 |COLUMN2 |COLUMN3 | COLUMN4 |
--------+--------+--------+---------+
ello W  |Hel     |ello W  |Hel      |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
SUBSTR('Hello World!', 2, 6),
PUBLIC.SUBSTR_UDF('Hello World!', -2, 6),
SUBSTRING('Hello World!', 2, 6),
PUBLIC.SUBSTR_UDF('Hello World!', -2, 6);
```

**Result**

Copy code

```
COLUMN1 |COLUMN2 |COLUMN3 | COLUMN4 |
--------+--------+--------+---------+
ello W  |Hel     |ello W  |Hel      |
```

### Related EWIs

No related EWIs.

## TD\_UNPIVOT

Translation specification for the transformation of TD\_UNPIVOT into an equivalent query in Snowflake

Note

Some parts in the output code are omitted for clarity reasons.

### Description

`TD_UNPIVOT` in Teradata can unpivot multiple columns at once, while Snowflake `UNPIVOT` can only unpivot a single column\*\*.\*\* The *unpivot* functionality is used to transform columns of the specified table into rows. For more information see [TD\_UNPIVOT](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Operators-and-User-Defined-Functions-17.20/Table-Operators/TD_UNPIVOT).

Copy code

```
[TD_SYSFNLIB.] TD_UNPIVOT (
  ON { tableName | ( query_expression ) }
  USING VALUE_COLUMNS ( 'value_columns_value' [,...] )
  UNPIVOT_COLUMN ( 'unpivot_column_value' )
  COLUMN_LIST ( 'column_list_value' [,...] )
  [ COLUMN_ALIAS_LIST ( 'column_alias_list_value' [,...] )
      INCLUDE_NULLS ( { 'No' | 'Yes' } )
  ]
)
```

The following transformation is able to generate a SQL query in Snowflake that unpivots multiple columns at the same time, the same way it works in Teradata.

### Sample Source Patterns

#### Setup data title

##### Teradata

##### Query

Copy code

```
 CREATE TABLE superunpivottest (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
);

INSERT INTO superUnpivottest VALUES (2020, 15440, 25430.57, 10322.15, 12355.36);
INSERT INTO superUnpivottest VALUES (2018, 18325.25, 25220.65, 15560.45, 15680.33);
INSERT INTO superUnpivottest VALUES (2019, 23855.75, 34220.22, 14582.55, 24122);
```

##### *Snowflake*

##### Query

Copy code

```
 CREATE OR REPLACE TABLE superunpivottest (
	myKey INTEGER NOT NULL PRIMARY KEY,
	firstSemesterIncome DECIMAL(10,2),
	secondSemesterIncome DECIMAL(10,2),
	firstSemesterExpenses DECIMAL(10,2),
	secondSemesterExpenses DECIMAL(10,2)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO superUnpivottest
VALUES (2020, 15440, 25430.57, 10322.15, 12355.36);

INSERT INTO superUnpivottest
VALUES (2018, 18325.25, 25220.65, 15560.45, 15680.33);

INSERT INTO superUnpivottest
VALUES (2019, 23855.75, 34220.22, 14582.55, 24122);
```

#### TD\_UNPIVOT transformation

##### *Teradata*

##### Query

Copy code

```
 SELECT * FROM
 TD_UNPIVOT(
 	ON superunpivottest
 	USING
 	VALUE_COLUMNS('Income', 'Expenses')
 	UNPIVOT_COLUMN('Semester')
 	COLUMN_LIST('firstSemesterIncome, firstSemesterExpenses', 'secondSemesterIncome, secondSemesterExpenses')
    COLUMN_ALIAS_LIST('First', 'Second')
 )X ORDER BY mykey, Semester;
```

##### Result

Copy code

```
myKey |Semester |Income   | Expenses |
------+---------+---------+----------+
2018  |First    |18325.25 |15560.45  |
------+---------+---------+----------+
2018  |Second   |25220.65 |15680.33  |
------+---------+---------+----------+
2019  |First    |23855.75 |14582.55  |
------+---------+---------+----------+
2019  |Second   |34220.22 |24122.00  |
------+---------+---------+----------+
2020  |First    |15440.00 |10322.15  |
------+---------+---------+----------+
2020  |Second   |25430.57 |12355.36  |
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
 * FROM
 !!!RESOLVE EWI!!! /*** SSC-EWI-TD0061 - TD_UNPIVOT TRANSFORMATION REQUIRES COLUMN INFORMATION THAT COULD NOT BE FOUND, COLUMNS MISSING IN RESULT ***/!!!
 (
  SELECT
   TRIM(GET_IGNORE_CASE(OBJECT_CONSTRUCT('FIRSTSEMESTERINCOME', 'First', 'FIRSTSEMESTEREXPENSES', 'First', 'SECONDSEMESTERINCOME', 'Second', 'SECONDSEMESTEREXPENSES', 'Second'), Semester), '"') AS Semester,
   Income,
   Expenses
  FROM
   superunpivottest UNPIVOT(Income FOR Semester IN (
    firstSemesterIncome,
    secondSemesterIncome
   )) UNPIVOT(Expenses FOR Semester1 IN (
    firstSemesterExpenses,
    secondSemesterExpenses
   ))
  WHERE
   Semester = 'FIRSTSEMESTERINCOME'
   AND Semester1 = 'FIRSTSEMESTEREXPENSES'
   OR Semester = 'SECONDSEMESTERINCOME'
   AND Semester1 = 'SECONDSEMESTEREXPENSES'
 ) X ORDER BY mykey, Semester;
```

##### Result

Copy code

```
myKey |Semester |Income   | Expenses |
------+---------+---------+----------+
2018  |First    |18325.25 |15560.45  |
------+---------+---------+----------+
2018  |Second   |25220.65 |15680.33  |
------+---------+---------+----------+
2019  |First    |23855.75 |14582.55  |
------+---------+---------+----------+
2019  |Second   |34220.22 |24122.00  |
------+---------+---------+----------+
2020  |First    |15440.00 |10322.15  |
------+---------+---------+----------+
2020  |Second   |25430.57 |12355.36  |
```

### Known Issues

1. **TD\_UNPIVOT with INCLUDE\_NULLS clause set to YES is not supported**

Snowflake UNPIVOT function used in the transformation will ignore null values always, and the user will be warned that the INCLUDE\_NULLS clause is not supported when it is set to YES.

2. **Table information is required to correctly transform the function**

The name of the columns that are being used in the TD\_UNPIVOT function is needed; if the user does not include the columns list in the query\_expression of the function but provides the name of the table being unpivoted, then it will try to retrieve the column names from the table definition. If the names can not be found then the user will be warned that the resulting query might be losing columns in the result.

### Related EWIs

1. [SSC-EWI-TD0061](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0061): TD\_UNPIVOT transformation requires column information that could not be found, columns missing in result.

## TO\_CHAR

### Description

The TO\_CHAR function casts a DateTime or numeric value to a string. For more information check [TO\_CHAR(Numeric)](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/4xbLyOA_385QLYctkj~hjw) and [TO\_CHAR(DateTime)](https://docs.teradata.com/r/kmuOwjp1zEYg98JsB8fu_A/he2a_fFPveMN9cjMlF3Tqg).

Copy code

```
-- Numeric version
[TD_SYSFNLIB.]TO_CHAR(numeric_expr [, format_arg [, nls_param]])

-- DateTime version
[TD_SYSFNLIB.]TO_CHAR(dateTime_expr [, format_arg])
```

Both Snowflake and Teradata have their own version of the TO\_CHAR function, however, Teradata supports plenty of formats that are not natively supported by Snowflake. To support these format elements Snowflake built-in functions and custom UDFs are used to generate a concatenation expression that produces the same string as the original TO\_CHAR function in Teradata.

### Sample Source Patterns

#### TO\_CHAR(DateTime) transformation

##### *Teradata*

**Query**

Copy code

```
SELECT
TO_CHAR(date '2012-12-23'),
TO_CHAR(date '2012-12-23', 'DS'),
TO_CHAR(date '2012-12-23', 'DAY DD, MON YY');
```

**Result**

Copy code

```
COLUMN1    | COLUMN2    | COLUMN3           |
-----------+------------+-------------------+
2012/12/23 | 12/23/2012 | SUNDAY 23, DEC 12 |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
TO_CHAR(date '2012-12-23') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
TO_CHAR(date '2012-12-23', 'MM/DD/YYYY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
PUBLIC.DAYNAME_LONG_UDF(date '2012-12-23', 'uppercase') || TO_CHAR(date '2012-12-23', ' DD, ') || PUBLIC.MONTH_SHORT_UDF(date '2012-12-23', 'uppercase') || TO_CHAR(date '2012-12-23', ' YY') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

**Result**

Copy code

```
COLUMN1    | COLUMN2    | COLUMN3           |
-----------+------------+-------------------+
2012/12/23 | 12/23/2012 | SUNDAY 23, DEC 12 |
```

#### TO\_CHAR(Numeric) transformation

##### *Teradata*

**Query**

Copy code

```
SELECT
TO_CHAR(1255.495),
TO_CHAR(1255.495, '9.9EEEE'),
TO_CHAR(1255.495, 'SC9999.9999', 'nls_iso_currency = ''EUR''');
```

**Result**

Copy code

```
COLUMN1  | COLUMN2 | COLUMN3       |
---------+---------+---------------+
1255.495 | 1.3E+03 | +EUR1255.4950 |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
TO_CHAR(1255.495) /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
TO_CHAR(1255.495, '9.0EEEE') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/,
PUBLIC.INSERT_CURRENCY_UDF(TO_CHAR(1255.495, 'S9999.0000'), 2, 'EUR') /*** SSC-FDM-TD0029 - SNOWFLAKE SUPPORTED FORMATS FOR TO_CHAR DIFFER FROM TERADATA AND MAY FAIL OR HAVE DIFFERENT BEHAVIOR ***/;
```

**Result**

Copy code

```
COLUMN1  | COLUMN2 | COLUMN3       |
---------+---------+---------------+
1255.495 | 1.3E+03 | +EUR1255.4950 |
```

### Known Issues

**1. Formats with different or unsupported behaviors**

Teradata offers an extensive list of format elements that may show different behavior in Snowflake after the transformation of the TO\_CHAR function. For the list of elements with different or unsupported behaviors check [SSC-EWI-TD0029](../../../issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0029).

### Related EWIs

1. [SSC-FDM-TD0029](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0029): Snowflake supported formats for TO\_CHAR differ from Teradata and may fail or have different behavior.

## XMLAGG

### Description

Construct an XML value by performing an aggregation of multiple rows. For more information check [XMLAGG](https://docs.teradata.com/r/Teradata-VantageTM-XML-Data-Type/June-2020/Functions-for-XML-Type-and-XQuery/XMLAGG).

Copy code

```
XMLAGG (
  XML_value_expr
  [ ORDER BY order_by_spec [,...] ]
  [ RETURNING { CONTENT | SEQUENCE } ]
)

order_by_spec := sort_key [ ASC | DESC ] [ NULLS { FIRST | LAST } ]
```

### Sample Source Patterns

#### Setup data

##### Teradata

**Query**

Copy code

```
create table orders (
	o_orderkey int,
	o_totalprice float);

insert into orders values (1,500000);
insert into orders values (2,100000);
insert into orders values (3,600000);
insert into orders values (4,700000);
```

##### *Snowflake*

**Query**

Copy code

```
CREATE OR REPLACE TABLE orders (
	o_orderkey int,
	o_totalprice float)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

INSERT INTO orders
VALUES (1,500000);

INSERT INTO orders
VALUES (2,100000);

INSERT INTO orders
VALUES (3,600000);

INSERT INTO orders
VALUES (4,700000);
```

#### XMLAGG transformation

##### *Teradata*

**Query**

Copy code

```
select
    xmlagg(o_orderkey order by o_totalprice desc) (varchar(10000))
from orders
where o_totalprice > 5;
```

**Result**

Copy code

```
COLUMN1 |
--------+
4 3 1 2 |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
    LEFT(TO_VARCHAR(LISTAGG ( o_orderkey, ' ')
    WITHIN GROUP(
 order by o_totalprice DESC NULLS LAST)), 10000)
    from
    orders
    where o_totalprice > 5;
```

**Result**

Copy code

```
COLUMN1 |
--------+
4 3 1 2 |
```

### Known Issues

**1. The RETURNING clause is currently not supported.**

The user will be warned that the translation of the returning clause will be added in the future.

### Related EWIs

No related EWIs.

## CAST

## Cast from Number Datatypes to Varchar Datatype

Teradata when casts to varchar uses default formats for each number datatype, so formats are added to keep the equivalence among platforms.

### Sample Source Patterns

#### BYTEINT

##### *Teradata*

**Query**

Copy code

```
SELECT '"'||cast(cast(12 as BYTEINT) as varchar(10))||'"';
```

**Result**

Copy code

```
(('"'||12)||'"')|
----------------+
"12"            |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
'"'|| LEFT(TO_VARCHAR(cast(12 as BYTEINT), 'TM'), 10) ||'"';
```

**Result**

Copy code

```
"'""'|| LEFT(TO_VARCHAR(CAST(12 AS BYTEINT), 'TM'), 10) ||'""'"
---------------------------------------------------------------
"12"
```

#### SMALLINT

##### *Teradata*

**Query**

Copy code

```
SELECT '"'||cast(cast(123 as SMALLINT) as varchar(10))||'"';
```

**Result**

Copy code

```
(('"'||123)||'"')|
-----------------+
"123"            |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(123 AS SMALLINT), 'TM'), 10) ||'"';
```

**Result**

Copy code

```
"'""'|| LEFT(TO_VARCHAR(CAST(123 AS SMALLINT), 'TM'), 10) ||'""'"
-----------------------------------------------------------------
"123"
```

#### INTEGER

##### *Teradata*

**Query**

Copy code

```
SELECT '"'||cast(cast(12345 as INTEGER) as varchar(10))||'"';
```

**Result**

Copy code

```
(('"'||12345)||'"')|
-------------------+
"12345"            |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS INTEGER), 'TM'), 10) ||'"';
```

**Result**

Copy code

```
"'""'|| LEFT(TO_VARCHAR(CAST(12345 AS INTEGER), 'TM'), 10) ||'""'"
------------------------------------------------------------------
"12345"
```

#### BIGINT

##### *Teradata*

**Query**

Copy code

```
SELECT '"'||cast(cast(12345 as BIGINT) as varchar(10))||'"';
```

**Result**

Copy code

```
(('"'||12345)||'"')|
-------------------+
"12345"            |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
       '"'|| LEFT(TO_VARCHAR(CAST(12345 AS BIGINT), 'TM'), 10) ||'"';
```

**Result**

Copy code

```
"'""'|| LEFT(TO_VARCHAR(CAST(12345 AS BIGINT), 'TM'), 10) ||'""'"
-----------------------------------------------------------------
"12345"
```

#### DECIMAL[(n[,m])] or NUMERIC[(n[,m])]

##### *Teradata*

**Query**

Copy code

```
SELECT '"'||cast(cast(12345 as DECIMAL) as varchar(10))||'"',
       '"'||cast(cast(12345 as DECIMAL(12, 2)) as varchar(10))||'"';
```

**Result**

Copy code

```
(('"'||12345)||'"')|(('"'||12345)||'"')|
-------------------+-------------------+
"12345."           |"12345.00"         |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL), 'TM.'), 10) ||'"',
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL(12, 2)), 'TM'), 10) ||'"';
```

**Result**

Copy code

```
'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL), 'TM.'), 10) ||'"'	'"'|| LEFT(TO_VARCHAR(CAST(12345 AS DECIMAL(12, 2)), 'TM'), 10) ||'"'
"12345."	"12345.00"
```

### Known Issues

- Teradata treats the numbers between 0 and 1 differently than Snowflake. For those values, Teradata does not add the zero before the dot; meanwhile, Snowflake does.

#### *Teradata*

**Query**

Copy code

```
SELECT '"'||cast(cast(-0.1 as DECIMAL(12, 2)) as varchar(10))||'"' AS column1,
       '"'||cast(cast(0.1 as DECIMAL(12, 2)) as varchar(10))||'"' AS column2;
```

**Result**

Copy code

```
COLUMN1          |COLUMN2
-----------------+--------------+
"-.10"           |".10"         |
```

#### *Snowflake*

**Query**

Copy code

```
SELECT
'"'|| LEFT(TO_VARCHAR(CAST(-0.1 AS DECIMAL(12, 2)), 'TM'), 10) ||'"' AS column1,
'"'|| LEFT(TO_VARCHAR(CAST(0.1 AS DECIMAL(12, 2)), 'TM'), 10) ||'"' AS column2;
```

**Result**

Copy code

```
COLUMN1           |COLUMN2
------------------+---------------+
"-0.10"           |"0.10"         |
```

### Related EWIs

No related EWIs.

## Cast to DATE using

### Description

The following syntax casts a date-formatted string to DATE datatype by putting a d before the string definition inside curly braces.

Copy code

```
SELECT {d '1233-10-10'}
```

### Sample Source Patterns

#### Cast to DATE using curly braces

**Teradata**

**Cast to Date**

Copy code

```
SELECT * FROM RESOURCE_DETAILS where change_ts >= {d '2022-09-10'};
```

**Snowflake**

**Cast to Date**

Copy code

```
SELECT
* FROM
PUBLIC.RESOURCE_DETAILS
where change_ts >= DATE('2022-09-10');
```

## Cast string expressions to TIMESTAMP/DATE

### Description

When a CAST expression converts a string-typed operand (column reference, concatenation, or expression) to a TIMESTAMP or DATE type without an explicit FORMAT clause, it is converted to the appropriate Snowflake function:

- `TO_TIMESTAMP(expr)` — when the target is TIMESTAMP and no timezone offset is detected
- `TO_TIMESTAMP_TZ(expr)` — when the target is TIMESTAMP and the concatenation includes a timezone offset literal (e.g., `'+00:00'` or `'-05:00'`)
- `TO_DATE(expr, format)` — when the target is DATE

For TIMESTAMP targets with non-literal operands, the format argument is omitted to let Snowflake’s AUTO format detection handle the conversion at runtime. This avoids hardcoding a format that may not match the actual data.

When a timezone offset literal is detected in a concatenation expression, `TO_TIMESTAMP_TZ` is used instead of `TO_TIMESTAMP` to preserve timezone information. Per Snowflake documentation, using `TO_TIMESTAMP` (which produces `TIMESTAMP_NTZ`) with timezone data silently discards the timezone offset.

For string literal operands (e.g., `CAST('2022-11-01' AS TIMESTAMP)`), a default format is applied and dashes are replaced with slashes to match Snowflake conventions.

### Sample Source Patterns

#### Concatenation with timezone offset to TIMESTAMP

##### *Teradata*

**Concatenation with TZ offset**

Copy code

```
SELECT CAST(SQ.EXTRACTION_DATE || '.000000' || '+00:00' AS TIMESTAMP(6)) AS EXTRACTION_DATE;
```

##### *Snowflake*

**Concatenation with TZ offset**

Copy code

```
SELECT
  TO_TIMESTAMP_TZ(SQ.EXTRACTION_DATE || '.000000' || '+00:00') AS EXTRACTION_DATE;
```

#### Concatenation with negative timezone offset to TIMESTAMP

##### *Teradata*

**Concatenation with negative TZ offset**

Copy code

```
SELECT CAST(COL1 || '.000000' || '-05:00' AS TIMESTAMP(6));
```

##### *Snowflake*

**Concatenation with negative TZ offset**

Copy code

```
SELECT
  TO_TIMESTAMP_TZ(COL1 || '.000000' || '-05:00');
```

#### Concatenation without timezone offset to TIMESTAMP

##### *Teradata*

**Concatenation without TZ offset**

Copy code

```
SELECT CAST(COL1 || '.000000' AS TIMESTAMP(6));
```

##### *Snowflake*

**Concatenation without TZ offset**

Copy code

```
SELECT
  TO_TIMESTAMP(COL1 || '.000000');
```

#### Column reference to TIMESTAMP without FORMAT

##### *Teradata*

**Column ref to TIMESTAMP**

Copy code

```
SELECT CAST(COL1 AS TIMESTAMP);
```

##### *Snowflake*

**Column ref to TIMESTAMP**

Copy code

```
SELECT
  TO_TIMESTAMP(COL1);
```

#### Concatenation to DATE

##### *Teradata*

**Concatenation to DATE**

Copy code

```
SELECT CAST(COL1 || '-01' AS DATE);
```

##### *Snowflake*

**Concatenation to DATE**

Copy code

```
SELECT
  TO_DATE(COL1 || '-01', 'YYYY/MM/DD');
```

### Known Issues

No related issues.

### Related EWIs

No related EWIs.

## Cast to INTERVAL datatype

### Description

Snowflake does not support the Interval data type, but it has INTERVAL constants that can be used in DateTime operations and other uses can be emulated using VARCHAR, CAST functions to the INTERVAL datatype will be transformed into an equivalent depending on the case:

- When the value being casted is of type interval an UDF will be generated to produce the new interval equivalent as a string
- When the value is a literal, a Snowflake interval constant will be generated if the cast is used in a datetime operation, otherwise a literal string will be generated
- When the value is non-literal then a cast to string will be generated

### Sample Source Patterns

#### Non-interval literals

##### *Teradata*

**Query**

Copy code

```
SELECT TIMESTAMP '2022-10-15 10:30:00' + CAST ('12:34:56.78' AS INTERVAL HOUR(2) TO SECOND(2)) AS VARCHAR_TO_INTERVAL,
TIMESTAMP '2022-10-15 10:30:00' + CAST(-5 AS INTERVAL YEAR(4)) AS NUMBER_TO_INTERVAL,
CAST('07:00' AS INTERVAL HOUR(2) TO MINUTE) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

Copy code

```
VARCHAR_TO_INTERVAL | NUMBER_TO_INTERVAL | OUTSIDE_DATETIME_OPERATION |
--------------------+--------------------+----------------------------+
2022-10-15 23:04:56 |2017-10-15 10:30:00 | 7:00                       |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
TIMESTAMP '2022-10-15 10:30:00' + INTERVAL '12 HOUR, 34 MINUTE, 56 SECOND, 780000 MICROSECOND' AS VARCHAR_TO_INTERVAL,
TIMESTAMP '2022-10-15 10:30:00' + INTERVAL '-5 YEAR' AS NUMBER_TO_INTERVAL,
'07:00' AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

Copy code

```
VARCHAR_TO_INTERVAL     | NUMBER_TO_INTERVAL     | OUTSIDE_DATETIME_OPERATION |
------------------------+------------------------+----------------------------+
2022-10-15 23:04:56.780 |2017-10-15 10:30:00.000 | 07:00                      |
```

#### Non-literal and non-interval values

##### *Teradata*

**Query**

Copy code

```
SELECT TIMESTAMP '2022-10-15 10:30:00' + CAST('20 ' || '10' AS INTERVAL DAY TO HOUR) AS DATETIME_OPERATION,
CAST('20 ' || '10' AS INTERVAL DAY TO HOUR) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

Copy code

```
DATETIME_OPERATION  | OUTSIDE_DATETIME_OPERATION |
--------------------+----------------------------+
2022-11-04 20:30:00 | 20 10                      |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
PUBLIC.DATETIMEINTERVALADD_UDF(TIMESTAMP '2022-10-15 10:30:00', CAST('20 ' || '10' AS VARCHAR(21)), 'DAY', '+') AS DATETIME_OPERATION,
CAST('20 ' || '10' AS VARCHAR(21)) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

Copy code

```
DATETIME_OPERATION      | OUTSIDE_DATETIME_OPERATION |
------------------------+----------------------------+
2022-11-04 20:30:00.000 | 20 10                      |
```

#### Cast of interval to another interval

##### *Teradata*

**Query**

Copy code

```
SELECT
TIMESTAMP '2022-10-15 10:30:00' + CAST(INTERVAL '5999' MINUTE AS INTERVAL DAY TO HOUR) AS DATETIME_OPERATION,
CAST(INTERVAL '5999' MINUTE AS INTERVAL DAY TO HOUR) AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

Copy code

```
DATETIME_OPERATION  | OUTSIDE_DATETIME_OPERATION |
--------------------+----------------------------+
2022-10-19 13:30:00 | 4 03                       |
```

##### *Snowflake*

**Query**

Copy code

```
SELECT
PUBLIC.DATETIMEINTERVALADD_UDF(
TIMESTAMP '2022-10-15 10:30:00', PUBLIC.INTERVALTOINTERVAL_UDF('5999', 'MINUTE', 'MINUTE', 'DAY', 'HOUR'), 'DAY', '+') AS DATETIME_OPERATION,
PUBLIC.INTERVALTOINTERVAL_UDF('5999', 'MINUTE', 'MINUTE', 'DAY', 'HOUR') AS OUTSIDE_DATETIME_OPERATION;
```

**Result**

Copy code

```
DATETIME_OPERATION      | OUTSIDE_DATETIME_OPERATION |
------------------------+----------------------------+
2022-10-19 13:30:00.000 | 4 03                       |
```

### Known Issues

**No known issues.**

### Related EWIs

No related EWIs.
