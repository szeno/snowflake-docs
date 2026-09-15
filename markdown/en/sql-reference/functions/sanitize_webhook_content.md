Categories:
:   [Notification functions](/sql-reference/functions-notification) (Message Sanitization)

# SANITIZE\_WEBHOOK\_CONTENT

Removes placeholders (for example, the SNOWFLAKE\_WEBHOOK\_SECRET placeholder, which specifies a secret) from the body of a
notification message to be sent.

Placeholders like SNOWFLAKE\_WEBHOOK\_SECRET are used in notification integrations. When you
[create a notification integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-integration), you can use placeholders to indicate where
you want the content inserted into the request. For example, you can use the SNOWFLAKE\_WEBHOOK\_SECRET placeholder to insert the
secret into the HTTP headers or body of the request.

The [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure replaces these placeholders in
the integration parameters with actual values. The stored procedure also replaces the placeholders if specified directly in the
message string passed to the function. If the placeholder is for a secret, this might unintentionally make the secret available
to others. For example, if this message is sent to a Slack webhook, the message containing the secret might be posted to a Slack
channel.

To avoid this situation, pass the message to SANITIZE\_WEBHOOK\_CONTENT to remove any placeholders from the message before passing
the message to SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION.

See also:
:   [Sending webhook notifications](/user-guide/notifications/webhook-notifications)

## Syntax

Copy code

```
SNOWFLAKE.NOTIFICATION.SANITIZE_WEBHOOK_CONTENT( <message> )
```

## Arguments

`message`
:   A VARCHAR value containing the message to sanitize.

## Returns

Returns a VARCHAR value with placeholders replaced with the string `REDACTED`.

## Examples

See [Sending a notification to a webhook](/user-guide/notifications/webhook-notifications#label-notifications-webhook-send).
