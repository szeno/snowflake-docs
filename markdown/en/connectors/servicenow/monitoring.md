# Monitoring the Snowflake Connector for ServiceNow®

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

This topic describes how to monitor the state of the Snowflake Connector for ServiceNow® and troubleshoot problems.

## About Monitoring the Connector

To monitor the state of the Snowflake Connector for ServiceNow® and troubleshoot problems, you can access
the connector configuration, error messages and statistics through the following views, which are defined
in the `PUBLIC` schema of [the connector application](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2):

| View Name | Description |
| --- | --- |
| `AGGREGATED_CONNECTOR_STATS` | Provides access to information about a total number of rows updated by the connector (records inserted, modified and deleted) in each full hour. |
| `APP_PROPERTIES` | Provides information to the User Interface about properties supported by the Snowflake Connector for ServiceNow® |
| `CONFIGURED_TABLES` | Provides the list of ServiceNow® tables that have been configured. You can use this view to determine which tables are enabled for synchronization, their ingestion strategy, schedule and other ingestion options. |
| `CONNECTOR_CONFIGURATION` | Provides a list of the values of the configuration settings used by the connector. |
| `CONNECTOR_ERRORS` | Provides access to the errors that occurred during data ingestion. |
| `CONNECTOR_OVERVIEW` | Provides general information about the connector. |
| `CONNECTOR_STATS` | Provides statistics about the ongoing data ingestion process and the amount of data collected by the connector in each ingestion run. |
| `RELOADED_TABLES` | Provides information about the tables that are currently being reloaded. It combines the configuration values from the `CONFIGURED_TABLES` view with the manually provided reload options and gives the reload process overview. |
| `SYNC_STATUS` | Provides the general status of the connector and the ingestion process:   - `PAUSED` - the connector is currently paused or in the middle of resuming and no ingestion of any table is currently ongoing. - `NOT_SYNCING` - the connector is ready to ingest data but has not ingested any data yet. - `SYNCING_DATA` - the connector is ingesting data but there is no table for which ingestion has finished yet. - `LAST_SYNCED` - ingestion for at least one table has finished. The timestamp of the last finished ingestion is provided in LAST\_SYNCED\_AT column. |
| `TABLES_STATE` | Provides access to information about the tables that have ever been enabled for synchronization. This information includes:   - the status of the table - whether it is enabled, disabled or in the middle of reload. - the status of the last ingestion:    - `DONE` means that the fetched data is available in the sync table.   - `RUNNING` means that the download is in progress or the data is already fetched into the event log table but the sync table was not updated yet.   - `FAILED` means that the ingestion run was interrupted because of an error. This may result in only part of the data being downloaded. This won’t cause any data discrepancy, and depending on ingestion strategy some batches might be collected again.   - `DISABLED` means that given table was disabled in the middle of this ingestion run. - the timestamp of the last scheduled synchronization. - the page size used in the requests collecting data for the table. - the status of flattened views creation. - the timestamp of the last time the connector checked if flattened views for the table need to be recreated. |
| `WORKERS_STATE` | Provides access to information about currently ingested tables and when were the worker tasks assigned to them. |

Expand

Show lessSee more

Please note that all the timestamps displayed in the above views are provided in the UTC timezone with no offset, which may
differ from the timezone of the dates displayed by the ServiceNow instance.

The following roles have access to these views:

- The owner of [the connector application](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2) (usually the ACCOUNTADMIN system role).
- Any role with ADMIN or VIEWER application role granted.

## Configuring Email Alerts

You can enable email alerts for the connector. The connector uses the
[Notification System Stored Procedure](/user-guide/notifications/email-stored-procedures)
to send the email notifications. In order to configure alerts, [the connector must be installed first](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-v2).
These email notifications include the number of errors encountered and the type of each error.

### Enabling Email Notifications Using Snowsight

To configure email alerts, navigate to the Snowflake Connector for ServiceNow® application in the Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for ServiceNow®, then select the tile for the connector.
4. In the page for the Snowflake Connector for ServiceNow®, select the **Settings** tab in the upper bar then switch to the
   **Email Alerts** section from the list on the left.
5. Enter the following information in the dialog box:

   | Field | Description |
   | --- | --- |
   | **Email Address** | Single email address where alerts should be sent. You must specify an email address that is associated with the Snowflake account. |
   | **Frequency** | There are two possible values:  - **Immediately** - Errors are summarized and the report is sent as often as the lowest configured ingestion schedule. - **Once per day** - An email message with a summary of all errors is sent once a day at 12PM UTC. |

   Expand

   Show lessSee more

### Disabling Email Notifications Using Snowsight

To disable email alerts, navigate to the Snowflake Connector for ServiceNow® application in Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for ServiceNow®, then select the tile for the connector.
4. In the page for the Snowflake Connector for ServiceNow®, select the **Settings** tab in the upper bar then switch to the
   **Email Alerts** section from the list on the left.
5. Select **Stop receiving alerts**, then confirm by selecting **Stop receiving alerts** again.

Under the hood, a [notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration) object, used to send email
alerts, is created. The name of this integration is the same as the name of
[the connector application](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2)
with an added suffix `_NOTIFICATION_INTEGRATION`. The connector references this object by name.
Changing name of this object or dropping it causes the email alerts functionality to break.

### Enabling Email Notifications Using SQL

To configure email alerts, you must create a [notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration).

After creating the notification integration, you must grant USAGE on this integration to [the connector application](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2).
For example, to grant the following privileges to the connector named `my_connector_servicenow`:

> Copy code
>
> ```
> GRANT USAGE ON INTEGRATION <notification_integration_name> TO APPLICATION <connector_application>;
> ```

To configure and enable email alerts, call the `CONFIGURE_ALERTS` procedure:

> Copy code
>
> ```
> CALL CONFIGURE_ALERTS({
>   'notification_integration_name': '<notification_integration_name>',
>   'email_addresses': ['<email_address>'],
>   'schedule_type': '<schedule>'
> });
> ```

Where:

`notification_integration_name`
:   Identifier for the [notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration) that you created for sending the email alerts.

`email_address`
:   Email address where the email notifications should be sent.

    - You can specify only one email address.
    - The email address must be specified in the ALLOWED\_RECIPIENTS clause of the notification integration.

`schedule`
:   The frequency with which notifications should be sent. Specify one of the following values:

    - ONCE\_PER\_DAY: Send email notifications once a day at 12PM UTC.
    - LOWEST\_INGESTION\_SCHEDULE: Send email notifications immediately after an error occurs.

For example, if you named your connector application MY\_CONNECTOR\_SERVICENOW, use the notification integration `SN_EMAILS`
to send daily email notifications to `john.doe@snowflake.com` email, run the following commands:

> Copy code
>
> ```
> GRANT USAGE ON INTEGRATION SN_EMAILS TO APPLICATION MY_CONNECTOR_SERVICENOW;
>
> CALL CONFIGURE_ALERTS({
>   'notification_integration_name': 'SN_EMAILS',
>   'email_addresses': ['john.doe@snowflake.com'],
>   'schedule_type': 'ONCE_PER_DAY'
> });
> ```

The connector references [notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration) object by name. Changing the name of this object or dropping it
causes the email alerts functionality to break.

### Disabling Email Notifications Using SQL

To disable email notifications, call the `DISABLE_ALERTS()` stored procedure:

> Copy code
>
> ```
> CALL DISABLE_ALERTS();
> ```

If you need to enable email notifications again, see [Enabling Email Notifications Using Snowsight](#label-monitoring-the-servicenow-connector-email-alerts-enabling-v2).
