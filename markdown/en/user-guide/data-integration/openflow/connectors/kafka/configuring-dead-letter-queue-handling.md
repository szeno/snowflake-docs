Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Snowflake Openflow Connector for Kafka: Configuring DLQ handling

This topic explains how to configure a **Kafka topic** as a destination for Dead Letter Queue (DLQ) messages on the **Kafka high-performance connector**, plus the other Kafka-specific parts of DLQ handling (the source processor, parse-failure relationship, and connection reuse).

DLQ handling is shared between the streaming connectors. Read the general guide first — [Configuring Dead Letter Queue (DLQ) handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling) — for the common concepts: the failure envelope, the Snowflake-table route, the raw/structured branches, funnels, and DLQ sink failure handling. This page covers only what is specific to Kafka.

Tip

You don’t have to apply this customization by hand. The **Openflow skill in Snowflake CoCo** can perform it for you — describe the change you want and it edits the flow following the steps on this page. We recommend using the skill instead of configuring the components manually.

## Connector grounding

| Item | Kafka high-performance |
| --- | --- |
| Source processor | `ConsumeKafka` |
| Parse-failure relationship | `parse failure` |
| Connection / credentials to reuse | `Kafka3ConnectionService` |
| Stream-route publisher | `PublishKafka` |
| Record reader / writer | `JsonTreeReader` / `JsonRecordSetWriter` |
| Destination processor | `PublishSnowpipeStreaming` |

Expand

Show lessSee more

## Route the parse failure into the DLQ

On a fresh connector the `ConsumeKafka` `parse failure` relationship is auto-terminated. Remove the auto-termination and connect `parse failure` to the **RAW funnel** described in the [common guide](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling).

## Kafka topic as destination for DLQ messages

Use this route to publish failed records back to a Kafka topic. **Publish the original failed payload as-is — there is no envelope and no record wrapping.** Connect the failure sources directly to a `PublishKafka` sink; the envelope (`raw_payload` / `structured_payload`) is only for the Snowflake-table route, because a Kafka consumer wants the original bytes.

Error context travels out-of-band as Kafka **headers** (via the FlowFile Attribute Header Pattern), not inside the message body.

Note

**Connection reuse:** The DLQ publisher reuses the same `Kafka3ConnectionService` as `ConsumeKafka` — that is, the **same cluster**. If your DLQ topic lives on a **different** Kafka cluster, create a separate `Kafka3ConnectionService` configured for that cluster and point `PublishKafka` at it. The same connector can write DLQ messages to any Kafka cluster and to any Snowflake environment. Otherwise the existing connection is reused.

### Step 1: Create the PublishKafka processor

1. Add a `PublishKafka` processor to the connector’s process group.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Topic Name | Your DLQ topic name. |
| Kafka Connection Service | The same `Kafka3ConnectionService` used by `ConsumeKafka`. |
| Failure Strategy | `Route to Failure` |
| FlowFile Attribute Header Pattern | `kafka\..*` |

Expand

Show lessSee more

### Step 2: Wire the failure sources to the publisher

- Connect the failure sources (the `parse failure` relationship, and any transformation/error relationships) **directly** to this publisher — no raw/structured branches are built for the stream route.
- Route the publisher’s `failure`, `invalid` relationships to the [DLQ sink failure handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling#label-openflow-streaming-dlq-sink-failure). Use a **bounded** `failure` retry (for example, retry count 3) so transient broker issues recover but persistent failures still reach the parking-lot. Do **not** use an effectively-infinite retry (for example, 9999).

## Snowflake table as destination for DLQ messages

Identical to both connectors. See [Route B — Snowflake table](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling#label-openflow-streaming-dlq-route-b) in the common guide.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| DLQ publisher writes to the wrong cluster | `PublishKafka` reuses the `Kafka3ConnectionService` of `ConsumeKafka` — a different cluster needs a separate connection service. |

Expand

Show lessSee more

For shared symptoms (raw branch, `structured_payload`, grants, parking-lot funnel), see the [common troubleshooting table](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling).
