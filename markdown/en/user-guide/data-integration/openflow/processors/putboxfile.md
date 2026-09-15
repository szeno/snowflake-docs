# PutBoxFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Puts content to a Box folder.

## Tags

box, put, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| Chunked Upload Threshold | The maximum size of the content which is uploaded at once. FlowFiles larger than this threshold are uploaded in chunks. Chunked upload is allowed for files larger than 20 MB. It is recommended to use chunked upload for files exceeding 50 MB. |
| Conflict Resolution Strategy | Indicates what should happen when a file with the same name already exists in the specified Box folder. |
| Create Subfolder | Specifies whether to check if the subfolder exists and to automatically create it if it does not. Permission to list folders is required. |
| Filename | The name of the file to upload to the specified Box folder. |
| Folder ID | The ID of the folder where the file is uploaded. Please see Additional Details to obtain Folder ID. |
| Subfolder Name | The name (path) of the subfolder where files are uploaded. The subfolder name is relative to the folder specified by ‘Folder ID’. Example: subFolder, subFolder1/subfolder2 |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Files that could not be written to Box for some reason are transferred to this relationship. |
| success | Files that have been successfully written to Box are transferred to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.id | The id of the file |
| filename | The name of the file |
| path | The folder path where the file is located |
| box.size | The size of the file |
| box.timestamp | The last modified time of the file |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
