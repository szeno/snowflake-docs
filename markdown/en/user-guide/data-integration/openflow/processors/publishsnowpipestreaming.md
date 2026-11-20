# PublishSnowpipeStreaming 2026.11.12.16

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowpipe-streaming-2-processors-nar

## Description

Publishes records formatted as newline-delimited JSON to Snowflake pipes or tables by using Snowpipe Streaming version 2.

With a **Standard** channel, the processor waits for the streaming channel to report committed offset tokens (according to **Offset Tracking Resolution** and **Offset Tracking Timeout**) before routing transferred FlowFiles to **success**, **invalid**, or **failure**. Standard channels support configurable delivery and ordering semantics. The processor can run when the incoming connection has no FlowFiles so that pending Standard-channel batches finish polling.

With an **Elastic** channel, the processor uses at-least-once delivery without ordering and routes FlowFiles after the transfer request completes. Offset tracking properties and **Channel Group** don’t apply to Elastic channels.

## Tags

NDJSON, Snowflake, Snowpipe Streaming

## Input requirement

REQUIRED

## Supports sensitive dynamic properties

false

## Properties

Configure Snowflake authentication, the destination, channel behavior, offset tracking, and record transfer.

| Property | Description |
| --- | --- |
| Account | Snowflake Account Identifier with Organization Name and Account Name formatted as [organization-name]-[account-name]. This property applies when **Authentication Strategy** is **Key Pair**. |
| Authentication Strategy | Strategy for authenticating Snowflake connections. Default: **Key Pair**. |
| Connection Strategy | Strategy for connecting to Snowpipe Streaming services. **Standard** uses public routing. **Private Connectivity** uses private addresses provided by the supporting cloud platform, such as AWS PrivateLink. This property applies when **Authentication Strategy** is **Key Pair**. Default: **Standard**. |
| Channel Group | Group for managing distinct Snowpipe Streaming channels with partitioning. Supports Expression Language using FlowFile attributes. This property applies when **Channel Type** is **Standard**. Default: `SHARED`. |
| Channel Type | Channel configuration strategy for Snowpipe Streaming. **Standard** provides configurable delivery and ordering semantics. **Elastic** provides at-least-once delivery without ordering. Default: **Standard**. |
| Channel Insert Timeout | Maximum duration to retry inserting records before failing. Must be from 1 second through 5 minutes. Default: 30 seconds. |
| Database | Snowflake Database destination for processed records |
| Destination Type | Snowflake destination object for processed records. **Pipe** uses a pipe created with `TYPE = STREAMING`. **Table** uses a default pipe derived by appending `-STREAMING` to the table name. Default: **Table**. |
| File Fragment Count | Maximum number of file fragments sent to object storage for Snowpipe Streaming ingestion from input FlowFiles. This property applies when **Transfer Strategy** is **File Fragments**. Must be from 1 through 100. Default: 4. |
| File Fragment Size | Maximum size for each file fragment sent to object storage for Snowpipe Streaming ingestion. This property applies when **Transfer Strategy** is **File Fragments**. Must be from 1 KB through 256 MB. Default: 64 MB. |
| Metric Resolution | Controls which Snowpipe Streaming metrics are emitted and which attributes they include. **Processor** emits only generic processor metrics. **Destination** emits `snowpipe.streaming.rows.sent`, `snowpipe.streaming.bytes.sent`, `snowpipe.streaming.last.push.time`, and `snowpipe.streaming.consume.to.push.latency` with destination pipe, database, and schema attributes. **Source and Destination** adds the `source.name` attribute to those metrics. Default: **Processor**. |
| Offset Token End Expression | Expression Language definition that produces the highest offset token for a FlowFile as a monotonically increasing number. This property applies to Standard channels when **Offset Tracking Resolution** is **FlowFile** or **Record**. |
| Offset Token Record Pointer | JSON Pointer to the offset token in each record. The processor uses this pointer when the last committed offset token is between the start and end boundaries. This property applies to Standard channels when **Offset Tracking Resolution** is **Record**. |
| Offset Token Start Expression | Expression Language definition that produces the lowest offset token for a FlowFile as a monotonically increasing number. This property applies to Standard channels when **Offset Tracking Resolution** is **Record**. |
| Offset Tracking Resolution | Resolution level for evaluating committed offset tokens against input FlowFiles and records. **Disabled** uses opaque offset token handling without tracking across FlowFiles or records. **FlowFile** tracks each FlowFile with monotonically increasing offset tokens. **Record** tracks each record in each FlowFile with monotonically increasing offset tokens. This property applies to Standard channels. Default: **Disabled**. |
| Offset Tracking Timeout | Maximum duration to wait for channel status to confirm committed offset tokens before routing to **failure**. This property applies to Standard channels. Default: 90 seconds. |
| Pipe | Snowflake pipe destination for processed records. Supports Expression Language using FlowFile attributes. This property applies when **Destination Type** is **Pipe**. |
| Private Key Service | RSA Private Key Service for authenticating connections. This property applies when **Authentication Strategy** is **Key Pair**. |
| Role | Snowflake role used to authorize connection operations. If not specified, the processor uses the user’s default role. This property applies when **Authentication Strategy** is **Key Pair**. |
| Schema | Snowflake Schema destination for processed records |
| Source Name | Value recorded as the `source.name` attribute on the Snowpipe Streaming metrics listed for **Metric Resolution**. Supports Expression Language using FlowFile attributes. This property applies when **Metric Resolution** is **Source and Destination**. |
| Source Timestamp | Epoch time in milliseconds for the earliest source record represented by each FlowFile. Snowpipe Streaming uses the earliest usable value in an insert request to calculate end-to-end latency. If the value is missing, nonpositive, can’t be parsed, or can’t be evaluated, the processor uses the FlowFile lineage start time. Default: `${lineageStartDate}`. |
| Table | Snowflake table destination for processed records. Supports Expression Language using FlowFile attributes. This property applies when **Destination Type** is **Table**. |
| Transfer Strategy | Strategy for transferring records to Snowpipe Streaming. **Managed** transfers records as either batches of rows or file fragments based on uncompressed size. **Rows** transfers batches of rows over HTTP to Snowpipe Streaming. **File Fragments** transfers file fragments over HTTP to cloud storage services. Default: **Managed**. |
| User | Snowflake User for authenticating connections. This property applies when **Authentication Strategy** is **Key Pair**. |
| Web Client Service Provider | Web Client Service Provider supporting HTTP request and response handling |

Expand

Show lessSee more

## Writes attributes

For completed Standard-channel batches, the processor writes this attribute to report row-level ingestion errors.

| Name | Description |
| --- | --- |
| channel.status.row.errors.added | Number of row errors reported for a pending Standard-channel batch. The value is `0` when the completed batch has no row errors. |

Expand

Show lessSee more

## Relationships

Connect these relationships to route each FlowFile according to its Snowpipe Streaming result.

| Name | Description |
| --- | --- |
| empty | Routes empty FlowFiles that weren’t sent to Snowflake. |
| failure | Routes FlowFiles that couldn’t be uploaded to Snowflake. |
| invalid | Routes partially transmitted FlowFiles for which Snowflake reported one or more invalid rows. |
| success | Routes FlowFiles successfully uploaded to Snowflake. |

Expand

Show lessSee more
