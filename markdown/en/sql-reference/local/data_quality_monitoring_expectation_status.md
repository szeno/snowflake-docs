Schema:
:   [LOCAL](/sql-reference/local)

# DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This view displays a row for every time a data metric function (DMF) with an [expectation](/user-guide/data-quality-expectations)
was run in your account.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `scheduled_time` | TIMESTAMP\_LTZ | The time the DMF is scheduled to run based on the schedule that you set for the table or view. |
| `change_commit_time` | TIMESTAMP\_LTZ | The time the DMF trigger operation occurred, or NULL if the DMF is not scheduled to run by a trigger operation.  For information about the trigger operation, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule). |
| `measurement_time` | TIMESTAMP\_LTZ | The time at which the metric was evaluated. |
| `table_id` | NUMBER | Internal/system-generated identifier of the table that is associated with the DMF. |
| `table_name` | VARCHAR | Name of the table that is associated with the DMF. |
| `table_schema` | VARCHAR | Name of the schema that contains the table that is associated with the DMF. |
| `table_database` | VARCHAR | Name of the database that contains the table that is associated with the DMF. |
| `metric_id` | NUMBER | Internal/system-generated identifier of the DMF. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `metric_return_type` | VARCHAR | Return type of the DMF. |
| `argument_ids` | ARRAY | Array of the identifiers of the DMF arguments. Array elements are in the same order as the arguments. |
| `argument_types` | ARRAY | Array of the domain/type of each argument. Array elements are in the same order as the arguments.  Currently only supports COLUMN type arguments. |
| `argument_names` | ARRAY | Array of the names of the DMF arguments. For column arguments, each element is the name of a column. Array elements are in the same order as the arguments. |
| `reference_id` | VARCHAR | The ID to uniquely identify the metric entity reference, known as the association ID. |
| `value` | VARIANT | The result of the DMF evaluation. |
| `expectation_name` | VARCHAR | Name that was given to the expectation when it was added to the association between the DMF and the object. |
| `expectation_id` | VARCHAR | System-generated identifier. |
| `expectation_expression` | VARCHAR | Boolean expression of the expectation. See [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression). |
| `expectation_violated` | BOOLEAN | If TRUE, the expectation was violated. An expectation is violated when the `expectation_expression` evaluates to FALSE.  A NULL value indicates the evaluation of the expectation failed. |

Expand

Show lessSee more

## Access control requirements

The role used to query the view must be granted one of the following application roles:

- SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER
- SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN
