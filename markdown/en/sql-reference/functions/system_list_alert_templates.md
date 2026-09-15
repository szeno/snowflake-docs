Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LIST\_ALERT\_TEMPLATES

Lists the [alert templates](/user-guide/alerts) that are available in your account, grouped by product.

Use this function to discover which templates exist before you inspect a specific template with
[SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) and create an alert
with [CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert).

## Syntax

Copy code

```
SYSTEM$LIST_ALERT_TEMPLATES( [ '<product>' ] )
```

## Arguments

`product`
:   An optional product category used to filter the results, so that only the templates owned by that
    product are returned (for example, `TASKS`, `OPENFLOW`, `DATA_QUALITY`). This is the same value
    reported in the `product` field of the returned payload. The value is not case-sensitive.

    If you omit this argument, the function returns the templates for all products.

## Returns

Returns a JSON object that describes the available templates. The top-level fields are:

- `catalog_version`. The version of the alert-template catalog that is active for your account.
- `template_groups`. An array of product groups. Each group has:
  - `product`. The product category that owns the templates (for example, `TASKS`, `OPENFLOW`, `DATA_QUALITY`).
  - `templates`. An array of the templates in that group.

Each object in `templates` has the following fields:

- `template_id`. The identifier you pass to [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template)
  and to the `FROM TEMPLATE` clause of [CREATE ALERT](/sql-reference/sql/create-alert).
- `template_version`. The version of the template.
- `display_name`. A human-readable name for the template.
- `alert_description`. A description of what the template monitors.
- `product`. The product category that owns the template.
- `supports_new_data_schedule`. Whether the template can be used for an
  [alert on new data](/user-guide/alerts#label-alerts-type-streaming) (`true`) in addition to a
  [scheduled alert](/user-guide/alerts#label-alerts-type-scheduled).
- `default_schedule`. The schedule applied when you do not specify one (for example, `30 MINUTES`).
- `scope`. The monitoring scopes the template supports (for example, `["Account", "Database", "Schema"]`).
- `subcategories`. Optional product subcategories, or `null`.
- `runbook`. An optional runbook reference for the template, or `null`.

## Usage notes

- This is a read-only function. It does not require a running warehouse.
- The set of available templates and their variables is managed by Snowflake and can change between
  catalog versions. Always use this function together with
  [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) to get the current
  template identifiers and variable definitions rather than hard-coding them.

## Examples

List all available alert templates:

Copy code

```
SELECT SYSTEM$LIST_ALERT_TEMPLATES();
```

List only the templates owned by a specific product:

Copy code

```
SELECT SYSTEM$LIST_ALERT_TEMPLATES('TASKS');
```

The function returns a JSON object similar to the following (abbreviated):

Copy code

```
{
  "catalog_version": 5,
  "template_groups": [
    {
      "product": "TASKS",
      "templates": [
        {
          "template_id": "TASKS_ERROR_RATE",
          "template_version": "4.0.0",
          "display_name": "Error rate alert",
          "alert_description": "Monitors when the cumulative error rate of tasks exceeds a threshold, indicating systematic task failures that require attention.",
          "product": "TASKS",
          "supports_new_data_schedule": false,
          "default_schedule": "30 MINUTES",
          "scope": ["Account", "Database", "Schema"],
          "subcategories": null,
          "runbook": "https://docs.snowflake.com/en/user-guide/tasks-ts"
        }
      ]
    },
    {
      "product": "DATA_QUALITY",
      "templates": [
        {
          "template_id": "DQ_ANOMALY_DETECTION",
          "template_version": "3.0.0",
          "display_name": "Anomaly detection alert",
          "alert_description": "Monitors for anomalies detected in data quality metrics, alerting when unusual patterns or outliers are identified.",
          "product": "DATA_QUALITY",
          "supports_new_data_schedule": true,
          "default_schedule": "1 HOUR",
          "scope": ["Account", "Database", "Schema", "Table"],
          "subcategories": null,
          "runbook": null
        }
      ]
    }
  ]
}
```
