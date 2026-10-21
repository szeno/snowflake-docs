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

The Machine Learning DMFs compare a column of predicted values with a column of actual values, for example, to monitor the output
of a machine learning model. Specify the predicted column first when you associate one of these DMFs with a table or view.

Many count and percentage DMFs measure undesirable values, so lower values are better. Other DMFs, such as `NOT_NULL_COUNT`, measure
values that meet an expectation. The `ROWS_IN_PAST` DMFs in the Volume category count values in a trailing window that ends at the
scheduled evaluation time; a value of 0 means that no data arrived.

## System DMFs

Currently, Snowflake supports these system DMFs to measure common metrics without having to define them:

| Category | System DMF | Description |
| --- | --- | --- |
| Completeness | [ALL\_SPACE\_COUNT](/sql-reference/functions/dmf_all_space_count) | Determine how many non-NULL values in a string column are not empty but contain only whitespace. |
|  | [ALL\_SPACE\_PERCENT](/sql-reference/functions/dmf_all_space_percent) | Determine what percentage of values in a string column are not empty but contain only whitespace. |
|  | [BLANK\_COUNT](/sql-reference/functions/dmf_blank_count) | Determine how many blank values are in a column. |
|  | [BLANK\_PERCENT](/sql-reference/functions/dmf_blank_percent) | Determine what percentage of a column’s values are blank. |
|  | [EMPTY\_STRING\_COUNT](/sql-reference/functions/dmf_empty_string_count) | Determine how many empty strings are in a column. |
|  | [EMPTY\_STRING\_PERCENT](/sql-reference/functions/dmf_empty_string_percent) | Determine what percentage of a column’s values are empty strings. |
|  | [NOT\_NULL\_COUNT](/sql-reference/functions/dmf_not_null_count) | Determine how many non-NULL values are in a column. |
|  | [NOT\_NULL\_PERCENT](/sql-reference/functions/dmf_not_null_percent) | Determine what percentage of a column’s values are not NULL. |
|  | [NULL\_COUNT](/sql-reference/functions/dmf_null_count) | Determine how many NULL values are in a column. |
|  | [NULL\_KEYWORD\_COUNT](/sql-reference/functions/dmf_null_keyword_count) | Determine how many non-NULL values in a string column are a text placeholder for a missing value. |
|  | [NULL\_KEYWORD\_PERCENT](/sql-reference/functions/dmf_null_keyword_percent) | Determine what percentage of values in a string column are a text placeholder for a missing value. |
|  | [NULL\_PERCENT](/sql-reference/functions/dmf_null_percent) | Determine what percentage of a column’s values are NULL. |
| Consistency | [CASE\_FORMAT\_VIOLATION\_COUNT](/sql-reference/functions/dmf_case_format_violation_count) | Determine how many non-NULL values in a string column have inconsistent casing (not all-uppercase, all-lowercase, or title-case). |
|  | [CASE\_FORMAT\_VIOLATION\_PERCENT](/sql-reference/functions/dmf_case_format_violation_percent) | Determine what percentage of non-NULL values in a string column have inconsistent casing. |
|  | [CONTAINS\_SPACES\_COUNT](/sql-reference/functions/dmf_contains_spaces_count) | Determine how many non-NULL values in a string column contain a space, tab, or no-break space. |
|  | [CONTAINS\_SPACES\_PERCENT](/sql-reference/functions/dmf_contains_spaces_percent) | Determine what percentage of values in a string column contain a space, tab, or no-break space. |
|  | [SPECIAL\_CHARACTER\_COUNT](/sql-reference/functions/dmf_special_character_count) | Determine how many non-NULL values in a string column contain characters outside the alphanumeric range. |
|  | [SPECIAL\_CHARACTER\_PERCENT](/sql-reference/functions/dmf_special_character_percent) | Determine what percentage of non-NULL values in a string column contain characters outside the alphanumeric range. |
|  | [UNTRIMMED\_STRING\_COUNT](/sql-reference/functions/dmf_untrimmed_string_count) | Determine how many non-NULL values in a string column have leading or trailing whitespace. |
|  | [UNTRIMMED\_STRING\_PERCENT](/sql-reference/functions/dmf_untrimmed_string_percent) | Determine what percentage of non-NULL values in a string column have leading or trailing whitespace. |
| Freshness | [FRESHNESS](/sql-reference/functions/dmf_freshness) | Determine the freshness of a table’s data based on a timestamp column or the most recent [DML operation](/sql-reference/sql-dml). |
|  | [SOURCE\_TARGET\_LAG](/sql-reference/functions/dmf_source_target_lag) | Determine how far, in seconds, the latest timestamp in a target table trails the latest timestamp in a source table. |
| Machine Learning | [ACCURACY](/sql-reference/functions/dmf_accuracy) | Determine what percentage of predicted values in a column are equal to the actual values in another column. |
|  | [MAE](/sql-reference/functions/dmf_mae) | Determine the mean absolute error between a column of predicted values and a column of actual values. |
|  | [MAPE](/sql-reference/functions/dmf_mape) | Determine the mean absolute percentage error between a column of predicted values and a column of actual values. |
|  | [MEAN\_ERROR](/sql-reference/functions/dmf_mean_error) | Determine whether a column of predicted values is, on average, higher or lower than a column of actual values. |
|  | [R\_SQUARED](/sql-reference/functions/dmf_r_squared) | Determine the coefficient of determination (R²) of a column of predicted values against a column of actual values. |
|  | [RMSE](/sql-reference/functions/dmf_rmse) | Determine the root mean squared error between a column of predicted values and a column of actual values. |
| Outliers | [EXTREME\_OUTLIER\_COUNT](/sql-reference/functions/dmf_extreme_outlier_count) | Determine how many non-NULL values in a numeric column fall outside the extreme asymmetric Tukey fences for the column. |
|  | [EXTREME\_OUTLIER\_IQR\_COUNT](/sql-reference/functions/dmf_extreme_outlier_iqr_count) | Determine how many non-NULL values in a numeric column fall outside the extreme Tukey fences (3 times the interquartile range). |
|  | [EXTREME\_OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_iqr_percent) | Determine what percentage of values in a numeric column fall outside the extreme Tukey fences (3 times the interquartile range). |
|  | [EXTREME\_OUTLIER\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_percent) | Determine what percentage of values in a numeric column fall outside the extreme asymmetric Tukey fences for the column. |
|  | [EXTREME\_OUTLIER\_ZSCORE\_COUNT](/sql-reference/functions/dmf_extreme_outlier_zscore_count) | Determine how many non-NULL values in a numeric column have a Z-score greater than 4.5. |
|  | [EXTREME\_OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_extreme_outlier_zscore_percent) | Determine what percentage of values in a numeric column have a Z-score greater than 4.5. |
|  | [OUTLIER\_COUNT](/sql-reference/functions/dmf_outlier_count) | Determine how many non-NULL values in a numeric column fall outside the asymmetric Tukey fences for the column. |
|  | [OUTLIER\_IQR\_COUNT](/sql-reference/functions/dmf_outlier_iqr_count) | Determine how many non-NULL values in a numeric column fall outside the standard Tukey fences (1.5 times the interquartile range). |
|  | [OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_outlier_iqr_percent) | Determine what percentage of values in a numeric column fall outside the standard Tukey fences (1.5 times the interquartile range). |
|  | [OUTLIER\_PERCENT](/sql-reference/functions/dmf_outlier_percent) | Determine what percentage of values in a numeric column fall outside the asymmetric Tukey fences for the column. |
|  | [OUTLIER\_ZSCORE\_COUNT](/sql-reference/functions/dmf_outlier_zscore_count) | Determine how many non-NULL values in a numeric column have a Z-score greater than 3. |
|  | [OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_outlier_zscore_percent) | Determine what percentage of values in a numeric column have a Z-score greater than 3. |
| Schema | [SCHEMA\_CHANGE\_ADD\_COUNT](/sql-reference/functions/dmf_schema_change_add_count) | Count columns added between consecutive evaluations. |
|  | [SCHEMA\_CHANGE\_COUNT](/sql-reference/functions/dmf_schema_change_count) | Count schema changes (column add, drop, rename, or type change) detected between consecutive evaluations. |
|  | [SCHEMA\_CHANGE\_DROP\_COUNT](/sql-reference/functions/dmf_schema_change_drop_count) | Count columns dropped between consecutive evaluations. |
|  | [SCHEMA\_CHANGE\_TYPE\_COUNT](/sql-reference/functions/dmf_schema_change_type_count) | Count columns whose data type changed between consecutive evaluations. |
| Statistics | [APPROX\_QUANTILE\_20](/sql-reference/functions/dmf_approx_quantile_20) | Determine the approximate 20th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_25](/sql-reference/functions/dmf_approx_quantile_25) | Determine the approximate 25th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_40](/sql-reference/functions/dmf_approx_quantile_40) | Determine the approximate 40th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_50](/sql-reference/functions/dmf_approx_quantile_50) | Determine the approximate 50th percentile (median) value for a numeric column. |
|  | [APPROX\_QUANTILE\_60](/sql-reference/functions/dmf_approx_quantile_60) | Determine the approximate 60th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_80](/sql-reference/functions/dmf_approx_quantile_80) | Determine the approximate 80th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_95](/sql-reference/functions/dmf_approx_quantile_95) | Determine the approximate 95th percentile value for a numeric column. |
|  | [APPROX\_QUANTILE\_99](/sql-reference/functions/dmf_approx_quantile_99) | Determine the approximate 99th percentile value for a numeric column. |
|  | [AVG](/sql-reference/functions/dmf_avg) | Determine the average value of a column. |
|  | [FALSE\_COUNT](/sql-reference/functions/dmf_false_count) | Determine how many non-NULL values in a Boolean column are FALSE. |
|  | [FALSE\_PERCENT](/sql-reference/functions/dmf_false_percent) | Determine what percentage of values in a Boolean column are FALSE. |
|  | [GEOMETRIC\_MEAN](/sql-reference/functions/dmf_geometric_mean) | Determine the geometric mean of the positive values in a numeric column. |
|  | [HARMONIC\_MEAN](/sql-reference/functions/dmf_harmonic_mean) | Determine the harmonic mean of the nonzero values in a numeric column. |
|  | [KURTOSIS](/sql-reference/functions/dmf_kurtosis) | Determine the sample excess kurtosis of the values in a numeric column. |
|  | [MAX](/sql-reference/functions/dmf_max) | Determine the maximum value of a column. |
|  | [MEDIAN](/sql-reference/functions/dmf_median) | Determine the exact median value for a numeric column. |
|  | [MIN](/sql-reference/functions/dmf_min) | Determine the minimum value of a column. |
|  | [NEGATIVE\_COUNT](/sql-reference/functions/dmf_negative_count) | Determine how many non-NULL values in a numeric column are negative. |
|  | [NEGATIVE\_PERCENT](/sql-reference/functions/dmf_negative_percent) | Determine what percentage of values in a numeric column are negative. |
|  | [SKEW](/sql-reference/functions/dmf_skew) | Determine the sample skewness of the values in a numeric column. |
|  | [STDDEV](/sql-reference/functions/dmf_stddev) | Determine the standard deviation value for a column. |
|  | [STRING\_LENGTH\_AVG](/sql-reference/functions/dmf_string_length_avg) | Determine the average string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_MAX](/sql-reference/functions/dmf_string_length_max) | Determine the maximum string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_MIN](/sql-reference/functions/dmf_string_length_min) | Determine the minimum string length of non-NULL values for a string column. |
|  | [STRING\_LENGTH\_STDDEV](/sql-reference/functions/dmf_string_length_stddev) | Determine the sample standard deviation of the string length of non-NULL values for a string column. |
|  | [SUM](/sql-reference/functions/dmf_sum) | Determine the sum of the values in a numeric column. |
|  | [TRUE\_COUNT](/sql-reference/functions/dmf_true_count) | Determine how many non-NULL values in a Boolean column are TRUE. |
|  | [TRUE\_PERCENT](/sql-reference/functions/dmf_true_percent) | Determine what percentage of values in a Boolean column are TRUE. |
|  | [VARIANCE](/sql-reference/functions/dmf_variance) | Determine the variance value for a numeric column. |
|  | [ZERO\_COUNT](/sql-reference/functions/dmf_zero_count) | Determine how many non-NULL values in a numeric column are equal to zero. |
|  | [ZERO\_PERCENT](/sql-reference/functions/dmf_zero_percent) | Determine what percentage of values in a numeric column are equal to zero. |
| Uniqueness | [DUPLICATE\_COUNT](/sql-reference/functions/dmf_duplicate_count) | Determine the number of duplicate values in a column, including NULL values. |
|  | [DUPLICATE\_PERCENT](/sql-reference/functions/dmf_duplicate_percent) | Determine what percentage of non-NULL rows have a value that occurs more than once. |
|  | [UNIQUE\_COUNT](/sql-reference/functions/dmf_unique_count) | Determine the number of unique, non-NULL values in a column. |
|  | [UNIQUE\_PERCENT](/sql-reference/functions/dmf_unique_percent) | Determine what percentage of non-NULL rows have a value that occurs exactly once. |
| Validity | [ACCEPTED\_VALUES](/sql-reference/functions/dmf_accepted_values) | Determine whether values in a column match a Boolean expression. |
|  | [FUTURE\_TIMESTAMP\_COUNT](/sql-reference/functions/dmf_future_timestamp_count) | Determine how many non-NULL values in a date/timestamp column are in the future relative to the scheduled evaluation time. |
|  | [FUTURE\_TIMESTAMP\_PERCENT](/sql-reference/functions/dmf_future_timestamp_percent) | Determine what percentage of values in a date/timestamp column are in the future relative to the scheduled evaluation time. |
|  | [INVALID\_CA\_POSTAL\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_ca_postal_code_count) | Determine how many non-NULL values in a string column are not a valid Canadian postal code. |
|  | [INVALID\_CA\_POSTAL\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_ca_postal_code_percent) | Determine what percentage of values in a string column are not a valid Canadian postal code. |
|  | [INVALID\_CA\_SIN\_COUNT](/sql-reference/functions/dmf_invalid_ca_sin_count) | Determine how many non-NULL values in a string column are not a valid Canadian Social Insurance Number. |
|  | [INVALID\_CA\_SIN\_PERCENT](/sql-reference/functions/dmf_invalid_ca_sin_percent) | Determine what percentage of values in a string column are not a valid Canadian Social Insurance Number. |
|  | [INVALID\_CH\_OASI\_COUNT](/sql-reference/functions/dmf_invalid_ch_oasi_count) | Determine how many non-NULL values in a string column are not a valid Swiss OASI number. |
|  | [INVALID\_CH\_OASI\_PERCENT](/sql-reference/functions/dmf_invalid_ch_oasi_percent) | Determine what percentage of values in a string column are not a valid Swiss OASI number. |
|  | [INVALID\_CUSIP\_COUNT](/sql-reference/functions/dmf_invalid_cusip_count) | Determine how many non-NULL values in a string column are not a valid CUSIP. |
|  | [INVALID\_CUSIP\_PERCENT](/sql-reference/functions/dmf_invalid_cusip_percent) | Determine what percentage of values in a string column are not a valid CUSIP. |
|  | [INVALID\_DE\_POSTAL\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_de_postal_code_count) | Determine how many non-NULL values in a string column are not a valid German postal code. |
|  | [INVALID\_DE\_POSTAL\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_de_postal_code_percent) | Determine what percentage of values in a string column are not a valid German postal code. |
|  | [INVALID\_DE\_TAX\_ID\_COUNT](/sql-reference/functions/dmf_invalid_de_tax_id_count) | Determine how many non-NULL values in a string column are not a valid German tax identification number. |
|  | [INVALID\_DE\_TAX\_ID\_PERCENT](/sql-reference/functions/dmf_invalid_de_tax_id_percent) | Determine what percentage of values in a string column are not a valid German tax identification number. |
|  | [INVALID\_EMAIL\_COUNT](/sql-reference/functions/dmf_invalid_email_count) | Determine how many non-NULL values in a string column are not a valid email address. |
|  | [INVALID\_EMAIL\_PERCENT](/sql-reference/functions/dmf_invalid_email_percent) | Determine what percentage of values in a string column are not a valid email address. |
|  | [INVALID\_ES\_DNI\_COUNT](/sql-reference/functions/dmf_invalid_es_dni_count) | Determine how many non-NULL values in a string column are not a valid Spanish DNI number. |
|  | [INVALID\_ES\_DNI\_PERCENT](/sql-reference/functions/dmf_invalid_es_dni_percent) | Determine what percentage of values in a string column are not a valid Spanish DNI number. |
|  | [INVALID\_FIGI\_COUNT](/sql-reference/functions/dmf_invalid_figi_count) | Determine how many non-NULL values in a string column are not a valid FIGI. |
|  | [INVALID\_FIGI\_PERCENT](/sql-reference/functions/dmf_invalid_figi_percent) | Determine what percentage of values in a string column are not a valid FIGI. |
|  | [INVALID\_FR\_INSEE\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_fr_insee_code_count) | Determine how many non-NULL values in a string column are not a valid French INSEE commune code. |
|  | [INVALID\_FR\_INSEE\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_fr_insee_code_percent) | Determine what percentage of values in a string column are not a valid French INSEE commune code. |
|  | [INVALID\_FR\_POSTAL\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_fr_postal_code_count) | Determine how many non-NULL values in a string column are not a valid French postal code. |
|  | [INVALID\_FR\_POSTAL\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_fr_postal_code_percent) | Determine what percentage of values in a string column are not a valid French postal code. |
|  | [INVALID\_INTEGER\_COUNT](/sql-reference/functions/dmf_invalid_integer_count) | Determine how many non-NULL values in a string column are not an integer. |
|  | [INVALID\_INTEGER\_PERCENT](/sql-reference/functions/dmf_invalid_integer_percent) | Determine what percentage of values in a string column are not an integer. |
|  | [INVALID\_ISIN\_COUNT](/sql-reference/functions/dmf_invalid_isin_count) | Determine how many non-NULL values in a string column are not a valid ISIN. |
|  | [INVALID\_ISIN\_PERCENT](/sql-reference/functions/dmf_invalid_isin_percent) | Determine what percentage of values in a string column are not a valid ISIN. |
|  | [INVALID\_ISO8601\_FORMAT\_COUNT](/sql-reference/functions/dmf_invalid_iso8601_format_count) | Determine how many non-NULL values in a string column are not in ISO 8601 layout. |
|  | [INVALID\_ISO8601\_FORMAT\_PERCENT](/sql-reference/functions/dmf_invalid_iso8601_format_percent) | Determine what percentage of values in a string column are not in ISO 8601 layout. |
|  | [INVALID\_IT\_FISCAL\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_it_fiscal_code_count) | Determine how many non-NULL values in a string column are not a valid Italian fiscal code. |
|  | [INVALID\_IT\_FISCAL\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_it_fiscal_code_percent) | Determine what percentage of values in a string column are not a valid Italian fiscal code. |
|  | [INVALID\_JSON\_COUNT](/sql-reference/functions/dmf_invalid_json_count) | Determine how many non-NULL values in a string column are not valid JSON. |
|  | [INVALID\_JSON\_PERCENT](/sql-reference/functions/dmf_invalid_json_percent) | Determine what percentage of non-NULL values in a string column are not valid JSON. |
|  | [INVALID\_LATITUDE\_COUNT](/sql-reference/functions/dmf_invalid_latitude_count) | Determine how many non-NULL values in a numeric column are outside the valid latitude range (-90 to 90). |
|  | [INVALID\_LATITUDE\_PERCENT](/sql-reference/functions/dmf_invalid_latitude_percent) | Determine what percentage of values in a numeric column are outside the valid latitude range (-90 to 90). |
|  | [INVALID\_LEI\_COUNT](/sql-reference/functions/dmf_invalid_lei_count) | Determine how many non-NULL values in a string column are not a valid LEI. |
|  | [INVALID\_LEI\_PERCENT](/sql-reference/functions/dmf_invalid_lei_percent) | Determine what percentage of values in a string column are not a valid LEI. |
|  | [INVALID\_LONGITUDE\_COUNT](/sql-reference/functions/dmf_invalid_longitude_count) | Determine how many non-NULL values in a numeric column are outside the valid longitude range (-180 to 180). |
|  | [INVALID\_LONGITUDE\_PERCENT](/sql-reference/functions/dmf_invalid_longitude_percent) | Determine what percentage of values in a numeric column are outside the valid longitude range (-180 to 180). |
|  | [INVALID\_NL\_BSN\_COUNT](/sql-reference/functions/dmf_invalid_nl_bsn_count) | Determine how many non-NULL values in a string column are not a valid Dutch citizen service number. |
|  | [INVALID\_NL\_BSN\_PERCENT](/sql-reference/functions/dmf_invalid_nl_bsn_percent) | Determine what percentage of values in a string column are not a valid Dutch citizen service number. |
|  | [INVALID\_NUMERIC\_TYPE\_CAST\_COUNT](/sql-reference/functions/dmf_invalid_numeric_type_cast_count) | Determine how many non-NULL values in a string column cannot be parsed as numeric. |
|  | [INVALID\_NUMERIC\_TYPE\_CAST\_PERCENT](/sql-reference/functions/dmf_invalid_numeric_type_cast_percent) | Determine what percentage of non-NULL values in a string column cannot be parsed as numeric. |
|  | [INVALID\_PERCENTAGE\_RANGE\_COUNT](/sql-reference/functions/dmf_invalid_percentage_range_count) | Determine how many non-NULL values in a numeric column are outside the range 0 to 100. |
|  | [INVALID\_PERCENTAGE\_RANGE\_PERCENT](/sql-reference/functions/dmf_invalid_percentage_range_percent) | Determine what percentage of values in a numeric column are outside the range 0 to 100. |
|  | [INVALID\_PERM\_ID\_COUNT](/sql-reference/functions/dmf_invalid_perm_id_count) | Determine how many non-NULL values in a string column are not a valid PermID. |
|  | [INVALID\_PERM\_ID\_PERCENT](/sql-reference/functions/dmf_invalid_perm_id_percent) | Determine what percentage of values in a string column are not a valid PermID. |
|  | [INVALID\_PL\_PESEL\_COUNT](/sql-reference/functions/dmf_invalid_pl_pesel_count) | Determine how many non-NULL values in a string column are not a valid Polish PESEL number. |
|  | [INVALID\_PL\_PESEL\_PERCENT](/sql-reference/functions/dmf_invalid_pl_pesel_percent) | Determine what percentage of values in a string column are not a valid Polish PESEL number. |
|  | [INVALID\_PROBABILITY\_RANGE\_COUNT](/sql-reference/functions/dmf_invalid_probability_range_count) | Determine how many non-NULL values in a numeric column are outside the range 0 to 1. |
|  | [INVALID\_PROBABILITY\_RANGE\_PERCENT](/sql-reference/functions/dmf_invalid_probability_range_percent) | Determine what percentage of values in a numeric column are outside the range 0 to 1. |
|  | [INVALID\_SEDOL\_COUNT](/sql-reference/functions/dmf_invalid_sedol_count) | Determine how many non-NULL values in a string column are not a valid SEDOL. |
|  | [INVALID\_SEDOL\_PERCENT](/sql-reference/functions/dmf_invalid_sedol_percent) | Determine what percentage of values in a string column are not a valid SEDOL. |
|  | [INVALID\_TIMESTAMP\_STRING\_COUNT](/sql-reference/functions/dmf_invalid_timestamp_string_count) | Determine how many non-NULL values in a string column can’t be parsed as a timestamp or date. |
|  | [INVALID\_TIMESTAMP\_STRING\_PERCENT](/sql-reference/functions/dmf_invalid_timestamp_string_percent) | Determine what percentage of values in a string column can’t be parsed as a timestamp or date. |
|  | [INVALID\_TR\_ID\_NO\_COUNT](/sql-reference/functions/dmf_invalid_tr_id_no_count) | Determine how many non-NULL values in a string column are not a valid Turkish national identification number. |
|  | [INVALID\_TR\_ID\_NO\_PERCENT](/sql-reference/functions/dmf_invalid_tr_id_no_percent) | Determine what percentage of values in a string column are not a valid Turkish national identification number. |
|  | [INVALID\_UK\_NINO\_COUNT](/sql-reference/functions/dmf_invalid_uk_nino_count) | Determine how many non-NULL values in a string column are not a valid UK National Insurance number. |
|  | [INVALID\_UK\_NINO\_PERCENT](/sql-reference/functions/dmf_invalid_uk_nino_percent) | Determine what percentage of values in a string column are not a valid UK National Insurance number. |
|  | [INVALID\_UK\_POSTAL\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_uk_postal_code_count) | Determine how many non-NULL values in a string column are not a valid UK postcode. |
|  | [INVALID\_UK\_POSTAL\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_uk_postal_code_percent) | Determine what percentage of values in a string column are not a valid UK postcode. |
|  | [INVALID\_USA\_PHONE\_COUNT](/sql-reference/functions/dmf_invalid_usa_phone_count) | Determine how many non-NULL values in a string column are not a valid U.S. phone number. |
|  | [INVALID\_USA\_PHONE\_PERCENT](/sql-reference/functions/dmf_invalid_usa_phone_percent) | Determine what percentage of values in a string column are not a valid U.S. phone number. |
|  | [INVALID\_USA\_STATE\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_usa_state_code_count) | Determine how many non-NULL values in a string column are not a valid U.S. state code. |
|  | [INVALID\_USA\_STATE\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_usa_state_code_percent) | Determine what percentage of values in a string column are not a valid U.S. state code. |
|  | [INVALID\_USA\_ZIP\_CODE\_COUNT](/sql-reference/functions/dmf_invalid_usa_zip_code_count) | Determine how many non-NULL values in a string column are not a valid U.S. ZIP Code. |
|  | [INVALID\_USA\_ZIP\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_usa_zip_code_percent) | Determine what percentage of values in a string column are not a valid U.S. ZIP Code. |
|  | [INVALID\_UUID\_COUNT](/sql-reference/functions/dmf_invalid_uuid_count) | Determine how many non-NULL values in a string column are not a valid UUID. |
|  | [INVALID\_UUID\_PERCENT](/sql-reference/functions/dmf_invalid_uuid_percent) | Determine what percentage of values in a string column are not a valid UUID. |
|  | [NAN\_COUNT](/sql-reference/functions/dmf_nan_count) | Determine how many non-NULL values in a numeric or string column are NaN. |
|  | [NAN\_PERCENT](/sql-reference/functions/dmf_nan_percent) | Determine what percentage of values in a numeric or string column are NaN. |
|  | [NOT\_FRIDAY\_COUNT](/sql-reference/functions/dmf_not_friday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Friday. |
|  | [NOT\_FRIDAY\_PERCENT](/sql-reference/functions/dmf_not_friday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Friday. |
|  | [NOT\_IN\_FUTURE\_COUNT](/sql-reference/functions/dmf_not_in_future_count) | Determine how many non-NULL values in a date/timestamp column are not in the future relative to the scheduled evaluation time. |
|  | [NOT\_IN\_FUTURE\_PERCENT](/sql-reference/functions/dmf_not_in_future_percent) | Determine what percentage of values in a date/timestamp column are not in the future relative to the scheduled evaluation time. |
|  | [NOT\_MONDAY\_COUNT](/sql-reference/functions/dmf_not_monday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Monday. |
|  | [NOT\_MONDAY\_PERCENT](/sql-reference/functions/dmf_not_monday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Monday. |
|  | [NOT\_SATURDAY\_COUNT](/sql-reference/functions/dmf_not_saturday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Saturday. |
|  | [NOT\_SATURDAY\_PERCENT](/sql-reference/functions/dmf_not_saturday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Saturday. |
|  | [NOT\_SUNDAY\_COUNT](/sql-reference/functions/dmf_not_sunday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Sunday. |
|  | [NOT\_SUNDAY\_PERCENT](/sql-reference/functions/dmf_not_sunday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Sunday. |
|  | [NOT\_THURSDAY\_COUNT](/sql-reference/functions/dmf_not_thursday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Thursday. |
|  | [NOT\_THURSDAY\_PERCENT](/sql-reference/functions/dmf_not_thursday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Thursday. |
|  | [NOT\_TODAY\_COUNT](/sql-reference/functions/dmf_not_today_count) | Determine how many non-NULL values in a date/timestamp column aren’t on the date of the scheduled evaluation time. |
|  | [NOT\_TODAY\_PERCENT](/sql-reference/functions/dmf_not_today_percent) | Determine what percentage of values in a date/timestamp column aren’t on the date of the scheduled evaluation time. |
|  | [NOT\_TUESDAY\_COUNT](/sql-reference/functions/dmf_not_tuesday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Tuesday. |
|  | [NOT\_TUESDAY\_PERCENT](/sql-reference/functions/dmf_not_tuesday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Tuesday. |
|  | [NOT\_WEDNESDAY\_COUNT](/sql-reference/functions/dmf_not_wednesday_count) | Determine how many non-NULL values in a date/timestamp column don’t fall on a Wednesday. |
|  | [NOT\_WEDNESDAY\_PERCENT](/sql-reference/functions/dmf_not_wednesday_percent) | Determine what percentage of values in a date/timestamp column don’t fall on a Wednesday. |
|  | [NOT\_WEEKDAY\_COUNT](/sql-reference/functions/dmf_not_weekday_count) | Determine how many non-NULL values in a date/timestamp column fall on a Saturday or a Sunday. |
|  | [NOT\_WEEKDAY\_PERCENT](/sql-reference/functions/dmf_not_weekday_percent) | Determine what percentage of values in a date/timestamp column fall on a Saturday or a Sunday. |
|  | [NOT\_YESTERDAY\_COUNT](/sql-reference/functions/dmf_not_yesterday_count) | Determine how many non-NULL values in a date/timestamp column aren’t on the day before the date of the scheduled evaluation time. |
|  | [NOT\_YESTERDAY\_PERCENT](/sql-reference/functions/dmf_not_yesterday_percent) | Determine what percentage of values in a date/timestamp column aren’t on the day before the date of the scheduled evaluation time. |
|  | [REFERENTIAL\_INTEGRITY\_COUNT](/sql-reference/functions/dmf_referential_integrity_count) | Determine how many source rows have non-NULL column values that don’t match a row in the referenced table. |
|  | [UNIX\_ZERO\_COUNT](/sql-reference/functions/dmf_unix_zero_count) | Determine how many non-NULL values in a date/timestamp column are equal to the Unix epoch (1970-01-01). |
|  | [UNIX\_ZERO\_PERCENT](/sql-reference/functions/dmf_unix_zero_percent) | Determine what percentage of values in a date/timestamp column are equal to the Unix epoch (1970-01-01). |
| Volume | [ROW\_COUNT](/sql-reference/functions/dmf_row_count) | Determine how many records are in the table or view. |
|  | [ROWS\_IN\_PAST\_DAY\_COUNT](/sql-reference/functions/dmf_rows_in_past_day_count) | Determine how many non-NULL values in a timestamp column fall in the 24 hours before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_DAY\_PERCENT](/sql-reference/functions/dmf_rows_in_past_day_percent) | Determine what percentage of values in a timestamp column fall in the 24 hours before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_HOUR\_COUNT](/sql-reference/functions/dmf_rows_in_past_hour_count) | Determine how many non-NULL values in a timestamp column fall in the hour before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_HOUR\_PERCENT](/sql-reference/functions/dmf_rows_in_past_hour_percent) | Determine what percentage of values in a timestamp column fall in the hour before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_MONTH\_COUNT](/sql-reference/functions/dmf_rows_in_past_month_count) | Determine how many non-NULL values in a date/timestamp column fall in the 30 days before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_MONTH\_PERCENT](/sql-reference/functions/dmf_rows_in_past_month_percent) | Determine what percentage of values in a date/timestamp column fall in the 30 days before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_WEEK\_COUNT](/sql-reference/functions/dmf_rows_in_past_week_count) | Determine how many non-NULL values in a date/timestamp column fall in the 7 days before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_WEEK\_PERCENT](/sql-reference/functions/dmf_rows_in_past_week_percent) | Determine what percentage of values in a date/timestamp column fall in the 7 days before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_YEAR\_COUNT](/sql-reference/functions/dmf_rows_in_past_year_count) | Determine how many non-NULL values in a date/timestamp column fall in the 365 days before the scheduled evaluation time. |
|  | [ROWS\_IN\_PAST\_YEAR\_PERCENT](/sql-reference/functions/dmf_rows_in_past_year_percent) | Determine what percentage of values in a date/timestamp column fall in the 365 days before the scheduled evaluation time. |
|  | [TABLE\_SIZE\_BYTES](/sql-reference/functions/dmf_table_size_bytes) | Determine the logical size of a table, in bytes. |

Expand

Show lessSee more

Some system DMFs measure closely related conditions:

- `NULL_COUNT` and `NOT_NULL_COUNT` are complements: together they count every row. The same is true of `NULL_PERCENT` and `NOT_NULL_PERCENT`.
- `BLANK_COUNT` counts values that are empty or contain only spaces, such as `''` and `' '`. `EMPTY_STRING_COUNT` counts only the empty
  string `''`. Neither function counts `NULL` values.
- `FUTURE_TIMESTAMP_COUNT` counts values that are later than the scheduled evaluation time, and `NOT_IN_FUTURE_COUNT` counts values that
  are at or before it. Neither function counts `NULL` values, so together they count every non-`NULL` value.
- `DUPLICATE_PERCENT` returns the percentage of non-`NULL` rows whose value occurs more than once, and `UNIQUE_PERCENT` returns the percentage
  whose value occurs exactly once. Both exclude `NULL` values, so together they add up to 100 when the column has a non-`NULL` value.
- `ALL_SPACE_COUNT` counts non-empty values that contain only whitespace, including tabs, line breaks, and no-break spaces. Unlike
  `BLANK_COUNT`, it doesn’t count the empty string `''`.
- `CONTAINS_SPACES_COUNT` counts values that contain a space, tab, or no-break space anywhere, and `UNTRIMMED_STRING_COUNT` counts only
  values with leading or trailing whitespace.
- `INVALID_ISO8601_FORMAT_COUNT` checks only the layout of a value, and `INVALID_TIMESTAMP_STRING_COUNT` checks whether the value can be
  parsed as a timestamp. For example, `2026-13-45` has a valid ISO 8601 layout but can’t be parsed.
- `INVALID_INTEGER_COUNT` counts values that aren’t written as a integer, and `INVALID_NUMERIC_TYPE_CAST_COUNT` counts values that
  can’t be cast to a number. For example, `3.7` is counted by `INVALID_INTEGER_COUNT` but not by `INVALID_NUMERIC_TYPE_CAST_COUNT`.
- `TRUE_PERCENT`, `FALSE_PERCENT`, and `NULL_PERCENT` add up to 100 for a Boolean column that has at least one row.
- `SCHEMA_CHANGE_ADD_COUNT`, `SCHEMA_CHANGE_DROP_COUNT`, and `SCHEMA_CHANGE_TYPE_COUNT` each count one kind of change that
  `SCHEMA_CHANGE_COUNT` also counts. Renamed columns are counted only by `SCHEMA_CHANGE_COUNT`.
- `FRESHNESS` measures how long ago a single table was last updated, and `SOURCE_TARGET_LAG` measures how far the latest timestamp in a
  target table trails the latest timestamp in a source table.

## Related functions

[DATA\_METRIC\_SCHEDULED\_TIME](/sql-reference/functions/dmf_data_metric_schedule_time) isn’t a metric and you can’t associate it with a table
or view. Call it in the body of a [custom DMF](/user-guide/data-quality-custom-dmfs) to retrieve the scheduled evaluation time, for example
to define a custom freshness metric.
