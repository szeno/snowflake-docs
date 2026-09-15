# BigQuery - Built-in functions

Translation reference for all the supported built-in functions for BigQuery.

Note

For more information about built-in functions and their Snowflake equivalents, also see [Common built-in functions](../../translation-references/general/built-in-functions).

## Aggregate Functions

| BigQuery | Snowflake |
| --- | --- |
| [ANY\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value) | [ANY\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/any_value)  *Note: Unlike BigQuery, Snowflake does not ignore NULLs . Additionally, Snowflake’s `OVER()` clause does not support the use of `ORDER BY` or explicit window frames.* |
| [ANY\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)( expr1, HAVING MAX expr2)  [ANY\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#any_value)( expr1, HAVING MIN expr2) | [MAX\_BY](https://docs.snowflake.com/en/sql-reference/functions/max_by)(expr1, expr1)  [MIN\_BY](https://docs.snowflake.com/en/sql-reference/functions/min_by)(expr1, expr2) |
| [AVG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#avg) | [AVG](https://docs.snowflake.com/en/sql-reference/functions/avg) |
| [COUNT](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#count) | [COUNT](https://docs.snowflake.com/en/sql-reference/functions/count) |
| [COUNTIF](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#countif) | [COUNT\_IF](https://docs.snowflake.com/en/sql-reference/functions/count_if) |
| [LOGICAL\_AND](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#logical_and) | [BOOLAND\_AGG](https://docs.snowflake.com/en/sql-reference/functions/booland_agg) |
| [LOGICAL\_OR](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#logical_or) | [BOOLOR\_AGG](https://docs.snowflake.com/en/sql-reference/functions/boolor_agg) |
| [MAX](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#max) | [MAX](https://docs.snowflake.com/en/sql-reference/functions/max) |
| [MIN](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#min) | [MIN](https://docs.snowflake.com/en/sql-reference/functions/min) |
| [SUM](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#sum) | [SUM](https://docs.snowflake.com/en/sql-reference/functions/sum) |

Expand

Show lessSee more

## Array Functions

| BigQuery | Snowflake |
| --- | --- |
| [ARRAY\_AGG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg) | [ARRAY\_AGG](https://docs.snowflake.com/en/sql-reference/functions/array_agg) |
| [ARRAY\_CONCAT](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_concat) | [ARRAY\_CAT](https://docs.snowflake.com/en/sql-reference/functions/array_cat) |
| [ARRAY\_CONCAT\_AGG](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_concat_agg) | [ARRAY\_FLATTEN](https://docs.snowflake.com/en/sql-reference/functions/array_flatten) |
| [ARRAY\_TO\_STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_to_string)(expr, delimiter) | [ARRAY\_TO\_STRING](https://docs.snowflake.com/en/sql-reference/functions/array_to_string)(ARRAY\_COMPACT(expr), delimiter) |
| [ARRAY\_TO\_STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions#array_to_string)(expr, delimiter, null\_text) | ARRAY\_TO\_STRING\_UDF(expr, delimiter, null\_text)  *Notes: A UDF is generated to handle the NULL replacement parameter which is not natively supported in Snowflake’s ARRAY\_TO\_STRING function.* |
| [SELECT ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#array_subquery) (SELECT query) | SELECT (SELECT ARRAY\_AGG(\*) FROM (SELECT query))  *Notes: BigQuery’s ARRAY subquery syntax is transformed to use ARRAY\_AGG with a subquery in Snowflake.* |

Expand

Show lessSee more

## Conditional Expressions

| BigQuery | Snowflake |
| --- | --- |
| [COALESCE](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#coalesce) | [COALESCE](https://docs.snowflake.com/en/sql-reference/functions/coalesce) |
| [IF](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#if) | [IFF](https://docs.snowflake.com/en/sql-reference/functions/iff) |
| [IFNULL](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#ifnull) | [IFNULL](https://docs.snowflake.com/en/sql-reference/functions/ifnull) |
| [NULLIF](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions#nullif) | [NULLIF](https://docs.snowflake.com/en/sql-reference/functions/nullif) |

## Conversion Functions

| BigQuery | Snowflake |
| --- | --- |
| [SAFE\_CAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions#safe_casting) | [TRY\_CAST](https://docs.snowflake.com/en/sql-reference/functions/try_cast) |
| [SAFE.](https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#safe_prefix) prefix on cast-style functions (e.g. `SAFE.PARSE_DATE`, `SAFE.PARSE_TIMESTAMP`, `SAFE.CAST`) | Equivalent `TRY_*` function (`TRY_TO_DATE`, `TRY_TO_TIMESTAMP_TZ`, `TRY_CAST`, etc.)  *Notes: The SAFE-prefixed call is rewritten to the corresponding `TRY_*` Snowflake function so failures return NULL instead of raising an error.* |

Expand

Show lessSee more

## Date Functions

| BigQuery | Snowflake |
| --- | --- |
| [CURRENT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#current_date) [CURRENT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#current_date)() | [CURRENT\_DATE](https://docs.snowflake.com/en/sql-reference/functions/current_date)  [CURRENT\_DATE](https://docs.snowflake.com/en/sql-reference/functions/current_date)() |
| [DATE\_ADD](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#date_add)(date, INTERVAL n part) | [DATEADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd)(‘part’, n, date)  *Notes: The arguments are re-ordered and the BigQuery `INTERVAL n part` literal is converted into Snowflake’s `(part_string, n, date)` argument layout. Negative literals are preserved.* |
| [DATE\_SUB](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#date_sub)(date, INTERVAL n part) | [DATEADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd)(‘part’, -n, date)  *Notes: Snowflake has no `DATE_SUB`; the call is rewritten to `DATEADD` with the integer expression negated. Literal negative intervals collapse, non-literals are wrapped with a unary minus.* |
| [DATE\_DIFF](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#date_diff)(date\_a, date\_b, part) | [DATEDIFF](https://docs.snowflake.com/en/sql-reference/functions/datediff)(‘part’, date\_b, date\_a)  *Notes: BigQuery’s `DATE_DIFF(a, b, part)` computes `a - b`; Snowflake’s `DATEDIFF('part', b, a)` reverses the operand order. The arguments are swapped so the result sign matches BigQuery. `ISOWEEK`, `ISOYEAR` and `WEEK(<weekday>)` are translated to the corresponding Snowflake date parts.* |
| [DATE\_TRUNC](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#date_trunc)(date, part) | [DATE\_TRUNC](https://docs.snowflake.com/en/sql-reference/functions/date_trunc)(‘part’, date)  *Notes: BigQuery uses `(date, part)` argument order; Snowflake uses `('part', date)`. The arguments are swapped and the part is quoted as a string literal.* |
| [EXTRACT](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#extract)(DAYOFWEEK FROM date) | [DAYOFWEEK](https://docs.snowflake.com/en/sql-reference/functions/dayofweek)(date) + 1  *Notes: BigQuery’s DAYOFWEEK returns 1..7 with Sunday = 1; Snowflake’s returns 0..6 with Sunday = 0. `+ 1` is added to keep the result aligned. See* [*SSC-FDM-BQ0008*](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0008) *when the argument is influenced by the `WEEK_START` session parameter.* |
| [EXTRACT](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#extract)(ISOWEEK FROM date) | [EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/extract)(WEEKISO FROM date)  *Notes: BigQuery’s `ISOWEEK` date part is renamed to Snowflake’s `WEEKISO`.* |
| [FORMAT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#format_date) | [TO\_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char)  *Note: For further details on this translation, please consult this* [*page*](format_date.md)*.* |
| [PARSE\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#parse_date)(format\_string, date\_string) | [TO\_DATE](https://docs.snowflake.com/en/sql-reference/functions/to_date)(date\_string, translated\_format)  *Notes: BigQuery format codes (`%Y`, `%m`, `%d`, etc.) are translated at compile time to Snowflake equivalents (`YYYY`, `MM`, `DD`, etc.). Non-literal format strings are passed through unchanged with a warning.* |

Expand

Show lessSee more

## Datetime Functions

| BigQuery | Snowflake |
| --- | --- |
| [CURRENT\_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime)  [CURRENT\_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime)() | [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp) :: TIMESTAMP\_NTZ [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)() :: TIMESTAMP\_NTZ |
| [DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#datetime)(year, month, day, hour, minute, second) | [TIMESTAMP\_NTZ\_FROM\_PARTS](https://docs.snowflake.com/en/sql-reference/functions/timestamp_ntz_from_parts)(year, month, day, hour, minute, second)  *Notes: BigQuery’s `DATETIME` constructor maps to Snowflake’s `TIMESTAMP_NTZ_FROM_PARTS`. The single-argument form `DATETIME(timestamp)` and the `DATETIME(date, time)` form are also supported.* |
| [PARSE\_DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#parse_datetime)(format\_string, datetime\_string) | [TO\_TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp)(datetime\_string, translated\_format)  *Notes: BigQuery format codes are translated at compile time to Snowflake equivalents. Non-literal format strings are passed through unchanged with a warning.* |

Expand

Show lessSee more

## Time Functions

| BigQuery | Snowflake |
| --- | --- |
| [PARSE\_TIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#parse_time)(format\_string, time\_string) | [TO\_TIME](https://docs.snowflake.com/en/sql-reference/functions/to_time)(time\_string, translated\_format)  *Notes: BigQuery format codes are translated at compile time to Snowflake equivalents. Non-literal format strings are passed through unchanged with a warning.* |
| [FORMAT\_TIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#format_time)(format\_string, time\_expr) | [TO\_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char)(time\_expr, translated\_format)  *Notes: BigQuery format codes are translated at compile time to Snowflake equivalents. Non-literal format strings are passed through unchanged with a warning.* |
| [TIME\_ADD](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#time_add)(time\_expr, INTERVAL n part) | [DATEADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd)(‘part’, n, time\_expr)  *Notes: The arguments are re-ordered and the BigQuery `INTERVAL n part` literal is converted into Snowflake’s `(part_string, n, time_expr)` argument layout.* |
| [TIME\_DIFF](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#time_diff)(time1, time2, part) | [DATEDIFF](https://docs.snowflake.com/en/sql-reference/functions/datediff)(‘part’, time2, time1)  *Notes: BigQuery’s `TIME_DIFF(a, b, part)` computes `a - b`; The arguments are swapped to match Snowflake’s `(start, end)` convention.* |
| [TIME\_SUB](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#time_sub)(time\_expr, INTERVAL n part) | [DATEADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd)(‘part’, -n, time\_expr)  *Notes: Snowflake has no `TIME_SUB`; the call is rewritten to `DATEADD` with the interval count negated.* |

Expand

Show lessSee more

## Time Functions

| BigQuery | Snowflake |
| --- | --- |
| [FORMAT\_TIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#format_time)(format, time\_expr) | [TO\_CHAR](https://docs.snowflake.com/en/sql-reference/functions/to_char)(time\_expr, converted\_format)  *Notes: BigQuery strptime-style format specifiers (e.g. %H, %M, %S, %T, %R) are mapped to Snowflake TO\_CHAR format codes. Unsupported specifiers emit SSC-EWI-0006. Non-literal format arguments fall through to SSC-EWI-0073.* |
| [TIME\_ADD](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#time_add)(time\_expr, INTERVAL n part) | [DATEADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd)(‘part’, n, time\_expr)  *Notes: The arguments are re-ordered and the BigQuery `INTERVAL n part` literal is converted into Snowflake’s argument layout.* |
| [TIME\_DIFF](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#time_diff)(time1, time2, part) | [DATEDIFF](https://docs.snowflake.com/en/sql-reference/functions/datediff)(‘part’, time2, time1)  *Notes: The arguments are swapped so the result sign matches BigQuery’s `time1 - time2` semantics.* |
| [TIME\_SUB](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions#time_sub)(time\_expr, INTERVAL n part) | [DATEADD](https://docs.snowflake.com/en/sql-reference/functions/dateadd)(‘part’, -n, time\_expr)  *Notes: Snowflake has no `TIME_SUB`; the call is rewritten to `DATEADD` with the interval count negated.* |

Expand

Show lessSee more

## Geography Functions

| BigQuery | Snowflake |
| --- | --- |
| [ST\_GEOGFROMTEXT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext) | [ST\_GEOGFROMTEXT](https://docs.snowflake.com/en/sql-reference/functions/st_geographyfromwkt)  *Note: For further details on this translation, please consult this* [*page*](st_geogfromtext.md)*.* |
| [ST\_GEOGPOINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint) | [ST\_POINT](https://docs.snowflake.com/en/sql-reference/functions/st_makepoint)  *Note: For further details on this translation, please consult this* [*page*](st_geogpoint.md)*.* |
| [ST\_DISTANCE](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_distance)(geog\_a, geog\_b [, use\_spheroid]) | [ST\_DISTANCE](https://docs.snowflake.com/en/sql-reference/functions/st_distance)(geog\_a, geog\_b)  *Notes: The two-argument form is a direct pass-through. The three-argument `use_spheroid` parameter has no Snowflake equivalent and is dropped; if its value is anything other than the literal `FALSE`, see* [*SSC-FDM-BQ0014*](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0014)*.* |

Expand

Show lessSee more

## JSON Functions

| BigQuery | Snowflake |
| --- | --- |
| [JSON\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_value) / [JSON\_EXTRACT\_SCALAR](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_extract_scalar) | [JSON\_EXTRACT\_PATH\_TEXT](https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text)  *Notes: BigQuery JSON paths are automatically translated to their Snowflake equivalents.* |
| [JSON\_VALUE\_ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_value_array) | JSON\_VALUE\_ARRAY\_UDF  *Notes: A UDF is generated to obtain an equivalent behavior for extracting arrays from JSON.* |
| [LAX\_INT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#lax_int64) | PUBLIC.LAX\_INT64\_UDF  *Notes: A UDF is generated to obtain an equivalent behavior.* |
| [LAX\_BOOL](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#lax_bool) | PUBLIC.LAX\_BOOL\_UDF  *Notes: A UDF is generated to obtain an equivalent behavior.* |
| [PARSE\_JSON](https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#parse_json)(json\_string [, wide\_number\_mode => ‘exact’ | ‘round’]) | [PARSE\_JSON](https://docs.snowflake.com/en/sql-reference/functions/parse_json)(json\_string)  *Notes: The single-argument form is a direct pass-through. The optional `wide_number_mode` argument has no Snowflake equivalent and is dropped; Snowflake preserves number precision up to 38 digits. See* [*SSC-FDM-BQ0015*](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0015)*.* |

Expand

Show lessSee more

## Mathematical Functions

| BigQuery | Snowflake |
| --- | --- |
| [ABS](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#abs) | [ABS](https://docs.snowflake.com/en/sql-reference/functions/abs) |
| [LEAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#least) | [LEAST](https://docs.snowflake.com/en/sql-reference/functions/least) |
| [MOD](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#mod) | [MOD](https://docs.snowflake.com/en/sql-reference/functions/mod) |
| [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y, ‘ROUND\_HALF\_EVEN’) [ROUND](https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)(X, Y, ‘ROUND\_HALF\_AWAY\_FROM\_ZERO’) | [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y, ‘HALF\_TO\_EVEN’) [ROUND](https://docs.snowflake.com/en/sql-reference/functions/round)(X, Y, ‘HALF\_AWAY\_FROM\_ZERO’) |

Expand

Show lessSee more

## Navigation Functions

| BigQuery | Snowflake |
| --- | --- |
| [FIRST\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#first_value) | [FIRST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/first_value) |
| [LAG](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#lag) | [LAG](https://docs.snowflake.com/en/sql-reference/functions/lag) |
| [LEAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#lead) | [LEAD](https://docs.snowflake.com/en/sql-reference/functions/lead) |
| [LAST\_VALUE](https://cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions#last_value) | [LAST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value) |

Expand

Show lessSee more

## Numbering Functions

| BigQuery | Snowflake |
| --- | --- |
| [RANK](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#rank) | [RANK](https://docs.snowflake.com/en/sql-reference/functions/rank) |
| [ROW\_NUMBER](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#row_number) | [ROW\_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/row_number) |

Expand

Show lessSee more

## Security Functions

| BigQuery | Snowflake |
| --- | --- |
| [SESSION\_USER](https://cloud.google.com/bigquery/docs/reference/standard-sql/security_functions#session_user) | [CURRENT\_USER](https://docs.snowflake.com/en/sql-reference/functions/current_user)  *Notes: BigQuery’s `SESSION_USER` returns the email address of the authenticated IAM principal; Snowflake’s `CURRENT_USER` returns the Snowflake username (not an email). See* [*SSC-FDM-BQ0016*](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0016)*.* |

Expand

Show lessSee more

## String Functions

| BigQuery | Snowflake |
| --- | --- |
| [BYTE\_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#byte_length)(expr) | LENGTH(TO\_BINARY(HEX\_ENCODE(expr)))  *Notes: BigQuery’s BYTE\_LENGTH returns the number of bytes in an encoded string. Snowflake equivalent converts to binary after hex encoding to get byte length.* |
| [CHARACTER\_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#character_length) [CHAR\_LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#char_length) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [CONCAT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#concat) | [CONCAT](https://docs.snowflake.com/en/sql-reference/functions/concat) |
| [ENDS\_WITH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#ends_with) | [ENDSWITH](https://docs.snowflake.com/en/sql-reference/functions/endswith) |
| [FROM\_BASE64](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#from_base64) | [TRY\_BASE64\_DECODE\_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_base64_decode_binary)  *Notes: BigQuery defaults to BASE64 for binary data output, but Snowflake uses HEX. In Snowflake, you can use the* [*`BASE64_ENCODE`*](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) *function or set* [*`BINARY_OUTPUT_FORMAT`*](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format) *to `'BASE64'` to view binary data in BASE64.* |
| [FROM\_HEX](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#from_hex) | [TRY\_HEX\_DECODE\_BINARY](https://docs.snowflake.com/en/sql-reference/functions/try_hex_decode_binary)  *Notes: BigQuery defaults to BASE64 for binary data output, but Snowflake uses HEX. In Snowflake, you can use the* [*`BASE64_ENCODE`*](https://docs.snowflake.com/en/sql-reference/functions/base64_encode) *function or set* [*`BINARY_OUTPUT_FORMAT`*](https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format) *to `'BASE64'` to view binary data in BASE64.* |
| [LEFT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#left) | [LEFT](https://docs.snowflake.com/en/sql-reference/functions/left) |
| [LENGTH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#length) | [LENGTH](https://docs.snowflake.com/en/sql-reference/functions/length) |
| [LOWER](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#lower) | [LOWER](https://docs.snowflake.com/en/sql-reference/functions/lower) |
| [LPAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#lpad) | [LPAD](https://docs.snowflake.com/en/sql-reference/functions/lpad) |
| [LTRIM](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#ltrim) | [LTRIM](https://docs.snowflake.com/en/sql-reference/functions/ltrim) |
| [REGEXP\_CONTAINS](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_contains)(value, regexp) | [REGEXP\_INSTR](/sql-reference/functions/regexp_instr)(value, regexp) > 0 |
| [REGEXP\_EXTRACT\_ALL](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#regexp_extract_all) | [REGEXP\_SUBSTR\_ALL](https://docs.snowflake.com/en/sql-reference/functions/regexp_substr_all) |
| [REPLACE](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#replace) | [REPLACE](https://docs.snowflake.com/en/sql-reference/functions/replace) |
| [RIGHT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#right) | [RIGHT](https://docs.snowflake.com/en/sql-reference/functions/right) |
| [RPAD](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#rpad) | [RPAD](https://docs.snowflake.com/en/sql-reference/functions/rpad) |
| [RTRIM](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#rtrim) | [RTRIM](https://docs.snowflake.com/en/sql-reference/functions/rtrim) |
| [SPLIT](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#split) | [SPLIT](https://docs.snowflake.com/en/sql-reference/functions/split) |
| [STARTS\_WITH](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#starts_with) | [STARTSWITH](https://docs.snowflake.com/en/sql-reference/functions/startswith) |
| [SUBSTR](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substr)(string, position)  [SUBSTRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substring)(string, position)  [SUBSTR](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substr)(string, position, length)  [SUBSTRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#substring)(string, position, length) | [SUBSTR](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position))  [SUBSTRING](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position))  [SUBSTR](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position), length)  [SUBSTRING](https://docs.snowflake.com/en/sql-reference/functions/substr)(string, IFF(position < -LENGTH(string), 1, position), length) |
| [TO\_HEX](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#to_hex) | [HEX\_ENCODE](https://docs.snowflake.com/en/sql-reference/functions/hex_encode) |
| [UNICODE](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#unicode)(string\_expr) | [UNICODE](https://docs.snowflake.com/en/sql-reference/functions/unicode)(string\_expr)  *Notes: Direct pass-through. Both functions return the Unicode code point of the first character of the input string.* |
| [UPPER](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#upper) | [UPPER](https://docs.snowflake.com/en/sql-reference/functions/upper) |

Expand

Show lessSee more

## Timestamp Functions

| BigQuery | Snowflake |
| --- | --- |
| [CURRENT\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp) [CURRENT\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp)() | [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)  [CURRENT\_TIMESTAMP](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp)() |
| [SAFE.TIMESTAMP\_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis) | IFF(expr BETWEEN -62135596800000 AND 253402300799999, TO\_TIMESTAMP(expr / 1000), null)  *Notes: Safe version with range validation to prevent overflow errors.* |
| [SAFE.TIMESTAMP\_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds) | SAFE\_TIMESTAMP\_SECONDS\_UDF(expr)  *Notes: A UDF is generated to provide safe timestamp conversion with error handling.* |
| [TIMESTAMP\_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis) | TO\_TIMESTAMP(expr / 1000)  *Notes: Converts milliseconds since epoch to timestamp by dividing by 1000.* |
| [TIMESTAMP\_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds)(expr) | DATEADD(‘seconds’, expr, ’1970-01-01’)  *Notes: Adds seconds to Unix epoch start date.* |
| [UNIX\_MICROS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_micros)(timestamp) | DATE\_PART(‘epoch\_microsecond’, CONVERT\_TIMEZONE(‘UTC’, timestamp))  *Notes: Extracts microseconds since Unix epoch from timestamp converted to UTC.* |
| [UNIX\_MILLIS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_millis)(timestamp) | DATE\_PART(‘epoch\_millisecond’, CONVERT\_TIMEZONE(‘UTC’, timestamp))  *Notes: Extracts milliseconds since Unix epoch from timestamp converted to UTC.* |
| [UNIX\_SECONDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#unix_seconds)(timestamp) | DATE\_PART(‘epoch\_seconds’, CONVERT\_TIMEZONE(‘UTC’, timestamp))  *Notes: Extracts seconds since Unix epoch from timestamp converted to UTC.* |
| [PARSE\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp)(format\_string, timestamp\_string [, timezone]) | [TO\_TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/functions/to_timestamp)(timestamp\_string, converted\_format) — or, when a timezone argument is supplied, [CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone)(timezone, ‘UTC’, TO\_TIMESTAMP\_NTZ(…)) :: TIMESTAMP\_TZ  *Notes: BigQuery format elements (e.g. `%Y-%m-%d %H:%M:%S`) are translated to the equivalent Snowflake format. The 3-argument form emits [SSC-EWI-BQ0018](../../issues-and-troubleshooting/conversion-issues/bigqueryEWI#ssc-ewi-bq0018) because Snowflake interprets the timezone as the source rather than the result of the parse.* |
| [FORMAT\_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#format_timestamp)(format\_string, timestamp [, timezone]) | [TO\_VARCHAR](https://docs.snowflake.com/en/sql-reference/functions/to_varchar)(timestamp, converted\_format) — or, when a timezone argument is supplied, [TO\_VARCHAR](https://docs.snowflake.com/en/sql-reference/functions/to_varchar)([CONVERT\_TIMEZONE](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone)(timezone, timestamp), converted\_format)  *Notes: BigQuery format elements are translated to the equivalent Snowflake format. The 3-argument form first shifts the timestamp into the requested timezone before formatting.* |

Expand

Show lessSee more

## FORMAT\_DATE

Format\_date function

### Description

Formats a `DATE` value according to a specified format string.

For more information, please refer to [FORMAT\_DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions#format_date) function.

### Grammar Syntax

Copy code

```
 FORMAT_DATE(format_string, date_expr)
```

#### Sample Source

##### BigQuery

Copy code

```
CREATE TABLE TEST_DATE (col1 DATE);
SELECT FORMAT_DATE('%Y', col1);
```

##### Snowflake

Copy code

```
CREATE TABLE TEST_DATE (col1 DATE);
SELECT
  TO_CHAR(col1, 'YYYY')
FROM
  TEST_DATE;
```

#### BigQuery Formats Equivalents

| BigQuery | Snowflake |
| --- | --- |
| %A | PUBLIC.DAYNAME\_LONG\_UDF(date\_expr)  *Note: Generate UDF in conversion for support.* |
| %a | DY |
| %B | MMMM |
| %b | MON |
| %C | PUBLIC.CENTURY\_UDF(date\_expr)  *Note: Generate UDF in conversion for support.* |
| %c | DY MON DD HH24:MI:SS YYYY |
| %D | MM/DD/YY |
| %d | DD |
| %e | DD |
| %F | YYYY-MM-DD |
| %G | YEAROFWEEKISO(date\_expr) |
| %g | PUBLIC.ISO\_YEAR\_PART\_UDF(date\_expr, 2)  *Note: Generate UDF in conversion for support.* |
| %H | HH24 |
| %h | MON |
| %I | HH12 |
| %J | PUBLIC.DAY\_OF\_YEAR\_ISO\_UDF(date\_expr)  *Note: Generate UDF in conversion for support.* |
| %j | DAYOFYEAR(date\_expr) |
| %k | HH24 |
| %l | HH12 |
| %M | MI |
| %m | MM |
| %n | *Not equivalent format* |
| %P | pm |
| %p | AM |
| %Q | QUARTER(date\_expr) |
| %R | HH24:MI |
| %S | SS |
| %s | *Not equivalent format* |
| %T | HH24:MI:SS |
| %t | *Not equivalent format* |
| %U | WEEK(date\_expr) |
| %u | DAYOFWEEKISO(date\_expr) |
| %V | WEEKISO(date\_expr) |
| %W | WEEK(date\_expr)   *Note: Unlike BigQuery, Snowflake results are dictated by the values set for the WEEK\_OF\_YEAR\_POLICY and/or WEEK\_START session parameters. So, results could differ from BigQuery based on those parameters.* |
| %w | DAYOFWEEK(date\_expr)  *Note: Unlike BigQuery, Snowflake results are dictated by the values set for the WEEK\_OF\_YEAR\_POLICY and/or WEEK\_START session parameters. So, results could differ from BigQuery based on those parameters.* |
| %X | HH24:MI:SS |
| %x | MM/DD/YY |
| %Y | YYYY |
| %y | YY |
| %Z | *Not equivalent format* |
| %z | *Not equivalent format* |
| %Ez | *Not equivalent format* |
| %E<number>S | *Not equivalent format* |
| %E\*S | *Not equivalent format* |
| %EY4 | YYYY |

Warning

In BigQuery, the format related to time is not applied when the type is DATE, but Snowflake applies the format with values in zero for HH:MI:SS usages.

Note

For more information, please refer to [BigQuery DateTime formats](https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements#format_elements_date_time).

## ST\_GEOGFROMTEXT

Geography Function.

### Description

> Returns a `GEOGRAPHY` value that corresponds to the input [WKT](https://en.wikipedia.org/wiki/Well-known_text) representation.

For more information, please refer to [ST\_GEOGFROMTEXT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext) function.

Note

:class: tip
ST\_GEOGFROMTEXT function is supported in Snowflake.

### Grammar Syntax

Copy code

```
 ST_GEOGFROMTEXT(wkt_string[, oriented])
```

#### Sample Source

The oriented parameter in the ST\_GEOGFROMTEXT function is not supported in Snowflake.

##### BigQuery

Copy code

```
 SELECT ST_GEOGFROMTEXT('POINT(-122.35 37.55)');
SELECT ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', TRUE);
```

##### Snowflake

Copy code

```
 SELECT ST_GEOGFROMTEXT('POINT(-122.35 37.55)');
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0006 - ORIENTED PARAMETER IN THE ST_GEOGFROMTEXT FUNCTION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
ST_GEOGFROMTEXT('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
```

Please keep in mind that the default output format for geography data types is **WKT** **(Well-Known Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the [ST\_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the [GEOGRAPHY\_OUTPUT\_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format) format if you want to view the data in **WKT** format.

#### Using ST\_GEOGFROMTEXT function to insert geography data

This function is not allowed in the values clause and is not required in Snowflake.

##### BigQuery

Copy code

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType VALUES
    (ST_GEOGFROMTEXT('POINT(-122.35 37.55)')),
    (ST_GEOGFROMTEXT('LINESTRING(-124.20 42.00, -120.01 41.99)'));
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'POINT(-122.35 37.55)'),
    (
     --** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
     'LINESTRING(-124.20 42.00, -120.01 41.99)');
```

### Related EWIs

1. [SSC-EWI-BQ0006](../../issues-and-troubleshooting/conversion-issues/bigqueryEWI#ssc-ewi-bq0006): Oriented parameter in the ST\_GEOGFROMTEXT function is not supported in Snowflake.
2. [SSC-FDM-BQ0010](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0010): Geography function is not required in Snowflake.

## ST\_GEOGPOINT

Geography Function.

### Description

> Creates a `GEOGRAPHY` with a single point. `ST_GEOGPOINT` creates a point from the specified `FLOAT64` longitude (in degrees, negative west of the Prime Meridian, positive east) and latitude (in degrees, positive north of the Equator, negative south) parameters and returns that point in a `GEOGRAPHY` value.

For more information, please refer to [ST\_GEOGPOINT](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint) function.

Note

The function ST\_GEOGPOINT is translated to ST\_POINT in Snowflake.

### Grammar Syntax

Copy code

```
 ST_GEOGPOINT(longitude, latitude)
```

#### Sample Source

##### BigQuery

Copy code

```
 SELECT ST_GEOGPOINT(-122.0838, 37.3860);
```

##### Snowflake

Copy code

```
 SELECT ST_POINT(-122.0838, 37.3860);
```

Please keep in mind that the default output format for geography data types is **WKT** **(Well-Known Text)** and in Snowflake **WKB (Well-Known Binary)**. You can use the [ST\_ASWKT](https://docs.snowflake.com/en/sql-reference/functions/st_aswkt) function or set the [GEOGRAPHY\_OUTPUT\_FORMAT](https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format) format if you want to view the data in **WKT** format.

#### Using ST\_POINT function to insert geography data

This function is not allowed in the values clause and is not required in Snowflake.

##### BigQuery

Copy code

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
);

INSERT INTO test.geographyType
VALUES (ST_GEOGPOINT(-122.0838, 37.3860));
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE test.geographyType
(
  COL1 GEOGRAPHY
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "04/03/2025",  "domain": "test" }}';

INSERT INTO test.geographyType
VALUES (
--** SSC-FDM-BQ0010 - THE FUNCTION 'ST_GEOGFROMTEXT' IS NOT REQUIRED IN SNOWFLAKE. **
'POINT(122.0838 37.3860)');
```

### Related EWIs

1. [SSC-FDM-BQ0010](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0010): Geography function is not required in Snowflake.

## Debugging Functions

| BigQuery | Snowflake |
| --- | --- |
| [ERROR](https://cloud.google.com/bigquery/docs/reference/standard-sql/debugging_functions#error)(message) | PUBLIC.ERROR\_UDF(message)  *Notes: BigQuery’s `ERROR` raises a runtime error with the supplied message. A UDF wrapper is generated that calls a Snowflake stored procedure to raise an equivalent exception, since Snowflake SQL does not provide a built-in `ERROR` function in scalar context.* |

Expand

Show lessSee more

## UUID Functions

| BigQuery | Snowflake |
| --- | --- |
| [GENERATE\_UUID](https://cloud.google.com/bigquery/docs/reference/standard-sql/uuid_functions#generate_uuid)() | [UUID\_STRING](https://docs.snowflake.com/en/sql-reference/functions/uuid_string)()  *Notes: Both functions return an RFC 4122-compliant version 4 UUID as a string. Direct replacement.* |

Expand

Show lessSee more
