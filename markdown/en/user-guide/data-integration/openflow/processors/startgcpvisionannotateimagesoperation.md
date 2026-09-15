# StartGcpVisionAnnotateImagesOperation 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Trigger a Vision operation on image input. It should be followed by GetGcpVisionAnnotateImagesOperationStatus processor in order to monitor operation status.

## Tags

Cloud, Google, Machine Learning, Vision

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| gcp-credentials-provider-service | The Controller Service used to obtain Google Cloud Platform credentials. |
| json-payload | JSON request for AWS Machine Learning services. The Processor will use FlowFile content for the request when this property is not specified. |
| output-bucket | Name of the GCS bucket where the output of the Vision job will be persisted. The value of this property applies when the JSON Payload property is configured. The JSON Payload property value can use Expression Language to reference the value of ${output-bucket} |
| vision-feature-type | Type of GCP Vision Feature. The value of this property applies when the JSON Payload property is configured. The JSON Payload property value can use Expression Language to reference the value of ${vision-feature-type} |

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
| operationKey | A unique identifier of the operation returned by the Vision server. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.vision.GetGcpVisionAnnotateImagesOperationStatus](/user-guide/data-integration/openflow/processors/getgcpvisionannotateimagesoperationstatus)
