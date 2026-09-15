# RemoveRecordField 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Modifies the contents of a FlowFile that contains Record-oriented data (i.e. data that can be read via a RecordReader and written by a RecordWriter) by removing selected fields. This Processor requires that at least one user-defined Property be added. The name of the property is ignored by the processor, but could be a meaningful identifier for the user. The value of the property should indicate a RecordPath that determines the field to be removed. The processor executes the removal in the order in which these properties are added to the processor. Set the “Record Writer” to “Inherit Record Schema” in order to use the updated Record Schema modified when removing Fields.

## Tags

avro, csv, delete, freeform, generic, json, record, remove, schema, text, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Record Reader | Specifies the Controller Service to use for reading incoming data |
| Record Writer | Specifies the Controller Service to use for writing out the records |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile cannot be transformed from the configured input format to the configured output format, the unchanged FlowFile will be routed to this relationship |
| success | FlowFiles that are successfully transformed will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.error.message | This attribute provides on failure the error message encountered by the Reader or Writer. |

Expand

Show lessSee more

## Use cases

| Remove one or more fields from a Record, where the names of the fields to remove are known. |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.UpdateRecord](/user-guide/data-integration/openflow/processors/updaterecord)
