# SnowflakeDetectDuplicate 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Checks if a FlowFile ‘s hash (provided as a FlowFile attribute) is already in a Snowflake table, and routes the FlowFile to’ duplicate ‘if found,’distinct ‘if not found, or’ failure’ on errors.

## Tags

database, detect, duplicates, hash, snowflake

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Content Hash | The name of the FlowFile attribute that holds the pre-computed hash. Supports Expression Language. |
| Document Source Identifier | Specifies the document source identifier (doc ID). Supports Expression Language. |
| Document Source Name | Specifies the document source system name. Supports Expression Language. |
| Snowflake Connection Service | The DBCPService that provides connection to Snowflake. |
| Snowflake Table Name | The Snowflake table name that stores the file hashes. The table name is case-insensitive. Database and schema must be configured prior in the Snowflake Connection Service. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| distinct | FlowFiles that do not match an existing document are routed here (new hash inserted). |
| duplicate | FlowFiles that match an existing document (same hash) are routed here. |
| failure | FlowFiles that encounter an error or exception during processing are routed here. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| snowflake.detect.duplicate | A ‘true’ or ‘false’ attribute indicating if the FlowFile was detected as a duplicate. |

Expand

Show lessSee more
