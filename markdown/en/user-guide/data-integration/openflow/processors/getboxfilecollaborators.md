# GetBoxFileCollaborators 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-box-nar

## Description

Retrieves all collaborators on a Box file and adds the collaboration information to the FlowFile’s attributes.

## Tags

box, collaboration, permissions, sharing, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Box Client Service | Controller Service used to obtain a Box API connection. |
| File ID | The ID of the Box file to retrieve collaborators for |
| Roles | A comma-separated list of collaboration roles to retrieve. Available roles: editor, viewer, previewer, uploader, previewer uploader, viewer uploader, co-owner, owner. If not specified, no filtering by role will be applied. |
| Statuses | A comma-separated list of collaboration statuses to retrieve. Available statuses: accepted, pending, rejected. If not specified, no filtering by status will be applied. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that encounter errors during processing will be routed to this relationship |
| not.found | FlowFiles for which the specified Box file was not found |
| success | FlowFiles that have been successfully processed will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| box.id | The id of the file |
| box.collaborations.<status>.users.ids | Comma-separated list of user collaborator IDs by status |
| box.collaborations.<status>.groups.ids | Comma-separated list of group collaborator IDs by status |
| box.collaborations.<status>.users.emails | Comma-separated list of user collaborator emails by status |
| box.collaborations.<status>.groups.emails | Comma-separated list of group collaborator emails by status |
| box.collaborations.<status>.<role>.users.ids | Comma-separated list of user collaborator IDs by status and role. Only present when both Roles and Statuses properties are set. |
| box.collaborations.<status>.<role>.users.logins | Comma-separated list of user collaborator logins by status and role. Only present when both Roles and Statuses properties are set. |
| box.collaborations.<status>.<role>.groups.ids | Comma-separated list of group collaborator IDs by status and role. Only present when both Roles and Statuses properties are set. |
| box.collaborations.<status>.<role>.groups.emails | Comma-separated list of group collaborator emails by status and role. Only present when both Roles and Statuses properties are set. |
| box.collaborations.count | Total number of collaborations on the file |
| error.code | The error code returned by Box |
| error.message | The error message returned by Box |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.box.FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile)
- [org.apache.nifi.processors.box.ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile)
