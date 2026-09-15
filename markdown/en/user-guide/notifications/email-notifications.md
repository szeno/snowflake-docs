# Sending email notifications

To send an email notification:

1. Make sure that the intended recipients [verify their email addresses](#label-email-notification-verify-address).
2. [Create a notification integration](#label-create-email-notification-integration).
3. [Call a stored procedure](#label-notification-stored-procedures-email) to send the notification.

## Verify the email addresses of the email notification recipients

You can send email notifications only to Snowflake users within the same account.

Users can verify their own email addresses through [Snowsight (the Snowflake web interface)](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address).

Administrators can verify the email address of other users by calling the [SYSTEM$START\_USER\_EMAIL\_VERIFICATION](/sql-reference/functions/system_start_user_email_verification) function.

## Create an email notification integration

To send email notifications, use an email notification integration that you create with the
[CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-email) command.

Note

You must use a role that has the global CREATE INTEGRATION or CREATE NOTIFICATION INTEGRATION privilege to run this command.

For example, to create an email notification integration named `my_email_int`, execute the following statement:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_email_int
  TYPE=EMAIL
  ENABLED=TRUE;
```

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

### Restrict the list of email addresses that can receive notifications

If you want to restrict the list of email addresses that can receive notifications through this integration, set
ALLOWED\_RECIPIENTS to the list of those email addresses. If you do not set ALLOWED\_RECIPIENTS, the integration can be used to
send notifications to any user in the account, provided that the
[email address has been verified](#label-email-notification-verify-address).

Note

For each email address in ALLOWED\_RECIPIENTS, make sure that the email address has been verified. If you specify an email
address that hasn’t been verified, the CREATE NOTIFICATION INTEGRATION command fails with an error.

For example, to restrict the notification integration so that email messages can be sent only to `first.last@example.com` and
`first2.last2@example.com`, set ALLOWED\_RECIPIENTS to the list of those addresses:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_email_int
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=('first.last@example.com','first2.last2@example.com');
```

For details about the syntax of this command, see [CREATE NOTIFICATION INTEGRATION (email)](/sql-reference/sql/create-notification-integration-email).

### Specify a default list of recipients and a default subject line

If you are using the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/user-guide/notifications/snowflake-notifications) stored
procedure to send email notifications, you can configure the notification integration with a default list of email addresses
and a default subject line to use. You can override the default list and subject line when you call the stored procedure.

- To specify a default list of email addresses, set the DEFAULT\_RECIPIENTS property of the notification integration.
- To specify a default subject line, set the DEFAULT\_SUBJECT property of the notification integration.

For example, suppose that you want to set up an email notification integration for the following purpose:

- You want to send most email notifications to `person_a@example.com` and `person_b@example.com`, but you also want the
  ability to send the notifications to the validated email addresses of any users in your account.
- You want most messages to use the subject line “Service status”, but you want to be able to use a different subject line for
  specific messages.

To create an email notification for this purpose, execute the following command:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_email_int
  TYPE=EMAIL
  ENABLED=TRUE
  DEFAULT_RECIPIENTS = ('person_a@example.com','person_b@example.com')
  DEFAULT_SUBJECT = 'Service status';
```

When sending the notification, you can override the list of default recipients and the default subject line. See
[Override the default values in the email notification integration](/user-guide/notifications/snowflake-notifications#label-notification-sending-email-override).

## Send the email notification

You can call one of the following stored procedures to send an email notification:

- [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification)

  For details, see [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
- [SYSTEM$SEND\_EMAIL](/sql-reference/stored-procedures/system_send_email)

  For details, see [Using SYSTEM$SEND\_EMAIL to send email notifications](/user-guide/notifications/email-stored-procedures).
