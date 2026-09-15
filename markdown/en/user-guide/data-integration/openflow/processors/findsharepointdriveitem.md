# FindSharepointDriveItem 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

Finds a Sharepoint Drive Item by its Drive ID and Item path.

## Tags

document, graph, microsoft, openflow, sharepoint, unstructured

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API. |
| Drive ID | The ID of the Sharepoint Drive. |
| Fallback Retry Duration | The time to wait before retrying the operation after a communication failure. This value is used when the response doesn’t contain a Retry-After header. |
| Item Path | The path of the Drive Item to find in a Drive. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed here if the processor failed to communicate with the Graph API. Can be retried |
| failure | An incoming FlowFile is routed to this relationship if an unexpected error has occurred |
| found | An incoming FlowFile is routed to this relationship, with attributes about the Item added, if the specified item was found in Sharepoint |
| not.found | An incoming FlowFile is routed to this relationship if the specified item was not found in Sharepoint |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sharepoint.item.id | The ID of the Sharepoint Drive Item. |
| sharepoint.item.type | The type of the Sharepoint Drive Item, possible values are ‘File’ and ‘Folder’. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.sharepoint.FetchSharepointFile](/user-guide/data-integration/openflow/processors/fetchsharepointfile)
- [com.snowflake.openflow.runtime.processors.sharepoint.ListSharepointDrives](/user-guide/data-integration/openflow/processors/listsharepointdrives)
