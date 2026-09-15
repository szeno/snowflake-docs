# Setting up alerts based on data in Snowflake

This topic explains how to set up an alert that periodically performs an action under specific conditions, based on data within
Snowflake.

## Introduction

In some cases, you might want to be notified or take action when data in Snowflake meets certain conditions. For example, you
might want to receive a notification when:

- The warehouse credit usage increases by a specified percentage of your current quota.
- The resource consumption for your pipelines, tasks, materialized views, and so on, increases beyond a specified amount.
- Your data fails to comply with a particular business rule that you have set up.

To do this, you can set up a Snowflake alert. A Snowflake alert is a schema-level object that specifies:

- A condition that triggers the alert (for example, the presence of queries that take longer than a second to complete).
- The action to perform when the condition is met (for example, send an email notification, capture some data in a table, and so on).
- When and how often the condition should be evaluated (for example, every 24 hours or every Sunday at midnight).

For example, suppose that you want to send an email notification when the credit consumption exceeds a certain limit for a
warehouse. Suppose that you want to check for this every 30 minutes. You can create an alert with the following properties:

- Condition: The credit consumption for a warehouse (the sum of the `credits_used` column in the
  [WAREHOUSE\_METERING\_HISTORY](/sql-reference/account-usage/warehouse_metering_history) view in the
  [ACCOUNT\_USAGE](/sql-reference/account-usage)) schema exceeds a specified limit.
- Action: Email the administrator.
- Frequency / schedule: Check for this condition every 30 minutes.

## Choosing the type of alert

You can create the following types of alerts:

- [Alert on a schedule](#label-alerts-type-scheduled): Snowflake evaluates the condition against the existing data on a
  scheduled basis.

  For example, you can set up an alert on a schedule to check if any of the existing rows in a table has a column value that
  exceeds a specified amount.
- [Alert on new data](#label-alerts-type-streaming): Snowflake evaluates the condition against any new rows in a specified
  table or a view.

  For example, you can set up an alert on new data to notify you when new rows for error messages are inserted into the
  [event table](/developer-guide/logging-tracing/event-table-setting-up) for your account. Because dynamic table refreshes
  and task executions log events to the event table, you can set up an alert on new data to:

  - [Monitor dynamic table refreshes](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-streaming-alerts).
  - [Monitor task executions](/user-guide/tasks-events).

### Alerts on a schedule

With an alert on a schedule, you can set up an alert to execute every `n` minutes or on a schedule specified by a cron
expression.

The condition of the alert is evaluated on all of the data (as opposed to alerts on new data, where conditions are evaluated
against only the new rows that have been inserted).

### Alerts on new data

With an alert on new data, you can set up an alert to execute only when new rows are inserted in a table or are made available
in a view.

Whenever new rows are inserted, the alert executes, evaluating the condition against just the new rows, and performing the action
if the condition evaluates to TRUE.

If you want to evaluate a condition on newly inserted rows, use an alert on new data, rather than setting up an alert on a
schedule (which executes on a fixed schedule, regardless of whether or not data has been added).

Because the alert operates only on newly inserted rows in a table or view, there are restrictions on the condition that you can
specify:

- In the SELECT statement, the FROM clause can specify only one regular table, view, or event table.
- You must [enable change tracking](/user-guide/streams-manage#label-enabling-change-tracking-views) on that table or view.
- You cannot use:
  - [Common table expressions (CTEs)](/user-guide/queries-cte)
  - [Data Manipulation Language (DML) commands](/sql-reference/sql-dml)
  - Calls to stored procedures
  - Joins

Note

You cannot use the [EXECUTE ALERT](/sql-reference/sql/execute-alert) command to execute an alert on new data.

## Choosing the warehouse for the alerts

An alert requires a [warehouse](/user-guide/warehouses) for execution. You can either use
[the serverless compute model](#label-alerts-serverless-compute) or
[a virtual warehouse that you specify](#label-alerts-warehouse-user-managed).

### Using the serverless compute model (serverless alerts)

Alerts that use the serverless compute model are called *serverless alerts*. If you use the serverless compute model, Snowflake
automatically resizes and scales the compute resources required for the alert. Snowflake determines the ideal size of the compute
resources for a given run based on a dynamic analysis of statistics for the most recent previous runs of the same alert. The
maximum size for a serverless alert run is equivalent to an XXLARGE warehouse. Multiple workloads in your account share a common
set of compute resources.

Billing is similar to other serverless features (such as serverless tasks). See [Understanding the costs of alerts](#label-alerts-costs).

Note

If you are creating an [alert on new data](#label-alerts-type-streaming) that is added infrequently, consider
configuring this as a serverless alert. If you configure the alert to use a warehouse instead, even a simple action that sends
an email notification incurs at least one minute of warehouse cost.

### Using a virtual warehouse that you specify

If you want to specify a virtual warehouse, you must choose a warehouse that is sized appropriately for the SQL actions that
are executed by the alert. For guidelines on choosing a warehouse, see [Warehouse considerations](/user-guide/warehouses-considerations).

## Understanding the costs of alerts

The costs associated with running an alert to execute SQL code differ depending on the compute resources used for the alert:

- For serverless alerts, Snowflake bills your account based on compute resource usage. Charges are calculated based on your
  total usage of the resources, including cloud service usage, measured in *compute-hours* credit usage. The compute-hours cost
  changes based on warehouse size and query runtime. For more information, see [Serverless credit usage](/user-guide/cost-understanding-compute#label-serverless-credit-usage).

  To learn how many credits are consumed by alerts, refer to the “Serverless Feature Credit Table” in
  the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

  To view the usage history of serverless alerts, you can:

  - Call the [SERVERLESS\_ALERT\_HISTORY](/sql-reference/functions/serverless_alert_history) function.
  - Query the [SERVERLESS\_ALERT\_HISTORY view](/sql-reference/account-usage/serverless_alert_history).
- For alerts that use a virtual warehouse that you specify, Snowflake bills your account for
  [credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage) based on the warehouse usage when an alert is running. This is
  similar to the warehouse usage for executing the same SQL statements in a client or Snowsight. Per-second credit
  billing and warehouse auto-suspend give you the flexibility to start with larger warehouse sizes and then adjust the size to
  match your alert workloads.

Tip

If you want to set up an alert that evaluates new rows added to a table or view, use an
[alert on new data](#label-alerts-type-streaming), rather than an alert on a schedule. An alert on a schedule will
execute at a scheduled time, regardless of whether or not new rows have been inserted.

## Granting the privileges to create alerts

In order to create an alert, you must use a role that has the following privileges:

- The EXECUTE ALERT privilege on the account.

  Note

  This privilege can only be granted by a user with the ACCOUNTADMIN role.
- One of the following privileges:

  - The EXECUTE MANAGED ALERT privilege on the account, if you are creating a serverless alert.
  - The USAGE privilege on the warehouse used to execute the alert, if you are specifying a virtual warehouse for the alert.
- The USAGE and CREATE ALERT privileges on the schema in which you want to create the alert.
- The USAGE privilege on the database containing the schema.
- The SELECT privilege on the table or view that you want to query in the alert condition (if you are creating an
  [alert on new data](#label-alerts-type-streaming)).

To grant these privileges to a role, use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command.

For example, suppose that you want to create a custom role named `my_alert_role` that has the privileges to create an alert in
the schema named `my_schema`. You want the alert to use the warehouse `my_warehouse`.

To do this:

1. Have a user with the ACCOUNTADMIN role do the following:

   1. [Create the custom role](/user-guide/security-access-control-configure#label-security-custom-role).

      For example:

      Copy code

      ```
      USE ROLE ACCOUNTADMIN;

      CREATE ROLE my_alert_role;
      ```
   2. Grant the EXECUTE ALERT global privilege to that custom role.

      For example:

      Copy code

      ```
      GRANT EXECUTE ALERT ON ACCOUNT TO ROLE my_alert_role;
      ```
   3. If you want to create a serverless alert, grant the EXECUTE MANAGED ALERT global privilege to that custom role.

      For example:

      Copy code

      ```
      GRANT EXECUTE MANAGED ALERT ON ACCOUNT TO ROLE my_alert_role;
      ```
   4. Grant the custom role to a user.

      For example:

      Copy code

      ```
      GRANT ROLE my_alert_role TO USER my_user;
      ```
2. Have the owners of the database, schema, and warehouse grant the privileges needed for creating the alert to the custom role:

   - The owner of the schema must grant the CREATE ALERT and USAGE privileges on the schema:

     Copy code

     ```
     GRANT CREATE ALERT ON SCHEMA my_schema TO ROLE my_alert_role;
     GRANT USAGE ON SCHEMA my_schema TO ROLE my_alert_role;
     ```
   - The owner of the database must grant the USAGE privilege on the database:

     Copy code

     ```
     GRANT USAGE ON DATABASE my_database TO ROLE my_alert_role;
     ```
   - If you want to specify a warehouse for the alert, the owner of that warehouse must grant the USAGE privilege on the
     warehouse:

     Copy code

     ```
     GRANT USAGE ON WAREHOUSE my_warehouse TO ROLE my_alert_role;
     ```

## Creating an alert

To get started quickly, you can create an alert from a predefined template for common alerting use
cases instead of writing the condition and action yourself. You can do this in
[Snowsight](/user-guide/alerts-ui) or with [Creating an alert from a template with SQL](#label-alerts-create-from-template).

The following sections provide the basic steps and an example of creating different types of alerts:

- [Creating an alert on a schedule](#label-alerts-create-scheduled)
- [Creating an alert on new data](#label-alerts-create-streaming)

### Creating an alert on a schedule

Suppose that whenever one or more rows in a table named `gauge` has a value in the `gauge_value` column that exceeds 200,
you want to insert the current timestamp into a table named `gauge_value_exceeded_history`.

You can create an alert that:

- Evaluates the condition that `gauge_value` exceeds 200.
- Inserts the timestamp into `gauge_value_exceeded_history` if this condition evaluates to true.

To create an alert named `my_alert` that does this:

1. Verify that you are using a role that has [the privileges to create an alert](#label-alerts-privileges-granting).

   If you are not using that role, execute the [USE ROLE](/sql-reference/sql/use-role) command to use that role.
2. Verify that you are using the database and schema in which you plan to create the alert.

   If you are not using that database and schema, execute the [USE DATABASE](/sql-reference/sql/use-database) and
   [USE SCHEMA](/sql-reference/sql/use-schema) commands to use that database and schema.
3. Execute the [CREATE ALERT](/sql-reference/sql/create-alert) command to create the alert:

   Copy code

   ```
   CREATE OR REPLACE ALERT my_alert
     WAREHOUSE = mywarehouse
     SCHEDULE = '1 minute'
     IF( EXISTS(
    SELECT gauge_value FROM gauge WHERE gauge_value>200))
     THEN
    INSERT INTO gauge_value_exceeded_history VALUES (current_timestamp());
   ```

   If you want to create a serverless alert, omit the WAREHOUSE parameter:

   Copy code

   ```
   CREATE OR REPLACE ALERT my_alert
     SCHEDULE = '1 minute'
     IF( EXISTS(
    SELECT gauge_value FROM gauge WHERE gauge_value>200))
     THEN
    INSERT INTO gauge_value_exceeded_history VALUES (current_timestamp());
   ```

   For the full description of the CREATE ALERT command, refer to [CREATE ALERT](/sql-reference/sql/create-alert).

   Note

   When you create an alert, the alert is suspended by default. You must resume the newly created alert in order for the alert
   to execute.
4. Resume the alert by executing the [ALTER ALERT … RESUME](/sql-reference/sql/alter-alert) command. For example:

   Copy code

   ```
   ALTER ALERT my_alert RESUME;
   ```

### Creating an alert on new data

Suppose that you want to receive an email notification when a stored procedure named `my_stored_proc` in the database and
schema `my_db.my_schema` logs a FATAL message to the
[active event table for your account](/developer-guide/logging-tracing/event-table-setting-up).

To create an alert named `my_alert` that does this:

1. Find the name of the active event table for your account:

   Copy code

   ```
   SHOW PARAMETERS LIKE 'EVENT_TABLE' IN ACCOUNT;
   ```

   ```
   +-------------+---------------------------+----------------------------+---------+-----------------------------------------+--------+
   | key         | value                     | default                    | level   | description                             | type   |
   |-------------+---------------------------+----------------------------+---------+-----------------------------------------+--------|
   | EVENT_TABLE | my_db.my_schema.my_events | snowflake.telemetry.events | ACCOUNT | Event destination for the given target. | STRING |
   +-------------+---------------------------+----------------------------+---------+-----------------------------------------+--------+
   ```
2. [Enable change tracking](/user-guide/streams-manage#label-enabling-change-tracking-views) on the table or view that you plan to query in the alert
   condition.

   Copy code

   ```
   ALTER TABLE my_db.my_schema.my_events SET CHANGE_TRACKING = TRUE;
   ```
3. [Set up a notification integration for sending email](/user-guide/notifications/email-notifications).
4. Verify that you are using a role that has [the privileges to create an alert](#label-alerts-privileges-granting).

   If you are not using that role, execute the [USE ROLE](/sql-reference/sql/use-role) command to use that role.
5. Verify that you are using the database and schema in which you plan to create the alert.

   If you are not using that database and schema, execute the [USE DATABASE](/sql-reference/sql/use-database) and
   [USE SCHEMA](/sql-reference/sql/use-schema) commands to use that database and schema.
6. Execute the [CREATE ALERT](/sql-reference/sql/create-alert) command to create the alert, and omit the SCHEDULE parameter.

   For example, the following example creates an alert on new data that monitors the event table for errors in dynamic table
   refreshes and sends a notification to a Slack channel. The example assumes the following:

   - Your active event table is the [default event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default)
     (SNOWFLAKE.TELEMETRY.EVENTS).
   - You have [set the severity level](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitoring-sql-events-level) to capture events for your dynamic
     table.
   - You have [set up a webhook notification integration](/user-guide/notifications/webhook-notifications) for that Slack
     channel.

   Copy code

   ```
   CREATE OR REPLACE ALERT my_alert
     WAREHOUSE = mywarehouse
     IF( EXISTS(
    SELECT * FROM SNOWFLAKE.TELEMETRY.EVENTS
      WHERE
        resource_attributes:"snow.executable.type" = 'DYNAMIC_TABLE' AND
        record_type='EVENT' AND
        value:"state"='ERROR'
     ))
     THEN
    BEGIN
      LET result_str VARCHAR;
      (SELECT ARRAY_TO_STRING(ARRAY_AGG(name)::ARRAY, ',') INTO :result_str
        FROM (
          SELECT resource_attributes:"snow.executable.name"::VARCHAR name
            FROM TABLE(RESULT_SCAN(SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID()))
            LIMIT 10
        )
      );
      CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
        SNOWFLAKE.NOTIFICATION.TEXT_PLAIN(:result_str),
        '{"my_slack_integration": {}}'
      );
    END;
   ```

   If you want to create a serverless alert, omit the WAREHOUSE parameter:

   Copy code

   ```
   CREATE OR REPLACE ALERT my_alert
     IF( EXISTS(
    SELECT * FROM SNOWFLAKE.TELEMETRY.EVENTS
      WHERE
        resource_attributes:"snow.executable.type" = 'DYNAMIC_TABLE' AND
        record_type='EVENT' AND
        value:"state"='ERROR'
     ))
     THEN
    BEGIN
      LET result_str VARCHAR;
      (SELECT ARRAY_TO_STRING(ARRAY_AGG(name)::ARRAY, ',') INTO :result_str
        FROM (
          SELECT resource_attributes:"snow.executable.name"::VARCHAR name
            FROM TABLE(RESULT_SCAN(SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID()))
            LIMIT 10
        )
      );
      CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
        SNOWFLAKE.NOTIFICATION.TEXT_PLAIN(:result_str),
        '{"my_slack_integration": {}}'
      );
    END;
   ```

   For the full description of the CREATE ALERT command, refer to [CREATE ALERT](/sql-reference/sql/create-alert).

   Note

   When you create an alert, the alert is suspended by default. You must resume the newly created alert in order for the alert
   to execute.
7. Resume the alert by executing the [ALTER ALERT … RESUME](/sql-reference/sql/alter-alert) command. For example:

   Copy code

   ```
   ALTER ALERT my_alert RESUME;
   ```

## Adding a runbook to an alert

You can attach a runbook reference to an alert so that responders know where to find
documentation or troubleshooting instructions when the alert triggers.

The runbook is a free-text string (up to 2048 characters), typically a URL pointing to
internal documentation.

### Setting the runbook

Use the `RUNBOOK` parameter in [CREATE ALERT](/sql-reference/sql/create-alert) or
[ALTER ALERT](/sql-reference/sql/alter-alert) to set the runbook:

Copy code

```
CREATE OR REPLACE ALERT my_alert
  WAREHOUSE = my_alert_wh
  SCHEDULE = '5 MINUTE'
  RUNBOOK = 'https://www.snowflake.com/alerts/my-alert-runbook'
  IF( EXISTS(
    SELECT 1 FROM my_table WHERE error_count > 100
  ))
  THEN
    CALL SYSTEM$SEND_EMAIL(...);
```

To update the runbook later:

Copy code

```
ALTER ALERT my_alert SET
  RUNBOOK = 'https://www.snowflake.com/alerts/my-alert-runbook-v2';
```

### Viewing the runbook

The runbook value appears in the output of [SHOW ALERTS](/sql-reference/sql/show-alerts),
[DESCRIBE ALERT](/sql-reference/sql/desc-alert), and
[ALERT\_HISTORY](/sql-reference/functions/alert_history).

## Passing configuration to an alert

You can store a JSON configuration on an alert and read it at runtime in both the condition
(`IF`) and action (`THEN`) SQL. This lets you parameterize alert logic (for example, thresholds,
notification targets, or feature flags) without modifying the alert’s SQL statements directly.

### Setting the configuration

Use the `CONFIG` parameter in [CREATE ALERT](/sql-reference/sql/create-alert) or
[ALTER ALERT](/sql-reference/sql/alter-alert) to set the configuration as a JSON string.

The configuration can contain any business-logic parameters that the alert’s SQL references at
runtime, for example, thresholds, enable/disable switches, and notification targets.

The following example creates an alert whose condition and action are both driven by configuration
values:

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

To update the configuration later, use ALTER ALERT … SET CONFIG. Setting the CONFIG
replaces the entire JSON object; you can’t update individual key-value pairs:

Copy code

```
ALTER ALERT my_metric_threshold_alert SET
  CONFIG = $${
    "enabled": true,
    "threshold": 25,
    "notify": "oncall"
  }$$;
```

### Reading configuration values at runtime

Call [SYSTEM$GET\_ALERT\_CONFIG](/sql-reference/functions/system_get_alert_config) to retrieve
configuration values. You can retrieve the full JSON object or a specific field:

- `SYSTEM$GET_ALERT_CONFIG()` returns the entire configuration as a JSON string.
- `SYSTEM$GET_ALERT_CONFIG('threshold')` returns the value of the `threshold` field.

If no configuration is set, the function returns `NULL`.

Note

SYSTEM$GET\_ALERT\_CONFIG can only be called during alert execution. Calling it outside of alert
runtime produces an error.

### Best practices for using configuration values

Because configuration values are stored as JSON and are read as strings, cast them defensively to
avoid runtime errors:

- Use [TRY\_TO\_NUMBER](/sql-reference/functions/try_to_decimal) or
  [TRY\_TO\_BOOLEAN](/sql-reference/functions/try_to_boolean) instead of direct casts.
- Use [COALESCE](/sql-reference/functions/coalesce) to provide fallback defaults when
  the configuration might not be set.
- Use a CTE to extract and cast configuration values once, then reference them in the rest of the
  query.

#### Example: Advanced alert with CTE-based config extraction

The following example shows a more complex alert that uses a CTE to extract configuration values,
filters task history by a configurable scope and name pattern, and passes the full configuration
to a handler procedure:

Copy code

```
CREATE OR REPLACE ALERT my_tasks_error_rate_alert
  WAREHOUSE = my_alert_wh
  SCHEDULE = '1 MINUTE'
  CONFIG = $${
    "ERROR_RATE_THRESHOLD": 0.05,
    "TASK_SCOPE": "ETL_",
    "SCOPE": "DATABASE",
    "DATABASE": "my_db"
  }$$
  IF( EXISTS(
    WITH cfg AS (
      SELECT
        COALESCE(TRY_TO_NUMBER(
          SYSTEM$GET_ALERT_CONFIG('ERROR_RATE_THRESHOLD')), 0.05)
          AS error_rate_threshold,
        COALESCE(SYSTEM$GET_ALERT_CONFIG('TASK_SCOPE')::STRING, '')
          AS task_scope,
        COALESCE(SYSTEM$GET_ALERT_CONFIG('DATABASE')::STRING, '')
          AS scope_database
    ),
    task_window AS (
      SELECT *
        FROM TABLE(
          INFORMATION_SCHEMA.TASK_HISTORY(
            SCHEDULED_TIME_RANGE_START =>
              SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME()
          )
        )
        WHERE DATABASE_NAME = (SELECT scope_database FROM cfg)
          AND NAME ILIKE (SELECT task_scope FROM cfg) || '%'
    ),
    agg AS (
      SELECT
        COUNT(*) AS total_runs,
        COUNT_IF(STATE = 'FAILED') AS failed_runs
        FROM task_window
    )
    SELECT 1
      FROM agg, cfg
      WHERE total_runs > 0
        AND failed_runs / total_runs::FLOAT > error_rate_threshold
  ))
  THEN
    CALL my_db.my_schema.handle_task_alert(
      PARSE_JSON(SYSTEM$GET_ALERT_CONFIG())
    );
```

In this example:

- The CTE `cfg` extracts and casts each configuration value once, with safe defaults.
- The `task_window` CTE filters task history by a configurable database and task name pattern.
- The action passes the full configuration as a parsed JSON object to a handler procedure, which
  can route notifications or take other actions based on the configuration.

#### Rich configuration used by alert templates

When you create an alert from a template in
[Snowsight](/user-guide/alerts-ui#label-alerts-center-edit-config), the template
sets a richer configuration structure where each field includes metadata such as a description and
available options. For example, a task error-rate template might set a configuration like the
following:

Copy code

```
CONFIG = $${
  "ERROR_RATE_THRESHOLD": {
    "description": "Trigger alert when cumulative task error rate exceeds this threshold (0.0 - 1.0).",
    "value": 0.1
  },
  "NOTIFICATION": {
    "EMAIL": {
      "recipients": ["alerts@example.com"],
      "value": "my_email_int"
    },
    "WEBHOOK": {
      "value": ""
    },
    "notification_value": {
      "active": "EMAIL",
      "options": ["EMAIL", "WEBHOOK"]
    }
  },
  "SCOPE": {
    "DATABASE": { "value": "my_db" },
    "SCHEMA": { "value": "" },
    "scope_value": {
      "active": "DATABASE",
      "options": ["ACCOUNT", "DATABASE", "SCHEMA"]
    }
  },
  "TASK_NAME_FILTER": {
    "description": "Optional filter pattern to scope alert to specific tasks. Leave empty for all tasks.",
    "value": "ETL_"
  }
}$$
```

The key components of this structure that allow Snowsight to render a rich editing form are:

- **description**: Human-readable help text that Snowsight displays beneath each input field. This
  turns a raw JSON key into a self-documenting form field.
- **value**: The actual runtime value that the alert’s SQL reads through SYSTEM$GET\_ALERT\_CONFIG.
  Separating the value from its metadata lets the UI render rich controls while the SQL only needs
  to read the `value` leaf.
- **options array and active selector**: For fields with a fixed set of valid choices (such as
  notification channel or monitoring scope), the `options` array lists the choices and `active`
  tracks the current selection. Snowsight renders these as dropdowns instead of free-text inputs.
- **Nested channel objects**: Each notification channel (such as `EMAIL` or `WEBHOOK`) carries its
  own sub-fields (integration name, recipients). Snowsight shows or hides the relevant sub-fields
  based on which channel is `active`.
- **Hierarchical scope objects**: The scope level controls which child fields are relevant. For
  example, selecting `DATABASE` displays a database picker, while selecting `SCHEMA` displays
  both a database and a schema picker.

The template’s SQL reads only the `value` fields at runtime using SYSTEM$GET\_ALERT\_CONFIG. If you
modify the configuration structure through SQL (for example, by flattening the JSON or removing
metadata keys), Snowsight falls back to a flat key-value editor.

#### Creating an alert from a template with SQL

In addition to [Snowsight](/user-guide/alerts-ui), you can create an alert from a template directly in
SQL, which is useful for scripting, Terraform, and other callers outside Snowsight:

1. List the available templates with
   [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates).
2. Inspect a template’s variables, data types, defaults, and allowed values with
   [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template).
3. Create the alert with
   [CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert#label-create-alert-from-template-syntax),
   passing the template’s variables in the `TEMPLATE_PARAMS` clause. To change the variables later,
   use [ALTER ALERT … FROM TEMPLATE](/sql-reference/sql/alter-alert).

For example:

Copy code

```
CREATE OR REPLACE ALERT my_db.my_schema.task_error_rate_alert
  FROM TEMPLATE TASKS_ERROR_RATE
  WAREHOUSE = my_wh
  SCHEDULE = '30 MINUTE'
  TEMPLATE_PARAMS = '{
    "template_variables": { "ERROR_RATE_THRESHOLD": 0.4 },
    "notification_config": {
      "notification_integration": "my_email_int",
      "email_config": { "toAddress": ["oncall@example.com"] }
    }
  }';
```

Snowflake renders the template on the server, so you don’t construct the full configuration JSON
yourself. Snowflake validates the variable bindings when the statement compiles, so an invalid value,
such as an out-of-range threshold or an unknown notification integration, is reported before the
alert is created.

## Specifying timestamps based on alert schedules

In some cases, you might need to define a condition or action based on the alert schedule.

For example, suppose that a table has a timestamp column that represents when a row was added, and you want to send an alert
if any new rows were added between the last alert that was successfully evaluated and the current scheduled alert. In other
words, you want to evaluate:

Copy code

```
<now> - <last_execution_of_the_alert>
```

If you use [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) and the scheduled time of the alert to calculate this range of
time, the calculated range does not account for latency between the time that the alert is scheduled and the time when the
alert condition is actually evaluated.

Instead, when you need the timestamps of the current schedule alert and the last alert that was successfully evaluated, use the
following functions:

- [SCHEDULED\_TIME](/sql-reference/functions/scheduled_time) returns the timestamp representing when the current alert was scheduled.
- [LAST\_SUCCESSFUL\_SCHEDULED\_TIME](/sql-reference/functions/last_successful_scheduled_time) returns the timestamp representing when the last successfully
  evaluated alert was scheduled.

These functions are defined in the [SNOWFLAKE.ALERT schema](/sql-reference/snowflake-db). To call these functions, you need
to use a role that has been granted the [SNOWFLAKE.ALERT\_VIEWER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-alert-schema). To
grant this role to another role, use the [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) command. For example, to grant this role
to the custom role `alert_role`, execute:

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.ALERT_VIEWER TO ROLE alert_role;
```

The following example sends an email message if any new rows were added to `my_table` between the time that the last
successfully evaluated alert was scheduled and the time when the current alert has been scheduled:

Copy code

```
CREATE OR REPLACE ALERT alert_new_rows
  WAREHOUSE = my_warehouse
  SCHEDULE = '1 MINUTE'
  IF (EXISTS (
      SELECT *
      FROM my_table
      WHERE row_timestamp BETWEEN SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME()
       AND SNOWFLAKE.ALERT.SCHEDULED_TIME()
  ))
  THEN CALL SYSTEM$SEND_EMAIL(...);
```

## Checking the results of the SQL statement for the condition in the alert action

Within the action of an alert, if you need to check the results of the SQL statement for the condition:

1. Call the [GET\_CONDITION\_QUERY\_UUID](/sql-reference/functions/get_condition_query_uuid) function to get the query ID for the SQL statement for the
   condition.
2. Pass the query ID to the [RESULT\_SCAN](/sql-reference/functions/result_scan) function to get the results of the execution of that SQL
   statement.

For example:

Copy code

```
CREATE ALERT my_alert
  WAREHOUSE = my_warehouse
  SCHEDULE = '1 MINUTE'
  IF (EXISTS (
    SELECT * FROM my_source_table))
  THEN
    BEGIN
      LET condition_result_set RESULTSET :=
        (SELECT * FROM TABLE(RESULT_SCAN(SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID())));
      ...
    END;
```

## Manually executing alerts

In some cases, you might need to execute an alert manually. For example:

- If you are creating a new alert, you might want to verify that the alert works as you would expect.
- You might want to execute the alert at a specific point in your data pipeline. For example, you might want to execute the
  alert at the end of a stored procedure call.

To execute an alert manually, run the [EXECUTE ALERT](/sql-reference/sql/execute-alert) command:

Copy code

```
EXECUTE ALERT my_alert;
```

Note

You cannot use EXECUTE ALERT to execute an [alert on new data](#label-alerts-type-streaming).

The EXECUTE ALERT command manually triggers a single run of an alert, independent of the schedule defined for the alert.

You can execute this command interactively. You can also execute this command from within a stored procedure or a Snowflake
Scripting block.

For details on the privileges required to run this command and the effect of this command on suspended, running, and scheduled
alerts, see [EXECUTE ALERT](/sql-reference/sql/execute-alert).

## Suspending and resuming an alert

If you need to prevent an alert from executing temporarily, you can suspend the alert by executing the
[ALTER ALERT … SUSPEND](/sql-reference/sql/alter-alert) command. For example:

Copy code

```
ALTER ALERT my_alert SUSPEND;
```

To resume a suspended alert, execute the [ALTER ALERT … RESUME](/sql-reference/sql/alter-alert) command. For example:

Copy code

```
ALTER ALERT my_alert RESUME;
```

Note

If you are not the owner of the alert, you must have the OPERATE privilege on the alert to suspend or resume the alert.

## Automatically suspend alerts after failed runs

Suspend alerts automatically after a specified number of consecutive failed runs.

Set the `SUSPEND_ALERT_AFTER_NUM_FAILURES = number` parameter on an alert. When the parameter
is set to a value greater than `0`, alerts are automatically suspended after the specified number of
consecutive alert runs that either fail or time out (for example, runs that end in the `ACTION_FAILED` or `CONDITION_FAILED` state).
The counter resets to `0` when the alert run succeeds, or when the alert is manually suspended or resumed.

The parameter can be set when creating an alert using [CREATE ALERT](/sql-reference/sql/create-alert) or later using
[ALTER ALERT](/sql-reference/sql/alter-alert).

The [SUSPEND\_ALERT\_AFTER\_NUM\_FAILURES](/sql-reference/parameters#label-suspend-alert-after-num-failures) parameter can also be set at the account, database, or schema level.
The setting applies to all alerts contained in the modified object.
Note that explicitly setting the parameter at a lower level overrides the parameter value set at a higher level.

When an alert is automatically suspended:

- The alert no longer runs on its schedule until you resume it.
- [SHOW ALERTS](/sql-reference/sql/show-alerts) reports the alert in the `SUSPENDED` state
  with `was_auto_suspended = TRUE`.
- In [ALERT\_HISTORY](/sql-reference/functions/alert_history), the execution that triggered
  auto-suspension is marked with `WAS_AUTO_SUSPENDED = TRUE`.

To resume an auto-suspended alert, execute the [ALTER ALERT … RESUME](/sql-reference/sql/alter-alert) command.

## Modifying an alert

To modify the properties of an alert, execute the [ALTER ALERT](/sql-reference/sql/alter-alert) command.

Note

- You must be the owner of the alert to modify the properties of the alert.
- You cannot change an [alert on new data](#label-alerts-type-streaming) to an
  [alert on a schedule](#label-alerts-type-scheduled). Similarly, you cannot change an alert on a schedule to an alert
  on new data.

For example:

- To change the warehouse for the alert named `my_alert` to `my_other_warehouse`, execute:

  Copy code

  ```
  ALTER ALERT my_alert SET WAREHOUSE = my_other_warehouse;
  ```
- To change the schedule for the alert named `my_alert` to be evaluated every 2 minutes, execute:

  Copy code

  ```
  ALTER ALERT my_alert SET SCHEDULE = '2 minutes';
  ```
- To change the condition for the alert named `my_alert` so that you are alerted if any rows in the table named `gauge` have
  values greater than `300` in the `gauge_value` column, execute:

  Copy code

  ```
  ALTER ALERT my_alert MODIFY CONDITION EXISTS (SELECT gauge_value FROM gauge WHERE gauge_value>300);
  ```
- To change the action for the alert named `my_alert` to `CALL my_procedure()`, execute:

  Copy code

  ```
  ALTER ALERT my_alert MODIFY ACTION CALL my_procedure();
  ```

## Dropping an alert

To drop an alert, execute the [DROP ALERT](/sql-reference/sql/drop-alert) command. For example:

Copy code

```
DROP ALERT my_alert;
```

To drop an alert without raising an error if the alert does not exist, execute:

Copy code

```
DROP ALERT IF EXISTS my_alert;
```

Note

You must be the owner of the alert to drop the alert.

## Viewing details about an alert

To list the alerts that have been created in an account, database, or schema, execute the [SHOW ALERTS](/sql-reference/sql/show-alerts)
command. For example, to list the alerts that were created in the current schema, run the following command:

Copy code

```
SHOW ALERTS;
```

This command lists the alerts that you own and the alerts that you have the MONITOR or OPERATE privilege on.

To view the details about a specific alert, execute the [DESCRIBE ALERT](/sql-reference/sql/desc-alert) command. For example:

Copy code

```
DESC ALERT my_alert;
```

Note

If you are not the owner of the alert, you must have the MONITOR or OPERATE privilege on the alert to view the details of the
alert.

## Cloning an alert

You can clone an alert (either by using [CREATE ALERT … CLONE](/sql-reference/sql/create-alert) or by cloning the
database or schema containing the alert).

If you are cloning a serverless alert, you don’t need to use a role that has the global EXECUTE MANAGED ALERT privilege. However,
you will not be able to resume that alert until the role that owns the alert has been granted the EXECUTE MANAGED ALERT privilege.

## Monitoring the execution of alerts

To monitor the execution of the alerts, you can:

- Check the results of the action that was specified for the alert. For example, if the action inserted rows into a table, you can
  check the table for new rows.
- View the history of alert executions by using one of the following:
  - The [ALERT\_HISTORY](/sql-reference/functions/alert_history) table function in the INFORMATION\_SCHEMA schema.

    For example, to view the executions of alerts over the past hour, execute the following statement:

    Copy code

    ```
    SELECT *
    FROM
      TABLE(INFORMATION_SCHEMA.ALERT_HISTORY(
        SCHEDULED_TIME_RANGE_START
    =>dateadd('hour',-1,current_timestamp())))
    ORDER BY SCHEDULED_TIME DESC;
    ```
  - The [ALERT\_HISTORY](/sql-reference/account-usage/alert_history) view in the ACCOUNT\_USAGE schema in the shared
    SNOWFLAKE database.

In the query history, the name of the user who executed the query will be SYSTEM. (The alerts are run by the
[system service](/user-guide/tasks-intro#label-system-service).)

## Viewing the query history of a serverless alert

To view the query history of a serverless alert, you must be the owner of the alert, or you must use a role that has the
MONITOR or OPERATE privilege on the alert itself. (This differs from alerts that use one your warehouses, which require the
MONITOR or OPERATE privilege on the warehouse.)

For example, suppose that you want to use the `my_alert_role` role when viewing the query history of the alert `my_alert`.
If `my_alert_role` is not the owner of `my_alert`, you must [grant](/sql-reference/sql/grant-privilege) that role the
MONITOR or OPERATE privilege on the alert:

Copy code

```
GRANT MONITOR ON ALERT my_alert TO ROLE my_alert_role;
```

After the role is granted this privilege, you can use the role to view the query history of the alert:

Copy code

```
USE ROLE my_alert_role;
```

Copy code

```
SELECT query_text FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
  WHERE query_text LIKE '%Some condition%'
    OR query_text LIKE '%Some action%'
  ORDER BY start_time DESC;
```
