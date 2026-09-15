# PutAzureQueueStorage\_v12 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Writes the content of the incoming FlowFiles to the configured Azure Queue Storage.

## Tags

azure, cloud, enqueue, microsoft, queue, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Credentials Service | Controller Service used to obtain Azure Storage Credentials. |
| Endpoint Suffix | Storage accounts in public Azure always use a common FQDN suffix. Override this endpoint suffix with a different suffix in certain circumstances (like Azure Stack or non-public Azure regions). |
| Message Time To Live | Maximum time to allow the message to be in the queue |
| Queue Name | Name of the Azure Storage Queue |
| Request Timeout | The timeout for read or write requests to Azure Queue Storage. Defaults to 1 second. |
| Visibility Timeout | The length of time during which the message will be invisible after it is read. If the processing unit fails to delete the message after it is read, then the message will reappear in the queue. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Unsuccessful operations will be transferred to the failure relationship. |
| success | All successfully processed FlowFiles are routed to this relationship |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.queue.GetAzureQueueStorage\_v12](/user-guide/data-integration/openflow/processors/getazurequeuestorage_v12)
