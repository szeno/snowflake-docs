# DeleteGCSObject 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Deletes objects from a Google Cloud Bucket. If attempting to delete a file that does not exist, FlowFile is routed to success.

## Tags

delete, gcs, google, google cloud, storage

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
| gcs-generation | The generation of the object to be deleted. If null, will use latest version of the object. |
| gcs-key | Name of the object. |
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

## See also

- [org.apache.nifi.processors.gcp.storage.FetchGCSObject](/user-guide/data-integration/openflow/processors/fetchgcsobject)
- [org.apache.nifi.processors.gcp.storage.ListGCSBucket](/user-guide/data-integration/openflow/processors/listgcsbucket)
- [org.apache.nifi.processors.gcp.storage.PutGCSObject](/user-guide/data-integration/openflow/processors/putgcsobject)
