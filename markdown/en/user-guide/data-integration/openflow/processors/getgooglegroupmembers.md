# GetGoogleGroupMembers 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-drive-nar

## Description

Retrieves the members of one or more Google Groups, specified as a comma-separated list of group IDs that is given as a FlowFile attribute. Supports both immediate (top-level) and nested group member retrieval. Outputs four FlowFile attributes: ‘google.group.member.user.ids’, ‘google.group.member.user.emails’, ‘google.group.member.group.ids’, and ‘google.group.member.group.emails’. When nested fetching is enabled, it recursively expands sub-groups up to the specified depth. If an attribute already exists on the FlowFile, the new values are concatenated to the existing value (separated by a comma).

## Tags

cloud, directory, gcp, google, groups, membership

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Fetch Nested Groups | When enabled, recursively fetches members from nested groups within the specified groups. When disabled, only top-level members are retrieved. |
| GCP Credentials Service | Specifies the Controller Service used to obtain Google Cloud Platform credentials. |
| Google Group IDs | Specifies the comma-separated list of Google Group IDs (email addresses for the groups). Supports Expression Language. |
| Nested Depth Limit | Maximum depth to traverse when fetching nested group members. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed here if the processor fails to retrieve Google group members. |
| not.found | A FlowFile is routed here if for each Google group that was not found. |
| retry | A FlowFile is routed here if the processor should retry the request (e.g., after rate limiting). |
| success | A FlowFile is routed here after successfully retrieving Google group members. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| google.group.ids | A comma-separated list of Google Group IDs that were found. |
| google.group.member.user.ids | A comma-separated list of user IDs found in the specified groups. When nested fetching is enabled, includes users from nested groups up to the specified depth. |
| google.group.member.user.emails | A comma-separated list of user email addresses found in the specified groups. When nested fetching is enabled, includes users from nested groups up to the specified depth. |
| google.group.member.group.ids | A comma-separated list of nested group IDs found in the specified groups. When nested fetching is enabled, includes all groups discovered during recursive traversal. |
| google.group.member.group.emails | A comma-separated list of nested group email addresses found in the specified groups. When nested fetching is enabled, includes all groups discovered during recursive traversal. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.google.CaptureGoogleDriveChanges](/user-guide/data-integration/openflow/processors/capturegoogledrivechanges)
