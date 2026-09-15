# JsonRecordSetWriter

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Writes the results of a RecordSet as either a JSON Array or one JSON object per line. If using Array output, then even if the RecordSet consists of a single row, it will be written as an array with a single element. If using One Line Per Object output, the JSON objects cannot be pretty-printed.

## Tags

json, record, recordset, resultset, row, serialize, writer

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Allow Scientific Notation \* | Allow Scientific Notation | false | - true - false | Specifies whether or not scientific notation should be used when writing numbers |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Pretty Print JSON \* | Pretty Print JSON | false | - true - false | Specifies whether or not the JSON should be pretty printed |
| Schema Access Strategy \* | Schema Access Strategy | inherit-record-schema | - Inherit Record Schema - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Cache | Schema Cache |  |  | Specifies a Schema Cache to add the Record Schema to so that Record Readers can quickly lookup the schema. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Reference Writer \* | Schema Reference Writer |  |  | Service implementation responsible for writing FlowFile attributes or content header with Schema reference information |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Schema Write Strategy \* | Schema Write Strategy | no-schema | - Do Not Write Schema - Set ‘schema.name’ Attribute - Set ‘avro.schema’ Attribute - Schema Reference Writer | Specifies how the schema for a Record should be added to the data. |
| Time Format | Time Format |  |  | Specifies the format to use when reading/writing Time fields. If not specified, Time fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, HH:mm:ss for a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 18:04:15). |
| Timestamp Format | Timestamp Format |  |  | Specifies the format to use when reading/writing Timestamp fields. If not specified, Timestamp fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy HH:mm:ss for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters; and then followed by a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 01/01/2017 18:04:15). |
| Compression Format \* | compression-format | none | - none - gzip - bzip2 - xz-lzma2 - snappy - snappy framed - zstd | The compression format to use. Valid values are: GZIP, BZIP2, ZSTD, XZ-LZMA2, LZMA, Snappy, and Snappy Framed |
| Compression Level \* | compression-level | 1 | - 0 - 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 | The compression level to use; this is valid only when using GZIP compression. A lower value results in faster processing but less compression; a value of 0 indicates no compression but simply archiving |
| Output Grouping \* | output-grouping | output-array | - Array - One Line Per Object | Specifies how the writer should output the JSON records (as an array or one object per line, e.g.) Note that if ‘One Line Per Object’ is selected, then Pretty Print JSON must be false. |
| Suppress Null Values \* | suppress-nulls | never-suppress | - Never Suppress - Always Suppress - Suppress Missing Values | Specifies how the writer should handle a null field |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
