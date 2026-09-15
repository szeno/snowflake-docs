# CaptureChangeSqlServer 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Reads CDC events from a SQL Server database. The processor periodically queries Change Tracking tables in the database, but only for the tables provided by the TableStateService. The processor maintains a state of the last processed event for each table. The processor moves the position after each processed table. The processor supports multi-threading. The number of threads and connection limit configured in the pool collectively define the upper bound of open connections to the source database. The processor outputs two types of FlowFiles: DDLs, containing the initial schema of a table, and then every time its schema changes, and DMLs, with records representing changes to data in the table. One FlowFile always represents data related to a single table. The DDL with the schema is written to the FlowFile content as a JSON object, in a form such as: { “columns”: [ { “name”: “<columnName>”, “type”: “<snowflakeType>”, “nullable”: <true|false>, “scale”: <scale>, “precision”: <precision> }, … ], “primaryKeys”: [“<primaryKey1>”, “<primaryKey2>”, …] } The DML records are structured as: { “primaryKeys”: { “<column>”: <value>, … }, “payload”: { “<column>”: <value>, … }, “metadata”: { “<column>”: <value>, … }

## Tags

cdc, event, jdbc, sql, sql server

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Filter Store | Service storing per-table column filtering settings. |
| Connection Pool | The connection pool |
| Fetch Size | The maximum number of rows loaded into memory at once |
| Max Batch Size | The maximum number of rows to fetch in a single batch |
| Record Writer | The Record Writer is used for serializing DML events |
| Table Changes Query Interval | The minimum time interval that must elapse before scheduling the next query for table changes. This controls the frequency of database polling to prevent excessive querying. |
| Table State Store | The shared store holding the state of replicated tables. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Information such as a version of the last processed record for each table is stored by this processor, such that it can continue from the same location if restarted. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Successfully created FlowFile from CDC stream events |

Expand

Show lessSee more
