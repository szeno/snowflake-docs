# ListFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Retrieves a listing of files from the input directory. For each file listed, creates a FlowFile that represents the file so that it can be fetched in conjunction with FetchFile. This Processor is designed to run on Primary Node only in a cluster when ‘Input Directory Location’ is set to ‘Remote’. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all the data. When ‘Input Directory Location’ is ‘Local’, the ‘Execution’ mode can be anything, and synchronization won’t happen. Unlike GetFile, this Processor does not delete any data from the local filesystem.

## Tags

file, filesystem, get, ingest, list, source

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Entity Tracking Initial Listing Target | Specify how initial listing should be handled. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Node Identifier | The configured value will be appended to the cache key so that listing state can be tracked per NiFi node rather than cluster wide when tracking state is scoped to LOCAL. Used by ‘Tracking Entities’strategy. |
| Entity Tracking State Cache | Listed entities are stored in the specified cache storage so that this processor can resume listing across NiFi restart or in case of primary node change. ‘Tracking Entities’strategy require tracking information of all listed entities within the last ‘Tracking Time Window’. To support large number of entities, the strategy uses DistributedMapCache instead of managed state. Cache key format is ‘ListedEntities::{processorId}(::{nodeId})’. If it tracks per node listed entities, then the optional ‘::{nodeId}’ part is added to manage state separately. E.g. cluster wide cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b’, per node cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b::nifi-node3’ The stored cache content is Gzipped JSON string. The cache key will be deleted when target listing configuration is changed. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Time Window | Specify how long this processor should track already-listed entities. ‘Tracking Entities’strategy can pick any entity whose timestamp is inside the specified time window. For example, if set to ’30 minutes’, any entity having timestamp in recent 30 minutes will be the listing target when this processor runs. A listed entity is considered ‘new/updated’ and a FlowFile is emitted if one of following condition meets: 1. does not exist in the already-listed entities, 2. has newer timestamp than the cached entity, 3. has different size than the cached entity. If a cached entity ‘s timestamp becomes older than specified time window, that entity will be removed from the cached already-listed entities. Used by’Tracking Entities’strategy. |
| File Filter | Only files whose names match the given regular expression will be picked up |
| Ignore Hidden Files | Indicates whether or not hidden files should be ignored |
| Include File Attributes | Whether or not to include information such as the file’s Last Modified Time and Owner as FlowFile Attributes. Depending on the File System being used, gathering this information can be expensive and as a result should be disabled. This is especially true of remote file shares. |
| Input Directory | The input directory from which files to pull files |
| Input Directory Location | Specifies where the Input Directory is located. This is used to determine whether state should be stored locally or across the cluster. |
| Listing Strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| Maximum File Age | The maximum age that a file must be in order to be pulled; any file older than this amount of time (according to last modification date) will be ignored |
| Maximum File Size | The maximum size that a file can be in order to be pulled |
| Minimum File Age | The minimum age that a file must be in order to be pulled; any file younger than this amount of time (according to last modification date) will be ignored |
| Minimum File Size | The minimum size that a file must be in order to be pulled |
| Path Filter | When Recurse Subdirectories is true, then only subdirectories whose path matches the given regular expression will be scanned |
| Record Writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| Recurse Subdirectories | Indicates whether to list files from subdirectories of the directory |
| Target System Timestamp Precision | Specify timestamp precision at the target system. Since this processor uses timestamp of entities to decide which should be listed, it is crucial to use the right timestamp precision. |
| max-listing-time | The maximum amount of time that listing any single directory is expected to take. If the listing for the directory specified by the ‘Input Directory’ property, or the listing of any subdirectory (if ‘Recurse’ is set to true) takes longer than this amount of time, a warning bulletin will be generated for each directory listing that exceeds this amount of time. |
| max-operation-time | The maximum amount of time that any single disk operation is expected to take. If any disk operation takes longer than this amount of time, a warning bulletin will be generated for each operation that exceeds this amount of time. |
| max-performance-metrics | If the ‘Track Performance’ property is set to ‘true’, this property indicates the maximum number of files whose performance metrics should be held onto. A smaller value for this property will result in less heap utilization, while a larger value may provide more accurate insights into how the disk access operations are performing |
| track-performance | Whether or not the Processor should track the performance of disk access operations. If true, all accesses to disk will be recorded, including the file being accessed, the information being obtained, and how long it takes. This is then logged periodically at a DEBUG level. While the amount of data will be capped, this option may still consume a significant amount of heap (controlled by the ‘Maximum Number of Files to Track’ property), but it can be very useful for troubleshooting purposes if performance is poor is degraded. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | After performing a listing of files, the timestamp of the newest file is stored. This allows the Processor to list only files that have been added or modified after this date the next time that the Processor is run. Whether the state is stored with a Local or Cluster scope depends on the value of the <Input Directory Location> property. |
| CLUSTER | After performing a listing of files, the timestamp of the newest file is stored. This allows the Processor to list only files that have been added or modified after this date the next time that the Processor is run. Whether the state is stored with a Local or Cluster scope depends on the value of the <Input Directory Location> property. |

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
| path | The path is set to the relative path of the file’s directory on filesystem compared to the Input Directory property. For example, if Input Directory is set to /tmp, then files picked up from /tmp will have the path attribute set to “/”. If the Recurse Subdirectories property is set to true and a file is picked up from /tmp/abc/1/2/3, then the path attribute will be set to “abc/1/2/3/”. |
| absolute.path | The absolute.path is set to the absolute path of the file’s directory on filesystem. For example, if the Input Directory property is set to /tmp, then files picked up from /tmp will have the path attribute set to “/tmp/”. If the Recurse Subdirectories property is set to true and a file is picked up from /tmp/abc/1/2/3, then the path attribute will be set to “/tmp/abc/1/2/3/”. |
| file.owner | The user that owns the file in filesystem |
| file.group | The group that owns the file in filesystem |
| file.size | The number of bytes in the file in filesystem |
| file.permissions | The permissions for the file in filesystem. This is formatted as 3 characters for the owner, 3 for the group, and 3 for other users. For example rw-rw-r– |
| file.lastModifiedTime | The timestamp of when the file in filesystem was last modified as ‘yyyy-MM-dd’T’HH:mm:ssZ’ |
| file.lastAccessTime | The timestamp of when the file in filesystem was last accessed as ‘yyyy-MM-dd’T’HH:mm:ssZ’ |
| file.creationTime | The timestamp of when the file in filesystem was created as ‘yyyy-MM-dd’T’HH:mm:ssZ’ |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.FetchFile](/user-guide/data-integration/openflow/processors/fetchfile)
- [org.apache.nifi.processors.standard.GetFile](/user-guide/data-integration/openflow/processors/getfile)
- [org.apache.nifi.processors.standard.PutFile](/user-guide/data-integration/openflow/processors/putfile)
