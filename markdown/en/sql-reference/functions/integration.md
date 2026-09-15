Categories:
:   [Notification functions](/sql-reference/functions-notification) (Integration Configuration)

# INTEGRATION

Returns a JSON object that specifies the notification integration to use to send a message. This is a helper function that you
use to construct an integration configuration object for the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

See also:
:   [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications) ,
    [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) ,
    [EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config)

## Syntax

Copy code

```
SNOWFLAKE.NOTIFICATION.INTEGRATION( '<integration_name>' )
```

## Arguments

`'integration_name'`
:   Name of the notification integration to use.

## Returns

A JSON-formatted string that specifies a notification integration for the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure to send.

For example, if you pass in the notification integration name `'my_queue_int'`, the function returns:

Copy code

```
'{"my_queue_int":{}}'
```

## Examples

See [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
