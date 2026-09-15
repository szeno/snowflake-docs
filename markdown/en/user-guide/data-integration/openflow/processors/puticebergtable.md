# PutIcebergTable 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-iceberg-processors-nar

## Description

Store records in Iceberg using configurable Catalog for managing namespaces and tables.

## Tags

analytics, iceberg, openflow, parquet, polaris, s3

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Iceberg Catalog | Provider Service for Iceberg Catalog |
| Iceberg Writer | Provider Service for Iceberg Row Writers responsible for producing formatted Iceberg Data Files |
| Namespace | Iceberg Namespace containing Tables |
| Record Reader | Record Reader for incoming FlowFiles |
| Table Name | Iceberg Table Name |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles not transferred to Iceberg |
| success | FlowFiles transferred to Iceberg |

Expand

Show lessSee more
