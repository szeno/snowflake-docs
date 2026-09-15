# ListDBFSDirectory 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-databricks-processors-nar

## Description

List file names in a DBFS directory and output a new FlowFile with the filename.

## Tags

databricks, dbfs, openflow

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| DBFS File Path | DBFS file path e.g. /directory/file.txt |
| Databricks Client | Databricks Client Service. |
| Include Directories | Include directories in FlowFiles produced. |
| Recursive Directory Listing | Recursively list files in sub directories. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Databricks failure relationship |
| original | The original FlowFile is routed to this relationship when processing is successful. |
| success | Databricks success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | Base filename of the DBFS file or directory. |
| path | Path to parent directory containing the DBFS file or directory. |
| absolute.path | Full path to the DBFS file or directory. |
| dbfs.resourceType | The type of resource, ‘file’ or ‘directory’ of the DBFS resource. |
| dbfs.size | The size of the DBFS file. |
| dbfs.lastModifiedTime | The last modified time of the DBFS file, in milliseconds since epoch in UTC time. |
| error.code | The error code for the SQL statement if an error occurred. |
| error.message | The error message for the SQL statement if an error occurred. |

Expand

Show lessSee more
