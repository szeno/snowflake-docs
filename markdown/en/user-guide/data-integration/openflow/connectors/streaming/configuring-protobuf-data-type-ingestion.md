Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Configuring Protobuf data type ingestion

The streaming connectors (Kafka high-performance, Kinesis high-performance) use a `Consume*` processor (`ConsumeKafka` / `ConsumeKinesis`) with a `JsonTreeReader` controller service to parse incoming messages. This topic describes how to switch to Protobuf-encoded messages by replacing `JsonTreeReader` with a `StandardProtobufReader`. The steps are identical for both connectors — on a Kinesis connector, use the `ConsumeKinesis` processor where `ConsumeKafka` is referenced.

Tip

You don’t have to apply this customization by hand. The **Openflow skill in Snowflake CoCo** can perform it for you — describe the change you want and it edits the flow following the steps on this page. We recommend using the skill instead of configuring the components manually.

Note

AWS Glue Schema Registry is **not** supported for Protobuf in these connectors. Use inline schema text or Confluent Schema Registry below.

Three schema access strategies are supported:

- **Inline schema text** — you provide the Proto 3 schema directly in the service configuration.
- **Schema name** — the schema name is resolved against a configured `SchemaRegistry` service (for example, `ConfluentSchemaRegistry`).
- **Schema reference reader** — the schema ID is read from the message using `ConfluentEncodedSchemaReferenceReader` and resolved against a `ConfluentSchemaRegistry`. This is the standard strategy for Confluent wire-format encoded messages.

In addition, because a single `.proto` file can define multiple message types, you must also configure how the correct message name is resolved:

- **Message name property** — you specify the fully qualified message name (including package) directly as a parameter, for example, `mypackage.MyMessage`.
- **Message name resolver** — the message name is resolved dynamically from the FlowFile content or attributes using a `MessageNameResolver` service. `ConfluentProtobufMessageNameResolver` resolves the name by decoding message indexes from the Confluent wire format and looking up the fully qualified name in the schema definition.

## Prerequisites

- You have an existing **Kafka high-performance** or **Kinesis high-performance** connector deployed in Openflow.
- Your Kafka topics / Kinesis stream produce **Protobuf-encoded messages**.
- If using Confluent Schema Registry: you have the registry URL and network access to it from the Openflow runtime. For Snowflake-managed deployments (SPCS), a proper [External Access Integration](/developer-guide/external-network-access/external-network-access-overview) must be configured and assigned to the runtime to allow outbound connections to the registry.

## Configure Protobuf data type ingestion

The steps below apply identically to the **Kafka high-performance** and **Kinesis high-performance** connectors (on a Kinesis connector, use the `ConsumeKinesis` processor where `ConsumeKafka` is referenced).

### Step 1: Create the StandardProtobufReader controller service

1. Open the connector’s process group in the Openflow UI.
2. Go to **Configure** > **Controller Services** (gear icon).
3. Select **+** to add a new controller service.
4. Search for and select `StandardProtobufReader` (`org.apache.nifi.services.protobuf.StandardProtobufReader`).
5. Select **Add**.

### Step 2: Configure the schema access strategy in StandardProtobufReader

In the `StandardProtobufReader` controller service created in Step 1, configure the schema access strategy and the message name resolution strategy. Choose the combination that matches how your Protobuf schema and message type are distributed.

#### Option A — Inline schema text with message name property

Use this when you have the Proto 3 schema as a text string and the message name does not change at runtime.

1. Select the **Edit** (gear) icon on the `StandardProtobufReader` service.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Schema Access Strategy | `Use 'Schema Text' Property` |
| Schema Text | The full Proto 3 formatted schema text. Supports Expression Language. |
| Message Name Resolution Strategy | `Message Name Property` |
| Message Name | The fully qualified name of the Protocol Buffers message including its package, for example, `mypackage.MyMessage`. Supports Expression Language. |

Expand

Show lessSee more

3. Select **Apply**.

#### Option B — Confluent Schema Registry with Confluent message name resolver

Use this when messages are encoded with the Confluent wire format (magic byte `0x00` followed by a 4-byte schema ID) and the message name should be resolved automatically. Three additional controller services are required:

- `ConfluentSchemaRegistry` — resolves the schema ID to the actual Proto 3 schema.
- `ConfluentEncodedSchemaReferenceReader` — reads the schema ID from each message.
- `ConfluentProtobufMessageNameResolver` — resolves the message name by decoding message indexes from the Confluent wire format and looking up the fully qualified name in the schema definition.

**Create the ConfluentSchemaRegistry controller service:**

1. Go to **Configure** > **Controller Services**.
2. Select **+** and search for `ConfluentSchemaRegistry` (`org.apache.nifi.confluent.schemaregistry.ConfluentSchemaRegistry`).
3. Select **Add**.
4. Select the **Edit** (gear) icon and set the following properties:

| Property | Value |
| --- | --- |
| Schema Registry URLs *(required)* | Comma-separated URL(s) of your Confluent Schema Registry, for example, `https://schema-registry.example.com:8081`. |
| SSL Context Service | *(optional)* An `SSLContextService` if the registry requires TLS. Implementations: `StandardSSLContextService`, `StandardRestrictedSSLContextService`, `PEMEncodedSSLContextProvider`. |
| Communications Timeout *(required)* | How long to wait for a response from the registry before failing. |
| Cache Size *(required)* | Number of schemas to cache locally. Raise it when a single topic/stream carries many distinct Protobuf message types at high throughput (more memory); the default is fine for a few schemas. |
| Cache Expiration *(required)* | How long cached schemas are valid before being re-fetched. |
| Authentication Type | `NONE` or `BASIC` if the registry requires HTTP Basic authentication. |
| Username | Username for Basic authentication. Only used when **Authentication Type** is `BASIC`. |
| Password | Password for Basic authentication. Sensitive property. Only used when **Authentication Type** is `BASIC`. |

Expand

Show lessSee more

5. Select **Apply**.
6. Select the **Enable** (lightning bolt) icon and wait until the status shows **Enabled**.

**Create the ConfluentEncodedSchemaReferenceReader controller service:**

1. Go to **Configure** > **Controller Services**.
2. Select **+** and search for `ConfluentEncodedSchemaReferenceReader` (`org.apache.nifi.confluent.schemaregistry.ConfluentEncodedSchemaReferenceReader`).
3. Select **Add**.
4. Select the **Enable** icon and wait until the status shows **Enabled**.

Note

`ConfluentEncodedSchemaReferenceReader` has no configurable properties. It simply reads the Confluent-encoded schema ID (magic byte `0x00` + 4-byte integer) from the beginning of each message.

**Create the ConfluentProtobufMessageNameResolver controller service:**

1. Go to **Configure** > **Controller Services**.
2. Select **+** and search for `ConfluentProtobufMessageNameResolver` (`org.apache.nifi.confluent.schemaregistry.ConfluentProtobufMessageNameResolver`).
3. Select **Add**.
4. Select the **Enable** icon and wait until the status shows **Enabled**.

Note

`ConfluentProtobufMessageNameResolver` has no configurable properties. It decodes the message index sequence embedded in the Confluent Protobuf wire format to determine the fully qualified message name. For details on the wire format, see the [Confluent Schema Registry documentation](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html#wire-format).

**Configure StandardProtobufReader to use the schema reference reader and message name resolver:**

1. Select the **Edit** (gear) icon on the `StandardProtobufReader` service created in Step 1.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Schema Access Strategy | `Schema Reference Reader` |
| Schema Reference Reader | Select the `ConfluentEncodedSchemaReferenceReader` created above. |
| Schema Registry | Select the `ConfluentSchemaRegistry` created above. |
| Message Name Resolution Strategy | `Message Name Resolver` |
| Message Name Resolver | Select the `ConfluentProtobufMessageNameResolver` created above. |

Expand

Show lessSee more

3. Select **Apply**.

### Step 3: Enable the StandardProtobufReader controller service

Select the **Enable** (lightning bolt) icon on `StandardProtobufReader` and wait until its status shows **Enabled**.

### Step 4: Update the source processor

1. Double-click the `ConsumeKafka` processor (or `ConsumeKinesis` on a Kinesis connector) to open its properties.
2. Update the following property:

| Property | Value |
| --- | --- |
| Record Reader | Select the `StandardProtobufReader` created above. |

Expand

Show lessSee more

3. Select **Apply**.

### Step 5: Disable the JsonTreeReader controller service

The original `JsonTreeReader` is no longer needed.

1. Stop the process group if it is running.
2. Go to **Configure** > **Controller Services**.
3. Select the **Disable** icon on `JsonTreeReader`.
4. If the service is not referenced by any other processor, you can also delete it by selecting the **Delete** (trash) icon.
5. Start the process group.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `SchemaNotFoundException` at runtime | The schema ID in the message is not present in the registry, or the registry URL is misconfigured. Verify **Schema Registry URLs** in `ConfluentSchemaRegistry`. |
| Parse failures or malformed records | The **Schema Text** does not match the actual message schema, or the wrong **Message Name** is specified. Compare the schema and message name with those used by the producer. Failed messages are routed to the parse-failure relationship (`parse failure` on Kafka, `parse.failure` on Kinesis). |
| `ConfluentSchemaRegistry` fails to enable | Network connectivity issue between the Openflow runtime and the registry. Check the External Access Integration and that the registry URL is reachable from the cluster. |
| Authentication failure against registry | Registry requires Basic auth — set **Authentication Type** to `BASIC` and provide **Username** and **Password** in `ConfluentSchemaRegistry`. |

Expand

Show lessSee more
