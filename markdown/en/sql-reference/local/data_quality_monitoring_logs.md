Schema:
:   [LOCAL](/sql-reference/local)

# DATA\_QUALITY\_MONITORING\_LOGS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This view displays a row for each structured log event emitted by a [data metric function](/user-guide/data-quality-intro)
that produces per-event detail in addition to its aggregate result. The row’s `value` column holds the event payload as a
VARIANT; the keys in that payload depend on the row’s `signal_type`.

The aggregate result of the DMF evaluation is written to
[DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results). The log rows in this view are
correlated with that aggregate result by the `run_id` column.

## Columns

The columns in the view are defined as follows:

| Column name | Data type | Description |
| --- | --- | --- |
| `scheduled_time` | TIMESTAMP\_LTZ | The time the DMF is scheduled to run based on the schedule that you set for the table or view. |
| `change_commit_time` | TIMESTAMP\_LTZ | The time the DMF trigger operation occurred, or `None` if the DMF is not scheduled to run by a trigger operation.  For information about the trigger operation, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule). |
| `measurement_time` | TIMESTAMP\_LTZ | The time at which the metric was evaluated. |
| `table_id` | NUMBER | Internal/system-generated identifier of the table that the DMF is associated with. |
| `table_name` | VARCHAR | Name of the table that the DMF is associated with. |
| `table_schema` | VARCHAR | Name of the schema that contains the table that the DMF is associated with. |
| `table_database` | VARCHAR | Name of the database that contains the table that the DMF is associated with. |
| `metric_id` | NUMBER | Internal/system-generated identifier of the DMF. |
| `metric_name` | VARCHAR | Name of the DMF that emitted the log row. For schema drift, this is `SCHEMA_CHANGE_COUNT`. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `reference_id` | VARCHAR | The ID that uniquely identifies the metric entity reference, known as the association ID. |
| `run_id` | VARCHAR | Identifier that correlates this log row with the aggregate row written to [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) for the same evaluation. |
| `signal_type` | VARCHAR | The category of the log row. Currently `SCHEMA_DRIFT`. |
| `value` | VARIANT | Per-change payload. The keys in this object depend on `signal_type`. For `SCHEMA_DRIFT` rows, the keys are described in the next table. |

Expand

Show lessSee more

For `SCHEMA_DRIFT` rows, the `value` VARIANT contains the following keys:

| Key | Data type | Description |
| --- | --- | --- |
| `snow.data_metric.schema_change.change_type` | VARCHAR | One of `ADD`, `DROP`, `RENAME`, or `TYPE_CHANGE`. |
| `snow.data_metric.schema_change.column_id` | NUMBER | Internal/system-generated identifier of the column the change applies to. |
| `snow.data_metric.schema_change.column_ordinal` | NUMBER | 1-based ordinal position of the column in the table. |
| `snow.data_metric.schema_change.column_name` | VARCHAR | Current name of the column after the change. |
| `snow.data_metric.schema_change.data_type` | VARCHAR | JSON-encoded descriptor of the column’s current data type. |
| `snow.data_metric.schema_change.old_column_name` | VARCHAR | Previous column name. Populated only when `change_type` is `RENAME`. |
| `snow.data_metric.schema_change.new_column_name` | VARCHAR | New column name. Populated only when `change_type` is `RENAME`. |
| `snow.data_metric.schema_change.old_data_type` | VARCHAR | JSON-encoded descriptor of the previous data type. Populated only when `change_type` is `TYPE_CHANGE`. |
| `snow.data_metric.schema_change.new_data_type` | VARCHAR | JSON-encoded descriptor of the new data type. Populated only when `change_type` is `TYPE_CHANGE`. |

Expand

Show lessSee more

## Access control requirements

The role used to query the view must be granted the SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER application role or the
SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN application role.
