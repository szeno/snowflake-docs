Schema:
:   [LOCAL](/sql-reference/local)

# AUTOMATIC\_DATA\_QUALITY\_MONITORING\_RESULTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This view displays the results of automatic data quality monitoring, which uses [anomaly detection](/user-guide/data-quality-anomaly)
to evaluate metrics such as row count and freshness for tables in your account. Each row represents the evaluation of a single metric
for a monitored table on a given evaluation date, and includes the observed value, the forecasted value and expected range, and whether
the observed value was flagged as an anomaly.

The view returns one row per table, metric, and evaluation date for the most recent evaluation, restricted to your account.

Snowflake automatically selects a set of popular tables in your account to monitor, based on recent query activity and related usage
signals such as how often tables are read and how frequently they change. For each selected table, Snowflake evaluates metrics such as
row count and freshness and writes the anomaly verdicts to this view.

Automatic monitoring is computed by Snowflake and does not incur compute charges to your account. Billing applies only when a data
metric function (DMF) that you configure explicitly runs on a scheduled object.

## Columns

The columns in the view are defined as follows:

| Column name | Data type | Description |
| --- | --- | --- |
| `MEASUREMENT_TIME` | TIMESTAMP\_LTZ | The time at which the monitoring job produced this result. |
| `EVALUATION_DATE` | DATE | The date for which the metric was evaluated. |
| `TABLE_ID` | NUMBER | Internal/system-generated identifier of the monitored table. |
| `TABLE_NAME` | VARCHAR | Name of the monitored table. |
| `TABLE_SCHEMA` | VARCHAR | Name of the schema that contains the monitored table. |
| `TABLE_DATABASE` | VARCHAR | Name of the database that contains the monitored table. |
| `METRIC_NAME` | VARCHAR | Name of the metric that was evaluated, such as `ROW_COUNT` or `FRESHNESS`. |
| `VALUE` | FLOAT | The observed (actual) value of the metric. |
| `FORECAST` | FLOAT | The value forecasted for the metric by the anomaly detector. |
| `LOWER_BOUND` | FLOAT | Lower bound of the expected range for the metric value. |
| `UPPER_BOUND` | FLOAT | Upper bound of the expected range for the metric value. |
| `IS_ANOMALY` | BOOLEAN | Whether the observed value was flagged as anomalous. |

Expand

Show lessSee more

## Access control requirements

The role used to query the view must be granted one of the following application roles:

- SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER
- SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN
