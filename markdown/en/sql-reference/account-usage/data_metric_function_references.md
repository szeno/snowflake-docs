Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_METRIC\_FUNCTION\_REFERENCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to identify data metric function objects and their references in your account.

The view is complementary to the Information Schema table function [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references).

## Columns

The view returns the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `metric_database_name` | VARCHAR | The database that stores the data metric function. |
| `metric_schema_name` | VARCHAR | The schema that stores the data metric function. |
| `metric_name` | VARCHAR | The name of the data metric function. |
| `argument_signature` | VARCHAR | The type signature of the metrics arguments. |
| `data_type` | VARCHAR | The return data type of the data metric function. |
| `ref_database_name` | VARCHAR | The database name that contains the object on which the data metric function is added. |
| `ref_schema_name` | VARCHAR | The schema name that contains the object on which the data metric function is added. |
| `ref_entity_name` | VARCHAR | The name of the table or view on which the data metric function is set. |
| `ref_entity_domain` | VARCHAR | The object type (table, view) on which the data metric function is set. |
| `ref_arguments` | ARRAY | Identifies the reference arguments used to evaluate the rule. |
| `ref_id` | VARCHAR | A unique identifier for the association of the data metric function to the table or view. |
| `schedule` | VARCHAR | The schedule to run the data metric function on the table or view. The value for the schedule is always the most recent and effective schedule. |
| `schedule_status` | VARCHAR | The status of the metrics association. One of the following:  `STARTED`  The data metric association on the table or view is scheduled to run.  `SUSPENDED`  The data metric association on the table or view is not scheduled to run. This value also occurs when the role in use that calls the function does not have the OWNERSHIP privilege on the table.  When querying the Account Usage view, the following values are visible by default; however, when calling the table function you must use a role with the OWNERSHIP privilege on the table to see these values:  `SUSPENDED_TABLE_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`  One of the following:   - The table is dropped. - The schema or database that contains the table is dropped - The schema or database that contains the table cannot be resolved by the table owner role.   “Resolved” means the role that calls the function does not have the appropriate privileges on the schema or database that contains the table.  `SUSPENDED_DATA_METRIC_FUNCTION_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`  One of the following:   - The DMF is dropped. - The schema or database that contains the DMF is dropped. - The schema or database that contains the DMF cannot be resolved by the table owner role.  `SUSPENDED_TABLE_COLUMN_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`  One of the following:   - The target table column is dropped. - The schema or database that contains the column is dropped. - The schema or database that contains the column cannot be resolved by the table owner role.  `SUSPENDED_INSUFFICIENT_PRIVILEGE_TO_EXECUTE_DATA_METRIC_FUNCTION`  The table owner role does not have the EXECUTE DATA METRIC FUNCTION privilege.  `SUSPENDED_ACTIVE_EVENT_TABLE_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`  The event table is not set at the account level. |
| `data_quality_notification_status` | VARCHAR | Reserved for future use. |
| `anomaly_detection_status` | VARCHAR | Indicates whether [anomaly detection](/user-guide/data-quality-anomaly) is enabled for the association between the DMF and the object. If the value is `TRAINING_IN_PROGRESS`, see [About the training period](/user-guide/data-quality-anomaly#label-data-quality-anomaly-training-period). |
| `anomaly_detection_sensitivity_level` | VARCHAR | The sensitivity level of anomaly detection. For more information, see [Adjust the sensitivity level of anomaly detection](/user-guide/data-quality-anomaly#label-data-quality-anomaly-sensitivity-level). |
| `use_role` | VARCHAR | The access control role used to execute the metric function. |
| `level` | VARCHAR | The level at which the DMF is associated with the object. Possible values are:   - `TABLE` — The DMF was associated directly with the object. - `SCHEMA` — The DMF was added to the schema, which created the association with the object. For more information, see   [Monitor the data quality of a schema](/user-guide/data-quality-schema-level). |
| `exclude_table_types` | VARCHAR | When a DMF is added at the schema level, this column shows which object types are excluded from the association. For more information, see [Monitor the data quality of a schema](/user-guide/data-quality-schema-level). |
| `properties` | VARIANT | Additional configuration for the DMF association, encoded as a JSON object. The object always includes the following keys, with NULL where the value isn’t set:   - `level` — `TABLE` or `SCHEMA`. Indicates whether the DMF is associated at the table or schema level. - `exclude_table_types` — For a schema-level association, a comma-separated string of table types excluded from the   association (for example, `"VIEW, EXTERNAL_TABLE"`). NULL for table-level associations. - `use_role` — The access control role used to run the DMF, or NULL if the default is used. - `anomaly_detection_status` — The anomaly detection state for the association, or NULL if anomaly detection isn’t configured. - `anomaly_detection_sensitivity_level` — The configured sensitivity level for anomaly detection, or NULL if not set. - `data_quality_notification_status` — The notification state for the association, or NULL if notifications aren’t configured. - `within_group` — A JSON-encoded string representing the array of column references used in the WITHIN GROUP clause, in the   format `"[{\"domain\":\"COLUMN\",\"id\":\"<id>\",\"name\":\"<col_name>\"}]"`. NULL if no grouping is configured. To get a parsed   array, apply `PARSE_JSON()` to the value. - `group_limit` — The maximum number of groups allowed per evaluation, or NULL if no grouping is configured. - `filter` — The filter predicate stored as a string, exactly as it was specified in the ADD DATA METRIC FUNCTION statement   (for example, `"status = 'ACTIVE'"`). NULL if no filter is configured. For more information about FILTER, see   [Apply data quality checks to a subset of rows](/user-guide/data-quality-filter).   Several of these keys mirror values that are also exposed as their own top-level columns in this view (for example, `use_role`, `anomaly_detection_status`, `anomaly_detection_sensitivity_level`, and `data_quality_notification_status`).  For more information about WITHIN GROUP, see [Apply data quality checks by group](/user-guide/data-quality-group-by). |

Expand

Show lessSee more

## Usage notes

- Latency for the view might be up to 3 hours.
- To query this view, use a role that is granted either of these [database roles](/sql-reference/snowflake-db-roles) at a minimum:
  SNOWFLAKE.GOVERNANCE\_VIEWER or SNOWFLAKE.USAGE\_VIEWER.
