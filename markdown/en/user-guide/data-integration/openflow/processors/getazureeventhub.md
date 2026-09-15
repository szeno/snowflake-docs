# GetAzureEventHub 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Receives messages from Microsoft Azure Event Hubs without reliable checkpoint tracking. In clustered environment, GetAzureEventHub processor instances work independently and all cluster nodes process all messages (unless running the processor in Primary Only mode). ConsumeAzureEventHub offers the recommended approach to receiving messages from Azure Event Hubs. This processor creates a thread pool for connections to Azure Event Hubs.

## Tags

azure, cloud, eventhub, events, microsoft, streaming, streams

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Consumer Group | The name of the consumer group to use when pulling events |
| Event Hub Name | Name of Azure Event Hubs source |
| Event Hub Namespace | Namespace of Azure Event Hubs prefixed to Service Bus Endpoint domain |
| Message Enqueue Time | A timestamp (ISO-8601 Instant) formatted as YYYY-MM-DDThhmmss.sssZ (2016-01-01T01:01:01.000Z) from which messages should have been enqueued in the Event Hub to start reading from |
| Partition Receiver Fetch Size | The number of events that a receiver should fetch from an Event Hubs partition before returning. The default is 100 |
| Partition Receiver Timeout | The amount of time in milliseconds a Partition Receiver should wait to receive the Fetch Size before returning. The default is 60000 |
| Service Bus Endpoint | To support namespaces not in the default windows.net domain. |
| Shared Access Policy Key | The key of the shared access policy. Either the primary or the secondary key can be used. |
| Shared Access Policy Name | The name of the shared access policy. This policy must have Listen claims. |
| Transport Type | Advanced Message Queuing Protocol Transport Type for communication with Azure Event Hubs |
| Use Azure Managed Identity | Choose whether or not to use the managed identity of Azure VM/VMSS |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Any FlowFile that is successfully received from the event hub will be transferred to this Relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| eventhub.enqueued.timestamp | The time (in milliseconds since epoch, UTC) at which the message was enqueued in the event hub |
| eventhub.offset | The offset into the partition at which the message was stored |
| eventhub.sequence | The Azure sequence number associated with the message |
| eventhub.name | The name of the event hub from which the message was pulled |
| eventhub.partition | The name of the event hub partition from which the message was pulled |
| eventhub.property.\* | The application properties of this message. IE: ‘application’ would be ‘eventhub.property.application’ |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.eventhub.ConsumeAzureEventHub](/user-guide/data-integration/openflow/processors/consumeazureeventhub)
