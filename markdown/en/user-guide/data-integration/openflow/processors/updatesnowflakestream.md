# UpdateSnowflakeStream 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Manages Snowflake streams by creating, dropping, or replacing them based on the configured operation. Streams in Snowflake capture data change for tables and can be used to track DML changes over time.

## Tags

cdc, create, drop, preview, replace, snowflake, stream, table

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Pool | The connection pool to use to connect to Snowflake |
| Object Identifier Resolution | Controls how source object identifiers (schemas, tables, columns) are stored and queried in Snowflake. This setting determines whether you will need to use double quotes in your SQL queries. |
| Schema Name | The name of the schema containing the stream and/or source table |
| Source Table Name | The name of the source table for the stream |
| Stream Creation Parameters | Additional parameters to include in the CREATE STREAM statement. For example, ‘APPEND\_ONLY=TRUE SHOW\_INITIAL\_ROWS=TRUE’ |
| Stream Name | The name of the stream to create, drop, or replace |
| Update Type | The type of stream operation to perform |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The incoming FlowFile is routed to this relationship if the stream operation cannot be completed |
| object not found | The incoming FlowFile is routed to this relationship if the specified stream or source table does not exist. |
| success | The incoming FlowFile is routed to this relationship after the stream operation has been completed successfully |

Expand

Show lessSee more
