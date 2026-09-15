# CEFReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Parses CEF (Common Event Format) events, returning each row as a record. This reader allows for inferring a schema based on the first event in the FlowFile or providing an explicit schema for interpreting the values.

## Tags

cef, parser, reader, record

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Schema Access Strategy \* | Schema Access Strategy | infer-schema | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader - Infer Schema | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Accept empty extensions \* | accept-empty-extensions | false | - true - false | If set to true, empty extensions will be accepted and will be associated to a null value. |
| DateTime Locale \* | datetime-representation | en-US |  | The IETF BCP 47 representation of the Locale to be used when parsing date fields with long or short month names (e.g. may <en-US> vs. mai. <fr-FR>. The defaultvalue is generally safe. Only change if having issues parsing CEF messages |
| Inference Strategy \* | inference-strategy | custom-extensions-inferred | - Headers only - Headers and extensions - With custom extensions as strings - With custom extensions inferred | Defines the set of fields should be included in the schema and the way the fields are being interpreted. |
| Invalid Field | invalid-message-field |  |  | Used when a line in the FlowFile cannot be parsed by the CEF parser. If set, instead of failing to process the FlowFile, a record is being added with one field. This record contains one field with the name specified by the property and the raw message as value. |
| Raw Message Field | raw-message-field |  |  | If set the raw message will be added to the record using the property value as field name. This is not the same as the “rawEvent” extension field! |
| Schema Inference Cache | schema-inference-cache |  |  | Specifies a Schema Cache to use when inferring the schema. If not populated, the schema will be inferred each time. However, if a cache is specified, the cache will first be consulted and if the applicable schema can be found, it will be used instead of inferring the schema. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
