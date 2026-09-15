# PostgreSQL - Built-in functions

## Applies to

- PostgreSQL
- Greenplum
- Netezza

Note

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../general/built-in-functions).

## Aggregate Functions

> Aggregate functions compute a single result value from a set of input values. ([PostgreSQL Language Reference Aggregate Functions](https://www.postgresql.org/docs/12/functions-aggregate.html)).

| PostgreSQL | Snowflake |
| --- | --- |
| [AVG](https://www.postgresql.org/docs/12/functions-aggregate.html) | [AVG](https://docs.snowflake.com/en/sql-reference/functions/avg)    *Notes:* PostgreSQL *and Snowflake may show different precision/decimals due to data type rounding/formatting.* |
| [COUNT](https://www.postgresql.org/docs/12/functions-aggregate.html) | [COUNT](https://docs.snowflake.com/en/sql-reference/functions/count) |
| [MAX](https://www.postgresql.org/docs/12/functions-aggregate.html) | [MAX](https://docs.snowflake.com/en/sql-reference/functions/max) |
| [MEDIAN](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-greenplum/7/greenplum-database/ref_guide-function-summary.html#topic31) | [MEDIAN](https://docs.snowflake.com/en/sql-reference/functions/median)    *Notes**: Snowflake does not allow the use of date types**, while* PostgreSQL *does. (See* [SSC-FDM-PG0013](../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0013)*).* |
| [MIN](https://www.postgresql.org/docs/12/functions-aggregate.html) | [MIN](https://docs.snowflake.com/en/sql-reference/functions/min) |
| [PERCENTILE\_CONT](https://www.postgresql.org/docs/9.4/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE) | [PERCENTILE\_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont) |
| [STDDEV/STDDEV\_SAMP](https://www.postgresql.org/docs/12/functions-aggregate.html) (*expression*) | [STDDEV/STDDEV\_SAMP](https://docs.snowflake.com/en/sql-reference/functions/stddev) (*expression*) |
| [STDDEV\_POP](https://www.postgresql.org/docs/12/functions-aggregate.html) (*expression*) | [STDDEV\_POP](https://docs.snowflake.com/en/sql-reference/functions/stddev_pop) (*expression*) |
| [SUM](https://www.postgresql.org/docs/12/functions-aggregate.html) | [SUM](https://docs.snowflake.com/en/sql-reference/functions/sum) |
| [VARIANCE/VAR\_SAMP](https://www.postgresql.org/docs/12/functions-aggregate.html) (*expression*) | [VARIANCE/VAR\_SAMP](https://docs.snowflake.com/en/sql-reference/functions/variance)  (*expression*) |
| [VAR\_POP](https://www.postgresql.org/docs/12/functions-aggregate.html) (*expression*) | [VAR\_POP](https://docs.snowflake.com/en/sql-reference/functions/variance_pop) (*expression*) |

Expand

Show lessSee more

## Conditional expressions

| PostgreSQL | Snowflake |
| --- | --- |
| [COALESCE](https://www.postgresql.org/docs/12/functions-conditional.html) ( value *[, …]* ) | [COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce) ( *expression*, *expression*, … ) |
| [GREATEST](https://www.postgresql.org/docs/12/functions-conditional.html) ( value [, …] ) | [GREATEST\_IGNORE\_NULLS](https://docs.snowflake.com/en/sql-reference/functions/greatest_ignore_nulls) ( <expr1> [, <expr2> … ] ) |
| [LEAST](https://www.postgresql.org/docs/12/functions-conditional.html) ( value [, …] ) | [LEAST\_IGNORE\_NULLS](https://docs.snowflake.com/en/sql-reference/functions/least_ignore_nulls) ( &lt;expr1> [, &lt;expr2> … ]) |
| [NULLIF](https://www.postgresql.org/docs/12/functions-conditional.html) | [NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif)   *Notes: PostgreSQL’s NULLIF ignores trailing spaces in some string comparisons, unlike Snowflake. Therefore, the transformation adds RTRIM for equivalence.* |

Expand

Show lessSee more

## Data type formatting functions

> Data type formatting functions provide an easy way to convert values from one data type to another. For each of these functions, the first argument is always the value to be formatted and the second argument contains the template for the new format. ([PostgreSQL Language Reference Data type formatting functions](https://www.postgresql.org/docs/12/functions-formatting.html)).

| PostgreSQL | Snowflake |
| --- | --- |
| [TO\_CHAR](https://www.postgresql.org/docs/12/functions-formatting.html) | [TO\_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char)    *Notes: Snowflake’s support for this function is partial (see* [*SSC-EWI-PG0005*](broken-reference)*).* |
| [TO\_DATE](https://www.postgresql.org/docs/12/functions-formatting.html) | [TO\_DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date)    *Notes: Snowflake’s `TO_DATE` fails on invalid dates like ’20010631’ (June has 30 days), unlike* PostgreSQL’*s lenient `TO_DATE`. Use `TRY_TO_DATE` in Snowflake to handle these cases by returning NULL. (see* [*SSC-EWI-PG0005*](broken-reference)*,* [*SSC-FDM-0032*](../../issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0032)*).* |

Expand

Show lessSee more

## Date and time functions

| PostgreSQL | Snowflake |
| --- | --- |
| [AT TIME ZONE ‘timezone’](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT) | [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <source\_tz> , <target\_tz> , <source\_timestamp\_ntz> )    [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) ( <target\_tz> , <source\_timestamp> )    *Notes:* PostgreSQL *defaults to UTC; the Snowflake function requires explicit UTC specification. Therefore, it will be added as the target timezone.* |
| [CURRENT\_DATE](https://www.postgresql.org/docs/8.2/functions-datetime.html) | [CURRENT\_DATE()](https://docs.snowflake.com/en/sql-reference/functions/current_date) |
| [DATE\_PART/PGDATE\_PART](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT) | [DATE\_PART](https://docs.snowflake.com/en/sql-reference/functions/date_part)    *Notes: this function is partially supported by Snowflake. (See* [*SSC-EWI-PG0005*](broken-reference)*).* |
| [DATE\_TRUNC](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT) | [DATE\_TRUNC](https://docs.snowflake.com/en/sql-reference/functions/date_trunc)    *Notes: Invalid date part formats are translated to Snowflake-compatible formats.* |
| [TO\_TIMESTAMP](https://www.postgresql.org/docs/12/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT) | [TO\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp) |
| [EXTRACT](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT) | [EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/extract)  *Notes:* Part-time or Date time supported: DAY, DOW, DOY, EPOCH, HOUR, MINUTE, MONTH, QUARTER, SECOND, WEEK, YEAR. |
| [TIMEZONE](https://www.postgresql.org/docs/16/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT) | [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone) |

Expand

Show lessSee more

Note

PostgreSQL timestamps default to microsecond precision (6 digits); Snowflake defaults to nanosecond precision (9 digits). Adjust precision as needed using ALTER SESSION (for example, `ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF2';`). Precision loss may occur depending on the data type used.  
  
Since some formats are incompatible with Snowflake, adjusting the account parameters [DATE\_INPUT\_FORMAT or TIME\_INPUT\_FORMAT](https://docs.snowflake.com/en/sql-reference/date-time-input-output#data-loading) might maintain functional equivalence between platforms.

## JSON Functions

| PostgreSQL | Snowflake |
| --- | --- |
| [JSON\_EXTRACT\_PATH\_TEXT](https://www.postgresql.org/docs/9.3/functions-json.html) | [JSON\_EXTRACT\_PATH\_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text)    *Notes:*   1. PostgreSQL *treats newline, tab, and carriage return characters literally; Snowflake interprets them.* 2. *A JSON literal and dot-separated path are required to access nested objects in the Snowflake function.* 3. *Paths with spaces in variables must be quoted.* |

Expand

Show lessSee more

## Math functions

| PostgreSQL | Snowflake |
| --- | --- |
| [ACOS](https://www.postgresql.org/docs/12/functions-math.html) | [ACOS](https://docs.snowflake.com/en/sql-reference/functions/acos) |
| [ASIN](https://www.postgresql.org/docs/12/functions-math.html) | [ASIN](https://docs.snowflake.com/en/sql-reference/functions/asin) |
| [ATAN](https://www.postgresql.org/docs/12/functions-math.html) | [ATAN](https://docs.snowflake.com/en/sql-reference/functions/atan) |
| [ATAN2](https://www.postgresql.org/docs/12/functions-math.html) | [ATAN2](https://docs.snowflake.com/en/sql-reference/functions/atan2) |
| [CBRT](https://www.postgresql.org/docs/12/functions-math.html) | [CBRT](https://docs.snowflake.com/en/sql-reference/functions/cbrt) |
| [CEIL/CEILING](https://www.postgresql.org/docs/12/functions-math.html) | [CEIL](https://docs.snowflake.com/en/sql-reference/functions/ceil) |
| [COS](https://www.postgresql.org/docs/12/functions-math.html) | [COS](https://docs.snowflake.com/en/sql-reference/functions/cos) |
| [COT](https://www.postgresql.org/docs/12/functions-math.html) | [COT](https://docs.snowflake.com/en/sql-reference/functions/cot) |
| [DEGREES](https://www.postgresql.org/docs/12/functions-math.html) | [DEGREES](https://docs.snowflake.com/en/sql-reference/functions/degrees) |
| [LN](https://www.postgresql.org/docs/12/functions-math.html) | [LN](https://docs.snowflake.com/en/sql-reference/functions/ln) |
| [EXP](https://www.postgresql.org/docs/12/functions-math.html) | [EXP](https://docs.snowflake.com/en/sql-reference/functions/exp) |
| [FLOOR](https://www.postgresql.org/docs/12/functions-math.html) | [FLOOR](https://docs.snowflake.com/en/sql-reference/functions/floor) |
| [LOG](https://www.postgresql.org/docs/12/functions-math.html) | [LOG](https://docs.snowflake.com/en/sql-reference/functions/log) |
| [MOD](https://www.postgresql.org/docs/12/functions-math.html) | [MOD](https://docs.snowflake.com/en/sql-reference/functions/mod) |
| [PI](https://www.postgresql.org/docs/12/functions-math.html) | [PI](https://docs.snowflake.com/en/sql-reference/functions/pi) |
| [POWER/POW](https://www.postgresql.org/docs/12/functions-math.html) | [POWER/POW](https://docs.snowflake.com/en/sql-reference/functions/pow) |
| [RADIANS](https://www.postgresql.org/docs/12/functions-math.html) | [RADIANS](https://docs.snowflake.com/en/sql-reference/functions/radians) |
| [RANDOM](https://www.postgresql.org/docs/12/functions-math.html) | [RANDOM](https://docs.snowflake.com/en/sql-reference/functions/random) |
| [ROUND](https://www.postgresql.org/docs/12/functions-math.html) | [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round) |
| [SIN](https://www.postgresql.org/docs/12/functions-math.html) | [SIN](https://docs.snowflake.com/en/sql-reference/functions/sin) |
| [SIGN](https://www.postgresql.org/docs/12/functions-math.html) | [SIGN](https://docs.snowflake.com/en/sql-reference/functions/sign) |
| [SQRT](https://www.postgresql.org/docs/12/functions-math.html) | [SQRT](https://docs.snowflake.com/en/sql-reference/functions/sqrt) |
| [TAN](https://www.postgresql.org/docs/12/functions-math.html) | [TAN](https://docs.snowflake.com/en/sql-reference/functions/tan) |
| [TRUNC](https://www.postgresql.org/docs/12/functions-math.html) | [TRUNC](https://docs.snowflake.com/en/sql-reference/functions/trunc) |

Expand

Show lessSee more

Note

PostgreSQL and Snowflake results may differ in scale.

## String functions

> String functions process and manipulate character strings or expressions that evaluate to character strings. ([PostgreSQL Language Reference String functions](https://www.postgresql.org/docs/12/functions-string.html)).

| PostgreSQL | Snowflake |
| --- | --- |
| [ASCII](https://www.postgresql.org/docs/12/functions-string.html) | [ASCII](https://docs.snowflake.com/en/sql-reference/functions/ascii) |
| [BTRIM](https://www.postgresql.org/docs/12/functions-string.html) | [TRIM](https://docs.snowflake.com/en/sql-reference/functions/trim) |
| [“char”](https://www.postgresql.org/docs/12/datatype-character.html) (internal type) | [LEFT](https://docs.snowflake.com/en/sql-reference/functions/left)(*expr*, 1). Both the function call form `"char"(expr)` and the explicit cast form `expr::"char"` are converted. |
| [CHAR\_LENGTH](https://www.postgresql.org/docs/12/functions-string.html) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [CHARACTER\_LENGTH](https://www.postgresql.org/docs/12/functions-string.html) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [CHR](https://www.postgresql.org/docs/9.1/functions-string.html) | [CHR](https://docs.snowflake.com/en/sql-reference/functions/chr) |
| [CONCAT](https://www.postgresql.org/docs/12/functions-string.html) | [CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) |
| [INITCAP](https://www.postgresql.org/docs/12/functions-string.html) | [INITCAP](https://docs.snowflake.com/en/sql-reference/functions/initcap) |
| [LEFT/RIGHT](https://www.postgresql.org/docs/12/functions-string.html) | [LEFT](https://docs.snowflake.com/en/sql-reference/functions/left)/[RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right) |
| [LOWER](https://www.postgresql.org/docs/12/functions-string.html) | [LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower) |
| [MD5](https://www.postgresql.org/docs/12/functions-string.html) | [MD5](https://docs.snowflake.com/en/sql-reference/functions/md5) |
| [OCTET\_LENGTH](https://www.postgresql.org/docs/12/functions-string.html) | [OCTET\_LENGTH](https://docs.snowflake.com/en/sql-reference/functions/octet_length)    *Notes:* *the results may vary between platforms (See* [SSC-FDM-PG0013](../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0013)*).* |
| [QUOTE\_IDENT](https://www.postgresql.org/docs/12/functions-string.html) (*string*) | [CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) (‘”’, *string,* ‘”’) |
| [REGEXP\_REPLACE](https://www.postgresql.org/docs/12/functions-string.html) | [REGEXP\_REPLACE](https://docs.snowflake.com/en/sql-reference/functions/regexp_replace)    *Notes: This function includes a `parameters` argument that enables the user to interpret the pattern using the Perl Compatible Regular Expression (PCRE) dialect, represented by the `p` value, this is removed to avoid any issues*. *(See* [*SSC-EWI-0009*](../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0009)*,* [*SC-FDM-0032*](../../issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0032)*,* [*SSC-FDM-PG0011*](../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0011)*).* |
| [REPEAT](https://www.postgresql.org/docs/12/functions-string.html) | [REPEAT](https://docs.snowflake.com/en/sql-reference/functions/repeat) |
| [REPLACE](https://www.postgresql.org/docs/12/functions-string.html) | [REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace) |
| [REVERSE](https://www.postgresql.org/docs/12/functions-string.html) | [REVERSE](https://docs.snowflake.com/en/sql-reference/functions/reverse) |
| [SPLIT\_PART](https://www.postgresql.org/docs/12/functions-string.html) | [SPLIT\_PART](https://docs.snowflake.com/en/sql-reference/functions/split_part)    *Notes: Snowflake and* PostgreSQL *handle SPLIT\_PART differently with case-insensitive collations.* |
| [STRPOS](https://www.postgresql.org/docs/12/functions-string.html) (*string*, *substring* ) | [POSITION](https://docs.snowflake.com/en/sql-reference/functions/position) ( &lt;expr1> IN &lt;expr> ) |
| [SUBSTRING](https://www.postgresql.org/docs/12/functions-string.html) | [*SUBSTRING*](https://docs.snowflake.com/en/sql-reference/functions/substr)    *Notes:* Snowflake partially supports this function. PostgreSQL’s `SUBSTRING`, with a non-positive `start_position`, calculates `start_position + number_characters` (returning ‘’ if the result is non-positive). Snowflake’s behavior differs. |
| [TRANSLATE](https://www.postgresql.org/docs/12/functions-string.html) | [TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/translate) |
| [TRIM](https://www.postgresql.org/docs/12/functions-string.html) | [*TRIM*](https://docs.snowflake.com/en/sql-reference/functions/trim)    *Notes:* PostgreSQL *uses keywords (BOTH, LEADING, TRAILING) for trim; Snowflake uses TRIM, LTRIM, RTRIM.* |
| [UPPER](https://www.postgresql.org/docs/12/functions-string.html) | [UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper) |

Expand

Show lessSee more

## Sequence functions

> Sequence manipulation functions provide methods to access and use sequence generators. ([PostgreSQL Language Reference Sequence functions](https://www.postgresql.org/docs/12/functions-sequence.html)).

| PostgreSQL | Snowflake |
| --- | --- |
| [NEXTVAL](https://www.postgresql.org/docs/12/functions-sequence.html) (‘*sequence\_name*’) | *sequence\_name*.NEXTVAL    *Notes: Both* `nextval('seq')` *and* `nextval('seq'::regclass)` *forms are supported. (See* [SSC-FDM-PG0009](../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0009)*).* |

Expand

Show lessSee more

## Window functions

| PostgreSQL | Snowflake |
| --- | --- |
| [AVG](https://www.postgresql.org/docs/9.4/functions-aggregate.html) | [*AVG*](https://docs.snowflake.com/en/sql-reference/functions/avg)    *Notes: AVG rounding/formatting can vary by data type between* PostgreSQL *and Snowflake.* |
| [COUNT](https://www.postgresql.org/docs/9.4/functions-aggregate.html) | [COUNT](https://docs.snowflake.com/en/sql-reference/functions/count) |
| [DENSE\_RANK](https://www.postgresql.org/docs/current/functions-window.html) | [DENSE\_RANK](https://docs.snowflake.com/en/sql-reference/functions/dense_rank)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [FIRST\_VALUE](https://www.postgresql.org/docs/current/functions-window.html) | [FIRST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value)    *Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY <expr>.`* |
| [LAG](https://www.postgresql.org/docs/current/functions-window.html) | [LAG](https://docs.snowflake.com/en/sql-reference/functions/lag) |
| [LAST\_VALUE](https://www.postgresql.org/docs/current/functions-window.html) | [LAST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value)    *Notes: Snowflake needs ORDER BY; missing clauses get `ORDER BY <expr>`.* |
| [LEAD](https://www.postgresql.org/docs/current/functions-window.html) | [LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead)    *Notes:* PostgreSQL *allows constant or expression offsets; Snowflake allows only constant offset*s. |
| [NTH\_VALUE](https://www.postgresql.org/docs/current/functions-window.html) | [NTH\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/nth_value)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [NTILE](https://www.postgresql.org/docs/current/functions-window.html) | [NTILE](https://docs.snowflake.com/en/sql-reference/functions/ntile)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`. (See* [SSC-FDM-PG0013](../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0013)*).* |
| [PERCENT\_RANK](https://www.postgresql.org/docs/current/functions-window.html) | [PERCENT\_RANK](https://docs.snowflake.com/en/sql-reference/functions/percent_rank)    *Notes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |
| [PERCENTILE\_CONT](https://www.postgresql.org/docs/9.4/functions-aggregate.html) | [PERCENTILE\_CONT](https://docs.snowflake.com/en/sql-reference/functions/percentile_cont)    *Notes: Rounding varies between platforms.* |
| [PERCENTILE\_DISC](https://www.postgresql.org/docs/9.4/functions-aggregate.html) | [PERCENTILE\_DISC](https://docs.snowflake.com/en/sql-reference/functions/percentile_disc) |
| [RANK](https://www.postgresql.org/docs/current/functions-window.html) | [RANK](https://docs.snowflake.com/en/sql-reference/functions/rank) |
| [ROW\_NUMBER](https://www.postgresql.org/docs/current/functions-window.html) | [ROW\_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number)    N*otes: ORDER BY is mandatory in Snowflake; missing clauses are replaced with `ORDER BY 1`.* |

Expand

Show lessSee more

## Related EWIs

- [SSC-FDM-0032](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0032): Parameter is not a literal value, transformation could not be fully applied
- [SSC-FDM-PG0013](../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0013): Function syntactically supported by Snowflake but may have functional differences.
- [SSC-EWI-0009](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0009): Regexp\_Substr Function only supports POSIX regular expressions.
- [SSC-FDM-PG0011](../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0011): The use of the COLLATE column constraint has been disabled for this pattern-matching condition.
