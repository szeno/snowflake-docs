# PutDropbox 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-dropbox-processors-nar

## Description

Puts content to a Dropbox folder.

## Tags

dropbox, put, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Chunked Upload Size | Defines the size of a chunk. Used when a FlowFile ‘s size exceeds’Chunked Upload Threshold ‘and content is uploaded in smaller chunks. It is recommended to specify chunked upload size smaller than’Chunked Upload Threshold’ and as multiples of 4 MB. Maximum allowed value is 150 MB. |
| Chunked Upload Threshold | The maximum size of the content which is uploaded at once. FlowFiles larger than this threshold are uploaded in chunks. Maximum allowed value is 150 MB. |
| Conflict Resolution Strategy | Indicates what should happen when a file with the same name already exists in the specified Dropbox folder. |
| Dropbox Credential Service | Controller Service used to obtain Dropbox credentials (App Key, App Secret, Access Token, Refresh Token). See controller service’s Additional Details for more information. |
| Filename | The full name of the file to upload. |
| Folder | The path of the Dropbox folder to upload files to. The folder will be created if it does not exist yet. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Files that could not be written to Dropbox for some reason are transferred to this relationship. |
| success | Files that have been successfully written to Dropbox are transferred to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| error.message | The error message returned by Dropbox |
| dropbox.id | The Dropbox identifier of the file |
| path | The folder path where the file is located |
| filename | The name of the file |
| dropbox.size | The size of the file |
| dropbox.timestamp | The server modified time of the file |
| dropbox.revision | Revision of the file |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.dropbox.FetchDropbox](/user-guide/data-integration/openflow/processors/fetchdropbox)
- [org.apache.nifi.processors.dropbox.ListDropbox](/user-guide/data-integration/openflow/processors/listdropbox)
