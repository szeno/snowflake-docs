# CreateBoxMetadataTemplate 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Creates a Box metadata template using field specifications from the flowFile content. Expects a schema with fields: “ ‘type’ (required), ‘key’ (required), ‘displayName’ (optional), ‘description’ (optional), ‘hidden’ (optional, boolean).

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
| Hidden | Whether the template should be hidden in the Box UI. |
| Record Reader | The Record Reader to use for parsing the incoming data |
| Template Key | The key of the metadata template to create (used for API calls). |
| Template Name | The display name of the metadata template to create. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if an error occurs during template creation. |
| success | A FlowFile is routed to this relationship after a template has been successfully created. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.template.name | The template name that was created |
| box.template.key | The template key that was created |
| box.template.scope | The template scope. |
| box.template.fields.count | Number of fields created for the template |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.ListBoxFileMetadataTemplates](/user-guide/data-integration/openflow/processors/listboxfilemetadatatemplates)
- [org.apache.nifi.processors.box.UpdateBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/updateboxfilemetadatainstance)
