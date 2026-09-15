Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_ALERT\_TEMPLATE

Returns the definition of a single [alert template](/user-guide/alerts), including the variables you
can set, their data types, defaults, allowed values, and a ready-to-adapt example statement.

Use [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates) to discover
template identifiers, then use this function to inspect a template before you create an alert with
[CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert).

## Syntax

Copy code

```
SYSTEM$GET_ALERT_TEMPLATE( '<template_id>' )
```

## Arguments

`template_id`
:   The identifier of the template to return, as reported by
    [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates).

    The identifier is not case-sensitive. The returned payload reports the canonical identifier in
    `template_id`.

## Returns

Returns a JSON object with a single `template` field. The `template` object includes the same
metadata that [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates)
reports for each template (`template_id`, `template_version`, `display_name`, `alert_description`,
`product`, `supports_new_data_schedule`, `default_schedule`, `scope`, `subcategories`, `runbook`),
plus the following:

- `template_variables`. An array describing each variable you can set through the `TEMPLATE_PARAMS`
  clause. Each variable has:
  - `name`. The variable name to use as a key in `TEMPLATE_PARAMS`.
  - `display_name`. A human-readable name.
  - `description`. Help text describing the variable.
  - `data_type`. The value type: `STRING`, `NUMBER`, or `INTEGER`.
  - `semantic_type`. The value category, such as `PERCENTAGE`, `DURATION_HOURS`, `COUNT`, or `PLAIN_TEXT`.
  - `default_value`. The value used when you omit the variable.
  - `optional`. Present and `true` when the variable is optional. Omitted otherwise.
  - `options`. For variables that accept a fixed set of values, the array of allowed values (for
    example, `["ACCOUNT", "DATABASE", "SCHEMA"]` for a monitoring scope).
  - `min`, `max`, `exclusive_min`. For numeric variables that have a range, the lower bound, the
    upper bound, and whether the lower bound is exclusive. Fields are omitted when they don’t apply.
- `create_syntax`. A ready-to-adapt [CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert)
  statement for the template, prefilled with defaults and sample values. Replace the placeholder
  object names before you run it.
- `alert_definition_template`. The raw template body. This field is informational. You do not need it
  to create an alert with the `FROM TEMPLATE` clause.

## Usage notes

- This is a read-only function. It does not require a running warehouse.
- A variable is required when it lacks both a `default_value` and an `optional: true` flag.
  There is no separate `required` field: requiredness is derived from `default_value` and `optional`.
- The `options` and `min`/`max` fields advertise exactly what the
  [CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert) clause enforces, so you can use
  them to build a valid `TEMPLATE_PARAMS` value before you run the statement.
- If the template ID doesn’t exist or you don’t have access to it, the function returns an
  *object does not exist or not authorized* error. Verify the identifier with
  [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates).

## Examples

Inspect the `TASKS_ERROR_RATE` template:

Copy code

```
SELECT SYSTEM$GET_ALERT_TEMPLATE('TASKS_ERROR_RATE');
```

The function returns a JSON object similar to the following (abbreviated):

Copy code

```
{
  "template": {
    "template_id": "TASKS_ERROR_RATE",
    "template_version": "4.0.0",
    "display_name": "Error rate alert",
    "alert_description": "Monitors when the cumulative error rate of tasks exceeds a threshold, indicating systematic task failures that require attention.",
    "product": "TASKS",
    "supports_new_data_schedule": false,
    "default_schedule": "30 MINUTES",
    "scope": ["Account", "Database", "Schema"],
    "subcategories": null,
    "runbook": "https://docs.snowflake.com/en/user-guide/tasks-ts",
    "template_variables": [
      {
        "name": "ERROR_RATE_THRESHOLD",
        "display_name": "Error rate threshold",
        "description": "Trigger alert when cumulative task error rate exceeds this threshold (0.0 - 1.0).",
        "data_type": "NUMBER",
        "semantic_type": "PERCENTAGE",
        "default_value": 0.15,
        "min": 0,
        "max": 1
      },
      {
        "name": "TASK_NAME_FILTER",
        "display_name": "Task name filter",
        "description": "Optional filter pattern to scope alert to specific tasks (for example, 'ETL_' for tasks starting with ETL_). Leave empty to include all tasks.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": ""
      },
      {
        "name": "SCOPE_ACTIVE",
        "display_name": "Monitoring scope",
        "description": "Monitoring scope for this alert.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": "ACCOUNT",
        "options": ["ACCOUNT", "DATABASE", "SCHEMA"]
      },
      {
        "name": "SCOPE_DATABASE",
        "display_name": "Scope database",
        "description": "Database to monitor when scope is DATABASE or SCHEMA.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": ""
      },
      {
        "name": "SCOPE_SCHEMA",
        "display_name": "Scope schema",
        "description": "Schema to monitor when scope is SCHEMA.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": ""
      },
      {
        "name": "NOTIFICATION_MODE",
        "display_name": "Notification mode",
        "description": "Active notification mode for this alert.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": "EMAIL",
        "options": ["EMAIL", "WEBHOOK"]
      },
      {
        "name": "EMAIL_NOTIFICATION_INTEGRATION",
        "display_name": "Email notification integration",
        "description": "Email notification integration name.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": ""
      },
      {
        "name": "WEBHOOK_NOTIFICATION_INTEGRATION",
        "display_name": "Webhook notification integration",
        "description": "Webhook notification integration name.",
        "data_type": "STRING",
        "semantic_type": "PLAIN_TEXT",
        "default_value": ""
      }
    ],
    "create_syntax": "CREATE OR REPLACE ALERT MY_DB.MY_SCHEMA.MY_ALERT\n  FROM TEMPLATE TASKS_ERROR_RATE\n  WAREHOUSE = MY_WAREHOUSE\n  SCHEDULE = '30 MINUTES'\n  TEMPLATE_PARAMS = '{\n  \"template_variables\" : {\n    \"ERROR_RATE_THRESHOLD\" : 0.15,\n    \"TASK_NAME_FILTER\" : \"\",\n    \"SCOPE_ACTIVE\" : \"ACCOUNT\",\n    \"SCOPE_DATABASE\" : \"\",\n    \"SCOPE_SCHEMA\" : \"\",\n    \"NOTIFICATION_MODE\" : \"EMAIL\",\n    \"EMAIL_NOTIFICATION_INTEGRATION\" : \"\",\n    \"WEBHOOK_NOTIFICATION_INTEGRATION\" : \"\"\n  },\n  \"notification_config\" : {\n    \"notification_integration\" : \"MY_EMAIL_INTEGRATION\",\n    \"email_config\" : {\n      \"toAddress\" : [ \"oncall@example.com\" ]\n    }\n  }\n}';"
  }
}
```

In this example, `ERROR_RATE_THRESHOLD` must be between `0` and `1`, `SCOPE_ACTIVE` must be one of
`ACCOUNT`, `DATABASE`, or `SCHEMA`, and `NOTIFICATION_MODE` must be `EMAIL` or `WEBHOOK`. Because no
variable lacks a `default_value`, every variable is optional for this template.
