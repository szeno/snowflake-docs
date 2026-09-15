# ForkRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor allows the user to fork a record into multiple records. The user must specify at least one Record Path, as a dynamic property, pointing to a field of type ARRAY containing RECORD objects. The processor accepts two modes: ‘split’ and ‘extract’. In both modes, there is one record generated per element contained in the designated array. In the ‘split’ mode, each generated record will preserve the same schema as given in the input but the array will contain only one element. In the ‘extract’ mode, the element of the array must be of record type and will be the generated record. Additionally, in the ‘extract’ mode, it is possible to specify if each generated record should contain all the fields of the parent records from the root level to the extracted record. This assumes that the fields to add in the record are defined in the schema of the Record Writer controller service. See examples in the additional details documentation of this processor.

## Tags

array, content, event, fork, record, stream

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| fork-mode | Specifies the forking mode of the processor |
| include-parent-fields | This parameter is only valid with the ‘extract’ mode. If set to true, all the fields from the root level to the given array will be added as fields of each element of the array to fork. |
| record-reader | Specifies the Controller Service to use for reading incoming data |
| record-writer | Specifies the Controller Service to use for writing out the records |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | In case a FlowFile generates an error during the fork operation, it will be routed to this relationship |
| fork | The FlowFiles containing the forked records will be routed to this relationship |
| original | The original FlowFiles will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The generated FlowFile will have a ‘record.count’ attribute indicating the number of records that were written to the FlowFile. |
| mime.type | The MIME Type indicated by the Record Writer |
| <Attributes from Record Writer> | Any Attribute that the configured Record Writer returns will be added to the FlowFile. |

Expand

Show lessSee more
