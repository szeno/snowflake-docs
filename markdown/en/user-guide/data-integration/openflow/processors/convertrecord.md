# ConvertRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Converts records from one data format to another using configured Record Reader and Record Write Controller Services. The Reader and Writer must be configured with “matching” schemas. By this, we mean the schemas must have the same field names. The types of the fields do not have to be the same if a field value can be coerced from one type to another. For instance, if the input schema has a field named “balance” of type double, the output schema can have a field named “balance” with a type of string, double, or float. If any field is present in the input that is not present in the output, the field will be left out of the output. If any field is specified in the output schema but is not present in the input data/schema, then the field will not be present in the output or will have a null value, depending on the writer.

## Tags

avro, convert, csv, freeform, generic, json, log, logs, record, schema, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Include Zero Record FlowFiles | When converting an incoming FlowFile, if the conversion results in no data, this property specifies whether or not a FlowFile will be sent to the corresponding relationship |
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
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records in the FlowFile |
| record.error.message | This attribute provides on failure the error message encountered by the Reader or Writer. |

Expand

Show lessSee more

## Use cases

| Convert data from one record-oriented format to another |
| --- |

Expand

Show lessSee more
