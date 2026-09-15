# CaptureGoogleDriveChanges 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-drive-nar

## Description

Captures changes to a Shared Google Drive and emits a FlowFile for each change that occurs. This includes addition and deletion of files, as well as changes to file metadata and permissions. The processor is designed to be used in conjunction with the FetchGoogleDrive processor.

## Tags

authorization, cdc, change data capture, cloud, drive, gcp, google, openflow, permissions, storage, unstructured

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Drive ID | The ID of the Shared Google Drive to monitor. |
| GCP Credentials Service | The Controller Service used to obtain Google Cloud Platform credentials. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores a token/cursor to track which changes have already been processed. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| created | This Relationship is used for any files that are created. |
| removed | This Relationship is used for any files that are deleted. |
| updated | This Relationship is used for any files that are updated. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| google.drive.drive.id | The ID of the Shared Google Drive. |
| google.drive.file.id | The ID of the file that was changed. |
| drive.id | The ID of the file that was changed. This is repeated for compatibility with FetchGoogleDrive’s default configuration. |
| google.drive.file.name | The name of the file that was changed. |
| google.drive.change.type | The type of change that occurred. Possible values are ‘CREATED’, ‘UPDATED’, or ‘DELETED’. |
| google.drive.change.time | The timestamp of the change, in milliseconds since the Unix epoch. |
| google.drive.created.time | The timestamp when the file was created, in milliseconds since the Unix epoch. |
| google.drive.webUrl | A link for opening the file in a relevant Google editor or viewer in a browser. |
| google.drive.size | The size of the file in bytes. |
| google.drive.md5 | The MD5 checksum of the file. |
| google.drive.version | The version of the file. This changes based on user and system based updates to the file. |
| google.drive.mime.type | The MIME type of the file. |
| google.drive.lastModifiedBy.displayName | A display name of the user that modified the file. |
| google.drive.lastModifiedBy.email | An email of the user that modified the file. |
| google.drive.permissions.<role>.users | A comma-separated list of email addresses for users with the specified role. Valid roles are ‘owner’, ‘organizer’, ‘fileOrganizer’, ‘writer’, ‘commenter’, ‘reader’. For example, if the owner is [john.doe@gmail.com](mailto:john.doe@gmail.com) and users [jane.doe@gmail.com](mailto:jane.doe@gmail.com) and [jake.doe@gmail.com](mailto:jake.doe@gmail.com) are readers, there would be an attribute named *google.drive.permissions.owner.users* with the value *[john.doe@gmail.com](mailto:john.doe@gmail.com)*, and an attribute named *google.drive.permissions.reader.users* with the value [\_jane.doe@gmail.com](mailto:_jane.doe@gmail.com), jake.doe@gmail.com\_ |
| google.drive.permissions.<role>.groups | A comma-separated list of email addresses for groups with the specified role. Valid roles are ‘owner’, ‘organizer’, ‘fileOrganizer’, ‘writer’, ‘commenter’, ‘reader’. For example, if the owner is *[employees@openflow-all-dev.iam.gserviceaccount.com](mailto:employees@openflow-all-dev.iam.gserviceaccount.com)* and the group *[contractors@openflow-all-dev.iam.gserviceaccount.com](mailto:contractors@openflow-all-dev.iam.gserviceaccount.com)* is a reader, there would be an attribute named *google.drive.permissions.owner.groups* with the value *[employees@openflow-all-dev.iam.gserviceaccount.com](mailto:employees@openflow-all-dev.iam.gserviceaccount.com)*, and an attribute named *google.drive.permissions.reader.groups* with the value *[contractors@openflow-all-dev.iam.gserviceaccount.com](mailto:contractors@openflow-all-dev.iam.gserviceaccount.com)* |
| google.drive.permissions.<role>.domains | A comma-separated list of domain names for which all users have the given role. Valid roles are ‘owner’, ‘organizer’, ‘fileOrganizer’, ‘writer’, ‘commenter’, ‘reader’. For example, if all users in the domain *snowflake.com* have the role of reader, there would be an attribute named *google.drive.permissions.reader.domains* with the value *snowflake.com* |
| google.drive.permissions.<role>.public | If a file is shared publicly, this attribute will be added with a value of ‘true’ for any role that applies to the public. |
| google.drive.file.path | The hierarchical path of the file in Google Drive, e.g. ‘parent\_folder/child\_folder/file.txt’. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.sharepoint.CaptureSharepointChanges](/user-guide/data-integration/openflow/processors/capturesharepointchanges)
- [org.apache.nifi.processors.gcp.drive.FetchGoogleDrive](/user-guide/data-integration/openflow/processors/fetchgoogledrive)
