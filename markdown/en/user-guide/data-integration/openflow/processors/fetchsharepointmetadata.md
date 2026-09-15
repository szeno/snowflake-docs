# FetchSharepointMetadata 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

For each drive item retrieves its metadata and permissions and writes them as FlowFile attributes.

## Tags

cdc, document, graph, library, microsoft, openflow, sharepoint, unstructured

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API |
| Drive ID | A drive id where the Sharepoint file resides |
| Fallback Retry Duration | The time to wait before retrying the operation after a communication failure. This value is used when the response doesn’t contain a Retry-After header. |
| Fetch Item Permissions | If true, the Processor will fetch user and group permission information for the captured Sharepoint item. |
| Item ID | An id of an item to retrieve the metadata for |
| Item Permissions To Fetch | A comma-separated list of permission types to fetch for the captured Sharepoint item. Available permission types: USER, GROUP, SITE\_USER, SITE\_GROUP. |
| Site ID | A site id where the Sharepoint file resides |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed here if the processor failed to communicate with the Graph API. Can be retried |
| failure | An incoming FlowFile is routed to this relationship if the metadata and permissions of the item could not be fetched |
| not.found | A FlowFile is routed here if the item was not found |
| success | An incoming FlowFile is routed to this relationship after the metadata and permissions of the item have been fetched and written to the FlowFile attributes |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sharepoint.item.id | The ID of the Sharepoint item. |
| sharepoint.item.type | The type of the Sharepoint item. Possible values are ‘File’ and ‘Folder’. |
| sharepoint.path | The path of the Sharepoint item. This is the path relative to the root of the Document Library. |
| sharepoint.filename | The name of the Sharepoint item. This attribute is not available for ‘Deleted’ changes. |
| sharepoint.size | The size of the Sharepoint item. |
| sharepoint.createdAt | The creation timestamp of the Sharepoint item. |
| sharepoint.lastModified | The last modified timestamp of the Sharepoint item. |
| sharepoint.createdBy.<identity>.id | An id of the identity that created the Sharepoint item. This attribute is not always available. |
| sharepoint.createdBy.<identity>.displayName | A display name of the identity that created the Sharepoint item. This attribute is not always available. |
| sharepoint.createdBy.<identity>.email | An email of the identity that created the Sharepoint item. This attribute is not always available. |
| sharepoint.lastModifiedBy.<identity>.id | An id of the identity that modified the Sharepoint item last. This attribute is not always available. |
| sharepoint.lastModifiedBy.<identity>.displayName | A display name of the identity that modified the Sharepoint item last. This attribute is not always available. |
| sharepoint.lastModifiedBy.<identity>.email | An email of the identity that modified the Sharepoint item last. This attribute is not always available. |
| sharepoint.drive.id | The ID of the Sharepoint Drive that contains the item. |
| sharepoint.site.id | The ID of the Sharepoint Site that contains the item. |
| sharepoint.ctag | The CTag of the Sharepoint item. |
| sharepoint.etag | The ETag of the Sharepoint item. |
| sharepoint.webUrl | The browser view url of the Sharepoint item. |
| sharepoint.permissions.read.groups | A comma-separated list of groups that have read permissions on the Sharepoint item. For each group, if an e-mail address is available in Sharepoint, it will be included. Additionally, the group principal, such as *[mygroup@mytenant.onmicrosoft.com](mailto:mygroup@mytenant.onmicrosoft.com)*, is included. |
| sharepoint.permissions.read.groups.ids | A comma-separated list of group IDs that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.users | A comma-separated list of users that have read permissions on the Sharepoint item. For each user, if an e-mail address is available in Sharepoint, it will be included. Additionally, the user principal, such as *[johndoe@mytenant.onmicrosoft.com](mailto:johndoe@mytenant.onmicrosoft.com)*, is included. |
| sharepoint.permissions.read.users.ids | A comma-separated list of Microsoft365 user IDs that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.siteusers | A comma-separated list of Sharepoint site user emails that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.siteusers.ids | A comma-separated list of Sharepoint site user IDs that have read permissions on the Sharepoint item. |
| sharepoint.permissions.read.sitegroups.ids | A comma-separated list of Sharepoint site group IDs that have read permissions on the Sharepoint item. |
| filename | The name of the Sharepoint item. |
| path | The path of the Sharepoint item. This is the path relative to the root of the Document Library. |
| mime.type | The MIME type of the Sharepoint item. This attribute is only available for ‘File’ items. |
| hash.quickxor | The QuickXor hash of the Sharepoint item. This attribute is not always available. |
| hash.sha256 | The SHA-256 hash of the Sharepoint item. This attribute is not always available. |
| hash.sha1 | The SHA-1 hash of the Sharepoint item. This attribute is not always available. |
| hash.crc32 | The CRC32 hash of the Sharepoint item. This attribute is not always available. |

Expand

Show lessSee more
