# ExtractStructuredBoxFileMetadata 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Extracts metadata from a Box file using Box AI. The extraction can use either a template or a list of fields. The extracted metadata is written to the FlowFile content as JSON.

## Tags

ai, box, extract, metadata, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| Extraction Method | The method to use for extracting metadata. TEMPLATE uses a Box metadata template for extraction. FIELDS uses a JSON schema of fields (read from FlowFile content) for extraction. |
| File ID | The ID of the file from which to extract metadata. |
| Record Reader | The Record Reader to use for parsing the incoming data. Required when Extraction Method is FIELDS. |
| Template Key | The key of the metadata template to use for extraction. Required when Extraction Method is TEMPLATE. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if an error occurs during metadata extraction. |
| file not found | FlowFiles for which the specified Box file was not found will be routed to this relationship. |
| success | A FlowFile is routed to this relationship after metadata has been successfully extracted. |
| template not found | FlowFiles for which the specified metadata template was not found will be routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.id | The ID of the file from which metadata was extracted |
| box.ai.template.key | The template key used for extraction (when using TEMPLATE extraction method) |
| box.ai.extraction.method | The extraction method used (TEMPLATE or FIELDS) |
| box.ai.completion.reason | The completion reason from the AI extraction |
| mime.type | Set to ‘application/json’ for the JSON content |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
- [org.apache.nifi.processors.box.ListBoxFileMetadataTemplates](/user-guide/data-integration/openflow/processors/listboxfilemetadatatemplates)
- [org.apache.nifi.processors.box.UpdateBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/updateboxfilemetadatainstance)
