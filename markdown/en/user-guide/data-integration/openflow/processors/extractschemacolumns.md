# ExtractSchemaColumns 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-record-schema-nar

## Description

Extracts the record schema columns from the FlowFile using the supplied Record Reader and writes it to the *schema.columns* attribute.

## Tags

avro, csv, freeform, generic, json, record, schema, text, xml

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| End Column Index | Specifies index of the column in schema to which columns should be taken. |
| Record Reader | Specifies the Controller Service to use for reading incoming data |
| Start Column Index | Specifies index of the column (numbered from 1) in schema from which columns should be taken. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile’s record schema cannot be extracted from the configured input format, the FlowFile will be routed to this relationship |
| success | FlowFiles whose record schemas are successfully extracted will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.error.message | This attribute provides on failure the error message encountered by the Reader. |
| schema.columns | This attribute provides columns extracted from the input FlowFile using the provided RecordReader. |

Expand

Show lessSee more
