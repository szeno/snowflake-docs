# XMLRecordSetWriter

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Writes a RecordSet to XML. The records are wrapped by a root tag.

## Tags

record, recordset, resultset, row, serialize, writer, xml

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Character Set \* | Character Set | UTF-8 |  | The Character set to use when writing the data to the FlowFile |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
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
| Array Tag Name | array\_tag\_name |  |  | Name of the tag used by property “Wrap Elements of Arrays” to write arrays |
| Wrap Elements of Arrays \* | array\_wrapping | no-wrapping | - Use Property as Wrapper - Use Property for Elements - No Wrapping | Specifies how the writer wraps elements of fields of type array |
| Omit XML Declaration \* | omit\_xml\_declaration | false | - true - false | Specifies whether or not to include XML declaration |
| Pretty Print XML \* | pretty\_print\_xml | false | - true - false | Specifies whether or not the XML should be pretty printed |
| Name of Record Tag | record\_tag\_name |  |  | Specifies the name of the XML record tag wrapping the record fields. If this is not set, the writer will use the record name in the schema. |
| Name of Root Tag | root\_tag\_name |  |  | Specifies the name of the XML root tag wrapping the record set. This property has to be defined if the writer is supposed to write multiple records in a single FlowFile. |
| Suppress Null Values \* | suppress\_nulls | never-suppress | - Never Suppress - Always Suppress - Suppress Missing Values | Specifies how the writer should handle a null field |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
