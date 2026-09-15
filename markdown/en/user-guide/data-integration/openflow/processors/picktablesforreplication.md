# PickTablesForReplication 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Accepts a list of fully qualified table names and determines if a table: - is new (is not replicated, but was added in the source) - is existing (is replicated and exists in the source) - is stale (is replicated but no longer exists in the source) Configuration is passed as a FlowFile attribute. Processor generates a separate FlowFile for each source table.

## Tags

snowflake, state, table

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Table State Service | A service containing currently replicated tables and their states |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| existing | FlowFile with qualified table name that is already being replicated |
| failure | If a FlowFile attribute cannot be read or is incorrect, it will be routed to this Relationship. |
| new | FlowFile with qualified table name that was is not replicated |
| stale | FlowFile with qualified table name that used to be replicated but no longer is, either because it was removed from source database or excluded by parameter |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| source.schema.name | Name of the schema of the table from which an event originated |
| source.table.name | Name of the table from which an event originated |

Expand

Show lessSee more
