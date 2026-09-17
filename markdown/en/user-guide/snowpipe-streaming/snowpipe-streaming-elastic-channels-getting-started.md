# Tutorial: Get started with Elastic Channels (SDK)

This tutorial walks through setting up and running a producer application using the Snowpipe Streaming SDK with an Elastic Channel. Elastic Channels are the recommended starting point for most new applications because Snowflake manages the channel lifecycle and scaling.

Use a [Named Channel](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-channels) instead when your application requires ordered ingestion or exactly-once recovery. Exactly-once recovery requires records retained in the source or durable application-managed storage for replay.

## Prerequisites

- Snowflake account with access to a user with sufficient privileges to create roles, databases, and tables.
- Outbound network access from your producer host to Snowflake and to the Snowflake-provided cloud storage endpoints used for SDK file uploads (AWS S3, Google Cloud Storage, or Azure Blob Storage, depending on your deployment).
- Java 11+, Python 3.9+, or Node.js 20+ depending on your chosen SDK.
- glibc version 2.26 or later on Linux.

Elastic Channels require SDK version 1.8.0 or later:

- Java: [Maven Central](https://central.sonatype.com/artifact/com.snowflake/snowpipe-streaming)
- Python: [PyPI](https://pypi.org/project/snowpipe-streaming/)
- Node.js: [npm](https://www.npmjs.com/package/snowpipe-streaming)

## Step 1: Configure Snowflake objects

### Generate a key pair for authentication

Generate a private-public key pair using OpenSSL. For more information, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Copy code

```
PUBK=$(cat ./rsa_key.pub | grep -v KEY- | tr -d '\012')
echo "ALTER USER MY_USER SET RSA_PUBLIC_KEY='$PUBK';"
```

Important

Save `rsa_key.p8` (private key) and `rsa_key.pub` (public key) securely. You will use the private key in subsequent steps.

### Create database, schema, table, and configure user authentication

Run the following SQL commands in your Snowflake account using Snowsight or the Snowflake CLI. Replace placeholders with your own values. For required privileges, see [Access control](/user-guide/snowpipe-streaming/snowpipe-streaming-access-control).

Copy code

```
-- Run the first two lines with a highly-privileged role (e.g., ACCOUNTADMIN)
CREATE OR REPLACE USER MY_USER;
CREATE ROLE IF NOT EXISTS MY_ROLE;
GRANT ROLE MY_ROLE TO USER MY_USER;

-- Set the public key for key-pair authentication
-- Replace 'YOUR_FORMATTED_PUBLIC_KEY' with the output from the key generation step.
ALTER USER MY_USER SET RSA_PUBLIC_KEY='YOUR_FORMATTED_PUBLIC_KEY';
ALTER USER MY_USER SET DEFAULT_ROLE=MY_ROLE;

-- Switch to the new role and create objects
USE ROLE MY_ROLE;
CREATE OR REPLACE DATABASE MY_DATABASE;
CREATE OR REPLACE SCHEMA MY_SCHEMA;

CREATE OR REPLACE TABLE MY_TABLE (
    data VARIANT,
    c1 NUMBER,
    c2 STRING
);
```

Note

The `data` column is a VARIANT type. Pass semi-structured data as a native object (Java `Map`, Python dict, or JavaScript object). Passing a raw JSON string stores the data as a string literal.

## Step 2: Configure an authentication profile

Create a `profile.json` file in the root directory of your project.

Copy code

```
{
    "user": "MY_USER",
    "account": "your_account_identifier",
    "url": "https://your_account_identifier.snowflakecomputing.com:443",
    "private_key_file": "rsa_key.p8",
    "role": "MY_ROLE"
}
```

Replace the placeholders:

- `MY_USER`: Your Snowflake username from Step 1.
- `your_account_identifier`: Your Snowflake account identifier (for example, `xy12345`).
- `rsa_key.p8`: The private key file generated in Step 1.
- `MY_ROLE`: The role you created in Step 1.

## Step 3: Add the SDK dependency

JavaPythonNode.js

**Download:** [Sample Java code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/java-example)

Add version 1.8.0 or later of the SDK to your Maven `pom.xml`. Check [Maven Central](https://central.sonatype.com/artifact/com.snowflake/snowpipe-streaming) for the latest version.

Copy code

```
<dependency>
    <groupId>com.snowflake</groupId>
    <artifactId>snowpipe-streaming</artifactId>
    <version>1.8.0</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.18.1</version>
</dependency>
```

**Download:** [Sample Python code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/python-example)

The SDK requires Python 3.9 or later.

Copy code

```
pip install "snowpipe-streaming>=1.8.0"
```

**Download:** [Sample Node.js code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/nodejs-example)

The SDK requires Node.js 20 or later.

Copy code

```
npm install snowpipe-streaming@^1.8.0
```

## Step 4: Append rows and wait for acknowledgement

The following examples create a table-mode client, get the implicit Elastic Channel, and append rows using an API that returns a Future or Promise. The returned `CompletableFuture` (Java), `Future` (Python), or `Promise` (Node.js) completes successfully when Snowflake durably acknowledges the append. An append token is required but can be `null` or `None`. It is an identifier returned in callbacks so you can match the result to your messages; it does not prevent duplicates.

Append events as they arrive; the SDK buffers and combines appends internally using time and size thresholds. The single-row example waits immediately to demonstrate acknowledgement. In production, retain a bounded set of Futures or Promises and periodically wait for all pending appends to be durably acknowledged rather than waiting after every row or collecting rows into another batch before submitting them. See [Bound outstanding acknowledgements](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#label-elastic-bound-acknowledgements).

JavaPythonNode.js

Copy code

```
ObjectMapper mapper = new ObjectMapper();
JsonNode profile = mapper.readTree(Files.readAllBytes(Paths.get("profile.json")));
Properties properties = new Properties();
profile.fields().forEachRemaining(
    entry -> properties.put(entry.getKey(), entry.getValue().asText()));

try (SnowflakeStreamingIngestClient client =
    SnowflakeStreamingIngestClientFactory.tableBuilder(
            "demo-client", "MY_DATABASE", "MY_SCHEMA", "MY_TABLE")
        .setProperties(properties)
        .build()) {
  SnowflakeStreamingIngestElasticChannel channel = client.getElasticChannel();

  Map<String, Object> row = Map.of(
      "DATA", Map.of("event_id", 1, "status", "active"),
      "C1", 1,
      "C2", "example");

  CompletableFuture<Void> ack = channel.appendRowWithWait(row, "batch-1");
  ack.get(); // blocks until durable acknowledgement or throws on failure

  // The successful completion above is the durable acknowledgement; status provides channel-health and row-error visibility.
  ChannelStatus status = channel.getChannelStatus();
}
```

Copy code

```
from snowflake.ingest.streaming import StreamingIngestClient

client = StreamingIngestClient.from_table(
    client_name="demo-client",
    db_name="MY_DATABASE",
    schema_name="MY_SCHEMA",
    table_name="MY_TABLE",
    profile_json="profile.json",
)
try:
    channel = client.get_elastic_channel()

    row = {
        "DATA": {"event_id": 1, "status": "active"},
        "C1": 1,
        "C2": "example",
    }
    future = channel.append_row_with_wait(row, "batch-1")
    future.result()  # blocks until durable acknowledgement or raises on failure

    # The successful completion above is the durable acknowledgement; status provides channel-health and row-error visibility.
    status = channel.get_channel_status()
finally:
    client.close(wait_for_flush=True, timeout_seconds=60)
```

Copy code

```
const { createTableClient } = require("snowpipe-streaming");

const client = await createTableClient({
  clientName: "demo-client",
  dbName: "MY_DATABASE",
  schemaName: "MY_SCHEMA",
  tableName: "MY_TABLE",
  profilePath: "profile.json",
});
try {
  const channel = await client.getElasticChannel();

  const row = {
    DATA: { event_id: 1, status: "active" },
    C1: 1,
    C2: "example",
  };
  await channel.appendRowWithWait(row, "batch-1");

  // The successful completion above is the durable acknowledgement; status provides channel-health and row-error visibility.
  const status = await channel.getChannelStatus();
} finally {
  await client.close({ waitForFlush: true, timeoutMs: 60000 });
}
```

The successfully completed Future or Promise indicates durable acknowledgement, not immediate table visibility. Synchronous validation, serialization, closed-client, and immediate backpressure failures are raised directly by the append call. Handle these at the call site.

Keep each event available until its acknowledgement succeeds, according to your delivery requirements. A caller wait timeout doesn’t mean the append failed; retain the original pending acknowledgement instead of immediately resubmitting. The SDK’s buffer isn’t persistent across process failure. For pausing intake, source replay, and producer-local retention options, see [Protect unacknowledged data](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#protect-unacknowledged-data).

## Step 5: Track acknowledgements with callbacks (optional)

As an alternative to tracking Futures or Promises, use `appendRow` or `appendRows` with registered success and error handlers. Both ways of tracking appends use the SDK’s automatic batching. Register handlers before the first append and use non-null append tokens so you can track outcomes. Limit how many appends are awaiting acknowledgement before submitting more.

JavaPythonNode.js

Copy code

```
SnowflakeStreamingIngestElasticChannel channel = client.getElasticChannel();

channel.setSuccessHandler(detail ->
    System.out.println("Acknowledged: " + detail.getAppendTokens()));
channel.setErrorHandler(detail ->
    System.err.println(
        "Failed: " + detail.getAppendTokens()
            + " cause: " + detail.getError()));

// Returns when the row is buffered locally; callbacks report the outcome
channel.appendRow(row, "batch-2");
// ... append more rows, then flush before shutdown
```

Copy code

```
channel = client.get_elastic_channel()

def on_success(detail):
    print("Acknowledged:", detail.append_tokens)

def on_error(detail):
    print("Failed:", detail.append_tokens, detail.error)

channel.set_success_handler(on_success)
channel.set_error_handler(on_error)

channel.append_row(row, "batch-2")
# ... append more rows, then flush before shutdown
```

Copy code

```
const channel = await client.getElasticChannel();

channel.setSuccessHandler((detail) =>
  console.log("Acknowledged:", detail.appendTokens));
channel.setErrorHandler((detail) =>
  console.error("Failed:", detail.appendTokens, detail.error));

channel.appendRow(row, "batch-2");
// ... append more rows, then flush before shutdown
```

Important

Keep callback bodies short. Callbacks run on the channel’s internal acknowledgement task. Delegate blocking I/O, retries, and reconciliation to your own queue or executor. A callback exception is caught and logged but does not replace checking Futures or Promises for appends that return them.

See the [Java](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/java-example), [Python](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/python-example), and [Node.js](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/nodejs-example) sample folders for producer examples. Use the [checkpoint guidance](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-operations#label-elastic-durability-checkpoints) and [error-handling guidance](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling) when adapting them to your source and delivery requirements.

## Step 6: Run the application

JavaPythonNode.js

Copy code

```
mvn clean install
mvn exec:java -Dexec.mainClass="com.snowflake.snowpipestreaming.demo.Main"
```

Copy code

```
python example.py
```

Copy code

```
node example.js
```

## Step 7: Verify the data

After the application runs, allow time for Snowflake to process and materialize the data, then query the target table.

Copy code

```
SELECT COUNT(*) FROM MY_DATABASE.MY_SCHEMA.MY_TABLE;
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE LIMIT 10;
```

If rows are missing from the target table after a durable acknowledgement, check the error table:

Copy code

```
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE__ERRORS LIMIT 20;
```

For more information on error tables, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Next steps

- [Best practices](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices): Automatic SDK batching, bounded acknowledgements, producer-side retention, and graceful shutdown.
- [Error handling](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling): Synchronous and asynchronous failures, retries, and duplicate handling.
- [Limitations](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-limitations): Request size, delivery guarantees, and SDK version requirements.
- [Costs](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-cost): Ingestion credit usage.
