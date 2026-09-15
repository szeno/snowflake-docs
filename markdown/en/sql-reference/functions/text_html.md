Categories:
:   [Notification functions](/sql-reference/functions-notification) (Message Construction)

# TEXT\_HTML

Returns a JSON object that specifies the HTML message to use for a notification. This is a helper function that you use to
construct a message object for the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

See also:
:   [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications) ,
    [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) ,
    [TEXT\_PLAIN](/sql-reference/functions/text_plain) ,
    [APPLICATION\_JSON](/sql-reference/functions/application_json)

## Syntax

Copy code

```
SNOWFLAKE.NOTIFICATION.TEXT_HTML( '<message>' )
```

## Arguments

`'message'`
:   Content of the message to send.

## Returns

A JSON-formatted string that specifies a message for the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure to send.

For example:

Copy code

```
'{"text/html":"<p>A message</p>"}'
```

## Examples

See [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
