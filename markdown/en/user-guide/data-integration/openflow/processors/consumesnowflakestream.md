# ConsumeSnowflakeStream 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Fetches data from a Snowflake stream and writes it to a FlowFile. The stream must be created in the database before using this processor. The processor will consume the stream and write the records to the FlowFile using the specified Record Writer. The processor will also add an attribute to the FlowFile with the name of the stream. The processor will not work if the stream is stale. Instead it will log an error message and stop processing. Stale stream has to be recreated in the database. After the stream is recreated in the database the processor will continue to read and process CDC records. For more information on Snowflake streams, see the <a href=”<https://docs.snowflake.com/en/user-guide/streams-intro>”>snowflake documentation</a>.

## Tags

connection, database, jdbc, openflow, snowflake, stream, table, view

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Max Chunk Size | Number of records to write into a single FlowFile. This value might be slightly exceeded. |
| Record Writer | The Record Writer to use for CDC record serialization |
| Snowflake Connection Service | Database Connection Service for accessing Snowflake |
| Stream Name | The name of the stream in the database |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | For FlowFiles with stream CDC records |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| snowflake.stream.name | Name of the Snowflake Stream |

Expand

Show lessSee more
