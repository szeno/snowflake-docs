# Snowflake Connector for Kafka: Install and configure

This topic describes the steps to install and configure the Snowflake Connector for Kafka.

## Installing the Kafka connector

The Kafka connector is provided as a JAR (Java executable) file.

Snowflake provides two versions of the connector:

- A version for the [Confluent Kafka installation](https://www.confluent.io/hub/snowflakeinc/snowflake-kafka-connector/).
- A version for the open source software (OSS) Apache Kafka https://central.sonatype.com/artifact/com.snowflake/snowflake-kafka-connector/ ecosystem.

The instructions in this topic specify which steps apply only to either version of the connector.

## Installation prerequisites

- The Kafka connector supports the following package versions:

  | Package | Snowflake Kafka Connector Version | Package Support (Tested by Snowflake) |
  | --- | --- | --- |
  | Apache Kafka | 2.0.0 (or later) | Apache Kafka 2.8.2, 3.7.2, 4.1.1 |
  | Confluent | 2.0.0 (or later) | Confluent 6.2.15, 7.8.2, 8.2.0 |

  Expand

  Show lessSee more
- The Kafka connector is built for use with Kafka Connect API 3.9.0. Later versions of the Kafka Connect API are untested.
  Versions prior to 3.9.0 are compatible with the connector.
  For more information, see [Kafka Compatibility](https://kafka.apache.org/protocol.html#protocol_compatibility).
- When you have both the Kafka connector and the JDBC driver jar files in your environment,
  ensure your JDBC version matches the `snowflake-jdbc` version specified in the `pom.xml` file of your intended Kafka connector version.
  You can go to your preferred Kafka connector release version, for example, [v4.0.0](https://github.com/snowflakedb/snowflake-kafka-connector/releases/tag/v4.0.0). Then browse the `pom.xml` file to find out the version of `snowflake-jdbc`.
- If you are using Avro format for ingesting data:

  - Use the Avro parser, version 1.8.2 (or higher), available from <https://central.sonatype.com/artifact/org.apache.avro/avro>.
  - If you use the schema registry feature with Avro, use version 5.0.0 (or higher) of the Kafka Connect Avro Converter available at <https://central.sonatype.com/artifact/io.confluent>.

    Note that the schema registry feature is not available in the OSS Apache Kafka package.
- Configure Kafka with the desired data retention time and/or storage limit.
- Install and configure the Kafka Connect cluster.

  Each Kafka Connect cluster node should include enough RAM for the Kafka connector. The minimum recommended amount is 5 MB per Kafka partition. This is in addition to the RAM required for any other work that Kafka Connect is doing.

  Important

  The v4 connector uses a Rust-based Snowpipe Streaming SDK that allocates off-heap (system)
  memory for buffering. Limit the JVM heap size to approximately 50% of the available memory
  to leave room for the SDK. For example, for a worker with 8 GB of RAM, set `-Xmx4g`.
- Snowflake recommends using the same versions on Kafka Broker and Kafka Connect Runtime.
- Snowflake strongly recommends running your Kafka Connect instance in the same cloud
  provider [region](/user-guide/intro-regions) as your Snowflake account. This isn’t strictly required, but typically improves throughput.

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

## Installing the connector

This section provides instructions for installing and configuring the Kafka connector for Confluent.
The following table describes the supported connector versions.

| Release Series | Status | Notes |
| --- | --- | --- |
| 4.x.x | Generally Available | Latest version. Migration from 3.x and 2.x must be done manually. |
| 3.x.x | Officially supported | Upgrade to v4 recommended. |
| 2.x.x | Officially supported | Upgrade recommended. |
| 1.x.x | Not supported |  |

Expand

Show lessSee more

### Installing the connector for Confluent

#### Download the Kafka connector files

Download the Kafka connector JAR file from either of the following locations:

Confluent Hub:
:   <https://www.confluent.io/hub/>

    The package includes all dependencies required to use either an encrypted or unencrypted private key for key pair authentication.
    For more information, see [Key pair authentication and key rotation](#label-kafkahp-key-pair-authn-rotation) later in this topic.

Maven Central Repository:
:   <https://central.sonatype.com/artifact/com.snowflake/snowflake-kafka-connector>

    When using this version you need to download the [Bouncy Castle](https://www.bouncycastle.org/) cryptography libraries (JAR files):

    > - <https://central.sonatype.com/artifact/org.bouncycastle/bc-fips/2.1.0>
    > - <https://central.sonatype.com/artifact/org.bouncycastle/bcpkix-fips/2.1.8>

    Download these files to the same local folder as the Kafka connector JAR file.

    The source code for the connector is available at <https://github.com/snowflakedb/snowflake-kafka-connector>.

#### Install the Kafka connector

Install the Kafka connector using the instructions provided for installing other connectors:

> <https://docs.confluent.io/current/connect/userguide.html>

### Installing the connector for open source Apache Kafka

This section provides instructions for installing and configuring the Kafka connector for open source Apache Kafka.

#### Install Apache Kafka

1. Download the Kafka package from the [Kafka official website](https://kafka.apache.org/downloads).
2. In a terminal window, change to the directory where you downloaded the package file.
3. Run the following command to decompress the `kafka_<scala_version>-<kafka_version>.tgz` file:

   Copy code

   ```
   tar xzvf kafka_<scala_version>-<kafka_version>.tgz
   ```

#### Install the JDK

Install and configure the Java Development Kit (JDK) version 11 or higher.
Snowflake tests with the Standard Edition (SE) of the JDK. The Enterprise Edition (EE) is expected to be compatible but has not been tested.

If you have previously installed the JDK, you can skip this section.

1. Download the JDK from the [Oracle JDK website](https://www.oracle.com/technetwork/java/javase/downloads/index.html).
2. Install or decompress the JDK.
3. Following the instructions for your operating system, set the environment variable JAVA\_HOME to point to the directory containing the JDK.

#### Download the Kafka connector JAR files

1. Download the Kafka connector JAR file from the Maven Central Repository:

   <https://central.sonatype.com/artifact/com.snowflake/snowflake-kafka-connector>
2. Download the [Bouncy Castle](https://www.bouncycastle.org/) cryptography library jar files:

   - <https://central.sonatype.com/artifact/org.bouncycastle/bc-fips/2.1.0>
   - <https://central.sonatype.com/artifact/org.bouncycastle/bcpkix-fips/2.1.8>
3. If your Kafka data is streamed in [Apache Avro](https://avro.apache.org/) format, download the Avro JAR file (1.11.4):

   - <https://central.sonatype.com/artifact/org.apache.avro/avro>

The source code for the connector is available at <https://github.com/snowflakedb/snowflake-kafka-connector>.

#### Install the Kafka connector

Copy the JAR files you downloaded in [Installing the connector for open source Apache Kafka](#label-install-kafkahp-oss) to the `<kafka_dir>/libs` folder.

## Configuring the Kafka connector

When deployed in standalone mode, the connector is configured by creating a file that
specifies parameters such as the Snowflake login credentials, topic name(s), Snowflake table name(s), and others.
When deployed in distributed mode the connector is configured by calling REST API endpoint of the kafka connect cluster.

Important

The Kafka Connect framework broadcasts the configuration settings for the Kafka connector from the primary node to worker nodes.
Configuration settings include sensitive information, specifically, the Snowflake username and private key.
Make sure to secure the communication channel between Kafka Connect nodes.
For more information, see the documentation for your Apache Kafka software.

Each configuration specifies the topics and corresponding tables for one database and one schema in that database.
Note that a connector can ingest messages from
any number of topics, but the corresponding tables must all be stored in a single database and schema.

This section provides instructions for both the distributed and standalone modes.

For descriptions of the configuration fields, see [Connector configuration properties](#label-kafkahp-connector-configuration-properties).

Important

Because the configuration file typically contains security related information,
such as the private key, set read/write privileges appropriately on the file to limit access.

In addition, consider storing the configuration file in a secure external
location or a key management service. For more information, see [Externalizing Secrets](#externalizing-secrets) (in this topic).

### Distributed mode

Create the Kafka configuration file, for example, `<path>/<config_file>.json`.
Populate the file with all connector configuration information.
The file must be in JSON format.

**Sample configuration file**

Copy code

```
{
  "name":"XYZCompanySensorData",
  "config":{
      "connector.class": "com.snowflake.kafka.connector.SnowflakeStreamingSinkConnector",
      "snowflake.topic2table.map": "topic1:table_1,topic2:table_2",
      "snowflake.url.name": "myorganization-myaccount.snowflakecomputing.com:443",
      "snowflake.private.key": "-----BEGIN PRIVATE KEY-----\n .... \n-----END PRIVATE KEY-----\n",
      "snowflake.schema.name": "MY_SCHEMA",
      "snowflake.database.name": "MY_DATABASE",
      "snowflake.role.name": "MY_ROLE",
      "snowflake.user.name": "MY_USER",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter": "org.apache.kafka.connect.storage.StringConverter",
      "errors.log.enable": "true",
      "topics": "topic1,topic2",
      "value.converter.schemas.enable": "false",
      "errors.tolerance": "none",
      "snowflake.streaming.validate.compatibility.with.classic": "false"
      }
}
```

### Standalone mode

Create a configuration file, for example `<kafka_dir>/config/SF_connect.properties`.
Populate the file with all connector
configuration information.

**Sample configuration file**

Copy code

```
connector.class=com.snowflake.kafka.connector.SnowflakeStreamingSinkConnector
snowflake.topic2table.map=topic1:table_1,topic2:table_2
snowflake.url.name=myorganization-myaccount.snowflakecomputing.com:443
snowflake.private.key=-----BEGIN PRIVATE KEY-----\n .... \n-----END PRIVATE KEY-----\n
snowflake.schema.name=MY_SCHEMA
snowflake.database.name=MY_DATABASE
snowflake.role.name=MY_ROLE
snowflake.user.name=MY_USER
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter=org.apache.kafka.connect.storage.StringConverter
errors.log.enable=true
topics=topic1,topic2
name=XYZCompanySensorData
value.converter.schemas.enable=false
errors.tolerance=none
snowflake.streaming.validate.compatibility.with.classic=false
```

## Cache considerations for testing and prototyping

The connector caches table and pipe lookup checks to improve performance during partition rebalances.
However, during testing and prototyping, this caching behavior can cause the connector
to not immediately detect manually created tables or pipes.

**Issue:** When you manually create a table or pipe while the connector is running,
the connector may continue to use cached existence check results (which may indicate the object doesn’t exist) for up to 5 minutes by default. This can lead to unexpected errors or behavior during testing.

**Recommendation for testing:** To avoid cache-related issues during testing and prototyping,
disable caching:

Copy code

```
snowflake.cache.table.exists=false
snowflake.cache.pipe.exists=false
```

This configuration ensures that the connector performs fresh existence checks on every partition rebalance, allowing you to see the effects of manually created tables and pipes immediately.

Important

These minimal cache settings are recommended **only for testing and prototyping**. In production environments, use the default cache expiration values (5 minutes or greater) to minimize metadata queries to Snowflake and improve rebalance performance, especially when handling many partitions.

## Connector configuration properties

### Minimal configuration for new installations

The following is a minimal configuration to get the connector running with v4 defaults.
This example uses JSON format for distributed mode:

Copy code

```
{
  "name": "my_kafka_connector",
  "config": {
    "connector.class": "com.snowflake.kafka.connector.SnowflakeStreamingSinkConnector",
    "topics": "my_topic",
    "snowflake.url.name": "https://myaccount.snowflakecomputing.com",
    "snowflake.user.name": "my_user",
    "snowflake.private.key": "<base64-encoded-private-key>",
    "snowflake.database.name": "MY_DB",
    "snowflake.schema.name": "MY_SCHEMA",
    "snowflake.role.name": "MY_ROLE",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "snowflake.streaming.validate.compatibility.with.classic": "false"
  }
}
```

This configuration uses all v4 defaults: server-side validation, schematized columns, and
case-sensitive identifiers. The connector auto-creates tables and pipes as needed.

Note

Set `snowflake.streaming.validate.compatibility.with.classic` to `false` for new
installations. This setting is only needed when migrating from v3.

Note

This example uses key pair authentication, the default method. For all supported
authentication methods, see [Authentication](#label-kafkahp-authentication).

### Required properties

`name`
:   Application name. This must be unique across all Kafka connectors used by the customer. This name must be a valid Snowflake unquoted identifier. For information about valid identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

`connector.class`
:   `com.snowflake.kafka.connector.SnowflakeStreamingSinkConnector`

`topics`
:   Comma-separated list of topics. By default, Snowflake assumes that the table name is the same as the topic name. If the table name is not the same as the topic name, then use the optional `topic2table.map` parameter (below) to specify the mapping from topic name to table name. This table name must be a valid Snowflake unquoted identifier. For information about valid table names, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    Either `topics` or `topics.regex` is required; not both.

`topics.regex`
:   This is a regular expression (“regex”) that specifies the topics that contain the messages to load into Snowflake tables. The connector loads data from any topic name that matches the regex. The regex must follow the rules for Java regular expressions (that is, be compatible with java.util.regex.Pattern). The configuration file should contain either `topics` or `topics.regex`, not both.

`snowflake.url.name`
:   The URL for accessing your Snowflake account. This URL must include your [account identifier](/user-guide/admin-account-identifier). Note that the protocol (`https://`) and port number are optional.

`snowflake.user.name`
:   User login name for the Snowflake account.

`snowflake.role.name`
:   The name of the role that the connector will use to insert data into the table.

`snowflake.database.name`
:   The name of the database that contains the table to insert rows into.

`snowflake.schema.name`
:   The name of the schema that contains the table to insert rows into.

`header.converter`
:   Required only if the records are formatted in Avro and include a header. The value is `"org.apache.kafka.connect.storage.StringConverter"`.

`key.converter`
:   The Kafka record’s key converter (for example, `"org.apache.kafka.connect.storage.StringConverter"`). This isn’t used by the Kafka connector, but is required by the Kafka Connect Platform.

`value.converter`
:   The connector supports standard Kafka community converters. Choose the appropriate converter based on your data format:

    - For JSON records: `"org.apache.kafka.connect.json.JsonConverter"`
    - For Avro records with Schema Registry: `"io.confluent.connect.avro.AvroConverter"`

    Note

    When `snowflake.enable.schematization=true` (the default), `StringConverter` and
    `ByteArrayConverter` aren’t supported as value converters. For more information,
    see [Troubleshoot the Snowflake Connector for Kafka](/user-guide/kafka-connector/troubleshoot).

### Authentication

The connector authenticates to Snowflake for both the JDBC connection and the Snowpipe Streaming SDK using `snowflake.authenticator`. Currently supported methods are key pair authentication (the default) and OAuth.

`snowflake.authenticator`
:   The authentication method for the JDBC connection and the Snowpipe Streaming SDK.

    Valid values:
    :   `snowflake_jwt` (key pair authentication), `oauth`

    Default:
    :   `snowflake_jwt`

#### Key pair authentication and key rotation

The connector authenticates with a key pair rather than a username and password. This method requires an RSA key pair of at least 2048 bits, with the public key assigned to the Snowflake user named in the connector configuration.

To generate the key pair and assign the public key to that user, follow [Generate a key pair for authentication](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-getting-started#generate-a-key-pair-for-authentication). To rotate keys later, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth). The connector requires no steps beyond those procedures.

Note

The Kafka connector supports encryption algorithms that are validated to meet the Federal Information Processing Standard (140-2) (that is, FIPS 140-2) requirements. For more information, see [FIPS 140-2](https://csrc.nist.gov/publications/detail/fips/140/2/final).

Once the key pair exists, set the following properties in the connector configuration file:

`snowflake.private.key`
:   The private key to authenticate the user. Include only the key, not the header or footer. If the key is split across multiple lines, remove the line breaks. You can provide an unencrypted key, or you can provide an encrypted key and provide the `snowflake.private.key.passphrase` parameter to enable Snowflake to decrypt the key. Use this parameter if and only if the `snowflake.private.key` parameter value is encrypted. This decrypts private keys that were encrypted according to the instructions in [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

`snowflake.private.key.passphrase`
:   If the value of this parameter is not empty, the connector uses this phrase to try to decrypt the private key.

Then evaluate the recommendation for [Externalizing secrets](#label-kafkahp-externalize-secrets), later in this topic.

#### OAuth authentication

Note

OAuth authentication is supported by the Kafka connector version 4.1.0 and later.

Instead of key pair authentication, the connector can authenticate to Snowflake with OAuth. The connector supports both Snowflake OAuth and External OAuth. For an overview, see [Introduction to OAuth](/user-guide/oauth-intro). By default, the connector uses your Snowflake account URL as the token endpoint (Snowflake OAuth); to use External OAuth, set `snowflake.oauth.token.endpoint` to your identity provider’s token endpoint.

To use OAuth, set `snowflake.authenticator` to `oauth` and provide your OAuth integration credentials. When you use OAuth, you don’t need to set the `snowflake.private.key` property.

`snowflake.oauth.client.id`
:   The client ID of the OAuth integration.

`snowflake.oauth.client.secret`
:   The client secret of the OAuth integration.

`snowflake.oauth.refresh.token`
:   The refresh token that the connector exchanges for an access token. If you leave this empty, the connector uses the `client_credentials` grant instead.

`snowflake.oauth.token.endpoint`
:   The token endpoint URL that the connector uses to exchange the refresh token for an access token. If you don’t set this property, it defaults to your Snowflake account URL.

`snowflake.oauth.include.scope`
:   Whether OAuth token requests include a `scope` parameter. When `false` (the default), the connector sends no scope. Set this to `true` to send a scope: either the explicit `snowflake.oauth.scope` value or, if that’s unset, `session:role:{role}` derived from `snowflake.role.name`.

    Default:
    :   `false`

`snowflake.oauth.scope`
:   The explicit OAuth scope to request. The connector uses this value only when `snowflake.oauth.include.scope` is `true`. When `snowflake.oauth.include.scope` is `true` and this property is unset, the scope defaults to `session:role:{role}`, derived from `snowflake.role.name`. This property has no effect while `snowflake.oauth.include.scope` is `false`, because no scope is sent.

Note

The client secret and refresh token are secrets. Snowflake recommends externalizing them, as described in [Externalizing secrets](#label-kafkahp-externalize-secrets).

#### Externalizing secrets

Snowflake strongly recommends externalizing secrets such as the private key and storing
them in an encrypted form or in a key management service such as AWS Key Management Service (KMS),
Microsoft Azure Key Vault, or HashiCorp Vault.
This can be accomplished by using a `ConfigProvider` implementation on your Kafka Connect cluster.

For more information, see the Confluent description of this [service](https://docs.confluent.io/current/connect/security.html#externalizing-secrets).

### Optional properties

#### Schematization and validation properties

These properties control how the connector processes and validates data. For new installations,
the defaults work well. If you’re migrating from v3, review [Migrate from Kafka connector v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4) for
guidance on which values to use.

`snowflake.enable.schematization`
:   Controls whether incoming records are schematized into individual table columns or wrapped
    into legacy VARIANT columns.

    When `true` (the default), record fields are mapped to individual table columns by name.
    When `false`, the connector stores records in two VARIANT columns (`RECORD_CONTENT` and
    `RECORD_METADATA`), matching v3 behavior.

    Default:
    :   `true`

`snowflake.validation`
:   Controls where data validation and schema evolution are performed.

    `server_side` (default): Validation is performed by the Snowflake backend, aligned with
    COPY and Snowpipe behavior. Invalid records are captured in
    [Error Tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling).
    Supports both default pipe and user-defined pipe modes.

    `client_side`: The connector validates data types and schema compatibility before sending
    rows to Snowflake. Supports Dead Letter Queue (DLQ) for invalid records. Only works with the
    default pipe mode.

    For details, see [Validation and error handling](/user-guide/kafka-connector/validation-error-handling).

    Default:
    :   `server_side`

#### Table auto-creation properties

Note

Auto-creating a standard Snowflake table is supported in all connector versions. The `snowflake.autocreate.table.type` and `snowflake.iceberg.create.table.options` properties, which add Iceberg table auto-creation and let you disable auto-creation, are supported by the Kafka connector version 4.1.0 and later.

These properties control whether and how the connector auto-creates the target table when it’s missing. An existing table is always used as-is, regardless of these settings.

`snowflake.autocreate.table.type`
:   Controls table auto-creation:

    - `snowflake` (the default): auto-create a standard Snowflake table if it’s missing.
    - `iceberg`: auto-create a Snowflake-managed [Apache Iceberg table](/user-guide/tables-iceberg) if it’s missing.
    - `none`: never auto-create the table, and fail fast if it’s missing. The connector still auto-manages the pipe as usual.

    Valid values:
    :   `snowflake`, `iceberg`, `none`

    Default:
    :   `snowflake`

`snowflake.iceberg.create.table.options`
:   SQL clauses spliced into the auto-created Iceberg table’s `CREATE` statement after the column list, for example `EXTERNAL_VOLUME='v' ICEBERG_VERSION=3 CLUSTER BY (id)`. This lets you set any Snowflake-managed Iceberg create option without a dedicated property for each one.

    The connector uses this property only when `snowflake.autocreate.table.type` is `iceberg`, and ignores it if the table already exists. Don’t include `CATALOG`, `ENABLE_SCHEMA_EVOLUTION`, or `ERROR_LOGGING`, because the connector always supplies those.

    Default:
    :   None (no extra clauses)

Note

Server-side schema evolution is supported for Iceberg tables.

Client-side schema evolution isn’t supported for Iceberg tables.

#### Migration and compatibility properties

These properties are relevant when migrating from v3. For fresh installations, you can skip
these and set `snowflake.streaming.validate.compatibility.with.classic=false`.

`snowflake.compatibility.enable.autogenerated.table.name.sanitization`
:   Controls how auto-generated table names are derived from topic names.

    When `false` (the default), topic names are used as-is for table names, preserving case and
    special characters. Table names are created as quoted identifiers.

    When `true`, invalid Snowflake identifier characters are replaced with underscores, names are
    uppercased, and a hash code is appended for uniqueness. This matches v3 behavior.

    Default:
    :   `false`

`snowflake.compatibility.enable.column.identifier.normalization`
:   Controls how column identifiers are handled.

    When `false` (the default), column identifiers preserve case and special characters as-is.

    When `true`, column identifiers are normalized to uppercase, matching v3 behavior.

    Default:
    :   `false`

`snowflake.streaming.validate.compatibility.with.classic`
:   Enables startup validation that checks whether all migration-related configs are explicitly set.
    When `true`, the connector fails at startup with a descriptive error if any of the following
    configs are missing or incompatible with v3 behavior:

    - `snowflake.validation` must be `client_side`
    - `snowflake.compatibility.enable.column.identifier.normalization` must be `true`
    - `snowflake.compatibility.enable.autogenerated.table.name.sanitization` must be `true`
    - `snowflake.enable.schematization` must be explicitly set to `true` or `false` (the default changed between v3 and v4)
    - `snowflake.streaming.classic.offset.migration` must be explicitly set
    - `snowflake.streaming.classic.offset.migration.include.connector.name` must be explicitly set
      (when offset migration is `strict` or `best_effort`)

    This prevents accidentally running v4 with a copied v3 configuration without reviewing the
    breaking changes. Set to `false` to skip this check after you’ve confirmed your configuration.

    Note

    For fresh installations (not migrating from v3), set this to `false`. The compatibility
    validator is only needed when upgrading from an existing v3 deployment.

    For more information, see [Migrate from Kafka connector v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

    Default:
    :   `true`

#### Offset migration properties

These properties control how v4 migrates committed offsets from v3 Snowpipe Streaming (SSv1)
channels. They’re only relevant when migrating from a v3 connector that used
`snowflake.ingestion.method=SNOWPIPE_STREAMING`. If you’re migrating from v3 Snowpipe mode
(file-based ingestion), set `snowflake.streaming.classic.offset.migration` to `skip`.

`snowflake.streaming.classic.offset.migration`
:   Controls how v4 migrates offsets from v3 Snowpipe Streaming (SSv1) channels.

    `strict`: v4 looks up the committed offset from the v3 SSv1 channel and resumes from that
    point. If the SSv1 channel isn’t found, the connector fails with an error.

    `best_effort`: v4 attempts to look up the committed offset from the v3 SSv1 channel. If the
    channel isn’t found, v4 falls back to the Kafka consumer group offset.

    `skip` (default): No SSv1 offset migration is performed. v4 uses the Kafka consumer group
    offset. Use this when migrating from v3 Snowpipe mode (not Snowpipe Streaming).

    Default:
    :   `skip`

`snowflake.streaming.classic.offset.migration.include.connector.name`
:   Controls whether the SSv1 channel name lookup includes the connector name. This must match how
    your v3 connector was configured. In v3, the
    `snowflake.streaming.channel.name.include.connector.name` property controlled whether the
    connector name was included in the channel name.

    Set to `true` if your v3 connector had
    `snowflake.streaming.channel.name.include.connector.name=true`, or if you were running
    Kafka connector version 2.1.0 or 2.1.1 (those versions included the connector name by default).
    Set to `false` otherwise.

    Only required when `snowflake.streaming.classic.offset.migration` is `strict` or
    `best_effort`.

    Default:
    :   none (must be explicitly set when offset migration is active)

#### Error handling properties

`errors.tolerance`
:   Controls how the connector responds to errors during ingestion.

    `none` (default): The connector task fails on the first error. With server-side validation,
    error detection is asynchronous, so a few records after the broken one may still be ingested
    before the task fails.

    `all`: The connector continues ingesting data. With client-side validation, invalid records
    are routed to the DLQ (if configured) or silently dropped.

    Warning

    Setting `errors.tolerance=all` without configuring a DLQ topic causes invalid records to be
    silently dropped when using client-side validation. This can cause data loss.

    Default:
    :   `none`

`errors.deadletterqueue.topic.name`
:   The Kafka topic name for the Dead Letter Queue. Only effective when
    `snowflake.validation=client_side` and `errors.tolerance=all`.

    Default:
    :   empty (DLQ disabled)

`errors.log.enable`
:   When `true`, errors are logged with details of the failed operation and record properties.

    Default:
    :   `false`

`enable.task.fail.on.authorization.errors`
:   When `true`, the connector task fails immediately on authorization errors from Snowflake.
    When `false`, the connector retries.

    Default:
    :   `false`

#### Caching properties

`snowflake.cache.table.exists`
:   Enables caching for table existence checks, reducing the number of metadata queries to Snowflake.

    Default:
    :   `true`

`snowflake.cache.table.exists.expire.ms`
:   Cache expiration time in milliseconds for table existence checks.

    Default:
    :   `300000` (5 minutes)

`snowflake.cache.pipe.exists`
:   Enables caching for pipe existence checks.

    Default:
    :   `true`

`snowflake.cache.pipe.exists.expire.ms`
:   Cache expiration time in milliseconds for pipe existence checks.

    Default:
    :   `300000` (5 minutes)

#### Monitoring and diagnostics properties

`jmx`
:   Enables JMX MBeans for connector metrics. For more information, see [Monitor the Snowflake Connector for Kafka](/user-guide/kafka-connector/monitor).

    Default:
    :   `true`

`enable.mdc.logging`
:   Enables MDC (Mapped Diagnostic Context) to prepend connector context to log messages,
    which is useful when running multiple connector instances.

    Default:
    :   `false`

`snowflake.streaming.metadata.connectorPushTime`
:   When `true`, includes the `SnowflakeConnectorPushTime` timestamp in `RECORD_METADATA`.
    This field records when the connector buffered a record for ingestion and is useful for
    estimating end-to-end latency.

    Default:
    :   `true`

#### Advanced properties

`snowflake.streaming.client.provider.override.map`
:   Overrides for Snowpipe Streaming client properties. Format: `key1:value1,key2:value2`.
    Use only after consulting Snowflake Support.

    Default:
    :   empty

#### Other properties

`tasks.max`
:   Number of tasks, usually the same as the number of CPU cores across the worker nodes in the Kafka Connect cluster. To achieve best performance, Snowflake recommends setting the number of tasks equal to the total number of Kafka partitions, but not exceeding the number of CPU cores. A high number of tasks may result in an increased memory consumption and frequent rebalances.

`snowflake.topic2table.map`
:   Comma-separated list of topic-to-table mappings in `topic:table` format. Supports regex
    patterns for topic names. The regular expressions can’t be ambiguous — any matched topic
    must match only a single target table.

    Both topic and table names can be double-quoted to support special characters (colons, commas,
    spaces). Unquoted table names are uppercased. Quoted table names preserve case.

    For detailed examples including regex patterns, many-to-one mappings, and quoting, see
    [Explicit topic-to-table mapping](/user-guide/kafka-connector/how-the-connector-works#label-kafkahp-explicit-topic-to-table-mapping).

    Example:

    Copy code

    ```
    snowflake.topic2table.map=topic1:low_range,topic2:low_range,"my:topic":"My_Table"
    ```

`snowflake.topic2table.map.regex.replacement`
:   When `true`, table names in `snowflake.topic2table.map` are treated as replacement templates, so `$` introduces a regex group reference (for example, `topic(.*):table$1`). To include a literal `$` in a table name in this mode, escape it as `\$`.

    When `false` (the default), the connector performs no group substitution and treats table names literally. This default preserves backward compatibility for existing mappings.

    This property is supported by the Kafka connector version 4.1.0 and later.

    Default:
    :   `false`

`value.converter.schema.registry.url`
:   If the format is Avro and you are using a Schema Registry Service, this should be the URL of the Schema Registry Service. Otherwise this field should be empty.

`value.converter.break.on.schema.registry.error`
:   If loading Avro data from the Schema Registry Service, this property determines if the Kafka connector should stop consuming records if it encounters an error while fetching the schema id. The default value is `false`. Set the value to `true` to enable this behavior.

`jvm.proxy.host`
:   To enable the Snowflake Kafka Connector to access Snowflake through a proxy server, set this parameter to specify the host of that proxy server.

`jvm.proxy.port`
:   To enable the Snowflake Kafka Connector to access Snowflake through a proxy server, set this parameter to specify the port of that proxy server.

`jvm.proxy.username`
:   Username that authenticates with the proxy server.

`jvm.proxy.password`
:   Password for the username that authenticates with the proxy server.

`snowflake.jdbc.map`
:   Example: `"snowflake.jdbc.map": "networkTimeout:20,tracing:WARNING"`

    Additional JDBC properties (see [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters)) are not validated. These additional properties
    are not validated, and must not override nor be used instead of required properties such as: `jvm.proxy.xxx`,
    `snowflake.user.name`, `snowflake.private.key`, `snowflake.schema.name`, and similar properties.

    Specifying either of the following combinations:
    :   - `tracing` property along with `JDBC_TRACE` env variable
        - `database` property along with `snowflake.database.name`

    Will result in an ambiguous behavior and the behavior will be determined by the JDBC Driver.

`value.converter.basic.auth.credentials.source`
:   If you are using the Avro data format and require secure access to the Kafka schema registry, set this parameter to the string “USER\_INFO”, and set the `value.converter.basic.auth.user.info` parameter described below. Otherwise, omit this parameter.

`value.converter.basic.auth.user.info`
:   If you are using the Avro data format and require secure access to the Kafka schema registry, set this parameter to the string “<user\_ID>:<password>”, and set the value.converter.basic.auth.credentials.source parameter described above. Otherwise, omit this parameter.

`snowflake.metadata.createtime`
:   If value is set to FALSE, the `CreateTime` property value is omitted from the metadata in the RECORD\_METADATA column. The default value is TRUE.

`snowflake.metadata.topic`
:   If value is set to FALSE, the `topic` property value is omitted from the metadata in the RECORD\_METADATA column. The default value is TRUE.

`snowflake.metadata.offset.and.partition`
:   If value is set to FALSE, the `Offset` and `Partition` property values are omitted from the metadata in the RECORD\_METADATA column. The default value is TRUE.

`snowflake.metadata.all`
:   If value is set to FALSE, the metadata in the RECORD\_METADATA column is completely empty. The default value is TRUE.

`snowflake.feature.structured.headers`
:   When `true`, Kafka record headers are written to `RECORD_METADATA:headers` preserving their converted structured types (objects, arrays, numbers, and booleans). When `false` (the default), header values are flattened to strings.

    This property is supported by the Kafka connector version 4.1.0 and later.

    Default:
    :   `false`

`transforms`
:   Specify to skip tombstone records encountered by the Kafka connector and not load them into the target table. A tombstone record is
    defined as a record where the entire value field is null.

    Set the property value to `"tombstoneHandlerExample"`.

    Note

    Use this property with the Kafka community converters (that is, `value.converter` property value) only (for example,
    `org.apache.kafka.connect.json.JsonConverter` or `org.apache.kafka.connect.json.AvroConverter`). To manage tombstone record
    handling with the Snowflake converters, use the `behavior.on.null.values` property instead.

`transforms.tombstoneHandlerExample.type`
:   Required when setting the `transforms` property.

    Set the property value to `"io.confluent.connect.transforms.TombstoneHandler"`

`behavior.on.null.values`
:   Specify how the Kafka connector should handle tombstone records. A tombstone record is defined as a record where the entire value field
    is null. For [Snowpipe](/user-guide/data-load-snowpipe-intro), this property is supported by the Kafka connector version 1.5.5 and later. For [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview), this property is supported by the Kafka connector version 2.1.0 and later.

    This property supports the following values:

    `DEFAULT`
    :   When the Kafka connector encounters a tombstone record, it inserts an empty JSON string in the content column.

    `IGNORE`
    :   The Kafka connector skips tombstone records and does not insert rows for these records.

    The default value is `DEFAULT`.

    Note

    Tombstone records ingestion varies by the ingestion methods:

    - For Snowpipe, the Kafka connector uses Snowflake converters only. To manage tombstone record handling with the Kafka community converters, use the `transform` and `transforms.tombstoneHandlerExample.type` properties instead.
    - For Snowpipe Streaming, the Kafka connector uses community converters only.

    Records sent to Kafka brokers must not be NULL because these records will be dropped by the Kafka connector resulting in missing offsets. The missing offsets will break the Kafka connector in specific use cases. It is recommended that you use tombstone records instead of NULL records.

## Starting the connector

Start Kafka using the instructions provided in the third-party Confluent or Apache Kafka documentation.
You can start the Kafka connector in either distributed mode or standalone mode. Instructions for each are shown below:

### Distributed mode

In a terminal window, run the following command:

Copy code

```
curl -X POST -H "Content-Type: application/json" --data @<path>/<config_file>.json http://localhost:8083/connectors
```

### Standalone mode

In a terminal window, run the following command:

Copy code

```
<kafka_dir>/bin/connect-standalone.sh <kafka_dir>/<path>/connect-standalone.properties <kafka_dir>/config/SF_connect.properties
```

Note

A default installation of Apache Kafka or Confluent Kafka should already include the file `connect-standalone.properties`.)

## Next steps

[test the connector](/user-guide/kafka-connector/test-connector).
