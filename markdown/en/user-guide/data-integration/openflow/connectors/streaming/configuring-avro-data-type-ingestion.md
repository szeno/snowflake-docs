Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Configuring Avro data type ingestion

The streaming connectors (Kafka high-performance, Kinesis high-performance) use a `Consume*` processor (`ConsumeKafka` / `ConsumeKinesis`) with a `JsonTreeReader` controller service to parse incoming messages. This topic describes how to switch to Avro-encoded messages by replacing `JsonTreeReader` with an `AvroReader`. The steps are identical for both connectors — on a Kinesis connector, use the `ConsumeKinesis` processor where `ConsumeKafka` is referenced.

Tip

You don’t have to apply this customization by hand. The **Openflow skill in Snowflake CoCo** can perform it for you — describe the change you want and it edits the flow following the steps on this page. We recommend using the skill instead of configuring the components manually.

The following schema access strategies are supported:

- **Inline schema text** — you provide the Avro schema directly in the service configuration.
- **Embedded Avro schema** — the schema is read from the Avro container file header, no external configuration needed.
- **Confluent Schema Registry** — the schema ID is read from the message using `ConfluentEncodedSchemaReferenceReader` and resolved against a `ConfluentSchemaRegistry`.
- **AWS Glue Schema Registry** — schemas are looked up by name in the AWS Glue Schema Registry (`AmazonGlueSchemaRegistry`), commonly used by **Amazon MSK** customers.

## Prerequisites

- You have an existing **Kafka high-performance** or **Kinesis high-performance** connector deployed in Openflow.
- Your Kafka topics / Kinesis stream produce **Avro-encoded messages**.
- If using Confluent Schema Registry: you have the registry URL and network access to it from the Openflow runtime. For Snowflake-managed deployments (SPCS), a proper [External Access Integration](/developer-guide/external-network-access/external-network-access-overview) must be configured and assigned to the runtime to allow outbound connections to the registry.

## Configure Avro data type ingestion

The steps below apply identically to the **Kafka high-performance** and **Kinesis high-performance** connectors (on a Kinesis connector, use the `ConsumeKinesis` processor where `ConsumeKafka` is referenced).

### Step 1: Create the AvroReader controller service

1. Open the connector’s process group in the Openflow UI.
2. Go to **Configure** > **Controller Services** (gear icon).
3. Select **+** to add a new controller service.
4. Search for and select `AvroReader` (`org.apache.nifi.avro.AvroReader`).
5. Select **Add**.

The following properties are present on `AvroReader` regardless of the schema access strategy chosen in Step 2:

| Property | Description |
| --- | --- |
| Fast Reader Enabled | When enabled, uses an optimized reader that improves performance but increases memory usage. Disable if `OutOfMemoryError` occurs during Avro processing. |
| Cache Size | Number of schemas to cache in memory. The default is fine for a few schemas; if a single topic/stream carries **many different schemas** at high throughput, raise it so schemas are not evicted and re-fetched repeatedly — at the cost of higher memory consumption. |

Expand

Show lessSee more

### Step 2: Configure the schema access strategy in AvroReader

In the `AvroReader` controller service created in Step 1, configure the schema access strategy. Choose the option that matches how your Avro schema is distributed.

#### Option A — Inline schema text (Use ‘Schema Text’ Property)

Use this when you have the Avro schema as a text string and it does not change at runtime.

1. Select the **Edit** (gear) icon on the `AvroReader` service.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Schema Access Strategy | `Use 'Schema Text' Property` |
| Schema Text | The full Avro-formatted schema text. Supports Expression Language. |

Expand

Show lessSee more

3. Select **Apply**.

#### Option B — Embedded Avro schema (Use Embedded Avro Schema)

Use this when messages are serialized as Avro Object Container Files (OCF), which include the writer schema in the file header. No additional services are required.

1. Select the **Edit** (gear) icon on the `AvroReader` service.
2. Set the following property:

| Property | Value |
| --- | --- |
| Schema Access Strategy | `Use Embedded Avro Schema` |

Expand

Show lessSee more

3. Select **Apply**.

Note

This strategy only works with self-contained Avro container files. If your Kafka messages are raw Avro-encoded records without a file header (which is the common case for Kafka producers), use Option A or Option C instead.

#### Option C — Confluent Schema Registry (Schema Reference Reader)

Use this when messages are encoded with the Confluent wire format (magic byte `0x00` followed by a 4-byte schema ID). Two additional controller services are required: `ConfluentSchemaRegistry` resolves the schema ID to an actual schema, and `ConfluentEncodedSchemaReferenceReader` reads the schema ID from each message.

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
| Cache Size *(required)* | Number of schemas to cache locally. Raise it when a single topic/stream carries many distinct schemas at high throughput (more memory); the default is fine for a few schemas. |
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

**Configure AvroReader to use the schema reference reader:**

1. Select the **Edit** (gear) icon on the `AvroReader` service created in Step 1.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Schema Access Strategy | `Schema Reference Reader` |
| Schema Reference Reader | Select the `ConfluentEncodedSchemaReferenceReader` created above. |
| Schema Registry | Select the `ConfluentSchemaRegistry` created above. |

Expand

Show lessSee more

3. Select **Apply**.

#### Option D — AWS Glue Schema Registry (Schema Name)

Use this when an **Amazon MSK** producer registers Avro schemas in the AWS Glue Schema Registry. One additional controller service is required: `AmazonGlueSchemaRegistry` resolves schemas **by name**.

**Create the AmazonGlueSchemaRegistry controller service:**

1. Go to **Configure** > **Controller Services**.
2. Select **+** and search for `AmazonGlueSchemaRegistry`.
3. Select **Add**.
4. Select the **Edit** (gear) icon and set the following properties:

| Property | Value |
| --- | --- |
| Schema Registry Name *(required)* | The name of your Glue Schema Registry. |
| Region *(required)* | The AWS region of the registry, for example, `us-west-2`. |
| AWS Credentials Provider Service | Reuse the connector’s `AWSCredentialsProviderControllerService` (Kinesis), or create one for MSK. |
| Cache Size *(required)* | Number of schemas to cache locally. Raise for many distinct schemas at high throughput (more memory); the default is fine otherwise. |
| Cache Expiration *(required)* | How long cached schemas are valid before being re-fetched. |

Expand

Show lessSee more

5. Select **Apply**, then **Enable** the service.

**Create the AmazonGlueEncodedSchemaReferenceReader controller service:**

1. Go to **Configure** > **Controller Services**.
2. Select **+** and search for `AmazonGlueEncodedSchemaReferenceReader`.
3. Select **Add**.
4. Select the **Enable** icon and wait until the status shows **Enabled**.

Note

`AmazonGlueEncodedSchemaReferenceReader` reads the AWS Glue schema reference (UUID and version number) embedded in each message by the Glue Schema Registry serializer. It has no configurable properties.

**Configure AvroReader to use the schema reference reader:**

1. Select the **Edit** (gear) icon on the `AvroReader` service created in Step 1.
2. Set the following properties:

| Property | Value |
| --- | --- |
| Schema Access Strategy | `Schema Reference Reader` |
| Schema Reference Reader | Select the `AmazonGlueEncodedSchemaReferenceReader` created above. |
| Schema Registry | Select the `AmazonGlueSchemaRegistry` created above. |

Expand

Show lessSee more

3. Select **Apply**.

### Step 3: Enable the AvroReader controller service

Select the **Enable** (lightning bolt) icon on `AvroReader` and wait until its status shows **Enabled**.

### Step 4: Update the source processor

1. Double-click the `ConsumeKafka` processor (or `ConsumeKinesis` on a Kinesis connector) to open its properties.
2. Update the following property:

| Property | Value |
| --- | --- |
| Record Reader | Select the `AvroReader` created above. |

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
| `InvalidAvroSchemaException` or parse failures | The **Schema Text** does not match the actual message schema. Compare the schema in the service with the one used by the producer. Failed messages are routed to the parse-failure relationship (`parse failure` on Kafka, `parse.failure` on Kinesis). |
| `ConfluentSchemaRegistry` fails to enable | Network connectivity issue between the Openflow runtime and the registry. Check the External Access Integration and that the registry URL is reachable from the cluster. |
| Authentication failure against registry | Registry requires Basic auth — set **Authentication Type** to `BASIC` and provide **Username** and **Password** in `ConfluentSchemaRegistry`. |

Expand

Show lessSee more
