# CreateBoxFileMetadataInstance 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Creates a metadata instance for a Box file using a specified template with values from the flowFile content. The Box API requires newly created templates to be created with the scope set as enterprise so no scope is required. The input record should be a flat key-value object where each field name is used as the metadata key.

## Tags

box, create, metadata, storage, templates

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| File ID | The ID of the file for which to create metadata. |
| Record Reader | The Record Reader to use for parsing the incoming data |
| Template Key | The key of the metadata template to use for creation. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if an error occurs during metadata creation. |
| file not found | FlowFiles for which the specified Box file was not found will be routed to this relationship. |
| success | A FlowFile is routed to this relationship after metadata has been successfully created. |
| template not found | FlowFiles for which the specified metadata template was not found will be routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.id | The ID of the file for which metadata was created |
| box.template.key | The template key used for metadata creation |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
- [org.apache.nifi.processors.box.ListBoxFileMetadataTemplates](/user-guide/data-integration/openflow/processors/listboxfilemetadatatemplates)
- [org.apache.nifi.processors.box.UpdateBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/updateboxfilemetadatainstance)
