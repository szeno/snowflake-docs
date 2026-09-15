# FetchGCSObject 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Fetches a file from a Google Cloud Bucket. Designed to be used in tandem with ListGCSBucket.

## Tags

fetch, gcs, google, google cloud, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| GCP Credentials Provider Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| gcp-project-id | Google Cloud Project ID |
| gcp-retry-count | How many retry attempts should be made before routing to the failure relationship. |
| gcs-bucket | Bucket of the object. |
| gcs-generation | The generation of the Object to download. If not set, the latest generation will be downloaded. |
| gcs-key | Name of the object. |
| gcs-object-range-length | The number of bytes to download from the object, starting from the Range Start. An empty value or a value that extends beyond the end of the object will read to the end of the object. |
| gcs-object-range-start | The byte position at which to start reading from the object. An empty value or a value of zero will start reading at the beginning of the object. |
| gcs-server-side-encryption-key | An AES256 Key (encoded in base64) which the object has been encrypted in. |
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
| filename | The name of the file, parsed if possible from the Content-Disposition response header |
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

## Use Cases Involving Other Components

| Retrieve all files in a Google Compute Storage (GCS) bucket |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.storage.DeleteGCSObject](/user-guide/data-integration/openflow/processors/deletegcsobject)
- [org.apache.nifi.processors.gcp.storage.ListGCSBucket](/user-guide/data-integration/openflow/processors/listgcsbucket)
- [org.apache.nifi.processors.gcp.storage.PutGCSObject](/user-guide/data-integration/openflow/processors/putgcsobject)
