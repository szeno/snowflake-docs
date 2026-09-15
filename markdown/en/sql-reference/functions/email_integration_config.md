Categories:
:   [Notification functions](/sql-reference/functions-notification) (Integration Configuration)

# EMAIL\_INTEGRATION\_CONFIG

Returns a JSON object that specifies the email notification integration, recipients, and subject line to use for an email
notification. This is a helper function that you use to construct an integration configuration object for the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

See also:
:   [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications) ,
    [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) ,
    [INTEGRATION](/sql-reference/functions/integration)

## Syntax

Copy code

```
SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
  '<email_integration_name>',
  '<subject>',
  <array_of_email_addresses_for_to_line> )
```

Copy code

```
SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
  '<email_integration_name>',
  '<subject>',
  <array_of_email_addresses_for_to_line>,
  <array_of_email_addresses_for_cc_line>,
  <array_of_email_addresses_for_bcc_line> )
```

## Arguments

`'email_integration_name'`
:   Name of the email notification integration to use.

`'subject'`
:   Subject of the email message.

    The subject cannot exceed 256 characters in length.

`array_of_email_addresses_for_to_line` `array_of_email_addresses_for_cc_line` `array_of_email_addresses_for_bcc_line`
:   ARRAYs of the email addresses to include in the “To:”, “Cc:”, and “Bcc:” lines of the message.

    You must specify email addresses of users in the current account. These users must
    [verify their email addresses](/user-guide/notifications/email-notifications#label-email-notification-verify-address).

    If the ALLOWED\_RECIPIENTS property is set to a list of email addresses in the
    [email notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration), the email addresses must be in that list.

    Call the [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) function to construct each ARRAY.

    Note

    You cannot send an email notification if you only specify the “Bcc:” line.

## Returns

A JSON-formatted string that specifies a notification integration for the
[SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure to send.

For example, suppose that you pass in the notification integration name `'my_email_int'` with the following subject line and
list of email addresses for the “To:” line:

Copy code

```
SELECT SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
  'my_email_int',
  'Updates',
   ARRAY_CONSTRUCT('person_a@example.com', 'person_b@example.com')
)
```

The function returns the following JSON-formatted string:

Copy code

```
'{"my_email_int":{"subject":"Updates","toAddress":["person_a@example.com","person_b@example.com"]}}'
```

The following example sends the same notification with an additional list of email addresses for the “Cc:” line. Note that this
example passes NULL for the “Bcc:” addresses to exclude the `bccAddress` property from the returned object.

Copy code

```
SELECT SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
  'my_email_int',
  'Updates',
   ARRAY_CONSTRUCT('person_a@example.com', 'person_b@example.com'),
   ARRAY_CONSTRUCT('cc_person_a@example.com'),
   NULL
)
```

The function returns the following JSON-formatted string:

Copy code

```
'{"my_email_int":{"subject":"Updates","toAddress":["person_a@example.com","person_b@example.com"],"ccAddress":["cc_person_a@snowflake.com"]}}'
```

The following example sends the same notification with an additional list of email addresses for the “Bcc:” line:

Copy code

```
SELECT SNOWFLAKE.NOTIFICATION.EMAIL_INTEGRATION_CONFIG(
  'my_email_int',
  'Updates',
   ARRAY_CONSTRUCT('person_a@example.com', 'person_b@example.com'),
   ARRAY_CONSTRUCT('cc_person_a@example.com'),
   ARRAY_CONSTRUCT('bcc_person_b@example.com')
)
```

The function returns the following JSON-formatted string:

Copy code

```
'{"my_email_int":{"subject":"Updates","toAddress":["person_a@example.com","person_b@example.com"],"ccAddress":["cc_person_a@example.com"],"bccAddress":["bcc_person_b@example.com"]}}'
```

## Examples

See [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
