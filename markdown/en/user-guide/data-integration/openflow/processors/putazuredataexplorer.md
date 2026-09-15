# PutAzureDataExplorer 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Acts as an Azure Data Explorer sink which sends FlowFiles to the provided endpoint. Data can be sent through queued ingestion or streaming ingestion to the Azure Data Explorer cluster.

## Tags

ADX, Azure, Data, Explorer, Kusto

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Data Format | The format of the data that is sent to Azure Data Explorer. Supported formats include: avro, csv, json |
| Database Name | Azure Data Explorer Database Name for ingesting data |
| Ingest Mapping Name | The name of the mapping responsible for storing the data in the appropriate columns. |
| Ingest Status Polling Interval | Defines the value of interval of time to poll for ingestion status |
| Ingest Status Polling Timeout | Defines the total amount time to poll for ingestion status |
| Ingestion Ignore First Record | Defines whether ignore first record while ingestion. |
| Kusto Ingest Service | Azure Data Explorer Kusto Ingest Service |
| Partially Succeeded Routing Strategy | Defines where to route FlowFiles that resulted in a partially succeeded status. |
| Poll for Ingest Status | Determines whether to poll on ingestion status after an ingestion to Azure Data Explorer is completed |
| Streaming Enabled | Whether to stream data to Azure Data Explorer. |
| Table Name | Azure Data Explorer Table Name for ingesting data |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Ingest processing failed |
| success | Ingest processing succeeded |

Expand

Show lessSee more
