# JoltTransformJSON 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-jolt-nar

## Description

Applies a list of Jolt specifications to either the FlowFile JSON content or a specified FlowFile JSON attribute. If the JSON transform fails, the original FlowFile is routed to the ‘failure’ relationship.

## Tags

cardinality, chainr, default, jolt, json, remove, shift, sort, transform

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Custom Module Directory | Comma-separated list of paths to files and/or directories which contain modules containing custom transformations (that are not included on NiFi’s classpath). |
| Custom Transformation Class Name | Fully Qualified Class Name for Custom Transformation |
| JSON Source | Specifies whether the Jolt transformation is applied to FlowFile JSON content or to specified FlowFile JSON attribute. |
| JSON Source Attribute | The FlowFile attribute containing JSON to be transformed. |
| Jolt Specification | Jolt Specification for transformation of JSON data. The value for this property may be the text of a Jolt specification or the path to a file containing a Jolt specification. ‘Jolt Specification’ must be set, or the value is ignored if the Jolt Sort Transformation is selected. |
| Jolt Transform | Specifies the Jolt Transformation that should be used with the provided specification. |
| Max String Length | The maximum allowed length of a string value when parsing the JSON document |
| Pretty Print | Apply pretty print formatting to the output of the Jolt transform |
| Transform Cache Size | Compiling a Jolt Transform can be fairly expensive. Ideally, this will be done only once. However, if the Expression Language is used in the transform, we may need a new Transform for each FlowFile. This value controls how many of those Transforms we cache in memory in order to avoid having to compile the Transform each time. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the JSON transformation fails (e.g., due to invalid JSON in the content or attribute), the original FlowFile is routed to this relationship. |
| success | The FlowFile with successfully transformed content or updated attribute will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Always set to application/json |

Expand

Show lessSee more
