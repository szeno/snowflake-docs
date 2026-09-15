# ExtractRecordSchema 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Extracts the record schema from the FlowFile using the supplied Record Reader and writes it to the *avro.schema* attribute.

## Tags

avro, csv, freeform, generic, json, record, schema, text, xml

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| cache-size | Specifies the number of schemas to cache. This value should reflect the expected number of different schemas that may be in the incoming FlowFiles. This ensures more efficient retrieval of the schemas and thus the processor performance. |
| record-reader | Specifies the Controller Service to use for reading incoming data |

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
| avro.schema | This attribute provides the schema extracted from the input FlowFile using the provided RecordReader. |

Expand

Show lessSee more
