Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Openflow Connector for Kinesis Data Streams: Configuring DLQ handling

This topic explains how to configure a **Kinesis stream** as a destination for Dead Letter Queue (DLQ) messages on the **Kinesis high-performance connector**, plus the other Kinesis-specific parts of DLQ handling (the source processor, parse-failure relationship, and credential reuse).

DLQ handling is shared between the streaming connectors. Read the general guide first — [Configuring Dead Letter Queue (DLQ) handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling) — for the common concepts: the failure envelope, the Snowflake-table route, the raw/structured branches, funnels, and DLQ sink failure handling. This page covers only what is specific to Kinesis.

Tip

You don’t have to apply this customization by hand. The **Openflow skill in Snowflake CoCo** can perform it for you — describe the change you want and it edits the flow following the steps on this page. We recommend using the skill instead of configuring the components manually.

## Connector grounding

| Item | Kinesis high-performance |
| --- | --- |
| Source processor | `ConsumeKinesis` |
| Parse-failure relationship | `parse.failure` |
| Connection / credentials to reuse | `AWSCredentialsProviderControllerService` + **Region** + **Stream Name** |
| Stream-route publisher | `PutKinesisStream` |
| Record reader / writer | `JsonTreeReader` / `JsonRecordSetWriter` |
| Destination processor | `PublishSnowpipeStreaming` |

Expand

Show lessSee more

## Route the parse failure into the DLQ

On a fresh connector the `ConsumeKinesis` `parse.failure` relationship is auto-terminated. Remove the auto-termination and connect `parse.failure` to the **RAW funnel** described in the [common guide](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling).

Tip

**Capture the error reason.** `ConsumeKinesis` writes a `record.error.message` FlowFile attribute on parse/serde failure. Use `${record.error.message}` for the `error_message` field in the raw/structured branch metadata (the Kafka connector has no equivalent attribute).

## Kinesis stream as destination for DLQ messages

Use this route to publish failed records back to a Kinesis stream. **Publish the original failed payload as-is — there is no envelope and no record wrapping.** Connect the failure sources directly to a `PutKinesisStream` sink; the envelope (`raw_payload` / `structured_payload`) is only for the Snowflake-table route, because a stream consumer wants the original bytes.

Note

**Credential reuse:** The DLQ publisher reuses the same `AWSCredentialsProviderControllerService` + **Region** as `ConsumeKinesis` — that is, the **same AWS account/region**. If your DLQ stream lives in a **different** account or region, configure the publisher with the appropriate credentials/region (and for a fully separate environment, a separate connector).

### Step 1: Create the PutKinesisStream processor

1. Add a `PutKinesisStream` processor to the connector’s process group.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Stream Name | Your DLQ stream name. |
| AWS Credentials Provider Service | The same `AWSCredentialsProviderControllerService` used by `ConsumeKinesis`. |
| Region | The same region as `ConsumeKinesis`. |

Expand

Show lessSee more

Note

`PutKinesisStream` publishes the entire FlowFile content as a single Kinesis message. If the FlowFile contains multiple records (for example, NDJSON with one record per line), use a `SplitText` processor before `PutKinesisStream` to split the FlowFile into individual FlowFiles, one per line.

### Step 2: Wire the failure sources to the publisher

- Connect the failure sources (the `parse.failure` relationship, and any transformation/error relationships) **directly** to this publisher — no raw/structured branches are built for the stream route.
- Route the publisher’s `failure`, `invalid` relationships to the [DLQ sink failure handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling#label-openflow-streaming-dlq-sink-failure). Use a **bounded** `failure` retry (for example, retry count 3) so transient stream issues recover but persistent failures still reach the parking-lot. Do **not** use an effectively-infinite retry (for example, 9999).

## Snowflake table as destination for DLQ messages

Identical to both connectors. See [Route B — Snowflake table](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling#label-openflow-streaming-dlq-route-b) in the common guide.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| DLQ publisher writes to the wrong stream/account | `PutKinesisStream` reuses the `AWSCredentialsProviderControllerService` + **Region** of `ConsumeKinesis` — a different account/region needs the appropriate credentials and region. |

Expand

Show lessSee more

For shared symptoms (raw branch, `structured_payload`, grants, parking-lot funnel), see the [common troubleshooting table](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling).
