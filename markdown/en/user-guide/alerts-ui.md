# Alerts in Snowsight

You can set up [alerts](/user-guide/alerts) for Snowflake features in Snowsight. This user interface simplifies
how you monitor your Snowflake account.

Rather than executing SQL statements to create and manage alerts, you can use wizards in Snowsight to create, manage,
and monitor your alerts.

The alerts management feature in Snowsight provides the following benefits:

- **Centralized visibility of alerts:** In the Snowflake Alerts Center, you can view all alerts, the history of these alerts, and
  the execution status of these alerts.
- **Templates for creating alerts:** You can quickly create alerts for the following features by using the alert templates
  provided in the Snowflake Alerts UI. Note: Once an alert is generated from a template, it is equivalent to any other alert with
  regard to lifecycle management, and contains no special properties.

  - [Tasks](/user-guide/tasks-intro)
  - [Openflow](/user-guide/data-integration/openflow/about)
  - [Data quality](/user-guide/data-quality-intro)
  - [Dynamic tables](/user-guide/dynamic-tables/overview)
  - [Iceberg tables](/user-guide/tables-iceberg-catalog-linked-database) (catalog-linked databases)
- **Proactive monitoring of Snowflake features:** You can easily configure notifications for failures, latency, or data anomalies
  to ensure your pipelines and budgets remain healthy.

## Prerequisites

Before you can use Snowsight to create, monitor, and manage alerts, you must fulfill the following prerequisites:

- [Prerequisites for task alerts](#prerequisites-for-task-alerts)
- [Prerequisites for Openflow alerts](#prerequisites-for-openflow-alerts)
- [Prerequisites for data quality alerts](#prerequisites-for-data-quality-alerts)
- [Prerequisites for dynamic table alerts](#prerequisites-for-dynamic-table-alerts)
- [Prerequisites for Iceberg catalog-linked database alerts](#prerequisites-for-iceberg-catalog-linked-database-alerts)
- [Setting up notifications for alerts](#setting-up-notifications-for-alerts)
- [Creating a role for accessing alerts in Snowsight](#creating-a-role-for-accessing-alerts-in-sf-web-interface)

### Prerequisites for task alerts

If you plan to create, manage, and monitor alerts on [tasks](/user-guide/tasks-intro), you must do the following:

- Set the severity level of logged messages that you want to capture for task events.

  The task alerts monitor error messages that are logged to the event table. You must set the [LOG\_LEVEL](/sql-reference/parameters#label-log-level) parameter to
  at least `ERROR` for the tasks that you want to monitor. You can set this parameter on one of the following types of objects:

  - To set the severity level to ERROR on all objects in the account (including tasks), execute
    [ALTER ACCOUNT SET LOG\_LEVEL](/sql-reference/sql/alter-account):

    Copy code

    ```
    ALTER ACCOUNT SET LOG_LEVEL = ERROR;
    ```

    Note

    This setting also affects the messages logged by UDFs, stored procedures, and dynamic tables.
  - To set the severity level to ERROR on all objects in a database containing the tasks, execute
    [ALTER DATABASE … SET LOG\_LEVEL](/sql-reference/sql/alter-database):

    Copy code

    ```
    ALTER DATABASE my_task_db SET LOG_LEVEL = ERROR;
    ```

    Note

    This setting also affects the messages logged by UDFs, stored procedures, and dynamic tables in that database.
  - To set the severity level to ERROR for specific tasks, execute
    [ALTER TASK … SET LOG\_LEVEL](/sql-reference/sql/alter-task):

    Copy code

    ```
    ALTER TASK my_task SET LOG_LEVEL = ERROR;
    ```
- Verify the privileges that have been granted to the role that you plan to use to access Snowsight.

  That role must be granted the privileges to query the [TASK\_HISTORY view](/sql-reference/account-usage/task_history) and
  [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) in the ACCOUNT\_USAGE schema.

  For information, see [Enabling other roles to use schemas in the SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles).

### Prerequisites for Openflow alerts

The [Openflow](/user-guide/data-integration/openflow/about) alerts monitor events recorded to an event table. Make sure that
Openflow is configured to log events. For information, see the following sections:

- [[Optional] Configure an Openflow-specific event table](/user-guide/data-integration/openflow/setup-openflow-byoc#label-openflow-event-table) (if you are using Openflow BYOC)
- [[Optional] Configure an Openflow-specific event table](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment#label-openflow-spcs-event-table) (if you are using Openflow Snowflake)

### Prerequisites for data quality alerts

Make sure that Data Metric Functions (DMF) are registered and are running against the tables and views that you want to monitor.

For information, see [Use SQL to set up data metric functions](/user-guide/data-quality-working).

### Prerequisites for dynamic table alerts

The [dynamic table](/user-guide/dynamic-tables/overview) alerts monitor refresh status events that are recorded to an event
table. Make sure that event logging is configured for the dynamic tables that you want to monitor, including the severity
level needed for refresh failures and upstream failures.

For information, see [Set up alerts with the event table](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitor-event-table-alerts).

### Prerequisites for Iceberg catalog-linked database alerts

The Iceberg alerts monitor events from [catalog-linked databases](/user-guide/tables-iceberg-catalog-linked-database). Make sure
that you have a catalog-linked database with a catalog integration configured. Generic Iceberg tables that aren’t part of a
catalog-linked database don’t emit the events that these alerts monitor.

For information, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

### Setting up notifications for alerts

When you create an alert in Snowsight, you can configure the alert to send a notification
through email or a webhook.

To send notifications, you must use a notification integration. You can either use an existing
notification integration or create a new one:

- To find existing notification integrations, run [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)
  and use the [pipe operator](/sql-reference/operators-flow) to filter the results:

  Copy code

  ```
  -- Find email integrations
  SHOW NOTIFICATION INTEGRATIONS ->> SELECT * FROM $1 WHERE "type" = 'EMAIL';

  -- Find webhook integrations
  SHOW NOTIFICATION INTEGRATIONS ->> SELECT * FROM $1 WHERE "type" = 'WEBHOOK';
  ```
- To create a new email notification integration, see [Sending email notifications](/user-guide/notifications/email-notifications).
- To create a new webhook notification integration, see
  [CREATE NOTIFICATION INTEGRATION (webhooks)](/sql-reference/sql/create-notification-integration-webhooks).

### Creating a role for accessing alerts in Snowsight

To allow users other than the account administrator to access alerts in Snowsight, you can create a custom role that has
been granted all of the privileges needed to create, manage, and monitor alerts. You can grant this role to users and other roles
that need to use alerts in Snowsight.

For example, suppose that you want to create a role named `my_alert_center_role` for this purpose. To create this role, complete
the following steps:

1. Switch to a role that is allowed to create your custom role (for example, the ACCOUNTADMIN role):

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ```
2. Create your custom role:

   Copy code

   ```
   CREATE OR REPLACE ROLE my_alert_center_role;
   ```
3. Grant the USAGE privilege on a warehouse that you plan to use when accessing alerts in Snowsight. You must grant this
   privilege because some of the features require an active warehouse.

   Copy code

   ```
   GRANT USAGE ON WAREHOUSE my_warehouse TO ROLE my_alert_center_role;
   ```
4. Grant the privileges for executing alerts to the role:

   - If you plan to create alerts that use a specific warehouse for execution, grant the following privileges to that role:

     - EXECUTE ALERT privilege on the account
     - USAGE privilege on the warehouse that you want to use for the alert

     For example:

     Copy code

     ```
     GRANT EXECUTE ALERT ON ACCOUNT TO ROLE my_alert_center_role;
     GRANT USAGE ON WAREHOUSE my_warehouse TO ROLE my_alert_center_role;
     ```
   - If you plan to create a serverless alert, grant the EXECUTE MANAGED ALERT privilege on the account:

     Copy code

     ```
     GRANT EXECUTE MANAGED ALERT ON ACCOUNT TO ROLE my_alert_center_role;
     ```
5. Grant the [privileges required to create alerts in a database and schema](/user-guide/alerts#label-alerts-privileges-granting).

   For example, if you plan to create the alerts in a database named `my_alerts_database` and in a schema named
   `my_alert_schema`, grant the USAGE privilege on that database and schema, and grant the CREATE ALERT privilege on the schema:

   Copy code

   ```
   GRANT USAGE ON DATABASE my_alerts_database TO ROLE my_alert_center_role;
   GRANT USAGE ON SCHEMA my_alerts_schema TO ROLE my_alert_center_role;
   GRANT CREATE ALERT ON SCHEMA my_alerts_schema TO ROLE my_alert_center_role;
   ```
6. Grant the USAGE privilege on the
   [email notification integration](#label-alerts-center-prerequisites-notification) that you set up earlier:

   Copy code

   ```
   GRANT USAGE ON INTEGRATION my_email_int TO ROLE my_alert_center_role;
   ```
7. Grant the application role that [allows access to the default event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles):

   Copy code

   ```
   GRANT APPLICATION ROLE SNOWFLAKE.EVENTS_VIEWER TO ROLE my_alert_center_role;
   ```
8. If you plan to set up alerts for data quality monitoring, grant the application role and privileges required to monitor data
   quality and execute data metric functions:

   Copy code

   ```
   GRANT APPLICATION ROLE SNOWFLAKE.DATA_QUALITY_MONITORING_VIEWER TO ROLE my_alert_center_role;
   GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE my_alert_center_role;
   ```
9. Grant the custom role to users or other roles:

   Copy code

   ```
   GRANT ROLE my_alert_center_role TO USER my_user;
   GRANT ROLE my_alert_center_role TO ROLE my_other_role;
   ```

## Accessing alerts in Snowsight

To access the alerts in Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Alerts**.

You can view a list of existing alerts and filter the alerts by the alert name and status. You can also view the status of recent
executions of alerts.

## Creating a new alert

You can create a new alert by using one of the templates provided.

Note

You can also create an alert from a template with SQL by using
[CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert#label-create-alert-from-template-syntax). Use
[SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates) and
[SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) to discover the available templates and
their variables.

To create an alert in Snowsight, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Alerts**, and select **+ Alert**.
3. In the **Name** field, enter a name for the alert.
4. In the **Description** field, describe the purpose of the alert.
5. From the **Location** menu, choose the database and schema in which you want to create the alert.
6. From the **Compute Type** menu, choose one of the following options:

   - To create a [serverless alert](/user-guide/alerts#label-alerts-serverless-compute), choose **Serverless**.
   - To specify the
     [warehouse that you want to use for the alert](/user-guide/alerts#label-alerts-warehouse-user-managed), choose **Warehouse**.

     If you selected this option, choose the warehouse from the **Warehouse** menu.
7. If you want to activate the alert after it is created, select **Activate alert upon creation**.

   If you don’t select this option, the newly created alert is suspended. You must resume the alert to make the alert active.
8. Select **Next**.
9. From the **Select warehouse** menu, choose the warehouse that you want to use for the alert.
10. From the **Alert template** menu, choose one of the template groups for Snowflake features, and choose the template that
    you want to use to create the alert.

The following table lists the template groups and templates that you can choose.

| Template group | Template | Description |
| --- | --- | --- |
| **DATA\_QUALITY** | **Anomaly detection alert** | Monitors for [anomalies detected in data quality metrics](/user-guide/data-quality-anomaly), triggering an alert when unusual patterns or outliers are identified. |
|  | **Expectation violations alert** | Monitors for [data quality expectation violations](/user-guide/data-quality-expectations), triggering an alert when defined expectations are violated. |
| **DYNAMIC\_TABLES** | **Refresh failure alert** | Monitors [dynamic table](/user-guide/dynamic-tables/overview) refresh failures, triggering an alert when a dynamic table’s own refresh fails. |
|  | **Upstream failure alert** | Monitors [dynamic table](/user-guide/dynamic-tables/overview) upstream failures, triggering an alert when a refresh fails because of an upstream dependency. |
| **ICEBERG** | **Refresh status alert** | Monitors auto-refresh status changes for tables in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), triggering an alert when refresh leaves a healthy state. |
|  | **Discovery failure alert** | Monitors discovery and sync failures for a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), triggering an alert when catalog objects fail to sync. |
| **OPENFLOW** | **Connector backpressure (object count)** | Monitors the connector queue count to determine if it exceeds the backpressure threshold, which can indicate that the downstream system can’t keep up with the data flow rate. |
|  | **Connector backpressure (bytes)** | Monitors the connector queued bytes to determine if it exceeds the backpressure threshold, which can indicate that there is memory pressure in the data pipeline. |
|  | **High queued bytes alert** | Monitors the connector queue bytes to determine if it approaches the backpressure threshold (>80%), which can provide an early warning before backpressure occurs. |
|  | **High queued count alert** | Monitors the connector queue object count to determine if it approaches the backpressure threshold (>80%), which can provide an early warning before backpressure occurs. |
|  | **No data alert** | Monitors for connectors that have an active processing time but are not receiving or sending any data, which can indicate potential data flow issues. |
|  | **Runtime high error rate alert** | Monitors the Openflow runtime processors for a high volume of ERROR-level logs, which can indicate processing failures. |
|  | **Table replication failure alert** | Monitors for table replication transitions to a FAILED state, which can indicate a critical data synchronization issue. |
| **TASKS** | **Error rate alert** | Triggers an alert when the cumulative task error rate exceeds a specified threshold. |

Expand

Show lessSee more

11. Fill in the configuration fields for the alert. The fields depend on the template that you have chosen.
12. Select the scope that you want to monitor. The scope determines the objects that are monitored for the alert. For example, to
    monitor all objects in the account, choose **Account** from the **Scope** menu.
13. From the **Schedule** menu, choose the type of schedule that you want to use to run the alert:

- To run the alert only when new objects are added (for example, new rows inserted into a table that you are monitoring),
  select **When new events are detected**.
- To run the alert on a regular schedule, and select the frequency for executing the alert (for example, every 10 minutes),
  select **On a schedule**.

14. From the **Notification integration** menu, choose the
    [notification integration that you created earlier](#label-alerts-center-prerequisites-notification).
    You can use an email integration or a
    [webhook integration](/sql-reference/sql/create-notification-integration-webhooks).
15. If you selected an email integration, from the **Email recipients** menu, choose the email
    addresses of the people to notify when the alert is triggered.
16. Select **Create**.

Note

- The template wizard generates the SQL statements for creating the alert. If you need to
  customize the alert further, you can modify those statements directly.
- The alert is visible only if your current role has the MONITOR or OWNERSHIP privilege on the
  alert.

## Viewing the details of an alert

To view the details of a specific alert, select the alert’s row in the alerts list. Snowsight
opens the alert detail page, which shows the following information:

- **Recent execution history**: A table of recent executions for the alert, including the completion
  time, status (for example, **Triggered** or **Condition not met**), the condition and action
  SQL that ran, and the corresponding query IDs. You can filter by time range and status, and load
  additional executions.
- **Description**: The comment or description set on the alert.
- **Details**: Metadata about the alert, including the alert name, status (Started or Suspended),
  owner role, database, schema, warehouse, and schedule.
- **Condition**: The SQL statement that represents the alert’s condition. This is the `IF(EXISTS(...))`
  block of the alert.
- **Action**: The SQL statement that the alert executes when the condition is met. This is the
  `THEN` block of the alert.

### Monitoring alert executions

In the recent execution history table on the alert detail page, the **Status** column shows the
state of each execution. The possible states include:

- **Triggered**: The condition evaluated to TRUE and the action was executed.
- **Condition not met**: The condition evaluated to FALSE and no action was taken.

For a full list of possible states and their meanings, see the STATE column in
[ALERT\_HISTORY](/sql-reference/functions/alert_history).

To investigate a failed execution, check the **Condition query ID** and **Action query ID**
columns. You can use these query IDs to look up the SQL\_ERROR\_CODE and SQL\_ERROR\_MESSAGE for the
execution in [ALERT\_HISTORY](/sql-reference/functions/alert_history), which provide the
specific error code and a description of what went wrong.

## Editing an alert

To edit an alert from the alert detail page, select [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) in the top-right corner and
choose **Edit**. Snowsight opens the edit dialog with two tabs: **General** and
**Config**.

### Editing general alert properties

On the **General** tab, you can modify the following properties of the alert:

- **Name**: The name of the alert. This field is read-only for existing alerts.
- **Comment**: A description of what the alert monitors. This maps to the COMMENT property in
  [ALTER ALERT](/sql-reference/sql/alter-alert).
- **Compute Type**: Whether the alert uses a [serverless](/user-guide/alerts#label-alerts-serverless-compute)
  compute model or a [specified warehouse](/user-guide/alerts#label-alerts-warehouse-user-managed). If you choose
  **Warehouse**, select the warehouse from the **Warehouse** menu.
- **Schedule**: How often the alert runs. Choose **On a schedule** and set the frequency (for
  example, every 30 minutes).

Select **Save** to apply the changes.

### Editing the configuration of an alert

On the **Config** tab, you can edit the [configuration](/user-guide/alerts#label-alerts-config) (CONFIG) of the
alert. When an alert is created from a template, the template sets a configuration that contains the
tunable parameters for the alert (for example, thresholds, notification targets, and monitoring
scope). The alert’s condition and action SQL read these values at runtime through
[SYSTEM$GET\_ALERT\_CONFIG](/sql-reference/functions/system_get_alert_config).

Editing the configuration lets you change the alert’s business logic without modifying the
underlying SQL statements.

Depending on the structure of the configuration, Snowsight displays one of two editing
experiences.

#### Editing a template configuration

If the alert was created from a template and the configuration retains the structure that the
template expects, Snowsight displays a rich editing form. Each field in the configuration
is displayed with a human-readable label and a description of expected values. The specific fields
depend on the template, but common examples include:

- A **threshold** value that triggers the alert (for example, an error rate between 0.0 and 1.0).
- A **notification method** such as EMAIL or WEBHOOK, with related fields for the integration and
  recipients.
- A **scope** that controls which objects the alert monitors (for example, ACCOUNT, DATABASE, or
  SCHEMA), with optional filters to narrow the scope further.

When you change these fields and select **Save**, Snowsight updates the CONFIG JSON on
the alert. The alert’s condition and action SQL then use the new values the next time the alert
runs.

#### Editing a flat key-value configuration

If the configuration doesn’t match the structure that the template expects (for example, if you
modified the CONFIG through SQL and changed its schema), Snowsight falls back to a flat
key-value editor.

In this view, the configuration is displayed as a list of key-value pairs. You can toggle between
two modes:

- **Key-value**: Edit each key-value pair individually.
- **JSON**: View and edit the raw JSON configuration directly.

Caution

The configuration values influence the alert’s condition and action logic, but they aren’t
managed parameters with a deep contract with Snowflake. The CONFIG is a JSON string that the
alert’s SQL reads at runtime, and the template’s SQL is responsible for interpreting these
values.

Changing configuration values changes the runtime behavior of the alert’s SQL. Incorrect values
(for example, a non-numeric value for a threshold or an invalid email address) can cause the alert
to malfunction or produce unexpected results. Review the template’s documentation or the alert’s
SQL before modifying configuration values.

For more information about how the CONFIG parameter works at the SQL level, see
[Passing configuration to an alert](/user-guide/alerts#label-alerts-config).
