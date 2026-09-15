# SplitAvro 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-avro-nar

## Description

Splits a binary encoded Avro datafile into smaller files based on the configured Output Size. The Output Strategy determines if the smaller files will be Avro datafiles, or bare Avro records with metadata in the FlowFile attributes. The output will always be binary encoded.

## Tags

avro, split

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Output Size | The number of Avro records to include per split file. In cases where the incoming file has less records than the Output Size, or when the total number of records does not divide evenly by the Output Size, it is possible to get a split file with less records. |
| Output Strategy | Determines the format of the output. Either Avro Datafile, or bare record. Bare record output is only intended for use with systems that already require it, and shouldn’t be needed for normal use. |
| Split Strategy | The strategy for splitting the incoming datafile. The Record strategy will read the incoming datafile by de-serializing each record. |
| Transfer Metadata | Whether or not to transfer metadata from the parent datafile to the children. If the Output Strategy is Bare Record, then the metadata will be stored as FlowFile attributes, otherwise it will be in the Datafile header. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, the FlowFile is not valid Avro), it will be routed to this relationship |
| original | The original FlowFile that was split. If the FlowFile fails processing, nothing will be sent to this relationship |
| split | All new files split from the original FlowFile will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| fragment.identifier | All split FlowFiles produced from the same parent FlowFile will have the same randomly generated UUID added for this attribute |
| fragment.index | A one-up number that indicates the ordering of the split FlowFiles that were created from a single parent FlowFile |
| fragment.count | The number of split FlowFiles generated from the parent FlowFile |
| segment.original.filename | The filename of the parent FlowFile |

Expand

Show lessSee more
