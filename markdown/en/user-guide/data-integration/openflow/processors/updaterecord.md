# UpdateRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Updates the contents of a FlowFile that contains Record-oriented data (i.e., data that can be read via a RecordReader and written by a RecordWriter). This Processor requires that at least one user-defined Property be added. The name of the Property should indicate a RecordPath that determines the field that should be updated. The value of the Property is either a replacement value (optionally making use of the Expression Language) or is itself a RecordPath that extracts a value from the Record. Whether the Property value is determined to be a RecordPath or a literal value depends on the configuration of the <Replacement Value Strategy> Property.

## Tags

avro, csv, freeform, generic, json, log, logs, record, schema, text, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Record Reader | Specifies the Controller Service to use for reading incoming data |
| Record Writer | Specifies the Controller Service to use for writing out the records |
| Replacement Value Strategy | Specifies how to interpret the configured replacement values |

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
| record.index | This attribute provides the current row index and is only available inside the literal value expression. |
| record.error.message | This attribute provides on failure the error message encountered by the Reader or Writer. |

Expand

Show lessSee more

## Use cases

| Combine multiple fields into a single field. |
| --- |
| Change the value of a record field to an explicit value. |
| Copy the value of one record field to another record field. |
| Enrich data by injecting the value of an attribute into each Record. |
| Change the format of a record field’s value. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ConvertRecord](/user-guide/data-integration/openflow/processors/convertrecord)
