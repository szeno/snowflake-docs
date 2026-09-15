# SplitRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Splits up an input FlowFile that is in a record-oriented data format into multiple smaller FlowFiles

## Tags

avro, csv, freeform, generic, json, log, logs, schema, split, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Record Reader | Specifies the Controller Service to use for reading incoming data |
| Record Writer | Specifies the Controller Service to use for writing out the records |
| Records Per Split | Specifies how many records should be written to each ‘split’ or ‘segment’ FlowFile |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile cannot be transformed from the configured input format to the configured output format, the unchanged FlowFile will be routed to this relationship. |
| original | Upon successfully splitting an input FlowFile, the original FlowFile will be sent to this relationship. |
| splits | The individual ‘segments’ of the original FlowFile will be routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer for the FlowFiles routed to the ‘splits’ Relationship. |
| record.count | The number of records in the FlowFile. This is added to FlowFiles that are routed to the ‘splits’ Relationship. |
| fragment.identifier | All split FlowFiles produced from the same parent FlowFile will have the same randomly generated UUID added for this attribute |
| fragment.index | A one-up number that indicates the ordering of the split FlowFiles that were created from a single parent FlowFile |
| fragment.count | The number of split FlowFiles generated from the parent FlowFile |
| segment.original.filename | The filename of the parent FlowFile |

Expand

Show lessSee more
