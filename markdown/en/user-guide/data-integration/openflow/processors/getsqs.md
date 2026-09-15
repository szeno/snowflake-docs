# GetSQS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Fetches messages from an Amazon Simple Queuing Service Queue

## Tags

AWS, Amazon, Fetch, Get, Poll, Queue, SQS

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Auto Delete Messages | Specifies whether the messages should be automatically deleted by the processors once they have been received. |
| Batch Size | The maximum number of messages to send in a single network request |
| Character Set | The Character Set that should be used to encode the textual content of the SQS message |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Queue URL | The URL of the queue to get messages from |
| Receive Message Wait Time | The maximum amount of time to wait on a long polling receive call. Setting this to a value of 1 second or greater will reduce the number of SQS requests and decrease fetch latency at the cost of a constantly active thread. |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Visibility Timeout | The amount of time after a message is received but not deleted that the message is hidden from other consumers |
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
| hash.value | The MD5 sum of the message |
| hash.algorithm | MD5 |
| sqs.message.id | The unique identifier of the SQS message |
| sqs.receipt.handle | The SQS Receipt Handle that is to be used to delete the message from the queue |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.sqs.DeleteSQS](/user-guide/data-integration/openflow/processors/deletesqs)
- [org.apache.nifi.processors.aws.sqs.PutSQS](/user-guide/data-integration/openflow/processors/putsqs)
