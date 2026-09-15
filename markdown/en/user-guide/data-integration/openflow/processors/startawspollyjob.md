# StartAwsPollyJob 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Trigger a AWS Polly job. It should be followed by GetAwsPollyJobStatus processor in order to monitor job status.

## Tags

AWS, Amazon, ML, Machine Learning, Polly

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| JSON Payload | JSON request for AWS Machine Learning services. The Processor will use FlowFile content for the request when this property is not specified. |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| original | Upon successful completion, the original FlowFile will be routed to this relationship. |
| success | FlowFiles are routed to success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| awsTaskId | The task ID that can be used to poll for Job completion in GetAwsPollyJobStatus |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.ml.polly.GetAwsPollyJobStatus](/user-guide/data-integration/openflow/processors/getawspollyjobstatus)
