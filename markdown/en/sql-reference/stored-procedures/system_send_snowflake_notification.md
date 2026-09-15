# SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION

Sends a notification message to an email address, webhook, or queue provided by a Cloud service (Amazon SNS, Google Cloud PubSub,
or Azure Event Grid).

See also:
:   [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications)

## Syntax

Copy code

```
SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  <message>,
  <integration_configuration> )

SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  ( <message>, [ <message>, ... ] ),
  <integration_configuration> )

SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  <message>,
  ( <integration_configuration> [ , <integration_configuration> , ... ] ) )

SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  ( <message> [ , <message> , ... ] ),
  ( <integration_configuration> [ , <integration_configuration> , ... ] ) )
```

## Arguments

`message`
:   JSON-formatted string that specifies the type and content of the message. The string must be in the following format:

    Copy code

    ```
    { "<content_type>": "<message_contents>" }
    ```

    Where:

    - `"content_type"` is one of the following:

      - `"text/plain"` for plain text messages.
      - `"text/html"` for HTML messages.
      - `"application/json"` for JSON messages.
    - `"<message_contents>"` is the content of the message.

    For example:

    Copy code

    ```
    { "text/html": "<p>A message</p>" }
    ```

    To construct this string, you can call one of the following functions:

    - To send an HTML email message, call the [TEXT\_HTML](/sql-reference/functions/text_html) function.
    - To send a plain text email message, call the [TEXT\_PLAIN](/sql-reference/functions/text_plain) function.
    - To send a JSON message to a queue, call the [APPLICATION\_JSON](/sql-reference/functions/application_json) function.

`integration_configuration`
:   JSON-formatted string that specifies the notification integration or the email configuration to use to send the notification.
    The string must be one of the following formats:

    Copy code

    ```
    { "<integration_name>": {} }
    ```

    Copy code

    ```
    { "<integration_name>": { <options> } }
    ```

    Where:

    - `"integration_name"` is the name of the notification integration.
    - `options` is a comma-delimited list of properties (in JSON format) that specify values that override the defaults
      in the integration. You can specify the following properties:

      | Property Name | Description |
      | --- | --- |
      | `subject` | Subject line of the email notification. For example:  Copy code  ``` { "subject" : "Service status update" } ```  The subject cannot exceed 256 characters in length.  If you do not set this property, the default subject line from the integration is used.  If the integration does not specify a default subject line, `"Snowflake Email Notification"` is used. |
      | `toAddress` | List of email addresses of the recipients to include in the “To:” line of the email notification.  Format this list as a JSON array. For example:  Copy code  ``` { "toAddress" : ["person_1@example.com", "person_2@example.com"] } ```  If you do not set this property, the stored procedure uses the list of email addresses from the DEFAULT\_RECIPIENTS property of the [email notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration). |
      | `ccAddress` | List of email addresses of the recipients to include in the “Cc:” line of the email notification.  Format this list as a JSON array. For example:  Copy code  ``` { "ccAddress" : ["person_to_cc1@example.com", "person_to_cc2@example.com"] } ``` |
      | `bccAddress` | List of email addresses of the recipients to include in the “Bcc:” line of the email notification.  Format this list as a JSON array. For example:  Copy code  ``` { "bccAddress" : ["person_to_bcc1@example.com", "person_to_bcc2@example.com"] } ``` |

      Expand

      Show lessSee more

      For example:

      Copy code

      ```
      { "my_queue_int": {} }
      ```

      Copy code

      ```
      { "my_email_int": { "subject" : "Different subject" } }
      ```

      Copy code

      ```
      { "my_email_int": { "subject" : "Different subject" }, { "toAddress": ["person_a@example.com"] }
      ```

    To construct the JSON-formatted strings for the integration configuration, call one of the following functions:

    - If you are sending the notification to a queue, or if you are sending an email notification and want to use the default values
      specified in the email notification integration, call the [INTEGRATION](/sql-reference/functions/integration) function.
    - if you are sending an email notification and want to override the default values specified in the email notification
      integration, call the [EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config) function.

`( message [ , message , ... ] )`
:   ARRAY of JSON-formatted strings, each of which specify a message type and content. Specify this argument if you want to send a
    message in multiple formats.

    Each message should use [the format described above](/sql-reference/stored-procedures/system_send_snowflake_notification#label-notification-message-json-format).

    To construct the ARRAY, call the [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) function.

    Note

    The ARRAY cannot contain more than one object for the same message content type.

`( integration_configuration [ , integration_configuration , ... ] )`
:   ARRAY of JSON-formatted strings, each of which specifies a notification integration and configuration to use. Specify this
    argument if you want to use multiple notification integrations or email configurations to send a message.

    Each integration configuration should use
    [the format described above](/sql-reference/stored-procedures/system_send_snowflake_notification#label-notification-integration-json-format).

    To construct the ARRAY, call the [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) function.

    Note

    The ARRAY cannot contain more than one object for the same notification integration.

## Returns

If the stored procedure executes successfully, it returns the string “Enqueued notifications”.

## Usage notes

- For email notifications, if the DEFAULT\_RECIPIENTS property is not set in the notification integration and you do not set the
  `toAddress:` property in the SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION call, the call fails.
- For webhook notifications, call [SANITIZE\_WEBHOOK\_CONTENT](/sql-reference/functions/sanitize_webhook_content) to sanitize the message before passing
  the message to SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION.

## Examples

See [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
