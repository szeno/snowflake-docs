# System data metric functions

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic is a reference for the system data metric functions (DMFs) that Snowflake provides to all accounts. DMFs are the building block
of [data quality checks](/user-guide/data-quality-intro).

## About system DMFs

Snowflake provides system DMFs in the CORE schema of the shared [SNOWFLAKE database](/sql-reference/snowflake-db). System DMFs are
maintained by Snowflake; you cannot change the name or functionality of any system DMF.

Each system DMF enables you to measure a different data quality attribute. You can assign more than one system DMF to a table or view to
allow for a more comprehensive data quality measurement to address your governance and compliance needs.

The Statistics DMFs return a measurement rather than a pass or fail signal. You define the expectation that determines whether a given
value indicates a problem. The Outliers DMFs apply a built-in threshold, such as Tukey fences or a Z-score cutoff, and return the number
or percentage of values that fall outside it.

## System DMFs

Currently, Snowflake supports these system DMFs to measure common metrics without having to define them:

| Category | System DMF | Description |
| --- | --- | --- |
| Completeness | [BLANK\_COUNT](/sql-reference/functions/dmf_blank_count) | Determine how many blank values are in a column. |
|  | [BLANK\_PERCENT](/sql-reference/functions/dmf_blank_percent) | Determine what percentage of a column’s values are blank. |
|  | [EMPTY\_STRING\_COUNT](/sql-reference/functions/dmf_empty_string_count) | Determine how many empty strings are in a column. |
|  | [EMPTY\_STRING\_PERCENT](/sql-reference/functions/dmf_empty_string_percent) | Determine what percentage of a column’s values are empty strings. |
|  | [NOT\_NULL\_COUNT](/sql-reference/functions/dmf_not_null_count) | Determine how many non-NULL values are in a column. |
|  | [NOT\_NULL\_PERCENT](/sql-reference/functions/dmf_not_null_percent) | Determine what percentage of a column’s values are not NULL. |
|  | [NULL\_COUNT](/sql-reference/functions/dmf_null_count) | Determine how many NULL values are in a column. |
|  | [NULL\_PERCENT](/sql-reference/functions/dmf_null_percent) | Determine what percentage of a column’s values are NULL. |
| Consistency | [CASE\_FORMAT\_VIOLATION\_COUNT](/sql-reference/functions/dmf_case_format_violation_count) | Determine how many non-NULL values in a string column have inconsistent casing (not all-uppercase, all-lowercase, or title-case). |
|  | [CASE\_FORMAT\_VIOLATION\_PERCENT](/sql-reference/functions/dmf_case_format_violation_percent) | Determine what percentage of non-NULL values in a string column have inconsistent casing. |
|  | [SPECIAL\_CHARACTER\_COUNT](/sql-reference/functions/dmf_special_character_count) | Determine how many non-NULL values in a string column contain characters outside the alphanumeric range. |
|  | [SPECIAL\_CHARACTER\_PERCENT](/sql-reference/functions/dmf_special_character_percent) | Determine what percentage of non-NULL values in a string column contain characters outside the alphanumeric range. |
|  | [UNTRIMMED\_STRING\_COUNT](/sql-reference/functions/dmf_untrimmed_string_count) | Determine how many non-NULL values in a string column have leading or trailing whitespace. |
|  | [UNTRIMMED\_STRING\_PERCENT](/sql-reference/functions/dmf_untrimmed_string_percent) | Determine what percentage of non-NULL values in a string column have leading or trailing whitespace. |
| Freshness | [FRESHNESS](/sql-reference/functions/dmf_freshness) | Determine the freshness of a table’s data based on a timestamp column or the most recent [DML operation](/sql-reference/sql-dml). |
| Outliers | [EXTREME\_OUTLIER\_COUNT](/sql-reference/functions/dmf_extreme_outlier_count) | Determine how many values in a numeric column fall outside the extreme asymmetric Tukey fences for the column. |
|  | [EXTREME\_OUTLIER\_IQR\_COUNT](/sql-reference/functions/dmf_extreme_outlier_iqr_count) | Determine how many values in a numeric column fall outside the extreme Tukey fences (3 times the interquartile range). |
|  | [EXTREME\_OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_iqr_percent) | Determine what percentage of values in a numeric column fall outside the extreme Tukey fences (3 times the interquartile range). |
|  | [EXTREME\_OUTLIER\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_percent) | Determine what percentage of values in a numeric column fall outside the extreme asymmetric Tukey fences for the column. |
|  | [EXTREME\_OUTLIER\_ZSCORE\_COUNT](/sql-reference/functions/dmf_extreme_outlier_zscore_count) | Determine how many values in a numeric column have a Z-score greater than 4.5. |
|  | [EXTREME\_OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_zscore_percent) | Determine what percentage of values in a numeric column have a Z-score greater than 4.5. |
|  | [OUTLIER\_COUNT](/sql-reference/functions/dmf_outlier_count) | Determine how many values in a numeric column fall outside the asymmetric Tukey fences for the column. |
|  | [OUTLIER\_IQR\_COUNT](/sql-reference/functions/dmf_outlier_iqr_count) | Determine how many values in a numeric column fall outside the standard Tukey fences (1.5 times the interquartile range). |
|  | [OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_outlier_iqr_percent) | Determine what percentage of values in a numeric column fall outside the standard Tukey fences (1.5 times the interquartile range). |
|  | [OUTLIER\_PERCENT](/sql-reference/functions/dmf_outlier_percent) | Determine what percentage of values in a numeric column fall outside the asymmetric Tukey fences for the column. |
|  | [OUTLIER\_ZSCORE\_COUNT](/sql-reference/functions/dmf_outlier_zscore_count) | Determine how many values in a numeric column have a Z-score greater than 3. |
|  | [OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_outlier_zscore_percent) | Determine what percentage of values in a numeric column have a Z-score greater than 3. |
| Schema | [SCHEMA\_CHANGE\_COUNT](/sql-reference/functions/dmf_schema_change_count) | Count schema changes (column add, drop, rename, or type change) detected between consecutive evaluations. |
| Statistics | [APPROX\_QUANTILE\_25](/sql-reference/functions/dmf_approx_quantile_25) | Determine the approximate 25th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_50](/sql-reference/functions/dmf_approx_quantile_50) | Determine the approximate 50th percentile (median) value for a numeric column. |
|  | [APPROX\_QUANTILE\_99](/sql-reference/functions/dmf_approx_quantile_99) | Determine the approximate 99th percentile value for a numeric column. |
|  | [AVG](/sql-reference/functions/dmf_avg) | Determine the average value of a column. |
|  | [GEOMETRIC\_MEAN](/sql-reference/functions/dmf_geometric_mean) | Determine the geometric mean of the positive values in a numeric column. |
|  | [HARMONIC\_MEAN](/sql-reference/functions/dmf_harmonic_mean) | Determine the harmonic mean of the nonzero values in a numeric column. |
|  | [MAX](/sql-reference/functions/dmf_max) | Determine the maximum value of a column. |
|  | [MEDIAN](/sql-reference/functions/dmf_median) | Determine the exact median value for a numeric column. |
|  | [MIN](/sql-reference/functions/dmf_min) | Determine the minimum value of a column. |
|  | [NEGATIVE\_COUNT](/sql-reference/functions/dmf_negative_count) | Determine how many values in a numeric column are negative. |
|  | [NEGATIVE\_PERCENT](/sql-reference/functions/dmf_negative_percent) | Determine what percentage of values in a numeric column are negative. |
|  | [STDDEV](/sql-reference/functions/dmf_stddev) | Determine the standard deviation value for a column. |
|  | [STRING\_LENGTH\_AVG](/sql-reference/functions/dmf_string_length_avg) | Determine the average string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_MAX](/sql-reference/functions/dmf_string_length_max) | Determine the maximum string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_MIN](/sql-reference/functions/dmf_string_length_min) | Determine the minimum string length of non-NULL values for a string column. |
|  | [SUM](/sql-reference/functions/dmf_sum) | Determine the sum of the values in a numeric column. |
|  | [VARIANCE](/sql-reference/functions/dmf_variance) | Determine the variance value for a numeric column. |
|  | [ZERO\_COUNT](/sql-reference/functions/dmf_zero_count) | Determine how many values in a numeric column are equal to zero. |
|  | [ZERO\_PERCENT](/sql-reference/functions/dmf_zero_percent) | Determine what percentage of values in a numeric column are equal to zero. |
| Uniqueness | [DUPLICATE\_COUNT](/sql-reference/functions/dmf_duplicate_count) | Determine the number of duplicate values in a column, including NULL values. |
|  | [DUPLICATE\_PERCENT](/sql-reference/functions/dmf_duplicate_percent) | Determine what percentage of non-NULL rows have a value that occurs more than once. |
|  | [UNIQUE\_COUNT](/sql-reference/functions/dmf_unique_count) | Determine the number of unique, non-NULL values in a column. |
|  | [UNIQUE\_PERCENT](/sql-reference/functions/dmf_unique_percent) | Determine what percentage of non-NULL rows have a value that occurs exactly once. |
| Validity | [ACCEPTED\_VALUES](/sql-reference/functions/dmf_accepted_values) | Determine whether values in a column match a Boolean expression. |
|  | [FUTURE\_TIMESTAMP\_COUNT](/sql-reference/functions/dmf_future_timestamp_count) | Determine how many values in a date/timestamp column are in the future relative to the scheduled evaluation time. |
|  | [FUTURE\_TIMESTAMP\_PERCENT](/sql-reference/functions/dmf_future_timestamp_percent) | Determine what percentage of values in a date/timestamp column are in the future relative to the scheduled evaluation time. |
|  | [INVALID\_CUSIP\_COUNT](/sql-reference/functions/dmf_invalid_cusip_count) | Determine how many non-NULL values in a string column are not a valid CUSIP. |
|  | [INVALID\_CUSIP\_PERCENT](/sql-reference/functions/dmf_invalid_cusip_percent) | Determine what percentage of values in a string column are not a valid CUSIP. |
|  | [INVALID\_EMAIL\_COUNT](/sql-reference/functions/dmf_invalid_email_count) | Determine how many non-NULL values in a string column are not a valid email address. |
|  | [INVALID\_EMAIL\_PERCENT](/sql-reference/functions/dmf_invalid_email_percent) | Determine what percentage of values in a string column are not a valid email address. |
|  | [INVALID\_FIGI\_COUNT](/sql-reference/functions/dmf_invalid_figi_count) | Determine how many non-NULL values in a string column are not a valid FIGI. |
|  | [INVALID\_FIGI\_PERCENT](/sql-reference/functions/dmf_invalid_figi_percent) | Determine what percentage of values in a string column are not a valid FIGI. |
|  | [INVALID\_ISIN\_COUNT](/sql-reference/functions/dmf_invalid_isin_count) | Determine how many non-NULL values in a string column are not a valid ISIN. |
|  | [INVALID\_ISIN\_PERCENT](/sql-reference/functions/dmf_invalid_isin_percent) | Determine what percentage of values in a string column are not a valid ISIN. |
|  | [INVALID\_JSON\_COUNT](/sql-reference/functions/dmf_invalid_json_count) | Determine how many non-NULL values in a string column are not valid JSON. |
|  | [INVALID\_JSON\_PERCENT](/sql-reference/functions/dmf_invalid_json_percent) | Determine what percentage of non-NULL values in a string column are not valid JSON. |
|  | [INVALID\_LATITUDE\_COUNT](/sql-reference/functions/dmf_invalid_latitude_count) | Determine how many values in a numeric column are outside the valid latitude range (-90 to 90). |
|  | [INVALID\_LATITUDE\_PERCENT](/sql-reference/functions/dmf_invalid_latitude_percent) | Determine what percentage of values in a numeric column are outside the valid latitude range (-90 to 90). |
|  | [INVALID\_LEI\_COUNT](/sql-reference/functions/dmf_invalid_lei_count) | Determine how many non-NULL values in a string column are not a valid LEI. |
|  | [INVALID\_LEI\_PERCENT](/sql-reference/functions/dmf_invalid_lei_percent) | Determine what percentage of values in a string column are not a valid LEI. |
|  | [INVALID\_LONGITUDE\_COUNT](/sql-reference/functions/dmf_invalid_longitude_count) | Determine how many values in a numeric column are outside the valid longitude range (-180 to 180). |
|  | [INVALID\_LONGITUDE\_PERCENT](/sql-reference/functions/dmf_invalid_longitude_percent) | Determine what percentage of values in a numeric column are outside the valid longitude range (-180 to 180). |
|  | [INVALID\_NUMERIC\_TYPE\_CAST\_COUNT](/sql-reference/functions/dmf_invalid_numeric_type_cast_count) | Determine how many non-NULL values in a string column cannot be parsed as numeric. |
|  | [INVALID\_NUMERIC\_TYPE\_CAST\_PERCENT](/sql-reference/functions/dmf_invalid_numeric_type_cast_percent) | Determine what percentage of non-NULL values in a string column cannot be parsed as numeric. |
|  | [INVALID\_PERM\_ID\_COUNT](/sql-reference/functions/dmf_invalid_perm_id_count) | Determine how many non-NULL values in a string column are not a valid PermID. |
|  | [INVALID\_PERM\_ID\_PERCENT](/sql-reference/functions/dmf_invalid_perm_id_percent) | Determine what percentage of values in a string column are not a valid PermID. |
|  | [INVALID\_SEDOL\_COUNT](/sql-reference/functions/dmf_invalid_sedol_count) | Determine how many non-NULL values in a string column are not a valid SEDOL. |
|  | [INVALID\_SEDOL\_PERCENT](/sql-reference/functions/dmf_invalid_sedol_percent) | Determine what percentage of values in a string column are not a valid SEDOL. |
|  | [INVALID\_TIMESTAMP\_STRING\_COUNT](/sql-reference/functions/dmf_invalid_timestamp_string_count) | Determine how many non-NULL values in a string column can’t be parsed as a timestamp or date. |
|  | [INVALID\_TIMESTAMP\_STRING\_PERCENT](/sql-reference/functions/dmf_invalid_timestamp_string_percent) | Determine what percentage of values in a string column can’t be parsed as a timestamp or date. |
|  | [INVALID\_USA\_PHONE\_COUNT](/sql-reference/functions/dmf_invalid_usa_phone_count) | Determine how many non-NULL values in a string column are not a valid U.S. phone number. |
|  | [INVALID\_USA\_PHONE\_PERCENT](/sql-reference/functions/dmf_invalid_usa_phone_percent) | Determine what percentage of values in a string column are not a valid U.S. phone number. |
|  | [INVALID\_USA\_STATE\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_usa_state_code_count) | Determine how many non-NULL values in a string column are not a valid U.S. state code. |
|  | [INVALID\_USA\_STATE\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_usa_state_code_percent) | Determine what percentage of values in a string column are not a valid U.S. state code. |
|  | [INVALID\_USA\_ZIP\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_usa_zip_code_count) | Determine how many non-NULL values in a string column are not a valid U.S. ZIP Code. |
|  | [INVALID\_USA\_ZIP\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_usa_zip_code_percent) | Determine what percentage of values in a string column are not a valid U.S. ZIP Code. |
|  | [INVALID\_UUID\_COUNT](/sql-reference/functions/dmf_invalid_uuid_count) | Determine how many non-NULL values in a string column are not a valid UUID. |
|  | [INVALID\_UUID\_PERCENT](/sql-reference/functions/dmf_invalid_uuid_percent) | Determine what percentage of values in a string column are not a valid UUID. |
|  | [NOT\_IN\_FUTURE\_COUNT](/sql-reference/functions/dmf_not_in_future_count) | Determine how many values in a date/timestamp column are not in the future relative to the scheduled evaluation time. |
|  | [NOT\_IN\_FUTURE\_PERCENT](/sql-reference/functions/dmf_not_in_future_percent) | Determine what percentage of values in a date/timestamp column are not in the future relative to the scheduled evaluation time. |
| Volume | [ROW\_COUNT](/sql-reference/functions/dmf_row_count) | Determine how many records are in the table or view. |

Expand

Show lessSee more

Some system DMFs measure closely related conditions:

- NULL\_COUNT and NOT\_NULL\_COUNT are complements: together they count every row. The same is true of NULL\_PERCENT and NOT\_NULL\_PERCENT.
- BLANK\_COUNT counts values that are empty or contain only spaces, such as `''` and `' '`. EMPTY\_STRING\_COUNT counts only the empty
  string `''`. Neither function counts NULL values.
- FUTURE\_TIMESTAMP\_COUNT counts values that are later than the scheduled evaluation time, and NOT\_IN\_FUTURE\_COUNT counts values that
  are at or before it. Neither function counts NULL values, so together they count every non-NULL value.
- DUPLICATE\_PERCENT returns the percentage of non-NULL rows whose value occurs more than once, and UNIQUE\_PERCENT returns the percentage
  whose value occurs exactly once. Both exclude NULL values, so together they add up to 100 when the column has a non-NULL value.

## Related functions

[DATA\_METRIC\_SCHEDULED\_TIME](/sql-reference/functions/dmf_data_metric_schedule_time) isn’t a metric and you can’t associate it with a table
or view. Call it in the body of a [custom DMF](/user-guide/data-quality-custom-dmfs) to retrieve the scheduled evaluation time, for example
to define a custom freshness metric.
