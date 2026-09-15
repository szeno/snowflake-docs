# CSVRecordSetWriter

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Writes the contents of a RecordSet as CSV data. The first line written will be the column names (unless the ‘Include Header Line’ property is false). All subsequent lines will be the values corresponding to the record fields.

## Tags

csv, delimited, record, recordset, result, row, separated, serializer, set, tab, tsv, writer

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| CSV Format \* | CSV Format | custom | - Custom Format - RFC 4180 - Microsoft Excel - Tab-Delimited - MySQL Format - Informix Unload - Informix Unload Escape Disabled | Specifies which “format” the CSV data is in, or specifies if custom formatting should be used. |
| Character Set \* | Character Set | UTF-8 |  | The Character Encoding that is used to encode/decode the CSV file |
| Comment Marker | Comment Marker |  |  | The character that is used to denote the start of a comment. Any line that begins with this comment will be ignored. |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Escape Character \* | Escape Character |  |  | The character that is used to escape characters that would otherwise have a specific meaning to the CSV Parser. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Escape Character at runtime, then it will be skipped and the default Escape Character will be used. Setting it to an empty string means no escape character should be used. |
| Include Header Line \* | Include Header Line | true | - true - false | Specifies whether or not the CSV column names should be written out as the first line. |
| Include Trailing Delimiter \* | Include Trailing Delimiter | false | - true - false | If true, a trailing delimiter will be added to each CSV Record that is written. If false, the trailing delimiter will be omitted. |
| Null String | Null String |  |  | Specifies a String that, if present as a value in the CSV, should be considered a null field instead of using the literal value. |
| Quote Character \* | Quote Character | “ |  | The character that is used to quote values so that escape characters do not have to be used. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Quote Character at runtime, then it will be skipped and the default Quote Character will be used. |
| Quote Mode \* | Quote Mode | MINIMAL | - Quote All Values - Quote Minimal - Quote Non-Numeric Values - Do Not Quote Values | Specifies how fields should be quoted when they are written |
| Record Separator \* | Record Separator | n |  | Specifies the characters to use in order to separate CSV Records |
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
| Trim Fields \* | Trim Fields | true | - true - false | Whether or not white space should be removed from the beginning and end of fields |
| Value Separator \* | Value Separator | , |  | The character that is used to separate values/fields in a CSV Record. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Value Separator at runtime, then it will be skipped and the default Value Separator will be used. |
| CSV Writer \* | csv-writer | commons-csv | - Apache Commons CSV - FastCSV | Specifies which writer implementation to use to write CSV records. NOTE: Different writers may support different subsets of functionality and may also exhibit different levels of performance. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
