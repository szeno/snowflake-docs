# ALTER NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)

Modifies the properties for an existing notification integration for
[sending a message to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns).

See also:
:   [CREATE NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)](/sql-reference/sql/create-notification-integration-queue-outbound-aws) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
ALTER [ NOTIFICATION ] INTEGRATION [ IF EXISTS ] <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  AWS_SNS_TOPIC_ARN = '<topic_arn>'
  AWS_SNS_ROLE_ARN = '<iam_role_arn>'
  [ COMMENT = '<string_literal>' ]

ALTER [ NOTIFICATION ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ NOTIFICATION ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER [ NOTIFICATION ] INTEGRATION [ IF EXISTS ] <name> UNSET COMMENT
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

    `AWS_SNS_TOPIC_ARN = 'topic_arn'`
    :   Amazon Resource Name (ARN) of the Amazon SNS (SNS) topic to which notifications are pushed.

    `AWS_SNS_ROLE_ARN = 'iam_role_arn'`
    :   ARN of the IAM role that has permissions to publish messages to the SNS topic.

        Note

        The value of AWS\_SNS\_ROLE\_ARN is case-sensitive. Use the exact value that is specified in your AWS account.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   String (literal) that specifies a comment for the integration.

        Default: No value

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the integration, which resets them back to their defaults:

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- Disabling or dropping an integration might not take effect immediately because the integration might be cached. To expedite the
  removal process, remove the integration privilege from the cloud provider.
