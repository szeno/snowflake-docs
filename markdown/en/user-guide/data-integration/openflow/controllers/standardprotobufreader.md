# StandardProtobufReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Parses Protocol Buffers messages from binary format into NiFi Records. Supports multiple schema access strategies including inline schema text, schema registry lookup, and schema reference readers. Protobuf reader needs to know the Proto schema message name in order to deserialize the binary payload correctly. The name of this message can be determined statically using ‘Message Name’ property, or dynamically, using a Message Name Resolver service.

## Tags

parser, protobuf, reader, record

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Message Name \* | Message Name |  |  | Fully qualified name of the Protocol Buffers message including its package (eg. mypackage.MyMessage). |
| Message Name Resolution Strategy \* | Message Name Resolution Strategy | MESSAGE\_NAME\_PROPERTY | - Message Name Property - Message Name Resolver | Strategy for determining the Protocol Buffers message name for processing |
| Message Name Resolver \* | Message Name Resolver |  |  | Service that dynamically resolves Protocol Buffer message names from FlowFile content or attributes |
| Schema Access Strategy \* | Schema Access Strategy | schema-name | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text \* | Schema Text | ${proto.schema} |  | The text of a Proto 3 formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
