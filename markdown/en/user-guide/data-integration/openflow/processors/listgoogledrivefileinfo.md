# ListGoogleDriveFileInfo 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-drive-nar

## Description

Lists all files and folders in a specified Google Drive. The processor requires a Drive ID and can optionally list files recursively through all folders within the drive.

## Tags

cloud, drive, files, gcp, google, list, openflow, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Drive ID | The ID of the drive to list files from. This can be a shared drive ID. |
| GCP Credentials Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| Include Folders | When ‘true’, both files and folders will be included in the results. When ‘false’, only files (not folders) will be included. |
| Minimum File Age | The minimum age a file must be in order to be considered; any files younger than this will be ignored. |
| Record Writer | Specifies the Controller Service to use for writing the metadata records. Must be set. |
| Search Recursively | When ‘true’, will recursively list files in all folders within the drive. When ‘false’, will only list files at the root level of the drive. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile will be routed here if there is an error fetching file metadata. |
| retry | A FlowFile is routed here if the processor should retry the request (e.g., after rate limiting). |
| success | A FlowFile containing the file metadata records will be routed to this relationship upon successful processing. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| google.drive.drive.id | The ID of the drive from which files were listed |
| record.count | The number of records in the FlowFile |
| mime.type | The MIME Type specified by the Record Writer |
| google.drive.error.code | The error code if the request to Google Drive API fails |
| google.drive.error.message | The error message if the request to Google Drive API fails |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.google.CaptureGoogleDriveChanges](/user-guide/data-integration/openflow/processors/capturegoogledrivechanges)
- [com.snowflake.openflow.runtime.processors.google.FetchGoogleDriveMetadata](/user-guide/data-integration/openflow/processors/fetchgoogledrivemetadata)
