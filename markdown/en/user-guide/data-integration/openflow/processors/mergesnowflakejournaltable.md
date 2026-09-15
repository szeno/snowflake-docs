# MergeSnowflakeJournalTable 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Triggers a merge operation on changes from journal table to a destination table in Snowflake. The merge operation is performed asynchronously and the processor polls the result of the operation. If the query is still in progress the FlowFile will be penalized.

## Tags

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Destination Database Name | The name of the Snowflake database where the data is being ingested to. |
| Merge Query Retry Count | Indicates how many times the merge query should be retried if it fails. |
| Object Identifier Resolution | Controls how source object identifiers (schemas, tables, columns) are stored and queried in Snowflake. This setting determines whether you will need to use double quotes in your SQL queries. The ‘Case-Sensitive’ option is the default, production behavior — ‘Case-Insensitive’ is considered preview for the time being. |
| Placeholder Value | The value of the payload placeholder to look for in a MERGE. This will be converted to the destination column’s data type. |
| Snowflake Connection Pool | The Controller Service that is used to obtain a connection to the Snowflake database to perform merge operation. |
| Unchanged Value Strategy | Determines how the MERGE query should handle unchanged values in journal columns. By default it expects full values. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| ddl | DDL to execute. |
| deleted during compaction | FlowFile deleted during compaction based on table name and generation. |
| failure | Failure query execution. |
| failure retry | Retry failure query execution. |
| poll query result | Scheduled async query execution. |
| success | Success query execution. |
| unknown file type | Unknown file type. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| merge.query.id | The ID of the query that is used to merge the journal table into the target table. |

Expand

Show lessSee more
