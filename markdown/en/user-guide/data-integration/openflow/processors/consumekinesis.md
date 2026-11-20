# ConsumeKinesis 2026.11.12.16

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-kinesis-nar

## Description

Reads records from an Amazon Kinesis data stream, writes them to FlowFiles, and stores checkpoints in DynamoDB so processing can resume after a restart.

When a shard splits or multiple shards merge, the processor consumes parent and child shards concurrently. It doesn’t wait for parent shards to be fully consumed before reading child shards, so record ordering isn’t guaranteed across a split or merge boundary.

## Tags

amazon, aws, consume, kinesis, record, stream

## Input requirement

FORBIDDEN

## Supports sensitive dynamic properties

false

## Properties

Configure the stream connection, starting position, consumer behavior, and FlowFile output.

| Property | Description | Default and conditions |
| --- | --- | --- |
| Application Name | The Kinesis application name. The processor uses this value as the DynamoDB checkpoint table name and, for Enhanced Fan-Out, as the registered consumer name. The value should be unique for the stream. | Required |
| AWS Credentials Provider Service | The Controller Service used to obtain an AWS credentials provider. | Required |
| Consumer Type | The strategy for reading records. Shared Throughput consumers share 2 MB per second of read throughput per shard and use `GetRecords`. Enhanced Fan-Out consumers receive dedicated read throughput of up to 2 MB per second per shard and use `SubscribeToShard`. Enhanced Fan-Out has additional AWS charges and requires permissions to register and use a stream consumer. | Enhanced Fan-Out |
| Custom Region | A custom region, such as a region used by an AWS-compatible service provider. | Required only when Region is Use Custom Region. Supports JVM environment variables and system properties. |
| Endpoint Override URL | An optional endpoint override URL used for both the Kinesis and DynamoDB clients. | Optional |
| Initial Stream Position | The position in the stream where the processor starts reading. The allowable values are Trim Horizon, Latest, and At Timestamp. | Trim Horizon |
| Max Batch Duration | The maximum time spent consuming records in one invocation before committing the session and writing checkpoints. | 5 sec |
| Max Batch Size | The maximum amount of data consumed in one invocation before committing the session and writing checkpoints. | 10 MB |
| Max Records Per Request | The maximum number of records retrieved by each `GetRecords` request. The maximum allowed value is 10,000. | 100. Available only for Shared Throughput. |
| Message Demarcator | The UTF-8 string inserted between Kinesis messages written to the same FlowFile. | Required only when Processing Strategy is DEMARCATOR. |
| Output Strategy | Controls how parsed records and Kinesis metadata are represented: Use Content as Value, Use Wrapper, or Inject Metadata. | Use Content as Value. Available only when Processing Strategy is RECORD. |
| Processing Strategy | Controls how records are written: FLOW\_FILE, LINE\_DELIMITED, RECORD, or DEMARCATOR. | FLOW\_FILE |
| Proxy Configuration Service | The Proxy Configuration Controller Service used to proxy network requests. | Optional |
| Record Reader | The Record Reader used to parse data received from Kinesis. | Required only when Processing Strategy is RECORD. |
| Record Writer | The Record Writer used to serialize parsed records. | Required only when Processing Strategy is RECORD. |
| Region | The AWS Region where the Kinesis and DynamoDB services are located. | US West (Oregon), `us-west-2` |
| Stream Name | The name of the Kinesis data stream to consume. | Required |
| Stream Position Timestamp | The point in time where consumption starts, in ISO 8601 format. | Required only when Initial Stream Position is At Timestamp. |

Expand

Show lessSee more

## Record processing and output

The RECORD strategy uses the Record Reader and Record Writer and batches records with the same schema into a FlowFile. When the schema changes, the processor closes the current FlowFile and creates one for the new schema. This preserves record order within one shard across schema changes. A reader that infers schemas might identify many distinct schemas and cause excessive FlowFile creation. For more predictable performance, use a predefined schema or a schema registry.

The Output Strategy property applies only to RECORD processing:

- **Use Content as Value** writes only the fields produced by the Record Reader.
- **Use Wrapper** writes the parsed value under `value` and metadata under `kinesisMetadata`.
- **Inject Metadata** writes the parsed fields at the root and adds a `kinesisMetadata` sub-record.

The `kinesisMetadata` record identifies the stream, shard, sequence and subsequence numbers, sharded sequence number, partition key, and approximate arrival time. The `approximateArrival` value is a timestamp in milliseconds since the Unix epoch.

## Checkpointing

The configured AWS identity requires the following access:

- For all consumer types, list shards with `ListShards` on `arn:aws:kinesis:{Region}:{Account}:stream/{Stream Name}`.
- For Shared Throughput, read records with `GetRecords` and `GetShardIterator` on `arn:aws:kinesis:{Region}:{Account}:stream/{Stream Name}`.
- For Enhanced Fan-Out, resolve the stream ARN and register the consumer with `DescribeStream` and `RegisterStreamConsumer` on `arn:aws:kinesis:{Region}:{Account}:stream/{Stream Name}`.
- For Enhanced Fan-Out, manage and use the registered consumer with `DescribeStreamConsumer`, `SubscribeToShard`, and `DeregisterStreamConsumer` on `arn:aws:kinesis:{Region}:{Account}:stream/{Stream Name}/consumer/{Application Name}` and `arn:aws:kinesis:{Region}:{Account}:stream/{Stream Name}/consumer/{Application Name}:*`.
- For all consumer types, manage leases and checkpoints with `CreateTable`, `DescribeTable`, `GetItem`, `UpdateItem`, and `Query` on `arn:aws:dynamodb:{Region}:{Account}:table/{Application Name}`.
- For all consumer types, check for an unfinished checkpoint migration at startup with `DescribeTable` on `arn:aws:dynamodb:{Region}:{Account}:table/{Application Name}_migration`.
- When migrating a checkpoint table created by an earlier version of ConsumeKinesis, use `CreateTable`, `DeleteTable`, `Scan`, `GetItem`, `PutItem`, and `UpdateItem` on the `{Application Name}` and `{Application Name}_migration` DynamoDB tables.

An IAM policy that supports both consumer types should include the normal-operation permissions and `DescribeTable` on the migration table. Add the checkpoint-migration permissions only when you need to migrate a table created by an earlier ConsumeKinesis version.

## Consumer types

Shared Throughput consumers share a total read throughput of 2 MB per second per shard. Message propagation delay averages approximately 200 milliseconds with one consumer and approximately 1,000 milliseconds with five consumers.

Enhanced Fan-Out gives each registered consumer up to 2 MB per second of read throughput per shard, independently of other consumers. Message propagation delay averages approximately 70 milliseconds with one or five consumers. Enhanced Fan-Out incurs data retrieval and consumer-shard-hour costs.

## Relationships

Connect this relationship to route FlowFiles after the processor reads and writes Kinesis records.

| Name | Description |
| --- | --- |
| success | Routes FlowFiles created from records successfully read from Kinesis. |

Expand

Show lessSee more

## Writes attributes

The processor writes these attributes to identify the source records and describe each output FlowFile.

| Name | Description |
| --- | --- |
| aws.kinesis.stream.name | Name of the source Kinesis stream. |
| aws.kinesis.shard.id | Identifier of the source shard. |
| aws.kinesis.partition.key | Partition key of the last record in the FlowFile. |
| aws.kinesis.first.sequence.number | Sequence number of the first record in the FlowFile. |
| aws.kinesis.first.subsequence.number | Subsequence number of the first record in the FlowFile. |
| aws.kinesis.last.sequence.number | Sequence number of the last record in the FlowFile. |
| aws.kinesis.last.subsequence.number | Subsequence number of the last record in the FlowFile. |
| aws.kinesis.approximate.arrival.timestamp.ms | Approximate arrival time of the record or records, in milliseconds since the Unix epoch. |
| kinesis.millis.behind | Consumer lag behind the stream tail, in milliseconds. |
| mime.type | MIME type supplied by the configured Record Writer, when available. |
| record.count | Number of records written to the FlowFile. |
| record.error.message | Error message from the Record Reader or Record Writer, when available. |

Expand

Show lessSee more

## System resource considerations

- **CPU:** The processor uses additional CPU resources when consuming data from Kinesis.
- **Network:** The processor continually polls for new records.
- **Memory:** Records are fetched in the background and buffered until they can be written to FlowFiles. Up to 200 responses can be buffered per shard. At the default Shared Throughput settings, the theoretical maximum is 20,000 records or approximately 2 GB per shard. For Enhanced Fan-Out, the theoretical maximum is approximately 400 MB per shard. Actual buffers are usually smaller because fetch threads block when the queue is full and most responses are smaller than the maximum.
