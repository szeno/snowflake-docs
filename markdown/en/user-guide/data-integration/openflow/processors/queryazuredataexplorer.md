# QueryAzureDataExplorer 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Query Azure Data Explorer and stream JSON results to output FlowFiles

## Tags

ADX, Azure, Data, Explorer, Kusto

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Database Name | Azure Data Explorer Database Name for querying |
| Kusto Query Service | Azure Data Explorer Kusto Query Service |
| Query | Query to be run against Azure Data Explorer |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles containing original input associated with a failed Query |
| success | FlowFiles containing results of a successful Query |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| query.error.message | Azure Data Explorer query error message on failures |
| query.executed | Azure Data Explorer query executed |
| mime.type | Content Type set to application/json |

Expand

Show lessSee more
