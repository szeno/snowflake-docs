Important

- Advance notice: The classic Kafka connector (v3 and earlier) is fully supported today,
  but it is planned for future deprecation.
- Action: No immediate changes are required. Your current workloads are safe
  and continue to be fully supported.
- Timeline: Snowflake plans to issue a formal deprecation announcement in mid-2026.
  After the announcement, an 18-month migration window begins before end-of-life.
- Recommendation: Use the
  [Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index)
  for all new implementations.

For migration guidance, see [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

# Installing and configuring the Kafka connector

The Kafka connector is provided as a JAR (Java executable) file.

Snowflake provides two versions of the connector:

- A version for the [Confluent package version of Kafka](https://www.confluent.io/hub/snowflakeinc/snowflake-kafka-connector).
- A version for the [open source software (OSS) Apache Kafka package](https://central.sonatype.com/artifact/com.snowflake/snowflake-kafka-connector/).

The instructions in this topic specify which steps apply only to either version of the connector.

## Configuring access control for Snowflake objects

### Required privileges

Creating and managing Snowflake objects used by the Kafka connector requires a role with the following minimum privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE   CREATE TABLE   CREATE STAGE   CREATE PIPE | After the schema-level objects have been created, the CREATE `object` privileges can be revoked. |
| Table | OWNERSHIP | Only required when using the Kafka connector to ingest data into an existing table.   If the connector creates a new target table for records from the Kafka topic, the default role for the user specified in the Kafka configuration file becomes the table owner (i.e. has the OWNERSHIP privilege on the table). |
| Stage | READ   WRITE | Only required when using the Kafka connector to stage data files from Kafka to an existing internal stage (not recommended).   If the connector creates a new stage to temporarily store data files consumed from the Kafka topic, the default role for the user specified in the Kafka configuration file becomes the stage owner (i.e. has the OWNERSHIP privilege on the stage). |

Expand

Show lessSee more

Snowflake recommends that you create a separate user (using [CREATE USER](/sql-reference/sql/create-user)) and role (using [CREATE ROLE](/sql-reference/sql/create-role)) for each Kafka instance so that the access privileges can be individually revoked if needed. The role should be assigned as the default role for the user.

### Creating a role to use the Kafka connector

The following script creates a custom role for use by the Kafka connector (e.g. KAFKA\_CONNECTOR\_ROLE\_1). Any role that can grant privileges (e.g. SECURITYADMIN or any role with the MANAGE GRANTS privilege) can grant this custom role to any user to allow the Kafka connector to create the required Snowflake objects and insert data into tables. The script references a specific existing database and schema (`kafka_db.kafka_schema`) and user (`kafka_connector_user_1`):

Copy code

```
-- Use a role that can create and manage roles and privileges.
USE ROLE securityadmin;

-- Create a Snowflake role with the privileges to work with the connector.
CREATE ROLE kafka_connector_role_1;

-- Grant privileges on the database.
GRANT USAGE ON DATABASE kafka_db TO ROLE kafka_connector_role_1;

-- Grant privileges on the schema.
GRANT USAGE ON SCHEMA kafka_schema TO ROLE kafka_connector_role_1;
GRANT CREATE TABLE ON SCHEMA kafka_schema TO ROLE kafka_connector_role_1;
GRANT CREATE STAGE ON SCHEMA kafka_schema TO ROLE kafka_connector_role_1;
GRANT CREATE PIPE ON SCHEMA kafka_schema TO ROLE kafka_connector_role_1;

-- Only required if the Kafka connector will load data into an existing table.
GRANT OWNERSHIP ON TABLE existing_table1 TO ROLE kafka_connector_role_1;

-- Only required if the Kafka connector will stage data files in an existing internal stage: (not recommended).
GRANT READ, WRITE ON STAGE existing_stage1 TO ROLE kafka_connector_role_1;

-- Grant the custom role to an existing user.
GRANT ROLE kafka_connector_role_1 TO USER kafka_connector_user_1;

-- Set the custom role as the default role for the user.
-- If you encounter an 'Insufficient privileges' error, verify the role that has the OWNERSHIP privilege on the user.
ALTER USER kafka_connector_user_1 SET DEFAULT_ROLE = kafka_connector_role_1;
```

Note that any privileges must be granted directly to the role used by the connector. Grants cannot be inherited from the role hierarchy.

For more information on creating custom roles and role hierarchies, see [Configuring access control](/user-guide/security-access-control-configure).

## Installation prerequisites

- The Kafka connector supports the following package versions:

  | Package | Snowflake Kafka Connector Version | Package Support (Tested by Snowflake) |
  | --- | --- | --- |
  | Apache Kafka | 2.0.0 (or higher) | Apache Kafka 2.8.2, 3.7.2 |
  | Confluent | 2.0.0 (or higher) | Confluent 6.2.15, 7.8.2 |

  Expand

  Show lessSee more
- The Kafka connector is built for use with Kafka Connect API 3.9.0. Any newer versions of Kafka Connect API have not been tested. Any versions older than 3.9.0 are compatible with the connector. For more information, see [Kafka Compatibility](https://kafka.apache.org/protocol.html#protocol_compatibility).
- When you have both the Kafka connector and the JDBC driver jar files in your environment, make sure your JDBC version matches the `snowflake-jdbc` version specified in the `pom.xml` file of your intended Kafka connector version. You can go to your preferred Kafka connector release version, for example, [v2.0.1](https://github.com/snowflakedb/snowflake-kafka-connector/releases/tag/v2.0.1). Then browse the `pom.xml` file to find out the version of `snowflake-jdbc`.
- If you use Avro format for ingesting data:

  - Use the Avro parser, version 1.8.2 (or higher), available from <https://central.sonatype.com/artifact/org.apache.avro/avro>.
  - If you use the schema registry feature with Avro, use version 5.0.0 (or higher) of the Kafka Connect Avro Converter available at <https://central.sonatype.com/artifact/io.confluent>.

    Note that the schema registry feature is not available in the OSS Apache Kafka package.
- Configure Kafka with the desired data retention time and/or storage limit.
- Install and configure the Kafka Connect cluster.

  Each Kafka Connect cluster node should include enough RAM for the Kafka connector. The minimum recommended amount is 5 MB per Kafka partition. This is in addition to the RAM required for any other work that Kafka Connect is doing.
- We recommend using the same versions on Kafka Broker and Kafka Connect Runtime.
- We strongly recommend running your Kafka Connect instance in the same cloud provider [region](/user-guide/intro-regions) as your Snowflake account. This is not strictly required, but typically improves throughput.

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

## Installing the connector

This section provides instructions for installing and configuring the Kafka connector for Confluent. Refer to the following table for Kafka connector versions:

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

    The package includes all dependencies required to use either an encrypted or unencrypted private key for key pair authentication. For more information, see [Using Key Pair Authentication & Key Rotation](#using-key-pair-authentication-key-rotation) (in this topic).

Maven Central Repository:
:   <https://central.sonatype.com/artifact/com.snowflake/snowflake-kafka-connector>

    The JAR file does not require any additional dependencies to use an unencrypted private key for key pair authentication. To use an encrypted private key, download the [Bouncy Castle](https://www.bouncycastle.org/) cryptography library (a JAR file). Snowflake uses Bouncy Castle to decrypt encrypted RSA private keys used to log in:

    > - <https://central.sonatype.com/artifact/org.bouncycastle/bc-fips/2.1.0>
    > - <https://central.sonatype.com/artifact/org.bouncycastle/bcpkix-fips/2.1.8>

    For the Kafka Connector versions prior to 3.1.1, use the following Bouncy Castle versions instead:

    > - <https://central.sonatype.com/artifact/org.bouncycastle/bc-fips/1.0.1>
    > - <https://central.sonatype.com/artifact/org.bouncycastle/bcpkix-fips/1.0.3>

    Download these files to the same local folder as the Kafka connector JAR file.

    The source code for the connector is available at <https://github.com/snowflakedb/snowflake-kafka-connector>.

#### Install the Kafka connector

Install the Kafka connector using the instructions provided for installing other connectors:

> <https://docs.confluent.io/current/connect/userguide.html>

### Installing the connector for open source Apache Kafka

This section provides instructions for installing and configuring the Kafka connector for open source Apache Kafka.

#### Install Apache Kafka

1. Download the Kafka package from its official website: <https://kafka.apache.org/downloads>.
2. In a terminal window, change to the directory where you downloaded the package file.
3. Execute the following command to decompress the `kafka_<scala_version>-<kafka_version>.tgz` file:

   Copy code

   ```
   tar xzvf kafka_<scala_version>-<kafka_version>.tgz
   ```

#### Install the JDK

Install and configure the Java Development Kit (JDK). Snowflake tests with the Standard Edition (SE) of the JDK. The Enterprise Edition (EE) is expected to be compatible but has not been tested.

If you have already completed this step, you can skip this section.

1. Download the JDK from <https://www.oracle.com/technetwork/java/javase/downloads/index.html>.
2. Install or decompress the JDK.
3. Following the instructions for your operating system, set the environment variable JAVA\_HOME to point to the directory containing the JDK.

#### Download the Kafka connector JAR files

1. Download the Kafka connector JAR file from the Maven Central Repository:

   <https://central.sonatype.com/artifact/com.snowflake/snowflake-kafka-connector>
2. The JAR file does not require any additional dependencies to use an unencrypted private key for key pair authentication. To use an encrypted private key, download the [Bouncy Castle](https://www.bouncycastle.org/) cryptography library (a JAR file). Snowflake uses Bouncy Castle to decrypt encrypted RSA private keys used to log in:

   - <https://central.sonatype.com/artifact/org.bouncycastle/bc-fips/1.0.1>
   - <https://central.sonatype.com/artifact/org.bouncycastle/bcpkix-fips/1.0.3>
3. If your Kafka data is streamed in [Apache Avro](https://avro.apache.org/) format, then download the Avro JAR file:

   <https://central.sonatype.com/artifact/org.apache.avro/avro>

The source code for the connector is available at <https://github.com/snowflakedb/snowflake-kafka-connector>.

#### Install the Kafka connector

Copy the JAR files you downloaded in [Download the Kafka Connector JAR Files](#download-the-kafka-connector-jar-files) to the `<kafka_dir>/libs` folder.

## Configuring the Kafka connector

The connector is configured by creating a file that specifies parameters such as the Snowflake login credentials, topic name(s), Snowflake table name(s), etc.

Important

The Kafka Connect framework broadcasts the configuration settings for the Kafka connector from the master node to worker nodes. The configuration settings include sensitive information (specifically, the Snowflake username and private key). Make sure to secure the communication channel between Kafka Connect nodes. For instructions, see the documentation for your Apache Kafka software.

Each configuration file specifies the topics and corresponding tables for one database and one schema in that database. Note that a connector can ingest messages from
any number of topics, but the corresponding tables must all be stored in a single database and schema.

This section provides instructions for both the distributed and standalone modes.

For descriptions of the configuration fields, see [Kafka configuration properties](#label-kafka-properties).

Important

Because the configuration file typically contains security related information, such as the private key, set read/write privileges appropriately on the file to limit access.

In addition, consider storing the configuration file in a secure external location or a key management service. For more information, see [Externalizing Secrets](#externalizing-secrets) (in this topic).

### Distributed mode

Create the Kafka configuration file, e.g. `<path>/<config_file>.json`. Populate the file with all connector configuration
information. The file should be in JSON format.

**Sample configuration file**

Copy code

```
{
  "name":"XYZCompanySensorData",
  "config":{
    "connector.class":"com.snowflake.kafka.connector.SnowflakeSinkConnector",
    "tasks.max":"8",
    "topics":"topic1,topic2",
    "snowflake.topic2table.map": "topic1:table1,topic2:table2",
    "buffer.count.records":"10000",
    "buffer.flush.time":"60",
    "buffer.size.bytes":"5000000",
    "snowflake.url.name":"myorganization-myaccount.snowflakecomputing.com:443",
    "snowflake.user.name":"jane.smith",
    "snowflake.private.key":"xyz123",
    "snowflake.private.key.passphrase":"jkladu098jfd089adsq4r",
    "snowflake.database.name":"mydb",
    "snowflake.schema.name":"myschema",
    "key.converter":"org.apache.kafka.connect.storage.StringConverter",
    "value.converter":"com.snowflake.kafka.connector.records.SnowflakeAvroConverter",
    "value.converter.schema.registry.url":"http://localhost:8081",
    "value.converter.basic.auth.credentials.source":"USER_INFO",
    "value.converter.basic.auth.user.info":"jane.smith:MyStrongPassword"
  }
}
```

### Standalone mode

Create a configuration file, e.g. `<kafka_dir>/config/SF_connect.properties`. Populate the file with all connector
configuration information.

**Sample configuration file**

Copy code

```
connector.class=com.snowflake.kafka.connector.SnowflakeSinkConnector
tasks.max=8
topics=topic1,topic2
snowflake.topic2table.map= topic1:table1,topic2:table2
buffer.count.records=10000
buffer.flush.time=60
buffer.size.bytes=5000000
snowflake.url.name=myorganization-myaccount.snowflakecomputing.com:443
snowflake.user.name=jane.smith
snowflake.private.key=xyz123
snowflake.private.key.passphrase=jkladu098jfd089adsq4r
snowflake.database.name=mydb
snowflake.schema.name=myschema
key.converter=org.apache.kafka.connect.storage.StringConverter
value.converter=com.snowflake.kafka.connector.records.SnowflakeAvroConverter
value.converter.schema.registry.url=http://localhost:8081
value.converter.basic.auth.credentials.source=USER_INFO
value.converter.basic.auth.user.info=jane.smith:MyStrongPassword
```

### Kafka configuration properties

The following properties can be set in the Kafka configuration file for either distributed mode or standalone mode:

#### Required properties

`name`
:   Application name. This must be unique across all Kafka connectors used by the customer. This name must be a valid Snowflake unquoted identifier. For information about valid identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

`connector.class`
:   `com.snowflake.kafka.connector.SnowflakeSinkConnector`

`topics`
:   Comma-separated list of topics. By default, Snowflake assumes that the table name is the same as the topic name. If the table name is not the same as the topic name, then use the optional `topic2table.map` parameter (below) to specify the mapping from topic name to table name. This table name must be a valid Snowflake unquoted identifier. For information about valid table names, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    Either `topics` or `topics.regex` is required; not both.

`topics.regex`
:   This is a regular expression (“regex”) that specifies the topics that contain the messages to load into Snowflake tables. The connector loads data from any topic name that matches the regex. The regex must follow the rules for Java regular expressions (i.e. be compatible with java.util.regex.Pattern). The configuration file should contain either `topics` or `topics.regex`, not both.

`snowflake.url.name`
:   The URL for accessing your Snowflake account. This URL must include your [account identifier](/user-guide/admin-account-identifier). Note that the protocol (`https://`) and port number are optional.

`snowflake.user.name`
:   User login name for the Snowflake account.

`snowflake.private.key`
:   The private key to authenticate the user. Include only the key, not the header or footer. If the key is split across multiple lines, remove the line breaks. You can provide an unencrypted key, or you can provide an encrypted key and provide the `snowflake.private.key.passphrase` parameter to enable Snowflake to decrypt the key. Use this parameter if and only if the `snowflake.private.key` parameter value is encrypted. This decrypts private keys that were encrypted according to the instructions in [Using Key Pair Authentication & Key Rotation](#using-key-pair-authentication-key-rotation) (in this topic).

    Note

    Also see `snowflake.private.key.passphrase` in [Optional Properties](#optional-properties) (in this topic).

`snowflake.database.name`
:   The name of the database that contains the table to insert rows into.

`snowflake.schema.name`
:   The name of the schema that contains the table to insert rows into.

`header.converter`
:   Required only if the records are formatted in Avro and include a header. The value is `"org.apache.kafka.connect.storage.StringConverter"`.

`key.converter`
:   This is the Kafka record’s key converter (e.g. `"org.apache.kafka.connect.storage.StringConverter"`). This is not used by the Kafka connector, but is required by the Kafka Connect Platform.

    See [Kafka connector limitations](/user-guide/kafka-connector-overview#label-kafka-connector-limitations) for current limitations.

`value.converter`
:   If the records are formatted in JSON, this should be `"com.snowflake.kafka.connector.records.SnowflakeJsonConverter"`.

    Note

    `"com.snowflake.kafka.connector.records.SnowflakeJsonConverter"` deserializes the records as is. Every JSON field is considered to be a record field and no special treatment is applied to a schema or any other field containing metadata.

    If the records are formatted in Avro and use Kafka’s Schema Registry Service, this should be `"com.snowflake.kafka.connector.records.SnowflakeAvroConverter"`.

    If the records are formatted in Avro and contain the schema (and therefore do not need Kafka’s Schema Registry Service), this should be `"com.snowflake.kafka.connector.records.SnowflakeAvroConverterWithoutSchemaRegistry"`.

    If the records are formatted in plain text, this should be `"org.apache.kafka.connect.storage.StringConverter"`.

    See [Kafka connector limitations](/user-guide/kafka-connector-overview#label-kafka-connector-limitations) for current limitations.

#### Optional properties

`snowflake.private.key.passphrase`
:   If the value of this parameter is not empty, the Kafka connector uses this phrase to try to decrypt the private key.

`tasks.max`
:   Number of tasks, usually the same as the number of CPU cores across the worker nodes in the Kafka Connect cluster. To achieve best performance, Snowflake recommends setting the number of tasks equal to the total number of Kafka partitions, but not exceeding the number of CPU cores. A high number of tasks may result in increased memory consumption and frequent rebalances.

`snowflake.topic2table.map`
:   This optional parameter lets a user specify which topics should be mapped to which tables. Each topic and its table name should be separated by a colon (see example below). This table name must be a valid Snowflake unquoted identifier. For information about valid table names, see [Identifier requirements](/sql-reference/identifiers-syntax). The topic configuration allows use of regular expressions to define topics, just as the use of `topics.regex` does. The regular expressions cannot be ambiguous — any matched topic must match only a single target table.

    Important

    If the `snowflake.topic2table.map` parameter is configured, Snowflake strongly recommends that you upgrade to version 3.1.0 of the connector.
    For more information about the Snowflake Connector for Kafka releases, see  [release notes](/release-notes/clients-drivers/kafka-connector).

    Example:

    Copy code

    ```
    topics="topic1,topic2,topic5,topic6"
    snowflake.topic2table.map="topic1:low_range,topic2:low_range,topic5:high_range,topic6:high_range"
    ```

    could be written as:

    Copy code

    ```
    topics.regex="topic[0-9]"
    snowflake.topic2table.map="topic[0-4]:low_range,topic[5-9]:high_range"
    ```

`buffer.count.records`
:   Number of records buffered in memory per Kafka partition before ingesting to Snowflake. The default value is `10000` records.

`buffer.flush.time`
:   Number of seconds between buffer flushes, where the flush is from the Kafka’s memory cache to the internal stage. The default value is `120` seconds.

`buffer.size.bytes`
:   Cumulative size in bytes of records buffered in memory per the Kafka partition before they are ingested in Snowflake as data files. The default value for this is `5000000` (5 MB).

    The records are compressed when they are written to data files. As a result, the size of the records in the buffer may be larger than the size of the data files created from the records.

`value.converter.schema.registry.url`
:   If the format is Avro and you are using a Schema Registry Service, this should be the URL of the Schema Registry Service. Otherwise this field should be empty.

`value.converter.break.on.schema.registry.error`
:   If loading Avro data from the Schema Registry Service, this property determines if the Kafka connector should stop consuming records if it encounters an error while fetching the schema id. The default value is `false`. Set the value to `true` to enable this behavior.

    Supported by Kafka connector version 1.4.2 (and higher).

`jvm.proxy.host`
:   To enable the Snowflake Kafka Connector to access Snowflake through a proxy server, set this parameter to specify the host of that proxy server.

`jvm.proxy.port`
:   To enable the Snowflake Kafka Connector to access Snowflake through a proxy server, set this parameter to specify the port of that proxy server.

`jvm.proxy.username`
:   Username that authenticates with the proxy server.

    Supported by Kafka connector version 1.4.4 (and higher).

`jvm.proxy.password`
:   Password for the username that authenticates with the proxy server.

    Supported by Kafka connector version 1.4.4 (and higher).

`snowflake.jdbc.map`
:   Example: `"snowflake.jdbc.map": "networkTimeout:20,tracing:WARNING"`

    Additional JDBC properties (see [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters)) are not validated. These additional properties
    are not validated, and must not override nor be used instead of required properties such as: `jvm.proxy.xxx`,
    `snowflake.user.name`, `snowflake.private.key`, `snowflake.schema.name` etc.

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

    Supported by the Kafka connector 1.2.0 (and higher).

`snowflake.metadata.topic`
:   If value is set to FALSE, the `topic` property value is omitted from the metadata in the RECORD\_METADATA column. The default value is TRUE.

    Supported by the Kafka connector 1.2.0 (and higher).

`snowflake.metadata.offset.and.partition`
:   If value is set to FALSE, the `Offset` and `Partition` property values are omitted from the metadata in the RECORD\_METADATA column. The default value is TRUE.

    Supported by the Kafka connector 1.2.0 (and higher).

`snowflake.metadata.all`
:   If value is set to FALSE, the metadata in the RECORD\_METADATA column is completely empty. The default value is TRUE.

    Supported by the Kafka connector 1.2.0 (and higher).

`transforms`
:   Specify to skip tombstone records encountered by the Kafka connector and not load them into the target table. A tombstone record is
    defined as a record where the entire value field is null.

    Set the property value to `"tombstoneHandlerExample"`.

    Note

    Use this property with the Kafka community converters (i.e. `value.converter` property value) only (e.g.
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

`snowflake.snowpipe.v2CleanerEnabled`
:   Specifies whether to run the improved version of stage file cleaner for Snowpipe ingestion method. The old cleaner had some limitations, which caused some of the files to be left on stage.

    This property is supported by the Kafka connector version 2.2.2 and later.

    Values:
    :   - `true`
        - `false`

    Default:
    :   `true` for versions 2.3.0 and later, `false` for version 2.2.2

`snowflake.snowpipe.v2CleanerIntervalSeconds`
:   Specifies how often the new file cleaner is run. For cost optimization purposes, Snowflake recommends that you increase the parameter value significantly, for example, to 30 minutes, if a small number of messages are being processed.

    This property is supported by the Kafka connector version 2.2.2 and later.

    Values:
    :   - Minimum: `1`
        - Maximum: No upper limit

    Default:
    :   `61` seconds

`snowflake.streaming.channel.name.include.connector.name`
:   When enabled, Snowflake Streaming channel names are prefixed with the connector name.
    This option enables or disables usage of channel names that were used in Kafka Connector versions 2.1.0 and 2.1.1 and are intended for users that previously used these versions and have not updated the connector.

    Supported by the Kafka connector 3.4.0 (and higher).

    Important

    Enabling this option when updating from versions other than 2.1.0 or 2.1.1 may result in data duplication.
    Cannot be used together with `enable.streaming.channel.offset.migration=true`

    Values:
    :   - `true`
        - `false`

    Default:
    :   `false`

`enable.streaming.channel.offset.migration`
:   This option is used to enable or disable streaming channel offset migration logic.
    When `true`, offset tokens are migrated from V2 channel name format V2 to V1 channel name format.
    The V2 channel name format was used in Kafka Connector versions 2.1.0 and 2.1.1 only and is deprecated.
    V1 format is used unless V2 format is enabled using `snowflake.streaming.channel.name.include.connector.name = true`.
    Disabling this option might have side effects.
    Please consult Snowflake support before disabling this option.

    Channel name formats:
    :   - V1 - `[topic]_[partition]`, used in all versions except 2.1.0 and 2.1.1
        - V2 - `[connectorName]_[topic]_[partition]`, used in versions 2.1.0 and 2.1.1. Can be used in 3.4.0 and later — Please see `snowflake.streaming.channel.name.include.connector.name`.

    Values:
    :   - `true`
        - `false`

    Default:
    :   `true` for versions from 2.1.2 until 3.4.0, `false` for version 3.4.0 and later

### Using key pair authentication & key rotation

The Kafka connector relies on key pair authentication rather than basic authentication (i.e. username and password). This authentication method requires a 2048-bit (minimum) RSA key pair.
Generate the public-private key pair using OpenSSL. The public key is assigned to the Snowflake user defined in the configuration file.

After completing the key pair authentication instructions on this page and the instructions for [key pair rotation](/user-guide/key-pair-auth), evaluate the recommendation for [Externalizing Secrets](#externalizing-secrets) (in this topic).

To configure the public/private key pair:

1. From the command line in a terminal window, generate a private key.

   You can generate either an encrypted version or unencrypted version of the private key.

   Note

   The Kafka connector supports encryption algorithms that are validated to meet the Federal Information Processing Standard (140-2) (i.e. FIPS 140-2) requirements. For more information, see [FIPS 140-2](https://csrc.nist.gov/publications/detail/fips/140/2/final).

   To generate an unencrypted version, use the following command:

   Copy code

   ```
   $ openssl genrsa -out rsa_key.pem 2048
   ```

   To generate an encrypted version, use the following command:

   Copy code

   ```
   $ openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 <algorithm> -inform PEM -out rsa_key.p8
   ```

   Where `<algorithm>` is a FIPS 140-2 compliant encryption algorithm.

   For example, to specify AES 256 as the encryption algorithm:

   Copy code

   ```
   $ openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 aes256 -inform PEM -out rsa_key.p8
   ```

   If you generate an encrypted version of the private key, record the passphrase. Later, you will specify the passphrase in the `snowflake.private.key.passphrase` property in the Kafka configuration file.

   **Sample PEM private key**

   Copy code

   ```
   -----BEGIN ENCRYPTED PRIVATE KEY-----
   MIIE6TAbBgkqhkiG9w0BBQMwDgQILYPyCppzOwECAggABIIEyLiGSpeeGSe3xHP1
   wHLjfCYycUPennlX2bd8yX8xOxGSGfvB+99+PmSlex0FmY9ov1J8H1H9Y3lMWXbL
   ...
   -----END ENCRYPTED PRIVATE KEY-----
   ```
2. From the command line, generate the public key by referencing the private key:

   Assuming the private key is encrypted and contained in the file named `rsa_key.p8`, use the following command:

   Copy code

   ```
   $ openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
   ```

   **Sample PEM public key**

   Copy code

   ```
   -----BEGIN PUBLIC KEY-----
   MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy+Fw2qv4Roud3l6tjPH4
   zxybHjmZ5rhtCz9jppCV8UTWvEXxa88IGRIHbJ/PwKW/mR8LXdfI7l/9vCMXX4mk
   ...
   -----END PUBLIC KEY-----
   ```
3. Copy the public and private key files to a local directory for storage. Record the path to the files. Note that the private key is stored using the PKCS#8 (Public Key Cryptography Standards) format
   and is encrypted using the passphrase you specified in the previous step; however, the file should still be protected from unauthorized access using the file permission mechanism provided by your
   operating system. It is your responsibility to secure the file when it is not being used.
4. Log into Snowflake. Assign the public key to the Snowflake user using [ALTER USER](/sql-reference/sql/alter-user). For example:

   Copy code

   ```
   ALTER USER jsmith SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
   ```

   Note

   - Only security administrators (i.e. users with the SECURITYADMIN role) or higher can alter a user.
   - Exclude the public key header and footer in the SQL statement.

   Verify the user’s public key fingerprint using [DESCRIBE USER](/sql-reference/sql/desc-user):

   Copy code

   ```
   DESC USER jsmith;
   +-------------------------------+-----------------------------------------------------+---------+-------------------------------------------------------------------------------+
   | property                      | value                                               | default | description                                                                   |
   |-------------------------------+-----------------------------------------------------+---------+-------------------------------------------------------------------------------|
   | NAME                          | JSMITH                                              | null    | Name                                                                          |
   ...
   ...
   | RSA_PUBLIC_KEY_FP             | SHA256:nvnONUsfiuycCLMXIEWG4eTp4FjhVUZQUQbNpbSHXiA= | null    | Fingerprint of user's RSA public key.                                         |
   | RSA_PUBLIC_KEY_2_FP           | null                                                | null    | Fingerprint of user's second RSA public key.                                  |
   +-------------------------------+-----------------------------------------------------+---------+-------------------------------------------------------------------------------+
   ```

   Note

   The `RSA_PUBLIC_KEY_2_FP` property is described in [Configuring key-pair rotation](/user-guide/key-pair-auth#label-key-pair-rotation).
5. Copy and paste the entire private key into the `snowflake.private.key` field in the configuration file. Save the file.

### Using external OAuth

The connector supports External OAuth, described in the section [External OAuth overview](/user-guide/oauth-ext-overview), but it works with [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) only.

To configure the connector, use these configuration properties. All of them are required.

`snowflake.authenticator`
:   Indicate you intend to use `oauth`. Use `oauth` value.

`snowflake.oauth.client.id`
:   The client ID associated with the OAuth app.

`snowflake.oauth.client.secret`
:   The client secret associated with the OAuth app.

`snowflake.oauth.refresh.token`
:   The refresh token used to exchange for an access token.

`snowflake.oauth.token.endpoint`
:   The endpoint used for exchanging the refresh token for the access token. You need to specify your OAuth server’s authorization endpoint.

#### Externalizing secrets

Snowflake strongly recommends externalizing secrets such as the private key and storing them in an encrypted form or in a key management service such as AWS Key Management Service (KMS), Microsoft Azure Key Vault,
or HashiCorp Vault. This can be accomplished by using a `ConfigProvider` implementation on your Kafka Connect cluster.

For more information, see the Confluent description of this [service](https://docs.confluent.io/current/connect/security.html#externalizing-secrets).

## Starting Kafka

Start Kafka using the instructions provided in the third-party Confluent or Apache Kafka documentation.

## Starting the Kafka connector

You can start the Kafka connector in either distributed mode or standalone mode. Instructions for each are shown below:

### Distributed mode

In a terminal window, execute the following command:

Copy code

```
curl -X POST -H "Content-Type: application/json" --data @<path>/<config_file>.json http://localhost:8083/connectors
```

### Standalone mode

In a terminal window, execute the following command:

Copy code

```
<kafka_dir>/bin/connect-standalone.sh <kafka_dir>/<path>/connect-standalone.properties <kafka_dir>/config/SF_connect.properties
```

(A default installation of Apache Kafka or Confluent Kafka should already have the file `connect-standalone.properties`.)

## Testing and using the Kafka connector

We recommend testing the Kafka connector with a small amount of data before using the connector in a production system. The process for testing is the same
as the process for using the connector normally:

1. Verify that Kafka and Kafka Connect are running.
2. Verify that you have created the appropriate Kafka topic.
3. Create (or use an existing) message publisher. Make sure that the messages published to the topic have the right format (JSON, Avro, or plain text).
4. Create a configuration file that specifies the topic to subscribe to and the Snowflake table to write to. For instructions, see [Configuring the Kafka Connector](#configuring-the-kafka-connector) (in this topic).
5. (Optional) Create a table into which to write data. This step is optional; if you do not create the table, the Kafka connector creates the table for you. If you do not plan to
   use the connector to add data to an existing, non-empty table, then we recommend that you let the connector create the table for you to minimize the possibility of a
   schema mismatch.
6. Grant the minimum privileges required on the Snowflake objects (database, schema, target table, etc.) to the role that will be used to ingest data.
7. Publish a sample set of data to the configured Kafka topic.
8. Wait a few minutes for data to propagate through the system, and then check the Snowflake table to verify that the records were inserted.

Tip

Consider verifying your network connection to Snowflake using [SnowCD](/user-guide/snowcd) before loading data to Snowflake in your test and production environments.
