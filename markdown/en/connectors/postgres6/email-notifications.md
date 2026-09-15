# Setting up Email Notifications for the PostgreSQL connector

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

You can enable email notifications for the connector. The connector uses the
[Notification System Stored Procedure](/user-guide/notifications/email-stored-procedures)
to send email notifications. Setting up email notifications is an optional but recommended action.

## Configuring email notifications

You can configure the connector to send email notifications when errors occur.

On a given schedule, the connector checks whether new errors have occurred. If so, an email containing the number of
errors is sent to specified recipients. Email notifications are sent on an incremental basis, meaning that only new errors
trigger notification. For security reasons, emails contains only information about the number of errors (not the errors
themselves).

To receive email notifications about errors, you must have already created and set up an event table for the account
(to capture the logged errors), and that event table must have CHANGE\_TRACKING set to TRUE.

To configure email notifications do the following:

1. [Create a notification integration](#create-a-notification-integration)
2. [Create a log view for the connector](#create-a-log-view-for-the-connector)
3. [Enable email notifications](#enable-email-notifications)

### Create a notification integration

To send email notifications, the connector uses the notification integration object, which is a Snowflake object that provides
an interface between Snowflake and email services.

To create notification integration, run the following command:

> Copy code
>
> ```
> CREATE NOTIFICATION INTEGRATION <integration_name>
>     TYPE=EMAIL
>     ENABLED=TRUE
>     ALLOWED_RECIPIENTS=('first.last@example.com','first2.last2@example.com');
> ```

Where:

> `integration_name`
> :   Specifies the name of the notification integration.

The connector requires the `USAGE` privilege on the notification integration that is used to send the email.
To grant this privilege, run the following command:

> Copy code
>
> ```
> GRANT USAGE ON INTEGRATION <integration_name> TO APPLICATION <app_db_name>;
> ```

Where:

> `integration_name`
> :   Specifies the name of the notification integration.
>
> `app_db_name`
> :   Specifies the name of the connector database.

More information about creating notification integration can be
found [here](/user-guide/notifications/email-notifications#label-create-email-notification-integration).

### Create a log view for the connector

To configure email notifications you must create a log view for the event table that stores the logged messages from the
connector. You can create the log view in any database and schema, except the database that serves as the connector instance.

Run the following command to create a log view on the event table:

> Copy code
>
> ```
> CREATE SECURE VIEW <logs_view> CHANGE_TRACKING = TRUE AS
>   SELECT *
>   FROM <fully_qualified_event_table_name>
>   WHERE RECORD_TYPE = 'LOG' AND
>   RESOURCE_ATTRIBUTES:"snow.database.name" = '<app_db_name>';
> ```

Where:

> `logs_view`
> :   Specifies the name of the view that you want to create.
>
> `fully_qualified_event_table_name`
> :   Specifies the fully-qualified name of the event table.
>
> `app_db_name`
> :   Specifies the name of the connector database.

The connector requires the `SELECT` privilege on the view. It also requires `USAGE` privilege both on the database
and the schema that contains the view. To grant these privileges, run the following commands:

> Copy code
>
> ```
> GRANT USAGE ON DATABASE <logs_db> TO APPLICATION <app_db_name>;
> GRANT USAGE ON SCHEMA <logs_db>.<logs_schema> TO APPLICATION <app_db_name>;
> GRANT SELECT ON VIEW <logs_db>.<logs_schema>.<logs_view> TO APPLICATION <app_db_name>;
> ```

Where:

> `logs_db`
> :   Specifies the name of the database that contains the view that you just created.
>
> `logs_schema`
> :   Specifies the name of the schema that contains the view that you just created.
>
> `logs_view`
> :   Specifies the name of the view that you just created.
>
> `app_db_name`
> :   Specifies the name of the connector database.

### Enable email notifications

After creating the email notification integration and the log view, run the following command to enable email notifications
from the connector:

> Copy code
>
> ```
> CALL PUBLIC.CONFIGURE_ALERTS('<integration_name>', '<logs_db>.<logs_schema>.<logs_view>', '<schedule>', ['<email_address_1>' [, ... '<email_address_2>']]);
> ```

Where:

> `integration_name`
> :   Specifies the name of the notification integration.
>
> `logs_db`
> :   Specifies the name of the database that contains the view that you created in the previous step.
>
> `logs_schema`
> :   Specifies the name of the schema that contains the view that you created in the previous step.
>
> `logs_view`
> :   Specifies the name of the view that you created in the previous step.
>
> `schedule`
> :   Specifies the schedule or frequency at which the connector should check for errors and send a notification. For details
>     on specifying the schedule or frequency, see [SCHEDULE parameter](/sql-reference/sql/create-task#label-create-task-schedule).
>
> `['email_address_1' [, ... 'email_address_2']]`
> :   Specifies the array of one or more quoted email addresses that can receive email notifications from the connector. The email
>     addresses in this array must be in the ALLOWED\_RECIPIENTS parameter specified in the [email notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration).

To change the configuration of an email notifications, use the above command providing the revised parameters.

### Disabling Email Notifications

To disable email notifications, run the following command:

> Copy code
>
> ```
> CALL PUBLIC.DISABLE_ALERTS();
> ```

This command removes all email addresses that were added during the initial configuration.

## Next steps

After completing these procedures, follow the steps in [Setting up the Snowflake Connector for PostgreSQL Agent container](/connectors/postgres6/install-agent)
