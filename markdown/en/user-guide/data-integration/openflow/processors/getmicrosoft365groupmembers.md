# GetMicrosoft365GroupMembers 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

Retrieves Microsoft365 group members and emits a FlowFile for each change that occurs. This includes membership changes.

## Tags

cdc, document, graph, library, microsoft, sharepoint, unstructured

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API |
| Fallback Retry Duration | The time to wait before retrying the operation after a communication failure. This value is used when the response doesn’t contain a Retry-After header. |
| Microsoft365 Group id | Specifies a Microsoft365 group id to retrieve the members for. Supports Expression Language. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed here if the processor failed to communicate with the Graph API. Can be retried |
| failure | An incoming FlowFile is routed to this relationship if the group members could not be fetched |
| not.found | A FlowFile is routed here if the group was not found |
| success | A FlowFile is routed here if the group members were successfully retrieved |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| microsoft365.group.user.ids | A comma-separated list of Microsoft365 user ids that are members of the Microsoft365 group. |
| microsoft365.group.user.emails | A comma-separated list of user emails that are members of the Microsoft365 group. |

Expand

Show lessSee more
