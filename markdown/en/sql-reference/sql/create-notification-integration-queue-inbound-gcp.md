# CREATE NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)

Creates a new notification integration in the account or replaces an existing integration for receiving messages from a Google
Pub/Sub topic.

See also:
:   [ALTER NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)](/sql-reference/sql/alter-notification-integration-queue-inbound-gcp) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  GCP_PUBSUB_SUBSCRIPTION_NAME = '<subscription_id>'
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

`NOTIFICATION_PROVIDER = GCP_PUBSUB`
:   Specifies Google Cloud Pub/Sub as the third-party cloud message queuing service.

`GCP_PUBSUB_SUBSCRIPTION_NAME = 'subscription_id'`
:   Pub/Sub topic subscription ID used to allow Snowflake access to event messages.

    Note

    A single notification integration supports a single Google Cloud Pub/Sub subscription. Referencing the same Pub/Sub
    subscription in multiple notification integrations can result in missing data in target tables because event notifications
    are split between notification integrations.

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

- Creating a single notification integration for multiple Google Cloud Pub/Sub subscriptions is not supported.

  When you create a new pipe using a notification integration with the same queue URL as another notification integration, the
  pipe creation fails with an error:

  ```
  Notification queue already in use with another integration.
  ```
- Using the same Google Cloud Pub/Sub subscription for multiple inbound notification integrations is not supported for automated
  data loads or metadata refreshes.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- The government regions of the cloud providers do not allow event notifications to be sent to or from other commercial regions.

## Examples

See the following topics:

- [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs)
- [Refresh directory tables automatically for Google Cloud Storage](/user-guide/data-load-dirtables-auto-gcs)
- [Refresh external tables automatically for Google Cloud Storage](/user-guide/tables-external-gcs)
