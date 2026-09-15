# ListGoogleDrive 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Performs a listing of concrete files (shortcuts are ignored) in a Google Drive folder. If the ‘Record Writer’ property is set, a single Output FlowFile is created, and each file in the listing is written as a single record to the output file. Otherwise, for each file in the listing, an individual FlowFile is created, the metadata being written as FlowFile attributes. This Processor is designed to run on Primary Node only in a cluster. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all of the data. Please see Additional Details to set up access to Google Drive.

## Tags

drive, google, storage

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
| connect-timeout | Maximum wait time for connection to Google Drive service. |
| folder-id | The ID of the folder from which to pull list of files. Please see Additional Details to set up access to Google Drive and obtain Folder ID. WARNING: Unauthorized access to the folder is treated as if the folder was empty. This results in the processor not creating outgoing FlowFiles. No additional error message is provided. |
| gcp-credentials-provider-service | The Controller Service used to obtain Google Cloud Platform credentials. |
| min-age | The minimum age a file must be in order to be considered; any files younger than this will be ignored. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |
| read-timeout | Maximum wait time for response from Google Drive service. |
| recursive-search | When ‘true’, will include list of files from concrete sub-folders (ignores shortcuts). Otherwise, will return only files that have the defined ‘Folder ID’ as their parent directly. WARNING: The listing may fail if there are too many sub-folders (500+). |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | The processor stores necessary data to be able to keep track what files have been listed already. What exactly needs to be stored depends on the ‘Listing Strategy’. State is stored across the cluster so that this Processor can be run on Primary Node only and if a new Primary Node is selected, the new node can pick up where the previous node left off, without duplicating the data. |

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
| drive.id | The id of the file |
| filename | The name of the file |
| mime.type | The MIME type of the file |
| drive.size | The size of the file. Set to 0 when the file size is not available (e.g. externally stored files). |
| drive.size.available | Indicates if the file size is known / available |
| drive.timestamp | The last modified time or created time (whichever is greater) of the file. The reason for this is that the original modified date of a file is preserved when uploaded to Google Drive. ‘Created time’ takes the time when the upload occurs. However uploaded files can still be modified later. |
| drive.created.time | The file’s creation time |
| drive.modified.time | The file’s last modification time |
| drive.path | The path of the file’s directory from the base directory. The path contains the folder names in URL encoded form because Google Drive allows special characters in file names, including ‘/’ (slash) and ‘’ (backslash). The URL encoded folder names are separated by ‘/’ in the path. |
| drive.owner | The owner of the file |
| drive.last.modifying.user | The last modifying user of the file |
| drive.web.view.link | Web view link to the file |
| drive.web.content.link | Web content link to the file |
| drive.parent.folder.id | The id of the file’s parent folder |
| drive.parent.folder.name | The name of the file’s parent folder |
| drive.listed.folder.id | The id of the base folder that was listed |
| drive.listed.folder.name | The name of the base folder that was listed |
| drive.shared.drive.id | The id of the shared drive (if the file is located on a shared drive) |
| drive.shared.drive.name | The name of the shared drive (if the file is located on a shared drive) |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.drive.FetchGoogleDrive](/user-guide/data-integration/openflow/processors/fetchgoogledrive)
- [org.apache.nifi.processors.gcp.drive.PutGoogleDrive](/user-guide/data-integration/openflow/processors/putgoogledrive)
