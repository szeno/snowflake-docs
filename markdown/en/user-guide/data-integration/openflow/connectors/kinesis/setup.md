# Set up Openflow Connector for Amazon Kinesis Data Streams

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to set up Openflow Connector for Amazon Kinesis Data Streams.

Openflow Connector for Amazon Kinesis Data Streams is designed for JSON message ingestion from Kinesis streams to Snowflake tables, with schema evolution capabilities.

## Set up the Openflow Connector for Kinesis

### Prerequisites

1. Review [Openflow Connector for Amazon Kinesis Data Streams](/user-guide/data-integration/openflow/connectors/kinesis/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If you are using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the Kinesis connector.

### Set up IAM roles and policies in AWS

As an AWS administrator, perform the following actions in your AWS account:

1. Create an AWS IAM user or role that Openflow will use to access the Kinesis data stream. For more information, see
   [Creating IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) in the AWS documentation.
2. Ensure that the AWS user has configured [Access Key credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).
3. Grant the AWS user the following IAM permissions:

   | Service | Actions | Resources (ARNs) | Purpose |
   | --- | --- | --- | --- |
   | Amazon Kinesis Data Streams | `kinesis:DescribeStream`, `kinesis:DescribeStreamConsumer`, `kinesis:GetRecords`, `kinesis:GetShardIterator`, `kinesis:ListShards`, `kinesis:RegisterStreamConsumer` | `arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/${STREAM_NAME}` | Discovers shards, reads records through shared-throughput polling, resolves the stream ARN, registers an Enhanced Fan-Out consumer, and polls consumer status during registration. |
   | Amazon Kinesis Data Streams | `kinesis:DeregisterStreamConsumer`, `kinesis:DescribeStreamConsumer`, `kinesis:SubscribeToShard` | `arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/${STREAM_NAME}/consumer/*` | Describes, subscribes to, and deregisters Enhanced Fan-Out consumers by consumer ARN. |
   | Amazon DynamoDB | `dynamodb:CreateTable`, `dynamodb:DeleteTable`, `dynamodb:DescribeTable`, `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:Query`, `dynamodb:Scan`, `dynamodb:UpdateItem` | `arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/${APPLICATION_NAME}`, `arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/${APPLICATION_NAME}_migration` | Creates and manages the checkpoint/lease table (shard leases, node heartbeats, checkpoints) and a temporary migration table used during one-time migration from legacy checkpoint tables. |

   Expand

   Show lessSee more

   Example IAM policy:

   Copy code

   ```
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KinesisStreamAccess",
            "Effect": "Allow",
            "Action": [
                "kinesis:DescribeStream",
                "kinesis:DescribeStreamConsumer",
                "kinesis:GetRecords",
                "kinesis:GetShardIterator",
                "kinesis:ListShards",
                "kinesis:RegisterStreamConsumer"
            ],
            "Resource": "arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/${STREAM_NAME}"
        },
        {
            "Sid": "KinesisConsumerAccess",
            "Effect": "Allow",
            "Action": [
                "kinesis:DeregisterStreamConsumer",
                "kinesis:DescribeStreamConsumer",
                "kinesis:SubscribeToShard"
            ],
            "Resource": "arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/${STREAM_NAME}/consumer/*"
        },
        {
            "Sid": "DynamoDBTableAccess",
            "Effect": "Allow",
            "Action": [
                "dynamodb:CreateTable",
                "dynamodb:DeleteTable",
                "dynamodb:DescribeTable",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/${APPLICATION_NAME}",
                "arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/${APPLICATION_NAME}_migration"
            ]
        }
    ]
   }
   ```

   Before using the example policy, replace the following placeholders:

   | Placeholder | Description |
   | --- | --- |
   | `${REGION}` | Your AWS region (for example, `us-east-1`) |
   | `${ACCOUNT_ID}` | Your AWS account ID (for example, `123456789012`) |
   | `${STREAM_NAME}` | The value of the **AWS Kinesis Stream Name** connector parameter |
   | `${APPLICATION_NAME}` | The value of the **AWS Kinesis Application Name** connector parameter. Used as the DynamoDB checkpoint table name and as the Enhanced Fan-Out registered consumer name. |

   Expand

   Show lessSee more

   Note

   - The `${APPLICATION_NAME}_migration` table is a temporary DynamoDB table created only
     during a one-time migration from legacy checkpoint tables to the new schema. It’s deleted
     automatically when migration completes. If your deployment has never used the legacy
     KCL-based connector, you can omit the migration table ARN from the policy.
   - The `dynamodb:DeleteTable` action is used during the migration process and can be removed
     from the policy after migration is confirmed complete.
   - The `kinesis:DeregisterStreamConsumer` action is invoked when the processor is removed
     from the canvas. If the IAM principal doesn’t have this permission, the consumer must be
     deregistered manually through the AWS console or CLI.

### Set up Snowflake account

As a Snowflake account administrator, perform the following tasks:

1. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property).
2. Create a new role or use an existing role and grant the [database privileges](/sql-reference/sql/grant-privilege).

   The connector requires the user to create the destination table. Make sure the user has the required privileges for managing Snowflake objects:

   | Object | Privilege | Notes |
   | --- | --- | --- |
   | Database | USAGE |  |
   | Schema | USAGE |  |
   | Table | OWNERSHIP | Required for the connector to ingest data into a table. |

   Expand

   Show lessSee more

   Snowflake recommends creating a separate user and role for each Kinesis stream for better access control.

   You can use the following script to create and configure a custom role (requires SECURITYADMIN or equivalent):

   Copy code

   ```
   USE ROLE securityadmin;

   CREATE ROLE openflow_kinesis_connector_role_1;
   GRANT USAGE ON DATABASE kinesis_db TO ROLE openflow_kinesis_connector_role_1;
   GRANT USAGE ON SCHEMA kinesis_schema TO ROLE openflow_kinesis_connector_role_1;
   ```

   Note

   Privileges must be granted directly to the connector role and can’t be inherited.
3. Configure the destination table

   Snowflake recommends using server-side schema evolution for schema changes and
   [an error table for DML error logging](#label-kinesis-dml-error-logging).

   The example below shows how to create a table and add OWNERSHIP permissions.

   Copy code

   ```
   USE ROLE openflow_kinesis_connector_role_1;

   CREATE TABLE kinesis_db.kinesis_schema.<DESTINATION_TABLE_NAME> (
     kinesisMetadata object
   )
   ENABLE_SCHEMA_EVOLUTION = TRUE
   ERROR_LOGGING = TRUE;

   USE ROLE securityadmin;
   GRANT OWNERSHIP ON TABLE <DESTINATION_TABLE_NAME> TO ROLE openflow_kinesis_connector_role_1;
   ```

   This connector provides support for automatic schema detection and evolution. The structure of tables in Snowflake is defined and evolved automatically to support the structure of new data loaded by the connector. It will automatically map the record content’s first-level keys to table columns matching by name (case-insensitive).

   With Schema evolution enabled, Snowflake can automatically expand the destination table by adding new columns that are detected in the incoming stream and dropping NOT NULL constraints to accommodate new data patterns. For more information, see [Table schema evolution](/user-guide/data-load-schema-evolution).

   If ENABLE\_SCHEMA\_EVOLUTION is not enabled, then you have to create the schema manually by extending the table definition. The connector tries to match the record content’s first-level keys to the table columns by name. If keys from the JSON do not match the table columns, the connector ignores the keys.
4. (Optional) Configure a secrets manager

   Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow, for example, AWS, Azure, and HashiCorp, and store the public and private keys in the secret store.

   1. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, it’s recommended that you use the EC2 instance role associated with Openflow as this way no other secrets have to be persisted.
   2. In the Openflow canvas, configure a Parameter Provider associated with this Secrets Manager, from the hamburger menu in the upper right. Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.
   3. At this point all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
5. Grant access to users

   Any other Snowflake users who require access to the raw ingested data by the connector (for example, for custom processing in Snowflake), should be granted the role created in step 2.

### (Optional) Configure outbound AWS PrivateLink

If you’re running the connector in Openflow - Snowflake Deployments and want to route the connector’s Kinesis traffic over
[outbound private connectivity](/user-guide/private-connectivity-outbound) (AWS PrivateLink) instead of the public internet,
follow the steps in this section.

The connector makes outbound calls to the following AWS services:

| Service | Purpose | PrivateLink support |
| --- | --- | --- |
| Amazon Kinesis Data Streams | Reads stream records. | Supported by this connector. |
| Amazon DynamoDB | Stores checkpoint metadata for processed records. | Not supported. Use the public endpoint. |

Expand

Show lessSee more

Important

Amazon DynamoDB doesn’t support Private DNS for its PrivateLink endpoint. See
[Considerations when using AWS PrivateLink for Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/privatelink-interface-endpoints.html#privatelink-considerations)
in the AWS documentation. Because Snowflake’s `PRIVATE_HOST_PORT` network rule type relies on Private DNS, the connector
can’t route DynamoDB traffic through a PrivateLink endpoint. Configure DynamoDB using `HOST_PORT` (public endpoint)
as shown in the example. Only checkpoint metadata flows through the public endpoint to DynamoDB. Stream records flow through the private Kinesis endpoint.

To configure outbound AWS PrivateLink, complete the following steps:

1. As ACCOUNTADMIN, provision an outbound PrivateLink endpoint for Amazon Kinesis Data Streams in the region where your stream is located. Replace `<region>` with your AWS region (for example, `us-east-1`):

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.<region>.kinesis-streams',
     'kinesis.<region>.amazonaws.com'
   );
   ```

   For more information, see [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) and [Managing outbound private connectivity endpoints on AWS](/user-guide/private-manage-endpoints-aws).
2. Create network rules that reach `kinesis.<region>.amazonaws.com` through the private endpoint and DynamoDB through the public endpoint. Replace `<openflow_network_schema>` with the schema you use to host network rules:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   USE SCHEMA <openflow_network_schema>;

   CREATE OR REPLACE NETWORK RULE openflow_kinesis_private_network_rule
     MODE = EGRESS
     TYPE = PRIVATE_HOST_PORT
     VALUE_LIST = ('kinesis.<region>.amazonaws.com');

   CREATE OR REPLACE NETWORK RULE openflow_kinesis_public_network_rule
     MODE = EGRESS
     TYPE = HOST_PORT
     VALUE_LIST = ('dynamodb.<region>.amazonaws.com:443');
   ```
3. Attach both network rules to an external access integration, then grant the execute-as role permission to use the integration:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION openflow_kinesis_eai
     ALLOWED_NETWORK_RULES = (
       openflow_kinesis_private_network_rule,
       openflow_kinesis_public_network_rule
     )
     ENABLED = TRUE
     COMMENT = 'External access integration for the Openflow Connector for Kinesis';

   GRANT USAGE ON INTEGRATION openflow_kinesis_eai TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

   For the steps to associate the integration with a runtime, see
   [Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).

### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

#### Install the connector

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the **Openflow connector for Amazon Kinesis Data Streams** and select **Install**.
3. In the Select runtime dialog, select your runtime from the **Available runtimes** drop-down list and click **Add**.

   Note

   Before you install the connector, ensure that you have created a database, schema, and a table in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

   The Openflow canvas appears with the connector process group added to it.

#### Configure the connector

1. If needed, customize the connector configuration before configuring the built-in parameters.
2. Populate the process group parameters
   1. Right-click on the imported process group and select **Parameters**.
   2. Fill out the required parameter values.

##### Common parameters

| Parameter | Description | Required |
| --- | --- | --- |
| AWS Access Key ID | The AWS Access Key ID to connect to your Kinesis Stream and DynamoDB. | Yes |
| AWS Kinesis Region | The AWS Region to connect to. Use regular AWS region format, for example: `us-west-2`, `ap-southeast-1`, `eu-west-1`. See the [AWS Regions](https://docs.aws.amazon.com/general/latest/gr/rande.html#kinesis_region) page. | Yes |
| AWS Secret Access Key | The AWS Secret Access Key to connect to your Kinesis Stream and DynamoDB. | Yes |
| AWS Kinesis Application Name | The name that is used as the DynamoDB table name for tracking the application’s progress on Kinesis Stream consumption. | Yes |
| AWS Kinesis Consumer Type | The strategy used to read records from a Kinesis Stream.  Must be one of the following values: **SHARED\_THROUGHPUT**, **ENHANCED\_FAN\_OUT**.  For more information, see [Differences between shared throughput consumer and enhanced fan-out consumer](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html). | Yes |
| AWS Kinesis Initial Stream Position | The initial stream position from which the data starts replication. This takes effect only during the initial start for a given AWS Kinesis Application Name.  Possible values are:  **LATEST**: Latest stored record,  **TRIM\_HORIZON**: Earliest stored record. | Yes |
| AWS Kinesis Stream Name | The AWS Kinesis Stream Name to consume data from. | Yes |
| Snowflake Destination Database | The database where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Snowflake Destination Schema | The schema where data will be persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME`.  `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively. | Yes |
| Snowflake Destination Table | The table where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |

Expand

Show lessSee more

#### Start the connector

1. Right-click on the canvas and select **Enable all Controller Services**.
2. Right-click on the canvas and select **Start**. The connector starts data ingestion.

## Understanding the KINESISMETADATA column

The connector populates the KINESISMETADATA structure with metadata about the Kinesis record. The structure contains the following information:

| Field Name | Field Type | Example Value | Description |
| --- | --- | --- | --- |
| stream | String | `stream-name` | The name of the Kinesis stream the record came from. |
| shardId | String | `shardId-000000000001` | The identifier of the shard in the stream the record came from. |
| approximateArrival | Number | `1782092074893` | The approximate time that the record was inserted into the stream, as a Unix timestamp in epoch milliseconds. |
| partitionKey | String | `key-1234` | The partition key specified by the data producer for the record. |
| sequenceNumber | String | `123456789` | The unique sequence number assigned by Kinesis Data Streams to the record in the shard. |
| subSequenceNumber | Number | `2` | The subsequence number for the record (used for aggregated records with the same sequence number). |
| shardedSequenceNumber | String | `12345678900002` | A combination of the sequence number and the subsequence number for the record. |

Expand

Show lessSee more

## Measuring ingestion latency

For change tracking, incremental processing, and Time Travel queries based on row modification time, the ROW\_TIMESTAMP feature can be used.

It can be enabled by running the following command on your destination table:

Copy code

```
ALTER TABLE <DESTINATION_TABLE> SET ROW_TIMESTAMP = TRUE;
```

After row timestamps are enabled, tables expose the `METADATA$ROW_LAST_COMMIT_TIME` column, which returns the timestamp when each row was last modified.

For more information, see [Row timestamps](/user-guide/data-engineering/row-timestamps).

Note

Row timestamp isn’t available for interactive tables. For more information, see [Limitations of interactive tables](/user-guide/interactive#label-limitations-of-interactive-tables).

## Using the connector with Apache Iceberg™ tables

The connector can ingest data into a Snowflake-managed Apache Iceberg™ table.

The connector doesn’t create Iceberg tables automatically. You must create the Iceberg table manually before you run the connector.

The connector supports server-side schema evolution for Iceberg destination tables, the same way it does for standard Snowflake tables. When the destination table has `ENABLE_SCHEMA_EVOLUTION = TRUE`, Snowflake automatically adds new columns that are detected in the incoming stream and drops NOT NULL constraints to accommodate new data patterns. For more information about how schema evolution behaves, see [Table schema evolution](/user-guide/data-load-schema-evolution).

The Iceberg table can use either of the following storage options:

- [Snowflake storage](/user-guide/tables-iceberg-internal-storage): Snowflake stores and manages the Iceberg table files for you, so you don’t need to create an external volume or grant the connector access to it.
- External cloud storage that you manage, accessed through an external volume. You must grant the connector role USAGE on the external volume.

### Grant usage on an external volume

This step applies only when the Iceberg table uses an external volume that you manage. If the table uses [Snowflake storage](/user-guide/tables-iceberg-internal-storage), skip this step.

For example, if your Iceberg table uses the `kinesis_external_volume` external volume and the connector uses the role `openflow_kinesis_connector_role_1`, run the following statement:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT USAGE ON EXTERNAL VOLUME kinesis_external_volume TO ROLE openflow_kinesis_connector_role_1;
```

### Create an Apache Iceberg™ table for ingestion

When you create an Iceberg table, you can use Iceberg data types (including VARIANT) or
[compatible Snowflake types](/user-guide/tables-iceberg-data-types).

For example, consider the following message:

Copy code

```
{
  "id": 1,
  "name": "Steve",
  "body_temperature": 36.6,
  "approved_coffee_types": ["Espresso", "Doppio", "Ristretto", "Lungo"],
  "animals_possessed": {
    "dogs": true,
    "cats": false
  },
  "options": {
    "can_walk": true,
    "can_talk": false
  },
  "date_added": "2024-10-15"
}
```

To create an Iceberg table for the example message, use one of the following statements.

To use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), set `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` and omit `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  kinesisMetadata OBJECT(
    stream STRING,
    shardId STRING,
    approximateArrival STRING,
    partitionKey STRING,
    sequenceNumber STRING,
    subSequenceNumber INTEGER,
    shardedSequenceNumber STRING
  ),
  id INT,
  name string,
  body_temperature float,
  approved_coffee_types array(string),
  animals_possessed variant,
  date_added date,
  options object(can_walk boolean, can_talk boolean)
)
EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
CATALOG = 'SNOWFLAKE'
ICEBERG_VERSION = 3;
```

To use your own external volume, set `EXTERNAL_VOLUME` to the volume name and provide a `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  kinesisMetadata OBJECT(
    stream STRING,
    shardId STRING,
    approximateArrival BIGINT,
    partitionKey STRING,
    sequenceNumber STRING,
    subSequenceNumber INTEGER,
    shardedSequenceNumber STRING
  ),
  id INT,
  name string,
  body_temperature float,
  approved_coffee_types array(string),
  animals_possessed variant,
  date_added date,
  options object(can_walk boolean, can_talk boolean)
)
EXTERNAL_VOLUME = 'my_volume'
CATALOG = 'SNOWFLAKE'
BASE_LOCATION = 'my_location/my_iceberg_table'
ICEBERG_VERSION = 3;
```

## Using the connector with Interactive Tables

Interactive tables are a special type of Snowflake table optimized for low-latency, high-concurrency queries. You can find out more about interactive tables in the [interactive tables documentation](/user-guide/interactive).

1. Create an interactive table:

   Copy code

   ```
   CREATE INTERACTIVE TABLE REALTIME_METRICS (
     metric_name VARCHAR,
     metric_value NUMBER,
     source_stream VARCHAR,
     approximate_arrival NUMBER
   ) CLUSTER BY (metric_name)
   AS (SELECT
     $1:M_NAME::VARCHAR,
     $1:M_VALUE::NUMBER,
     $1:kinesisMetadata.stream::VARCHAR,
     $1:kinesisMetadata.approximateArrival::NUMBER
   from TABLE(DATA_SOURCE(TYPE => 'STREAMING')));
   ```

Important considerations:

- Interactive tables have specific limitations and query restrictions. Review the [interactive tables documentation](/user-guide/interactive) before using them with the connector.
- For interactive tables, any required transformations must be handled in the table definition.
- Interactive warehouses are required to query interactive tables efficiently.

## Using the connector with a customer-defined schema for the destination table

The connector treats each Kinesis record as a row to be inserted into a Snowflake table. For example, if you have a Kinesis stream with the content of the message structured like the following JSON:

Copy code

```
{
  "order_id": 12345,
  "customer_name": "John",
  "order_total": 100.00,
  "isPaid": true
}
```

By default you don’t have to specify all fields from the JSON. Schema evolution will take care of it. However, if you prefer a static schema, it can be created by running:

Copy code

```
CREATE TABLE ORDERS (
  kinesisMetadata OBJECT,
  order_id NUMBER,
  customer_name VARCHAR,
  order_total FLOAT,
  ispaid BOOLEAN
);
```

## Using the connector with a customer-defined PIPE

If you choose to create your own pipe, you can define the data transformation logic in the pipe’s
[COPY INTO](/sql-reference/sql/copy-into-table) statement. You can rename columns as required and cast the data types as needed. For example:

Copy code

```
CREATE TABLE ORDERS (
  order_id VARCHAR,
  customer_name VARCHAR,
  order_total VARCHAR,
  ispaid VARCHAR
);

CREATE PIPE ORDERS AS
COPY INTO ORDERS
FROM (
  SELECT
    $1:order_id::STRING,
    $1:customer_name,
    $1:order_total::STRING,
    $1:isPaid::STRING
  FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);
```

When you define your own pipe your destination table columns do not have to match the JSON keys. You can rename the columns to your desired names and cast the data types if required.

To adjust the connector to work with a custom pipe, perform the following tasks:

1. Right-click on the PublishSnowpipeStreaming processor used in your Kinesis ingestion flow in the Openflow canvas.
2. Select **Configure** from the context menu.
3. Navigate to the **Properties** tab.
4. In the Destination type field, pick **Pipe**.
5. In the Pipe field, type the name of your pipe.
6. Select **Apply** to save the configuration.

## Customizing error handling

Error handling is split between Openflow-side failures and server-side failures within the Snowpipe Streaming service.

- **Openflow Errors (Client-Side Failures)**: Errors such as unparseable payloads or custom transformation failures occur before records reach Snowflake. By default these records are discarded. It’s possible to process these errors in Openflow - use FlowFiles from the parse failure relationship in the ConsumeKinesis processor. For a complete walkthrough, see [Kinesis as destination for DLQ messages](configuring-dead-letter-queue-handling) and the shared [Configuring Dead Letter Queue (DLQ) handling](/user-guide/data-integration/openflow/connectors/streaming/configuring-dead-letter-queue-handling).
- **Snowpipe Streaming Errors (Server-Side Failures)**: Errors for records that successfully reach Snowflake but are incompatible with the destination table’s schema (for example, type mismatches) are captured by the Snowflake infrastructure. When error logging is enabled on the destination table (`error_logging = true`), these failed rows are automatically ingested into the destination Error table.

## Next steps

- [Performance tuning of the Openflow Connector for Amazon Kinesis Data Streams](/user-guide/data-integration/openflow/connectors/kinesis/performance-tuning)
- [Maintain Openflow Connector for Amazon Kinesis Data Streams](/user-guide/data-integration/openflow/connectors/kinesis/maintenance)
- [Troubleshooting the Openflow Connector for Amazon Kinesis Data Streams](/user-guide/data-integration/openflow/connectors/kinesis/troubleshoot)
- [Openflow Connector for Kinesis Data Streams: Configuring DLQ handling](/user-guide/data-integration/openflow/connectors/kinesis/configuring-dead-letter-queue-handling)
- [Configuring custom transformations](/user-guide/data-integration/openflow/connectors/streaming/configuring-custom-transformations)
