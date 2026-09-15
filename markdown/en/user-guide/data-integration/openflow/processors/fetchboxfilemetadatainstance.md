# FetchBoxFileMetadataInstance 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Retrieves specific metadata instance associated with a Box file using template key and scope.

## Tags

box, instance, metadata, storage, template

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| File ID | The ID of the file for which to fetch metadata. |
| Template Key | The metadata template key to retrieve. |
| Template Scope | The metadata template scope (e.g., ‘enterprise’, ‘global’). |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile will be routed here if there is an error fetching metadata instance from the file. |
| file not found | FlowFiles for which the specified Box file was not found will be routed to this relationship. |
| success | A FlowFile containing the metadata instance will be routed to this relationship upon successful processing. |
| template not found | FlowFiles for which the specified metadata template was not found will be routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.id | The ID of the file from which metadata was fetched |
| box.metadata.template.key | The metadata template key |
| box.metadata.template.scope | The metadata template scope |
| mime.type | The MIME Type of the FlowFile content |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.FetchBoxFileInfo](/user-guide/data-integration/openflow/processors/fetchboxfileinfo)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
- [org.apache.nifi.processors.box.ListBoxFileMetadataInstances](/user-guide/data-integration/openflow/processors/listboxfilemetadatainstances)
