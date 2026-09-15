# FetchFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Reads the contents of a file from disk and streams it into the contents of an incoming FlowFile. Once this is done, the file is optionally moved elsewhere or deleted to help keep the file system organized.

## Tags

fetch, files, filesystem, get, ingest, ingress, input, local, source

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Completion Strategy | Specifies what to do with the original file on the file system once it has been pulled into NiFi |
| File to Fetch | The fully-qualified filename of the file to fetch from the file system |
| Log level when file not found | Log level to use in case the file does not exist when the processor is triggered |
| Log level when permission denied | Log level to use if the current application user does not have sufficient permissions to read the file |
| Move Conflict Strategy | If Completion Strategy is set to Move File and a file already exists in the destination directory with the same name, this property specifies how that naming conflict should be resolved |
| Move Destination Directory | The directory to the move the original file to once it has been fetched from the file system. This property is ignored unless the Completion Strategy is set to “Move File”. If the directory does not exist, it will be created. |

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
| failure | Any FlowFile that could not be fetched from the file system for any reason other than insufficient permissions or the file not existing will be transferred to this Relationship. |
| not.found | Any FlowFile that could not be fetched from the file system because the file could not be found will be transferred to this Relationship. |
| permission.denied | Any FlowFile that could not be fetched from the file system due to the user running NiFi not having sufficient permissions will be transferred to this Relationship. |
| success | Any FlowFile that is successfully fetched from the file system will be transferred to this Relationship. |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Ingest all files from a directory into NiFi |
| --- |
| Ingest specific files from a directory into NiFi, filtering on filename |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.GetFile](/user-guide/data-integration/openflow/processors/getfile)
- [org.apache.nifi.processors.standard.ListFile](/user-guide/data-integration/openflow/processors/listfile)
- [org.apache.nifi.processors.standard.PutFile](/user-guide/data-integration/openflow/processors/putfile)
