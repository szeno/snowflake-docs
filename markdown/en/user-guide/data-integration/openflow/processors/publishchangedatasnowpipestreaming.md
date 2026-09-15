# PublishChangeDataSnowpipeStreaming 2026.4.28.15

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowpipe-streaming-2-processors-nar

## Description

Publishes change data records formatted as Newline Delimited JSON to Snowflake Database Pipes using Snowpipe Streaming High Availability. The processor supports **Concurrency Group** serialization so FlowFiles that share the same group are not processed against the channel concurrently.

After data is transferred, the processor waits for the streaming channel to report committed offset tokens (according to **Offset Tracking Resolution** and **Offset Tracking Timeout**) before routing FlowFiles to **success**, **invalid**, or **failure**. It can run when the incoming connection has no FlowFiles so that pending batches finish polling.

## Tags

CDC, Change Data Capture, NDJSON, Snowflake, Snowpipe Streaming

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Account | Snowflake Account Identifier with Organization Name and Account Name formatted as [organization-name]-[account-name] |
| Authentication Strategy | Strategy for authenticating Snowflake connections |
| Channel Group | Group for managing distinct Snowpipe Streaming Channels with partitioning |
| Channel Insert Timeout | Maximum duration to retry inserting records before failing with an upper bound of 5 minutes |
| Concurrency Group | Controls access to the configured channel with serialized claims according to the configured value or expression |
| Database | Snowflake Database destination for processed records |
| Destination Type | Snowflake destination object for processed records with support for derived default pipes |
| Offset Token End Expression | Expression Language definition to produce the highest offset token for a FlowFile as a monotonically increasing number |
| Offset Token Record Pointer | JSON Pointer to offset token in each record required when the last committed offset token is between start and end boundaries |
| Offset Token Start Expression | Expression Language definition to produce the lowest offset token for a FlowFile as a monotonically increasing number |
| Offset Tracking Resolution | Resolution level for evaluating committed offset tokens against input FlowFiles and records. **Disabled**: opaque offset token handling without tracking across FlowFiles or records. **FlowFile**: track each FlowFile with monotonically increasing offset tokens. **Record**: track each record in each FlowFile with monotonically increasing offset tokens. |
| Offset Tracking Timeout | Maximum duration to wait for channel status to confirm committed offset tokens before routing to failure |
| Pipe | Snowflake Pipe destination for processed records |
| Private Key Service | RSA Private Key Service for authenticating connections |
| Role | Snowflake Role the user will assume when authenticating connections |
| Schema | Snowflake Schema destination for processed records |
| Table | Snowflake Table destination for processed records |
| Transfer Strategy | Strategy for transferring records to Snowpipe Streaming. **Managed**: transfer records as either batches of rows or file fragments based on uncompressed size. **Rows**: transfer records as batches of rows over HTTP to Snowpipe Streaming. **File Fragments**: transfer records as file fragments over HTTP to cloud storage services. |
| User | Snowflake User for authenticating connections |
| Web Client Service Provider | Web Client Service Provider supporting HTTP request and response handling |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| empty | FlowFiles with empty content not sent to Snowflake |
| failure | FlowFiles that failed to upload to Snowflake |
| invalid | FlowFiles that Snowflake identified as containing one or more invalid rows resulting in partial transmission |
| success | FlowFiles successfully uploaded to Snowflake |

Expand

Show lessSee more
