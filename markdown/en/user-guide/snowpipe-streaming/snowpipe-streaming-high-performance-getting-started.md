# Tutorial: Get started with Named Channels using the SDK

This tutorial provides step-by-step instructions for setting up and running a Named Channel demo application with the `snowpipe-streaming` SDK. Named Channels provide ordered, exactly-once ingestion. Exactly-once recovery requires records retained in the source or durable application-managed storage for replay.

For Elastic Channels (the recommended starting point for most new applications), see [Tutorial: Get started with Elastic Channels (SDK)](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-getting-started).

## Prerequisites

Before you run the demo, ensure that you meet the following prerequisites:

- Snowflake account: Verify that you have access to a Snowflake account. You will need a user with sufficient privileges (e.g., ACCOUNTADMIN or USERADMIN for the initial setup) to create the dedicated user and custom role detailed in [Step 1: Configure Snowflake objects](#label-snowpipe-streaming-high-performance-demo-project-step-1).
- Network access: Ensure that your network allows outbound connectivity to Snowflake and Amazon S3 or Google Cloud Platform (GCS) or Azure Blob Storage. Adjust firewall rules if necessary because the SDK makes REST API calls to Snowflake and to your cloud storage provider.

  - To verify network connectivity, use the following command:

  Copy code

  ```
  # Test connectivity to Snowflake; replace with your account URL
  curl -I https://<your_account_identifier>.snowflakecomputing.com

  # Test connectivity to AWS S3
  curl -I https://s3.amazonaws.com

  # Test connectivity to GCS
  curl -I https://storage.googleapis.com

  # Test connectivity to Azure Blob Storage
  curl -I https://azure.blob.core.windows.net  or curl -I https://<your_account_name>.blob.core.windows.net
  ```
- Java Development Environment: Install Java 11 or later, and Maven for dependency management.
- Python: Install Python version 3.9 or later.
- Node.js: Install Node.js version 20 or later.
- System requirements: The SDK requires glibc version 2.26 or later. You can check your current glibc version with:

  Copy code

  ```
  ldd --version
  ```
- Snowpipe Streaming SDKs and the sample code:

  Download the sample code for your preferred language from the [Snowpipe Streaming SDK examples in the GitHub repository](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples).

## Prerequisites and setup

The following steps configure the Snowflake objects, authentication, and SDK dependency required for Named Channel ingestion.

### Step 1: Configure Snowflake objects

Before you can use the `snowpipe-streaming` SDK, you must create a target table within your Snowflake environment. Unlike the classic architecture, the high-performance architecture requires a PIPE object for data ingestion. This tutorial uses the default pipe that is automatically created at ingest time for your target table. If you require additional features, such as in-flight transformations or clustering at ingest time, see [CREATE PIPE](/sql-reference/sql/create-pipe).

#### Generate a key pair for authentication

Generate a private-public key pair for authentication using OpenSSL. For more information, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

Run the following commands in your terminal to generate the keys:

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

Save the generated `rsa_key.p8` (private key) and `rsa_key.pub` (public key) files securely. You will use these keys in subsequent authentication steps.

#### Create database, schema, table, and configure user authentication

Run the following SQL commands in your Snowflake account; for example, by using Snowsight or Snowflake CLI). You must have a role with permissions to create users, roles, and databases — such as ACCOUNTADMIN or USERADMIN for the first few lines, and then switching to the new role. Replace placeholders like MY\_USER, MY\_ROLE, MY\_DATABASE, and so on, with the names that you want.

Copy code

```
-- 1. Create a dedicated role and user (Run with a highly-privileged role)
CREATE OR REPLACE USER MY_USER;
CREATE ROLE IF NOT EXISTS MY_ROLE;
GRANT ROLE MY_ROLE TO USER MY_USER;

-- 2. Set the public key for key-pair authentication
-- NOTE: Replace 'YOUR_FORMATTED_PUBLIC_KEY' with the output of the PUBK variable from the key generation step.
ALTER USER MY_USER SET RSA_PUBLIC_KEY='YOUR_FORMATTED_PUBLIC_KEY';

-- 3. Set the default role (Recommended)
ALTER USER MY_USER SET DEFAULT_ROLE=MY_ROLE;

-- 4. Switch to the new role and create objects
USE ROLE MY_ROLE;
-- NOTE: You may also need to run USE WAREHOUSE YOUR_WH; here if a default warehouse isn't set.

-- Create database and schema
CREATE OR REPLACE DATABASE MY_DATABASE;
CREATE OR REPLACE SCHEMA MY_SCHEMA;

-- Create a target table
CREATE OR REPLACE TABLE MY_TABLE (
    data VARIANT,
    c1 NUMBER,
    c2 STRING
);

-- 5. Configure authentication policy (Optional, but recommended for explicit control)
CREATE OR REPLACE AUTHENTICATION POLICY testing_auth_policy
  AUTHENTICATION_METHODS = ('KEYPAIR')
  CLIENT_TYPES = ('DRIVERS');

-- Apply authentication policy (if created)
ALTER USER MY_USER SET AUTHENTICATION POLICY testing_auth_policy;
```

Note

The `data` column in the sample table is a VARIANT type. The high-performance SDK requires that data for this column be passed as a native object; for example, a Java `Map`, Python dictionary, or JavaScript object. Passing a raw JSON string results in the data being stored as a string literal.

### Step 2: Configure an authentication profile

The demo application requires a `profile.json` file to store connection settings, including authentication details. The SDK uses key-pair authentication for secure connections.

#### Create a profile configuration file

Create or update the `profile.json` file in the root directory of your demo project.

#### profile.json template

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

- `MY_USER`: Your Snowflake username configured in [Step 1: Configure Snowflake objects](#label-snowpipe-streaming-high-performance-demo-project-step-1).
- `your_account_identifier`: Your Snowflake account identifier (for example, `xy12345`).
- `rsa_key.p8`: The private key file you generated in [Step 1: Configure Snowflake objects](#label-snowpipe-streaming-high-performance-demo-project-step-1).
- `MY_ROLE`: The dedicated role (`MY_ROLE`) you created and granted to the user in [Step 1: Configure Snowflake objects](#label-snowpipe-streaming-high-performance-demo-project-step-1).

### Step 3: Set up the demo project

JavaPythonNode.js

**Download:** [Sample Java code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/java-example)

**Add the JAR dependency**

To include the Snowpipe Streaming SDK, add the following dependency to your Maven `pom.xml`. Maven automatically downloads the JAR from the public repository.

Copy code

```
<dependency>
    <groupId>com.snowflake</groupId>
    <artifactId>snowpipe-streaming</artifactId>
    <version>YOUR_SDK_VERSION</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.18.1</version>
</dependency>
```

Important

Replace `YOUR_SDK_VERSION` with the specific version available on [Maven Central](https://central.sonatype.com/artifact/com.snowflake/snowpipe-streaming).

**Download:** [Sample Python code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/python-example)

**Add the Python dependency**

The SDK requires Python version 3.9 or later.

To install the Snowpipe Streaming SDK for Python, run the following command:

Copy code

```
pip install snowpipe-streaming
```

For more information about the package, see [PyPI](https://pypi.org/project/snowpipe-streaming/).

**Download:** [Sample Node.js code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/nodejs-example)

**Add the Node.js dependency**

The SDK requires Node.js version 20 or later.

To install the Snowpipe Streaming SDK for Node.js, run the following command:

Copy code

```
npm install snowpipe-streaming
```

For more information about the package, see [npm](https://www.npmjs.com/package/snowpipe-streaming).

#### Place the profile file

Ensure that the `profile.json` file that you configured in [Step 2: Configure an authentication profile](#label-snowpipe-streaming-high-performance-demo-project-step-2) is located in the root directory of your project.

## Open and use a Named Channel

Use a Named Channel when your application requires ordering within a channel or exactly-once recovery. Complete Steps 1 through 3 in [Prerequisites and setup](#named-channel-sdk-setup) before running the following code.

The examples open `MY_CHANNEL` with an initial offset token, asynchronously append three rows with offset tokens `1`, `2`, and `3` without waiting on each individual append, retrieve channel status, then wait once for offset token `3` to commit before closing.

Append rows as they arrive; the SDK combines appends internally using time and size thresholds. Submit rows serially in source order within each Named Channel, but don’t wait for every row to commit. Bound outstanding work and checkpoint periodically without collecting rows into another batch before submitting them.

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
  SnowflakeStreamingIngestChannel channel =
      client.openChannel("MY_CHANNEL", "0").getChannel();

  Map<String, Object> row1 = Map.of("DATA", Map.of("event_id", 1, "status", "active"), "C1", 1, "C2", "example");
  Map<String, Object> row2 = Map.of("DATA", Map.of("event_id", 2, "status", "active"), "C1", 2, "C2", "example");
  Map<String, Object> row3 = Map.of("DATA", Map.of("event_id", 3, "status", "active"), "C1", 3, "C2", "example");

  channel.appendRow(row1, "1");
  channel.appendRow(row2, "2");
  channel.appendRow(row3, "3");

  ChannelStatus status = channel.getChannelStatus();

  // Wait until offset 3 or a later offset is committed.
  channel.waitForCommit(
      token -> token != null && Long.parseLong(token) >= 3,
      Duration.ofMinutes(1)).get();
  channel.close();
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
channel, status = client.open_channel("MY_CHANNEL", "0")

def make_row(event_id):
    return {
        "DATA": {"event_id": event_id, "status": "active"},
        "C1": event_id,
        "C2": "example",
    }

channel.append_row(make_row(1), "1")
channel.append_row(make_row(2), "2")
channel.append_row(make_row(3), "3")

status = channel.get_channel_status()

# Wait until offset 3 or a later offset is committed.
channel.wait_for_commit(
    lambda token: token is not None and int(token) >= 3,
    timeout_seconds=60,
)
channel.close()
client.close()
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
const { channel } = await client.openChannel({
  name: "MY_CHANNEL",
  offsetToken: "0",
});

const makeRow = (eventId) => ({
  DATA: { event_id: eventId, status: "active" },
  C1: eventId,
  C2: "example",
});

channel.appendRow(makeRow(1), "1");
channel.appendRow(makeRow(2), "2");
channel.appendRow(makeRow(3), "3");

const status = await channel.getChannelStatus();

// Wait until offset 3 or a later offset is committed.
await channel.waitForCommit(
  (token) => token !== null && Number(token) >= 3,
  { timeoutMs: 60000 },
);
await channel.close();
await client.close();
```

Important

Don’t call `waitForCommit` after every row or small batch. Waiting on every append serializes ingestion around commit latency and defeats the purpose of asynchronous appends. `waitForCommit` polls channel status until the target offset commits, so reserve it for checkpoints, source handoffs, or graceful shutdown.

See the full [Java](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/java-example), [Python](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/python-example), and [Node.js](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/nodejs-example) samples for complete examples.

Run the application, then query the target table to verify the rows. In a production application, retrieve the latest committed offset when you open the Named Channel and resume the source from the next record. For more information, see [Offset tokens and exactly-once delivery](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-offset-tokens).
