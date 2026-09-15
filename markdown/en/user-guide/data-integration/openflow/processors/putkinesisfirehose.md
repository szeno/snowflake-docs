# PutKinesisFirehose 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Sends the contents to a specified Amazon Kinesis Firehose. In order to send data to firehose, the firehose delivery stream name has to be specified.

## Tags

amazon, aws, firehose, kinesis, put, stream

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Amazon Kinesis Firehose Delivery Stream Name | The name of kinesis firehose delivery stream |
| Batch Size | Batch size for messages (1-500). |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Max message buffer size | Max message buffer |
| Region |  |
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
| aws.kinesis.firehose.error.message | Error message on posting message to AWS Kinesis Firehose |
| aws.kinesis.firehose.error.code | Error code for the message when posting to AWS Kinesis Firehose |
| aws.kinesis.firehose.record.id | Record id of the message posted to Kinesis Firehose |

Expand

Show lessSee more
