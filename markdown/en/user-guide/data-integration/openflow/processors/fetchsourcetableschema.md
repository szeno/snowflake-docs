# FetchSourceTableSchema 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Fetches the table schema (i.e., column names, data types, etc.) for a given table in a database, converting the data types to Snowflake-compatible types. The schema is written to the FlowFile content as a JSON object, in a form such as: { “columns”: [ { “name”: “<columnName>”, “type”: “<snowflakeType>”, “nullable”: <true|false>, “scale”: <scale>, “precision”: <precision> }, … ], “primaryKeys”: [“<primaryKey1>”, “<primaryKey2>”, …] }

## Tags

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Filter Service | Specifies the Column Filter Service to be used for filtering out unwanted columns |
| Connection Pool | The connection pool to use to fetch the source table schema |
| Schema Name | The name of the schema that the source table is stored in |
| Table Name | The name of the source table |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to this relationship in the event that the source table’s schema cannot be fetched |
| success | FlowFiles are routed to this relationship when the source table’s schema is successfully fetched |
| table not found | FlowFiles are routed to this relationship when the source table does not exist |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | application/json |
| dbms.type | The type of database management system (DBMS) that the source table is stored in. E.g. *POSTGRESQL* |
| primary.key.count | The number of primary keys in the source table |
| column.count | The number of columns in the source table |

Expand

Show lessSee more
