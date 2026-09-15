# GetAzureQueueStorage\_v12 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Retrieves the messages from an Azure Queue Storage. The retrieved messages will be deleted from the queue by default. If the requirement is to consume messages without deleting them, set ‘Auto Delete Messages’ to ‘false’. Note: There might be chances of receiving duplicates in situations like when a message is received but was unable to be deleted from the queue due to some unexpected situations.

## Tags

azure, cloud, dequeue, microsoft, queue, storage

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Auto Delete Messages | Specifies whether the received message is to be automatically deleted from the queue. |
| Credentials Service | Controller Service used to obtain Azure Storage Credentials. |
| Endpoint Suffix | Storage accounts in public Azure always use a common FQDN suffix. Override this endpoint suffix with a different suffix in certain circumstances (like Azure Stack or non-public Azure regions). |
| Message Batch Size | The number of messages to be retrieved from the queue. |
| Queue Name | Name of the Azure Storage Queue |
| Request Timeout | The timeout for read or write requests to Azure Queue Storage. Defaults to 1 second. |
| Visibility Timeout | The duration during which the retrieved message should be invisible to other consumers. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All successfully processed FlowFiles are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| azure.queue.uri | The absolute URI of the configured Azure Queue Storage |
| azure.queue.insertionTime | The time when the message was inserted into the queue storage |
| azure.queue.expirationTime | The time when the message will expire from the queue storage |
| azure.queue.messageId | The ID of the retrieved message |
| azure.queue.popReceipt | The pop receipt of the retrieved message |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.queue.PutAzureQueueStorage\_v12](/user-guide/data-integration/openflow/processors/putazurequeuestorage_v12)
