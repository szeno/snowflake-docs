# Redshift - Built-in functions

Note

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../general/built-in-functions).

## Aggregate Functions

> Aggregate functions compute a single result value from a set of input values. ([Redshift SQL Language Reference Aggregate Functions](https://docs.aws.amazon.com/redshift/latest/dg/c_Aggregate_Functions.html)).

| Redshift | Snowflake |
| --- | --- |
| [ANY\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/any_value) ( [ DISTINCT | ALL ] expression ) | [ANY\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/any_value) ( [ DISTINCT ]expression )    *Notes: Snowflake supports the grammar, though ALL is disallowed. DISTINCT has no effect in either.* |
| [AVG](https://docs.aws.amazon.com/redshift/latest/dg/r_AVG.html) ( [ DISTINCT | ALL ] *expression* ) | [AVG](https://docs.snowflake.com/en/sql-reference/functions/avg) ( [ DISTINCT ] expression)    *Notes: Redshift and Snowflake may show different precision/decimals due to data type rounding/formatting.* |
| [COUNT](https://docs.aws.amazon.com/redshift/latest/dg/r_COUNT.html) | [COUNT](https://docs.snowflake.com/en/sql-reference/functions/count) |
| [LISTAGG](https://docs.aws.amazon.com/redshift/latest/dg/r_LISTAGG.html) | [LISTAGG](https://docs.snowflake.com/en/sql-reference/functions/listagg)    *Notes: Redshift’s DISTINCT ignores trailing spaces (‘a ‘ = ‘a’); Snowflake’s does not. (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [MAX](https://docs.aws.amazon.com/redshift/latest/dg/r_MAX.html) | [MAX](https://docs.snowflake.com/en/sql-reference/functions/max) |
| [MEDIAN](https://docs.aws.amazon.com/redshift/latest/dg/r_MEDIAN.html) | [MEDIAN](https://docs.snowflake.com/en/sql-reference/functions/median)    *Notes**: Snowflake does not allow the use of date types**, while Redshift does. (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [MIN](https://docs.aws.amazon.com/redshift/latest/dg/r_MIN.html) | [MIN](https://docs.snowflake.com/en/sql-reference/functions/min) |
| [PERCENTILE\_CONT](https://docs.aws.amazon.com/redshift/latest/dg/r_PERCENTILE_CONT.html) | [PERCENTILE\_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont) |
| [STDDEV/STDDEV\_SAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_STDDEV_functions.html) ( [ DISTINCT | ALL ] *expression*)    [STDDEV\_POP](https://docs.aws.amazon.com/redshift/latest/dg/r_STDDEV_functions.html) ( [ DISTINCT | ALL ] *expression*) | [STDDEV/STDDEV\_SAMP](https://docs.snowflake.com/en/sql-reference/functions/stddev) ( [ DISTINCT ] *expression*)    [STDDEV\_POP](https://docs.snowflake.com/en/sql-reference/functions/stddev_pop) ( [ DISTINCT ] *expression*)    *Notes: Snowflake supports all the grammar, though ALL is disallowed.* |
| [SUM](https://docs.aws.amazon.com/redshift/latest/dg/r_SUM.html) | [SUM](https://docs.snowflake.com/en/sql-reference/functions/sum) |
| [VARIANCE/VAR\_SAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_VARIANCE_functions.html) ( [ DISTINCT | ALL ] *expression*)    [VAR\_POP](https://docs.aws.amazon.com/redshift/latest/dg/r_VARIANCE_functions.html) ( [ DISTINCT | ALL ] *expression*) | [VARIANCE/VAR\_SAMP](https://docs.snowflake.com/en/sql-reference/functions/variance)  ( [ DISTINCT ] *expression*)    [VAR\_POP](https://docs.snowflake.com/en/sql-reference/functions/variance_pop) ( [ DISTINCT ] *expression*)    *Notes: Snowflake supports all the grammar, though ALL is disallowed.* |

Expand

Show lessSee more

## Array Functions

> Creates an array of the SUPER data type. ([Redshift SQL Language Reference Array Functions](https://docs.aws.amazon.com/redshift/latest/dg/c_Array_Functions.html)).

| Redshift | Snowflake |
| --- | --- |
| [ARRAY](https://docs.aws.amazon.com/redshift/latest/dg/r_array.html) ( [ expr1 ] [ , expr2 [ , … ] ] ) | [ARRAY\_CONSTRUCT](https://docs.snowflake.com/en/sql-reference/functions/array_construct)  ( [ <expr1> ] [ , <expr2> [ , … ] ] ) |
| [ARRAY\_CONCAT](https://docs.aws.amazon.com/redshift/latest/dg/r_array_concat.html) ( super\_expr1, super\_expr2 ) | [ARRAY\_CAT](https://docs.snowflake.com/en/sql-reference/functions/array_cat) ( &lt;array1> , &lt;array2> ) |
| [ARRAY\_FLATTEN](https://docs.aws.amazon.com/redshift/latest/dg/array_flatten.html)  ( *super\_expr1*,*super\_expr2*,.. ) | [ARRAY\_FLATTEN](https://docs.snowflake.com/en/sql-reference/functions/array_flatten) ( <array> )    *Notes: the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [GET\_ARRAY\_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/get_array_length.html) ( *super\_expr* ) | [ARRAY\_SIZE](https://docs.snowflake.com/en/sql-reference/functions/array_size) ( &lt;array> | &lt;variant>) |
| [SPLIT\_TO\_ARRAY](https://docs.aws.amazon.com/redshift/latest/dg/split_to_array.html) ( *string*,*delimiter* ) | [SPLIT](https://docs.snowflake.com/en/sql-reference/functions/split) (<string>, <separator>)    *Notes: Redshift allows missing delimiters; Snowflake requires them, defaulting to comma* |
| [SUBARRAY](https://docs.aws.amazon.com/redshift/latest/dg/r_subarray.html) ( *super\_expr*, *start\_position*, *length* ) | [ARRAY\_SLICE](https://docs.snowflake.com/en/sql-reference/functions/array_slice) ( <array> , <from> , <to> )    *Notes: Function names and the second argument differ; adjust arguments for equivalence.* |

Expand

Show lessSee more

## Conditional expressions

| Redshift | Snowflake |
| --- | --- |
| [DECODE](https://docs.aws.amazon.com/redshift/latest/dg/r_DECODE_expression.html) | [DECODE](https://docs.snowflake.com/en/sql-reference/functions/decode)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [COALESCE](https://docs.aws.amazon.com/redshift/latest/dg/r_NVL_function.html) ( *expression*, *expression*, … ) | [COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce) ( *expression*, *expression*, … ) |
| [GREATEST](https://docs.aws.amazon.com/redshift/latest/dg/r_GREATEST_LEAST.html) ( value [, …] ) | [GREATEST\_IGNORE\_NULLS](https://docs.snowflake.com/en/sql-reference/functions/greatest_ignore_nulls) ( <expr1> [, <expr2> … ] ) |
| [LEAST](https://docs.aws.amazon.com/redshift/latest/dg/r_GREATEST_LEAST.html) ( value [, …] ) | [LEAST\_IGNORE\_NULLS](https://docs.snowflake.com/en/sql-reference/functions/least_ignore_nulls) ( &lt;expr1> [, &lt;expr2> … ]) |
| [NVL](https://docs.aws.amazon.com/redshift/latest/dg/r_NVL_function.html)( *expression*, *expression*, … ) | [*NVL*](https://docs.snowflake.com/en/sql-reference/functions/nvl) *( expression, expression )*    *Notes: Redshift’s NVL accepts multiple arguments; Snowflake’s NVL accepts only two. To match Redshift behavior, NVL with more than two arguments is converted to COALESCE.* |
| [NVL2](https://docs.aws.amazon.com/redshift/latest/dg/r_NVL2.html) | [NVL2](https://docs.snowflake.com/en/sql-reference/functions/nvl2) |
| [NULLIF](https://docs.aws.amazon.com/redshift/latest/dg/r_NULLIF_function.html) | [NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif)    *Notes: Redshift’s NULLIF ignores trailing spaces in some string comparisons, unlike Snowflake. Therefore, the transformation adds RTRIM for equivalence.* |

Expand

Show lessSee more

## Data type formatting functions

> Data type formatting functions provide an easy way to convert values from one data type to another. For each of these functions, the first argument is always the value to be formatted and the second argument contains the template for the new format. ([Redshift SQL Language Reference Data type formatting functions](https://docs.aws.amazon.com/redshift/latest/dg/r_Data_type_formatting.html)).

| Redshift | Snowflake |
| --- | --- |
| [TO\_CHAR](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_CHAR.html) | [TO\_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char)    *Notes: Snowflake’s support for this function is partial (see* [*SSC-EWI-0006*](../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0006)*).* |
| [TO\_DATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_DATE_function.html) | [TO\_DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date)    *Notes: Snowflake’s `TO_DATE` fails on invalid dates like ’20010631’ (June has 30 days), unlike Redshift’s lenient `TO_DATE`. Use `TRY_TO_DATE` in Snowflake to handle these cases by returning NULL. (see* [*SSC-FDM-RS0004*](../../../issues-and-troubleshooting/functional-difference/redshift/ssc-fdm-rs0004.md)*,* [*SSC-EWI-0006*](../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0006)*,* [*SSC-FDM-0032*](../../../issues-and-troubleshooting/functional-difference/general/ssc-fdm-0032.md)*).* |

Expand

Show lessSee more

## Date and time functions

| Redshift | Snowflake |
| --- | --- |
| [ADD\_MONTHS](https://docs.aws.amazon.com/redshift/latest/dg/r_ADD_MONTHS.html) | [ADD\_MONTHS](https://docs.snowflake.com/en/sql-reference/functions/add_months)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [AT TIME ZONE ‘timezone’](https://docs.aws.amazon.com/redshift/latest/dg/r_AT_TIME_ZONE.html) | [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <source\_tz> , <target\_tz> , <source\_timestamp\_ntz> )    [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <target\_tz> , <source\_timestamp> )    *Notes: Redshift defaults to UTC; the Snowflake function requires explicit UTC specification. Therefore, it will be added as the target timezone.* |
| [CONVERT\_TIMEZONE](https://docs.aws.amazon.com/redshift/latest/dg/CONVERT_TIMEZONE.html) | [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) |
| [CURRENT\_DATE](https://docs.aws.amazon.com/redshift/latest/dg/r_CURRENT_DATE_function.html) | [CURRENT\_DATE()](https://docs.snowflake.com/en/sql-reference/functions/current_date) |
| [DATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_DATE_function.html) | [DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date) |
| [DATEADD/DATE\_ADD](https://docs.aws.amazon.com/redshift/latest/dg/r_DATEADD_function.html) ( *datepart*, *interval*, {*date* | *time* | *timetz* | *timestamp*} ) | [DATE\_ADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd) ( <date\_or\_time\_part>, <value>, <date\_or\_time\_expr> )    *Notes: Invalid date part formats are translated to Snowflake-compatible formats.* |
| [DATEDIFF/DATE\_DIFF](https://docs.aws.amazon.com/redshift/latest/dg/r_DATEDIFF_function.html) | [DATEDIFF](https://docs.snowflake.com/en/sql-reference/functions/datediff)    *Notes: Invalid date part formats are translated to Snowflake-compatible formats.* |
| [DATE\_PART/PGDATE\_PART](https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_function.html) | [DATE\_PART](https://docs.snowflake.com/en/sql-reference/functions/date_part)    *Notes: this function is partially supported by Snowflake. (See* [*SSC-EWI-0006*](../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0006)*).* |
| [DATE\_PART\_YEAR](https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_YEAR.html) (*date*) | [YEAR](https://docs.snowflake.com/en/sql-reference/functions/year) ( <date\_or\_timestamp\_expr> )    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [DATE\_TRUNC](https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_TRUNC.html) | [DATE\_TRUNC](https://docs.snowflake.com/en/sql-reference/functions/date_trunc)    *Notes: Invalid date part formats are translated to Snowflake-compatible formats.* |
| [GETDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_GETDATE.html)() | [GETDATE](https://docs.snowflake.com/en/sql-reference/functions/getdate)() |
| [LAST\_DAY](https://docs.aws.amazon.com/redshift/latest/dg/r_LAST_DAY.html) | [LAST\_DAY](https://docs.snowflake.com/en/sql-reference/functions/last_day)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [NEXT\_DAY](https://docs.aws.amazon.com/redshift/latest/dg/r_NEXT_DAY.html) | [NEXT\_DAY](https://docs.snowflake.com/en/sql-reference/functions/next_day)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [SYSDATE](https://docs.aws.amazon.com/redshift/latest/dg/r_SYSDATE.html) | [SYSDATE](https://docs.snowflake.com/en/sql-reference/functions/sysdate)() |
| [TIMESTAMP](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_TIMESTAMP.html) | [TO\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp) |
| [TRUNC](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNC_date.html) | [TRUNC](https://docs.snowflakhttps/docs.snowflake.com/en/sql-reference/functions/trunc2e.com/en/sql-reference/functions/trunc2) |
| [EXTRACT](https://docs.aws.amazon.com/redshift/latest/dg/r_EXTRACT_function.html) | [EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/extract)  *Notes:* Part-time or Date time supported: DAY, DOW, DOY, EPOCH, HOUR, MINUTE, MONTH, QUARTER, SECOND, WEEK, YEAR. |

Expand

Show lessSee more

Note

Redshift timestamps default to microsecond precision (6 digits); Snowflake defaults to nanosecond precision (9 digits). Adjust precision as needed using ALTER SESSION (for example, `ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF2';`). Precision loss may occur depending on the data type used.  
  
Since some formats are incompatible with Snowflake, adjusting the account parameters [DATE\_INPUT\_FORMAT or TIME\_INPUT\_FORMAT](https://docs.snowflake.com/en/sql-reference/date-time-input-output#data-loading) might maintain functional equivalence between platforms.

## Hash Functions

> A hash function is a mathematical function that converts a numerical input value into another value. ([Redshift SQL Language Reference Hash functions](https://docs.aws.amazon.com/redshift/latest/dg/hash-functions.html)).

| Redshift | Snowflake |
| --- | --- |
| [FNV\_HASH](https://docs.aws.amazon.com/redshift/latest/dg/r_FNV_HASH.html) (value [, seed]) | [*HASH*](https://docs.snowflake.com/en/sql-reference/functions/hash) *( <expr> [ , <expr> … ] | \*)*    *Notes: In Redshift’s FNV\_HASH function, the seed parameter is optional, but it is not used in the Snowflake’s Hash function since the seed parameter is only used on FNV algorithm.* |

Expand

Show lessSee more

## JSON Functions

| Redshift | Snowflake |
| --- | --- |
| [JSON\_EXTRACT\_PATH\_TEXT](https://docs.aws.amazon.com/redshift/latest/dg/JSON_EXTRACT_PATH_TEXT.html) | [JSON\_EXTRACT\_PATH\_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text)    *Notes:*   1. *Redshift treats newline, tab, and carriage return characters literally; Snowflake interprets them.* 2. *A JSON literal and dot-separated path are required to access nested objects in the Snowflake function.* 3. *Paths with spaces in variables must be quoted.* |

Expand

Show lessSee more

## Math functions

| Redshift | Snowflake |
| --- | --- |
| [ACOS](https://docs.aws.amazon.com/redshift/latest/dg/r_ACOS.html) | [ACOS](https://docs.snowflake.com/en/sql-reference/functions/acos) |
| [ASIN](https://docs.aws.amazon.com/redshift/latest/dg/r_ASIN.html) | [ASIN](https://docs.snowflake.com/en/sql-reference/functions/asin) |
| [ATAN](https://docs.aws.amazon.com/redshift/latest/dg/r_ATAN.html) | [ATAN](https://docs.snowflake.com/en/sql-reference/functions/atan) |
| [ATAN2](https://docs.aws.amazon.com/redshift/latest/dg/r_ATAN2.html) | [ATAN2](https://docs.snowflake.com/en/sql-reference/functions/atan2) |
| [CBRT](https://docs.aws.amazon.com/redshift/latest/dg/r_CBRT.html) | [CBRT](https://docs.snowflake.com/en/sql-reference/functions/cbrt) |
| [CEIL/CEILING](https://docs.aws.amazon.com/redshift/latest/dg/r_CEILING_FLOOR.html) | [CEIL](https://docs.snowflake.com/en/sql-reference/functions/ceil) |
| [COS](https://docs.aws.amazon.com/redshift/latest/dg/r_COS.html) | [COS](https://docs.snowflake.com/en/sql-reference/functions/cos) |
| [COT](https://docs.aws.amazon.com/redshift/latest/dg/r_COT.html) | [COT](https://docs.snowflake.com/en/sql-reference/functions/cot) |
| [DEGREES](https://docs.aws.amazon.com/redshift/latest/dg/r_DEGREES.html) | [DEGREES](https://docs.snowflake.com/en/sql-reference/functions/degrees) |
| [DEXP](https://docs.aws.amazon.com/redshift/latest/dg/r_DEXP.html) | [EXP](https://docs.snowflake.com/en/sql-reference/functions/exp) |
| [DLOG1/LN](https://docs.aws.amazon.com/redshift/latest/dg/r_DLOG1.html) | [LN](https://docs.snowflake.com/en/sql-reference/functions/ln) |
| [DLOG10](https://docs.aws.amazon.com/redshift/latest/dg/r_DLOG10.html) (*number*) | [LOG](https://docs.snowflake.com/en/sql-reference/functions/log) (10, *number*) |
| [EXP](https://docs.aws.amazon.com/redshift/latest/dg/r_EXP.html) | [EXP](https://docs.snowflake.com/en/sql-reference/functions/exp) |
| [FLOOR](https://docs.aws.amazon.com/redshift/latest/dg/r_FLOOR.html) | [FLOOR](https://docs.snowflake.com/en/sql-reference/functions/floor) |
| [LOG](https://docs.aws.amazon.com/redshift/latest/dg/r_LOG.html) | [LOG](https://docs.snowflake.com/en/sql-reference/functions/log) |
| [MOD](https://docs.aws.amazon.com/redshift/latest/dg/r_MOD.html) | [MOD](https://docs.snowflake.com/en/sql-reference/functions/mod) |
| [PI](https://docs.aws.amazon.com/redshift/latest/dg/r_PI.html) | [PI](https://docs.snowflake.com/en/sql-reference/functions/pi) |
| [POWER/POW](https://docs.aws.amazon.com/redshift/latest/dg/r_POWER.html) | [POWER/POW](https://docs.snowflake.com/en/sql-reference/functions/pow) |
| [RADIANS](https://docs.aws.amazon.com/redshift/latest/dg/r_RADIANS.html) | [RADIANS](https://docs.snowflake.com/en/sql-reference/functions/radians) |
| [RANDOM](https://docs.aws.amazon.com/redshift/latest/dg/r_RANDOM.html) | [RANDOM](https://docs.snowflake.com/en/sql-reference/functions/random) |
| [ROUND](https://docs.aws.amazon.com/redshift/latest/dg/r_ROUND.html) | [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round) |
| [SIN](https://docs.aws.amazon.com/redshift/latest/dg/r_SIN.html) | [SIN](https://docs.snowflake.com/en/sql-reference/functions/sin) |
| [SIGN](https://docs.aws.amazon.com/redshift/latest/dg/r_SIGN.html) | [SIGN](https://docs.snowflake.com/en/sql-reference/functions/sign) |
| [SQRT](https://docs.aws.amazon.com/redshift/latest/dg/r_SQRT.html) | [SQRT](https://docs.snowflake.com/en/sql-reference/functions/sqrt) |
| [TAN](https://docs.aws.amazon.com/redshift/latest/dg/r_TAN.html) | [TAN](https://docs.snowflake.com/en/sql-reference/functions/tan) |
| [TRUNC](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNC.html) | [TRUNC](https://docs.snowflake.com/en/sql-reference/functions/trunc) |

Expand

Show lessSee more

Note

Redshift and Snowflake results may differ in scale.

## String functions

> String functions process and manipulate character strings or expressions that evaluate to character strings. ([Redshift SQL Language Reference String functions](https://docs.aws.amazon.com/redshift/latest/dg/String_functions_header.html)).

| Redshift | Snowflake |
| --- | --- |
| [ASCII](https://docs.aws.amazon.com/redshift/latest/dg/r_ASCII.html) | [ASCII](https://docs.snowflake.com/en/sql-reference/functions/ascii) |
| [BTRIM](https://docs.aws.amazon.com/redshift/latest/dg/r_BTRIM.html) | [TRIM](https://docs.snowflake.com/en/sql-reference/functions/trim) |
| [CHAR\_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/r_CHAR_LENGTH.html) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [CHARACTER\_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/r_CHARACTER_LENGTH.html) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [CHARINDEX](https://docs.aws.amazon.com/redshift/latest/dg/r_CHARINDEX.html) | [CHARINDEX](https://docs.snowflake.com/en/sql-reference/functions/charindex) |
| [CHR](https://docs.aws.amazon.com/redshift/latest/dg/r_CHR.html) | [CHR](https://docs.snowflake.com/en/sql-reference/functions/chr) |
| [CONCAT](https://docs.aws.amazon.com/redshift/latest/dg/r_CONCAT.html) | [CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) |
| [INITCAP](https://docs.aws.amazon.com/redshift/latest/dg/r_INITCAP.html) | [INITCAP](https://docs.snowflake.com/en/sql-reference/functions/initcap) |
| [LEFT/RIGHT](https://docs.snowflake.com/en/sql-reference/functions/initcap) | [LEFT](https://docs.snowflake.com/en/sql-reference/functions/left)/[RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right)    *Notes: For negative lengths in `LEFT`/`RIGHT`, Snowflake returns an empty string; Redshift raises an error.* |
| [LEN](https://docs.aws.amazon.com/redshift/latest/dg/r_LEN.html) | [LEN](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [LOWER](https://docs.aws.amazon.com/redshift/latest/dg/r_LOWER.html) | [LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower) |
| [OCTET\_LENGTH](https://docs.aws.amazon.com/redshift/latest/dg/r_OCTET_LENGTH.html) | [OCTET\_LENGTH](https://docs.snowflake.com/en/sql-reference/functions/octet_length)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [QUOTE\_IDENT](https://docs.aws.amazon.com/redshift/latest/dg/r_QUOTE_IDENT.html) (*string*) | [CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) (‘”’, *string,* ‘”’) |
| [REGEXP\_REPLACE](https://docs.aws.amazon.com/redshift/latest/dg/REGEXP_REPLACE.html) | [REGEXP\_REPLACE](https://docs.snowflake.com/en/sql-reference/functions/regexp_replace)    *Notes: This function includes a `parameters` argument that enables the user to interpret the pattern using the Perl Compatible Regular Expression (PCRE) dialect, represented by the `p` value, this is removed to avoid any issues*. *(See* [*SSC-EWI-0009*](../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0009)*,* [*SC-FDM-0032*](../../../issues-and-troubleshooting/functional-difference/general/ssc-fdm-0032.md)*,* [*SSC-FDM-PG0011*](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0011.md)*).* |
| [REPEAT](https://docs.aws.amazon.com/redshift/latest/dg/r_REPEAT.html) | [REPEAT](https://docs.snowflake.com/en/sql-reference/functions/repeat) |
| [REPLACE](https://docs.aws.amazon.com/redshift/latest/dg/r_REPLACE.html) | [REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace) |
| [REPLICATE](https://docs.aws.amazon.com/redshift/latest/dg/r_REPLICATE.html) | [REPEAT](https://docs.snowflake.com/en/sql-reference/functions/repeat) |
| [REVERSE](https://docs.aws.amazon.com/redshift/latest/dg/r_REVERSE.html) | [REVERSE](https://docs.snowflake.com/en/sql-reference/functions/reverse) |
| [SOUNDEX](https://docs.aws.amazon.com/redshift/latest/dg/SOUNDEX.html) | [SOUNDEX](https://docs.snowflake.com/en/sql-reference/functions/soundex)    *Notes: Certain special characters, the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [SPLIT\_PART](https://docs.aws.amazon.com/redshift/latest/dg/SPLIT_PART.html) | [SPLIT\_PART](https://docs.snowflake.com/en/sql-reference/functions/split_part)    *Notes: Snowflake and Redshift handle SPLIT\_PART differently with case-insensitive collations.* |
| [STRPOS](https://docs.aws.amazon.com/redshift/latest/dg/r_STRPOS.html) (*string*, *substring* ) | [POSITION](https://docs.snowflake.com/en/sql-reference/functions/position) ( &lt;expr1> IN &lt;expr> ) |
| [SUBSTRING](https://docs.aws.amazon.com/redshift/latest/dg/r_SUBSTRING.html) | [*SUBSTRING*](https://docs.snowflake.com/en/sql-reference/functions/substr)    *Notes:* Snowflake partially supports this function. Redshift’s `SUBSTRING`, with a non-positive `start_position`, calculates `start_position + number_characters` (returning ‘’ if the result is non-positive). Snowflake’s behavior differs. (See [SSC-EWI-RS0006](../../../issues-and-troubleshooting/conversion-issues/redshift/ssc-ewi-rs0006.md)). |
| [TEXTLEN](https://docs.aws.amazon.com/redshift/latest/dg/r_TEXTLEN.html) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [TRANSLATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TRANSLATE.html) | [TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/translate) |
| [TRIM](https://docs.aws.amazon.com/redshift/latest/dg/r_TRIM.html) | [*TRIM*](https://docs.snowflake.com/en/sql-reference/functions/trim)    *Notes: Redshift uses keywords (BOTH, LEADING, TRAILING) for trim; Snowflake uses TRIM, LTRIM, RTRIM.* |
| [UPPER](https://docs.aws.amazon.com/redshift/latest/dg/r_UPPER.html) | [UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper) |

Expand

Show lessSee more

## SUPER type information functions

| Redshift | Snowflake |
| --- | --- |
| [IS\_ARRAY](https://docs.aws.amazon.com/redshift/latest/dg/r_is_array.html) | [IS\_ARRAY](https://docs.snowflake.com/en/sql-reference/functions/is_array)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [IS\_BOOLEAN](https://docs.aws.amazon.com/redshift/latest/dg/r_is_boolean.html) | [IS\_BOOLEAN](https://docs.snowflake.com/en/sql-reference/functions/is_boolean)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |

Expand

Show lessSee more

## Window functions

| Redshift | Snowflake |
| --- | --- |
| [AVG](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_AVG.html) | [*AVG*](https://docs.snowflake.com/en/sql-reference/functions/avg)    *Notes: AVG rounding/formatting can vary by data type between Redshift and Snowflake.* |
| [COUNT](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_COUNT.html) | [COUNT](https://docs.snowflake.com/en/sql-reference/functions/count) |
| [DENSE\_RANK](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_DENSE_RANK.html) | [DENSE\_RANK](https://docs.snowflake.com/en/sql-reference/functions/dense_rank)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [FIRST\_VALUE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_first_value.html) | [FIRST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value)    *Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY <expr>.`* |
| [LAG](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_LAG.html) | [LAG](https://docs.snowflake.com/en/sql-reference/functions/lag) |
| [LAST\_VALUE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_last_value.html) | [LAST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value)    *Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY <expr>`.* |
| [LEAD](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_LEAD.html) | [LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead)    *Notes: Redshift allows constant or expression offsets; Snowflake allows only constant offset*s. |
| [LISTAGG](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_LISTAGG.html) | [LISTAGG](https://docs.snowflake.com/en/sql-reference/functions/listagg)    *Notes: Redshift’s DISTINCT ignores trailing spaces (‘a ‘ = ‘a’); Snowflake’s does not. (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [MEDIAN](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_MEDIAN.html) | [MEDIAN](https://docs.snowflake.com/en/sql-reference/functions/median)    *Notes**: Snowflake does not allow the use of date types**, while Redshift does. (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [NTH\_VALUE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_NTH.html) | [NTH\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/nth_value)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [NTILE](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_NTILE.html) | [NTILE](https://docs.snowflake.com/en/sql-reference/functions/ntile)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`. (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [PERCENT\_RANK](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_PERCENT_RANK.html) | [PERCENT\_RANK](https://docs.snowflake.com/en/sql-reference/functions/percent_rank)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [PERCENTILE\_CONT](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_PERCENTILE_CONT.html) | [PERCENTILE\_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont)    *Notes: Rounding varies between platforms.* |
| [PERCENTILE\_DISC](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_PERCENTILE_DISC.html) | [PERCENTILE\_DISC](https://docs.snowflake.com/en/sql-reference/functions/percentile_disc) |
| [RANK](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_RANK.html) | [RANK](https://docs.snowflake.com/en/sql-reference/functions/rank) |
| [RATIO\_TO\_REPORT](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_RATIO_TO_REPORT.html) | [RATIO\_TO\_REPORT](https://docs.snowflake.com/en/sql-reference/functions/ratio_to_report)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../../issues-and-troubleshooting/functional-difference/postgresql/ssc-fdm-pg0013.md)*).* |
| [ROW\_NUMBER](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_ROW_NUMBER.html) | [ROW\_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number)    N*otes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [STDDEV\_SAMP | STDDEV | STDDEV\_POP](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_STDDEV.html)  ( [ ALL ] *expression* )  OVER ( [ PARTITION BY *expr\_list* ]  [ ORDER BY *order\_list* *frame\_clause* ] ) | [STDDEV/STDDEV\_SAMP](https://docs.snowflake.com/en/sql-reference/functions/stddev) /[STDDEV\_POP](https://docs.snowflake.com/en/sql-reference/functions/stddev_pop)  ( [ DISTINCT ] expr1) OVER ( [ PARTITION BY expr2 ] [ ORDER BY expr3 [ ASC | DESC ] [ <window\_frame> ] ] )    *Notes: Snowflake supports all the grammar, though ALL is disallowed.* |
| [VAR\_SAMP | VARIANCE | VAR\_POP](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_VARIANCE.html)  ( [ ALL ] *expression* )  OVER ( [ PARTITION BY *expr\_list* ]  [ ORDER BY *order\_list* *frame\_clause* ] ) | [VARIANCE/VAR\_SAMP](https://docs.snowflake.com/en/sql-reference/functions/variance) / [VAR\_POP](https://docs.snowflake.com/en/sql-reference/functions/variance_pop)  ( [ DISTINCT ] expr1) OVER ( [ PARTITION BY expr2 ] [ ORDER BY expr3 [ ASC | DESC ] [ <window\_frame> ] ] )    *Notes: Snowflake supports all the grammar, though ALL is disallowed.* |

Expand

Show lessSee more

## Known Issues

1. For more information, see [Quoted identifiers in functions](redshift-basic-elements#quoted-identifiers-in-functions).

## Related EWIs

- [SSC-EWI-0006](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0006): Date or time format is not supported in Snowflake.
- [SSC-FDM-0032](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0032): Parameter is not a literal value, transformation could not be fully applied
- [SSC-FDM-RS0004](../../issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0004): Invalid dates will cause errors in Snowflake.
- [SSC-FDM-PG0013](../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0013): Function syntactically supported by Snowflake but may have functional differences.

## IDENTITY

### Description

The IDENTITY function is a system function that operates on a specified column of a table to determine the initial value for the identity. If the initial value is not available, it defaults to the value provided in the function. This will be translation to a Sequence in Snowflake.

### Grammar Syntax

Copy code

```
 "identity"(oid_id, oid_table_id, default)
```

Note

This function is no longer supported in Redshift. It uses the default value to define the identity and behaves like a standard identity column.

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE IF NOT EXISTS table_test
(
    id integer,
    inventory_combo BIGINT  DEFAULT "identity"(850178, 0, '5,3'::text)
);

INSERT INTO table_test (id) VALUES
    (1),
    (2),
    (3),
    (4);

SELECT * FROM table_test;
```

##### Results

| id | inventory\_combo |
| --- | --- |
| 1 | 5 |
| 2 | 8 |
| 3 | 11 |
| 3 | 14 |

Expand

Show lessSee more

**Output Code:**

##### Snowflake

Copy code

```
 CREATE TABLE IF NOT EXISTS table_test
(
    id integer,
    inventory_combo BIGINT IDENTITY(5,3) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/13/2024",  "domain": "test" }}';

INSERT INTO table_test (id) VALUES
    (1),
    (2),
    (3),
    (4);

SELECT * FROM
    table_test;
```

##### Results

| id | inventory\_combo |
| --- | --- |
| 1 | 5 |
| 2 | 8 |
| 3 | 11 |
| 3 | 14 |

Expand

Show lessSee more

### Related EWIs

There are no known issues.

## TO\_CHAR

Date function

## Description

> TO\_CHAR converts a timestamp or numeric expression to a character-string data format. ([Redshift SQL Language Reference TO\_CHAR function](https://docs.aws.amazon.com/redshift/latest/dg/r_TO_CHAR.html))

Warning

This function is partially supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/functions/to_char).

For more information, see [Quoted identifiers in functions](./redshift-basic-elements#quoted-identifiers-in-functions).

## Grammar Syntax

Copy code

```
 TO_CHAR(timestamp_expression | numeric_expression , 'format')
```

## Sample Source Patterns

### Input Code:

#### Redshift

Copy code

```
 SELECT TO_CHAR(timestamp '2009-12-31 23:15:59', 'YYYY'),
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'YYY'),
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'TH'),
       "to_char"(timestamp '2009-12-31 23:15:59', 'MON-DY-DD-YYYY HH12:MIPM'),
       TO_CHAR(125.8, '999.99'),
       "to_char"(125.8, '999.99');
```

##### Results

| TO\_CHAR | TO\_CHAR | TO\_CHAR | TO\_CHAR | TO\_CHAR |
| --- | --- | --- | --- | --- |
| 2009 | 009 | DEC-THU-31-2009 11:15PM | 125.80 | 125.80 |

Expand

Show lessSee more

#### Output Code:

##### Snowflake

Copy code

```
 SELECT
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'YYYY'),
       PUBLIC.YEAR_PART_UDF(timestamp '2009-12-31 23:15:59', 3),
       TO_CHAR(timestamp '2009-12-31 23:15:59', 'TH') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - TH FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
       PUBLIC.MONTH_SHORT_UDF(timestamp '2009-12-31 23:15:59', 'uppercase') || '-' || PUBLIC.DAYNAME_SHORT_UDF(timestamp '2009-12-31 23:15:59', 'uppercase') || TO_CHAR(timestamp '2009-12-31 23:15:59', '-DD-YYYY HH12:MI') || PUBLIC.MERIDIAN_INDICATORS_UDF(timestamp '2009-12-31 23:15:59', 'uppercase'),
       TO_CHAR(125.8, '999.99'),
       TO_CHAR(125.8, '999.99');
```

##### Results

| TO\_CHAR | TO\_CHAR |
| --- | --- |
| 2009 | Dec-Thu-31-2009 11:15PM |

Expand

Show lessSee more

## Known Issues

No issues were found.

## Related EWIs

- [SSC-EWI-0006](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0006): The current date/numeric format may have a different behavior in Snowflake.

## For datetime values

Translation specification for the TO\_CHAR function when transforming date or timestamp values to string

### Description

> The following format strings apply to functions such as TO\_CHAR. These strings can contain datetime separators (such as ‘`-`’, ‘`/`’, or ‘`:`’) and the following “dateparts” and “timeparts”. ([Redshift Datetime format strings reference page](https://docs.aws.amazon.com/redshift/latest/dg/r_FORMAT_strings.html))

### Grammar Syntax

Copy code

```
TO_CHAR (timestamp_expression, 'format')
```

The following table specifies the mapping of each format element to Snowflake:

| Redshift | Snowflake |
| --- | --- |
| `BC, AD, bc, ad` (upper and lowercase era indicators) | `PUBLIC.ERA_INDICATORS_UDF` |
| `B.C,. A.D., b.c., a.d.` (upper and lowercase era indicators with points) | `PUBLIC.ERA_INDICATORS_WITH_POINTS_UDF` |
| `CC` | `PUBLIC.CENTURY_UDF` |
| `YYYY` and `YY` | Directly supported |
| `YYY` and `Y` | `PUBLIC.YEAR_PART_UDF` |
| `Y,YYY` | `PUBLIC.YEAR_WITH_COMMA_UDF` |
| `IYYY` | `YEAROFWEEKISO` |
| `I, IY, IYY` | `PUBLIC.ISO_YEAR_PART_UDF` |
| `Q` | `QUARTER` |
| `MONTH, Month, month` | `PUBLIC.FULL_MONTH_NAME_UDF` |
| `MON, Mon, mon` | `PUBLIC.MONTH_SHORT_UDF` |
| `RM, rm` | `PUBLIC.ROMAN_NUMERALS_MONTH_UDF` |
| `W` | `PUBLIC.WEEK_OF_MONTH_UDF` |
| `WW` | `PUBLIC.WEEK_NUMBER_UDF` |
| `IW` | `WEEKISO` |
| `DAY, Day, day` | `PUBLIC.DAYNAME_LONG_UDF` |
| `DY, Dy, dy` | `PUBLIC.DAYNAME_SHORT_UDF` |
| `DDD` | `DAYOFYEAR` |
| `IDDD` | `PUBLIC.DAY_OF_YEAR_ISO_UDF` |
| `D` | `PUBLIC.DAY_OF_WEEK_UDF`    *Notes: For this UDF to work correctly the Snowflake session parameter `WEEK_START` should have its default value (`0`).* |
| `ID` | `DAYOFWEEKISO` |
| `J` | `PUBLIC.JULIAN_DAY_UDF` |
| `HH24` | Directly supported |
| `HH` | `HH12` |
| `HH12` | Directly supported |
| `MI` | Directly supported |
| `SS` | Directly supported |
| `MS` | `FF3` |
| `US` | `FF6` |
| `AM, PM, am, pm` (upper and lowercase meridian indicators) | `PUBLIC.MERIDIAN_INDICATORS_UDF` |
| `A.M., P.M., a.m., p.m.` (upper and lowercase meridian indicators with points) | `PUBLIC.MERIDIAN_INDICATORS_WITH_POINTS_UDF` |
| `TZ` and `tz` | `UTC` and `utc`    *Notes: According to the* [*redshift documentation*](https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html#r_Datetime_types-timestamptz)*, all timestamp with time zone are stored in UTC, which causes this format element to return a fixed result.* |
| `OF` | +00    *Notes: According to the* [*redshift documentation*](https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html#r_Datetime_types-timestamptz)*, all timestamp with time zone are stored in UTC, which causes this format element to return a fixed result.* |
| `SSSS` | `PUBLIC.SECONDS_PAST_MIDNIGHT` |
| `SP` | *Notes: This is a PostgreSQL template pattern modifier for “spell mode”, however it does nothing on Redshift, so it is removed from the output.* |
| `FX` | *Notes: This is another template pattern modifier for “fixed format”, however it has no use on the TO\_CHAR function so it is removed.* |

Expand

Show lessSee more

### Sample Source Patterns

#### Direct format elements transformation (no functions/UDFs)

The result is preserved as a single TO\_CHAR function

##### *Redshift*

##### Query

Copy code

```
 SELECT TO_CHAR('2013-10-03 13:50:15.456871'::TIMESTAMP, 'DD/MM/YY HH:MI:SS.MS') AS col1;
```

##### Result

Copy code

```
+----------------------+
|col1                  |
+----------------------+
|03/10/13 01:50:15.456 |
+----------------------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT TO_CHAR('2013-10-03 13:50:15.456871'::TIMESTAMP, 'DD/MM/YY HH12:MI:SS.FF3') AS col1;
```

##### Result

Copy code

```
+----------------------+
|col1                  |
+----------------------+
|03/10/13 01:50:15.456 |
+----------------------+
```

#### Format transformation using functions/UDFs

The result is a concatenation of multiple TO\_CHAR, UDFs and Snowflake built-in functions that generate the equivalent string representation of the datetime value

##### *Redshift*

##### Query

Copy code

```
 SELECT TO_CHAR(DATE '2025-07-05', '"Today is " Month DAY DD, "it belongs to the week " IW') AS result;
```

##### Result

Copy code

```
+-------------------------------------------------------------+
|result                                                       |
+-------------------------------------------------------------+
|Today is  July      SATURDAY  05, it belongs to the week  27 |
+-------------------------------------------------------------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
    'Today is ' ||
    TO_CHAR(DATE '2025-07-05', ' ') ||
    PUBLIC.FULL_MONTH_NAME_UDF(DATE '2025-07-05', 'firstOnly') ||
    ' ' ||
    PUBLIC.DAYNAME_LONG_UDF(DATE '2025-07-05', 'uppercase') ||
    TO_CHAR(DATE '2025-07-05', ' DD, ') ||
    'it belongs to the week ' ||
    TO_CHAR(DATE '2025-07-05', ' ') ||
    WEEKISO(DATE '2025-07-05') AS result;
```

##### Result

Copy code

```
+-------------------------------------------------------------+
|result                                                       |
+-------------------------------------------------------------+
|Today is  July      SATURDAY  05, it belongs to the week  27 |
+-------------------------------------------------------------+
```

#### Quoted text

Format elements in double quoted text are added to the output directly without interpreting them, escaped double quotes are transformed to their Snowflake escaped equivalent.

##### *Redshift*

##### Query

Copy code

```
 SELECT
    TO_CHAR(DATE '2025-01-16', 'MM "TESTING DD" DD') AS result1,
    TO_CHAR(DATE '2025-01-16', 'MM TESTING \\"DD\\" DD') AS result2,
    TO_CHAR(DATE '2025-01-16', 'MM "TESTING \\"DD\\"" DD') AS result3;
```

##### Result

Copy code

```
+-----------------+-------------------+-------------------+
|result1          |result2            |result3            |
+-----------------+-------------------+-------------------+
|01 TESTING DD 16 |01 TEST5NG "16" 16 |01 TESTING "DD" 16 |
+-----------------+-------------------+-------------------+
```

##### *Snowflake*

##### Query

Copy code

```
 SELECT
    TO_CHAR(DATE '2025-01-16', 'MM ') || 'TESTING DD' || TO_CHAR(DATE '2025-01-16', ' DD') AS result1,
    TO_CHAR(DATE '2025-01-16', 'MM TEST') || PUBLIC.ISO_YEAR_PART_UDF(DATE '2025-01-16', 1) || TO_CHAR(DATE '2025-01-16', 'NG ""DD"" DD') AS result2,
    TO_CHAR(DATE '2025-01-16', 'MM ') || 'TESTING "DD"' || TO_CHAR(DATE '2025-01-16', ' DD') AS result3;
```

##### Result

Copy code

```
+-----------------+-------------------+-------------------+
|result1          |result2            |result3            |
+-----------------+-------------------+-------------------+
|01 TESTING DD 16 |01 TEST5NG "16" 16 |01 TESTING "DD" 16 |
+-----------------+-------------------+-------------------+
```

### Known Issues

#### Template pattern modifiers not supported

The following format template modifiers:

- FM (fill mode)
- TH and th (uppercase and lowercase ordinal number suffix)
- TM (translation mode)

Are not supported, including them in a format will generate [SSC-EWI-0006](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0006)

Input code:

Copy code

```
 SELECT TO_CHAR(CURRENT_DATE, 'FMMonth'),
TO_CHAR(CURRENT_DATE, 'DDTH'),
TO_CHAR(CURRENT_DATE, 'DDth'),
TO_CHAR(CURRENT_DATE, 'TMMonth');
```

Output code:

Copy code

```
 SELECT
TO_CHAR(CURRENT_DATE(), 'FM') || PUBLIC.FULL_MONTH_NAME_UDF(CURRENT_DATE(), 'firstOnly') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - FMMonth FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
TO_CHAR(CURRENT_DATE(), 'DDTH') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - DDTH FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
TO_CHAR(CURRENT_DATE(), 'DDth') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - DDth FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!,
TO_CHAR(CURRENT_DATE(), 'TM') || PUBLIC.FULL_MONTH_NAME_UDF(CURRENT_DATE(), 'firstOnly') !!!RESOLVE EWI!!! /*** SSC-EWI-0006 - TMMonth FORMAT MAY FAIL OR MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/!!!;
```

**Format parameter passed through variable**

When the format parameter is passed as a variable instead of a string literal, the transformation of format elements can not be applied, an FDM will be added to the uses of the function warning about it.

Input code:

Copy code

```
 SELECT TO_CHAR(d, 'YYYY/MM/DD'),
TO_CHAR(d, f)
FROM (SELECT TO_DATE('2001-01-01','YYYY-MM-DD') as d, 'DD/MM/YYYY' as f);
```

Output code:

Copy code

```
 SELECT TO_CHAR(d, 'YYYY/MM/DD'),
--** SSC-FDM-0032 - PARAMETER 'format_string' IS NOT A LITERAL VALUE, TRANSFORMATION COULD NOT BE FULLY APPLIED **
TO_CHAR(d, f)
FROM (SELECT TO_DATE('2001-01-01','YYYY-MM-DD') as d, 'DD/MM/YYYY' as f);
```

### Related EWIs

1. [SSC-EWI-0006](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0006): The current date/numeric format may have a different behavior in Snowflake.
2. [SSC-FDM-0032](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0032): Parameter is not a literal value, transformation could not be fully applied
