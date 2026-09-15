# ALTER ALERT

Modifies the properties of an existing alert and suspends or resumes an existing [alert](/user-guide/alerts).

See also:
:   [CREATE ALERT](/sql-reference/sql/create-alert), [DESCRIBE ALERT](/sql-reference/sql/desc-alert), [DROP ALERT](/sql-reference/sql/drop-alert), [SHOW ALERTS](/sql-reference/sql/show-alerts), [EXECUTE ALERT](/sql-reference/sql/execute-alert)

## Syntax

Copy code

```
ALTER ALERT [ IF EXISTS ] <name> { RESUME | SUSPEND };

ALTER ALERT [ IF EXISTS ] <name> SET
  [ WAREHOUSE = <string> ]
  [ SCHEDULE = '{ <number> MINUTE | USING CRON <expr> <time_zone> }' ]
  [ COMMENT = '<string_literal>' ]
  [ CONFIG = '<configuration_string>' ]
  [ RUNBOOK = '<string_literal>' ]
  [ SUSPEND_ALERT_AFTER_NUM_FAILURES = <number> ]

ALTER ALERT [ IF EXISTS ] <name> FROM TEMPLATE <template_id> SET
  [ WAREHOUSE = <string> ]
  [ SCHEDULE = '{ <number> MINUTE | USING CRON <expr> <time_zone> }' ]
  [ COMMENT = '<string_literal>' ]
  [ RUNBOOK = '<string_literal>' ]
  [ SUSPEND_ALERT_AFTER_NUM_FAILURES = <number> ]
  [ TEMPLATE_PARAMS = '<json_string>' ]

ALTER ALERT [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER ALERT [ IF EXISTS ] <name> UNSET
  [ WAREHOUSE ]
  [ COMMENT ]
  [ CONFIG ]
  [ RUNBOOK ]
  [ SUSPEND_ALERT_AFTER_NUM_FAILURES ]

ALTER ALERT <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER ALERT [ IF EXISTS ] <name> MODIFY CONDITION EXISTS (<condition>)

ALTER ALERT [ IF EXISTS ] <name> MODIFY ACTION <action>
```

## Parameters

`name`
:   Identifier for the alert to alter. If the identifier contains spaces or special characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`{ RESUME | SUSPEND }`
:   Specifies the action to perform on the alert:

    - `RESUME` makes a suspended alert active.
    - `SUSPEND` puts the alert into a “Suspended” state.

    If the alert schedule is set to an interval (that is, `num MINUTE`), then to avoid ambiguity, the *base interval time* for
    the schedule is reset to the current time when the alert is resumed.

    The base interval time starts the interval counter from the current clock time. For example, if an alert is created with
    `10 MINUTE` and the alert is resumed at 9:03 AM, then the alert runs at 9:13 AM, 9:23 AM, and so on. Note that we make a best
    effort to ensure absolute precision, but only guarantee that alerts do not execute before their set interval occurs
    (for example, in the current example, the alert could first run at 9:14 AM, but will definitely not run at 9:12 AM).

`SET ...`
:   Specifies one (or more) properties to set for the alert (separated by blank spaces, commas, or new lines).

    `WAREHOUSE = warehouse_name`
    :   Specifies the [virtual warehouse](/user-guide/warehouses) that provides compute resources for executing this alert.

        Note

        For [serverless alerts](/user-guide/alerts#label-alerts-serverless-compute), do not set this property.

    `SCHEDULE ...`
    :   Specifies the schedule for periodically evaluating the condition for the alert on a schedule.

        When you create an alert, omitting this parameter or setting it to NULL creates an
        [alert on new data](/user-guide/alerts#label-alerts-type-streaming).

        For alerts on a schedule, you can specify the schedule in one of the following ways:

        - `USING CRON expr time_zone`

          Specifies a cron expression and time zone for periodically evaluating the condition for the alert. Supports a subset of
          standard cron utility syntax.

          The cron expression consists of the following fields:

          Copy code

          ```
          # __________ minute (0-59)
          # | ________ hour (0-23)
          # | | ______ day of month (1-31, or L)
          # | | | ____ month (1-12, JAN-DEC)
          # | | | | _ day of week (0-6, SUN-SAT, or L)
          # | | | | |
          # | | | | |
            * * * * *
          ```

          The following special characters are supported:

          | Special Character | Description |
          | --- | --- |
          | `*` | Wildcard. When specified for a given field, the alert runs at every unit of time for that field.  For example, `*` in the month field specifies that the alert runs every month. |
          | `L` | Stands for “last”. When used in the day-of-week field, it allows you to specify constructs such as “the last Friday” (“5L”) of a given month. In the day-of-month field, it specifies the last day of the month. |
          | `/n` | Indicates the `n`th instance of a given unit of time. Each quanta of time is computed independently.  For example, if `4/3` is specified in the month field, then the evaluation of the condition is scheduled for April, July and October (i.e. every 3 months, starting with the 4th month of the year).  The same schedule is maintained in subsequent years. That is, the condition is not scheduled to be evaluated in January (3 months after the October run). |

          Expand

          Show lessSee more

          Note

          - The cron expression currently evaluates against the specified time zone only. Altering the
            [TIMEZONE](/sql-reference/parameters#label-timezone) parameter value for the account (or setting the value at the user or session level) does not
            change the time zone for the alert.
          - The cron expression defines all valid times for the evaluation of the condition for the alert. Snowflake attempts
            to evaluate the condition based on this schedule; however, any valid run time is skipped if a previous run has not
            completed before the next valid run time starts.
          - When both a specific day of month and day of week are included in the cron expression, then the evaluation of the
            condition is scheduled on days satisfying either the day of month or day of week. For example,
            `SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'` schedules an evaluation at 0AM on any 10th to 20th day of the month
            and also on any Tuesday or Thursday outside of those dates.
        - `num MINUTE`

          Specifies an interval (in minutes) of wait time inserted between evaluations of the alert. Accepts positive integers only.

          Also supports `num M` syntax.

          To avoid ambiguity, a *base interval time* is set when the alert is resumed (using
          [ALTER ALERT … RESUME](/INCLUDE/text/alter-alert)).

          The base interval time starts the interval counter from the current clock time. For example, if an alert is created with
          `10 MINUTE` and the alert is resumed at 9:03 AM, then the condition for the alert is evaluated at 9:13 AM, 9:23 AM, and so
          on. Note that we make a best effort to ensure absolute precision, but only guarantee that conditions are not evaluated
          before their set interval occurs (e.g. in the current example, the condition could be evaluated first at 9:14 AM but
          definitely not at 9:12 AM).

          Note

          The maximum supported value is `11520` (8 days). Alerts that have a greater `num MINUTE` value never have their
          conditions evaluated.

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the alert.

    `CONFIG = 'configuration_string'`
    :   Specifies the configuration for the alert. For details, see
        [CREATE ALERT … CONFIG](/sql-reference/sql/create-alert).

    `RUNBOOK = 'string_literal'`
    :   Specifies a URL or free-text reference to a runbook for this alert. For details, see
        [CREATE ALERT](/sql-reference/sql/create-alert).

    `SUSPEND_ALERT_AFTER_NUM_FAILURES = number`
    :   Specifies the number of consecutive failed alert runs after which the alert is suspended automatically.
        For more details, see [SUSPEND\_ALERT\_AFTER\_NUM\_FAILURES](/sql-reference/parameters#label-suspend-alert-after-num-failures).

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the alert, which resets them back to their defaults:

    - `WAREHOUSE`
    - `COMMENT`
    - `CONFIG`
    - `RUNBOOK`
    - `SUSPEND_ALERT_AFTER_NUM_FAILURES`
    - `TAG tag_key [ , tag_key ... ]`

`MODIFY CONDITION EXISTS (condition)`
:   Specifies the SQL statement that should represent the condition for the alert. You can use the following commands:

    - [SELECT](/sql-reference/sql/select)
    - [SHOW <objects>](/sql-reference/sql/show)
    - [CALL](/sql-reference/sql/call)

    If the statement returns one or more rows, the action for the alert is executed.

`MODIFY ACTION action`
:   Specifies the SQL statement that should be executed if the condition returns one or more rows.

    To send a notification, you can
    [call the SYSTEM$SEND\_EMAIL or SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION stored procedure](/user-guide/notifications/about-notifications).

`FROM TEMPLATE template_id`
:   Specifies the [alert template](/user-guide/alerts) to render the alert from. Snowflake renders the
    template using the values you supply in `TEMPLATE_PARAMS` and builds the alert in a single statement.

    The identifier is not case-sensitive. Use
    [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates) to discover
    available templates and
    [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) to see a template’s
    variables, data types, defaults, and allowed values.

    When you use `FROM TEMPLATE`, supply the template’s variables through `TEMPLATE_PARAMS`. The `CONFIG`
    parameter and the `IF ... THEN` condition and action are not allowed on a `FROM TEMPLATE` statement,
    because they are generated from the template.

`TEMPLATE_PARAMS = 'json_string'`
:   A JSON string that supplies the template’s variables and notification configuration. Valid only with
    a `FROM TEMPLATE` clause.

    The JSON object can contain the following:

    - `template_variables`. An object of variable name to value, for example
      `{ "ERROR_RATE_THRESHOLD": 0.4, "SCOPE_ACTIVE": "DATABASE" }`. You can also pass these variables as
      a flat top-level object without the `template_variables` wrapper. Omitted variables use the
      template’s default value. Use
      [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) to see the variable
      names, types, defaults, and allowed values.
    - `notification_config`. The notification integration and, for email, the recipients. For example:

      Copy code

      ```
      "notification_config": {
        "notification_integration": "my_email_int",
        "email_config": { "toAddress": ["oncall@example.com"], "subject": "..." }
      }
      ```

      Recipients are a rendering input, not a template variable.

    Statement attributes such as the alert name, `WAREHOUSE`, `SCHEDULE`, `COMMENT`, `RUNBOOK`,
    `SUSPEND_ALERT_AFTER_NUM_FAILURES`, and tags are specified with the normal alert clauses, not in
    `TEMPLATE_PARAMS`.

    When you re-render an existing alert with [ALTER ALERT … FROM TEMPLATE](/sql-reference/sql/alter-alert)
    or CREATE OR ALTER ALERT, `TEMPLATE_PARAMS` is applied in full: any variable you omit resets to the
    template’s default value rather than keeping its previous value.

**Common errors**

Snowflake resolves the template and validates `TEMPLATE_PARAMS` when the statement compiles, before
the alert is created. The statement fails if any of the following are true:

- The `template_id` doesn’t name a template that exists and that you have access to (returns an
  *object does not exist or not authorized* error).
- A `TEMPLATE_PARAMS` key is not a declared template variable.
- A value has the wrong data type.
- An enumerated value is not one of the variable’s allowed `options`.
- A numeric value is outside the variable’s `min`/`max` range.
- A required variable (one with no `default_value` and not `optional: true`) is missing or empty.
- A referenced notification integration does not exist or is the wrong type.

## Access control requirements

Executing this SQL command requires [roles](/user-guide/security-access-control-overview#label-access-control-overview-roles) with the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

- To resume an alert:

  - The role executing ALTER ALERT must have either the OPERATE or OWNERSHIP privilege on the alert.
  - The role with the OWNERSHIP privilege on the alert must also have the following privileges:
    - The global EXECUTE ALERT privilege.
    - The global EXECUTE MANAGED ALERT privilege, if the alert is a [serverless alert](/user-guide/alerts#label-alerts-serverless-compute).
    - The USAGE privilege on the warehouse, if the [alert uses a specified warehouse](/user-guide/alerts#label-alerts-warehouse-user-managed).
- To suspend an alert, the role executing ALTER ALERT must have either the OPERATE or OWNERSHIP privilege on the alert.
- To modify the properties of the alert, the role executing ALTER ALERT must have the OWNERSHIP privilege on the alert.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot change an [alert on new data](/user-guide/alerts#label-alerts-type-streaming) to an
  [alert on a schedule](/user-guide/alerts#label-alerts-type-scheduled). Similarly, you cannot change an alert on a schedule to an alert
  on new data.
- When an alert is resumed, Snowflake verifies that the role with the OWNERSHIP privilege on the alert also has the USAGE
  privilege on the warehouse assigned to the alert, as well as the global EXECUTE ALERT privilege; if not, an error is produced.
- Only account administrators (users with the ACCOUNTADMIN role) can grant the EXECUTE ALERT privilege to a role. For ease of use,
  we recommend creating a custom role (for example, alert\_admin) and assigning the EXECUTE ALERT privilege to this role. Any role that can
  grant privileges (for example, SECURITYADMIN or any role with the MANAGE GRANTS privilege) can then grant this custom role to any alert
  owner role to allow altering their own alerts. For instructions for creating custom roles and role hierarchies, see
  [Configuring access control](/user-guide/security-access-control-configure).
- To alter the CONFIG, you must supply the entire replacement JSON string. You can’t update individual
  key-value pairs.
- You can use the `FROM TEMPLATE` clause only on an alert that was created from a template. Use it to change template
  variables in place using the latest version of the same template, or to re-point the alert to a different template by specifying a different `template_id`.
- You cannot use `FROM TEMPLATE` to change an alert on a schedule into an alert on new data, or the reverse.

- When you execute CREATE ALERT or ALTER ALERT, some validation checks are not performed on the statements in the condition and
  action, including:

  - The resolution of the identifiers for objects.
  - The resolution of the data types of expressions.
  - The verification of the number and types of arguments in a function call.

  The CREATE ALERT and ALTER ALERT commands do not fail if the SQL statement for a condition or action specifies an invalid
  identifier, incorrect data type, incorrect number and types of function arguments, etc. Instead, the failure occurs when the
  alert executes.

  To check for failures in an existing alert, use the [ALERT\_HISTORY](/sql-reference/functions/alert_history) table function.

  To avoid these types of failures, before you specify the conditions and actions for alerts, verify the SQL expressions and
  statements for those conditions and actions.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

See [Suspending and resuming an alert](/user-guide/alerts#label-alerts-suspend-resume).

Update an existing alert with new or replacement configuration:

Copy code

```
ALTER ALERT my_alert SET
  CONFIG=$${
    "enabled": true,
    "threshold": 25,
    "notify": "oncall"
  }$$;
```

Remove the configuration from an existing alert:

Copy code

```
ALTER ALERT my_alert UNSET CONFIG;
```

Set a runbook on an existing alert:

Copy code

```
ALTER ALERT my_alert SET
  RUNBOOK='https://www.snowflake.com/alerts/my-alert-runbook';
```

Remove the runbook from an existing alert:

Copy code

```
ALTER ALERT my_alert UNSET RUNBOOK;
```

Re-render a templated alert with a new threshold. Any template variable you omit resets to the template’s default:

Copy code

```
ALTER ALERT my_db.my_schema.task_error_rate_alert FROM TEMPLATE TASKS_ERROR_RATE SET
  TEMPLATE_PARAMS = '{ "ERROR_RATE_THRESHOLD": 0.75 }';
```
