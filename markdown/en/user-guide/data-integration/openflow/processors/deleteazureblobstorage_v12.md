# DeleteAzureBlobStorage\_v12 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Deletes the specified blob from Azure Blob Storage. The processor uses Azure Blob Storage client library v12.

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
| Container Name | Name of the Azure storage container. In case of PutAzureBlobStorage processor, container can be created if it does not exist. |
| Delete Snapshots Option | Specifies the snapshot deletion options to be used when deleting a blob. |
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

## See also

- [org.apache.nifi.processors.azure.storage.CopyAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/copyazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.FetchAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/fetchazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.ListAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/listazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.PutAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/putazureblobstorage_v12)
