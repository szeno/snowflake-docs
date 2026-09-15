# PutAzureBlobStorage\_v12 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Puts content into a blob on Azure Blob Storage. The processor uses Azure Blob Storage client library v12.

## Tags

azure, blob, cloud, microsoft, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Blob Name | The full name of the blob |
| Client-Side Encryption Key ID | Specifies the ID of the key to use for client-side encryption. |
| Client-Side Encryption Key Type | Specifies the key type to use for client-side encryption. |
| Client-Side Encryption Local Key | When using local client-side encryption, this is the raw key, encoded in hexadecimal |
| Conflict Resolution Strategy | Specifies whether an existing blob will have its contents replaced upon conflict. |
| Container Name | Name of the Azure storage container. In case of PutAzureBlobStorage processor, container can be created if it does not exist. |
| Create Container | Specifies whether to check if the container exists and to automatically create it if it does not. Permission to list containers is required. If false, this check is not made, but the Put operation will fail if the container does not exist. |
| File Resource Service | File Resource Service providing access to the local resource to be transferred |
| Resource Transfer Source | The source of the content to be transferred |
| Storage Credentials | Controller Service used to obtain Azure Blob Storage Credentials. |
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

- [org.apache.nifi.processors.azure.storage.CopyAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/copyazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.DeleteAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/deleteazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.FetchAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/fetchazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.ListAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/listazureblobstorage_v12)
