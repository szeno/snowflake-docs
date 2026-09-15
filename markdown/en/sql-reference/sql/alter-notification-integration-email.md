# ALTER NOTIFICATION INTEGRATION (email)

Modifies the properties for an existing notification integration for
[sending email messages](/user-guide/notifications/email-notifications).

See also:
:   [CREATE NOTIFICATION INTEGRATION (email)](/sql-reference/sql/create-notification-integration-email) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
ALTER [ NOTIFICATION ] INTEGRATION [ IF EXISTS ] <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ ALLOWED_RECIPIENTS = ( '<email_address>' [ , ... '<email_address>' ] ) ]
  [ DEFAULT_RECIPIENTS = ( '<email_address>' [ , ... '<email_address>' ] ) ]
  [ DEFAULT_SUBJECT = '<subject_line>' ]
  [ COMMENT = '<string_literal>' ]

ALTER [ NOTIFICATION ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ NOTIFICATION ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER [ NOTIFICATION ] INTEGRATION [ IF EXISTS ] <name> UNSET
  ENABLED            |
  ALLOWED_RECIPIENTS |
  DEFAULT_RECIPIENTS |
  DEFAULT_SUBJECT    |
  COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the integration to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether to initiate operation of the integration or suspend it.

        - `TRUE` enables the integration.
        - `FALSE` disables the integration for maintenance. Any integration between Snowflake and a third-party service fails to
          work.

        The value is case-insensitive.

        The default is `TRUE`.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `ALLOWED_RECIPIENTS = ( 'email_address' [ , ... 'email_address' ] )`
    :   (For `TYPE = EMAIL`) A comma-separated list of quoted email addresses that can receive notification emails from this
        integration.

        You must specify email addresses of users in the current account. These users must
        [verify their email addresses](/user-guide/notifications/email-notifications#label-email-notification-verify-address).

        The maximum number of email addresses that you can specify is 50.

        If you omit this parameter, you can send email notifications to any verified email address in the current account.

    `DEFAULT_RECIPIENTS = ( 'email_address' [ , ... 'email_address' ] )`
    :   Specifies the list of default recipients for messages sent with this integration. Use a comma-separated list of quoted email
        addresses to specify the default recipients.

        You must specify email addresses of users in the current account. These users must verify their email addresses.

        To override the default recipients for a given message, use the [EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config) helper
        function when calling the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

    `DEFAULT_SUBJECT = 'subject_line'`
    :   Specifies the default subject line for messages sent with this integration.

        The subject cannot exceed 256 characters in length.

        Default: ‘Snowflake Email Notification’

        To override the default subject line for a given message, use the [EMAIL\_INTEGRATION\_CONFIG](/sql-reference/functions/email_integration_config)
        helper function when calling the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure.

    `COMMENT = 'string_literal'`
    :   String (literal) that specifies a comment for the integration.

        Default: No value

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the integration, which resets them back to their defaults:

    - `ENABLED`
    - `ALLOWED_RECIPIENTS`
    - `DEFAULT_RECIPIENTS`
    - `DEFAULT_SUBJECT`
    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
