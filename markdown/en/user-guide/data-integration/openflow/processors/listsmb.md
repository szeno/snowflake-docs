# ListSmb 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-smb-nar

## Description

Lists concrete files shared via SMB protocol. Each listed file may result in one FlowFile, the metadata being written as FlowFile attributes. Or - in case the ‘Record Writer’ property is set - the entire result is written as records to a single FlowFile. This Processor is designed to run on Primary Node only in a cluster. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all of the data.

## Tags

list, samba, smb, cifs, files

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Entity Tracking Initial Listing Target | Specify how initial listing should be handled. Used by ‘Tracking Entities’strategy. |
| Entity Tracking State Cache | Listed entities are stored in the specified cache storage so that this processor can resume listing across NiFi restart or in case of primary node change. ‘Tracking Entities’strategy require tracking information of all listed entities within the last ‘Tracking Time Window’. To support large number of entities, the strategy uses DistributedMapCache instead of managed state. Cache key format is ‘ListedEntities::{processorId}(::{nodeId})’. If it tracks per node listed entities, then the optional ‘::{nodeId}’ part is added to manage state separately. E.g. cluster wide cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b’, per node cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b::nifi-node3’ The stored cache content is Gzipped JSON string. The cache key will be deleted when target listing configuration is changed. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Time Window | Specify how long this processor should track already-listed entities. ‘Tracking Entities’strategy can pick any entity whose timestamp is inside the specified time window. For example, if set to ’30 minutes’, any entity having timestamp in recent 30 minutes will be the listing target when this processor runs. A listed entity is considered ‘new/updated’ and a FlowFile is emitted if one of following condition meets: 1. does not exist in the already-listed entities, 2. has newer timestamp than the cached entity, 3. has different size than the cached entity. If a cached entity ‘s timestamp becomes older than specified time window, that entity will be removed from the cached already-listed entities. Used by’Tracking Entities’strategy. |
| Listing Strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| Record Writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| Target System Timestamp Precision | Specify timestamp precision at the target system. Since this processor uses timestamp of entities to decide which should be listed, it is crucial to use the right timestamp precision. |
| directory | The network folder from which to list files. This is the remaining relative path after the share: [smb://HOSTNAME:PORT/SHARE/[DIRECTORY]/sub/directories](smb://HOSTNAME:PORT/SHARE/%5BDIRECTORY%5D/sub/directories). It is also possible to add subdirectories. The given path on the remote file share must exist. This can be checked using verification. You may mix Windows and Linux-style directory separators. |
| file-filter | Only files whose names match the given regular expression will be listed. |
| file-name-suffix-filter | Files ending with the given suffix will be omitted. Can be used to make sure that files that are still uploading are not listed multiple times, by having those files have a suffix and remove the suffix once the upload finishes. This is highly recommended when using ‘Tracking Entities’ or ‘Tracking Timestamps’ listing strategies. |
| initial-listing-strategy | Specifies how to handle existing files on the SMB share when the processor is started for the first time (or its state has been cleared). |
| initial-listing-timestamp | The timestamp from which the files will be listed when the processor is started for the first time (or its state has been cleared). The value can be specified as an epoch timestamp in milliseconds or as a UTC datetime in a format such as 2025-02-01T00:00:00Z |
| max-file-age | Any file older than the given value will be omitted. |
| max-file-size | Any file larger than the given value will be omitted. |
| min-file-age | The minimum age that a file must be in order to be listed; any file younger than this amount of time will be ignored. |
| min-file-size | Any file smaller than the given value will be omitted. |
| path-filter | Only files whose paths (up to the file’s parent directory) match the given regular expression will be listed. |
| smb-client-provider-service | Specifies the SMB client provider to use for creating SMB connections. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a listing of files, the state of the previous listing can be stored in order to list files continuously without duplication. |

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
| filename | The name of the file that was read from filesystem. |
| shortName | The short name of the file that was read from filesystem. |
| path | The path is set to the relative path of the file’s directory on the remote filesystem compared to the Share root directory. For example, for a given remote locationsmb://HOSTNAME:PORT/SHARE/DIRECTORY, and a file is being listed from smb://HOSTNAME:PORT/SHARE/DIRECTORY/sub/folder/file then the path attribute will be set to “DIRECTORY/sub/folder”. |
| serviceLocation | The SMB URL of the share. |
| lastModifiedTime | The timestamp of when the file’s content changed in the filesystem as ‘yyyy-MM-dd’T’HH:mm:ss’. |
| creationTime | The timestamp of when the file was created in the filesystem as ‘yyyy-MM-dd’T’HH:mm:ss’. |
| lastAccessTime | The timestamp of when the file was accessed in the filesystem as ‘yyyy-MM-dd’T’HH:mm:ss’. |
| changeTime | The timestamp of when the file’s attributes was changed in the filesystem as ‘yyyy-MM-dd’T’HH:mm:ss’. |
| size | The size of the file in bytes. |
| allocationSize | The number of bytes allocated for the file on the server. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.smb.FetchSmb](/user-guide/data-integration/openflow/processors/fetchsmb)
- [org.apache.nifi.processors.smb.GetSmbFile](/user-guide/data-integration/openflow/processors/getsmbfile)
- [org.apache.nifi.processors.smb.PutSmbFile](/user-guide/data-integration/openflow/processors/putsmbfile)
