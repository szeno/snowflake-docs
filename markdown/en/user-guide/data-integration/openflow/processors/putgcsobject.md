# PutGCSObject 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Writes the contents of a FlowFile as an object in a Google Cloud Storage.

## Tags

archive, gcs, google, google cloud, put

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| File Resource Service | File Resource Service providing access to the local resource to be transferred |
| GCP Credentials Provider Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| Resource Transfer Source | The source of the content to be transferred |
| gcp-project-id | Google Cloud Project ID |
| gcp-retry-count | How many retry attempts should be made before routing to the failure relationship. |
| gcs-bucket | Bucket of the object. |
| gcs-content-disposition-type | Type of RFC-6266 Content Disposition to be attached to the object |
| gcs-content-type | Content Type for the file, i.e. text/plain |
| gcs-key | Name of the object. |
| gcs-object-acl | Access Control to be attached to the object uploaded. Not providing this will revert to bucket defaults. |
| gcs-object-crc32c | CRC32C Checksum (encoded in Base64, big-Endian order) of the file for server-side validation. |
| gcs-overwrite-object | If false, the upload to GCS will succeed only if the object does not exist. |
| gcs-server-side-encryption-key | An AES256 Encryption Key (encoded in base64) for server-side encryption of the object. |
| gzip.content.enabled | Signals to the GCS Blob Writer whether GZIP compression during transfer is desired. False means do not gzip and can boost performance in many cases. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |
| storage-api-url | Overrides the default storage URL. Configuring an alternative Storage API URL also overrides the HTTP Host header on requests as described in the Google documentation for Private Service Connections. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to this relationship if the Google Cloud Storage operation fails. |
| success | FlowFiles are routed to this relationship after a successful Google Cloud Storage operation. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
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
| gcs.uri | The URI of the object as a string. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.storage.DeleteGCSObject](/user-guide/data-integration/openflow/processors/deletegcsobject)
- [org.apache.nifi.processors.gcp.storage.FetchGCSObject](/user-guide/data-integration/openflow/processors/fetchgcsobject)
- [org.apache.nifi.processors.gcp.storage.ListGCSBucket](/user-guide/data-integration/openflow/processors/listgcsbucket)
