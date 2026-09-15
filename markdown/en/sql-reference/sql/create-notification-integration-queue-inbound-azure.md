# CREATE NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)

Creates a new notification integration in the account or replaces an existing integration for receiving messages from an Azure
Event Grid topic.

See also:
:   [ALTER NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)](/sql-reference/sql/alter-notification-integration-queue-inbound-azure) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = '<queue_url>'
  AZURE_TENANT_ID = '<ad_directory_id>';
  [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
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

`NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE`
:   Specifies Microsoft Azure Event Grid as the third-party cloud message queuing service.

`AZURE_STORAGE_QUEUE_PRIMARY_URI = 'queue_url`
> Specifies the queue URL for the Azure Queue Storage queue created for Event Grid notifications. Use a URL in the following
> format:
>
> `https://storage_queue_account.queue.core.windows.net/storage_queue_name`
>
> Note
>
> A single notification integration supports a single Azure Storage queue. Referencing the same storage queue in multiple
> notification integrations can result in missing data in target tables because event notifications are split between
> notification integrations.

`AZURE_TENANT_ID = 'ad_directory_id'`
:   Specifies the ID of the Azure Active Directory tenant used for identity management. This ID is needed to generate the consent URL
    that grants Snowflake access to the Event Grid notification subscription.

## Optional parameters

`USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
:   Specifies whether to use private connectivity. For information about using this parameter, see [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private).

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

- Creating a single notification integration for multiple Microsoft Azure Storage queues is not supported.

  When you create a new pipe using a notification integration with the same queue URL as another notification integration, the
  pipe creation fails with an error:

  ```
  Notification queue already in use with another integration.
  ```
- Using the same Microsoft Azure Storage queue for multiple inbound notification integrations is not supported for automated
  data loads or metadata refreshes.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- The government regions of the cloud providers do not allow event notifications to be sent to or from other commercial regions.
  For more information, see [Azure Government](https://learn.microsoft.com/en-us/azure/azure-government/).

## Examples

See the following topics:

- [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure)
- [Refresh directory tables automatically for Azure Blob Storage](/user-guide/data-load-dirtables-auto-azure)
- [Refresh external tables automatically for Azure Blob Storage](/user-guide/tables-external-azure)
