# FetchBoxFileInfo 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Fetches metadata for files from Box and adds it to the FlowFile’s attributes.

## Tags

box, fetch, metadata, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| File ID | The ID of the File to fetch metadata for |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile will be routed here if fetching the file metadata fails. |
| not.found | FlowFiles for which the specified Box file was not found. |
| success | A FlowFile will be routed here after successfully fetching the file metadata. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.id | The id of the file |
| filename | The name of the file |
| path | The folder path where the file is located |
| box.path.folder.ids | A comma separated list of file path\_collection IDs |
| box.size | The size of the file |
| box.timestamp | The last modified time of the file |
| box.created.at | The creation date of the file |
| box.owner | The name of the file owner |
| box.owner.id | The ID of the file owner |
| box.owner.login | The login of the file owner |
| box.description | The description of the file |
| box.etag | The etag of the file |
| box.sha1 | The SHA-1 hash of the file |
| box.content.created.at | The date the content was created |
| box.content.modified.at | The date the content was modified |
| box.item.status | The status of the file (active, trashed, etc.) |
| box.sequence\_id | The sequence ID of the file |
| box.parent.folder.id | The ID of the parent folder |
| box.trashed.at | The date the file was trashed, if applicable |
| box.purged.at | The date the file was purged, if applicable |
| box.shared.link | The shared link of the file, if any |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
- [org.apache.nifi.processors.box.PutBoxFile](/user-guide/data-integration/openflow/processors/putboxfile)
