# Notification functions

Notification functions are helper functions that you can call when using the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure to
[send a notification](/user-guide/notifications/snowflake-notifications).

The integration configuration and message construction functions return JSON-formatted strings that you pass to the
SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION stored procedure.

| Sub-category | Function | Notes |
| --- | --- | --- |
| Integration Configuration | [EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config) |  |
|  | [INTEGRATION](/sql-reference/functions/integration) |  |
| Message Construction | [APPLICATION\_JSON](/sql-reference/functions/application_json) |  |
|  | [TEXT\_HTML](/sql-reference/functions/text_html) |  |
|  | [TEXT\_PLAIN](/sql-reference/functions/text_plain) |  |
| Message Sanitization | [SANITIZE\_WEBHOOK\_CONTENT](/sql-reference/functions/sanitize_webhook_content) |  |

Expand

Show lessSee more
