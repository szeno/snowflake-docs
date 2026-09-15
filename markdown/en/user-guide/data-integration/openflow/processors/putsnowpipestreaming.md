# PutSnowpipeStreaming 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowpipe-processors-nar

## Description

Streams records into a Snowflake table. The table must be created in the Snowflake account beforehand.

## Tags

connection, database, jdbc, openflow, snowflake, snowpipe streaming

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Account | Snowflake Account Identifier with Organization Name and Account Name formatted as [organization-name]-[account-name] |
| Authentication Strategy | Strategy for authenticating Snowflake connections |
| Client Lag | The maximum amount of time that the client will wait before flushing records to Snowflake. A larger value can increase latency while sending to Snowflake, but for tables that are not constantly updated it can result in queries that are faster and more cost efficient. |
| Concurrency Group | Allows specifying a ‘Concurrency Group’ that a given FlowFile belongs to, so that the number of Concurrent Tasks that write to tables in a given group can be limited. |
| Connection Strategy | Strategy for connecting to Snowflake Snowpipe Streaming services |
| Database | Snowflake Database destination for processed records |
| Delivery Guarantee | Specifies the delivery guarantee for the records being sent to Snowflake. |
| Iceberg Enabled | Specifies whether the processor ingests data into an Iceberg table. The processor fails if this property doesn’t match the actual table type. |
| Max Batch Size | Maximum number of records to ingest in a single call. Multiple ingest calls will be made if the number of records exceeds the max batch size. Current guidance recommends batch sizes less than 16MB. The Max Batch Size can be tuned based on the average record size such that batches are generally less than 16MB. |
| Max Tasks Per Group | The maximum number of channels to create for a given Snowpipe Channel Prefix. This allows limiting the number of concurrent tasks that can be writing to a given Snowflake table. |
| Private Key Service | RSA Private Key Service for authenticating connections |
| Record Offset | The Expression Language expression to use to determine the offset of the first record in a FlowFile. |
| Record Offset Record Path | The Record Path expression to use to determine the offset of the first record in a FlowFile. |
| Record Offset Strategy | Specifies the strategy for determining the offset of each record. |
| Record Reader | The Record Reader to use for reading the input |
| Role | Snowflake Role the user will assume when authenticating connections |
| Schema | Snowflake Schema destination for processed records |
| Snowpipe Channel Index | The index to use for the Snowpipe channel name. The full channel name will be constructed as openflow.[prefix].[index]. This is necessary in order to provide Exactly Once delivery to Snowflake, as any retry must be tried against the same channel as was previously used. |
| Snowpipe Channel Prefix | The prefix to use for the Snowpipe channel name. The full channel name will be constructed as openflow.[prefix].[index]. The default value is ${hostname(false)}, which ensures that each NiFi node in the cluster writes to a unique channel by incorporating the hostname of the NiFi instance into the channel name. |
| Table | Snowflake Table destination for processed records |
| User | Snowflake User for authenticating connections |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | For FlowFiles that failed to upload to Snowflake |
| success | For FlowFiles successfully uploaded to Snowflake |

Expand

Show lessSee more

## Use cases

| Write record-oriented data to a Snowflake table as fast as possible, accepting the possible of occasional duplicates. |
| --- |

Expand

Show lessSee more
