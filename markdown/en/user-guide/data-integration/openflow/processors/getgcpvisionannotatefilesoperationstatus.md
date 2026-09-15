# GetGcpVisionAnnotateFilesOperationStatus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Retrieves the current status of an Google Vision operation.

## Tags

Cloud, Google, Machine Learning, Vision

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| gcp-credentials-provider-service | The Controller Service used to obtain Google Cloud Platform credentials. |
| operationKey | The unique identifier of the Vision operation. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| original | Upon successful completion, the original FlowFile will be routed to this relationship. |
| running | The job is currently still being processed |
| success | FlowFiles are routed to success relationship |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.vision.StartGcpVisionAnnotateFilesOperation](/user-guide/data-integration/openflow/processors/startgcpvisionannotatefilesoperation)
