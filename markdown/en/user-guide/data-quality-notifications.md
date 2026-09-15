# Sending notifications for data quality issues

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake provides the following features that identify when the value returned by a data metric function (DMF) indicates a data
quality issue:

- [Expectations](/user-guide/data-quality-expectations) — Lets you use a Boolean expression to compare the output of a DMF to
  an expected value. A return value that doesn’t match the Boolean expression is considered an expectation violation.
- [Anomaly detection](/user-guide/data-quality-anomaly) — Snowflake automatically detects when the output of the DMF
  constitutes an anomaly. An anomaly occurs when the value returned by a DMF is above or below an expected range based on historical
  data.

You can send a notification when either of these features identifies a data quality issue. After
Snowflake is configured, a notification is sent whenever an expectation is violated or Snowflake identifies an anomaly.

You enable notifications at the database level. Once enabled, all objects with an associated DMF in that database generate
notifications when there is a quality issue. Within a database that is enabled for notifications, you can turn off notifications for
a specific association between an object in the database and a DMF.

## Workflow

Configuring Snowflake to send notifications for data quality issues consists of the following tasks:

1. [Configure who receives notifications](#label-data-quality-notifications-create).
2. [Grant access control privileges](#label-data-quality-notifications-grant) to the database owner.
3. Modify the database to [configure and turn on notifications](#label-data-quality-notifications-database).

For an end-to-end example of this workflow, see [Extended example](#label-data-quality-notifications-example).

## Configure who receives notifications

Define notification recipients by adding email addresses directly, or by creating a notification integration.

A notification integration is a Snowflake object that provides an interface between Snowflake and third-party messaging services. To
send notifications for data quality issues, create a notification integration for the messaging service. Data quality monitoring
supports the following types of notifications:

- Email notifications
- Notifications sent via external systems such as Slack, using webhooks.

If you want to add email addresses without creating an email integration, see [Configure database settings for data quality notifications](#label-data-quality-notifications-database).

### Send notifications via email

To send notifications to a list of email addresses, execute a
[CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-email) statement to create an integration
of type `EMAIL`. Your integration must use the ALLOWED\_RECIPIENTS parameter to specify a list of email addresses where
notifications are sent. You can only add email addresses that are verified. For information about verifying an email address, see
[Verify the email addresses of the email notification recipients](/user-guide/notifications/email-notifications#label-email-notification-verify-address).

Tip

You can send email notifications to a distribution list or group that is managed outside of Snowflake. For more information, see
the related [Knowledge Base article](https://community.snowflake.com/s/article/How-to-send-Alerts-and-Notifications-to-an-email-distribution-list-or-group-and-manage-the-group-membership-outside-of-Snowflake).

For example, to create a notification integration so user `joe.smith@example.com` can be emailed when there is a data quality
issue, run the following command:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_email_int
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS = ('joe.smith@example.com');
```

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

### Send notifications by using a webhook for an external system

You can send data quality notifications via an external system by creating a webhook integration. For a list of the external
systems that you can use, see [Sending webhook notifications](/user-guide/notifications/webhook-notifications).

To use webhooks to send data quality notifications, complete the following steps:

1. [Create a secret for a webhook URL](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret).
2. [Create a webhook notification integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-integration).

For example, if you want to use Slack to send notifications, you might run the following commands:

Copy code

```
CREATE OR REPLACE SECRET my_slack_webhook_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = 'T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX';

CREATE OR REPLACE NOTIFICATION INTEGRATION my_slack_webhook_int
  TYPE=WEBHOOK
  ENABLED=TRUE
  WEBHOOK_URL='https://hooks.slack.com/services/SNOWFLAKE_WEBHOOK_SECRET'
  WEBHOOK_SECRET=my_db.sch1.my_slack_webhook_secret
  WEBHOOK_BODY_TEMPLATE='{"text": "SNOWFLAKE_WEBHOOK_MESSAGE"}'
  WEBHOOK_HEADERS=('Content-Type'='application/json');
```

## Grant privileges

To set up notifications for objects within a database, the database owner must have the following privileges:

- MANAGE DATA QUALITY on the account
- USAGE on any notification integration that is used to send notifications. This is required only if a notification integration is used.

For example, suppose a user with the `data_steward` role is the owner of database `my_db`. To use the notification integration
`my_email_int` to send notifications for quality issues uncovered by DMFs associated with tables and views in `my_db`, run the
following commands:

Copy code

```
GRANT MANAGE DATA QUALITY ON ACCOUNT TO ROLE data_steward;
GRANT USAGE ON INTEGRATION my_email_int TO ROLE data_steward;
```

## Configure database settings for data quality notifications

You can turn on notifications for a database by
running an [ALTER DATABASE](/sql-reference/sql/alter-database) statement with the DATA\_QUALITY\_MONITORING\_SETTINGS property.
This property uses a [dollar-quoted](/sql-reference/data-types-text#label-dollar-quoted-string-constants) YAML specification to define the notification settings.

DATA\_QUALITY\_MONITORING\_SETTINGS specifies the following aspects of data quality notifications:

- Whether notifications are enabled or disabled for the database.
- Which email addresses receive notifications (specified without a notification integration).
- Which [notification integrations](/sql-reference/sql/create-notification-integration), if any, send the notifications. You can specify
  multiple notification integrations to send notifications through different channels.
- How often notifications are sent.
- Whether the notifications include the name of the specific table or view that has the data quality issue. This metadata helps
  quickly identify and address the problem.

For example:

> Copy code
>
> ```
> ALTER DATABASE my_db SET DATA_QUALITY_MONITORING_SETTINGS =
>   $$
>   notification:
>     enabled: TRUE
>     email_recipients: [ 'joe@example.com', 'mary@example.com']
>     integrations:
>       - WEBHOOK_NOTIFY_INT
>     cooldown_hours: 4
>     metadata_included: TRUE
>   $$;
> ```

This example specifies the following configuration:

- Notifications are enabled for the database `my_db`.
- Notifications are sent to two email addresses and one external channel.
- Notifications aren’t sent more frequently than once every four hours.
- Notifications include metadata that identifies the object and its associated DMF.

## Turn off notifications for a specific DMF association

By default, after you turn on notifications for a database, data quality issues in any object within the database generate a
notification. You can turn off notifications for a specific association between an object and a DMF to prevent notifications from
being sent. To turn off notifications for an association, run an ALTER <object> MODIFY DATA METRIC FUNCTION statement to set the
DATA\_QUALITY\_NOTIFICATION parameter to FALSE.

For example, suppose notifications are turned on for the database that contains view `v2`. If you don’t want notifications to be
sent when the BLANK\_COUNT DMF finds quality issues with column `c1`, run the following command:

Copy code

```
ALTER VIEW v2
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.BLANK_COUNT ON (c1)
    SET DATA_QUALITY_NOTIFICATION = FALSE;
```

## Determine whether notifications are turned on

The [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) function returns information about the association between an
object and a DMF. The output includes a column `data_quality_notification_status`, which you can use to determine whether
notifications are turned on for the association.

## Extended example

Suppose you have the following items in your account:

- A database `my_db` that contains two tables (`t1` and `t2`) and one view (`v1`).
- Tables `t1` and `t2` that are associated with the ROW\_COUNT DMF, and anomaly detection is turned on for both associations.
- Role `analyst` is the owner of `my_db`.
- View `v1` is associated with the NULL\_COUNT DMF, and there is an expectation defined for the association.

You want users to receive an email when there is an anomaly in tables `t1` or `t2`, but you don’t want a notification sent when
there is a quality issue with view `v1`.

Note

This example demonstrates how to use a notification integration to specify email addresses. You can also specify email addresses directly
when running the ALTER DATABASE command.

1. [Create a notification integration](#label-data-quality-notifications-create) that indicates who should receive
   notifications when there is a data quality issue:

   Copy code

   ```
   CREATE NOTIFICATION INTEGRATION notify_int
     TYPE=EMAIL
     ENABLED=TRUE
     ALLOWED_RECIPIENTS=('joe.smith@example.com');
   ```
2. [Grant privileges](#label-data-quality-notifications-grant) to the role `analyst`,
   which is the owner of `my_db`:

   Copy code

   ```
   GRANT MANAGE DATA QUALITY ON ACCOUNT TO ROLE analyst;
   GRANT USAGE ON INTEGRATION notify_int TO ROLE analyst;
   ```
3. [Configure the database settings](#label-data-quality-notifications-database) to turn on notifications. These notifications
   will include the name of the object that had the data quality issue.

   Copy code

   ```
   ALTER DATABASE my_db SET DATA_QUALITY_MONITORING_SETTINGS =
     $$
     notification:
    enabled: TRUE
    integrations:
      - NOTIFY_INT
    metadata_included: TRUE
     $$
   ```
4. [Turn off notifications](#label-data-quality-notifications-turn-off) for an association between view `v1` and the
   NULL\_COUNT DMF:

   Copy code

   ```
   ALTER VIEW v1
     MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT ON (c1)
    SET DATA_QUALITY_NOTIFICATION = FALSE;
   ```
