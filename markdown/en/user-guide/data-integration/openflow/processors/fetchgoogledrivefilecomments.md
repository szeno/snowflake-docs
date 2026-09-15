# FetchGoogleDriveFileComments 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-drive-nar

## Description

Fetches comments and their replies for a Google Drive file. The file ID can be set by a FlowFile attribute. Records include comment metadata such as deleted status, resolved status, anchors, and a nested array of replies.

## Tags

comments, drive, gcp, google, openflow, replies

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| File ID | Google Drive file ID. |
| GCP Credentials Service | Controller Service used to obtain Google Cloud Platform credentials. |
| Record Writer | Specifies the Record Writer to use when writing the comments. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed here if the processor fails to retrieve comments. |
| not.found | A FlowFile is routed here if the file was not found. |
| retry | FlowFiles are routed here if a connection or rate-limit issue occurs. |
| success | All FlowFiles that are successfully processed are routed here. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | Number of comment records returned (not including replies). |
| google.drive.file.id | The file ID from which comments were fetched. |

Expand

Show lessSee more
