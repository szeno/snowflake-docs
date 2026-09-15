# GetUnityCatalogFileMetadata 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-databricks-processors-nar

## Description

Checks for Unity Catalog file metadata.

## Tags

databricks, openflow, unity catalog

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Databricks Client | Databricks Client Service. |
| Unity Catalog File Path | Unity Catalog file path e.g. /Volumes/catalog/schema/volume\_name/file.txt |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Databricks failure relationship |
| not.found | The original FlowFile is transferred to this relationship if no Unity Catalog can be found at the specified path |
| success | Databricks success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The content type of the checked file. |
| uc.size | The size of the Unity Catalog file. |
| uc.lastModifiedTime | The last modified time of the Unity Catalog file in milliseconds since epoch in UTC time. |
| error.code | The error code for the SQL statement if an error occurred. |
| error.message | The error message for the SQL statement if an error occurred. |

Expand

Show lessSee more
