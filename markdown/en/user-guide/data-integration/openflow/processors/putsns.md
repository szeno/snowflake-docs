# PutSNS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Sends the content of a FlowFile as a notification to the Amazon Simple Notification Service

## Tags

amazon, aws, publish, pubsub, put, sns, topic

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| ARN Type | The type of Amazon Resource Name that is being used. |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Amazon Resource Name (ARN) | The name of the resource to which notifications should be published |
| Character Set | The character set in which the FlowFile’s content is encoded |
| Communications Timeout |  |
| Deduplication Message ID | The token used for deduplication of sent messages |
| E-mail Subject | The optional subject to use for any subscribers that are subscribed via E-mail |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Message Group ID | If using FIFO, the message group to which the flowFile belongs |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Use JSON Structure | If true, the contents of the FlowFile must be JSON with a top-level element named ‘default’. Additional elements can be used to send different messages to different protocols. See the Amazon SNS Documentation for more information. |
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

- [org.apache.nifi.processors.aws.sqs.GetSQS](/user-guide/data-integration/openflow/processors/getsqs)
- [org.apache.nifi.processors.aws.sqs.PutSQS](/user-guide/data-integration/openflow/processors/putsqs)
