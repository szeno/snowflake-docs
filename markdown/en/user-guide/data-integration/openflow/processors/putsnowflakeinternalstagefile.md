# PutSnowflakeInternalStageFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Puts files into a Snowflake internal stage. The internal stage must be created in the Snowflake account beforehand.

## Tags

connection, database, jdbc, openflow, snowflake, snowpipe

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Compression Enabled | Set true to compress data before uploading the file |
| Database | The database to use by default. The same as passing ‘db=DATABASE\_NAME’ to the connection string. |
| File Name | Destination file name to use. |
| File Prefix | Path prefix under which the data should be uploaded on the stage. |
| Internal Stage Type | The type of internal stage to use |
| Schema | The schema to use by default. The same as passing ‘schema=SCHEMA’ to the connection string. |
| Snowflake Connection Service | Database Connection Service for accessing Snowflake |
| Stage | The name of the internal stage in the Snowflake account to put files into. |
| Table | The name of the table in the Snowflake account. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | For FlowFiles of failed PUT operation |
| success | For FlowFiles of successful PUT operation |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| snowflake.staged.file.path | Staged file path |

Expand

Show lessSee more
