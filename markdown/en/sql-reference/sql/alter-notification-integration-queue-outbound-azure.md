# ALTER NOTIFICATION INTEGRATION (outbound to an Azure Event Grid topic)

Modifies the properties for an existing notification integration for
[sending a message to an Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid).

See also:
:   [CREATE NOTIFICATION INTEGRATION (outbound to an Azure Event Grid topic)](/sql-reference/sql/create-notification-integration-queue-outbound-azure) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
ALTER [ NOTIFICATION ] INTEGRATION [ IF EXISTS ] <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  AZURE_STORAGE_QUEUE_PRIMARY_URI = '<queue_URL>'
  AZURE_TENANT_ID = '<directory_ID>';
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

    `AZURE_EVENT_GRID_TOPIC_ENDPOINT = 'event_grid_topic_endpoint'`
    :   Event Grid topic endpoint to which Snowflake pushes notifications.

    `AZURE_TENANT_ID = 'ad_directory_id'`
    :   ID of the Azure Active Directory tenant used for identity management. This ID is needed to generate the consent URL that grants
        Snowflake access to the Event Grid topic.

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
