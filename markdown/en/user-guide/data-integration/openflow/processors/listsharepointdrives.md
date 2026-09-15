# ListSharepointDrives 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

Emits a FlowFile for each Drive present in the specified Sharepoint Site.

## Tags

document, graph, microsoft, openflow, sharepoint, unstructured

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API. |
| Site URL | The URL of the Sharepoint Site. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles for each Drive are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sharepoint.site.url | The URL of the Sharepoint Site. |
| sharepoint.site.id | The ID of the Sharepoint Site. |
| sharepoint.drive.name | The name of the Sharepoint Drive. |
| sharepoint.drive.id | The ID of the Sharepoint Drive. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.sharepoint.FetchSharepointFile](/user-guide/data-integration/openflow/processors/fetchsharepointfile)
- [com.snowflake.openflow.runtime.processors.sharepoint.FindSharepointDriveItem](/user-guide/data-integration/openflow/processors/findsharepointdriveitem)
