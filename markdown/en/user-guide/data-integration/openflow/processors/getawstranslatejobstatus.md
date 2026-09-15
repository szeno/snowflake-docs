# GetAwsTranslateJobStatus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Retrieves the current status of an AWS Translate job.

## Tags

AWS, Amazon, ML, Machine Learning, Translate

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| AWS Task ID |  |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The job failed, the original FlowFile will be routed to this relationship. |
| original | Upon successful completion, the original FlowFile will be routed to this relationship. |
| running | The job is currently still being processed |
| success | Job successfully finished. FlowFile will be routed to this relation. |
| throttled | Retrieving results failed for some reason, but the issue is likely to resolve on its own, such as Provisioned Throughput Exceeded or a Throttling failure. It is generally expected to retry this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| outputLocation | S3 path-style output location of the result. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.ml.translate.StartAwsTranslateJob](/user-guide/data-integration/openflow/processors/startawstranslatejob)
