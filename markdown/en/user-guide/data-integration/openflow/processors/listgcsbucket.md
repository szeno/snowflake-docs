# ListGCSBucket 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Retrieves a listing of objects from a GCS bucket. For each object that is listed, creates a FlowFile that represents the object so that it can be fetched in conjunction with FetchGCSObject. This Processor is designed to run on Primary Node only in a cluster. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all of the data.

## Tags

gcs, google, google cloud, list, storage

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
| GCP Credentials Provider Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| gcp-project-id | Google Cloud Project ID |
| gcp-retry-count | How many retry attempts should be made before routing to the failure relationship. |
| gcs-bucket | Bucket of the object. |
| gcs-prefix | The prefix used to filter the object list. In most cases, it should end with a forward slash ( ‘/’). |
| gcs-use-generations | Specifies whether to use GCS Generations, if applicable. If false, only the latest version of each object will be returned. |
| listing-strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |
| record-writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| storage-api-url | Overrides the default storage URL. Configuring an alternative Storage API URL also overrides the HTTP Host header on requests as described in the Google documentation for Private Service Connections. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a listing of keys, the timestamp of the newest key is stored, along with the keys that share that same timestamp. This allows the Processor to list only keys that have been added or modified after this date the next time that the Processor is run. State is stored across the cluster so that this Processor can be run on Primary Node only and if a new Primary Node is selected, the new node can pick up where the previous node left off, without duplicating the data. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles are routed to this relationship after a successful Google Cloud Storage operation. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The name of the file |
| gcs.bucket | Bucket of the object. |
| gcs.key | Name of the object. |
| gcs.size | Size of the object. |
| gcs.cache.control | Data cache control of the object. |
| gcs.component.count | The number of components which make up the object. |
| gcs.content.disposition | The data content disposition of the object. |
| gcs.content.encoding | The content encoding of the object. |
| gcs.content.language | The content language of the object. |
| mime.type | The MIME/Content-Type of the object |
| gcs.crc32c | The CRC32C checksum of object’s data, encoded in base64 in big-endian order. |
| gcs.create.time | The creation time of the object (milliseconds) |
| gcs.update.time | The last modification time of the object (milliseconds) |
| gcs.encryption.algorithm | The algorithm used to encrypt the object. |
| gcs.encryption.sha256 | The SHA256 hash of the key used to encrypt the object |
| gcs.etag | The HTTP 1.1 Entity tag for the object. |
| gcs.generated.id | The service-generated for the object |
| gcs.generation | The data generation of the object. |
| gcs.md5 | The MD5 hash of the object’s data encoded in base64. |
| gcs.media.link | The media download link to the object. |
| gcs.metageneration | The metageneration of the object. |
| gcs.owner | The owner (uploader) of the object. |
| gcs.owner.type | The ACL entity type of the uploader of the object. |
| gcs.acl.owner | A comma-delimited list of ACL entities that have owner access to the object. Entities will be either email addresses, domains, or project IDs. |
| gcs.acl.writer | A comma-delimited list of ACL entities that have write access to the object. Entities will be either email addresses, domains, or project IDs. |
| gcs.acl.reader | A comma-delimited list of ACL entities that have read access to the object. Entities will be either email addresses, domains, or project IDs. |
| gcs.uri | The URI of the object as a string. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.storage.DeleteGCSObject](/user-guide/data-integration/openflow/processors/deletegcsobject)
- [org.apache.nifi.processors.gcp.storage.FetchGCSObject](/user-guide/data-integration/openflow/processors/fetchgcsobject)
- [org.apache.nifi.processors.gcp.storage.PutGCSObject](/user-guide/data-integration/openflow/processors/putgcsobject)
