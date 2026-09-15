Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Configuring Dead Letter Queue (DLQ) handling

The streaming connectors (Kafka high-performance, Kinesis high-performance) consume messages with a `Consume*` processor and deliver them to Snowflake with `PublishSnowpipeStreaming`. Failures occur on two sides:

- **Client-side (Openflow) failures** — records that fail to parse or transform before they reach Snowflake. By default these are **dropped** (the parse-failure relationship is auto-terminated), so they are silently lost unless you add DLQ handling. This topic describes the **common** building blocks for routing those failed records to a dedicated destination instead.
- **Server-side (Snowpipe Streaming) failures** — records that reach Snowflake but can’t be ingested, for example, due to a schema mismatch. These are persisted in a server-side error table when error tables are enabled — see [Snowpipe Streaming error tables](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables). Note that error tables are **not enabled by default**, so without them these failures are silently discarded. The DLQ handling described here is for the client-side failures only.

Tip

You don’t have to apply this customization by hand. The **Openflow skill in Snowflake CoCo** can perform it for you — describe the change you want and it edits the flow following the steps on this page. We recommend using the skill instead of configuring the components manually.

This is the shared reference. For the connector-specific pieces — the source processor and configuring a Kafka topic or Kinesis stream as the DLQ destination — see:

- [Kafka as destination for DLQ messages](/user-guide/data-integration/openflow/connectors/kafka/configuring-dead-letter-queue-handling)
- [Kinesis as destination for DLQ messages](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling)

A DLQ can send failed records to one of two destinations:

- **Kafka topic / Kinesis stream** — republish the failed payload **as-is, with no envelope**, to a messaging destination. Connector-specific — see [Route A for Kafka](/user-guide/data-integration/openflow/connectors/kafka/configuring-dead-letter-queue-handling#label-openflow-kafka-dlq-route-a) / [Route A for Kinesis](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling#label-openflow-kinesis-dlq-route-a).
- **Snowflake table** — wrap failures in the JSON envelope and insert them into a dedicated DLQ table (common — see [Route B](#label-openflow-streaming-dlq-route-b)).

For the **Snowflake-table route**, each failed record is wrapped in a uniform JSON envelope so it can be queried as table columns. The **messaging-destination route does not wrap anything** — it republishes the original failed payload as-is (a Kafka/Kinesis consumer wants the original bytes), so the envelope below applies to Route B only. The fields are a **suggested** structure — you can add, remove, or rename fields to fit your own needs. If you change the envelope, keep the DLQ table schema (see [Route B](#label-openflow-streaming-dlq-route-b)) and the metadata fields in the raw/structured branches consistent with it.

| Field | Description |
| --- | --- |
| `raw_payload` | The original, unparseable bytes captured as a string. |
| `structured_payload` | The parsed JSON record, when available (only for transformation failures). |
| `error_message` | A short description of why the record failed. |
| `failure_timestamp` | UTC timestamp of the failure, stored as `TIMESTAMP_NTZ`. |

Expand

Show lessSee more

## Scope

This topic customizes an **already-installed** streaming connector **in place** by adding components in the Openflow UI and rewiring failure relationships.

**DLQ complexity scales with what the connector contains:**

- A **vanilla / unmodified** connector has only one failure source — the `Consume*` **parse failure** relationship. For these, build a **raw-only DLQ**: capture the unparseable bytes as a `raw_payload` string. No structured handling is needed.
- If the connector has **custom processors** or a **Custom Transformations** process group, those can emit *structured* (valid-JSON) failures. Only then should you add the optional `structured_payload` branch.

**Out of scope — the main `PublishSnowpipeStreaming` (PSS) delivery failures.** PSS retries delivery and Snowflake persists rows it can’t ingest in a server-side error table (when enabled) — see [Snowpipe Streaming error tables](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables). Do **not** wire the main PSS `failure` or `invalid` relationships into the DLQ. Leave them as the connector ships them. The `failure` relationship covers communication errors; the `invalid` relationship routes FlowFiles where at least one record turned out to be invalid.

Note

**Exception.** If you specifically want **all** errors — including PSS delivery failures — to land in the same DLQ table, you can wire the main PSS `failure` relationship into the DLQ as well. This is not recommended: it duplicates what the server-side error table already captures and adds load to the flow. Use it only when a single, unified error destination is a hard requirement.

## Prerequisites

- You have an existing **Kafka high-performance** or **Kinesis high-performance** connector deployed in Openflow.
- You know where failed records should go (a Kafka topic / Kinesis stream, or a Snowflake table).
- For a **Snowflake table** destination: the execute-as role can insert data into the target table (see [Grants](#label-openflow-streaming-dlq-grants)).
- For a **messaging destination** (Kafka topic / Kinesis stream): follow the connector-specific page.

## Error sources

| # | Source | When | Routed to |
| --- | --- | --- | --- |
| 1 | `Consume*` **parse failure** | Always | RAW branch (unparseable bytes) |
| 2 | Custom processor / Custom Transformations failure | Only if such components exist **and** you opt into structured handling | STRUCTURED branch (or RAW branch if you chose raw-only) |
| 3 | Main `PublishSnowpipeStreaming` `failure` / `invalid` | Never (out of scope) | Left as-is (`failure` = communication errors; `invalid` = at least 1 invalid record) |

Expand

Show lessSee more

**The raw-vs-structured choice only applies to the Snowflake-table route** — `structured_payload` is a table column. The stream route publishes the envelope content regardless.

Note

The parse-failure relationship name is connector-specific: `parse failure` (Kafka, with a space) vs `parse.failure` (Kinesis, with a dot). See the connector page for the exact name.

## Common setup

Set up the shared building blocks below first — the DLQ table, grants, capture branches, funnels, and sink failure handling. Then pick a destination route: [Route A](#label-openflow-streaming-dlq-route-a) (Kafka topic / Kinesis stream) or [Route B](#label-openflow-streaming-dlq-route-b) (Snowflake table). The Snowflake-table route uses all of these components; the messaging route reuses only the failure wiring — it publishes the original payload as-is, with no table or envelope.

### Table setup

Decide where the DLQ table lives — the **same** database and schema as the main destination (the default, reusing the existing `Snowflake Destination Database` / `Snowflake Destination Schema` parameters), or a **different** one.

Create the table (adjust the database/schema to your choice):

Copy code

```
CREATE TABLE pipeline_dlq (
    error_message      VARCHAR,
    failure_timestamp  TIMESTAMP_NTZ,
    raw_payload        VARCHAR,
    structured_payload VARIANT
);
```

**Keep this full schema even for a raw-only DLQ** — `structured_payload` simply stays null. That way, adding structured handling later requires no table change.

### Grants

The execute-as role needs the following grants:

Copy code

```
GRANT USAGE ON DATABASE <db> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
GRANT USAGE ON SCHEMA <db>.<schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
GRANT INSERT ON TABLE <db>.<schema>.<table> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

### Raw branch (always)

Captures any non-JSON / unparseable content into the `raw_payload` string field. This is the **only** branch for a vanilla connector, and the fallback for the structured branch.

Note

**Capture the whole payload, not one line at a time.** Reading the failed content line-by-line (for example, a `GrokReader` with **No Match Behavior** = `raw-line`) emits one record **per line**, so a multi-line payload (pretty-printed JSON, multi-line text) is split into many bogus DLQ rows. Capture the **entire FlowFile content** as a single `raw_payload` value instead, using `ExtractText` -> `UpdateAttribute` -> `AttributesToJSON`. This works for any non-JSON content regardless of line breaks.

**Step 1 — Add an `ExtractText` processor** (“Capture Whole Payload”). It copies the entire content into a `raw_payload` attribute, with DOTALL enabled so newlines are included:

| Property | Value |
| --- | --- |
| Enable DOTALL Mode | `true` |
| Maximum Buffer Size | `1 MB` |
| Maximum Capture Group Length | `1048576` |
| `raw_payload` *(dynamic property)* | `(?s)(.*)` |

Expand

Show lessSee more

Note

For **binary** or very large payloads, use a small `ExecuteGroovyScript` that reads the whole content and writes `{"raw_payload": <json-escaped-content>, ...}` directly instead.

**Step 2 — Add an `UpdateAttribute` processor** (“Add Raw DLQ Metadata”):

| Property | Value |
| --- | --- |
| `error_message` | `raw payload (non-JSON)` — on Kinesis you can use `${record.error.message}` instead (see the [Kinesis page](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling)) |
| `failure_timestamp` | `${now():format('yyyy-MM-dd HH:mm:ss.SSS', 'UTC')}` |

Expand

Show lessSee more

**Step 3 — Add an `AttributesToJSON` processor** (“Build Raw DLQ Envelope”). It writes the envelope to FlowFile content (values are JSON-escaped automatically):

| Property | Value |
| --- | --- |
| Attributes List | `raw_payload,error_message,failure_timestamp` |
| Destination | `flowfile-content` |
| Include Core Attributes | `false` |

Expand

Show lessSee more

**Step 4 — Add a `PublishSnowpipeStreaming` processor** (“Ingest Failed Records into DLQ Table”). Reuse the existing PSS auth / web-client service. Point it at the DLQ table:

| Property | Value |
| --- | --- |
| Destination Type | `TABLE` |
| Database | The DLQ table’s database. |
| Schema | The DLQ table’s schema. |
| Table | The DLQ table name (for example, `pipeline_dlq`). |
| Channel Group | `${hostname(false)}.dlq` |
| Authentication Strategy | `SNOWFLAKE_MANAGED` |
| Connection Strategy | `STANDARD` |
| Web Client Service Provider | The existing web-client service. |

Expand

Show lessSee more

Auto-terminate `success`, `empty`. Route `failure`, `invalid` to the [DLQ sink failure handling](#label-openflow-streaming-dlq-sink-failure).

### Structured branch (conditional)

Build this **only** when custom components exist and you want to preserve the parsed JSON in the `structured_payload` VARIANT column.

**Step 1 — Add a `JoltTransformRecord` processor** (“Move Payload to structured\_payload + Add Metadata”). A single processor both shifts the record under `structured_payload` **and** adds the envelope metadata — the **Jolt Specification** property supports Expression Language:

| Property | Value |
| --- | --- |
| Record Reader | The existing `JsonTreeReader`. |
| Record Writer | The existing `JsonRecordSetWriter`. |
| Jolt Transform | `jolt-transform-chain` |
| Jolt Specification | The chain spec below. |

Expand

Show lessSee more

```
[
  {"operation": "shift",   "spec": {"*": "structured_payload.&"}},
  {"operation": "default", "spec": {
    "error_message": "pipeline failure",
    "failure_timestamp": "${now():format('yyyy-MM-dd HH:mm:ss.SSS','UTC')}"
  }}
]
```

(On Kinesis, set `error_message` to `${record.error.message}` — see the [Kinesis page](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling).) This yields the **same envelope fields** as the raw branch (`error_message`, `failure_timestamp`, plus `structured_payload`). Auto-terminate `original`. Route `failure` to the **raw funnel** (fallback: if structuring fails, still capture the bytes).

Route `JoltTransformRecord` `success` to the same `PublishSnowpipeStreaming` processor (“Ingest Failed Records into DLQ Table”) configured in the raw branch. No separate PSS is needed — both branches produce the same envelope schema and share the same channel group (`${hostname(false)}.dlq`).

### Funnels and wiring

Use **funnels** as merge points so multiple failure sources converge cleanly:

- **RAW funnel** — all unparseable / ser-de-failure sources (the `Consume*` parse-failure relationship, and the structured-branch failures) converge here, then flow into `ExtractText` -> `UpdateAttribute` -> `AttributesToJSON` -> the single `PublishSnowpipeStreaming` (“Ingest Failed Records into DLQ Table”).
- **JSON funnel** (only if the structured branch exists) — custom / transformation failures converge here, then flow into `JoltTransformRecord` -> the same single `PublishSnowpipeStreaming`.

For a **raw-only** connector, omit the JSON funnel and structured branch entirely — every source goes to the RAW funnel.

### DLQ sink failure handling

If even the DLQ publish/insert fails, do not lose the record:

1. Route the DLQ sink’s `failure`, `invalid` relationships (the `PublishSnowpipeStreaming`, `PublishKafka`, or `PublishKinesis`) to a `LogAttribute` processor (“Log DLQ Ingestion Error”, **Log Level** = `error`, with a prefix such as “Failed to ingest data into the DLQ”).
2. Route `LogAttribute` `success` to a **parking-lot funnel** where un-deliverable records accumulate for inspection.

## Route A — Kafka topic / Kinesis stream

This route republishes the failed payload **as-is, with no envelope**, to a messaging destination — it does not use the DLQ table or the raw/structured branches in [Common setup](#label-openflow-streaming-dlq-common-setup). The publisher and the connection/credentials it reuses are connector-specific, so the steps live on the connector pages:

- [Kafka as destination for DLQ messages](/user-guide/data-integration/openflow/connectors/kafka/configuring-dead-letter-queue-handling#label-openflow-kafka-dlq-route-a)
- [Kinesis as destination for DLQ messages](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling#label-openflow-kinesis-dlq-route-a)

## Route B — Snowflake table

This route assembles the building blocks from [Common setup](#label-openflow-streaming-dlq-common-setup) — the DLQ table, grants, raw/structured branches, and funnels — with `PublishSnowpipeStreaming` as the terminal sink. It is identical for both connectors.

## Data types and JSONL handling

Both sinks consume the same envelope: `PublishSnowpipeStreaming` expects **JSONL** (one JSON object per line), and the stream publishers send that same JSONL content as the message value. Failures arrive in different shapes, so route them through a reader that produces valid records:

- **Unparseable / non-JSON** (parse failure): the raw branch’s `ExtractText` (DOTALL) captures the **whole payload** — any text, including multi-line content — into a single `raw_payload` field. (A line-based reader such as `GrokReader` with **No Match Behavior** = `raw-line` only wraps a single text *line* per record, so it splits multi-line payloads; use the whole-content capture instead.) This is what makes the raw branch robust against malformed input.
- **Valid JSON** (downstream / transformation failures): the structured branch’s Jolt shift `{"*":"structured_payload.&"}` nests the parsed object under `structured_payload`. On any failure it **falls back to the raw funnel**, so nothing is lost.

Note

**Watch for data-type changes along the flow.** A message may be one type at the source (for example, CSV/TSV or a malformed line) and a different type after a downstream mapping. Match the capture to the content **at the point of failure** — do not feed raw CSV/TSV into a JSON reader. The whole-content raw branch handles this safely for any non-JSON content.

## Verification

After wiring, enable all controller services **first** (processors referencing a disabled service show as INVALID), then validate the process group. Fix any validation failures before starting the flow.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `CREATE TABLE` / insert denied | Missing grants on the DLQ schema (see [Grants](#label-openflow-streaming-dlq-grants)). |
| Records pile up in the parking-lot funnel | DLQ table/schema mismatch or wrong database/schema/table parameters — inspect the `LogAttribute` error output. |

Expand

Show lessSee more

For connector-specific symptoms (parse-failure relationship name, publishing to a topic/stream), see the [Kafka](/user-guide/data-integration/openflow/connectors/kafka/configuring-dead-letter-queue-handling) and [Kinesis](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling) troubleshooting tables.
