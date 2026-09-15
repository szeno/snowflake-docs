# Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

If you need to send notifications to an email address, webhook, or a queue provided by a cloud service (Amazon SNS, Google Cloud
PubSub, or Azure Event Grid), use the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

With a single call to this stored procedure, you can:

- Send a message to multiple types of destinations (email addresses, webhooks, and queues).
- Send a message to multiple email addresses, webhooks, and queues.
- Send a message in a specified format, according to the type of notification integration (plain text or HTML for email, JSON
  for queues).

For example, with a single call, you can send messages in plain text, HTML, and JSON formats to multiple email addresses and
multiple SNS, PubSub, and Event Grid topics.

You can use multiple notification integrations to send the notification to different queues. You can also create multiple email
notification integrations that have different sets of email addresses and subject lines, making it easier to configure email
messages for different recipients.

## Send a notification

Before you send a notification, you must have a notification integration that you will use to send the notification. If you are
sending an email notification, you must also validate the email addresses of the recipients. For details, see
[Notifications in Snowflake](/user-guide/notifications/about-notifications).

To send a notification to email addresses or queues, call the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure, specifying the messages and the
notification integrations to use.

The following is an example of a call to this stored procedure:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
   -- Message type and content.
  '{ "text/html": "<p>This is a message.</p>" }',
  -- Integration used to send the notification and values used for the subject and recipients.
  -- These values override the defaults specified in the integration.
  '{
    "my_email_int": {
      "subject": "Status update",
      "toAddress": ["person_a@example.com", "person_b@example.com"],
      "ccAddress": ["person_c@example.com"],
      "bccAddress": ["person_d@example.com"]
    }
  }'
);
```

As shown in the example above, you pass in JSON-formatted strings as arguments to specify the message to send and the
notification integration to use.

For the syntax for these strings, see [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification).

To construct these JSON-formatted strings, you can call helper functions like [TEXT\_HTML](/sql-reference/functions/text_html) to specify
the message and [EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config) to specify the notification integration, subject line,
and email addresses. For example:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_HTML('<p>a message</p>'),
  SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
    'my_email_int',
    'Status update',
    ARRAY_CONSTRUCT('person_a@example.com', 'person_b@example.com'),
    ARRAY_CONSTRUCT('person_c@example.com'),
    ARRAY_CONSTRUCT('person_d@example.com')
  )
);
```

For the list of helper functions that you can use, see [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification).

## Override the default values in the email notification integration

To use a different set of recipients or a different subject line from
[the default specified in the email notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration), set the
following properties of the integration configuration object that you pass to
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification):

- `subject` (this cannot exceed 256 characters in length)
- `toAddress`
- `ccAddress`
- `bccAddress`

For example, to use the email notification integration `my_email_int` and override the subject line, “To:” line, “Cc:” line,
and “Bcc:” line:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  '{ "text/html": "<p>This is a message.</p>" }',
  '{
    "my_email_int": {
      "subject": "Status update",
      "toAddress": ["person_a@example.com", "person_b@example.com"],
      "ccAddress": ["person_c@example.com"],
      "bccAddress": ["person_d@example.com"]
    }
  }'
);
```

To construct the JSON-formatted string for the integration configuration, you can call the
[EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config) helper function.

For example, to send the email message to [oncall-a@snowflake.com](mailto:oncall-a@snowflake.com) and [oncall-b@snowflake.com](mailto:oncall-b@snowflake.com) with the subject line “Service down”, execute the following statement:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('Your message'),
  SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
    'my_email_int,
    'Service down',
    ARRAY_CONSTRUCT('oncall-a@example.com', 'oncall-b@example.com')
  )
);
```

To include the “Cc:” and “Bcc:” lines in the email message, pass in additional arguments with arrays of email addresses for those
lines:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('Your message'),
  SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
    'my_email_int,
    'Service down',
    ARRAY_CONSTRUCT('oncall-a@example.com', 'oncall-b@example.com'),
    ARRAY_CONSTRUCT('cc-a@example.com', 'cc-b@example.com'),
    ARRAY_CONSTRUCT('bcc-a@example.com', 'bcc-b@example.com')
  )
);
```

If you only want to set the “Cc:” or “Bcc:” line (not both), pass in an empty array or NULL for the corresponding arguments.
If you are constructing the JSON object without using the helper function, omit the `ccAddress` or `bccAddress`
property from the JSON object.

## Send HTML, plain text, and JSON messages

To send a message in HTML, plain text, or JSON, pass in a JSON object that contains the message type as the name of the property
and the message as the value of the property:

Copy code

```
'{ "<message_type>": "<message>" }'
```

`"message_type"` can be one of the following values:

- `"text/html"`
- `"text/plain"`
- `"application/json"`

For example:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  '{ "text/html": "<p>This is a message.</p>" }',
  '{ "my_email_int": {} }'
);
```

To construct the JSON object for the message, you can use the following helper functions:

- For an HTML message, call [TEXT\_HTML](/sql-reference/functions/text_html).
- For a plain text message, call [TEXT\_HTML](/sql-reference/functions/text_html).
- For a JSON message, call [APPLICATION\_JSON](/sql-reference/functions/application_json).

The following example sends an HTML message, using the `my_email_int` email notification integration:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_HTML('<p>a message</p>'),
  SNOWFLAKE.NOTIFICATION.INTEGRATION('my_email_int')
);
```

The following example sends a plain text message, using the same integration:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('A message'),
  SNOWFLAKE.NOTIFICATION.INTEGRATION('my_email_int')
);
```

The following example sends a JSON message to the queue specified by the `my_queue_int` notification integration. For
instructions on creating a notification integration for a queue, see the following topics:

- [Creating a notification integration to send notifications to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns)
- [Creating a notification integration to send notifications to a Microsoft Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid)
- [Creating a notification integration to send notifications to a Google Cloud Pub/Sub topic](/user-guide/notifications/creating-notification-integration-google-pubsub)

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.APPLICATION_JSON('{ "name": "value" }'),
  SNOWFLAKE.NOTIFICATION.INTEGRATION('my_sns_int')
);
```

## Send a notification using multiple integrations

You can use multiple integrations to send messages when:

- You want to send a message in email and to a topic in the same function call.
- You want to send a message to different email addresses specified by different email notification integrations.

To use multiple integrations, call the [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) function to construct an array of
integration configurations, and pass the array as the second argument of the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

For example, to send a plain text message to a queue and email addresses configured in different notification integrations:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  '{"text/plain":"A message"}',
  ARRAY_CONSTRUCT(
    '{"my_sns_int":{}}',
    '{"my_email_int":{}}',
 )
);
```

Note

The array cannot contain more than one object for the same notification integration.

If you prefer to use the helper functions to construct the integration configurations, you can pass the values returned by the
helper functions to the ARRAY\_CONSTRUCT function. For example:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('A message'),
  ARRAY_CONSTRUCT(
    SNOWFLAKE.NOTIFICATION.INTEGRATION('my_sns_int'),
    SNOWFLAKE.NOTIFICATION.INTEGRATION('my_email_int')
  )
);
```

The following example sends messages in different formats to a queue and email addresses:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  ARRAY_CONSTRUCT(
    SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('A message'),
    SNOWFLAKE.NOTIFICATION.TEXT_HTML('<p>A message</p>'),
    SNOWFLAKE.NOTIFICATION.APPLICATION_JSON('{ "name": "value" }')
  ),
  ARRAY_CONSTRUCT(
    SNOWFLAKE.NOTIFICATION.INTEGRATION('my_sns_int'),
    SNOWFLAKE.NOTIFICATION.INTEGRATION('my_email_int')
  )
);
```
