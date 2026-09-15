# FetchMicrosoftDataverseTable 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-dataverse-processors-nar

## Description

Fetch records from Microsoft Dataverse Tables

## Tags

dataverse

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Delete Schema |  |
| Environment URL | URL to Microsoft Dataverse Environment |
| Logical Name | Logical Name of Dataverse Table |
| Max Page Size | Defines how many records will be fetched from Dataverse at once |
| OAuth2 Access Token Provider | Enables managed retrieval of OAuth2 Bearer Token. |
| Record Writer | Specifies the Controller Service to use for writing out the records |
| Rows Number Limit | Defines maximum number of rows returned in a single flow file. Multiple request will be made to API to reach the limit. When not set, a page size value will be used effectively. |
| Table Name | Dataverse Table Name |
| Upsert Schema |  |
| Web Client Service Provider | Creates instance of web client. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | status |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFile with errors occurred while fetching from Dataverse. |
| retry | FlowFile with maintainable errors occurred while fetching from Dataverse. |
| success | FlowFile with fetched data stored as records. |

Expand

Show lessSee more
