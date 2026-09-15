# ANOMALY\_INSIGHTS!SET\_ACCOUNT\_NOTIFICATION\_EMAILS

Defines the list of email addresses that will receive a notification when there is an
[account-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level) in the current account.

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!SET_ACCOUNT_NOTIFICATION_EMAILS(
  '<email_address> [, <email_address> ... ]' )
```

## Arguments

`'email_address [, email_address ... ]'`
:   Comma-delimited list of email addresses that will receive a notification when there is an account-level cost anomaly.

    Each email address must have been [verified by the user](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address), otherwise it is ignored.

## Output

Returns a table with the following column:

| Column name | Data type | Description |
| --- | --- | --- |
| EMAIL\_LIST | VARCHAR | Comma-delimited list of email addresses where notifications are sent when there is an account-level cost anomaly in the current account. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

- This method sets the email notification list for the account in which it is called.
- Executing this method overwrites email addresses that were previously added to the notification list.
- Each email address must have been [verified by the user](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address).
- You can use a group email address, such as a distribution list, for notifications, but this email address must be verified. Before adding
  a group email address to the notification list, you might need to create a new Snowflake user with the group email address so you can
  verify it.

## Example

Set the email notification list so that users with email addresses `user1@example.com` and `user2@example.com` receive a notification
when there is a cost anomaly in the current account:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!SET_ACCOUNT_NOTIFICATION_EMAILS(
  'user1@example.com, user2@example.com');
```
