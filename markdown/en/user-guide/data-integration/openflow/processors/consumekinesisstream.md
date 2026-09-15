# ConsumeKinesisStream 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Reads data from the specified AWS Kinesis stream and outputs a FlowFile for every processed Record (raw) or a FlowFile for a batch of processed records if a Record Reader and Record Writer are configured. At-least-once delivery of all Kinesis Records within the Stream while the processor is running. AWS Kinesis Client Library can take several seconds to initialise before starting to fetch data. Uses DynamoDB for check pointing and CloudWatch (optional) for metrics. Ensure that the credentials provided have access to DynamoDB and CloudWatch (optional) along with Kinesis.

## Tags

amazon, aws, consume, kinesis, stream

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Amazon Kinesis Stream Name | The name of Kinesis Stream |
| Application Name | The Kinesis stream reader application name. |
| Checkpoint Interval | Interval between Kinesis checkpoints |
| Communications Timeout |  |
| DynamoDB Override | DynamoDB override to use non-AWS deployments |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Failover Timeout | Kinesis Client Library failover timeout |
| FlowFile Handling On Schema Difference | The strategy used when records in a Kinesis Stream change their schema in a single batch. |
| Graceful Shutdown Timeout | Kinesis Client Library graceful shutdown timeout |
| Initial Stream Position | Initial position to read Kinesis streams. |
| Output Strategy | The format used to output the Kinesis Record into a FlowFile Record. |
| Record Reader | The Record Reader to use for reading received messages. The Kinesis Stream name can be referred to by Expression Language ‘${kinesis.name}’ to access a schema. If Record Reader/Writer are not specified, each Kinesis Record will create a FlowFile. |
| Record Writer | The Record Writer to use for serializing Records to an output FlowFile. The Kinesis Stream name can be referred to by Expression Language ‘${kinesis.name}’ to access a schema. If Record Reader/Writer are not specified, each Kinesis Record will create a FlowFile. |
| Region |  |
| Report Metrics to CloudWatch | Whether to report Kinesis usage metrics to CloudWatch. |
| Retry Count | Number of times to retry a Kinesis operation (process record, checkpoint, shutdown) |
| Retry Wait | Interval between Kinesis operation retries (process record, checkpoint, shutdown) |
| Stream Position Timestamp | Timestamp position in stream from which to start reading Kinesis Records. Required if Initial position to read Kinesis streams. is AT\_TIMESTAMP. Uses the Timestamp Format to parse value into a Date. |
| Timestamp Format | Format to use for parsing the Stream Position Timestamp into a Date and converting the Kinesis Record’s Approximate Arrival Timestamp into a FlowFile attribute. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles are routed to success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| aws.kinesis.partition.key | Partition key of the (last) Kinesis Record read from the Shard |
| aws.kinesis.shard.id | Shard ID from which the Kinesis Record was read |
| aws.kinesis.sequence.number | The unique identifier of the (last) Kinesis Record within its Shard |
| aws.kinesis.approximate.arrival.timestamp | Approximate arrival timestamp of the (last) Kinesis Record read from the stream |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer (if configured) |
| record.count | Number of records written to the FlowFiles by the Record Writer (if configured) |
| record.error.message | This attribute provides on failure the error message encountered by the Record Reader or Record Writer (if configured) |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.kinesis.stream.PutKinesisStream](/user-guide/data-integration/openflow/processors/putkinesisstream)
