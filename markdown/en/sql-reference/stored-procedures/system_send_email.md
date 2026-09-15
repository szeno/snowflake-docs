# SYSTEM$SEND\_EMAIL

Sends an [email notification](/user-guide/notifications/email-stored-procedures) to the specified recipients from
`no-reply@snowflake.net`.

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

## Syntax

Copy code

```
SYSTEM$SEND_EMAIL(
  '<integration_name>',
  '<email_address_1> [ , ... <email_address_N> ]',
  '<email_subject>',
  '<email_content>',
  [ '<mime_type>' ] )
```

## Arguments

### Required

`integration_name`
:   Name of the [notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration) that you want to use to send the
    email message.

`email_address_1 [ , ... email_address_N ]`
:   List of email addresses that should receive the email notification.

    Specify one or more unquoted email addresses in a comma-separated string.

    If the `ALLOWED_RECIPIENTS` property of the
    [notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration) is set and any of the email addresses is
    not in that list, no email notifications are sent.

`email_subject`
:   Subject line of the email notification. You cannot specify an empty string.

`email_content`
:   Body of the email. You cannot specify an empty string.

### Optional

`mime_type`
:   The MIME type of the `email_content` value, the email’s content. Default is `text/plain`.

    The following types are supported:

    - `text/plain` – Specify this when `email_content` is plain text. This is the default value.
    - `text/html` – Specify this when `email_content` is HTML.

      Note that the content of a message of the `text/html` type is not validated as well-formed HTML.

## Returns

Returns TRUE if the stored procedure executes successfully.

## Examples

See [Using SYSTEM$SEND\_EMAIL to send email notifications](/user-guide/notifications/email-stored-procedures).
