# CaptureSharepointChanges 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

Captures changes from a Sharepoint Document Library and emits a FlowFile for each change that occurs. This includes additions and deletions of files and folders, as well as changes to permissions, metadata, and file content.

## Tags

cdc, document, graph, library, microsoft, openflow, sharepoint, unstructured

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API |
| Change Capture Initial Action | If the Processor is run without having any prior state, this property dictates how the Processor should treat existing Sharepoint items. |
| Document Library Name | The name of the Document Library to list. If not specified, all Document Libraries associated with the Site will be listed. |
| Fallback Retry Duration | The time to wait before retrying the operation after a communication failure. This value is used when the response doesn’t contain a Retry-After header. |
| Fetch Item Permissions | If true, the Processor will fetch user and group permission information for the captured Sharepoint item. |
| Folder Name | The name of the Folder/Directory to list |
| Item Permissions To Fetch | A comma-separated list of permission types to fetch for the captured Sharepoint item. Available permission types: USER, GROUP, SITE\_USER, SITE\_GROUP. |
| Site URL | The URL of the Sharepoint Site that data will be retrieved from. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores tokens for each Sharepoint folder to track state about which events have already been captured. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| created | A FlowFile is routed to this relationship for each Sharepoint item that is created. |
| deleted | A FlowFile is routed to this relationship for each Sharepoint item that is deleted. |
| updated | A FlowFile is routed to this relationship for each Sharepoint item that is updated. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sharepoint.change.type | The type of change that occurred. Possible values are ‘Created’, ‘Updated’, ‘PermissionsUpdated’, ‘Deleted’. |
| sharepoint.item.id | The ID of the Sharepoint item that was changed. |
| sharepoint.item.type | The type of the Sharepoint item that was changed. Possible values are ‘File’ and ‘Folder’. |
| sharepoint.path | The path of the Sharepoint item that was changed. This is the path relative to the root of the Document Library. |
| sharepoint.filename | The name of the Sharepoint item that was changed. This attribute is not available for ‘Deleted’ changes. |
| sharepoint.size | The size of the Sharepoint item that was changed. |
| sharepoint.createdAt | The creation timestamp of the Sharepoint item that was changed. |
| sharepoint.lastModified | The last modified timestamp of the Sharepoint item that was changed. |
| sharepoint.createdBy.<identity>.id | An id of the identity that created the Sharepoint item that was changed. This attribute is not always available. |
| sharepoint.createdBy.<identity>.displayName | A display name of the identity that created the Sharepoint item that was changed. This attribute is not always available. |
| sharepoint.createdBy.<identity>.email | An email of the identity that created the Sharepoint item that was changed. This attribute is not always available. |
| sharepoint.lastModifiedBy.<identity>.id | An id of the identity that modified the Sharepoint item that was changed. This attribute is not always available. |
| sharepoint.lastModifiedBy.<identity>.displayName | A display name of the identity that modified the Sharepoint item that was changed. This attribute is not always available. |
| sharepoint.lastModifiedBy.<identity>.email | An email of the identity that modified the Sharepoint item that was changed. This attribute is not always available. |
| sharepoint.drive.id | The ID of the Sharepoint Drive that contains the item that was changed. |
| sharepoint.drive.name | The name of the Sharepoint Drive that contains the item that was changed. |
| sharepoint.site.id | The ID of the Sharepoint Site that contains the item that was changed. |
| sharepoint.site.url | The URL of the Sharepoint Site that contains the item that was changed. |
| sharepoint.ctag | The CTag of the Sharepoint item that was changed. |
| sharepoint.etag | The ETag of the Sharepoint item that was changed. |
| sharepoint.webUrl | The browser view url of the Sharepoint item that was changed. |
| sharepoint.permissions.read.groups | A comma-separated list of groups that have read permissions on the Sharepoint item that was changed. For each group, if an e-mail address is available in Sharepoint, it will be included. Additionally, the group principal, such as *[mygroup@mytenant.onmicrosoft.com](mailto:mygroup@mytenant.onmicrosoft.com)*, is included. |
| sharepoint.permissions.read.groups.ids | A comma-separated list of group IDs that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.users | A comma-separated list of users that have read permissions on the Sharepoint item that was changed. For each user, if an e-mail address is available in Sharepoint, it will be included. Additionally, the user principal, such as *[johndoe@mytenant.onmicrosoft.com](mailto:johndoe@mytenant.onmicrosoft.com)*, is included. |
| sharepoint.permissions.read.users.ids | A comma-separated list of Microsoft365 user IDs that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.siteusers | A comma-separated list of Sharepoint site user emails that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.siteusers.ids | A comma-separated list of Sharepoint site user IDs that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.sitegroups.ids | A comma-separated list of Sharepoint site group IDs that have read permissions on the Sharepoint item. |
| filename | The name of the Sharepoint item that was changed. This attribute is not available for ‘Deleted’ changes. |
| path | The path of the Sharepoint item that was changed. This is the path relative to the root of the Document Library. |
| mime.type | The MIME type of the Sharepoint item that was changed. This attribute is only available for ‘File’ items. |
| hash.quickxor | The QuickXor hash of the Sharepoint item that was changed. This attribute is not always available. |
| hash.sha256 | The SHA-256 hash of the Sharepoint item that was changed. This attribute is not always available. |
| hash.sha1 | The SHA-1 hash of the Sharepoint item that was changed. This attribute is not always available. |
| hash.crc32 | The CRC32 hash of the Sharepoint item that was changed. This attribute is not always available. |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Perform Change Data Capture on a Sharepoint Document Library, retrieving all data in the Document Library, including permissions, in order to keep a destination system in sync with Sharepoint. |
| --- |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.sharepoint.FetchSharepointFile](/user-guide/data-integration/openflow/processors/fetchsharepointfile)
