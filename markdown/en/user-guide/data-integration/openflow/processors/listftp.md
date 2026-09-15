# ListFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Performs a listing of the files residing on an FTP server. For each file that is found on the remote server, a new FlowFile will be created with the filename attribute set to the name of the file on the remote server. This can then be used in conjunction with FetchFTP in order to fetch those files.

## Tags

files, ftp, ingest, input, list, remote, source

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Mode | The FTP Connection Mode |
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Entity Tracking Initial Listing Target | Specify how initial listing should be handled. Used by ‘Tracking Entities’strategy. |
| Entity Tracking State Cache | Listed entities are stored in the specified cache storage so that this processor can resume listing across NiFi restart or in case of primary node change. ‘Tracking Entities’strategy require tracking information of all listed entities within the last ‘Tracking Time Window’. To support large number of entities, the strategy uses DistributedMapCache instead of managed state. Cache key format is ‘ListedEntities::{processorId}(::{nodeId})’. If it tracks per node listed entities, then the optional ‘::{nodeId}’ part is added to manage state separately. E.g. cluster wide cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b’, per node cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b::nifi-node3’ The stored cache content is Gzipped JSON string. The cache key will be deleted when target listing configuration is changed. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Time Window | Specify how long this processor should track already-listed entities. ‘Tracking Entities’strategy can pick any entity whose timestamp is inside the specified time window. For example, if set to ’30 minutes’, any entity having timestamp in recent 30 minutes will be the listing target when this processor runs. A listed entity is considered ‘new/updated’ and a FlowFile is emitted if one of following condition meets: 1. does not exist in the already-listed entities, 2. has newer timestamp than the cached entity, 3. has different size than the cached entity. If a cached entity ‘s timestamp becomes older than specified time window, that entity will be removed from the cached already-listed entities. Used by’Tracking Entities’strategy. |
| File Filter Regex | Provides a Java Regular Expression for filtering Filenames; if a filter is supplied, only files whose names match that Regular Expression will be fetched |
| Follow Symbolic Links | If true, will pull even symbolic files and also nested symbolic subdirectories; otherwise, will not read symbolic files and will not traverse symbolic link subdirectories |
| Hostname | The fully qualified hostname or IP address of the remote system |
| Ignore Dotted Files | If true, files whose names begin with a dot (“.”) will be ignored |
| Internal Buffer Size | Set the internal buffer size for buffered data streams |
| Listing Strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| Password | Password for the user account |
| Path Filter Regex | When Search Recursively is true, then only subdirectories whose path matches the given Regular Expression will be scanned |
| Port | The port to connect to on the remote host to fetch the data from |
| Record Writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| Remote Path | The path on the remote system from which to pull or push files |
| Remote Poll Batch Size | The value specifies how many file paths to find in a given directory on the remote system when doing a file listing. This value in general should not need to be modified but when polling against a remote system with a tremendous number of files this value can be critical. Setting this value too high can result very poor performance and setting it too low can cause the flow to be slower than normal. |
| Search Recursively | If true, will pull files from arbitrarily nested subdirectories; otherwise, will not traverse subdirectories |
| Target System Timestamp Precision | Specify timestamp precision at the target system. Since this processor uses timestamp of entities to decide which should be listed, it is crucial to use the right timestamp precision. |
| Transfer Mode | The FTP Transfer Mode |
| Username | Username |
| ftp-use-utf8 | Tells the client to use UTF-8 encoding when processing files and filenames. If set to true, the server must also support UTF-8 encoding. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a listing of files, the timestamp of the newest file is stored. This allows the Processor to list only files that have been added or modified after this date the next time that the Processor is run. State is stored across the cluster so that this Processor can be run on Primary Node only and if a new Primary Node is selected, the new node will not duplicate the data that was listed by the previous Primary Node. |

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
| ftp.remote.host | The hostname of the FTP Server |
| ftp.remote.port | The port that was connected to on the FTP Server |
| ftp.listing.user | The username of the user that performed the FTP Listing |
| file.owner | The numeric owner id of the source file |
| file.group | The numeric group id of the source file |
| file.permissions | The read/write/execute permissions of the source file |
| file.size | The number of bytes in the source file |
| file.lastModifiedTime | The timestamp of when the file in the filesystem waslast modified as ‘yyyy-MM-dd’T’HH:mm:ssZ’ |
| filename | The name of the file on the FTP Server |
| path | The fully qualified name of the directory on the FTP Server from which the file was pulled |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.FetchFTP](/user-guide/data-integration/openflow/processors/fetchftp)
- [org.apache.nifi.processors.standard.GetFTP](/user-guide/data-integration/openflow/processors/getftp)
- [org.apache.nifi.processors.standard.PutFTP](/user-guide/data-integration/openflow/processors/putftp)
