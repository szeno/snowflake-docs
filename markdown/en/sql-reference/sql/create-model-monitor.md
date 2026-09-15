# CREATE MODEL MONITOR

Create or replace a model monitor in the current or specified schema. Snowflake currently supports two types of model monitors. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

See also:
:   [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor),
    [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors),
    [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor),
    [DROP MODEL MONITOR](/sql-reference/sql/drop-model-monitor)

## Syntax

### Model version monitor

Copy code

```
CREATE [ OR REPLACE ] MODEL MONITOR [ IF NOT EXISTS ] <monitor_name> WITH
    MODEL = <model_name>
    VERSION = '<version_name>'
    FUNCTION = '<function_name>'
    SOURCE = <source_name>
    WAREHOUSE = <warehouse_name>
    REFRESH_INTERVAL = '<num> { seconds | minutes | hours | days }'
    AGGREGATION_WINDOW = '<num> days'
    TIMESTAMP_COLUMN = <timestamp_name>
    [ BASELINE = <baseline_name> ]
    [ ID_COLUMNS = <id_column_name_array> ]
    [ PREDICTION_CLASS_COLUMNS = <prediction_class_column_name_array> ]
    [ PREDICTION_SCORE_COLUMNS = <prediction_column-name_array> ]
    [ ACTUAL_CLASS_COLUMNS = <actual_class_column_name_array> ]
    [ ACTUAL_SCORE_COLUMNS = <actual_column_name_array> ]
    [ SEGMENT_COLUMNS = <segment_column_name_array> ]
    [ CUSTOM_METRIC_COLUMNS = <custom_metric_column_name_array> ]
    [ COMMENT = '<string_literal>' ]
```

### Gateway model monitor

Copy code

```
CREATE [ OR REPLACE ] MODEL MONITOR [ IF NOT EXISTS ] <monitor_name> WITH
    MODEL = <model_name>
    GATEWAY = <gateway_name>
    FUNCTION = '<function_name>'
    WAREHOUSE = <warehouse_name>
    REFRESH_INTERVAL = '<num> { seconds | minutes | hours | days }'
    AGGREGATION_WINDOW = '<num> { hours | days }'
    [ GROUND_TRUTH = <ground_truth_table> ]
    [ ID_COLUMNS = <id_column_name_array> ]
    [ PREDICTION_CLASS_COLUMNS = <prediction_class_column_name_array> ]
    [ PREDICTION_SCORE_COLUMNS = <prediction_score_column_name_array> ]
    [ ACTUAL_CLASS_COLUMNS = <actual_class_column_name_array> ]
    [ ACTUAL_SCORE_COLUMNS = <actual_score_column_name_array> ]
    [ COMMENT = '<string_literal>' ]
```

## Required parameters

### All monitor types

`monitor_name`
:   Specifies the identifier for the model monitor; must be unique in the schema where the monitor is created.

    If the monitor identifier is not fully qualified (in the form of `db_name.schema_name.name` or
    `schema_name.name`), the command creates the model in the current schema for the session.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`MODEL = model_name`
:   The name of the model to be monitored.

`FUNCTION = 'function_name'`
:   The name of the model function to monitor.
    For model version monitors, must be a function in the specified model version.
    For gateway model monitors, must match a function exposed by each active inference service behind the gateway that backs the specified model.

`WAREHOUSE = warehouse_name`
:   The name of the Snowflake warehouse to use for the monitor’s internal compute operations.

`REFRESH_INTERVAL = 'num { seconds | minutes | hours | days }'`
:   The interval at which the monitor refreshes its internal state. The value must be a string representing a time period,
    such as `'1 day'`. The minimum refresh interval is `'60 seconds'`. Supported units include seconds, minutes, hours, and days.
    You may use singular (“hour”) or plural (“hours”) for the interval name.

`AGGREGATION_WINDOW = 'num { hours | days }'`
:   The window over which the monitor aggregates data. The value must be a string representing a time period, such as `'1 day'`.
    For model version monitors, only days are supported. For gateway model monitors, both **hours** and **days** are supported.
    You may use singular (“day”) or plural (“days”) for the interval name.

### Model version monitor

`VERSION = 'version_name'`
:   Name of the model version to be monitored.

`SOURCE = source_name`
:   Name of the source table or view that contains the feature, inferences and ground truth labels.

`TIMESTAMP_COLUMN = timestamp_name`
:   Name of the column in the source data that contains the timestamps. Must be of type TIMESTAMP\_NTZ.

### Gateway model monitor

`GATEWAY = gateway_name`
:   Name of the Snowflake Gateway whose routed inference services you want to monitor.

## Optional parameters

### All monitor types

`COMMENT = 'string_literal'`
:   Specifies a comment for the model monitor.

`ID_COLUMNS = id_column_name_array`
:   An array of string column names that, together, uniquely identify each row in the source data. See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).

    For gateway model monitors, specify `ID_COLUMNS` and `GROUND_TRUTH` together to enable performance metrics monitoring, or omit both.
    The column names must match the field names listed in [`extra_columns`](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference#label-extra-columns) in inference requests to join the ground truth table with the auto-captured inference logs.

Note for prediction and actual columns

Model version monitors

- At least one prediction column (either a prediction score or a prediction class) is mandatory.

Gateway model monitors

- On a single-output model, Snowflake infers prediction columns from auto-captured inference logs when you omit them.
- When you specify `GROUND_TRUTH`, Snowflake infers actual columns from the ground truth table when you omit them.
- On a multi-output model, you must specify prediction and actual columns explicitly.

Rules by model task

- Binary classification: Predictions can be either scores or classes; actuals must be classes.
- Multi-class classification: Predictions and actuals must be classes.
- Regression: Both predictions and actuals must be numbers.

`PREDICTION_CLASS_COLUMNS = prediction_class_column_name_array`
:   An array of strings naming all prediction class columns in the SOURCE for model version monitors
    and output feature names in auto-captured inference logs for gateway model monitors.
    See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).

    If the model task is `TABULAR_BINARY_CLASSIFICATION` or `TABULAR_REGRESSION`, the columns must be of type NUMBER.
    If the model task is `TABULAR_MULTI_CLASSIFICATION`, the columns must be of type STRING.

`PREDICTION_SCORE_COLUMNS = prediction_column_name_array`
:   An array of strings naming all prediction score columns in the SOURCE for model version monitors
    and output feature names in auto-captured inference logs for gateway model monitors.
    See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).
    Columns must be of type NUMBER.

`ACTUAL_CLASS_COLUMNS = actual_class_column_name_array`
:   An array of strings naming all actual class columns in the SOURCE for model version monitors
    and in the GROUND\_TRUTH for gateway model monitors.
    See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).

    If the model task is `TABULAR_BINARY_CLASSIFICATION` or `TABULAR_REGRESSION`, the columns must be of type NUMBER.
    If the model task is `TABULAR_MULTI_CLASSIFICATION`, the columns must be of type STRING.

`ACTUAL_SCORE_COLUMNS = actual_column_name_array`
:   An array of strings naming all actual score columns in the SOURCE for model version monitors
    and in the GROUND\_TRUTH for gateway model monitors.
    See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).
    Columns must be of type NUMBER.

### Model version monitor

`BASELINE = baseline_name`
:   Name of the baseline table that contains a snapshot of data similar to SOURCE, which is used to compute drift.
    A snapshot of this data is embedded within the monitor object. Although this parameter is optional, if it is not set, the
    monitor cannot detect drift.

`SEGMENT_COLUMNS = segment_column_name_array`
:   An array of strings naming all segment columns in the data source. See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).
    Segment columns must be of type STRING in source data.
    You can specify up to 5 segment columns per monitor. Each segment column should have fewer than 25 unique values for optimal
    performance.
    For more information about segments, see [ML Observability: Monitoring model behavior over time](/developer-guide/snowflake-ml/model-registry/model-observability).

`CUSTOM_METRIC_COLUMNS = custom_metric_column_name_array`
:   An array of strings naming columns in the source data that are used for custom metrics. These columns are not treated as features.
    See [ARRAY constants](/sql-reference/data-types-semistructured#label-array-constant).
    Columns must be of type NUMBER.

### Gateway model monitor

`GROUND_TRUTH = ground_truth_table`
:   Name of the ground truth table that contains labels for performance metrics on a gateway model monitor.
    The table must include every column in ID\_COLUMNS (type STRING) and exactly one additional column for
    the actual label or score, unless you specify ACTUAL\_CLASS\_COLUMNS or ACTUAL\_SCORE\_COLUMNS explicitly.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

### Model version monitor

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Model monitor | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| CREATE MODEL MONITOR | Schema |  |
| SELECT | Table or view specified by the SOURCE parameter |  |
| USAGE | Warehouse specified by the WAREHOUSE parameter |  |
| USAGE | Model specified by the MODEL parameter |  |

Expand

Show lessSee more

### Gateway model monitor

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Model monitor | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| CREATE MODEL MONITOR | Schema |  |
| SELECT | Table specified by the GROUND\_TRUTH parameter |  |
| USAGE | Warehouse specified by the WAREHOUSE parameter |  |
| OWNERSHIP | Model specified by the MODEL parameter |  |
| USAGE | Gateway specified by the GATEWAY parameter |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The following requirements apply to the parameters:

  - You cannot specify both `VERSION` and `GATEWAY` in the same statement; specify one to indicate the monitor type.
  - Model task must be `tabular_binary_classification`, `tabular_regression`, or `tabular_multi_classification`.
  - Multiple-output models are not currently supported. Although the prediction and actual columns are arrays, the arrays must have at most one
    element.
  - A column may be specified once across all parameters (for example, an ID column cannot also be a prediction column).
  - For model version monitors:
    - At least one of the prediction columns must be specified.
    - Actual columns are optional, but accuracy metrics are not computed if they are not specified.
  - For gateway model monitors:
    - Prediction columns may be omitted on single-output models, but at least one prediction column must be specified for multi-output models.
    - Ground truth and ID columns are optional, but accuracy metrics are not computed if they are not specified.
    - Actual columns may be omitted when the ground truth table has a single non-ID column, but must be specified when there are multiple non-ID columns.
    - You can create multiple monitors for the same model, gateway, and function combination. Each monitor name must still be unique in the schema.
- Additional gateway model monitor requirements:

  - At least one active service that backs the model must be included in the gateway.
  - A representative service will be selected by the order of the endpoint list in the gateway to infer the model task and columns.
  - Every service behind the gateway must have the same output feature name for the monitored function, or metrics may be incomplete or incorrect.
    Input feature names may differ.
- The number of monitored features is limited to 500.
- Segment column requirements:

  - Segment columns must be of type STRING.
  - A maximum of 5 segment columns per monitor (hard limit).
  - Each segment column should have fewer than 25 unique values (recommended limit).
  - Segment values are case sensitive and special characters are not supported for segment queries.
- The basic configuration of MODEL MONITOR instances, including the model it monitors and source table or ground truth table it uses, cannot be
  changed after the monitor is created. You can modify only a few options using
  [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor). To change a monitor’s configuration, drop the instance and create a new
  one.
- [Replication](/user-guide/account-replication-intro) is supported only for instances
  of the [CUSTOM\_CLASSIFIER](/sql-reference/classes/custom_classifier) class.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

### Model version monitor

**Basic example**

Create a model version monitor that refreshes daily and uses single prediction and actual score columns.

Copy code

```
CREATE MODEL MONITOR my_monitor WITH
    MODEL = my_model
    VERSION = 'v1'
    FUNCTION = 'predict'
    SOURCE = mydb.myschema.scoring_data
    WAREHOUSE = compute_wh
    REFRESH_INTERVAL = '1 day'
    AGGREGATION_WINDOW = '1 day'
    TIMESTAMP_COLUMN = event_time
    PREDICTION_SCORE_COLUMNS = ( 'prediction_score' )
    ACTUAL_SCORE_COLUMNS = ( 'actual_score' );
```

**Example with CUSTOM\_METRIC\_COLUMNS**

Specify custom numeric columns to compute additional bespoke metrics.

Copy code

```
CREATE MODEL MONITOR my_monitor_custom WITH
    MODEL = my_model
    VERSION = 'v1'
    FUNCTION = 'predict'
    SOURCE = mydb.myschema.scoring_data
    WAREHOUSE = compute_wh
    REFRESH_INTERVAL = '1 day'
    AGGREGATION_WINDOW = '1 day'
    TIMESTAMP_COLUMN = event_time
    PREDICTION_SCORE_COLUMNS = ( 'prediction_score' )
    ACTUAL_SCORE_COLUMNS = ( 'actual_score' )
    CUSTOM_METRIC_COLUMNS = ( 'latency_ms', 'num_impressions' );
```

In this example, we include two custom metrics: `latency_ms` and `num_impressions`.
These are columns in the source data that are not features to the model, but are useful to track next to the model’s
performance.

### Gateway model monitor

**Basic example**

Create a gateway model monitor that aggregates metrics every hour and uses the inferred prediction and actual columns.

Copy code

```
CREATE MODEL MONITOR my_monitor_inferred WITH
    MODEL = my_model
    GATEWAY = my_gateway
    FUNCTION = 'predict'
    WAREHOUSE = compute_wh
    REFRESH_INTERVAL = '1 minute'
    AGGREGATION_WINDOW = '1 hour'
    GROUND_TRUTH = mydb.myschema.ground_truth_data
    ID_COLUMNS = ( 'request_id' );
```

**Example with explicit columns**

Specify prediction and actual columns for a multi-output model.

Copy code

```
CREATE MODEL MONITOR my_monitor_explicit WITH
    MODEL = my_model
    GATEWAY = my_gateway
    FUNCTION = 'predict'
    WAREHOUSE = compute_wh
    REFRESH_INTERVAL = '1 minute'
    AGGREGATION_WINDOW = '1 hour'
    GROUND_TRUTH = mydb.myschema.ground_truth_data
    ID_COLUMNS = ( 'request_id' )
    PREDICTION_SCORE_COLUMNS = ( 'prediction_score' )
    ACTUAL_SCORE_COLUMNS = ( 'actual_score' );
```
