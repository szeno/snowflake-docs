# Error notifications for replication and failover groups

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can receive error notifications for refresh operation failures by setting a notification integration for a primary replication
or failover group.

## Error notifications for refresh operation failures

When you enable error notifications for a replication or failover group, a notification is sent via the designated email, cloud messaging
service, or the webhook when a refresh operation fails.

Notifications include the following information:

- Source and target account names.
- Source and target regions (and region group, if applicable).
- Primary and secondary replication or failover group name.
- Timestamp when the error occurred.
- Error code and message.
- Source and target login URL.

## Error notifications and failover

Notifications are enabled on the primary replication or failover group and sent using a notification integration. The
notification integration is not required to be replicated to the target account. In the case of failover, if the notification
integration has been replicated, or there is an existing notification integration with the same name, in the newly promoted
source account, error notifications continue to be sent.

If the notification integration is not available, error notifications are not sent for refresh operation failures.

## Prerequisite: Notification integration for error notifications

A notification integration is required to send error notifications. The notification integration must be one of the
following types to send email notifications on refresh operation failures:

TYPE = EMAIL:
:   The email notification integration must have at least one verified email address in the DEFAULT\_RECIPIENTS list.

    For more information about creating an email notification with a default list of recipients, see
    [Specify a default list of recipients and a default subject line](/user-guide/notifications/email-notifications#label-create-notification-integration-email-default-addresses).

TYPE = QUEUE:
:   You can use a notification integration that is configured to push notifications to a messaging service for any of the
    cloud providers supported by Snowflake. You must set the notification integration TYPE parameter to QUEUE and the DIRECTION
    parameter to OUTBOUND.

    For more information, see [Sending notifications to cloud provider queues (Amazon SNS, Google Cloud PubSub, and Azure Event Grid)](/user-guide/notifications/queue-notifications).

TYPE = WEBHOOK:
:   You can use a notification integration that is configured to push notifications to a webhook for any of the external systems
    supported by Snowflake. Set the notification integration TYPE parameter to WEBHOOK. You may also need to create a secret
    (if required by the external system).

    For more information, see [Sending webhook notifications](/user-guide/notifications/webhook-notifications).

### Create a notification integration (TYPE = EMAIL)

To create an email notification integration named `my_notification_int` with email address `first.last@example.com`, follow
these steps:

1. Ensure that the email address `first.last@example.com` [has been verified](/user-guide/notifications/email-notifications#label-email-notification-verify-address).
2. Create the notification integration by executing the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-email) command. For example:

   Copy code

   ```
   CREATE NOTIFICATION INTEGRATION my_notification_int
     TYPE = EMAIL
     ENABLED = TRUE
     DEFAULT_RECIPIENTS = ('first.last@example.com');
   ```

### Create a notification integration (TYPE = QUEUE)

To create a notification integration for pushing notifications to a cloud provider queue, follow the instructions provided for the
currently supported cloud provider queues:

- [Creating a notification integration to send notifications to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns)
- [Creating a notification integration to send notifications to a Microsoft Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid)
- [Creating a notification integration to send notifications to a Google Cloud Pub/Sub topic](/user-guide/notifications/creating-notification-integration-google-pubsub)

### Create a notification integration (TYPE = WEBHOOK)

To create a notification integration for pushing notifications to an external system webhook, follow the instructions provided for
the currently supported external system webhooks:

- Creating a [Slack secret](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret-slack) and [Slack notification integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-integration-slack)
- Creating a [Microsoft Teams secret](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret-teams) and [Microsoft Teams notification integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-integration-teams)
- Creating a [PagerDuty secret](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret-pagerduty) and [PagerDuty notification integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-integration-pagerduty)

Important

The webhook notification integration must specify the WEBHOOK\_BODY\_TEMPLATE parameter with `SNOWFLAKE_WEBHOOK_MESSAGE`
as a placeholder value. When the notification is sent, the placeholder is replaced with the contents of the replication
error notification, as described in [Error notifications for refresh operation failures](#error-notifications-for-refresh-operation-failures).

The format for specifying WEBHOOK\_BODY\_TEMPLATE depends on the external system:

- For Slack or Microsoft Teams, WEBHOOK\_BODY\_TEMPLATE utilizes the following single-value JSON object
  format as its value:

  Copy code

  ```
  WEBHOOK_BODY_TEMPLATE='{"text": "SNOWFLAKE_WEBHOOK_MESSAGE"}'
  ```
- For PagerDuty, WEBHOOK\_BODY\_TEMPLATE utilizes a multi-value JSON object as its value, but with the following differences
  from a standard PagerDuty notification integration:

  - Within the `payload` key, the `summary` key is not used to specify `SNOWFLAKE_WEBHOOK_MESSAGE`.
  - Instead, an additional `custom_details` key is used to specify `SNOWFLAKE_WEBHOOK_MESSAGE`.

  For example:

  Copy code

  ```
  WEBHOOK_BODY_TEMPLATE='{
    "routing_key": "SNOWFLAKE_WEBHOOK_SECRET",
    "event_action": "trigger",
    "payload": {
   "summary": "Snowflake replication failure",
   "source": "Snowflake monitoring",
   "severity": "INFO",
   "custom_details": {
     "message": "SNOWFLAKE_WEBHOOK_MESSAGE"
   }
    }
  }'
  ```

## Add an error notification for a replication or failover group

To enable error notifications for an existing replication/failover group, use the [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group)
or [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) command to set the ERROR\_INTEGRATION parameter.

For example, add notification integration `my_notification_int` to failover group `my_fg`. The following statement must
be executed from the source account:

Copy code

```
ALTER FAILOVER GROUP my_fg SET
  ERROR_INTEGRATION = my_notification_int;
```

To create a replication/failover group and enable error notifications, use the [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group)
or [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) command and set the ERROR\_INTEGRATION parameter.

For example, to create failover group `my_fg` to enable replication and failover of databases `db1`, `db2` to accounts
`myaccount2` and `myaccount3` in organization `myorg`, execute the following statement in the source account to
create a primary failover group:

Copy code

```
CREATE FAILOVER GROUP my_fg
  OBJECT_TYPES = DATABASES
  ALLOWED_DATABASES = db1, db2
  ALLOWED_ACCOUNTS = myorg.myaccount2, myorg.myaccount3
  REPLICATION_SCHEDULE = '10 MINUTE'
  ERROR_INTEGRATION = my_notification_int;
```

Note

If the replication schedule for a replication or failover group is set to a high frequency, for example one minute,
error notifications for the same issue are sent for every scheduled refresh operation.
