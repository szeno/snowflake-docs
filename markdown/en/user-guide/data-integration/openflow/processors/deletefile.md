# DeleteFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Deletes a file from the filesystem.

## Tags

delete, file, files, filesystem, local, remove

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Directory Path | The path to the directory the file to delete is located in. |
| Filename | The name of the file to delete. |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |
| write filesystem | Provides operator the ability to delete any file that NiFi has access to. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles, for which an existing file could not be deleted, are routed to this relationship |
| not found | All FlowFiles, for which the file to delete did not exist, are routed to this relationship |
| success | All FlowFiles, for which an existing file has been deleted, are routed to this relationship |

Expand

Show lessSee more

## Use cases

| Delete source file only after its processing completed |
| --- |

Expand

Show lessSee more
