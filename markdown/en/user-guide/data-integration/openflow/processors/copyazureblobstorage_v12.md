# CopyAzureBlobStorage\_v12 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Copies a blob in Azure Blob Storage from one account/container to another. The processor uses Azure Blob Storage client library v12.

## Tags

azure, blob, cloud, microsoft, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Conflict Resolution Strategy | Specifies whether an existing blob will have its contents replaced upon conflict. |
| Create Container | Specifies whether to check if the container exists and to automatically create it if it does not. Permission to list containers is required. If false, this check is not made, but the Put operation will fail if the container does not exist. |
| Destination Blob Name | The full name of the destination blob defaults to the Source Blob Name when not specified |
| Destination Container Name | Name of the Azure storage container destination defaults to the Source Container Name when not specified |
| Destination Storage Credentials | Controller Service used to obtain Azure Blob Storage Credentials. |
| Source Blob Name | The full name of the source blob |
| Source Container Name | Name of the Azure storage container that will be copied |
| Source Storage Credentials | Credentials Service used to obtain Azure Blob Storage Credentials to read Source Blob information |
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

## Writes attributes

| Name | Description |
| --- | --- |
| azure.container | The name of the Azure Blob Storage container |
| azure.blobname | The name of the blob on Azure Blob Storage |
| azure.primaryUri | Primary location of the blob |
| azure.etag | ETag of the blob |
| azure.blobtype | Type of the blob (either BlockBlob, PageBlob or AppendBlob) |
| mime.type | MIME Type of the content |
| lang | Language code for the content |
| azure.timestamp | Timestamp of the blob |
| azure.length | Length of the blob |
| azure.error.code | Error code reported during blob operation |
| azure.ignored | When Conflict Resolution Strategy is ‘ignore’, this property will be true/false depending on whether the blob was ignored. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.DeleteAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/deleteazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.FetchAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/fetchazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.ListAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/listazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.PutAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/putazureblobstorage_v12)
