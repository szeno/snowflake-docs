# ANOMALY\_INSIGHTS!SET\_MONITOR\_NOTIFICATION\_EMAILS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Defines the list of email addresses that receive a notification when an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) detects a
cost anomaly.

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!SET_MONITOR_NOTIFICATION_EMAILS(
  '<alias>',
  '<email_address> [, <email_address> ... ]' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

`'email_address [, email_address ... ]'`
:   Comma-delimited list of email addresses that receive a notification when the monitor detects a cost anomaly.

    Each email address must have been [verified by the user](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address). Addresses that aren’t verified are ignored.

    Data type: VARCHAR

## Output

Returns a VARCHAR status message that confirms the operation and lists the email addresses that were saved.

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

- Each monitor has its own notification list, separate from the account-level and organization-level lists.
- Running this method overwrites email addresses that were previously added to the monitor’s notification list.
- Each email address must have been [verified by the user](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address). Addresses that aren’t verified aren’t
  saved, but the verified addresses in the same call are.
- You can use a group email address, such as a distribution list, for notifications, but this email address must be verified. Before adding
  a group email address to the notification list, you might need to create a new Snowflake user with the group email address so you can
  verify it.

## Example

Set the notification list for the monitor `Eng-Platform` so that users with email addresses `user1@example.com` and `user2@example.com`
receive a notification when the monitor detects a cost anomaly:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!SET_MONITOR_NOTIFICATION_EMAILS(
  'Eng-Platform', 'user1@example.com,user2@example.com');
```
