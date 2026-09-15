# GetBoxGroupMembers 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Retrieves members for a Box Group and writes their details in FlowFile attributes.

## Tags

box, metadata, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| Group ID | The ID of the Group to retrieve members for |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The FlowFile will be routed here when Group memberships retrieval was attempted but failed. |
| not.found | The FlowFile will be routed here when the Group was not found. |
| success | The FlowFile will be routed here after successfully retrieving Group members. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.group.user.ids | A comma-separated list of user IDs in the group. |
| box.group.user.logins | A comma-separated list of user Logins (emails) in the group. |
| error.code | An http error code returned by Box. |
| error.message | An error message returned by Box. |

Expand

Show lessSee more
