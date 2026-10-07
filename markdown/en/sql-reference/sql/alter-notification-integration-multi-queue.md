# ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)

Modifies the properties for an existing Multi-Queue Notification Integration (MQNI). An MQNI (`TYPE = MULTI_QUEUE`) lists one
queue for each of your cloud storage locations, and its active queue determines which queue the auto-ingest pipes that use it
receive notifications from in the current account.

See also:
:   [CREATE NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/create-notification-integration-multi-queue) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
ALTER [ NOTIFICATION ] INTEGRATION [ IF EXISTS ] <name> SET
  ACTIVE = '<queue_name>'
  [ ENABLED = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]

ALTER [ NOTIFICATION ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ NOTIFICATION ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the integration to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `ACTIVE = 'queue_name'`
    :   Specifies the queue to set as the active queue for the integration in the current account. The value must match the `NAME` of a
        queue in the integration’s `QUEUES` list exactly, including case. To see the queue names, run
        [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration).

        Required in every `ALTER ... SET` statement that sets properties of an MQNI, even when you change only `ENABLED` or `COMMENT`. `SET TAG` doesn’t need it.

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

    `COMMENT = 'string_literal'`
    :   String (literal) that specifies a comment for the integration.

        Default: No value

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the integration, which resets them back to their defaults:

    - `TAG tag_name [ , tag_name ... ]`

## Usage notes

- You can’t change the `QUEUES` list or `DIRECTION` after you create the integration.
- Setting `ACTIVE` rebinds every auto-ingest pipe in the current account whose `INTEGRATION` value matches the integration’s name
  exactly, so that the pipe receives notifications from the active queue. The rebind uses the current storage location of each pipe’s
  stage, so if the stage uses a Multi-Location Storage Integration (MLSI), set the MLSI’s active location first. If you change the
  MLSI’s active location later, set `ACTIVE` again. Snowflake rebinds the pipes even if the active queue doesn’t change. If Snowflake can’t rebind a pipe, the statement fails, and some pipes might be left without a queue. For more
  information, see [Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).
- The active queue is a setting for each account. Replication doesn’t copy the active queue from the source account, and a refresh
  doesn’t change it in a target account. When Snowflake first replicates an MQNI to a target account, the replica has no active
  queue until you set one.
- A pipe that a refresh replicates to a target account doesn’t load there until you set `ACTIVE` in that account, even if the MQNI
  already has an active queue and the pipe’s status looks normal. Set `ACTIVE` again, with the name of the queue that’s already
  active, after each refresh that replicates new pipes that use the integration. For more information, see
  [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later).
- In a secondary account, such as the target account before a failover or the source account before a failback, the replicated MQNI is
  read-only, except that you can set its active queue. Omit the `NOTIFICATION` keyword
  and set only `ACTIVE`:

  Copy code

  ```
  ALTER INTEGRATION my_mqni SET ACTIVE = 'my-us-east-1';
  ```

  If you include the `NOTIFICATION` keyword, the statement fails with the following error:

  ```
  Cannot ALTER NOTIFICATION integration "<name>" because it is a read-only secondary.
  ```
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- Disabling or dropping an integration might not take effect immediately because the integration might be cached. To expedite the
  removal process, remove the integration privilege from the cloud provider.

## Examples

In your source account, set the active queue of the MQNI `my_mqni` to the queue named `my-us-west-1`:

Copy code

```
ALTER NOTIFICATION INTEGRATION my_mqni SET ACTIVE = 'my-us-west-1';
```

In your source account, disable the MQNI. The statement also includes `ACTIVE`, because every `SET` of MQNI properties requires it:

Copy code

```
ALTER NOTIFICATION INTEGRATION my_mqni SET ACTIVE = 'my-us-west-1' ENABLED = FALSE;
```

In a target account, set the active queue of the replicated MQNI to the queue named `my-us-east-1`:

Copy code

```
ALTER INTEGRATION my_mqni SET ACTIVE = 'my-us-east-1';
```
