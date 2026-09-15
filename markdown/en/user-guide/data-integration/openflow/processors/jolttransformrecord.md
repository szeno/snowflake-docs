# JoltTransformRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-jolt-nar

## Description

Applies a JOLT specification to each record in the FlowFile payload. A new FlowFile is created with transformed content and is routed to the ‘success’ relationship. If the transform fails, the original FlowFile is routed to the ‘failure’ relationship.

## Tags

cardinality, chainr, defaultr, jolt, record, removr, shiftr, sort, transform

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Custom Module Directory | Comma-separated list of paths to files and/or directories which contain modules containing custom transformations (that are not included on NiFi’s classpath). |
| Custom Transformation Class Name | Fully Qualified Class Name for Custom Transformation |
| Jolt Specification | Jolt Specification for transformation of JSON data. The value for this property may be the text of a Jolt specification or the path to a file containing a Jolt specification. ‘Jolt Specification’ must be set, or the value is ignored if the Jolt Sort Transformation is selected. |
| Jolt Transform | Specifies the Jolt Transformation that should be used with the provided specification. |
| Transform Cache Size | Compiling a Jolt Transform can be fairly expensive. Ideally, this will be done only once. However, if the Expression Language is used in the transform, we may need a new Transform for each FlowFile. This value controls how many of those Transforms we cache in memory in order to avoid having to compile the Transform each time. |
| jolt-record-record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema. |
| jolt-record-record-writer | Specifies the Controller Service to use for writing out the records |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, the FlowFile records cannot be parsed), it will be routed to this relationship |
| original | The original FlowFile that was transformed. If the FlowFile fails processing, nothing will be sent to this relationship |
| success | The FlowFile with transformed content will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The number of records in an outgoing FlowFile |
| mime.type | The MIME Type that the configured Record Writer indicates is appropriate |

Expand

Show lessSee more
