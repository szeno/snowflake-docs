# ExecuteSQLStatement 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-processors-nar

## Description

Executes a SQL DDL or DML Statement against a database. This Processor allows Expression Language to be evaluated against FlowFile attributes in order to parameterize the SQL for each FlowFile.

## Tags

database, delete, insert, jdbc, openflow, sql, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Pooling Service | The Connection Pooling Service that is used to obtain a connection to the database |
| Max Batch Size | The maximum number of FlowFiles to process in a single batch |
| Max Content Reference Size | If the SQL property references ${flowfile\_content}, this property specifies the maximum size of the FlowFile that is allowed to be read into memory. If the FlowFile is larger than this value, the FlowFile will be routed to failure. If the SQL property does not reference ${flowfile\_content}, this value has no effect. |
| SQL | The SQL statement to execute. The SQL may make use of Expression Language to reference attributes. In this case, the Processor will rewrite the query using parameters in order to avoid SQL Injection attacks. When referencing Expression Language, the entire value must be a single Expression. For example, *INSERT INTO TABLE X (name) VALUES ( ‘${name}’)* is valid, but *INSERT INTO TABLE X (name) VALUES ( ‘Mr. ${name}’)* is not because Expression Language is used within a String value. The SQL may also reference *${flowfile\_content}* in order to reference the content of the FlowFile as UTF-8 encoded text. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The SQL statement could not be executed |
| success | The SQL statement was successfully executed |

Expand

Show lessSee more
