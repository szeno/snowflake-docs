# CREATE NOTIFICATION INTEGRATION (inbound from multiple queues)

Creates a new Multi-Queue Notification Integration (MQNI) in the account or replaces an existing integration. An MQNI
(`TYPE = MULTI_QUEUE`) lists one queue for each of your cloud storage locations. Its active queue determines which queue the
auto-ingest pipes that use it receive notifications from in the current account. You use an MQNI with a Multi-Location Storage
Integration (MLSI) so that your pipes can keep loading data from your secondary storage location after a failover.

To create an MQNI from the queues of pipes that already exist, use `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` instead, as described in
[Scenario B: Create an MQNI from your existing pipes’ queues](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-b).

See also:
:   [ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) ,
    [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = MULTI_QUEUE
  DIRECTION = INBOUND
  QUEUES = ( <queue> [ , <queue> ] )
  ACTIVE = '<queue_name>'
  [ COMMENT = '<string_literal>' ]
```

Where `<queue>` has one of the following forms, depending on the cloud provider that hosts the storage location:

Copy code

```
-- Amazon S3
(
  NAME = '<queue_name>'
  NOTIFICATION_PROVIDER = AWS_SNS
  AWS_SNS_TOPIC_ARN = '<topic_arn>'
)

-- Google Cloud Storage
(
  NAME = '<queue_name>'
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  GCP_PUBSUB_SUBSCRIPTION_NAME = '<subscription_id>'
)

-- Microsoft Azure
(
  NAME = '<queue_name>'
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = '<queue_url>'
  AZURE_TENANT_ID = '<tenant_id>'
)
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

`TYPE = MULTI_QUEUE`
:   Specifies that this is a multi-queue integration between Snowflake and one or more third-party cloud message-queuing services.

`DIRECTION = INBOUND`
:   Specifies that Snowflake receives notifications sent by the cloud messaging services. `OUTBOUND` isn’t supported.

`QUEUES = ( queue [ , queue ] )`
:   Specifies the queues for the integration, typically one for each storage location of your MLSI. An MQNI can have at most two
    queues by default. The queues can use different cloud providers.

    Each queue requires `NAME`, `NOTIFICATION_PROVIDER`, and the parameters for its cloud provider, and accepts no other parameters:

    `NAME = 'queue_name'`
    :   Specifies the name of the queue. You use this name to set the active queue with `ACTIVE`.

    `NOTIFICATION_PROVIDER = { AWS_SNS | GCP_PUBSUB | AZURE_STORAGE_QUEUE }`
    :   Specifies the third-party cloud message-queuing service for the queue:

        - `AWS_SNS`: Amazon SNS. Also requires the following parameter:

          - `AWS_SNS_TOPIC_ARN = 'topic_arn'`: ARN of the Amazon SNS topic to which Amazon S3 sends
            event notifications for the storage location.
        - `GCP_PUBSUB`: Google Cloud Pub/Sub. Also requires the following parameter:

          - `GCP_PUBSUB_SUBSCRIPTION_NAME = 'subscription_id'`: ID of the Pub/Sub subscription. For more
            information, see [CREATE NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)](/sql-reference/sql/create-notification-integration-queue-inbound-gcp).
        - `AZURE_STORAGE_QUEUE`: Azure Queue Storage. Also requires the following parameters:

          - `AZURE_STORAGE_QUEUE_PRIMARY_URI = 'queue_url'`: URL of the storage queue.
          - `AZURE_TENANT_ID = 'tenant_id'`: ID of the Microsoft Entra ID tenant.

          For more information, see [CREATE NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)](/sql-reference/sql/create-notification-integration-queue-inbound-azure).

    Other notification integration parameters, such as `ENABLED`, `TYPE`, and `DIRECTION`, aren’t allowed inside a queue.

`ACTIVE = 'queue_name'`
:   Specifies the queue to set as the active queue for the integration in the current account. The value must match the `NAME` of a
    queue in the `QUEUES` list exactly, including case. Set it to the queue for the storage location that’s active in your MLSI.
    To change the active queue of an existing MQNI, use [ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue) instead of
    replacing the integration.

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

- You can’t change the `QUEUES` list or `DIRECTION` after you create the integration. To change the active queue later, use
  [ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue).
- Replacing an existing notification integration with `CREATE OR REPLACE` invalidates all pipes that use it. To change the active
  queue of an MQNI that pipes use, use [ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue) instead of replacing the
  integration. If you replace an MQNI that pipes use, set its active queue again with
  [ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue), and then recreate each pipe that uses it.
- After you create the integration, grant Snowflake access to the queue that’s active in the current account before you create pipes
  that use the integration. On Google Cloud and Azure, the values that you need for the grant, such as `GCP_PUBSUB_SERVICE_ACCOUNT`,
  `AZURE_CONSENT_URL`, and `AZURE_MULTI_TENANT_APP_NAME`, are in each queue’s entry in the `QUEUES` row of the
  [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) output. For the full procedure, see
  [Scenario A: Create a new MQNI and new pipes](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-a).
- To use the integration in a pipe, set the pipe’s `INTEGRATION` parameter to the integration name in all uppercase, such as
  `INTEGRATION = 'MY_MQNI'`. Snowflake looks up a quoted integration name exactly as you type it, and setting the active queue rebinds
  only the pipes whose `INTEGRATION` value matches the integration’s name exactly.
- When Snowflake replicates an MQNI to a target account, the replica has no active queue until you set one in that account. A pipe
  that uses the MQNI doesn’t load in the target account until you set `ACTIVE` there after the refresh that replicates the pipe, so
  set it again after each refresh that replicates new pipes. For more information, see
  [ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create an MQNI with an Amazon SNS topic for each of two Amazon S3 storage locations, and set the queue for `us-west-1` as the active
queue in the current account:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_mqni
  ENABLED = TRUE
  TYPE = MULTI_QUEUE
  DIRECTION = INBOUND
  QUEUES = (
    (
      NAME = 'my-us-west-1'
      NOTIFICATION_PROVIDER = AWS_SNS
      AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-west-1:12345:my-snowpipe-mlsi-west'
    ),
    (
      NAME = 'my-us-east-1'
      NOTIFICATION_PROVIDER = AWS_SNS
      AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:67890:my-snowpipe-mlsi-east'
    )
  )
  ACTIVE = 'my-us-west-1';
```

Create an MQNI for a storage location on Azure and another on Google Cloud, and set the Azure queue as the active queue in the
current account:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_cross_cloud_mqni
  ENABLED = TRUE
  TYPE = MULTI_QUEUE
  DIRECTION = INBOUND
  QUEUES = (
    (
      NAME = 'my-azure-eastus'
      NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
      AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myaccount.queue.core.windows.net/my-queue'
      AZURE_TENANT_ID = '<tenant_id>'
    ),
    (
      NAME = 'my-gcp-us-central1'
      NOTIFICATION_PROVIDER = GCP_PUBSUB
      GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/my-project/subscriptions/my-subscription'
    )
  )
  ACTIVE = 'my-azure-eastus';
```
