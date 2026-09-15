# PutSQS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Publishes a message to an Amazon Simple Queuing Service Queue

## Tags

AWS, Amazon, Publish, Put, Queue, SQS

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Communications Timeout |  |
| Deduplication Message ID | The token used for deduplication of sent messages |
| Delay | The amount of time to delay the message before it becomes available to consumers |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Message Group ID | If using FIFO, the message group to which the FlowFile belongs |
| Queue URL | The URL of the queue to act upon |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
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

## See also

- [org.apache.nifi.processors.aws.sqs.DeleteSQS](/user-guide/data-integration/openflow/processors/deletesqs)
- [org.apache.nifi.processors.aws.sqs.GetSQS](/user-guide/data-integration/openflow/processors/getsqs)
