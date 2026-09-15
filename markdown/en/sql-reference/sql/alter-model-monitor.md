# ALTER MODEL MONITOR

Modifies the properties of a model monitor. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

For all monitor types:

- Suspends or resumes the monitor.
- Sets the refresh interval for dynamic table operations within the monitor.
- Sets the warehouse the monitor uses.
- Sets or unsets a comment on the monitor.

For model version monitors only:

- Sets or unsets the baseline table the monitor uses.
- Adds or removes segment columns for monitoring specific data segments.

See also:
:   [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor),
    [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors),
    [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor),
    [DROP MODEL MONITOR](/sql-reference/sql/drop-model-monitor)

## Syntax

### All monitor types

Suspend or resume the monitor, or change the warehouse or refresh interval:

Copy code

```
ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> { SUSPEND | RESUME }

ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> SET
   [ REFRESH_INTERVAL='<refresh_interval>' ]
   [ WAREHOUSE=<warehouse_name> ]
   [ COMMENT = '<string_literal>' ]

ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> UNSET COMMENT
```

### Model version monitor only

Set the baseline table, or add or remove segment columns:

Copy code

```
ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> SET BASELINE = '<baseline_table_name>'

ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> UNSET BASELINE

ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> ADD segment_column = '<segment_column_name>'

ALTER MODEL MONITOR [ IF EXISTS ] <monitor_name> DROP segment_column = '<segment_column_name>'
```

## Parameters

`monitor_name`
:   Specifies the identifier (that is, the name) of the model monitor.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more model monitor properties to be set.

    `BASELINE='<baseline_table_name>'`
    :   Sets the baseline table for drift detection. Supported for model version monitors only. Gateway model monitors do not use a baseline table; instead, drift compares two inference services behind the gateway.

    `WAREHOUSE = warehouse_name`
    :   Sets the warehouse that the monitor uses.

    `REFRESH_INTERVAL = 'refresh_interval'`
    :   The interval at which the monitor refreshes its internal state. The value must be a string representing a time period,
        such as `'1 day'`. The minimum refresh interval is `'60 seconds'`. Supported units include seconds, minutes, hours, and days.
        You may use singular (“hour”) or plural (“hours”) for the interval name.

    `COMMENT = 'string_literal'`
    :   Sets the comment for the model monitor.

`UNSET BASELINE`
:   Removes the baseline table from the monitor. Supported for model version monitors only. After unsetting, drift metrics that require a baseline will no longer be computed until a new baseline is set.

`ADD segment_column = '<segment_column_name>'`
:   Adds a segment column to the monitor. Supported for model version monitors only. The specified column must exist in the source data and be of type STRING.
    You can add up to 5 segment columns per monitor. Each segment column should have fewer than 25 unique values for optimal performance.

`DROP segment_column = '<segment_column_name>'`
:   Removes a segment column from the monitor. Supported for model version monitors only.

For more information about segments, see [ML Observability: Monitoring model behavior over time](/developer-guide/snowflake-ml/model-registry/model-observability).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Modify | Model monitor |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).
