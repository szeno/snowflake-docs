# CREATE NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)

Creates a new notification integration in the account or replaces an existing integration for
[sending a message to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns).

Note

Currently, this feature is limited to Snowflake accounts hosted on AWS.

See also:
:   [ALTER NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)](/sql-reference/sql/alter-notification-integration-queue-outbound-aws) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = QUEUE
  DIRECTION = OUTBOUND
  NOTIFICATION_PROVIDER = AWS_SNS
  AWS_SNS_TOPIC_ARN = '<topic_arn>'
  AWS_SNS_ROLE_ARN = '<iam_role_arn>'
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ENABLED = { TRUE | FALSE }`
:   Specifies whether to initiate operation of the integration or suspend it.

    - `TRUE` enables the integration.
    - `FALSE` disables the integration for maintenance. Any integration between Snowflake and a third-party service fails to
      work.

    The value is case-insensitive.

    The default is `TRUE`.

`TYPE = QUEUE`
:   Specifies that this is an integration between Snowflake and a third-party cloud message-queuing service.

`DIRECTION = OUTBOUND`
:   Specifies that Snowflake produces the notification sent to the cloud messaging service.

`NOTIFICATION_PROVIDER = AWS_SNS`
:   Specifies Amazon Simple Notification Service (SNS) as the third-party cloud message queuing service.

`AWS_SNS_TOPIC_ARN = 'topic_arn'`
:   Amazon Resource Name (ARN) of the Amazon SNS (SNS) topic to which notifications are pushed.

`AWS_SNS_ROLE_ARN = 'iam_role_arn'`
:   ARN of the IAM role that has permissions to publish messages to the SNS topic.

    Note

    The value of AWS\_SNS\_ROLE\_ARN is case-sensitive. Use the exact value that is specified in your AWS account.

## Optional parameters

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| CREATE NOTIFICATION INTEGRATION | Account | Grants the ability to create notification integrations. This privilege does not grant the ability to create other types of integrations. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Using the same outbound notification integration for multiple pipes is supported for push notifications.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- The government regions of the cloud providers do not allow event notifications to be sent to or from other commercial regions.
  For more information, see [AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-s3.html).

## Examples

See the following topics:

- [Enabling Snowpipe error notifications for Amazon SNS](/user-guide/data-load-snowpipe-errors-sns)
- [Creating a notification integration to send notifications to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns)
