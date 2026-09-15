Schema:
:   [LOCAL](/sql-reference/local)

# DATA\_QUALITY\_MONITORING\_RESULTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This view displays a row for each result of calling a [data metric function](/user-guide/data-quality-intro) in your
account.

## Columns

The columns in the view are defined as follows:

| Column name | Data type | Description |
| --- | --- | --- |
| `scheduled_time` | TIMESTAMP\_LTZ | The time the DMF is scheduled to run based on the schedule that you set for the table or view. |
| `change_commit_time` | TIMESTAMP\_LTZ | The time the DMF trigger operation occurred, or `NULL` if the DMF is not scheduled to run by a trigger operation.  For information about the trigger operation, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule). |
| `measurement_time` | TIMESTAMP\_LTZ | The time at which the metric was evaluated. |
| `table_id` | NUMBER | Internal/system-generated identifier of the table that the DMF is associated with. |
| `table_name` | VARCHAR | Name of the table that the DMF is associated with. |
| `table_schema` | VARCHAR | Name of the schema that contains the table that the DMF is associated with. |
| `table_database` | VARCHAR | Name of the database that contains the table that the DMF is associated with. |
| `metric_id` | NUMBER | Internal/system-generated identifier of the DMF. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `metric_return_type` | VARCHAR | Return type of the DMF. |
| `argument_ids` | ARRAY | Array of the identifiers of the DMF arguments. Array elements are in the same order as the arguments. |
| `argument_types` | ARRAY | Array of the domain/type of each DMF argument. Array elements are in the same order as the arguments.  Currently only supports COLUMN type arguments. |
| `argument_names` | ARRAY | Array of the names of the DMF arguments. For column arguments, each element is the name of a column. Array elements are in the same order as the arguments. |
| `reference_id` | VARCHAR | The ID to uniquely identify the metric entity reference, known as the association ID. |
| `value` | VARIANT | The result of the DMF evaluation. |

Expand

Show lessSee more

## Access control requirements

The role used to query the view must be granted the SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER application role or the
SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN application role.
