# PutKinesisStream 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Sends the contents to a specified Amazon Kinesis. In order to send data to Kinesis, the stream name has to be specified.

## Tags

amazon, aws, kinesis, put, stream

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Max Message Buffer Size | Max message buffer size defined with standard data size units |
| Message Batch Size | Batch size for messages (1-500). |
| Region |  |
| Stream Name | The name of Kinesis Stream |
| Stream Partition Key | The partition key attribute. If it is not set, a random value is used |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| success | FlowFiles are routed to success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| aws.kinesis.error.message | Error message on posting message to AWS Kinesis |
| aws.kinesis.error.code | Error code for the message when posting to AWS Kinesis |
| aws.kinesis.sequence.number | Sequence number for the message when posting to AWS Kinesis |
| aws.kinesis.shard.id | Shard id of the message posted to AWS Kinesis |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.kinesis.stream.ConsumeKinesisStream](/user-guide/data-integration/openflow/processors/consumekinesisstream)
