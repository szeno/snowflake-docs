# ListBoxFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Lists files in a Box folder. Each listed file may result in one FlowFile, the metadata being written as FlowFile attributes. Or - in case the ‘Record Writer’ property is set - the entire result is written as records to a single FlowFile. This Processor is designed to run on Primary Node only in a cluster. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all of the data.

## Tags

box, storage

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| Entity Tracking Initial Listing Target | Specify how initial listing should be handled. Used by ‘Tracking Entities’strategy. |
| Entity Tracking State Cache | Listed entities are stored in the specified cache storage so that this processor can resume listing across NiFi restart or in case of primary node change. ‘Tracking Entities’strategy require tracking information of all listed entities within the last ‘Tracking Time Window’. To support large number of entities, the strategy uses DistributedMapCache instead of managed state. Cache key format is ‘ListedEntities::{processorId}(::{nodeId})’. If it tracks per node listed entities, then the optional ‘::{nodeId}’ part is added to manage state separately. E.g. cluster wide cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b’, per node cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b::nifi-node3’ The stored cache content is Gzipped JSON string. The cache key will be deleted when target listing configuration is changed. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Time Window | Specify how long this processor should track already-listed entities. ‘Tracking Entities’strategy can pick any entity whose timestamp is inside the specified time window. For example, if set to ’30 minutes’, any entity having timestamp in recent 30 minutes will be the listing target when this processor runs. A listed entity is considered ‘new/updated’ and a FlowFile is emitted if one of following condition meets: 1. does not exist in the already-listed entities, 2. has newer timestamp than the cached entity, 3. has different size than the cached entity. If a cached entity ‘s timestamp becomes older than specified time window, that entity will be removed from the cached already-listed entities. Used by’Tracking Entities’strategy. |
| Folder ID | The ID of the folder from which to pull list of files. |
| Listing Strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| Minimum File Age | The minimum age a file must be in order to be considered; any files younger than this will be ignored. |
| Record Writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| Search Recursively | When ‘true’, will include list of files from sub-folders. Otherwise, will return only files that are within the folder defined by the ‘Folder ID’ property. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | The processor stores necessary data to be able to keep track what files have been listed already. What exactly needs to be stored depends on the ‘Listing Strategy’. |

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
| box.id | The id of the file |
| filename | The name of the file |
| path | The folder path where the file is located |
| box.size | The size of the file |
| box.timestamp | The last modified time of the file |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.PutBoxFile](/user-guide/data-integration/openflow/processors/putboxfile)
