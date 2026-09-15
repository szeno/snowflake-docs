# FetchDropbox 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-dropbox-processors-nar

## Description

Fetches files from Dropbox. Designed to be used in tandem with ListDropbox.

## Tags

dropbox, fetch, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Dropbox Credential Service | Controller Service used to obtain Dropbox credentials (App Key, App Secret, Access Token, Refresh Token). See controller service’s Additional Details for more information. |
| File | The Dropbox identifier or path of the Dropbox file to fetch. The ‘File’should match the following regular expression pattern: /.*|id:.* . When ListDropbox is used for input, either ‘${dropbox.id}’ (identifying files by Dropbox id) or ‘${path}/${filename}’ (identifying files by path) can be used as ‘File’ value. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

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

- [org.apache.nifi.processors.dropbox.ListDropbox](/user-guide/data-integration/openflow/processors/listdropbox)
- [org.apache.nifi.processors.dropbox.PutDropbox](/user-guide/data-integration/openflow/processors/putdropbox)
