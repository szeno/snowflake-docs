Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Configuring custom transformations

The streaming connectors (Kafka high-performance, Kinesis high-performance) consume messages with a `Consume*` processor and deliver them to Snowflake with `PublishSnowpipeStreaming`. By default the source connects directly to `PublishSnowpipeStreaming`. This topic describes how to insert **custom processing** between the source and the destination — filtering, field mapping (flatten / rename / remove), topic-to-table mapping, content-based routing to multiple tables, default values, and custom Groovy scripts — by adding a **Custom Transformations** process group in the Openflow UI. You apply this to an already-deployed streaming connector. If you don’t have one yet, first set up the [Kafka](/user-guide/data-integration/openflow/connectors/kafka/setup) or [Kinesis](/user-guide/data-integration/openflow/connectors/kinesis/setup) connector.

Streaming connectors use at-least-once (ALO) delivery. Custom processing sits directly in that path, so a set of **restriction rules** must be followed or you risk duplication, out-of-order delivery, or data loss (if records are explicitly dropped). Read [Restriction rules](#label-openflow-streaming-custom-transformations-restriction-rules) before adding any processor.

Tip

You don’t have to apply this customization by hand. The **Openflow skill in Snowflake CoCo** can perform it for you — describe the change you want and it edits the flow following the steps on this page. We recommend using the skill instead of configuring the components manually.

To get started, install and connect the [Snowflake CoCo CLI](/user-guide/cortex-code/cortex-code-cli), then ask the bundled [`openflow` skill](/user-guide/cortex-code/bundled-skills#label-bundled-skill-openflow) to make the change.

For switching the message data type (JSON to Avro / Protobuf), see:

- [Configuring Avro data type ingestion](configuring-avro-data-type-ingestion)
- [Configuring Protobuf data type ingestion](configuring-protobuf-data-type-ingestion)

For routing failed records to a dedicated destination instead of dropping them, see:

- [Configuring Dead Letter Queue (DLQ) handling](configuring-dead-letter-queue-handling)

## Scope

This topic customizes an **already-installed** streaming connector **in place** by adding a process group and processors in the Openflow UI and rewiring the source-to-destination path.

What this topic covers:

- Optionally inserting a **Custom Transformations** process group for readability (processors can also be added directly to the connector canvas).
- The **restriction rules** for safe in-flight processing.
- Reusing the connector’s existing `JsonTreeReader` / `JsonRecordSetWriter` and adding a schema cache.
- Planning a pipeline that minimizes serialization/deserialization (ser/de) passes.
- Common transformation patterns and the processors that implement them.

Out of scope — broker authentication, data-type switching, and Snowflake Private Key Auth. See the [See also](#label-openflow-streaming-custom-transformations-see-also) links.

## Prerequisites

- You have an existing **Kafka high-performance** or **Kinesis high-performance** connector deployed in Openflow.
- The connector currently connects its source processor (for example, `ConsumeKafka`) directly to `PublishSnowpipeStreaming`.
- You know which transformation you need and to which table(s) records should be written.
- The execute-as role can create any target tables used for routing (see the connector’s destination grants).

## Architecture

Insert the transformation processors between the source processor and `PublishSnowpipeStreaming` — that is, remove the direct source to `PublishSnowpipeStreaming` connection and chain your processors in between.

Note

The Custom Transformations process group is optional. You can add the transformation processors directly onto the connector’s canvas, between the source processor and `PublishSnowpipeStreaming`. Grouping them inside a dedicated process group named **Custom Transformations** (with an Input Port and an Output Port) is purely for **readability and maintainability** — it visually separates your customizations from the connector’s built-in components and makes them easy to find, label, and reason about. It changes nothing functionally: the same processors, restriction rules, FIFO connections, and reader/writer apply either way. The rest of this topic describes the grouped layout. If you skip the group, ignore the Input/Output Port steps and connect the source processor directly to your first transformation processor and your last one directly to `PublishSnowpipeStreaming`.

The recommended (grouped) layout. An **Input Port** receives messages from the source, transformation processors run inside the group, and an **Output Port** feeds the result to `PublishSnowpipeStreaming`:

```
ConsumeKafka (or ConsumeKinesis)
    | (success)
    v
[Custom Transformations Input]   <- Input Port
    |
    ... transformation processors ...
    |
[Custom Transformations Output]  <- Output Port
    |
    v
PublishSnowpipeStreaming
```

### Step 1: Create the process group (optional)

This step (and Step 2) is only needed if you want the grouped layout. To add processors directly onto the connector canvas instead, do Step 1.1–1.2 below, then skip to [Step 3](#label-openflow-streaming-custom-transformations-wire) and connect the source processor straight to your first transformation processor.

1. Open the connector’s process group in the Openflow UI.
2. Remove the existing connection between the source processor and `PublishSnowpipeStreaming`.
3. Drag a new **Process Group** onto the canvas and name it `Custom Transformations`.

### Step 2: Add the input and output ports (optional)

Only if you created the process group in Step 1. Inside the `Custom Transformations` group:

1. Add an **Input Port** named `Custom Transformations Input`.
2. Add an **Output Port** named `Custom Transformations Output`.

### Step 3: Wire the processing into the flow

1. Connect the source processor’s `success` relationship to `Custom Transformations Input` (or directly to your first transformation processor if you skipped the group).
2. Connect `Custom Transformations Output` to `PublishSnowpipeStreaming` (or your last transformation processor to `PublishSnowpipeStreaming` if you skipped the group).
3. Configure **every** connection (both these external connections and all internal connections you add later) with the **FirstInFirstOut** prioritizer. See [Connection configuration](#label-openflow-streaming-custom-transformations-connection-config).

## Restriction rules

Warning

These rules MUST be followed. Violating them might cause data loss, duplication, or performance degradation.

1. **Minimize ser/de operations.** Plan the full pipeline *before* creating processors. Combine filtering, renaming, and defaults into as few record-aware processors as possible. Extract useful values (for example, routing fields) as attributes early so downstream steps can use attribute-only processors (`RouteOnAttribute`, `UpdateAttribute`) instead of content-aware ones.
2. **Reuse the existing reader/writer where possible.** The connector already defines a `JsonTreeReader` (schema inference) and a `JsonRecordSetWriter` at the parent process-group level, and these are visible to your processors. When a processor reads or writes content of the same data type, prefer reusing these existing services rather than creating new ones — it keeps the flow simple and consistent. See [Reader and writer setup](#label-openflow-streaming-custom-transformations-reader-writer).
3. **One table per FlowFile.** A single FlowFile can contain records for only ONE table. Prefer `RouteOnAttribute` over `PartitionRecord` when the routing value is already available as an attribute (it saves a ser/de pass).
4. **Use FIFO prioritizers on connections.** Apply the **FirstInFirstOut** prioritizer on ALL connections (internal and external). This keeps records in arrival order within each partition and avoids unexpected interleaving. It does not affect throughput.
5. **No array exploding to the same table.** Exploding an array into multiple records destined for the *same* table is NOT allowed (it can cause data loss or duplicates). Array exploding is valid only when the resulting records route to *different* tables.
6. **Let schema inference handle structure.** With the existing `JsonTreeReader` (plus a `VolatileSchemaCache`) and `JsonRecordSetWriter`, structural changes are handled automatically — you do not need to define schemas manually.

## Reader and writer setup

Transformation processors that access FlowFile content need a Record Reader and Record Writer. The connector already defines a `JsonTreeReader` and a `JsonRecordSetWriter` at the parent process-group level, and these are visible inside the `Custom Transformations` group. When a processor works with the same data type, prefer reusing these existing services rather than creating new ones.

### Add a schema cache to the reader (recommended)

The existing `JsonTreeReader` uses schema inference. To avoid re-inferring the schema on every FlowFile, add a `VolatileSchemaCache` and point the reader at it.

1. At the **connector** process-group level, go to **Configure** > **Controller Services**.
2. Add a `VolatileSchemaCache` service.

| Property | Value |
| --- | --- |
| Maximum Cache Size | `100` (default is usually sufficient) |

Expand

Show lessSee more

3. **Enable** the `VolatileSchemaCache` service.
4. **Disable** the `JsonTreeReader` (required before editing it).
5. Edit `JsonTreeReader` and set:

| Property | Value |
| --- | --- |
| Schema Inference Cache | The `VolatileSchemaCache` created above. |

Expand

Show lessSee more

6. **Enable** the `JsonTreeReader` again.

This caches the inferred schema and reuses it for messages with the same structure, improving performance.

## Transformation planning

**Plan the full pipeline before creating any processor** (rule 1). The goal is the fewest possible ser/de passes. Building processors one-by-one without a plan almost always produces a wasteful pipeline.

### Planning checklist

1. **List every required transformation** (filter, rename, defaults, routing, and so on).
2. **Identify which can run on attributes alone** (zero ser/de). Attribute-only processors work only when the FlowFile already carries the attribute (for example, `kafka.topic` set by `ConsumeKafka`, `aws.kinesis.stream.name` set by `ConsumeKinesis`, or an attribute set by an upstream `PartitionRecord`):

   - Routing by source (topic / stream) or by an existing attribute → `UpdateAttribute` to derive a target table name into an attribute (for example, `table.name`), which `PublishSnowpipeStreaming` then reads to pick the destination table. This is explained in detail under [Topic-to-table mapping](#label-openflow-streaming-custom-transformations-topic-to-table) and [Content-based routing to multiple tables](#label-openflow-streaming-custom-transformations-content-routing).
   - Attribute-based filtering → `RouteOnAttribute`.
3. **Combine content transformations** into the fewest content-aware processors:

   - Filter + rename + defaults → ONE `QueryRecord` (SQL `SELECT` aliases, `COALESCE`, `WHERE`) or ONE `JoltTransformRecord` (Chain spec).
4. **Use `PartitionRecord` for multi-table routing.** A FlowFile may contain many records with *different* values for a routing field. Partitioning splits the FlowFile so each output FlowFile holds records for one value only, and sets that value as a FlowFile attribute.
5. **Order operations:** content transforms first (one pass on the whole FlowFile) → partition (split into per-value FlowFiles) → `UpdateAttribute` to set a target table-name attribute from the partitioned value (zero ser/de — `PublishSnowpipeStreaming` uses this attribute to choose the destination table) → `RouteOnAttribute` only if filtering is needed (zero ser/de). The table-name attribute is explained under [Content-based routing to multiple tables](#label-openflow-streaming-custom-transformations-content-routing).

### Choosing between readable and optimized pipelines

After planning the standard-processor pipeline, count its ser/de passes:

- **1 pass** — nothing to optimize, so implement it.
- **2 or more passes** — a single `ExecuteGroovyScript` could consolidate all content operations into 1 pass. Weigh maintainability (standard processors are easier to read and modify) against performance (one Groovy script can be faster for performance-critical workloads — confirm assumptions with testing before optimizing — but is harder to change). Choose the readable option unless you specifically need maximum performance.

**Example — “filter by timestamp, rename fields, add defaults, route to tables by field value”:**

Readable (2 ser/de passes):

```
Input Port
  -> QueryRecord    (ser/de #1: rename via SELECT aliases, defaults via COALESCE, filter via WHERE)
  -> PartitionRecord (ser/de #2: split by routing field -> sets attribute)
  -> UpdateAttribute (zero ser/de: table.name = ${routing-field})
  -> RouteOnAttribute (zero ser/de: drop unwanted values, auto-terminate unmatched)
  -> Output Port
```

Optimized (1 ser/de pass):

```
Input Port
  -> ExecuteGroovyScript (ser/de #1: rename + defaults + filter + partition by routing field)
  -> UpdateAttribute (zero ser/de: table.name = ${routing-field})
  -> RouteOnAttribute (zero ser/de: drop unwanted values)
  -> Output Port
```

`PublishSnowpipeStreaming` handles multi-table routing natively — set its **Table** property to `${table.name}` (or the routing attribute directly). `RouteOnAttribute` is only for *filtering*, never required for routing alone.

**Anti-pattern (avoid):** separate processors for each of filter / rename / partition (3 ser/de passes where 2 suffice), or a separate `UpdateAttribute` per route value. Combine where possible, and use a single `UpdateAttribute` driven by the partitioned attribute.

## Connection configuration

**Every** connection — both into/out of the `Custom Transformations` group and between processors inside it — MUST be configured with:

1. **FirstInFirstOut prioritizer** — keeps records in arrival order within each partition (rule 4).
2. **Back pressure** — leave at defaults unless you have a specific reason to change it.

To set the prioritizer: edit the connection, open the **Settings** tab, and add **FirstInFirstOutPrioritizer** under **Prioritizers**.

This applies to:

- Source processor to `Custom Transformations Input`
- `Custom Transformations Output` to `PublishSnowpipeStreaming`
- All connections between processors inside the group

Note

**Connection queue before `PublishSnowpipeStreaming`:** Set the connection queue size limit to **5 GB** (not the default 1 GB). `PublishSnowpipeStreaming` keeps FlowFiles queued until they are acknowledged by Snowflake; with the default 1 GB limit, backpressure activates too early under normal load.

## Transformation patterns

Pick the pattern that matches your need. All patterns assume the reader/writer setup above and obey the restriction rules.

### Pattern: Filtering messages

**By attribute / key (no ser/de — preferred).** Use `RouteOnAttribute`. It reads only FlowFile attributes, so there is no content-parsing cost.

1. Add a `RouteOnAttribute` processor.
2. Add dynamic properties whose values are Expression Language conditions. Each becomes a relationship.
3. Connect the desired relationship to the next step. Connect `unmatched` to auto-terminate (to drop) or to the Output Port (to keep).

**By content (requires ser/de).** Use `QueryRecord` with a SQL `WHERE` clause.

| Property | Value |
| --- | --- |
| Record Reader | The existing `JsonTreeReader`. |
| Record Writer | The existing `JsonRecordSetWriter`. |
| `filtered` *(dynamic)* | `SELECT * FROM FLOWFILE WHERE <condition>` |

Expand

Show lessSee more

Route the `filtered` relationship to the next step, and auto-terminate `original`.

### Pattern: Mapping / field transformations

Use `JoltTransformRecord` (record-aware) for flatten / rename / remove / default operations.

| Property | Value |
| --- | --- |
| Record Reader | The existing `JsonTreeReader`. |
| Record Writer | The existing `JsonRecordSetWriter`. |
| Jolt Transform | `jolt-transform-chain` |
| Jolt Specification | A Chain spec (see below). |

Expand

Show lessSee more

Combine operations in one Chain spec to keep it to a single ser/de pass:

Copy code

```
[
  {"operation": "default", "spec": {"fieldName": "defaultValue"}},
  {"operation": "shift",   "spec": {"oldName": "newName", "*": "&"}},
  {"operation": "remove",  "spec": {"unwantedField": ""}}
]
```

Note

**Use `JoltTransformRecord`, not `JoltTransformJSON`.** `JoltTransformRecord` is record-aware and processes NDJSON correctly using the configured RecordReader/RecordWriter. **Do NOT use `JoltTransformJSON`** — it treats the entire FlowFile as a single JSON document and fails with NDJSON input.

For simpler operations (add/rename/remove fields, set defaults), `UpdateRecord` with RecordPath expressions is a straightforward alternative to Jolt spec syntax. For content-based filtering, `QueryRecord` (SQL `WHERE`) is the alternative.

### Pattern: Topic-to-table mapping

Route messages to different Snowflake tables based on the Kafka topic (or, for Kinesis, the source stream). `ConsumeKafka` sets the `kafka.topic` attribute automatically, and `ConsumeKinesis` sets `aws.kinesis.stream.name`, so this is attribute-only (no ser/de). The steps below use `kafka.topic` — for Kinesis, substitute `aws.kinesis.stream.name`.

1. Add an `UpdateAttribute` processor with a dynamic property:

| Property | Value |
| --- | --- |
| `table.name` | Kafka: `${kafka.topic:replaceByPattern(#{'Topic To Table Map'})}` Kinesis: `${aws.kinesis.stream.name:replaceByPattern(#{'Topic To Table Map'})}` |

Expand

Show lessSee more

2. Add a `Topic To Table Map` parameter to the connector’s parameter context. Format: `topic:table` pairs separated by commas. Table names must be valid unquoted Snowflake identifiers. Regex patterns must map a topic to a single table. If empty or no match, the topic name is used as the table name.

   - Explicit: `topic1:low_range,topic2:low_range,topic5:high_range`
   - Regex: `topic[0-4]:low_range,topic[5-9]:high_range`
3. Update `PublishSnowpipeStreaming`:

| Property | Value |
| --- | --- |
| Table | `${table.name}` |

Expand

Show lessSee more

### Pattern: Default values for null / empty fields

Use `JoltTransformRecord` with a `default` operation (preferably combined into the Chain spec above), or `UpdateRecord` with RecordPath:

| Property | Value |
| --- | --- |
| Record Reader | The existing `JsonTreeReader`. |
| Record Writer | The existing `JsonRecordSetWriter`. |
| Replacement Value Strategy | `record-path-value` |
| `/field_name` *(dynamic)* | `replaceNull(/field_name, 'default_value')` |

Expand

Show lessSee more

### Pattern: Content-based routing to multiple tables

Route records to different tables based on a field value in the message content.

**A single FlowFile can contain records with different routing-field values, so `PartitionRecord` is always required** — there is no shortcut.

**Step 1 — `PartitionRecord`** splits by the routing field and sets the value as a FlowFile attribute:

| Property | Value |
| --- | --- |
| Record Reader | The existing `JsonTreeReader`. |
| Record Writer | The existing `JsonRecordSetWriter`. |
| `<routing-field-name>` *(dynamic)* | `/routing_field` |

Expand

Show lessSee more

**Step 2 (optional) — `UpdateAttribute`** to map the attribute to a table name, only if they differ:

| Property | Value |
| --- | --- |
| `table.name` | `${<routing-field-attribute>}` |

Expand

Show lessSee more

If the attribute value *is* the table name, skip this and point `PublishSnowpipeStreaming` directly at the attribute.

**Step 3 (optional) — `RouteOnAttribute`** only if you must drop unwanted values:

| Property | Value |
| --- | --- |
| `matched` *(dynamic)* | `${table.name:isEmpty():not()}` |

Expand

Show lessSee more

Records that satisfy the expression flow to the `matched` relationship; connect it to the Output Port. Everything else falls to the built-in `unmatched` relationship — auto-terminate it to drop those records.

**Step 4 — `PublishSnowpipeStreaming`:** set **Table** = `${table.name}` (or the routing attribute directly). `PublishSnowpipeStreaming` writes each FlowFile to whatever table the attribute resolves to.

Note

**Dynamic database and schema too.** `PublishSnowpipeStreaming` supports Expression Language (FlowFile attributes) on its **Database**, **Schema**, **Table**, and **Pipe** properties — not just **Table**. So you can route to a fully dynamic destination by setting, for example, **Database** = `${target.db}`, **Schema** = `${target.schema}`, and **Table** = `${table.name}`, where each attribute is set upstream by `UpdateAttribute` / `PartitionRecord`. Each evaluates per FlowFile, so a single processor can fan out across databases, schemas, and tables.

| Need | Pipeline |
| --- | --- |
| Route to multiple tables (all values valid) | `PartitionRecord` -> Output Port, with `PublishSnowpipeStreaming` **Table** = `${field}` |
| Route to multiple tables + rename attribute | `PartitionRecord` -> `UpdateAttribute` -> Output Port |
| Route to multiple tables + drop some values | `PartitionRecord` -> `UpdateAttribute` -> `RouteOnAttribute` -> Output Port |

Expand

Show lessSee more

Set FIFO on all connections.

### Pattern: Custom Groovy script (catch-all)

Use `ExecuteGroovyScript` for anything that does not fit the patterns above. All restriction rules still apply: FIFO on connections, one table per output FlowFile, and preserved ordering.

Warning

**Preserve original attributes.** The script MUST NOT remove or overwrite incoming attributes. For Kafka these include `kafka.topic` and `kafka.partition`. For Kinesis these include `aws.kinesis.stream.name` and `aws.kinesis.shard.id`. These are used in `PublishSnowpipeStreaming` channel names and must be preserved — the connectors provide at-least-once delivery and do not track offsets. When emitting output FlowFiles, always inherit attributes from the incoming FlowFile.

Validate the script against edge cases (nulls, missing fields, type mismatches) before enabling the flow.

## Combining transformations

Chain multiple processors inside the group:

```
Input Port -> Processor A -> Processor B -> ... -> Output Port
```

- **Order:** place attribute-only processors (no ser/de) *before* content-aware ones, so unwanted data is dropped early and costly ser/de runs only on records that will actually be written.
- **Minimize ser/de:** combine content operations into a single processor where possible (one `QueryRecord` or one chained `JoltTransformRecord`). Keep `PartitionRecord` separate — it changes FlowFile boundaries.
- **Connections:** FIFO on all. Route failures to auto-terminate or a dead-letter output.

## Parameterization

After wiring the transformations, move suitable hardcoded values into the connector’s parameter context so the flow can be reconfigured without editing processors.

Good candidates: connection strings / URLs, topic-to-table mappings, credentials, thresholds and constants.

Not suitable (keep inline): Groovy scripts, Jolt specs, filter/routing conditions, large schema definitions.

## Verification

After creating all processors, wiring all connections, and updating `PublishSnowpipeStreaming`:

1. **Enable all controller services first.** Processors that reference a disabled service show as INVALID, so enable every service before validating.
2. Validate the process group and resolve any validation failures.
3. Confirm `PublishSnowpipeStreaming` references the correct **Table** value (for example, `${table.name}`).
4. Start the flow.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Data loss or duplicate data | FIFO prioritizer missing on a connection. |
| Out-of-order delivery | Missing FIFO prioritizer on a connection between processors. |
| Processor shows INVALID | A referenced controller service is disabled, or a required property is missing — enable services first, then re-validate. |
| Records written to the wrong table | `PublishSnowpipeStreaming` **Table** not set to the routing attribute, or `PartitionRecord` / `UpdateAttribute` not setting the expected attribute. |
| Schema re-inferred on every message (slow) | `VolatileSchemaCache` not configured on the `JsonTreeReader` (see [Reader and writer setup](#label-openflow-streaming-custom-transformations-reader-writer)). |
| Lost `kafka.*` attributes after a Groovy step | The script created new FlowFiles without inheriting the incoming attributes. |

Expand

Show lessSee more

## See also

- [Configuring Avro data type ingestion](configuring-avro-data-type-ingestion) — JSON to Avro switching
- [Configuring Protobuf data type ingestion](configuring-protobuf-data-type-ingestion) — JSON to Protobuf switching
- [Configuring Dead Letter Queue (DLQ) handling](configuring-dead-letter-queue-handling) — routing failed records to a destination
