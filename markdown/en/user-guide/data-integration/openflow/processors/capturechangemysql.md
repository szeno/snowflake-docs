# CaptureChangeMySQL 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Reads CDC events from a MySQL database. The processor continuously reads events from binary log files, filtering those related to the tables provided by the TableStateService, and discarding the rest. The processor outputs two types of FlowFiles: - DDLs containing the schema of a table (the initial schema and a new schema on every schema change). - DMLs with records representing changes to the data in the table. One FlowFile always represents data related to a single table. The DDL with the schema is written to the FlowFile content as a JSON object: { “columns”: [ { “name”: “<columnName>”, “type”: “<snowflakeType>”, “nullable”: <true|false>, “scale”: <scale>, “precision”: <precision> }, … ], “primaryKeys”: [“<primaryKey1>”, “<primaryKey2>”, …] } Structure of the FlowFiles containing the DML records: { “primaryKeys”: { “<column>”: <value>, … }, “payload”: { “<column>”: <value>, … }, “metadata”: { “<column>”: <value>, … }

## Tags

cdc, event, jdbc, mysql, sql

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Filter Store | Service storing per-table column filtering settings. |
| Connection Timeout | Connection to source database timeout |
| JDBC Driver Location | Comma-separated list of files/folders and/or URLs containing the driver JAR and its dependencies (if any). For example ‘/var/tmp/mariadb-java-client-3.4.1.jar’ |
| JDBC URL | JDBC URL of the database connection, ie. <jdbc:mariadb://localhost:3306/mysql> |
| Max Batch Size | The maximum number of records to process in a single iteration. The number of records may exceed the maximum batch size when the last binlog event contains more than one row. |
| Max Batch Wait Time | The maximum time to wait for data to appear in the binlog. |
| Max Queue Size | The maximum number of elements read from binlog until reader thread will wait for onTrigger |
| Password | Password to access the MySQL database |
| Record Writer | The Record Writer is used for serializing DML events |
| SSL Context Service | SSL Context Service supporting encrypted socket communication |
| SSL Mode | SSL Mode used when SSL Context Service configured supporting certificate verification options |
| Server ID | Server ID (in the range from 1 to 2^32 - 1). This value MUST be unique across whole replication group (that is, different from any other Server ID being used by any master or slave). Keep in mind that each binary log client should be treated as a simplified slave and thus MUST also use a different Server ID. |
| Server ID Strategy | Determines how the server ID is selected |
| Table State Store | The shared store holding the state of replicated tables. |
| Username | Username to access the MySQL database |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Information such as a ‘pointer’ to the current CDC event in the database is stored by this processor, such that it can continue from the same location if restarted. |

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
