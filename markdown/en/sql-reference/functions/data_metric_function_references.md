Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DATA\_METRIC\_FUNCTION\_REFERENCES

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns a row for each object that has the specified data metric function assigned to the object or returns a row for each data
metric function assigned to the specified object.

See also:
:   [DATA\_METRIC\_FUNCTION\_REFERENCES view](/sql-reference/account-usage/data_metric_function_references) (Account Usage view)

## Syntax

Copy code

```
DATA_METRIC_FUNCTION_REFERENCES(
  METRIC_NAME => '<string>' )

DATA_METRIC_FUNCTION_REFERENCES(
  REF_ENTITY_NAME => '<string>' ,
  REF_ENTITY_DOMAIN => '<string>'
  )
```

## Arguments

`METRIC_NAME => 'string'`
:   Specifies the name of the data metric function.

    - The entire data metric name must be enclosed in single quotes.
    - If the data metric name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes, such as `'"<metric_name>"'`.

`REF_ENTITY_NAME => 'string'`
:   The name of the object, such as `table_name`, `view_name`, or `external_table_name`, on which the data metric function is added.

    - The entire object name must be enclosed in single quotes.
    - If the object name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes, such as `'"<table_name>"'`.

`REF_ENTITY_DOMAIN => 'string'`
:   The object type, such as table or materialized view, on which the data metric function is added.

    Use `'TABLE'` for all [supported table types](/user-guide/data-quality-intro#label-data-quality-supported-tables).

## Returns

The function returns the following columns:

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
| `schedule_status` | VARCHAR | The status of the metrics association. One of the following:  `STARTED`  The data metric association on the table or view is scheduled to run.  `STARTED_AND_PENDING_SCHEDULE_UPDATE`  A change to the data metric schedule occurred and the new schedule is not yet effective. Allow Snowflake to update the schedule and synchronize the schedule with the data metric function. This value is temporary until the updates are complete.  If you unset the schedule with an ALTER TABLE or ALTER VIEW command, this value remains until a new schedule is set.  `SUSPENDED`  The data metric association on the table or view is not scheduled to run. This value also occurs when the role in use that calls the function does not have the OWNERSHIP privilege on the table.  For a full list of possible values, see [Usage notes: Suspended statuses](#label-data-metric-function-references-usage-notes-suspended). |
| `data_quality_notification_status` | VARCHAR | Indicates whether notifications are being sent when there is an expectation violation or an anomaly in data quality. Possible values are:   - `ENABLED` — Notifications are turned on for the database that contains the object *and* no one has turned off notifications   at the object level. - `DISABLED` — Notifications aren’t being sent for data quality issues uncovered by the DMF. - `ERROR_INSUFFICIENT_PRIVILEGE` — Notifications aren’t being sent because the database owner doesn’t have the required   privileges. For a list of the required privileges, see [Grant privileges](/user-guide/data-quality-notifications#label-data-quality-notifications-grant). |
| `anomaly_detection_status` | VARCHAR | Indicates whether [anomaly detection](/user-guide/data-quality-anomaly) is enabled for the association between the DMF and the object. If the value is `TRAINING_IN_PROGRESS`, see [About the training period](/user-guide/data-quality-anomaly#label-data-quality-anomaly-training-period). |
| `anomaly_detection_sensitivity_level` | VARCHAR | The sensitivity level of anomaly detection. For more information, see [Adjust the sensitivity level of anomaly detection](/user-guide/data-quality-anomaly#label-data-quality-anomaly-sensitivity-level). |
| `use_role` | VARCHAR | Access control role with which the DMF runs. For more information, see [Required privilege on the table or view](/user-guide/data-quality-access-control#label-data-quality-access-control-object-privilege). |
| `level` | VARCHAR | The level at which the DMF is associated with the object. Possible values are:   - `TABLE` — The DMF was associated directly with the object. - `SCHEMA` — The DMF was added to the schema, which created the association with the object. For more information, see   [Monitor the data quality of a schema](/user-guide/data-quality-schema-level). |
| `exclude_table_types` | VARCHAR | When a DMF is added at the schema level, this column shows which object types are excluded from the association. For more information, see [Monitor the data quality of a schema](/user-guide/data-quality-schema-level). |
| `properties` | VARIANT | Additional configuration for the DMF association, encoded as a JSON object. The object always includes the following keys, with NULL where the value isn’t set:   - `level` — `TABLE` or `SCHEMA`. Indicates whether the DMF is associated at the table or schema level. - `exclude_table_types` — For a schema-level association, a comma-separated string of table types excluded from the   association (for example, `"VIEW, EXTERNAL_TABLE"`). NULL for table-level associations. - `use_role` — The access control role used to run the DMF, or NULL if the default is used. - `anomaly_detection_status` — The anomaly detection state for the association, or NULL if anomaly detection isn’t configured. - `anomaly_detection_sensitivity_level` — The configured sensitivity level for anomaly detection, or NULL if not set. - `data_quality_notification_status` — The notification state for the association, or NULL if notifications aren’t configured. - `within_group` — A JSON-encoded string representing the array of column references used in the WITHIN GROUP clause, in the   format `"[{\"domain\":\"COLUMN\",\"id\":\"<id>\",\"name\":\"<col_name>\"}]"`. NULL if no grouping is configured. To get a parsed   array, apply `PARSE_JSON()` to the value. - `group_limit` — The maximum number of groups allowed per evaluation, or NULL if no grouping is configured. - `filter` — The filter predicate stored as a string, exactly as it was specified in the ADD DATA METRIC FUNCTION statement   (for example, `"status = 'ACTIVE'"`). NULL if no filter is configured. For more information about FILTER, see   [Apply data quality checks to a subset of rows](/user-guide/data-quality-filter).   Several of these keys mirror values that are also exposed as their own top-level columns in the function output (for example, `use_role`, `anomaly_detection_status`, `anomaly_detection_sensitivity_level`, and `data_quality_notification_status`).  For more information about WITHIN GROUP, see [Apply data quality checks by group](/user-guide/data-quality-group-by). |

Expand

Show lessSee more

## Access control requirements

Results are returned based on the privileges granted to the role executing the query.

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

- Any supported privilege on the data metric function.

  - For system DMFs, the role can be granted the DATA\_METRIC\_USER database role.
- The SELECT privilege on the table or view.

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function must
  use the fully-qualified object name. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).
- Choose one syntax variation to execute a query. Mixing arguments results in errors and query failure.

  The argument values for `REF_ENTITY_NAME` and `REF_ENTITY_DOMAIN` must be included together otherwise the query fails.
- Snowflake returns errors if the specified object name does not exist or if the query operator is not authorized to view any data metric
  function on the object. Snowflake can return a result set of data metric associations if the operator is allowed to view a subset of the
  data metric associations.
- Unsupported object types listed as the `REF_ENTITY_DOMAIN`, such as `'stream'`, return errors.

## Usage notes: Suspended statuses

When the DMF association is suspended, the status can be one of the following:

`SUSPENDED_TABLE_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`
:   One of the following:

    - The table is dropped.
    - The schema or database that contains the table is dropped.
    - The schema or database that contains the table cannot be resolved by the table owner role.

      “Resolved” means the role that calls the function does not have the appropriate privileges on the schema or database that
      contains the table.

`SUSPENDED_DATA_METRIC_FUNCTION_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`
:   One of the following:

    - The DMF is dropped.
    - The schema or database that contains the DMF is dropped.
    - The schema or database that contains the DMF cannot be resolved by the table owner role.

`SUSPENDED_TABLE_COLUMN_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`
:   One of the following:

    - The target table column is dropped.
    - The schema or database that contains the column is dropped.
    - The schema or database that contains the column cannot be resolved by the table owner role.

`SUSPENDED_INSUFFICIENT_PRIVILEGE_TO_EXECUTE_DATA_METRIC_FUNCTION`
:   The table owner role does not have the EXECUTE DATA METRIC FUNCTION privilege.

`SUSPENDED_ACTIVE_EVENT_TABLE_DOES_NOT_EXIST_OR_NOT_AUTHORIZED`
:   The event table is not set at the account level.

## Examples

To return a row for each DMF assigned to the table named `hr.tables.empl_info`, execute the following:

> Copy code
>
> ```
> USE DATABASE governance;
> USE SCHEMA INFORMATION_SCHEMA;
> SELECT *
>   FROM TABLE(
>     INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
>       REF_ENTITY_NAME => 'hr.tables.empl_info',
>       REF_ENTITY_DOMAIN => 'table'
>     )
>   );
> ```

To return a row for each object (table or view) that has the DMF named `count_positive_numbers` set on that table or
view, execute the following:

> Copy code
>
> ```
> USE DATABASE governance;
> USE SCHEMA INFORMATION_SCHEMA;
> SELECT *
>   FROM TABLE(
>     INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
>       METRIC_NAME => 'governance.dmfs.count_positive_numbers'
>     )
>   );
> ```
