# JSLTTransformJSON 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-jslt-nar

## Description

Applies a JSLT transformation to the FlowFile JSON payload. A new FlowFile is created with transformed content and is routed to the ‘success’ relationship. If the JSLT transform fails, the original FlowFile is routed to the ‘failure’ relationship.

## Tags

jslt, json, transform

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| jslt-transform-cache-size | Compiling a JSLT Transform can be fairly expensive. Ideally, this will be done only once. However, if the Expression Language is used in the transform, we may need a new Transform for each FlowFile. This value controls how many of those Transforms we cache in memory in order to avoid having to compile the Transform each time. |
| jslt-transform-pretty\_print | Apply pretty-print formatting to the output of the JSLT transform |
| jslt-transform-result-filter | A filter for output JSON results using a JSLT expression. This property supports changing the default filter, which removes JSON objects with null values, empty objects and empty arrays from the output JSON. This JSLT must return true for each JSON object to be included and false for each object to be removed. Using a filter value of “true” to disables filtering. |
| jslt-transform-transformation | JSLT Transformation for transform of JSON data. Any NiFi Expression Language present will be evaluated first to get the final transform to be applied. The JSLT Tutorial provides an overview of supported expressions: <https://github.com/schibsted/jslt/blob/master/tutorial.md> |
| jslt-transform-transformation-strategy | Whether to apply the JSLT transformation to the entire FlowFile contents or each JSON object in the root-level array |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, the FlowFile is not valid JSON), it will be routed to this relationship |
| success | The FlowFile with transformed content will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Always set to application/json |

Expand

Show lessSee more
