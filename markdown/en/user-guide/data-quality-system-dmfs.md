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

## System DMFs

Currently, Snowflake supports these system DMFs to measure common metrics without having to define them:

| Category | System DMF | Description |
| --- | --- | --- |
| Accuracy | [BLANK\_COUNT](/sql-reference/functions/dmf_blank_count) | Determine how many blank values are in a column. |
|  | [BLANK\_PERCENT](/sql-reference/functions/dmf_blank_percent) | Determine what percentage of a column’s values are blank. |
|  | [CASE\_FORMAT\_VIOLATION\_COUNT](/sql-reference/functions/dmf_case_format_violation_count) | Determine how many non-NULL values in a string column have inconsistent casing (not all-uppercase, all-lowercase, or title-case). |
|  | [CASE\_FORMAT\_VIOLATION\_PERCENT](/sql-reference/functions/dmf_case_format_violation_percent) | Determine what percentage of non-NULL values in a string column have inconsistent casing. |
|  | [FUTURE\_TIMESTAMP\_COUNT](/sql-reference/functions/dmf_future_timestamp_count) | Determine how many values in a date/timestamp column are in the future relative to the scheduled evaluation time. |
|  | [FUTURE\_TIMESTAMP\_PERCENT](/sql-reference/functions/dmf_future_timestamp_percent) | Determine what percentage of values in a date/timestamp column are in the future relative to the scheduled evaluation time. |
|  | [INVALID\_JSON\_COUNT](/sql-reference/functions/dmf_invalid_json_count) | Determine how many non-NULL values in a string column are not valid JSON. |
|  | [INVALID\_JSON\_PERCENT](/sql-reference/functions/dmf_invalid_json_percent) | Determine what percentage of non-NULL values in a string column are not valid JSON. |
|  | [INVALID\_NUMERIC\_TYPE\_CAST\_COUNT](/sql-reference/functions/dmf_invalid_numeric_type_cast_count) | Determine how many non-NULL values in a string column cannot be parsed as numeric. |
|  | [INVALID\_NUMERIC\_TYPE\_CAST\_PERCENT](/sql-reference/functions/dmf_invalid_numeric_type_cast_percent) | Determine what percentage of non-NULL values in a string column cannot be parsed as numeric. |
|  | [NEGATIVE\_COUNT](/sql-reference/functions/dmf_negative_count) | Determine how many values in a numeric column are negative. |
|  | [NEGATIVE\_PERCENT](/sql-reference/functions/dmf_negative_percent) | Determine what percentage of values in a numeric column are negative. |
|  | [NULL\_COUNT](/sql-reference/functions/dmf_null_count) | Determine how many NULL values are in a column. |
|  | [NULL\_PERCENT](/sql-reference/functions/dmf_null_percent) | Determine what percentage of a column’s values are NULL. |
|  | [SPECIAL\_CHARACTER\_COUNT](/sql-reference/functions/dmf_special_character_count) | Determine how many non-NULL values in a string column contain characters outside the alphanumeric range. |
|  | [SPECIAL\_CHARACTER\_PERCENT](/sql-reference/functions/dmf_special_character_percent) | Determine what percentage of non-NULL values in a string column contain characters outside the alphanumeric range. |
|  | [UNTRIMMED\_STRING\_COUNT](/sql-reference/functions/dmf_untrimmed_string_count) | Determine how many non-NULL values in a string column have leading or trailing whitespace. |
|  | [UNTRIMMED\_STRING\_PERCENT](/sql-reference/functions/dmf_untrimmed_string_percent) | Determine what percentage of non-NULL values in a string column have leading or trailing whitespace. |
|  | [ZERO\_COUNT](/sql-reference/functions/dmf_zero_count) | Determine how many values in a numeric column are equal to zero. |
|  | [ZERO\_PERCENT](/sql-reference/functions/dmf_zero_percent) | Determine what percentage of values in a numeric column are equal to zero. |
| Freshness | [FRESHNESS](/sql-reference/functions/dmf_freshness) | Determine the freshness of a table’s data based on a timestamp column or the most recent [DML operation](/sql-reference/sql-dml). |
|  | [DATA\_METRIC\_SCHEDULE\_TIME](/sql-reference/functions/dmf_data_metric_schedule_time) | Define custom freshness metrics. |
| Schema | [SCHEMA\_CHANGE\_COUNT](/sql-reference/functions/dmf_schema_change_count) | Count schema changes (column add, drop, rename, or type change) detected between consecutive evaluations. |
| Statistics | [APPROX\_QUANTILE\_25](/sql-reference/functions/dmf_approx_quantile_25) | Determine the approximate 25th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_50](/sql-reference/functions/dmf_approx_quantile_50) | Determine the approximate 50th percentile (median) value for a numeric column. |
|  | [APPROX\_QUANTILE\_99](/sql-reference/functions/dmf_approx_quantile_99) | Determine the approximate 99th percentile value for a numeric column. |
|  | [AVG](/sql-reference/functions/dmf_avg) | Determine the average value of a column. |
|  | [EXTREME\_OUTLIER\_COUNT](/sql-reference/functions/dmf_extreme_outlier_count) | Determine how many values in a numeric column fall outside the extreme asymmetric Tukey fences for the column. |
|  | [EXTREME\_OUTLIER\_IQR\_COUNT](/sql-reference/functions/dmf_extreme_outlier_iqr_count) | Determine how many values in a numeric column fall outside the extreme Tukey fences (3 times the interquartile range). |
|  | [EXTREME\_OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_iqr_percent) | Determine what percentage of values in a numeric column fall outside the extreme Tukey fences (3 times the interquartile range). |
|  | [EXTREME\_OUTLIER\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_percent) | Determine what percentage of values in a numeric column fall outside the extreme asymmetric Tukey fences for the column. |
|  | [EXTREME\_OUTLIER\_ZSCORE\_COUNT](/sql-reference/functions/dmf_extreme_outlier_zscore_count) | Determine how many values in a numeric column have a Z-score greater than 4.5. |
|  | [EXTREME\_OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_zscore_percent) | Determine what percentage of values in a numeric column have a Z-score greater than 4.5. |
|  | [MAX](/sql-reference/functions/dmf_max) | Determine the maximum value of a column. |
|  | [MEDIAN](/sql-reference/functions/dmf_median) | Determine the exact median value for a numeric column. |
|  | [MIN](/sql-reference/functions/dmf_min) | Determine the minimum value of a column. |
|  | [OUTLIER\_COUNT](/sql-reference/functions/dmf_outlier_count) | Determine how many values in a numeric column fall outside the asymmetric Tukey fences for the column. |
|  | [OUTLIER\_IQR\_COUNT](/sql-reference/functions/dmf_outlier_iqr_count) | Determine how many values in a numeric column fall outside the standard Tukey fences (1.5 times the interquartile range). |
|  | [OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_outlier_iqr_percent) | Determine what percentage of values in a numeric column fall outside the standard Tukey fences (1.5 times the interquartile range). |
|  | [OUTLIER\_PERCENT](/sql-reference/functions/dmf_outlier_percent) | Determine what percentage of values in a numeric column fall outside the asymmetric Tukey fences for the column. |
|  | [OUTLIER\_ZSCORE\_COUNT](/sql-reference/functions/dmf_outlier_zscore_count) | Determine how many values in a numeric column have a Z-score greater than 3. |
|  | [OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_outlier_zscore_percent) | Determine what percentage of values in a numeric column have a Z-score greater than 3. |
|  | [STDDEV](/sql-reference/functions/dmf_stddev) | Determine the standard deviation value for a column. |
|  | [STRING\_LENGTH\_AVG](/sql-reference/functions/dmf_string_length_avg) | Determine the average string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_MAX](/sql-reference/functions/dmf_string_length_max) | Determine the maximum string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_MIN](/sql-reference/functions/dmf_string_length_min) | Determine the minimum string length of non-NULL values for a string column. |
|  | [VARIANCE](/sql-reference/functions/dmf_variance) | Determine the variance value for a numeric column. |
| Uniqueness | [ACCEPTED\_VALUES](/sql-reference/functions/dmf_accepted_values) | Determine whether values in a column match a Boolean expression. |
|  | [DUPLICATE\_COUNT](/sql-reference/functions/dmf_duplicate_count) | Determine the number of duplicate values in a column, including NULL values. |
|  | [UNIQUE\_COUNT](/sql-reference/functions/dmf_unique_count) | Determine the number of unique, non-NULL values in a column. |
| Volume | [ROW\_COUNT](/sql-reference/functions/dmf_row_count) | Determine how many records are in the table or view. |

Expand

Show lessSee more
