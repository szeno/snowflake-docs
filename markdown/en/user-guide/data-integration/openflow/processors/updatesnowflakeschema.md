# UpdateSnowflakeSchema 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Creates Snowflake database schema if it does not exist.

## Tags

create, ddl, preview, schema, snowflake

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Pool | The connection pool to use to connect to Snowflake |
| Object Identifier Resolution | Controls how source object identifiers (schemas, tables, columns) are stored and queried in Snowflake. This setting determines whether you will need to use double quotes in your SQL queries. |
| Schema Creation Cache Expiration Time | The time after which the cache entry will be removed |
| Schema Name | The name of the schema to create |
| Use Schema Creation Cache | Whether to cache schema’s creation instead of executing CREATE SCHEMA IF NOT EXISTS statement for each FlowFile. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The incoming FlowFile is routed to this relationship if the schema cannot be created |
| success | The incoming FlowFile is routed to this relationship after the schema has been created successfully |

Expand

Show lessSee more
