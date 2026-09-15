# GetSharepointSiteGroupMembers 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-sharepoint-rest-nar

## Description

Retrieves all members of a SharePoint site group.

## Tags

groups, membership, microsoft, openflow, sharepoint

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Group ID | The ID of the SharePoint group. |
| OAuth2 Access Token Provider | Enables managed retrieval of OAuth2 Bearer Token. |
| Site URL | The URL of the SharePoint site. |
| Web Client Service | The Web Client Service to use for communicating with SharePoint. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed here if the processor failed to communicate with SharePoint. Can be retried |
| failure | A FlowFile is routed here if the group members could not be fetched |
| success | A FlowFile is routed here if the group members were successfully retrieved |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sharepoint.group.user.ids | The IDs of the users in the SharePoint site group. |
| sharepoint.group.user.emails | The emails of the users in the SharePoint site group. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.sharepoint.rest.ListSharepointSiteGroups](/user-guide/data-integration/openflow/processors/listsharepointsitegroups)
