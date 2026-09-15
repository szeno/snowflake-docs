# JsonPathReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Parses JSON records and evaluates user-defined JSON Path ‘s against each JSON object. While the reader expects each record to be well-formed JSON, the content of a FlowFile may consist of many records, each as a well-formed JSON array or JSON object with optional whitespace between them, such as the common’JSON-per-line’ format. If an array is encountered, each element in that array will be treated as a separate record. User-defined properties define the fields that should be extracted from the JSON in order to form the fields of a Record. Any JSON field that is not extracted via a JSONPath will not be returned in the JSON Records.

## Tags

json, jsonpath, parser, reader, record

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Allow Comments \* | Allow Comments | false | - true - false | Whether to allow comments when parsing the JSON document |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Max String Length \* | Max String Length | 20 MB |  | The maximum allowed length of a string value when parsing the JSON document |
| Schema Access Strategy \* | Schema Access Strategy | infer-schema | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader - Infer Schema | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Time Format | Time Format |  |  | Specifies the format to use when reading/writing Time fields. If not specified, Time fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, HH:mm:ss for a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 18:04:15). |
| Timestamp Format | Timestamp Format |  |  | Specifies the format to use when reading/writing Timestamp fields. If not specified, Timestamp fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy HH:mm:ss for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters; and then followed by a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 01/01/2017 18:04:15). |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
