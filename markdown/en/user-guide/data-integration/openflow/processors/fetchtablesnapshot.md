# FetchTableSnapshot 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Fetches a snapshot of a table from a database. The snapshot is fetched incrementally, using the primary key columns of the table to fetch rows in batches. Replicating a table without primary key is not supported. The snapshot is written to a FlowFile in the specified Record Writer format. The input FlowFile is expected to consist of a JSON representation of the table schema in the following format: { “columns”: [{ “name”: “<column name>”, “type”: “<column type>” }, { “name”: “<column name>”, “type”: “<column type>” }, … ], “primaryKeys”: [“<name of first primary key column>”, “<name of second primary key column>”, …] } Only those columns that are specified in the schema will be fetched from the table.

## Tags

database, fetch, rdbms, snapshot, snowflake, table

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Pool | The connection pool to use to fetch the database snapshot |
| Fetch Size | The maximum number of rows loaded into memory at once |
| JDBC Driver Location | Comma-separated list of files/folders and/or URLs containing the driver JAR and its dependencies (if any). For example ‘/var/tmp/postgresql-java-client-42.7.5.jar’ |
| Max Batch Size | The maximum number of rows to fetch in a single batch |
| Record Writer | The record writer to use to write the fetched snapshot |
| Schema Name | The name of the schema to fetch the snapshot from |
| Table Name | The name of the table to fetch the snapshot from |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| complete | When the snapshot is complete, the original FlowFile will be routed to this relationship |
| failure | If the data cannot be retrieved from the table represented by the FlowFile, the FlowFile will be routed to this relationship. |
| retryable failure | If the data cannot be retrieved from the table represented by the FlowFile but we expect it to be possible in future, the FlowFile will be routed to this relationship. |
| rows | When the snapshot is successfully retrieved from the table represented by the FlowFile, the rows will be routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| snapshot.complete | Indicates whether the snapshot is complete |
| rows.total.fetched | The total number of rows fetched for the table |
| rows.delta.fetched | The number of rows fetched for the table in the last iteration |
| start.row.index | The index of the first row within the snapshot for a given iteration, starting from 0 |
| last.row.index | The index of the last row within the snapshot for a given iteration, starting from 0 |
| fetch.delta.time.in.millis | The time in milliseconds taken to fetch the rows in the last iteration |
| fetch.total.time.in.millis | The time in milliseconds taken so far to fetch the rows |

Expand

Show lessSee more
