# PutGoogleDrive 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Writes the contents of a FlowFile as a file in Google Drive.

## Tags

drive, google, put, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| chunked-upload-size | Defines the size of a chunk. Used when a FlowFile ‘s size exceeds’Chunked Upload Threshold’ and content is uploaded in smaller chunks. Minimum allowed chunk size is 256 KB, maximum allowed chunk size is 1 GB. |
| chunked-upload-threshold | The maximum size of the content which is uploaded at once. FlowFiles larger than this threshold are uploaded in chunks. |
| conflict-resolution-strategy | Indicates what should happen when a file with the same name already exists in the specified Google Drive folder. |
| connect-timeout | Maximum wait time for connection to Google Drive service. |
| file-name | The name of the file to upload to the specified Google Drive folder. |
| folder-id | The ID of the shared folder. Please see Additional Details to set up access to Google Drive and obtain Folder ID. |
| gcp-credentials-provider-service | The Controller Service used to obtain Google Cloud Platform credentials. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |
| read-timeout | Maximum wait time for response from Google Drive service. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Files that could not be written to Google Drive for some reason are transferred to this relationship. |
| success | Files that have been successfully written to Google Drive are transferred to this relationship. |

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
| error.code | The error code returned by Google Drive |
| error.message | The error message returned by Google Drive |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.drive.FetchGoogleDrive](/user-guide/data-integration/openflow/processors/fetchgoogledrive)
- [org.apache.nifi.processors.gcp.drive.ListGoogleDrive](/user-guide/data-integration/openflow/processors/listgoogledrive)
