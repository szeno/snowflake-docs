# ExtractAvroMetadata 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-avro-nar

## Description

Extracts metadata from the header of an Avro datafile.

## Tags

avro, metadata, schema

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Count Items | If true the number of items in the datafile will be counted and stored in a FlowFile attribute ‘item.count’. The counting is done by reading blocks and getting the number of items for each block, thus avoiding de-serializing. The items being counted will be the top-level items in the datafile. For example, with a schema of type record the items will be the records, and for a schema of type Array the items will be the arrays (not the number of entries in each array). |
| Fingerprint Algorithm | The algorithm used to generate the schema fingerprint. Available choices are based on the Avro recommended practices for fingerprint generation. |
| Metadata Keys | A comma-separated list of keys indicating key/value pairs to extract from the Avro file header. The key ‘avro.schema’ can be used to extract the full schema in JSON format, and ‘avro.codec’ can be used to extract the codec name if one exists. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if it cannot be parsed as Avro or metadata cannot be extracted for any reason |
| success | A FlowFile is routed to this relationship after metadata has been extracted. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| schema.type | The type of the schema (i.e. record, enum, etc.). |
| schema.name | Contains the name when the type is a record, enum or fixed, otherwise contains the name of the primitive type. |
| schema.fingerprint | The result of the Fingerprint Algorithm as a Hex string. |
| item.count | The total number of items in the datafile, only written if Count Items is set to true. |

Expand

Show lessSee more
