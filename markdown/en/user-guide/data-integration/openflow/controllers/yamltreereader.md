# YamlTreeReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Parses YAML into individual Record objects. While the reader expects each record to be well-formed YAML, the content of a FlowFile may consist of many records, each as a well-formed YAML array or YAML object. If an array is encountered, each element in that array will be treated as a separate record. If the schema that is configured contains a field that is not present in the YAML, a null value will be used. If the YAML contains a field that is not present in the schema, that field will be skipped. Please note this controller service does not support resolving the use of YAML aliases. Any alias present will be treated as a string. See the Usage of the Controller Service for more information and examples.

## Tags

parser, reader, record, tree, yaml

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Allow Comments \* | Allow Comments | false | - true - false | Whether to allow comments when parsing the YAML document |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Max String Length \* | Max String Length | 20 MB |  | The maximum allowed length of a string value when parsing the YAML document |
| Schema Access Strategy \* | Schema Access Strategy | infer-schema | - Infer Schema - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Time Format | Time Format |  |  | Specifies the format to use when reading/writing Time fields. If not specified, Time fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, HH:mm:ss for a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 18:04:15). |
| Timestamp Format | Timestamp Format |  |  | Specifies the format to use when reading/writing Timestamp fields. If not specified, Timestamp fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy HH:mm:ss for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters; and then followed by a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 01/01/2017 18:04:15). |
| Schema Application Strategy \* | schema-application-strategy | SELECTED\_PART | - Whole JSON - Selected Part | Specifies whether the schema is defined for the whole JSON or for the selected part starting from “Starting Field Name”. |
| Schema Inference Cache | schema-inference-cache |  |  | Specifies a Schema Cache to use when inferring the schema. If not populated, the schema will be inferred each time. However, if a cache is specified, the cache will first be consulted and if the applicable schema can be found, it will be used instead of inferring the schema. |
| Starting Field Name | starting-field-name |  |  | Skips forward to the given nested field (array or object) to begin processing. |
| Starting Field Strategy \* | starting-field-strategy | ROOT\_NODE | - Root Node - Nested Field | Start processing from the root node or from a specified nested node. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
