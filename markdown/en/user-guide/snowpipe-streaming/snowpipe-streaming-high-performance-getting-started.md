# Tutorial: Get started with Named Channels using the SDK

This tutorial provides step-by-step instructions for setting up and running a Named Channel demo application with the `snowpipe-streaming` SDK. Named Channels provide ordered, exactly-once ingestion. Exactly-once recovery requires records retained in the source or durable application-managed storage for replay.

For Elastic Channels (the recommended starting point for most new applications), see [Tutorial: Get started with Elastic Channels (SDK)](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-getting-started).

## Prerequisites

Before you run the demo, ensure that you meet the following prerequisites:

- Snowflake account: Verify that you have access to a Snowflake account. You will need a user with sufficient privileges (e.g., ACCOUNTADMIN or USERADMIN for the initial setup) to create the dedicated user and custom role detailed in [Step 1: Configure Snowflake objects](#label-snowpipe-streaming-high-performance-demo-project-step-1).
- Network access: Complete the [network connectivity prerequisites](/user-guide/snowpipe-streaming/snowpipe-streaming-network-connectivity) from your producer runtime. Verify the account endpoint, discovered ingest endpoint, and cloud-storage upload destinations. Private connectivity also requires DNS configuration for the ingest hostname.
- Java Development Environment: Install Java 11 or later, and Maven for dependency management.
- Python: Install Python version 3.9 or later.
- C++: Install a C++ compiler that supports C++17 or later.
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

-- 3. Set the default role (Optional: you can instead specify a non-default role in your client configuration)
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

The `data` column in the sample table is a VARIANT, so pass its value as an object, not a JSON-encoded string, which is stored as a plain string. In Java, Python, and Node.js, use a native object (Java `Map`, Python `dict`, or JavaScript object). In C++, where each row is a JSON string, write `data` as a nested JSON object, for example `{"DATA": {"event_id": 1}}`.

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

JavaPythonC++Node.js

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

**Download:** [Sample C++ code](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/cpp-example)

**Add the C++ dependency**

The SDK requires C++ version 17 or later.

Download the C++ Snowpipe Streaming SDK from the [Snowflake Client Repository](https://sfc-repo.snowflakecomputing.com/snowpipe-streaming-cpp/index.html).

Each package in the repository has a matching `.sha256` checksum file and `.asc` signature file. The following commands download all three files into the current directory, then validate and unpack the package. Set `SDK_VERSION` to the version you want, `PLATFORM` to your package’s platform, and `PLATFORM_DIR` to the matching repository directory:

| `PLATFORM` | `PLATFORM_DIR` |
| --- | --- |
| `Linux-x86_64` | `linux_x86_64` |
| `Linux-aarch64` | `linux_aarch64` |
| `Darwin-arm64` | `macos_arm64` |

Expand

Show lessSee more

Set `GPG_KEY_ID` to the ID of the Snowflake public key that signed the package. Beginning with version 1.9.4, packages are signed with the Snowflake public key `3C98F63C9292CE02`.

Copy code

```
SDK_VERSION=1.9.4
PLATFORM=Linux-x86_64
PLATFORM_DIR=linux_x86_64
GPG_KEY_ID=3C98F63C9292CE02
PACKAGE=snowflake-streaming-ingest-cpp-${SDK_VERSION}-${PLATFORM}.tar.gz
BASE_URL=https://sfc-repo.snowflakecomputing.com/snowpipe-streaming-cpp/${SDK_VERSION}/${PLATFORM_DIR}

# Download the package, checksum, and signature into the current directory.
curl -fLO "${BASE_URL}/${PACKAGE}"
curl -fLO "${BASE_URL}/${PACKAGE}.sha256"
curl -fLO "${BASE_URL}/${PACKAGE}.asc"

# Verify the checksum. On macOS, run: shasum -a 256 -c "${PACKAGE}.sha256"
sha256sum -c "${PACKAGE}.sha256"

# Import the Snowflake public key, then verify the signature.
gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys "${GPG_KEY_ID}"
gpg --verify "${PACKAGE}.asc" "${PACKAGE}"

tar -xzf "${PACKAGE}"
SDK_DIR="$PWD/snowflake-streaming-ingest-cpp-${SDK_VERSION}-${PLATFORM}"
```

Do not use the package if either check fails.

Note

Verifying the signature produces a warning similar to the following:

> Copy code
>
> ```
> gpg: Signature made Mon 24 Sep 2018 03:03:45 AM UTC using RSA key ID <gpg_key_id>
> gpg: Good signature from "Snowflake Computing <snowflake_gpg@snowflake.net>" unknown
> gpg: WARNING: This key is not certified with a trusted signature!
> gpg: There is no indication that the signature belongs to the owner.
> ```

To avoid the warning, you can grant the Snowflake GPG public key implicit trust.

Important

Keep the unpacked package directory intact when you build. The package’s build files (the CMake package configuration file and the Bazel BUILD file) locate the headers and libraries by their paths inside the package, so move or rename the whole directory rather than copying individual files out of it.

Add the SDK to your `CMakeLists.txt`. The following file builds `example.cc` into an `example` executable that links to the SDK. When you build, set `CMAKE_PREFIX_PATH` to the absolute path of the unpacked package directory (`SDK_DIR` from the previous step).

Copy code

```
cmake_minimum_required(VERSION 3.21)
project(example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(SnowflakeStreamingIngest REQUIRED)

add_executable(example example.cc)
target_link_libraries(example PRIVATE Snowflake::snowflake_streaming_ingest)
```

To build your application, configure CMake with the SDK package directory, then build:

Copy code

```
cmake -S . -B build -DCMAKE_PREFIX_PATH="$SDK_DIR"
cmake --build build
```

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

JavaPythonC++Node.js

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
#include <snowflake/ingest/streaming/client.h>

#include <chrono>
#include <future>
#include <iostream>
#include <memory>
#include <optional>
#include <string>
#include <utility>

namespace sn = snowflake::ingest::streaming;

int main() {
  sn::TableClientOptions options;
  options.client_name = "demo-client";
  options.db_name = "MY_DATABASE";
  options.schema_name = "MY_SCHEMA";
  options.table_name = "MY_TABLE";
  options.profile_json = "profile.json";

  sn::Result<std::unique_ptr<sn::StreamingIngestClient>> client_result =
      sn::StreamingIngestClient::CreateFromTable(options);
  if (!client_result.has_value()) {
    std::cerr << "Failed to create client: " << client_result.error().message() << "\n";
    return 1;
  }
  sn::StreamingIngestClient& client = **client_result;

  sn::Result<std::pair<std::unique_ptr<sn::StreamingIngestChannel>, sn::ChannelStatus>>
      channel_result = client.OpenChannel("MY_CHANNEL", "0");
  if (!channel_result.has_value()) {
    std::cerr << "Failed to open channel: " << channel_result.error().message() << "\n";
    return 1;
  }
  sn::StreamingIngestChannel& channel = *channel_result->first;

  channel.AppendRow(R"({"DATA": {"event_id": 1, "status": "active"}, "C1": 1, "C2": "example"})", "1");
  channel.AppendRow(R"({"DATA": {"event_id": 2, "status": "active"}, "C1": 2, "C2": "example"})", "2");
  channel.AppendRow(R"({"DATA": {"event_id": 3, "status": "active"}, "C1": 3, "C2": "example"})", "3");

  sn::Result<sn::ChannelStatus> status_result = channel.GetChannelStatus();

  // Wait until offset 3 or a later offset is committed.
  sn::Result<std::future<sn::Result<void>>> commit_future = channel.WaitForCommit(
      [](const std::optional<std::string>& token) {
        return token.has_value() && std::stoll(*token) >= 3;
      },
      std::chrono::seconds(60));
  if (!commit_future.has_value()) {
    std::cerr << "WaitForCommit failed: " << commit_future.error().message() << "\n";
    return 1;
  }
  sn::Result<void> commit_result = commit_future->get();
  if (!commit_result.has_value()) {
    std::cerr << "WaitForCommit failed: " << commit_result.error().message() << "\n";
    return 1;
  }

  channel.Close();
  client.Close();
}
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

See the full [Java](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/java-example), [Python](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/python-example), [C++](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/cpp-example), and [Node.js](https://github.com/snowflakedb/snowpipe-streaming-sdk-examples/tree/main/nodejs-example) samples for complete examples.

Run the application, then query the target table to verify the rows. In a production application, retrieve the latest committed offset when you open the Named Channel and resume the source from the next record. For more information, see [Offset tokens and exactly-once delivery](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-offset-tokens).
