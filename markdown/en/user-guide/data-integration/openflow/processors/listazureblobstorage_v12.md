# ListAzureBlobStorage\_v12 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Lists blobs in an Azure Blob Storage container. Listing details are attached to an empty FlowFile for use with FetchAzureBlobStorage. This Processor is designed to run on Primary Node only in a cluster. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all of the data. The processor uses Azure Blob Storage client library v12.

## Tags

azure, blob, cloud, microsoft, storage

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Blob Name Prefix | Search prefix for listing |
| Container Name | Name of the Azure storage container. In case of PutAzureBlobStorage processor, container can be created if it does not exist. |
| Entity Tracking Initial Listing Target | Specify how initial listing should be handled. Used by ‘Tracking Entities’strategy. |
| Entity Tracking State Cache | Listed entities are stored in the specified cache storage so that this processor can resume listing across NiFi restart or in case of primary node change. ‘Tracking Entities’strategy require tracking information of all listed entities within the last ‘Tracking Time Window’. To support large number of entities, the strategy uses DistributedMapCache instead of managed state. Cache key format is ‘ListedEntities::{processorId}(::{nodeId})’. If it tracks per node listed entities, then the optional ‘::{nodeId}’ part is added to manage state separately. E.g. cluster wide cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b’, per node cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b::nifi-node3’ The stored cache content is Gzipped JSON string. The cache key will be deleted when target listing configuration is changed. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Time Window | Specify how long this processor should track already-listed entities. ‘Tracking Entities’strategy can pick any entity whose timestamp is inside the specified time window. For example, if set to ’30 minutes’, any entity having timestamp in recent 30 minutes will be the listing target when this processor runs. A listed entity is considered ‘new/updated’ and a FlowFile is emitted if one of following condition meets: 1. does not exist in the already-listed entities, 2. has newer timestamp than the cached entity, 3. has different size than the cached entity. If a cached entity ‘s timestamp becomes older than specified time window, that entity will be removed from the cached already-listed entities. Used by’Tracking Entities’strategy. |
| Listing Strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| Maximum File Age | The maximum age that a file must be in order to be pulled; any file older than this amount of time (according to last modification date) will be ignored |
| Maximum File Size | The maximum size that a file can be in order to be pulled |
| Minimum File Age | The minimum age that a file must be in order to be pulled; any file younger than this amount of time (according to last modification date) will be ignored |
| Minimum File Size | The minimum size that a file must be in order to be pulled |
| Record Writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| Storage Credentials | Controller Service used to obtain Azure Blob Storage Credentials. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a listing of blobs, the timestamp of the newest blob is stored if ‘Tracking Timestamps’ Listing Strategy is in use (by default). This allows the Processor to list only blobs that have been added or modified after this date the next time that the Processor is run. State is stored across the cluster so that this Processor can be run on Primary Node only and if a new Primary Node is selected, the new node can pick up where the previous node left off, without duplicating the data. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles that are received are routed to success |

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

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.CopyAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/copyazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.DeleteAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/deleteazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.FetchAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/fetchazureblobstorage_v12)
- [org.apache.nifi.processors.azure.storage.PutAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/putazureblobstorage_v12)
