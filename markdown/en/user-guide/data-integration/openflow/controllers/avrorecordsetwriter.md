# AvroRecordSetWriter

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Writes the contents of a RecordSet in Binary Avro format.

## Tags

avro, record, recordset, result, row, serializer, set, writer

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Schema Access Strategy \* | Schema Access Strategy | inherit-record-schema | - Inherit Record Schema - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Cache | Schema Cache |  |  | Specifies a Schema Cache to add the Record Schema to so that Record Readers can quickly lookup the schema. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Reference Writer \* | Schema Reference Writer |  |  | Service implementation responsible for writing FlowFile attributes or content header with Schema reference information |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Schema Write Strategy \* | Schema Write Strategy | avro-embedded | - Embed Avro Schema - Do Not Write Schema - Set ‘schema.name’ Attribute - Set ‘avro.schema’ Attribute - Schema Reference Writer | Specifies how the schema for a Record should be added to the data. |
| Cache Size \* | cache-size | 1000 |  | Specifies how many Schemas should be cached |
| Compression Format \* | compression-format | NONE | - BZIP2 - DEFLATE - NONE - SNAPPY - LZO | Compression type to use when writing Avro files. Default is None. |
| Encoder Pool Size \* | encoder-pool-size | 32 |  | Avro Writers require the use of an Encoder. Creation of Encoders is expensive, but once created, they can be reused. This property controls the maximum number of Encoders that can be pooled and reused. Setting this value too small can result in degraded performance, but setting it higher can result in more heap being used. This property is ignored if the Avro Writer is configured with a Schema Write Strategy of ‘Embed Avro Schema’. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
