Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_ALERT\_CONFIG

Returns information from an [alert](/user-guide/alerts) configuration.

For information about storing configuration values on an alert, see [CREATE ALERT … CONFIG](/sql-reference/sql/create-alert).

## Syntax

Copy code

```
SYSTEM$GET_ALERT_CONFIG( [<configuration_path>] )
```

## Arguments

`configuration_path`
:   Optional path of the configuration value to return.

    Uses the same syntax as Snowflake queries for semi-structured data.
    See [GET\_PATH](/sql-reference/functions/get_path) for more information.

    If omitted, the function returns the entire configuration as a JSON string.

## Returns

The value at the specified path in the configuration, or the full JSON string if no path is specified.

Returns `NULL` if no configuration is set on the alert.

## Usage notes

- This function can only be called during alert execution (in the condition or action SQL of the alert).
  Calling it outside of alert runtime produces an error.
- Use defensive casting functions such as [TRY\_TO\_NUMBER](/sql-reference/functions/try_to_decimal)
  and [TRY\_TO\_BOOLEAN](/sql-reference/functions/try_to_boolean) when converting configuration values
  to specific types. Use [COALESCE](/sql-reference/functions/coalesce) to provide default values when
  the configuration might be `NULL`.

## Examples

The following example creates an alert with a configuration and uses
SYSTEM$GET\_ALERT\_CONFIG to read values in both the condition and the action:

Copy code

```
CREATE OR REPLACE ALERT my_metric_threshold_alert
  WAREHOUSE = my_alert_wh
  SCHEDULE = '5 MINUTE'
  CONFIG = $${
    "enabled": true,
    "threshold": 10,
    "notify": "ops"
  }$$
  IF( EXISTS(
    SELECT 1
      FROM my_db.my_schema.my_source_table
      WHERE COALESCE(TRY_TO_BOOLEAN(SYSTEM$GET_ALERT_CONFIG('enabled')), FALSE)
        AND metric_value > COALESCE(
          TRY_TO_NUMBER(SYSTEM$GET_ALERT_CONFIG('threshold')), 0)
  ))
  THEN
    INSERT INTO my_db.my_schema.my_output_table
      SELECT CURRENT_TIMESTAMP(), SYSTEM$GET_ALERT_CONFIG('notify');
```
