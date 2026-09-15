# DESCRIBE MODEL MONITOR

Displays information about a specific model monitor. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

This command displays all the information shown by the [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors) command, plus additional information. DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor),
    [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor),
    [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors),
    [DROP MODEL MONITOR](/sql-reference/sql/drop-model-monitor)

## Syntax

Copy code

```
{ DESCRIBE | DESC } MODEL MONITOR <monitor_name>
```

## Parameters

`monitor_name`
:   Specifies the identifier for the model monitor to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides model monitor properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the model monitor was created. |
| `name` | Name of the model monitor. |
| `database_name` | Database in which the model monitor is stored. |
| `schema_name` | Schema in which the model monitor is stored. |
| `warehouse_name` | Warehouse used to monitor the model. |
| `refresh_interval` | The refresh interval (target lag) for triggering refresh of the model monitor. |
| `aggregation_window` | The aggregation window for calculating metrics. |
| `model_task` | The task of the model being monitored: `TABULAR_BINARY_CLASSIFICATION`, `TABULAR_REGRESSION`, or `TABULAR_MULTI_CLASSIFICATION`. |
| `type` | The type of monitor, either `MODEL_VERSION_MONITOR` or `GATEWAY_MODEL_MONITOR`. |
| `gateway` | String representation of a JSON object containing information about the Snowflake Gateway associated with gateway model monitors. For model version monitors, the value is empty. See [Gateway JSON object specification](#gateway-json-object-specification). |
| `ground_truth` | String representation of a JSON object detailing the ground truth table for gateway model monitors, if one was specified at creation. Empty otherwise. See [Table JSON object specification](#table-json-object-specification). |
| `monitor_state` | The state of the model monitor:   - ACTIVE: The model monitor is active and operating correctly. - SUSPENDED: Model monitoring is paused. - PARTIALLY\_SUSPENDED: An error condition in which one of the underlying tables has stopped refreshing at the expected interval. See DESCRIBE for more details. - UNKNOWN: An error condition in which the state of the underlying tables cannot be identified. |
| `source` | String representation of a JSON object detailing the source table or view on which aggregations are based for model version monitors. For gateway model monitors, the value is empty. If the table does not exist or is not accessible, the value is an empty string. See [Table JSON object specification](#table-json-object-specification). |
| `baseline` | String representation of a JSON object detailing baseline table being used for monitoring, of which a clone is embedded in the model version monitor object. For gateway model monitors, the value is empty. See [Table JSON object specification](#table-json-object-specification). |
| `model` | String representation of a JSON object containing information specifically about the model being monitored. See [Model JSON object specification](#model-json-object-specification). |
| `comment` | Comment about the model monitor. |
| \*The following columns are the additional columns displayed by DESCRIBE compared to SHOW\* |  |
| `aggregation_status` | JSON object containing aggregation status for each dynamic table type.  **Keys:**   - `SOURCE_AGGREGATED` / `ACCURACY_AGGREGATED` (non-segment) - `SOURCE_AGGREGATED_<segment_column>` / `ACCURACY_AGGREGATED_<segment_column>` (segment-specific)   **Values:** `ACTIVE` or `SUSPENDED` |
| `aggregation_last_error` | JSON object containing the last error for each dynamic table type.  **Keys:** Same as `aggregation_status`  **Values:** Error message, or empty string if successful |
| `aggregation_last_data_timestamp` | JSON object containing the last update timestamp for each dynamic table type.  **Keys:** Same as `aggregation_status`  **Values:** Timestamp of last successful update |
| `columns` | A string representation of a JSON object that contains names of columns being used by the monitor. See [Column JSON object specification](#column-json-object-specification). |
| `monitor_start_time` | Earliest timestamp from which the gateway model monitor aggregates auto-captured inference logs. Empty for model version monitors. |

Expand

Show lessSee more

### Table JSON object specification

The following is the format of the JSON representation of a table, as used by the `source`, `baseline`, and `ground_truth` columns in the command output:

| `name` | Name of the source, baseline, or ground truth table or view. |
| --- | --- |
| `database_name` | Database in which the table or view is stored. |
| `schema_name` | Schema in which the table or view is stored. |
| `status` | The status of the table:   - ACTIVE: The table or view is accessible by the user. - MASKED: The current user does not have access to the table or view. Values of other fields appear masked (that is, as a series of asterisks). - DELETED: The table or view has been deleted. - NOT\_SET: The status has not been set. |

Expand

Show lessSee more

### Gateway JSON object specification

The following is the format of the JSON representation of a gateway, as used by the `gateway` column in the command output:

| Field | Description |
| --- | --- |
| `name` | Name of the gateway being monitored by a gateway model monitor. |
| `database_name` | Database in which the gateway is stored. |
| `schema_name` | Schema in which the gateway is stored. |
| `status` | The status of the gateway. Can be `ACTIVE`, `MASKED`, or `DELETED`. `MASKED` indicates that the user does not have access to the gateway; other fields show as a series of asterisks. |

Expand

Show lessSee more

### Model JSON object specification

The following is the format of the JSON representation of a model, as used by the `model` column in the command output:

| Field | Description |
| --- | --- |
| `model_name` | Name of the model being monitored. |
| `version_name` | The name of the model version being monitored. Empty for gateway model monitors because gateway monitors track the model, not a specific version. |
| `function_name` | Name of the specific function being monitored. |
| `database_name` | Database in which the model is stored. |
| `schema_name` | Schema in which the model is stored. |
| `model_status` | The status of the model. Can be ACTIVE, MASKED, or DELETED. MASKED indicates that the user does not have access to the model; other fields show as a series of asterisks. |
| `version_status` | The status of the model version being monitored. Can be ACTIVE or DELETED (MASKED is not a valid status for a model version, because they do not have access control). Empty for gateway model monitors. |

Expand

Show lessSee more

### Column JSON object specification

The following is the format of the JSON representation of columns, as used by the `columns` column in the command output:

| Field | Description |
| --- | --- |
| `timestamp_column` | Name of the timestamp column in the data source. |
| `id_columns` | An array of ID column names. For model version monitors, columns in the source data that together uniquely identify each row. For gateway model monitors, join keys in the ground truth table that match auto-captured inference logs. |
| `prediction_class_columns` | An array of strings naming all prediction class columns. |
| `prediction_score_columns` | An array of strings naming all prediction score columns. |
| `actual_class_columns` | An array of strings naming all actual class columns in the source table for model version monitors and in the ground truth table for gateway model monitors. |
| `actual_score_columns` | An array of strings naming all actual score columns in the source table for model version monitors and in the ground truth table for gateway model monitors. |
| `numerical_columns` | An array of strings naming all numerical feature columns that the model version monitor uses from the source table. Empty for gateway model monitors. |
| `string_columns` | An array of strings naming all string (categorical) feature columns that the model version monitor uses from the source table. Empty for gateway model monitors. |
| `boolean_columns` | An array of strings naming all Boolean (categorical) feature columns that the model version monitor uses from the source table. Empty for gateway model monitors. |
| `segment_columns` | An array of strings naming all segment columns in the data source. For existing model version monitors created without segments, this field will be an empty array. Empty for gateway model monitors. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | Model monitor |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.
