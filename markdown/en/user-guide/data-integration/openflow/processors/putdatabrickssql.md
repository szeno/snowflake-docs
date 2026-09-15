# PutDatabricksSQL 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-databricks-processors-nar

## Description

Submit a SQL Execution using Databricks REST API then write the JSON response to FlowFile Content. For high performance SELECT or INSERT queries use ExecuteSQL instead.

## Tags

databricks, openflow, sql

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Databricks Client | Databricks Client Service. |
| Default Catalog | Default table catalog, some SQL statements such as ‘COPY INTO’ do not support using a default catalog |
| Default Schema | Default table schema, some SQL statements such as ‘COPY INTO’ do not support using a default schema |
| Record Writer | Specifies the Controller Service to use for writing results to a FlowFile. The Record Writer may use Inherit Schema to emulate the inferred schema behavior, i.e. an explicit schema need not be defined in the writer, and will be supplied by the same logic used to infer the schema from the column types. |
| SQL Warehouse ID | Warehouse ID used to execute SQL |
| SQL Warehouse Name | SQL Warehouse Name used to execute SQL, will search through all SQL Warehouses to find matching name. |
| Statement | SQL statement to execute |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Databricks failure relationship |
| http.response | HTTP Response to SQL API Request |
| original | The original FlowFile is routed to this relationship when processing is successful. |
| records | Serialized SQL Records |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| statement.state | The final state of the executed SQL statement |
| error.code | The error code for the SQL statement if an error occurred. |
| error.message | The error message for the SQL statement if an error occurred. |

Expand

Show lessSee more
