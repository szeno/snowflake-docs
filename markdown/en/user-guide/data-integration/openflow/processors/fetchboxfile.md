# FetchBoxFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Fetches files from a Box Folder. Designed to be used in tandem with ListBoxFile.

## Tags

box, fetch, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| File ID | The ID of the File to fetch |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile will be routed here for each File for which fetch was attempted but failed. |
| success | A FlowFile will be routed here for each successfully fetched File. |

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

- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
- [org.apache.nifi.processors.box.PutBoxFile](/user-guide/data-integration/openflow/processors/putboxfile)
