Categories:
:   [Notification functions](/sql-reference/functions-notification) (Message Construction)

# APPLICATION\_JSON

Returns a JSON object that specifies the JSON message to use for a notification. This is a helper function that you use to
construct a message object for the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

See also:
:   [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications) ,
    [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) ,
    [TEXT\_HTML](/sql-reference/functions/text_html) ,
    [TEXT\_PLAIN](/sql-reference/functions/text_plain)

## Syntax

Copy code

```
SNOWFLAKE.NOTIFICATION.APPLICATION_JSON( '<message>' )
```

## Arguments

`'message'`
:   Content of the message to send.

    You do not need to escape the double quotes around strings within the message (for example, double quotes around the keys
    and values). The function escapes these double quotes for you.

## Returns

A JSON-formatted string that specifies a message for the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure to send.

For example, suppose that you call the function and pass in a JSON message:

Copy code

```
SELECT SNOWFLAKE.NOTIFICATION.APPLICATION_JSON('{"data": "hello world"}');
```

The function returns the following JSON-formatted string:

Copy code

```
'{"application/json":"{\"data\": \"hello world\"}"}'
```

Note how the function escapes the double quotes around the keys and values in your message.

## Examples

See [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
