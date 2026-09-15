# ConvertToJournalSchema 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Converts the incoming database schema into the appropriate schema for a Snowflake CDC Journal table.

## Tags

Snowflake, cdc, journal

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to this relationship if the schema cannot be translated. |
| original | The original FlowFile is routed to this relationship when the schema is successfully converted. |
| success | FlowFiles are routed to this relationship after the schema has been converted. |

Expand

Show lessSee more
