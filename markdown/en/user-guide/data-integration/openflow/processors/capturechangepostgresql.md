# CaptureChangePostgreSQL 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Reads CDC events from a PostgreSQL database. The processor continuously reads events arriving in the stream, filtering for those related to tables provided by the TableStateService, and discarding the rest. After the current batch of events is processed, the processor confirms the replication slot position back to PostgreSQL, letting it trim the WAL. The processor outputs two types of FlowFiles: DDLs, containing the initial schema of a table, and then every time its schema changes, and DMLs, with records representing changes to data in the table. One FlowFile always represents data related to a single table. The DDL with the schema is written to the FlowFile content as a JSON object, in a form such as: { “columns”: [ { “name”: “<columnName>”, “type”: “<snowflakeType>”, “nullable”: <true|false>, “scale”: <scale>, “precision”: <precision> }, … ], “primaryKeys”: [“<primaryKey1>”, “<primaryKey2>”, …] } The DML records are structured as: { “primaryKeys”: { “<column>”: <value>, … }, “payload”: { “<column>”: <value>, … }, “metadata”: { “<column>”: <value>, … }

## Tags

cdc, event, jdbc, postgresql, sql

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Filter Store | Service storing per-table column filtering settings. |
| JDBC Driver Location | Comma-separated list of files/folders and/or URLs containing the driver JAR and its dependencies (if any). For example ‘/var/tmp/postgresql-java-client-42.7.5.jar’ |
| JDBC URL | JDBC URL of the database connection, ie. <jdbc:postgresql://localhost:5432/postgres> |
| Max Batch Size | The maximum number of records to process in a single iteration |
| Max Batch Wait Time | The maximum time to wait for data to appear in the CDC stream. |
| Password | Password to access the PostgreSQL database |
| Publication Name | The name of the CDC publication to read from. |
| Record Writer | The Record Writer is used for serializing DML events |
| Replication Slot Name | The name of the replication slot to use. 63 characters maximum. If the slot doesn’t exist, the processor will create it. |
| SSL Context Service | SSL Context Service supporting encrypted socket communication |
| SSL Mode | Whether to use and enforce SSL when connecting to PostgreSQL |
| TOASTed Value Placeholder | The value to put into a TOASTed column |
| TOASTed Value Strategy | Determines how to handle TOASTed values. |
| Table State Store | The shared store holding the state of replicated tables. |
| Username | Username to access the PostgreSQL database |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Information such as a ‘pointer’ to the current CDC event in the database is stored by this processor, such that it can continue from the same location if restarted, and the name of the replication slot created in PostgreSQL. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Successfully created FlowFile from CDC stream events |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| source.schema.name | Name of the schema of the table from which an event originated |
| source.table.name | Name of the table from which an event originated |
| cdc.event.type | Type of event carried by the FlowFile: ddl or dml |
| cdc.most.significant.position | Ddl’s most significant position in cdc stream |
| cdc.least.significant.position | Ddl’s least significant position in cdc stream |
| cdc.event.seen.at | Timestamp from time when ddl event has been read by the processor |

Expand

Show lessSee more
