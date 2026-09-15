Schema:
:   [LOCAL](/sql-reference/local)

# DATA\_QUALITY\_MONITORING\_ANOMALY\_DETECTION\_STATUS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This view displays a row for every time a data metric function (DMF) ran with [anomaly detection](/user-guide/data-quality-anomaly) enabled.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `scheduled_time` | TIMESTAMP\_LTZ | The time that the DMF is scheduled to run based on the schedule that you set for the table or view. |
| `change_commit_time` | TIMESTAMP\_LTZ | The time that the DMF trigger operation occurred, or `None` if the DMF is not scheduled to run by a trigger operation.  For information about the trigger operation, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule). |
| `measurement_time` | TIMESTAMP\_LTZ | The time at which the metric was evaluated. |
| `table_id` | NUMBER | Internal, system-generated identifier of the table that is associated with the DMF. |
| `table_name` | VARCHAR | Name of the table that is associated with the DMF. |
| `table_schema` | VARCHAR | Name of the schema name that contains the table that is associated with the DMF. |
| `table_database` | VARCHAR | Name of the database that contains the table that is associated with the DMF. |
| `metric_id` | NUMBER | Internal, system-generated identifier of the DMF. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `metric_return_type` | VARCHAR | Return type of the DMF. |
| `reference_id` | VARCHAR | The ID to uniquely identify the metric entity reference, known as the *association ID*. |
| `value` | VARIANT | The result of the DMF evaluation. |
| `is_anomaly` | BOOLEAN | If TRUE, the `value` returned by the DMF is an anomaly because it was outside the range of `upperbound` and `lowerbound`. |
| `upperbound` | NUMBER | Highest value that should be returned by the DMF based on the anomaly-detecting algorithm. Values returned by the DMF that are above this upper bound are considered anomalies. |
| `lowerbound` | NUMBER | Lowest value that should be returned by the DMF based on the anomaly-detecting algorithm. Values returned by the DMF that are below this lower bound are considered anomalies. |
| `forecast` | NUMBER | Value that the anomaly-detecting algorithm predicted would be returned by the DMF. |

Expand

Show lessSee more

## Access control requirements

The role used to query the view must be granted one of the following application roles:

- SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER
- SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN
