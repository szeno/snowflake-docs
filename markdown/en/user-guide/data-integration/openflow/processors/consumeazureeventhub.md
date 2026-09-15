# ConsumeAzureEventHub 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Receives messages from Microsoft Azure Event Hubs with checkpointing to ensure consistent event processing. Checkpoint tracking avoids consuming a message multiple times and enables reliable resumption of processing in the event of intermittent network failures. Checkpoint tracking requires external storage and provides the preferred approach to consuming messages from Azure Event Hubs. In clustered environment, ConsumeAzureEventHub processor instances form a consumer group and the messages are distributed among the cluster nodes (each message is processed on one cluster node only).

## Tags

azure, cloud, eventhub, events, microsoft, streaming, streams

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The number of messages to process within a NiFi session. This parameter affects throughput and consistency. NiFi commits its session and Event Hubs checkpoints after processing this number of messages. If NiFi session is committed, but fails to create an Event Hubs checkpoint, then it is possible that the same messages will be received again. The higher number, the higher throughput, but possibly less consistent. |
| Checkpoint Strategy | Specifies which strategy to use for storing and retrieving partition ownership and checkpoint information for each partition. |
| Consumer Group | The name of the consumer group to use. |
| Event Hub Name | The name of the event hub to pull messages from. |
| Event Hub Namespace | The namespace that the Azure Event Hubs is assigned to. This is generally equal to <Event Hub Names>-ns. |
| Initial Offset | Specify where to start receiving messages if offset is not yet stored in the checkpoint store. |
| Message Receive Timeout | The amount of time this consumer should wait to receive the Batch Size before returning. |
| Prefetch Count |  |
| Record Reader | The Record Reader to use for reading received messages. The event hub name can be referred by Expression Language ‘${eventhub.name}’ to access a schema. |
| Record Writer | The Record Writer to use for serializing Records to an output FlowFile. The event hub name can be referred by Expression Language ‘${eventhub.name}’ to access a schema. If not specified, each message will create a FlowFile. |
| Service Bus Endpoint | To support namespaces not in the default windows.net domain. |
| Shared Access Policy Key | The key of the shared access policy. Either the primary or the secondary key can be used. |
| Shared Access Policy Name | The name of the shared access policy. This policy must have Listen claims. |
| Storage Account Key | The Azure Storage account key to store event hub consumer group state. |
| Storage Account Name | Name of the Azure Storage account to store event hub consumer group state. |
| Storage Container Name | Name of the Azure Storage container to store the event hub consumer group state. If not specified, event hub name is used. |
| Storage SAS Token | The Azure Storage SAS token to store Event Hub consumer group state. Always starts with a ? character. |
| Transport Type | Advanced Message Queuing Protocol Transport Type for communication with Azure Event Hubs |
| Use Azure Managed Identity | Choose whether or not to use the managed identity of Azure VM/VMSS |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | Local state is used to store the client id. Cluster state is used to store partition ownership and checkpoint information when component state is configured as the checkpointing strategy. |
| CLUSTER | Local state is used to store the client id. Cluster state is used to store partition ownership and checkpoint information when component state is configured as the checkpointing strategy. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles received from Event Hub. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| eventhub.enqueued.timestamp | The time (in milliseconds since epoch, UTC) at which the message was enqueued in the event hub |
| eventhub.offset | The offset into the partition at which the message was stored |
| eventhub.sequence | The sequence number associated with the message |
| eventhub.name | The name of the event hub from which the message was pulled |
| eventhub.partition | The name of the partition from which the message was pulled |
| eventhub.property.\* | The application properties of this message. IE: ‘application’ would be ‘eventhub.property.application’ |

Expand

Show lessSee more
